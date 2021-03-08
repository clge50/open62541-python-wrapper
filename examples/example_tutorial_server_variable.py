import threading
import time

from ua import *


class Vars:
    server = UaServer()
    thread = None


def server_start():
    Vars.thread = threading.Thread(target=Vars.server.run, args=[UaBoolean(True)], daemon=True)
    Vars.thread.start()
    time.sleep(0.40)


def server_shut_down():
    Vars.server.run_shutdown()
    Vars.thread.join(1)


def add_variable():
    attr = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
    my_integer = UaInt32(42)
    attr.data_value.set_scalar(my_integer, TYPES.INT32)
    attr.description = UaLocalizedText("en-US", "the answer")
    attr.display_name = UaLocalizedText("en-US", "the answer")
    attr.data_type = TYPES.INT32.type_id
    attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE

    my_integer_node_id = UaNodeId(1, "the.answer")
    my_integer_name = UaQualifiedName(1, "the answer")
    parent_node_id = NS0ID.OBJECTSFOLDER
    parent_reference_node_id = NS0ID.ORGANIZES

    result = Vars.server.add_variable_node(my_integer_node_id,
                                      parent_node_id,
                                      parent_reference_node_id,
                                      my_integer_name,
                                      NS0ID.BASEDATAVARIABLETYPE,
                                      attr)

    print(result.status_code)


def add_matrix_variable():
    attr = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
    attr.display_name = UaLocalizedText("en-US", "Double Matrix")
    attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE

    attr.data_type = TYPES.DOUBLE.type_id
    attr.value_rank = UaValueRanks.TWO_DIMENSIONS
    array_dims = UaUInt32([2, 2])
    attr.array_dimensions = array_dims
    attr.array_dimensions_size = SizeT(2)

    zero = UaDouble([0.0, 0.0, 0.0, 0.0])
    attr.data_value.set_array(zero, 4, TYPES.DOUBLE)
    attr.data_value.array_dimensions = array_dims
    attr.data_value.array_dimensions_size = SizeT(2)

    my_integer_node_id = UaNodeId(1, "double.matrix")
    my_integer_name = UaQualifiedName(1, "double matrix")
    parent_node_id = NS0ID.OBJECTSFOLDER
    parent_reference_node_id = NS0ID.ORGANIZES

    result = Vars.server.add_variable_node(my_integer_node_id,
                                      parent_node_id,
                                      parent_reference_node_id,
                                      my_integer_name,
                                      NS0ID.BASEDATAVARIABLETYPE,
                                      attr)

    print(result.status_code)


def write_variable():
    my_integer_node_id = UaNodeId(1, "the.answer")
    my_integer = UaInt32(43)
    my_var = UaVariant()
    my_var.set_scalar(my_integer, TYPES.INT32)

    result = Vars.server.write_value(my_integer_node_id, my_var)
    print(result)


    wv = UaWriteValue()
    wv.node_id = my_integer_node_id
    wv.attribute_id = UaAttributeId(UaAttributeId.UA_ATTRIBUTEID_VALUE)
    wv.data_value.status = UaStatusCode(UaStatusCode.UA_STATUSCODE_BADNOTCONNECTED)
    wv.data_value.has_status = UaBoolean(True)

    result = Vars.server.write(wv)
    print(result)

    wv.data_value.has_status = UaBoolean(False)
    wv.data_value.variant = my_var
    wv.data_value.has_variant = UaBoolean(True)

    result = Vars.server.write(wv)
    print(result)


server_start()

add_variable()
add_matrix_variable()
write_variable()

server_shut_down()
