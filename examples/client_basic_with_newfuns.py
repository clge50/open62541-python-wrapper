import sys

sys.path.append("../build/api")
import clientApi

from intermediateApi import ffi, lib

client = clientApi.UaClient()
retval = client.connect(b"opc.tcp://stellaluna:4840/")
