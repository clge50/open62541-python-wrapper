import sys
sys.path.append("../build/")
from intermediateApi import ffi, lib

class UaClient:
	def __init__(self):
		self.ua_client = lib.UA_Client_new()

	def getConfig(self):
		return lib.UA_Client_getConfig(self.ua_client)

	def connect(self, address):
		return lib.UA_Client_connect(self.ua_client, address)

	def readValueAttribute(self, nodeId, value):
		return lib.UA_Client_readValueAttribute(self.ua_client, nodeId, value.value)

	@staticmethod
	def setDefaultConfig(config):
		lib.UA_ClientConfig_setDefault(config)

class Variant:
	def __init__(self):
		self.value = ffi.new("UA_Variant*")
		lib.UA_Variant_init(self.value)

	def hasScalarType(self, dataType):
		return lib.UA_Variant_hasScalarType(self.value, dataType)

class StatusCode:
	@staticmethod
	def good():
		return lib.UA_STATUSCODE_GOOD

class DataType:
	@staticmethod
	def dateTime():
		return Utils.UA_TYPE(lib.UA_TYPES_DATETIME)

class Utils:
	@staticmethod
	def UA_TYPES():
		return lib.UA_TYPES

	@staticmethod
	def UA_TYPE(id):
		return ffi.new("UA_DataType*", lib.UA_TYPES[id])

	@staticmethod
	def nodeIdNumeric(namespaceIndex, id):
		return lib.UA_NODEID_NUMERIC(0, id)

	@staticmethod
	def serverStatusCurrentTimeId():
		return lib.UA_NS0ID_SERVER_SERVERSTATUS_CURRENTTIME

	@staticmethod
	def castToDateTime(variant):
		return ffi.cast("UA_DateTime", variant.value.data)

	@staticmethod
	def uaDateTimeToStruct(rawdate):
		return lib.UA_DateTime_toStruct(rawdate)

	@staticmethod
	def uint16(val):
		return ffi.cast("UA_UInt16", val)

class Log:
	@staticmethod
	def logStdout():
		return lib.UA_Log_Stdout

	@staticmethod
	def logCategoryUserland():
		return lib.UA_LOGCATEGORY_USERLAND

	@staticmethod
	def loginfo(channel, mode, str, *args):
		lib.UA_LOG_INFO(channel, mode, str, *args)


#class UaServer:
#	def __init__(self):
#		self.ua_client = lib.UA_Server_new()
