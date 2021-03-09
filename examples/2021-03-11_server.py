import threading
import time

from ua import *


class Global:
    server = UaServer()
    thread = None


def server_start():
    Global.thread = threading.Thread(target=Global.server.run, args=[UaBoolean(True)], daemon=True)
    Global.thread.start()
    time.sleep(0.40)


def server_shut_down():
    Global.server.run_shutdown()
    Global.thread.join(1)


def add_matrix_variable():
    attr = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
    attr.display_name = UaLocalizedText("en-US", "Double Matrix")
    attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE

    attr.data_type = TYPES.DOUBLE.type_id
    attr.value_rank = UaValueRanks.TWO_DIMENSIONS
    array_dims = UaUInt32([2, 2])
    attr.array_dimensions = array_dims
    attr.array_dimensions_size = SizeT(2)

    matrix = UaDouble([1.5, 4.0, 2.5, 0.0])
    attr.data_value.set_array(matrix, 4, TYPES.DOUBLE)
    attr.data_value.array_dimensions = array_dims
    attr.data_value.array_dimensions_size = SizeT(2)

    my_integer_node_id = UaNodeId(1, "double.matrix")
    my_integer_name = UaQualifiedName(1, "double matrix")
    parent_node_id = NS0ID.OBJECTSFOLDER
    parent_reference_node_id = NS0ID.ORGANIZES

    result = Global.server.add_variable_node(my_integer_node_id,
                                      parent_node_id,
                                      parent_reference_node_id,
                                      my_integer_name,
                                      NS0ID.BASEDATAVARIABLETYPE,
                                      attr)

    print(result.status_code)


server_start()

add_matrix_variable()

server_shut_down()
