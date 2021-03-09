# Connecting a Variable with a Physical Process
from ua import *
from intermediateApi import ffi, lib


def update_current_time(server: UaServer):
    now = UaDateTime.now()
    value = UaVariant()
    UaVariant.set_scalar(value, now, TYPES.DATETIME)
    current_node_id = UaNodeId(1, "current-time-value-callback")
    server.write_value(current_node_id, value)


def add_current_time_variable(server: UaServer):
    now = UaDateTime.now()
    attr = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
    attr.display_name = UaLocalizedText("en-US", "Current time - value callback")
    attr.access_level = UaByte(0x01 << 0 | 0x01 << 1)  # todo: introduce macros or similar
    UaVariant.set_scalar(attr.data_value, now, TYPES.DATETIME)

    current_node_id = UaNodeId(1, "current-time-value-callback")
    current_name = UaQualifiedName(1, "current-time-value-callback")
    parent_node_id = NS0ID.OBJECTSFOLDER
    parent_reference_node_id = NS0ID.ORGANIZES
    variable_type_node_id = NS0ID.BASEDATAVARIABLETYPE
    server.add_variable_node(current_node_id, parent_node_id, parent_reference_node_id, current_name,
                             variable_type_node_id)
    update_current_time(server)


# variable value callback

def before_read_time(server, session_id, session_context, node_id, node_context, numeric_range, data):
    update_current_time(server)


def after_write_time(server, session_id, session_context, node_id, node_context, numeric_range, data):
    logger = UaLogger()
    logger.info(UaLogCategory.UA_LOGCATEGORY_USERLAND, "The variable was updated")


def add_value_callback_to_current_time_variable(server: UaServer):
    current_node_id = UaNodeId(1, "current-time-value-callback")
    callback = UaValueCallback()
    callback.read_callback = before_read_time
    callback.write_callback = after_write_time
    server.set_variable_node_value_callback(current_node_id, callback)


# Variable Data Sources
def read_current_time(server, session_id, session_context, node_id, node_context, source_time_stamp, numeric_range,
                      data_value: UaDataValue):
    now = UaDateTime.now()
    UaVariant.set_scalar(data_value.variant, now,
                         TYPES.DATETIME)  # todo: call set scalar implicitly when setting the value
    data_value.has_variant = UaBoolean(True)
    return UaStatusCode.UA_STATUSCODE_GOOD


def write_current_time(server, session_id, session_context, node_id, node_context, numeric_range, data):
    logger = UaLogger()
    logger.info(UaLogCategory.UA_LOGCATEGORY_USERLAND, "Changing the system time is not implemented")
    return UaStatusCode.UA_STATUSCODE_BADINTERNALERROR


ua_data_value = UaDataValue()


def add_current_time_data_source_variable(server: UaServer):
    attr = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
    attr.display_name = UaLocalizedText("en-US", "Current time - data source")
    attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE

    current_node_id = UaNodeId(1, "current-time-datasource")
    current_name = UaQualifiedName(1, "current-time-datasource")
    parent_node_id = NS0ID.OBJECTSFOLDER
    parent_reference_node_id = NS0ID.ORGANIZES
    variable_type_node_id = NS0ID.BASEDATAVARIABLETYPE

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
    retval = server.run(UaBoolean(True))


if __name__ == "__main__":
    main()
