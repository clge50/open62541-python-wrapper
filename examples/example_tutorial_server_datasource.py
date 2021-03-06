# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

# Connecting a Variable with a Physical Process
from ua import *


def update_current_time(server: UaServer):
    value = UaVariant()
    value.data = UaDateTime.now()
    current_node_id = UaNodeId(1, "current-time-value-callback")
    server.write_value(current_node_id, value)


def add_current_time_variable(server: UaServer):
    attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    attr.display_name = UaLocalizedText("en-US", "Current time - value callback")
    attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE
    attr.data_value.data = UaDateTime.now()

    current_node_id = UaNodeId(1, "current-time-value-callback")
    current_name = UaQualifiedName(1, "current-time-value-callback")
    parent_node_id = UA_NS0ID.OBJECTSFOLDER
    parent_reference_node_id = UA_NS0ID.ORGANIZES
    variable_type_node_id = UA_NS0ID.BASEDATAVARIABLETYPE
    server.add_variable_node(current_node_id, parent_node_id, parent_reference_node_id, current_name,
                             variable_type_node_id)
    update_current_time(server)


# variable value callback

def before_read_time(server, session_id, session_context, node_id, node_context, numeric_range, data):
    update_current_time(server)


def after_write_time(server, session_id, session_context, node_id, node_context, numeric_range, data):
    logger = UaLogger()
    logger.info(UaLogCategory.USERLAND(), "The variable was updated")


def add_value_callback_to_current_time_variable(server: UaServer):
    current_node_id = UaNodeId(1, "current-time-value-callback")
    callback = UaValueCallback()
    callback.read_callback = before_read_time
    callback.write_callback = after_write_time
    server.set_variable_node_value_callback(current_node_id, callback)


# Variable Data Sources
def read_current_time(server, session_id, session_context, node_id, node_context, source_time_stamp, numeric_range,
                      data_value: UaDataValue):
    data_value.variant.data = UaDateTime.now()
    data_value.has_variant = UaBoolean(True)
    return UA_STATUSCODES.GOOD


def write_current_time(server, session_id, session_context, node_id, node_context, numeric_range, data):
    UaLogger().info(UaLogCategory.USERLAND(), "Changing the system time is not implemented")
    return UA_STATUSCODES.BADINTERNALERROR


ua_data_value = UaDataValue()


def add_current_time_data_source_variable(server: UaServer):
    attr = UA_ATTRIBUTES_DEFAULT.VARIABLE
    attr.display_name = UaLocalizedText("en-US", "Current time - data source")
    attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE

    current_node_id = UaNodeId(1, "current-time-datasource")
    current_name = UaQualifiedName(1, "current-time-datasource")
    parent_node_id = UA_NS0ID.OBJECTSFOLDER
    parent_reference_node_id = UA_NS0ID.ORGANIZES
    variable_type_node_id = UA_NS0ID.BASEDATAVARIABLETYPE

    time_data_source = UaDataSource()
    time_data_source.read_callback = read_current_time
    time_data_source.write_callback = write_current_time
    server.add_data_source_variable_node(current_node_id, parent_node_id, parent_reference_node_id, current_name,
                                         variable_type_node_id, time_data_source, attr)


def add_current_time_external_data_source(server: UaServer):
    current_node_id = UaNodeId(1, "current-time-external-source")
    value_backend = UaValueBackend()
    value_backend.set_external(ua_data_value)

    server.set_variable_node_value_backend(current_node_id, value_backend)


def main():
    server = UaServer()

    add_current_time_variable(server)
    add_value_callback_to_current_time_variable(server)
    add_current_time_data_source_variable(server)

    add_current_time_external_data_source(server)
    ret_val = server.run()


if __name__ == "__main__":
    main()
