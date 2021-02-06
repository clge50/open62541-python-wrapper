import sys

sys.path.append("../build/open62541")
import clientApi
from ua_types import NodeId, QualifiedName, UaString
from intermediateApi import ffi, lib
from node_ids import NodeIds
from status_code import StatusCode

client = clientApi.UaClient()
retval = client.connect(b"opc.tcp://127.0.0.1:4840/")

# adding node
myIntegerNodeId = NodeId.new_string(1, "Xa")
myIntegerName = QualifiedName.new(1, "na")
parentNodeId = NodeId.new_numeric(0, NodeIds.UA_NS0ID_OBJECTSFOLDER)
parentReferenceNodeId = NodeId.new_numeric(0, NodeIds.UA_NS0ID_ORGANIZES)
variableType = NodeId.new_numeric(0, NodeIds.UA_NS0ID_BASEDATAVARIABLETYPE)

parent_node_read_result = client.read_node_id_attribute(parentReferenceNodeId)
print("parent node read status code is bad: " + str(StatusCode.isBad(parent_node_read_result.status_code)))

add_variable_node_result = client.add_variable_node(myIntegerNodeId, parentNodeId, parentReferenceNodeId, myIntegerName, variableType)
print("Status code is bad: " + str(lib.UA_StatusCode_isBad(add_variable_node_result.status_code)))
#print("Node id: " + UaString.to_string(add_variable_node_result.out_new_node_id.identifier.string))

# reading node
myIntNodeIdResult = client.read_node_id_attribute(add_variable_node_result.out_new_node_id[0])
print("Status code: " + str(myIntNodeIdResult.status_code))
print("Node id: " + str(myIntNodeIdResult.out_node_id.identifier.numeric))
