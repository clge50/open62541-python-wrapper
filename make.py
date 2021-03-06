# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import os
import os.path
from functools import reduce
from shutil import copytree, rmtree

from cffi import FFI

dirname = os.path.dirname(os.path.abspath(__file__))


def setup_open62541():
    # if not os.path.isdir(dirname + r"/open62541"):
    #     open62541_repo = r"https://github.com/open62541/open62541.git"
    #     os.chdir(dirname)
    #     os.system("git clone " + open62541_repo)

    # todo: currently we force version open62541-1.2 to ensure that a version is used for the amalgamated files that wrappy(o6) can work with
    # https://github.com/open62541/open62541/releases/tag/v1.2
    if not os.path.isdir(dirname + r"/open62541-1.2/build"):
        os.mkdir(dirname + r"/open62541-1.2/build")
        os.chdir(dirname + r"/open62541-1.2/build")
        os.system("cmake .. -DUA_ENABLE_AMALGAMATION=TRUE")
        os.system("make")
        os.chdir(dirname)


# todo: create a generic generate function instead of multiple functions that do basically the same
def generate_status_codes():
    with open(dirname + r"/open62541-1.2/build/src_generated/open62541/statuscodes.h") as file_handler:
        lines = (line.rstrip() for line in file_handler)
        lines = (line.replace("#define ", "") for line in lines if line.startswith("#define"))
        lines = list(map(lambda l: "\t" + l.split()[0].replace("UA_STATUSCODE_", "") +
                                   " = UaStatusCode(" + l.split()[1] + ")\n", lines))
        lines.insert(0, "from ua_types_primitive import UaStatusCode\n\n\n")
        lines.insert(1, "class UA_STATUSCODES:\n")

    os.chdir(dirname + r"/build/wrappy_o6/")
    with open('ua_consts_status_codes.py', 'w+') as file:
        file.writelines(lines)


def generate_node_ids():
    with open(dirname + r"/open62541-1.2/build/src_generated/open62541/nodeids.h") as file_handler:
        lines = (line.rstrip() for line in file_handler)
        lines = (line.replace("#define ", "") for line in lines if
                 line.startswith("#define") and "#define UA_NODEIDS_NS0_H_" not in line)
        lines = list(map(lambda l: "\t" + l.split()[0].replace("UA_NS0ID_", "") +
                                   " = UaNodeId(0, " + l.split()[1] + ")\n", lines))
        lines.insert(0, "class UA_NS0ID:\n")
        lines.insert(0, "from ua_types_base import UaNodeId\n")
        lines.insert(1, "\n")
        lines.insert(1, "\n")

    os.chdir(dirname + r"/build/wrappy_o6/")
    with open('ua_consts_ns0ids.py', 'w+') as file:
        file.writelines(lines)


def generate_data_types():
    with open(dirname + r"/open62541-1.2/build/src_generated/open62541/types_generated.h") as file_handler:
        lines = (line.rstrip() for line in file_handler)
        lines = (line.replace("#define ", "") for line in lines if line.startswith("#define UA_TYPES_"))
        lines = list(map(lambda l: "\t" + l.split()[0].split("_")[2] + " = UaDataType(val=lib.UA_TYPES[" +
                                   l.split()[1] + "])\n", lines))
        count = lines.pop(0)
        lines.insert(0, count.replace("UaDataType(val=lib.UA_TYPES[", "").replace("])", ""))
        lines.insert(0, "class UA_TYPES:\n")
        lines.insert(0, "from ua_types_base import UaDataType\n")
        lines.insert(0, "from intermediateApi import ffi, lib\n")
        lines.insert(2, "\n")
        lines.insert(2, "\n")

    os.chdir(dirname + r"/build/wrappy_o6/")
    with open('ua_consts_data_types.py', 'w+') as file:
        file.writelines(lines)


def generate_type_ids():
    with open(dirname + r"/open62541-1.2/build/src_generated/open62541/types_generated.h") as file_handler:
        lines = (line.rstrip() for line in file_handler)
        lines = (line.replace("#define ", "") for line in lines if line.startswith("#define UA_TYPES_"))
        lines = list(map(lambda l: "\t_" + l.split()[0].split("_")[2] + " = lib.UA_TYPES[" +
                                   l.split()[1] + "]\n", lines))
        lines.pop(0)
        lines.insert(0, "class _UA_TYPES:\n")
        lines.insert(0, "from intermediateApi import ffi, lib\n")
        lines.insert(1, "\n")
        lines.insert(1, "\n")

    os.chdir(dirname + r"/build/wrappy_o6/")
    with open('ua_consts_types_raw.py', 'w+') as file:
        file.writelines(lines)


