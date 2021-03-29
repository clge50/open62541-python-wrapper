import sys

from signal import signal, SIGINT, SIGTERM

sys.path.append("../build/wrappy_o6")
from ua import *

log_stdout = UaLogger()
server = UaServer()


def data_change_notification_callback(server: UaServer, monitored_item_id: UaUInt32,
                                      monitored_item_context: Void,
                                      node_id: UaNodeId, node_context: Void, attribute_id: UaUInt32,
                                      value: UaDataValue):
    log_stdout.info(UaLogCategory.USERLAND(), "Received Notification")


def add_monitored_item_to_current_time_variable(server: UaServer):
    current_time_node_id = UA_NS0ID.SERVER_SERVERSTATUS_CURRENTTIME
    mon_request: UaMonitoredItemCreateRequest() = UaMonitoredItemCreateRequest.default(current_time_node_id)
    mon_request.requested_parameters.sampling_interval = UaDouble(1000.0)
    print(mon_request)
    mon_result = server.create_data_change_monitored_item(UaTimestampsToReturn.SOURCE(), mon_request, Void.NULL(),
                                                          data_change_notification_callback)
    print(mon_result)


def stop_handler(arg1, arg2):
    log_stdout.info(UaLogCategory.SERVER(), "received ctrl-c")
    server.running = False


if __name__ == '__main__':
    signal(SIGINT, stop_handler)
    signal(SIGTERM, stop_handler)

    add_monitored_item_to_current_time_variable(server)
    server.run()
