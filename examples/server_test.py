import sys


sys.path.append("../build/open62541")
import serverApi
import clientApi
import ua_types
from intermediateApi import ffi, lib
from ua_types import UaNodeId, UaQualifiedName, UaString
from node_ids import NodeIds
from status_code import StatusCode



# TODO: change when types are properly implemented!
attr = lib.UA_VariableAttributes_default
node_id = ua_types.UaNodeId(1, "test1")
qualified_name = ua_types.UaQualifiedName(1, "Test1")
parent_node_id = ua_types.UaNodeId(0, NodeIds.UA_NS0ID_OBJECTSFOLDER)
parent_node_ref = ua_types.UaNodeId(0, NodeIds.UA_NS0ID_ORGANIZES)

running:ua_types.UaBoolean = True


# Create new server object
server = serverApi.UaServer()

status = server.add_variable_node(node_id, parent_node_id, parent_node_ref, qualified_name, ua_types.UaNodeId(0, NodeIds.UA_NS0ID_BASEDATAVARIABLETYPE), None, attr ,ua_types.UaNodeId(1, ""))

retval = server.run([True])












