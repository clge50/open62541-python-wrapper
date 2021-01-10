import sys
sys.path.append("../src/")
import api

uaClient = api.UaClient()
api.UaClient.setDefaultConfig(uaClient.getConfig())
retval = uaClient.connect(b"opc.tcp://127.0.0.1:16664")
if retval != 0:
	print("something went wrong")
