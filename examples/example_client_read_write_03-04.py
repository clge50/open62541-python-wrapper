from ua import *

client = UaClient()
client.connect("opc.tcp://127.0.0.1:4840/")

variable_node_id = UaNodeId(1, "abc")
browse_name = UaQualifiedName(1, "fgh")
variable_attributes = UA_ATTRIBUTES_DEFAULT.VARIABLE
v3 = UaVariant()
d = [1.1, 1.2, 1.3,
     2.1, 2.2, 2.3,
     3.1, 3.2, 3.3]
d = UaDouble(d)

v3.set_array(d, SizeT(9), UA_TYPES.DOUBLE)
v3.array_dimensions = UaUInt32([3, 3])
v3.array_dimensions_size = SizeT(2)

variable_attributes.data_value = v3

parent_node_id = UA_NS0ID.OBJECTSFOLDER
parent_reference_node_id = UA_NS0ID.ORGANIZES
variable_type = UA_NS0ID.BASEDATAVARIABLETYPE

parent_node_read_result = client.read_node_id_attribute(parent_reference_node_id)
print(f"read_node_id_attribute UaStatuscode was: {str(parent_node_read_result.status_code)}")
print(f"read_node_id_attribute read node id: {str(parent_node_read_result.out_node_id)}")

add_variable_node_result = client.add_variable_node(parent_node_id,
                                                    parent_reference_node_id, browse_name,
                                                    variable_type, attr=variable_attributes)
print(add_variable_node_result.out_new_node_id)
print(add_variable_node_result.status_code)

read_node_id_attribute_result = client.read_node_id_attribute(add_variable_node_result.out_new_node_id)
print(f"read_node_id_attribute UaStatuscode was: {str(read_node_id_attribute_result.status_code)}")
print(
    f"myIntegerNodeId (string) read from server read_node_id_attribute: {str(read_node_id_attribute_result.out_node_id)}")

result = client.read_value_attribute(read_node_id_attribute_result.out_node_id)
print(f"read_value_attribute UaStatuscode was: {str(result.status_code)}")
print(result.value)
array = UaList(result.value.data, 9, UaDouble)
print(array.value)
