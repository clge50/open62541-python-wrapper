# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import threading
import time

from ua import *


class Vars:
    server = UaServer()


def add_variable():
    attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    my_integer = UaInt32(42)
    attr.data_value.set_scalar(my_integer, UA_TYPES.INT32)
    attr.description = UaLocalizedText("en-US", "the answer")
    attr.display_name = UaLocalizedText("en-US", "the answer")
    attr.data_type = UA_TYPES.INT32.type_id
    attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE

    my_integer_node_id = UaNodeId(1, "the.answer")
    my_integer_name = UaQualifiedName(1, "the answer")
    parent_node_id = UA_NS0ID.OBJECTSFOLDER
    parent_reference_node_id = UA_NS0ID.ORGANIZES

    result = Vars.server.add_variable_node(my_integer_node_id,
                                           parent_node_id,
                                           parent_reference_node_id,
                                           my_integer_name,
                                           UA_NS0ID.BASEDATAVARIABLETYPE,
                                           attr)

    print(result.status_code)


def add_matrix_variable():
    attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    attr.display_name = UaLocalizedText("en-US", "Double Matrix")
    attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE

    attr.data_type = UA_TYPES.DOUBLE.type_id
    attr.value_rank = UaValueRanks.TWO_DIMENSIONS
    array_dims = UaUInt32([2, 2])
    attr.array_dimensions = array_dims
    attr.array_dimensions_size = SizeT(2)

    zero = UaDouble([0.0, 0.0, 0.0, 0.0])
    attr.data_value.set_array(zero, 4, UA_TYPES.DOUBLE)
    attr.data_value.array_dimensions = array_dims
    attr.data_value.array_dimensions_size = SizeT(2)

    my_integer_node_id = UaNodeId(1, "double.matrix")
    my_integer_name = UaQualifiedName(1, "double matrix")
    parent_node_id = UA_NS0ID.OBJECTSFOLDER
    parent_reference_node_id = UA_NS0ID.ORGANIZES

    result = Vars.server.add_variable_node(my_integer_node_id,
                                           parent_node_id,
                                           parent_reference_node_id,
                                           my_integer_name,
                                           UA_NS0ID.BASEDATAVARIABLETYPE,
                                           attr)

    print(result.status_code)


def write_variable():
    my_integer_node_id = UaNodeId(1, "the.answer")
    my_integer = UaInt32(43)
    my_var = UaVariant()
    my_var.date = my_integer

    result = Vars.server.write_value(my_integer_node_id, my_var)
    print(result)

    wv = UaWriteValue()
    wv.node_id = my_integer_node_id
    wv.attribute_id = UaAttributeId.VALUE()
    wv.data_value.status = UA_STATUSCODES.BADNOTCONNECTED
    wv.data_value.has_status = UaBoolean(True)

    result = Vars.server.write(wv)
    print(result)

    wv.data_value.has_status = UaBoolean(False)
    wv.data_value.variant = my_var
    wv.data_value.has_variant = UaBoolean(True)

    result = Vars.server.write(wv)
    print(result)


Vars.server.run_async()

add_variable()
add_matrix_variable()
write_variable()

Vars.server.running = False
