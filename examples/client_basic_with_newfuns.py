import sys

sys.path.append("../build/open62541")
import clientApi
from ua_types import NodeId, QualifiedName, StatusCode
from intermediateApi import ffi, lib
from node_ids import NodeIds

client = clientApi.UaClient()
retval = client.connect(b"opc.tcp://127.0.0.1:4840/")

# adding node
myIntegerNodeId = NodeId.new_string(1, "the.answer")
myIntegerName = QualifiedName.new(1, "the answer")
parentNodeId = NodeId.new_numeric(0, NodeIds.UA_NS0ID_OBJECTSFOLDER)
parentReferenceNodeId = NodeId.new_numeric(0, NodeIds.UA_NS0ID_ORGANIZES)
variableType = NodeId.new_numeric(0, NodeIds.UA_NS0ID_BASEDATAVARIABLETYPE)

parentNodeReadResult = client.read_node_id_attribute(parentReferenceNodeId)
print("parent node read status code is bad: " + str(lib.UA_StatusCode_isBad(parentNodeReadResult.status_code)))

# wrapper = client.add_variable_node(myIntegerNodeId, parentNodeId, parentReferenceNodeId, myIntegerName, variableType)
# print("Status code is bad: " + str(lib.UA_StatusCode_isBad(wrapper.status_code)))
# print("Node id: " + wrapper.out_new_node_id.identifier.string.data)

# reading node
# myIntNodeIdResult = client.read_node_id_attribute(wrapper.out_new_node_id[0])
# print("Status code: " + str(myIntNodeIdResult.status_code))
# print("Node id: " + str(myIntNodeIdResult.out_node_id.identifier.numeric))
