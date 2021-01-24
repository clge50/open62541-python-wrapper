import sys
sys.path.append("../build/api")
import clientApi

client = clientApi.UaClient()
retval = client.connect(b"opc.tcp://christian-ThinkPad:4840/")
