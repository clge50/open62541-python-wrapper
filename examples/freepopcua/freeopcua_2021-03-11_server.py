from opcua import ua, uamethod, Server


def add_matrix_variable(server):
    objects = server.get_objects_node()
    my_integer_node_id = ua.NodeId("double.matrix", 1)
    matrix = ua.Variant([[1.5, 4.0], [2.5, 0.0]], ua.VariantType.Double)
    matrix_var = objects.add_variable(nodeid=my_integer_node_id,
                                      bname=ua.QualifiedName("double.matrix", 1),
                                      val=matrix)
    matrix_var.set_writable()


server = Server()
server.set_endpoint("opc.tcp://127.0.0.1:4841/freeopcua/server/")
uri = "http://examples.freeopcua.github.io"
idx = server.register_namespace(uri)
server.start()
add_matrix_variable(server)
server.stop()
