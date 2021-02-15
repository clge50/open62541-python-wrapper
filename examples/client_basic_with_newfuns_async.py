import sys
import time

sys.path.append("../build/open62541")
import clientApi
from ua_types import UaNodeId, UaQualifiedName, UaString
from intermediateApi import ffi, lib
from node_ids import NodeIds
from status_code import StatusCode

client = clientApi.UaClient()
retval = client.connect("opc.tcp://127.0.0.1:4840/")

# adding node
myIntegerNodeId = UaNodeId.new_string(1, "a")
myIntegerName = UaQualifiedName.new(1, "b")
parentNodeId = UaNodeId.new_numeric(0, NodeIds.UA_NS0ID_OBJECTSFOLDER)
parentReferenceNodeId = UaNodeId.new_numeric(0, NodeIds.UA_NS0ID_ORGANIZES)
variableType = UaNodeId.new_numeric(0, NodeIds.UA_NS0ID_BASEDATAVARIABLETYPE)

fun = ffi.new_handle(lambda _client, req_id, out, user_data="Test": print(f"Node id: {str(out.identifier.numeric)}, request-id: {str(req_id)} user_data: {user_data}"))
parent_node_read_result = client.read_node_id_attribute_async(parentReferenceNodeId, fun)
print("req_id: " + str(parent_node_read_result.req_id))

client.run_iterate(4)
print("parent node read status code is bad: " + str(StatusCode.isBad(parent_node_read_result.status_code)))

fun2 = ffi.new_handle(lambda _client, req_id, ar, user_data="Test": print(f"Request-id: {str(req_id)} user_data: {user_data}"))
add_variable_node_result = client.add_variable_node_async(myIntegerNodeId, parentNodeId, parentReferenceNodeId, myIntegerName, variableType, fun2)

for i in range(0, 4):
    print("Status code is bad: " + str(lib.UA_StatusCode_isBad(add_variable_node_result.status_code)))
    time.sleep(5)
    client.run_iterate(4)

# reading node
#myIntNodeIdResult = client.read_node_id_attribute_async(add_variable_node_result.out_new_node_id[0])
#print("Status code: " + str(myIntNodeIdResult.status_code))
#print("Node id: " + str(myIntNodeIdResult.out_node_id.identifier.numeric))
