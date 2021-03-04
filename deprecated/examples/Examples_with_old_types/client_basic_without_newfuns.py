import sys

sys.path.append("../../../build/open62541")
import clientApi

from intermediateApi import ffi, lib

client = clientApi.UaClient()
retval = client.connect(b"opc.tcp://christian-ThinkPad:4840/")

# node 1
node1 = ffi.new("UA_NodeId*")
node1.namespaceIndex = ffi.cast("UA_UInt16", 1)
node1.identifierType = lib.UA_NODEIDTYPE_NUMERIC
node1.identifier.numeric = ffi.cast("UA_UInt32", 42)


qualified_name = ffi.new("UA_QualifiedName*")
qualified_name.namespaceIndex = ffi.cast("UA_UInt16", 1)
name = ffi.new("UA_String*", None)
name.length = ffi.cast("size_t", 5)
name.data = ffi.cast("UA_Byte*", 4)
qualified_name.name = name[0]

# node 2
node2 = ffi.new("UA_NodeId*")
node2.namespaceIndex = ffi.cast("UA_UInt16", 1)
node2.identifierType = lib.UA_NODEIDTYPE_NUMERIC
node2.identifier.numeric = ffi.cast("UA_UInt32", 42)


qualified_name2 = ffi.new("UA_QualifiedName*")
qualified_name2.namespaceIndex = ffi.cast("UA_UInt16", 1)
name2 = ffi.new("UA_String*", None)
name2.length = ffi.cast("size_t", 5)
name2.data = ffi.cast("UA_Byte*", 4)
qualified_name2.name = name[0]


# browse name
qualified_name3 = ffi.new("UA_QualifiedName*")
qualified_name3.namespaceIndex = ffi.cast("UA_UInt16", 1)
name3 = ffi.new("UA_String*", None)
name3.length = ffi.cast("size_t", 5)
name3.data = ffi.cast("UA_Byte*", 4)
qualified_name3.name = name[0]


# node 4
node4 = ffi.new("UA_NodeId*")
node4.namespaceIndex = ffi.cast("UA_UInt16", 1)
node4.identifierType = lib.UA_NODEIDTYPE_NUMERIC
node4.identifier.numeric = ffi.cast("UA_UInt32", 42)


qualified_name4 = ffi.new("UA_QualifiedName*")
qualified_name4.namespaceIndex = ffi.cast("UA_UInt16", 1)
name4 = ffi.new("UA_String*", None)
name4.length = ffi.cast("size_t", 5)
name4.data = ffi.cast("UA_Byte*", 4)
qualified_name4.name = name[0]



client.add_variable_node(node1[0], node2[0], node2[0], qualified_name3[0], node4[0])
