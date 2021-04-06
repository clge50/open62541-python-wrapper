# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from ua import *

logger = UaLogger()
logger.error(UaLogCategory(0), "Eine Nachricht")

x = UaStatusCode(0x80000000)
print(x.is_bad())

client = UaClient()
ret_val = client.connect("opc.tcp://127.0.0.1:4840/")

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
parent_node_id = UA_NS0ID.OBJECTSFOLDER
parent_reference_node_id = UA_NS0ID.ORGANIZES
variable_type = UA_NS0ID.BASEDATAVARIABLETYPE

parent_node_read_result = client.read_node_id_attribute(parent_reference_node_id)
print(f"read_node_id_attribute UaStatuscode was: {str(parent_node_read_result.status_code)}")
print(f"read_node_id_attribute read node id: {str(parent_node_read_result.out_node_id)}")

add_variable_node_result = client.add_variable_node(parent_node_id,
                                                    parent_reference_node_id,
                                                    my_integer_name,
                                                    variable_type)
print(f"add_variable_node UaStatuscode was: {str(add_variable_node_result.status_code)}")
print(
    f"myIntegerNodeId (string) read from server add_variable_node_result response: {str(add_variable_node_result.out_new_node_id)}")

# reading node
my_int_node_id_result = client.read_node_id_attribute(add_variable_node_result.out_new_node_id)
print(f"read_node_id_attribute UaStatuscode was: {str(my_int_node_id_result.status_code)}")
print(f"myIntegerNodeId (string) read from server read_node_id_attribute: {str(my_int_node_id_result.out_node_id)}")
