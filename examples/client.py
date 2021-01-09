from _intermediateApi import ffi, lib

client = lib.UA_Client_new()

lib.UA_ClientConfig_setDefault(lib.UA_Client_getConfig(client))

lib.UA_Client_connect(client, b"opc.tcp://127.0.0.1:16664")
