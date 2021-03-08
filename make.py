# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import os
import os.path
import re
from functools import reduce
from shutil import copytree, rmtree

from cffi import FFI

dirname = os.path.dirname(os.path.abspath(__file__))


def setup_open62541():
    if not os.path.isdir(dirname + r"/open62541"):
        open62541_repo = r"https://github.com/open62541/open62541.git"
        os.chdir(dirname)
        os.system("git clone " + open62541_repo)

    if not os.path.isdir(dirname + r"/open62541/build"):
        os.mkdir(dirname + r"/open62541/build")
        os.chdir(dirname + r"/open62541/build")
        os.system("cmake .. -DUA_ENABLE_AMALGAMATION=TRUE")
        os.system("make")
        os.chdir(dirname)


# todo: create a generic generate function instead of multiple functions that do basically the same
def generate_status_codes():
    with open(dirname + r"/open62541/build/src_generated/open62541/statuscodes.h") as file_handler:
        lines = (line.rstrip() for line in file_handler)
        lines = (line.replace("#define ", "") for line in lines if line.startswith("#define"))
        lines = list(map(lambda l: "\t" + l.split()[0] + " = " + l.split()[1] + "\n", lines))
        lines.insert(0, "from intermediateApi import lib\n\n\n")
        lines.insert(1, "class StatusCode:\n")
        lines.insert(2,
                     "\t@staticmethod\n\tdef isBad(status_code):\n\t\treturn lib.UA_StatusCode_isBad(status_code)\n\n")

    os.chdir(dirname + r"/build/open62541/")
    with open('status_code.py', 'w+') as file:
        file.writelines(lines)


def generate_node_ids():
    with open(dirname + r"/open62541/build/src_generated/open62541/nodeids.h") as file_handler:
        lines = (line.rstrip() for line in file_handler)
        lines = (line.replace("#define ", "") for line in lines if
                 line.startswith("#define") and "#define UA_NODEIDS_NS0_H_" not in line)
        lines = list(map(lambda l: "\t" + l.split()[0].replace("UA_NS0ID_", "") +
                                   " = UaNodeId(0, " + l.split()[1] + ")\n", lines))
        lines.insert(0, "class NS0ID:\n")
        lines.insert(0, "from ua_types import UaNodeId\n")
        lines.insert(1, "\n")
        lines.insert(1, "\n")

    os.chdir(dirname + r"/build/open62541/")
    with open('ua_ns0_node_ids.py', 'w+') as file:
        file.writelines(lines)


def generate_type_ids():
    with open(dirname + r"/open62541/build/src_generated/open62541/types_generated.h") as file_handler:
        lines = (line.rstrip() for line in file_handler)
        lines = (line.replace("#define ", "") for line in lines if line.startswith("#define UA_TYPES_"))
        lines = list(map(lambda l: "\t" + l.split()[0].split("_")[2] + " = UaDataType(val=lib.UA_TYPES[" +
                                   l.split()[1] + "])\n", lines))
        count = lines.pop(0)
        lines.insert(0, count.replace("UaDataType(val=lib.UA_TYPES[", "").replace("])", ""))
        lines.insert(0, "class TYPES:\n")
        lines.insert(0, "from ua_types import UaDataType\n")
        lines.insert(0, "from intermediateApi import ffi, lib\n")
        lines.insert(2, "\n")
        lines.insert(2, "\n")

    os.chdir(dirname + r"/build/open62541/")
    with open('ua_data_types.py', 'w+') as file:
        file.writelines(lines)


def generate_api():
    os.chdir(dirname)
    if os.path.isdir(dirname + "/build"):
        rmtree("build")
    decl_files_list = ["c_basics",
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
                       "nodestore",
                       "server"]
    decls_list = []

    for file_name in decl_files_list:
        with open(dirname + r"/src/definitions/" + file_name) as file_handler:
            decls_list.append(file_handler.read())

    decls_list.append("void pseudoFree(void *ptr);")
    cffi_input = reduce(lambda s1, s2: s1 + "\n" + s2, decls_list)

    ffi_builder = FFI()
    ffi_builder.set_source("intermediateApi",
                           r"""#include "open62541.h"
                           
                            void pseudoFree(void *ptr) {
                                printf("doing nothing\n");
                            }
                           
                           """,
                           include_dirs=[dirname + r"/open62541/build"],
                           library_dirs=[dirname + r"/open62541/build/bin"],
                           libraries=['open62541'])

    ffi_builder.cdef(cffi_input)
    # os.mkdir("build")
    copytree(dirname + r"/src/api", dirname + r"/build/open62541")
    os.chdir(dirname + r"/build/open62541/")
    ffi_builder.compile(verbose=True)
    os.remove("intermediateApi.c")
    os.remove("intermediateApi.o")
    print("finished building intermediateApi")


def generate_pdoc():
    os.chdir(dirname + r"/build/open62541")
    os.system("pdoc3 --html --output-dir " + dirname + "/doc " + dirname + r"/build/open62541 --force")


if __name__ == "__main__":
    setup_open62541()
    os.chdir(dirname)
    generate_api()
    generate_status_codes()
    generate_node_ids()
    generate_type_ids()
    generate_pdoc()
