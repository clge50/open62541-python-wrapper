from ua import *


def write_matrix_variable(client):
    my_integer_node_id = UaNodeId(1, "double.matrix")
    
    matrix = UaDouble([0.0, 0.0, 0.0, 0.0])
    
    my_variant = UaVariant()
    my_variant.set_array(matrix, 4, UA_TYPES.DOUBLE)
    my_variant.array_dimensions = UaUInt32([2, 2])
    my_variant.array_dimensions_size = SizeT(2)
    
    result = client.write_value_attribute(my_integer_node_id, my_variant)
    print(f"write_value_attribute UaStatuscode was: {result}\n")


def read_matrix_variable(client):
    my_integer_node_id = UaNodeId(1, "double.matrix")

    result = client.read_value_attribute(my_integer_node_id)
    print(f"read_value_attribute UaStatuscode was: {result.status_code}")

    dimensions = UaList(result.value.array_dimensions, result.value.array_dimensions_size, UaUInt32)
    array = UaList(result.value.data, 4, UaDouble)

    print(f"Result variant: {array} in dimensions {dimensions}\n")


if __name__ == '__main__':
    client = UaClient()
    client.connect("opc.tcp://127.0.0.1:4840/")
    read_matrix_variable(client)
    write_matrix_variable(client)
    read_matrix_variable(client)
