import sys
import time

sys.path.append("../build/open62541")
import clientApi
from ua_types import *
from intermediateApi import ffi, lib

x = UaStatusCode(0x80000000)
print(x.is_bad())

client = clientApi.UaClient()
retval = client.connect("opc.tcp://127.0.0.1:4840/")

# configuring attribute
# attr = clientApi.DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
# myInteger = UaInt32(42)
# UA_Variant_setScalar(&attr.value, &myInteger, &UA_TYPES[UA_TYPES_INT32]);
# attr.description = UaLocalizedText("en-US", "hello world!")
# attr.displayName = UaLocalizedText("en-US", "Just to be sure")
# attr.dataType = UA_TYPES[UA_TYPES_INT32].typeId;

# adding node
my_integer_node_id = UaNodeId(1, "the answer")
my_integer_name = UaQualifiedName(1, "the.answer")
parent_node_id = UaNodeId(0, UaNodeId.UA_NS0ID_OBJECTSFOLDER)
parent_reference_node_id = UaNodeId(0, UaNodeId.UA_NS0ID_ORGANIZES)
variable_type = UaNodeId(0, UaNodeId.UA_NS0ID_BASEDATAVARIABLETYPE)

fun = lambda _client, req_id, out, user_data="Test": print(
    f"Node id: {str(out)}, request-id: {str(req_id)} user_data: {user_data}")
parent_node_read_result = client.read_node_id_attribute_async(parent_reference_node_id, fun)
print("req_id: " + str(parent_node_read_result.req_id))
client.run_iterate(4)
print("parent node read status code: " + str(parent_node_read_result.status_code))

fun2 = lambda _client, req_id, ar, user_data="Test": print(f"Request-id: {str(req_id)} user_data: {user_data}")
add_variable_node_result = client.add_variable_node_async(my_integer_node_id, parent_node_id, parent_reference_node_id,
                                                          my_integer_name, variable_type, fun2)

for i in range(0, 4):
    print("Status code: " + str(add_variable_node_result.status_code))
    time.sleep(5)
    client.run_iterate(4)
