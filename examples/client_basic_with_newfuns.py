import sys

sys.path.append("../build/open62541")
import clientApi

from intermediateApi import ffi, lib

client = clientApi.UaClient()
retval = client.connect(b"opc.tcp://127.0.0.1:4840/")

# adding node
myIntegerNodeId = lib.UA_NODEID_STRING(1, b"the.answer")
myIntegerName = lib.UA_QUALIFIEDNAME(1, b"the answer")
parentNodeId = lib.UA_NODEID_NUMERIC(ffi.cast("UA_UInt16", 0), ffi.cast("UA_UInt32", 85))
parentReferenceNodeId = lib.UA_NODEID_NUMERIC(ffi.cast("UA_UInt16", 0), ffi.cast("UA_UInt32", 35))
variableType = lib.UA_NODEID_NUMERIC(0, 63)

parentNodeReadResult = client.read_node_id_attribute(parentReferenceNodeId)
print("parent node read status code is bad: " + str(lib.UA_StatusCode_isBad(parentNodeReadResult.status_code)))

wrapper = client.add_variable_node(myIntegerNodeId, parentNodeId, parentReferenceNodeId, myIntegerName, variableType)
print("Status code is bad: " + str(lib.UA_StatusCode_isBad(wrapper.status_code)))
print("Node id: " + wrapper.out_new_node_id.identifier.string.data)

# reading node
myIntNodeIdResult = client.read_node_id_attribute(wrapper.out_new_node_id[0])
print("Status code: " + str(myIntNodeIdResult.status_code))
print("Node id: " + str(myIntNodeIdResult.out_node_id.identifier.numeric))