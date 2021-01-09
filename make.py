from cffi import FFI
import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))


def setupOpen62541():
	open62541Repo = r"https://github.com/open62541/open62541.git"

	os.chdir(dirname)
	os.system("git clone " + open62541Repo)
	os.system("mkdir ./open62541/build")
	os.chdir(dirname + r"/open62541/build")
	os.system("cmake .. -DUA_ENABLE_AMALGAMATION=TRUE")
	os.system("make")

def generateIntermediateApi():
	ffibuilder = FFI()
	ffibuilder.set_source("_intermediateApi",
		r"""#include "open62541.h" """,
		include_dirs=[dirname + r"/open62541/build"],
		library_dirs=[dirname + r"/open62541/build/bin"],
		libraries=['open62541'])

	ffibuilder.cdef("""
		typedef struct UA_Client UA_Client;
		typedef uint32_t UA_StatusCode;
		typedef struct UA_ClientConfig UA_ClientConfig;
		UA_Client *UA_Client_new(void);
		UA_StatusCode UA_ClientConfig_setDefault(UA_ClientConfig *config);
		UA_ClientConfig *UA_Client_getConfig(UA_Client *client);
		UA_StatusCode UA_Client_connect(UA_Client *client, const char *endpointUrl);
		""")
	os.chdir(dirname + r"/src")
	ffibuilder.compile(verbose=True)
	print("finished building generateIntermediateApi")

setupOpen62541()
os.chdir(dirname)
generateIntermediateApi()