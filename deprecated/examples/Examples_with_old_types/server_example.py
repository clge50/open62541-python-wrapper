import sys
sys.path.append("../../../build/open62541")

import serverApi
import clientApi
import ua_types
from intermediateApi import ffi, lib
from ua_types import UaNodeId, UaQualifiedName, UaString
from node_ids import NodeIds
from status_code import StatusCode



# Set default variable attributes
attr = lib.UA_VariableAttributes_default

# The node's display and browse name
node_id = ua_types.UaNodeId(1, "test1")
qualified_name = ua_types.UaQualifiedName(1, "Test1")

# The node's parent node object / object folder
parent_node_id = ua_types.UaNodeId(0, NodeIds.UA_NS0ID_OBJECTSFOLDER)
parent_node_ref = ua_types.UaNodeId(0, NodeIds.UA_NS0ID_ORGANIZES)


# Create new server object
server = serverApi.UaServer()

# Add our custom variable
status = server.add_variable_node(node_id, parent_node_id, parent_node_ref, qualified_name, ua_types.UaNodeId(0, NodeIds.UA_NS0ID_BASEDATAVARIABLETYPE), None, attr ,ua_types.UaNodeId(1, ""))

# Start server
retval = server.run([True])