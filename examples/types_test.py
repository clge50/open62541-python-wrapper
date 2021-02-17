import sys

sys.path.append("../build/open62541")
import clientApi
from ua_types import *
from intermediateApi import ffi, lib
from node_ids import NodeIds

x = UaStatusCode(0x80000000)
print(x.is_bad())

client = clientApi.UaClient()
retval = UaStatusCode(client.connect(b"opc.tcp://127.0.0.1:4840/"))

# adding node
myIntegerNodeId = UaNodeId(1, "the.answer")
myIntegerName = UaQualifiedName(1, "the answer")
parentNodeId = UaNodeId(0, NodeIds.UA_NS0ID_OBJECTSFOLDER)
parentReferenceNodeId = UaNodeId(0, NodeIds.UA_NS0ID_ORGANIZES)
variableType = UaNodeId(0, NodeIds.UA_NS0ID_BASEDATAVARIABLETYPE)

parent_node_read_result = client.read_node_id_attribute(parentReferenceNodeId.value)
print("read_node_id_attribute was successful: " + str(not UaStatusCode(parent_node_read_result.status_code).is_bad()))

add_variable_node_result = client.add_variable_node(myIntegerNodeId.value, parentNodeId.value,
                                                    parentReferenceNodeId.value, myIntegerName.value,
                                                    variableType.value)
out_node_id = UaNodeId(val=add_variable_node_result.out_new_node_id)
print("add_variable_node was successful: " + str(not UaStatusCode(add_variable_node_result.status_code).is_bad()))
print("myIntegerNodeId (string) read from server add_variable_node_result response: " +
      str(out_node_id))

# reading node
myIntNodeIdResult = client.read_node_id_attribute(out_node_id._deref())
print("read_node_id_attribute was successful: " + str(not UaStatusCode(myIntNodeIdResult.status_code).is_bad()))
int_node_id = UaNodeId(val=myIntNodeIdResult.out_node_id)
print("myIntegerNodeId (string) read from server read_node_id_attribute response: " + str(int_node_id))
