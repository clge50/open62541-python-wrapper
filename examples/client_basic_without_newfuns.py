import sys

sys.path.append("../build/api")
import clientApi

from intermediateApi import ffi, lib

client = clientApi.UaClient()
retval = client.connect(b"opc.tcp://stellaluna:4840/")
node = ffi.new("UA_NodeId*")
node.namespaceIndex = ffi.cast("UA_UInt16", 1)

node.identifierType = lib.UA_NODEIDTYPE_NUMERIC
node.identifier.numeric = ffi.cast("UA_UInt32", 42)

new_node = ffi.new("UA_NodeId*")

qualified_name = ffi.new("UA_QualifiedName*")
qualified_name.namespaceIndex = ffi.cast("UA_UInt16", 1)
name = ffi.new("UA_String*")
name.length = ffi.cast("size_t", 5)
name.data = ffi.cast("UA_Byte*", 4)
qualified_name.name = name

