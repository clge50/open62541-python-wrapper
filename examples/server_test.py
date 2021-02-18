import sys


sys.path.append("../build/open62541")
import serverApi
import clientApi

from ua_types import UaNodeId, UaQualifiedName, UaString
from node_ids import NodeIds
from status_code import StatusCode



# TODO: change when types are properly implemented!
defaults = clientApi.DefaultAttributes

attr = defaults.VARIABLE_ATTRIBUTES_DEFAULT
node_id = UaNodeId.new_string(1, "test1")
qualified_name = UaQualifiedName.new(1, "Test1")
parent_node_id = UaNodeId.new_numeric(0, NodeIds.UA_NS0ID_OBJECTSFOLDER)
parent_node_ref = UaNodeId.new_numeric(0, NodeIds.UA_NS0ID_ORGANIZES)




# Create new server object
server = serverApi.UaServer()

status = server.add_variable_node(node_id, parent_node_id, parent_node_ref, qualified_name, UaNodeId.new_numeric(0, NodeIds.UA_NS0ID_BASEDATAVARIABLETYPE), attr, None , UaNodeId.new_string(1, "") )

retval = server.run([True])












