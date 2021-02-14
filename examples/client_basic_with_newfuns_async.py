import sys
import time

sys.path.append("../build/open62541")
import clientApi
from ua_types import UaNodeId, UaQualifiedName, UaString
from intermediateApi import ffi, lib
from node_ids import NodeIds
from status_code import StatusCode

client = clientApi.UaClient()
retval = client.connect(b"opc.tcp://127.0.0.1:4840/")

# adding node
myIntegerNodeId = UaNodeId.new_string(1, "Xa")
myIntegerName = UaQualifiedName.new(1, "na")
parentNodeId = UaNodeId.new_numeric(0, NodeIds.UA_NS0ID_OBJECTSFOLDER)
parentReferenceNodeId = UaNodeId.new_numeric(0, NodeIds.UA_NS0ID_ORGANIZES)
variableType = UaNodeId.new_numeric(0, NodeIds.UA_NS0ID_BASEDATAVARIABLETYPE)

fun = ffi.new_handle(lambda _client, req_id, out: print("Node id: " + str(out.identifier.numeric)))
parent_node_read_result = client.read_node_id_attribute_async(parentReferenceNodeId, fun, 5)
print("a")
while True:
    time.sleep(5)
    client.run_iterate(5)
    print("parent node read status code is bad: " + str(StatusCode.isBad(parent_node_read_result)))

#time.sleep(10)
#print("parent node read status code is bad: " + str(StatusCode.isBad(parent_node_read_result.status_code)))

#add_variable_node_result = client.add_variable_node(myIntegerNodeId, parentNodeId, parentReferenceNodeId, myIntegerName, variableType)
#print("Status code is bad: " + str(lib.UA_StatusCode_isBad(add_variable_node_result.status_code)))
#print("Node id: " + UaString.to_string(add_variable_node_result.out_new_node_id.identifier.string))

# reading node
#myIntNodeIdResult = client.read_node_id_attribute(add_variable_node_result.out_new_node_id[0])
#print("Status code: " + str(myIntNodeIdResult.status_code))
#print("Node id: " + str(myIntNodeIdResult.out_node_id.identifier.numeric))
