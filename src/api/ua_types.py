from intermediateApi import ffi, lib


class UaNodeId:

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

    @staticmethod
    def order(ua_node_id_1, ua_node_id_2):
        return lib.UA_NodeId_order(ua_node_id_1, ua_node_id_2)


class UaQualifiedName:
    @staticmethod
    def new(namespace_index, string):
        return lib.UA_QUALIFIEDNAME(namespace_index, bytes(string, 'utf-8'))

    @staticmethod
    def equal(ua_qualified_name_1, ua_qualified_name_2):
        return lib.UA_QualifiedName_equal(ua_qualified_name_1, ua_qualified_name_2)


class UaString:
    @staticmethod
    def new(string):
        return lib.UA_String_fromChars(string)

    @staticmethod
    def equal(ua_string_1, ua_string_2):
        return lib.UA_String_equal(ua_string_1, ua_string_2)

    @staticmethod
    def equal_ignore_case(ua_string_1, ua_string_2):
        return lib.UA_String_equal_ignorecase(ua_string_1, ua_string_2)


    @staticmethod
    def to_string(ua_string):
        return ffi.string(ffi.cast(f"char[{ua_string.length}]", ua_string.data), ua_string.length).decode("utf-8")

class UaDateTime:
    @staticmethod
    def to_struct(ua_date_time):
        return lib.UA_DateTime_toStruct(ua_date_time)

    @staticmethod
    def from_struct(ua_date_time_struct):
        return lib.UA_DateTime_fromStruct(ua_date_time_struct)


class UaGuid:
    @staticmethod
    def equal(ua_guid_1, ua_guid_2):
        return lib.UA_Guid_equal(ua_guid_1, ua_guid_2)

    @staticmethod
    def random():
        return lib.UA_Guid_random()


class UaExtensionObject:
    @staticmethod
    def set_value(ua_extension_object, p, ua_data_type):
        return lib.UA_ExtensionObject_setValue(ua_extension_object, p, ua_data_type)

    @staticmethod
    def set_value_no_delete(ua_extension_object, p, ua_data_type):
        return lib.UA_ExtensionObject_setValueNoDelete(ua_extension_object, p, ua_data_type)

    @staticmethod
    def set_value_no_copy(ua_extension_object, p, ua_data_type):
        return lib.UA_ExtensionObject_setValueCopy(ua_extension_object, p, ua_data_type)


class UaVariant:
    @staticmethod
    def set_scalar(ua_variant, p, ua_data_type):
        return lib.UA_Variant_setScalar(ua_variant, p, ua_data_type)

    @staticmethod
    def set_scalar_copy(ua_variant, p, ua_data_type):
        return lib.UA_Variant_setScalarCopy(ua_variant, p, ua_data_type)

    @staticmethod
    def set_array(ua_variant, array, array_size, ua_data_type):
        return lib.UA_Variant_setArray(ua_variant, array, array_size, ua_data_type)

    @staticmethod
    def set_array_copy(ua_variant, array, array_size, ua_data_type):
        return lib.UA_Variant_setArrayCopy(ua_variant, array, array_size, ua_data_type)


class UAGeneric:
    @staticmethod
    def new(ua_data_type):
        return lib.UA_new(ua_data_type)

    @staticmethod
    def is_numeric(ua_data_type):
        return lib.UA_DataType_isNumeric(ua_data_type)


class UaArray:
    @staticmethod
    def new(size, ua_data_type):
        return lib.UA_Array_new(size, ua_data_type)


class UaNumericRange:
    @staticmethod
    def parse(ua_numeric_range, ua_string):
        return lib.UA_NumericRange_parse(ua_numeric_range, ua_string)
