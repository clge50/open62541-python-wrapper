from intermediateApi import ffi, lib


class NodeId:

    @staticmethod
    def new_numeric(namespace_index, numeric):
        return lib.UA_NODEID_NUMERIC(namespace_index, numeric)

    @staticmethod
    def new_string(namespace_index, string):
        return lib.UA_NODEID_STRING(namespace_index, bytes(string, 'utf-8'))

    @staticmethod
    def new_guid(namespace_index, guid):
        return lib.UA_NODEID_GUID(namespace_index, guid)

    @staticmethod
    def new_byte_string(namespace_index, string):
        return lib.UA_NODEID_BYTESTRING(namespace_index, bytes(string, 'utf-8'))


class QualifiedName:
    @staticmethod
    def new(namespace_index, string):
        return lib.UA_QUALIFIEDNAME(namespace_index, bytes(string, 'utf-8'))