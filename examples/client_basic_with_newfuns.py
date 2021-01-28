import sys

sys.path.append("../build/api")
import clientApi

from intermediateApi import ffi, lib

client = clientApi.UaClient()
retval = client.connect(b"opc.tcp://127.0.0.1:4840/")

# adding node
myIntegerNodeId = lib.UA_NODEID_STRING(1, b"the.answer");
myIntegerName = lib.UA_QUALIFIEDNAME(1, b"the answer");
parentNodeId = lib.UA_NODEID_NUMERIC(ffi.cast("UA_UInt16", 0), ffi.cast("UA_UInt32", 85))
parentReferenceNodeId = lib.UA_NODEID_NUMERIC(ffi.cast("UA_UInt16", 0), ffi.cast("UA_UInt32", 35))
variableType = lib.UA_NODEID_NUMERIC(0, 63)
wrapper = client.add_variable_node(myIntegerNodeId, parentNodeId, parentReferenceNodeId, myIntegerName, variableType)
print("Status code: " + str(wrapper.status_code))
print("Node id: " + wrapper.out_new_node_id.identifier.string)

# reading node
myIntNodeIdResult = client.read_node_id_attribute(wrapper.out_new_node_id[0])
print("Status code: " + str(myIntNodeIdResult.status_code))
print("Node id: " + str(myIntNodeIdResult.out_node_id.identifier.numeric))