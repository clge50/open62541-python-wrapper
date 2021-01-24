import sys
sys.path.append("../../build/")
from intermediateApi import ffi, lib

client = lib.UA_Client_new()
lib.UA_ClientConfig_setDefault(lib.UA_Client_getConfig(client))
retval = lib.UA_Client_connect(client, b"opc.tcp://christian-ThinkPad:4840/")

if retval != lib.UA_STATUSCODE_GOOD:
	print("An error occurred. stopping client")
	quit()

value = ffi.new("UA_Variant*")
lib.UA_Variant_init(value)

dataType = ffi.new("UA_DataType*", lib.UA_TYPES[lib.UA_TYPES_DATETIME])
nodeId = lib.UA_NODEID_NUMERIC(0, lib.UA_NS0ID_SERVER_SERVERSTATUS_CURRENTTIME)
retval = lib.UA_Client_readValueAttribute(client, nodeId, value);

if retval == lib.UA_STATUSCODE_GOOD and False == lib.UA_Variant_hasScalarType(value, dataType):
	rawDate = ffi.cast("UA_DateTime", value.data)
	dts = lib.UA_DateTime_toStruct(rawDate);
	lib.UA_LOG_INFO(lib.UA_Log_Stdout, lib.UA_LOGCATEGORY_USERLAND, b"date is: %u-%u-%u %u:%u:%u.%03u\n",
		ffi.cast("UA_UInt16", dts.day), ffi.cast("UA_UInt16", dts.month), ffi.cast("UA_UInt16", dts.year), ffi.cast("UA_UInt16", dts.hour), 
		ffi.cast("UA_UInt16", dts.min), ffi.cast("UA_UInt16", dts.sec), ffi.cast("UA_UInt16", dts.milliSec));
