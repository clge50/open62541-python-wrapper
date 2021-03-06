from ua import *

client = UaClient()

variable_node_id = UaNodeId(0, "abc")
browse_name = UaQualifiedName(0, "fgh")
variable_attributes = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
v3 = UaVariant()
d = [1.1, 1.2, 1.3,
     2.1, 2.2, 2.3,
     3.1, 3.2, 3.3]
d = UaDouble(d)

v3.set_array(d, SizeT(9), TYPES.DOUBLE)
v3.array_dimensions = UaUInt32([3, 3])
v3.array_dimensions_size = SizeT(2)

variable_attributes.data_value = v3

parent_node_id = NS0ID.OBJECTSFOLDER
parent_reference_node_id = NS0ID.ORGANIZES
variable_type = NS0ID.BASEDATAVARIABLETYPE

parent_node_read_result = client.read_node_id_attribute(parent_reference_node_id)
print(f"read_node_id_attribute UaStatuscode was: {str(parent_node_read_result.status_code)}")
print(f"read_node_id_attribute read node id: {str(parent_node_read_result.out_node_id)}")

add_variable_node_result = client.add_variable_node(parent_node_id,
                                                    parent_reference_node_id, browse_name,
                                                    variable_type)

result = client.read_value_attribute(add_variable_node_result.out_new_node_id)
print(result.value)