def generate_api():
    os.chdir(dirname)
    if os.path.isdir(dirname + "/build"):
        rmtree("build")
    decl_files_list = ["c_basics",
                       "aa_tree",
                       "common",
                       "types",
                       "types_generated",
                       "util",
                       "log",
                       "network",
                       "client",
                       "client_highlevel",
                       "client_highlevel_async",
                       "client_config_default",
                       "accesscontrol",
                       "securitypolicy",
                       "pki",
                       "nodestore",
                       "session",
                       "server",
                       "server_config_default",
                       "client_subscription",
                       "statuscodes"]
    decls_list = []

    for file_name in decl_files_list:
        with open(dirname + r"/src/definitions/" + file_name) as file_handler:
            decls_list.append(file_handler.read())

    decls_list.append("void pseudoFree(void *ptr);")
    cffi_input = reduce(lambda s1, s2: s1 + "\n" + s2, decls_list)

    ffi_builder = FFI()
    ffi_builder.set_source("intermediateApi",
                           r"""#include "open62541.h"
                           
                           struct ContinuationPoint;
                            typedef struct ContinuationPoint ContinuationPoint;
                            struct ContinuationPoint {
                                ContinuationPoint *next;
                                UA_ByteString identifier;
                            
                                /* Parameters of the Browse Request */
                                UA_BrowseDescription browseDescription;
                                UA_UInt32 maxReferences;
                                UA_ReferenceTypeSet relevantReferences;
                            
                                /* The next target to be transmitted to the client */
                                UA_ExpandedNodeId nextTarget;
                                UA_Byte nextRefKindIndex;
                            };
                            
                            typedef struct UA_SessionHeader {
                                struct {
                                    struct UA_SessionHeader *sle_next;
                                } next;
                                UA_NodeId authenticationToken;
                                UA_SecureChannel *channel; /* The pointer back to the SecureChannel in the session. */
                            } UA_SessionHeader;
                            
                            typedef struct {
                                UA_SessionHeader  header;
                                UA_ApplicationDescription clientDescription;
                                UA_String         sessionName;
                                UA_Boolean        activated;
                                void             *sessionHandle; /* pointer assigned in userland-callback */
                                UA_NodeId         sessionId;
                                UA_UInt32         maxRequestMessageSize;
                                UA_UInt32         maxResponseMessageSize;
                                UA_Double         timeout; /* in ms */
                                UA_DateTime       validTill;
                                UA_ByteString     serverNonce;
                                UA_UInt16         availableContinuationPoints;
                                ContinuationPoint *continuationPoints;
                                #ifdef UA_ENABLE_SUBSCRIPTIONS
                                    size_t subscriptionsSize;
                                    struct {
                                        struct UA_Subscription *tqh_first;	
                                        struct UA_Subscription **tqh_last;
                                    };
                                    struct {
                                        struct UA_PublishResponseEntry *sqh_first;
                                        struct UA_PublishResponseEntry **sqh_last;
                                    };
                                    UA_UInt32 numPublishReq;
                                    size_t totalRetransmissionQueueSize; /* Retransmissions of all subscriptions */
                                #endif
                            } UA_Session;
                           
                            void pseudoFree(void *ptr) {
                                printf("doing nothing\n");
                            }
                            
                            /*void setServerConfig(UA_Server server, UA_ServerConfig config) {
                                server.config = config;
                            }
                            
                            void setServerStartTime(UA_Server server, UA_DateTime startTime) {
                                server.startTime = startTime;
                            }
                            
                            void setServerEndTime(UA_Server server, UA_DateTime endTime) {
                                server.endTime = endTime;
                            }
                            
                            UA_ServerConfig getServerConfig(UA_Server server) {
                                return server.config;
                            }
                            
                            UA_DateTime getServerStartTime(UA_Server server) {
                                return server.startTime;
                            }
                            
                            UA_DateTime getServerEndTime(UA_Server server) {
                                return server.endTime;
                            }*/
                           
                           """,
                           include_dirs=[dirname + r"/open62541-1.2/build"],
                           library_dirs=[dirname + r"/open62541-1.2/build/bin"],
                           libraries=['open62541'])

    ffi_builder.cdef(cffi_input)
    # os.mkdir("build")
    copytree(dirname + r"/src/api", dirname + r"/build/wrappy_o6")
    os.chdir(dirname + r"/build/wrappy_o6/")
    ffi_builder.compile(verbose=True)
    os.remove("intermediateApi.c")
    os.remove("intermediateApi.o")
    print("finished building intermediateApi")


if __name__ == "__main__":
    setup_open62541()
    os.chdir(dirname)
    generate_api()
    generate_status_codes()
    generate_node_ids()
    generate_data_types()
    generate_type_ids()
