import sys

sys.path.append("../build/open62541")
import clientApi
from ua_types import *
from intermediateApi import ffi, lib

logger = UaLogger()
logger.info(UaLogCategory(0), b"eine nachticht")

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

parent_node_read_result = client.read_node_id_attribute(parent_reference_node_id)
print(f"read_node_id_attribute UaStatuscode was: {str(parent_node_read_result.status_code)}")
print(f"read_node_id_attribute read node id: {str(parent_node_read_result.out_node_id)}")

add_variable_node_result = client.add_variable_node(my_integer_node_id, parent_node_id,
                                                    parent_reference_node_id, my_integer_name,
                                                    variable_type)
print(f"add_variable_node UaStatuscode was: {str(add_variable_node_result.status_code)}")
print(
    f"myIntegerNodeId (string) read from server add_variable_node_result response: {str(add_variable_node_result.out_new_node_id)}")

# reading node
my_int_node_id_result = client.read_node_id_attribute(add_variable_node_result.out_new_node_id)
print(f"read_node_id_attribute UaStatuscode was: {str(my_int_node_id_result.status_code)}")
print(f"myIntegerNodeId (string) read from server read_node_id_attribute: {str(my_int_node_id_result.out_node_id)}")
