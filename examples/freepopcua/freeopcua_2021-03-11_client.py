from opcua import ua, Client


def write_matrix_variable(client):
    my_integer_node_id = ua.NodeId("double.matrix", 1)
    my_integer_node = client.get_node(my_integer_node_id)

    matrix = ua.Variant([[0.0, 0.0], [0.0, 0.0]], ua.VariantType.Double)

    client.set_values([my_integer_node], [matrix])
    print("write new values.")


def read_matrix_variable(client):
    my_integer_node_id = ua.NodeId("double.matrix", 1)
    my_integer_node = client.get_node(my_integer_node_id)

    matrix = client.get_values([my_integer_node])[0]

    print(f"Result variant: {matrix}")


client = Client("opc.tcp://localhost:4841/freeopcua/server/")
client.connect()

read_matrix_variable(client)
write_matrix_variable(client)
read_matrix_variable(client)




