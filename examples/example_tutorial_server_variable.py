import threading
import time

from ua import *

def add_variable():
    attr = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT
    my_integer = UaInt32(42)
    attr.data_value.set_scalar(my_integer, TYPES.INT32)
    attr.description = UaLocalizedText("en-US", "the answer")
    attr.display_name = UaLocalizedText("en-US", "the answer")
    attr.data_type = TYPES.INT32.type_id
    attr.access_level = UaAccessLevelMasks.READ | UaAccessLevelMasks.WRITE

    my_integer_node_id = UaNodeId(1, "the.answer37373737")
    my_integer_name = UaQualifiedName(1, "the answer")
    parent_node_id = NS0ID.OBJECTSFOLDER
    parent_reference_node_id = NS0ID.ORGANIZES

    result = server.add_variable_node(my_integer_node_id,
                                      parent_node_id,
                                      parent_reference_node_id,
                                      my_integer_name,
                                      NS0ID.BASEDATAVARIABLETYPE,
                                      attr)

    return result


server = UaServer()

thread = threading.Thread(target=server.run, args=[UaBoolean(True)], daemon=True)
thread.start()
time.sleep(0.40)
server.run_shutdown()
thread.join(1)

print(add_variable().status_code)
print(add_variable().out_node)

