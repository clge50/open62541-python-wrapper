# Connecting a Variable with a Physical Process
from ua import *


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

def before_read_time(server, session_id, session_context, nodeid, nodeContext, range, data):
    update_current_time(server)


def after_write_time(server, sessionId, sessionContext, nodeId, nodeContext, numeric_range, data):
    logger = UaLogger()
    logger.info(UaLogCategory.UA_LOGCATEGORY_USERLAND, "The variable was updated")


def add_value_callback_to_current_time_variable(server: UaServer):
    current_node_id = UaNodeId(1, "current-time-value-callback")
    callback = UaValueCallback(before_read_time, after_write_time)
    server.set_variable_node_value_callback(current_node_id, callback)


# Variable Data Sources
def read_current_time(server, session_id, session_context, node_id, node_context, source_time_stamp, numeric_range,
                      data_value: UaDataValue):
    now = UaDateTime.now()
    UaVariant.set_scalar(data_value.variant, now,
                         TYPES.DATETIME)  # todo: call set scalar implicitly when setting the value
    data_value.has_variant = True
    return UaStatusCode.UA_STATUSCODE_GOOD


def write_current_time(server, sessionId, sessionContext, nodeId, nodeContext, numeric_range, data):
    logger = UaLogger()
    logger.info(UaLogCategory.UA_LOGCATEGORY_USERLAND, "Changing the system time is not implemented")
    return UaStatusCode.UA_STATUSCODE_BADINTERNALERROR


def add_current_time_data_source_variable(server):
    pass


def add_current_time_external_data_source(server):
    pass


def main():
    server = UaServer()

    add_current_time_variable(server)
    add_value_callback_to_current_time_variable(server)
    # add_current_time_data_source_variable(server)

    # add_current_time_external_data_source(server)
    retval = server.run(UaBoolean(True))


if __name__ == "__main__":
    main()
