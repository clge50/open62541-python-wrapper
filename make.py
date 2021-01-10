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
	ffibuilder.set_source("intermediateApi",
		r"""#include "open62541.h"
		#define UA_STATUSCODE_GOOD 0x00 
		#define UA_NS0ID_SERVER_SERVERSTATUS_CURRENTTIME 2258 
		#define UA_TYPES_COUNT 190
		#define UA_TYPES_DATETIME 12
		""",
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

		typedef uint16_t UA_UInt16;
		typedef uint32_t UA_UInt32;

		struct UA_DataType {...;};
		typedef struct UA_DataType UA_DataType;
		const UA_DataType UA_TYPES[190];
		#define UA_TYPES_DATETIME 12

		typedef bool UA_Boolean;
		typedef int64_t UA_DateTime;


		typedef struct { void *data;                   /* Points to the scalar or array data */
		...;} UA_Variant;
		void UA_Variant_init(UA_Variant *p);
		UA_Boolean UA_Variant_hasScalarType(const UA_Variant *v, const UA_DataType *type);

		typedef struct {...;} UA_NodeId;
		UA_NodeId UA_NODEID_NUMERIC(UA_UInt16 nsIndex, UA_UInt32 identifier);
		UA_StatusCode UA_Client_readValueAttribute(UA_Client *client, const UA_NodeId nodeId, UA_Variant *outValue);


typedef enum {
    UA_LOGCATEGORY_NETWORK = 0,
    UA_LOGCATEGORY_SECURECHANNEL,
    UA_LOGCATEGORY_SESSION,
    UA_LOGCATEGORY_SERVER,
    UA_LOGCATEGORY_CLIENT,
    UA_LOGCATEGORY_USERLAND,
    UA_LOGCATEGORY_SECURITYPOLICY
} UA_LogCategory;


typedef struct {...;} UA_Logger;

		typedef struct UA_DateTimeStruct {
    UA_UInt16 nanoSec;
    UA_UInt16 microSec;
    UA_UInt16 milliSec;
    UA_UInt16 sec;
    UA_UInt16 min;
    UA_UInt16 hour;
    UA_UInt16 day;   /* From 1 to 31 */
    UA_UInt16 month; /* From 1 to 12 */
    UA_UInt16 year;
} UA_DateTimeStruct;


		UA_Logger *UA_Log_Stdout;
		UA_DateTimeStruct UA_DateTime_toStruct(UA_DateTime t);

		#define UA_STATUSCODE_GOOD 0x00
		#define UA_NS0ID_SERVER_SERVERSTATUS_CURRENTTIME 2258

		void UA_LOG_INFO(const UA_Logger *logger, UA_LogCategory category, const char *msg, ...);

		""")
	os.system("mkdir build")
	os.chdir(dirname + r"/build")
	ffibuilder.compile(verbose=True)
	print("finished building generateIntermediateApi")

setupOpen62541()
os.chdir(dirname)
generateIntermediateApi()
