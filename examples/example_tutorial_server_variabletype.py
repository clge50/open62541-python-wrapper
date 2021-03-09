import threading
import time

from ua import *


class Vars:
    server = UaServer()
    thread = None
    point_type_id = None
    point_variable_id = None


def server_start():
    Vars.thread = threading.Thread(target=Vars.server.run, args=[UaBoolean(True)], daemon=True)
    Vars.thread.start()
    time.sleep(0.40)


def server_shut_down():
    Vars.server.run_shutdown()
    Vars.thread.join(1)


def add_variable_type_2d_point():
    vt_attr = DefaultAttributes.VARIABLE_TYPE_ATTRIBUTES_DEFAULT
    vt_attr.data_type = TYPES.DOUBLE.type_id
    vt_attr.value_rank = UaValueRanks.ONE_DIMENSION
    array_dims = UaUInt32([2])
    vt_attr.array_dimensions = array_dims
    vt_attr.array_dimensions_size = SizeT(1)
    vt_attr.display_name = UaLocalizedText("en-US", "2DPoint Type")

    zero = UaDouble([0.0, 0.0], 2)
    vt_attr.data_value.set_array(zero, 2, TYPES.DOUBLE)

    result = Vars.server.add_variable_type_node(UaNodeId(UaNodeId.NULL),
                                                NS0ID.BASEDATAVARIABLETYPE,
                                                NS0ID.HASSUBTYPE,
                                                UaQualifiedName(1, "2DPoint Type"),
                                                UaNodeId(UaNodeId.NULL),
                                                vt_attr)
    Vars.point_type_id = result.out_node


def add_variable():
    v_attr = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
    v_attr.data_type = TYPES.DOUBLE.type_id
    v_attr.value_rank = UaValueRanks.ONE_DIMENSION
    array_dims = UaUInt32([2])
    v_attr.array_dimensions = array_dims
    v_attr.array_dimensions_size = SizeT(1)
    v_attr.display_name = UaLocalizedText("en-US", "2DPoint Variable")
    v_attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE

    result = Vars.server.add_variable_node(UaNodeId(UaNodeId.NULL),
                                           NS0ID.OBJECTSFOLDER,
                                           NS0ID.HASCOMPONENT,
                                           UaQualifiedName(1, "2DPoint Type"),
                                           Vars.point_type_id,
                                           v_attr)
    Vars.point_variable_id = result.out_node


def add_variable_fail():
    v_attr = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
    v_attr.data_type = TYPES.DOUBLE.type_id
    v_attr.value_rank = UaValueRanks.SCALAR
    v_attr.display_name = UaLocalizedText("en-US", "2DPoint Type (fail)")
    s = UaString("2dpoint?")
    v_attr.data_value.set_scalar(s, TYPES.STRING)

    result = Vars.server.add_variable_node(UaNodeId(UaNodeId.NULL),
                                           NS0ID.OBJECTSFOLDER,
                                           NS0ID.HASCOMPONENT,
                                           UaQualifiedName(1, "2DPoint Type (fail)"),
                                           Vars.point_type_id,
                                           v_attr)
    UaLogger().info(UaLogCategory(UaLogCategory.UA_LOGCATEGORY_USERLAND), f"failed with {result.status_code}")


def write_variable():
    ret_val = Vars.server.write_value_rank(Vars.point_variable_id,
                                           UaValueRanks.ONE_OR_MORE_DIMENSIONS)
    UaLogger().info(UaLogCategory(UaLogCategory.UA_LOGCATEGORY_USERLAND), f"failed with {ret_val}")



server_start()

add_variable_type_2d_point()
add_variable()
add_variable_fail()
write_variable()

server_shut_down()
