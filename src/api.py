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

	@staticmethod
	def setDefaultConfig(config):
		lib.UA_ClientConfig_setDefault(config)

#class Variant:
#	def __init__(self):
#		self.variant = None
#		lib.UA_Variant_init(self.variant)

#class UaServer:
#	def __init__(self):
#		self.ua_client = lib.UA_Server_new()
