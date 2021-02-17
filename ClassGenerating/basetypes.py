# TODO: add UaExtensionObject, UaDataType

# +++++++++++++++++++ UaNodeIdType +++++++++++++++++++++++
class UaNodeIdType(UaType):
    UA_NODEIDTYPE_NUMERIC = 0
    UA_NODEIDTYPE_NUMERIC_TWO_BYTE = 1
    UA_NODEIDTYPE_NUMERIC_FOUR_BYTE = 2
    UA_NODEIDTYPE_STRING = 3
    UA_NODEIDTYPE_GUID = 4
    UA_NODEIDTYPE_BYTESTRING = 5

    val_to_string = dict([
        (0, "UA_NODEIDTYPE_NUMERIC"),
        (1, "UA_NODEIDTYPE_NUMERIC_TWO_BYTE"),
        (2, "UA_NODEIDTYPE_NUMERIC_FOUR_BYTE"),
        (3, "UA_NODEIDTYPE_STRING"),
        (4, "UA_NODEIDTYPE_GUID"),
        (5, "UA_NODEIDTYPE_BYTESTRING")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("enum UA_NodeIdType*"), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        if val in self.val_to_string.keys():
            self._p_value = val
            super().__init__(ffi.new("enum UA_NodeIdType*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaNodeIdType: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)

# +++++++++++++++++++ UaVariantStorageType +++++++++++++++++++++++
class UaVariantStorageType(UaType):
    UA_VARIANT_DATA = 0
    UA_VARIANT_DATA_NODELETE = 1

    val_to_string = dict([
        (0, "UA_VARIANT_DATA"),
        (1, "UA_VARIANT_DATA_NODELETE")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_VariantStorageType*"), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        if val in self.val_to_string.keys():
            self._p_value = val
            super().__init__(ffi.new("UA_VariantStorageType*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaVariantStorageType: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


# +++++++++++++++++++ UaExtensionObjectEncoding +++++++++++++++++++++++
class UaExtensionObjectEncoding(UaType):
    UA_EXTENSIONOBJECT_ENCODED_NOBODY     = 0
    UA_EXTENSIONOBJECT_ENCODED_BYTESTRING = 1
    UA_EXTENSIONOBJECT_ENCODED_XML        = 2
    UA_EXTENSIONOBJECT_DECODED            = 3
    UA_EXTENSIONOBJECT_DECODED_NODELETE   = 4

    val_to_string = dict([
        (0, "UA_EXTENSIONOBJECT_ENCODED_NOBODY    "),
        (1, "UA_EXTENSIONOBJECT_ENCODED_BYTESTRING"),
        (2, "UA_EXTENSIONOBJECT_ENCODED_XML       "),
        (3, "UA_EXTENSIONOBJECT_DECODED           "),
        (4, "UA_EXTENSIONOBJECT_DECODED_NODELETE  ")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_ExtensionObjectEncoding*"), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        if val in self.val_to_string.keys():
            self._p_value = val
            super().__init__(ffi.new("UA_ExtensionObjectEncoding*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaExtensionObjectEncoding: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


# +++++++++++++++++++ UaDataTypeKind +++++++++++++++++++++++
class UaDataTypeKind(UaType):
    UA_DATATYPEKIND_BOOLEAN = 0
    UA_DATATYPEKIND_SBYTE = 1
    UA_DATATYPEKIND_BYTE = 2
    UA_DATATYPEKIND_INT16 = 3
    UA_DATATYPEKIND_UINT16 = 4
    UA_DATATYPEKIND_INT32 = 5
    UA_DATATYPEKIND_UINT32 = 6
    UA_DATATYPEKIND_INT64 = 7
    UA_DATATYPEKIND_UINT64 = 8
    UA_DATATYPEKIND_FLOAT = 9
    UA_DATATYPEKIND_DOUBLE = 10
    UA_DATATYPEKIND_STRING = 11
    UA_DATATYPEKIND_DATETIME = 12
    UA_DATATYPEKIND_GUID = 13
    UA_DATATYPEKIND_BYTESTRING = 14
    UA_DATATYPEKIND_XMLELEMENT = 15
    UA_DATATYPEKIND_NODEID = 16
    UA_DATATYPEKIND_EXPANDEDNODEID = 17
    UA_DATATYPEKIND_STATUSCODE = 18
    UA_DATATYPEKIND_QUALIFIEDNAME = 19
    UA_DATATYPEKIND_LOCALIZEDTEXT = 20
    UA_DATATYPEKIND_EXTENSIONOBJECT = 21
    UA_DATATYPEKIND_DATAVALUE = 22
    UA_DATATYPEKIND_VARIANT = 23
    UA_DATATYPEKIND_DIAGNOSTICINFO = 24
    UA_DATATYPEKIND_DECIMAL = 25
    UA_DATATYPEKIND_ENUM = 26
    UA_DATATYPEKIND_STRUCTURE = 27
    UA_DATATYPEKIND_OPTSTRUCT = 28
    UA_DATATYPEKIND_UNION = 29
    UA_DATATYPEKIND_BITFIELDCLUSTER = 30

    val_to_string = dict([
        (0, "UA_DATATYPEKIND_BOOLEAN"),
        (1, "UA_DATATYPEKIND_SBYTE"),
        (2, "UA_DATATYPEKIND_BYTE"),
        (3, "UA_DATATYPEKIND_INT16"),
        (4, "UA_DATATYPEKIND_UINT16"),
        (5, "UA_DATATYPEKIND_INT32"),
        (6, "UA_DATATYPEKIND_UINT32"),
        (7, "UA_DATATYPEKIND_INT64"),
        (8, "UA_DATATYPEKIND_UINT64"),
        (9, "UA_DATATYPEKIND_FLOAT"),
        (10, "UA_DATATYPEKIND_DOUBLE"),
        (11, "UA_DATATYPEKIND_STRING"),
        (12, "UA_DATATYPEKIND_DATETIME"),
        (13, "UA_DATATYPEKIND_GUID"),
        (14, "UA_DATATYPEKIND_BYTESTRING"),
        (15, "UA_DATATYPEKIND_XMLELEMENT"),
        (16, "UA_DATATYPEKIND_NODEID"),
        (17, "UA_DATATYPEKIND_EXPANDEDNODEID"),
        (18, "UA_DATATYPEKIND_STATUSCODE"),
        (19, "UA_DATATYPEKIND_QUALIFIEDNAME"),
        (20, "UA_DATATYPEKIND_LOCALIZEDTEXT"),
        (21, "UA_DATATYPEKIND_EXTENSIONOBJECT"),
        (22, "UA_DATATYPEKIND_DATAVALUE"),
        (23, "UA_DATATYPEKIND_VARIANT"),
        (24, "UA_DATATYPEKIND_DIAGNOSTICINFO"),
        (25, "UA_DATATYPEKIND_DECIMAL"),
        (26, "UA_DATATYPEKIND_ENUM"),
        (27, "UA_DATATYPEKIND_STRUCTURE"),
        (28, "UA_DATATYPEKIND_OPTSTRUCT"),
        (29, "UA_DATATYPEKIND_UNION"),
        (30, "UA_DATATYPEKIND_BITFIELDCLUSTER")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_DataTypeKind*"), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        if val in self.val_to_string.keys():
            self._p_value = val
            super().__init__(ffi.new("UA_DataTypeKind*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaDataTypeKind: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


################################################################

# +++++++++++++++++++ UaString +++++++++++++++++++++++
class UaString(UaType):
    def __init__(self, string="", is_pointer=False, val=ffi.new("UA_String*")):
        if string != "":
            val = lib.UA_String_fromChars(bytes(string, 'utf-8'))
        super().__init__(val, is_pointer)
        self._length = SizeT(val=val.length)
        self._data = UaByte(val=val.data, is_pointer=True)

    @property
    def length(self):
        return self._length

    @property
    def data(self):
        return self._data

    def __eq__(self, ua_string):
        return lib.UA_String_equal(self._value, ua_string._value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def equal_ignore_case(self, ua_string):
        return lib.UA_String_equal_ignorecase(self._value, ua_string._value)

    def to_string(self):
        return ffi.string(ffi.cast(f"char[{self.length}]", self.data), self.length).decode("utf-8")

    def __str__(self):
        return "UaString: " + self.to_string()

    def str_helper(self, n: int):
        return "\t" * n + str(self)


# +++++++++++++++++++ UaByteString +++++++++++++++++++++++
class UaByteString(UaType):
    def __init__(self, string="", is_pointer=False, val=ffi.new("UA_ByteString*")):
        if string != "":
            val = lib.UA_String_fromChars(bytes(string, 'utf-8'))
        super().__init__(val, is_pointer)
        self._length = SizeT(val=val.length)
        self._data = UaByte(val=val.data, is_pointer=True)

    @property
    def length(self):
        return self._length

    @property
    def data(self):
        return self._data

    def __eq__(self, ua_string):
        return lib.UA_String_equal(self._value, ua_string._value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def equal_ignore_case(self, ua_string):
        return lib.UA_String_equal_ignorecase(self._value, ua_string._value)

    def to_string(self):
        return ffi.string(ffi.cast(f"char[{self.length}]", self.data), self.length).decode("utf-8")

    def __str__(self):
        return "UaByteString: " + self.to_string()

    def str_helper(self, n: int):
        return "\t" * n + str(self)


# +++++++++++++++++++ UaXmlElement +++++++++++++++++++++++
class UaXmlElement(UaType):
    def __init__(self, string="", is_pointer=False, val=ffi.new("UA_XmlElement*")):
        if string != "":
            val = lib.UA_String_fromChars(bytes(string, 'utf-8'))
        super().__init__(val, is_pointer)
        self._length = SizeT(val=val.length)
        self._data = UaByte(val=val.data, is_pointer=True)

    @property
    def length(self):
        return self._length

    @property
    def data(self):
        return self._data

    def __eq__(self, ua_string):
        return lib.UA_String_equal(self._value, ua_string._value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def equal_ignore_case(self, ua_string):
        return lib.UA_String_equal_ignorecase(self._value, ua_string._value)

    def to_string(self):
        return ffi.string(ffi.cast(f"char[{self.length}]", self.data), self.length).decode("utf-8")

    def __str__(self):
        return "UaXmlElement: " + self.to_string()
    
    def str_helper(self, n: int):
        return "\t"*n + str(self)


# +++++++++++++++++++ UaGuid +++++++++++++++++++++++
class UaGuid(UaType):
    NULL = lib.UA_GUID_NULL
    
    def __init__(self, string="", is_pointer=False, val=ffi.new("UA_Guid*")):
        if string != "":
            val = lib.UA_GUID(bytes(string, 'utf-8'))
            if val == UaGuid.NULL:
                raise ValueError(
                    f""""{string}" has to be formated like: 
"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", with X in [0..9, A..F]""")
        super().__init__(val, is_pointer)
        self._data1 = UaUInt32(val=val.data1)
        self._data2 = UaUInt16(val=val.data2)
        self._data3 = UaUInt16(val=val.data3)
        self._data4 = UaByte(val=val.data4, is_pointer=True)

    @staticmethod
    def random():
        # TODO: does there have to be a seed set before using the random fun?
        # lib.UA_random_seed(ffi.new("UA_UInt64*", ))
        return UaGuid(lib.UA_Guid_random())
    

    @property
    def data1(self):
        return self._data1

    @data1.setter
    def data1(self, val):
        self._data1 = val
        self._value.data1 = val.value

    @property
    def data2(self):
        return self._data2

    @data2.setter
    def data2(self, val):
        self._data2 = val
        self._value.data2 = val.value

    @property
    def data3(self):
        return self._data3

    @data3.setter
    def data3(self, val):
        self._data3 = val
        self._value.data3 = val.value

    @property
    def data4(self):
        return self._data4

    #byte array of length 8
    @data4.setter
    def data4(self, val):
        self._data4 = val
        self._value.data4 = val.value

    def __eq__(self, other):
        return lib.UA_Guid_equal(self._value, other._value)

    def __ne__(self, other):
        return not self.__eq__(other)


    def __str__(self):
        d1 = '{0:0{1}X}'.format(self._data1.value,8)
        d2 = '{0:0{1}X}'.format(self._data2.value,4)
        d3 = '{0:0{1}X}'.format(self._data3.value,4)
        d4 =""
        for i in range(2):
            d4 += '{0:0{1}X}'.format(self._data4.value[i],2)
        d5 = ""
        for i in range(2, 8):
            d5 += '{0:0{1}X}'.format(self._data4.value[i],2)

        return "UaGuid: " + f"{d1}-{d2}-{d3}-{d4}-{d5}"
    
    def str_helper(self, n: int):
        return "\t" * n + str(self)

# +++++++++++++++++++ UaNodeId +++++++++++++++++++++++
class UaNodeId(UaType):
    NULL = lib.UA_NODEID_NULL

    def __init__(self, ns_index=None, ident=None, is_pointer=False, val=ffi.new("UA_NodeId*")):
        if ns_index is int:
            if ident is int:
                val = lib.UA_NODEID_NUMERIC(UaUInt16(ns_index), UaUInt32(ident))
            elif ident is UaUInt32:
                val = lib.UA_NODEID_NUMERIC(UaUInt16(ns_index), ident)
            elif ident is str:
                val = lib.UA_NODEID_STRING_ALLOC(UaUInt16(ns_index), bytes(ident, 'utf-8'))
            elif ident is bytearray:
                val = lib.UA_NODEID_BYTESTRING_ALLOC(UaUInt16(ns_index), ident)
            elif ident is UaString:
                val = lib.UA_NODEID_STRING_ALLOC(UaUInt16(ns_index), bytes(str(ident), 'utf-8'))
            elif ident is UaGuid:
                val = lib.A_NODEID_GUID(UaUInt16(ns_index), ident)
            elif ident is UaByteString:
                val = lib.UA_NODEID_BYTESTRING_ALLOC(UaUInt16(ns_index), bytes(str(ident), 'utf-8'))
            else:
                raise TypeError(f"ident={ident} hast invalid type, must be int, UaUInt32, "
                                f"str, bytearray, UaString, UaGuid or UaByteString")
        elif ns_index is UaUInt16:
            if ident is int:
                val = lib.UA_NODEID_NUMERIC(ns_index, UaUInt32(ident))
            elif ident is UaUInt32:
                val = lib.UA_NODEID_NUMERIC(ns_index, ident)
            elif ident is str:
                val = lib.UA_NODEID_STRING_ALLOC(ns_index, bytes(ident, 'utf-8'))
            elif ident is bytearray:
                val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index, ident)
            elif ident is UaString:
                val = lib.UA_NODEID_STRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
            elif ident is UaGuid:
                val = lib.A_NODEID_GUID(ns_index, ident)
            elif ident is UaByteString:
                val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
            else:
                raise TypeError(f"ident={ident} hast invalid type, must be int, UaUInt32, "
                                f"str, bytearray, UaString, UaGuid or UaByteString")
        else:
            raise TypeError(f"ns_index={ns_index} hast invalid type, must be UaUInt16 or int")

        super().__init__(val, is_pointer)
        self._namespace_index = UaUInt16(val=val.namespaceIndex)
        self._identifier_type = UaNodeIdType(val=val.identifierType)
        cases = {
            0: lambda: UaUInt32(val=val.identifier),
            1: lambda: UaUInt32(val=val.identifier),
            2: lambda: UaUInt32(val=val.identifier),
            3: lambda: UaString(val=val.identifier),
            4: lambda: UaGuid(val=val.identifier),
            5: lambda: UaByteString(val=val.identifier),
        }
        self._identifier = cases[self._identifierType]

    @property
    def namespace_index(self):
        return self._namespace_index

    @namespace_index.setter
    def namespace_index(self, val):
        self._namespace_index = val
        self._value.namespaceIndex = val.value

    @property
    def identifier_type(self):
        return self._identifier_type

    @identifier_type.setter
    def identifier_type(self, val):
        self._identifier_type = val
        self._value.identifierType = val.value

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, val):
        self._identifier = val
        self._value.identifier = val.value

    def __str__(self):
        return ("UaNodeId:\n" +
                self._namespace_index.str_helper(1) +
                self._identifier_type.str_helper(1) +
                self._identifier.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaNodeId:\n" +
                self._namespace_index.str_helper(n + 1) +
                self._identifier_type.str_helper(n + 1) +
                self._identifier.str_helper(n + 1))
    
    def __eq__(self, other):
        return lib.UA_NodeId_equal(self._value, other._value)

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def is_null(self):
        return lib.UA_NodeId_isNull(self._value)



# +++++++++++++++++++ UaExpandedNodeId +++++++++++++++++++++++
class UaExpandedNodeId(UaType):
    NULL = lib.UA_EXPANDEDNODEID_NULL

    def __init__(self, ns_index=None, ident=None, val=ffi.new("UA_ExpandedNodeId*")):
        if ns_index is int:
            if ident is int:
                val = lib.UA_EXPANDEDNODEID_NUMERIC(UaUInt16(ns_index), UaUInt32(ident))
            elif ident is UaUInt32:
                val = lib.UA_EXPANDEDNODEID_NUMERIC(UaUInt16(ns_index), ident)
            elif ident is str:
                val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(UaUInt16(ns_index), bytes(ident, 'utf-8'))
            elif ident is bytearray:
                val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(UaUInt16(ns_index), ident)
            elif ident is UaString:
                val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(UaUInt16(ns_index), bytes(str(ident), 'utf-8'))
            elif ident is UaGuid:
                val = lib.UA_EXPANDEDNODEID_STRING_GUID(UaUInt16(ns_index), ident)
            elif ident is UaByteString:
                val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(UaUInt16(ns_index), bytes(str(ident), 'utf-8'))
            else:
                raise TypeError(f"ident={ident} hast invalid type, must be int, UaUInt32, "
                                f"str, bytearray, UaString, UaGuid or UaByteString")
        elif ns_index is UaUInt16:
            if ident is int:
                val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index, UaUInt32(ident))
            elif ident is UaUInt32:
                val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index, ident)
            elif ident is str:
                val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index, bytes(ident, 'utf-8'))
            elif ident is bytearray:
                val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index, ident)
            elif ident is UaString:
                val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
            elif ident is UaGuid:
                val = lib.UA_EXPANDEDNODEID_STRING_GUID(ns_index, ident)
            elif ident is UaByteString:
                val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
            else:
                raise TypeError(f"ident={ident} hast invalid type, must be int, UaUInt32, "
                                f"str, bytearray, UaString, UaGuid or UaByteString")
        else:
            raise TypeError(f"ns_index={ns_index} hast invalid type, must be UaUInt16 or int")

        super().__init__(val, is_pointer)
        self._node_id = UaNodeId(val=val.nodeId)
        self._namespace_uri = UaString(val=val.namespaceUri)
        self._server_index = UaUInt32(val=val.serverIndex)

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val.value

    @property
    def namespace_uri(self):
        return self._namespace_uri

    @namespace_uri.setter
    def namespace_uri(self, val):
        self._namespace_uri = val
        self._value.namespaceUri = val.value

    @property
    def server_index(self):
        return self._server_index

    @server_index.setter
    def server_index(self, val):
        self._server_index = val
        self._value.serverIndex = val.value

    def __str__(self):
        return ("UaExpandedNodeId:\n" + 
                self._node_id.str_helper(1) +
                self._namespace_uri.str_helper(1) +
                self._server_index.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaExpandedNodeId:\n" + 
                self._node_id.str_helper(n+1) +
                self._namespace_uri.str_helper(n+1) +
                self._server_index.str_helper(n+1))

    def is_local(self):
        return lib.UA_ExpandedNodeId_isLocal(self._value)

    def __eq__(self, other):
        return lib.UA_ExpandedNodeId_equal(self._value, other._value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return lib.UA_ExpandedNodeId_order(self._value, other._value) == 1

    def __lt__(self, other):
        return lib.UA_ExpandedNodeId_order(self._value, other._value) == -1

    def __ge__(self, other):
        return lib.UA_ExpandedNodeId_order(self._value, other._value) in [1, 0]

    def __le__(self, other):
        return lib.UA_ExpandedNodeId_order(self._value, other._value) in [-1, 0]

    def __hash__(self):
        return lib.UA_ExpandedNodeId_hash(self._value)


# +++++++++++++++++++ UaQualifiedName +++++++++++++++++++++++
class UaQualifiedName(UaType):
    def __init__(self, ns_index=None, string=None , val=ffi.new("UA_QualifiedName*"), is_pointer=False):
        if ns_index is not None and string is not None:
            if ns_index is int:
                if string is str:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ffi.cast("UA_UInt16", ns_index), bytes(string, "utf-8"))
                if string is UaString:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ffi.cast("UA_UInt16", ns_index), bytes(str(string), "utf-8"))
                else:
                    raise AttributeError(f"string={string} has to be str or UaString")
            if ns_index is UaUInt16:
                if string is str:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index, bytes(string, "utf-8"))
                if string is UaString:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index, bytes(str(string), "utf-8"))
                else:
                    raise AttributeError(f"string={string} has to be str or UaString")
            else:
                raise AttributeError(f"ns_index={ns_index} has to be int or UaUInt16")

        super().__init__(val, is_pointer)
        self._namespace_index = UaUInt16(val=val.namespaceIndex)
        self._name = UaString(val=val.name)
    

    @property
    def namespace_index(self):
        return self._namespace_index

    @namespace_index.setter
    def namespace_index(self, val):
        self._namespace_index = val
        self._value.namespace_index = val.value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val
        self._value.name = val.value

    def __str__(self):
        return ("UaQualifiedName:\n" + 
                self._namespace_index.str_helper(1) +
                self._name.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaQualifiedName:\n" + 
                self._namespace_index.str_helper(n+1) +
                self._name.str_helper(n+1))

    def is_null(self):
        return lib.UA_QualifiedName_isNull(self._value)

    def __hash__(self):
        return lib.UA_QualifiedName_hash(self._value)

    def __eq__(self, other):
        return lib.UA_QualifiedName_equal(self._value, other._value)


# +++++++++++++++++++ UaLocalizedText +++++++++++++++++++++++
class UaLocalizedText(UaType):
    def __init__(self, locale=None, text=None, val=ffi.new("UA_LocalizedText*"), is_pointer=False):
        if locale is not None and text is not None:
            if locale is str:
                if text is str:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale, "utf-8"), bytes(text, "utf-8"))
                if text is UaString:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale, "utf-8"), bytes(str(text), "utf-8"))
                else:
                    raise AttributeError(f"text={text} has to be str or UaString")
            if locale is UaString:
                if text is str:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(str(locale), "utf-8"), bytes(text, "utf-8"))
                if text is UaString:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(str(locale), "utf-8"), bytes(str(text), "utf-8"))
                else:
                    raise AttributeError(f"text={text} has to be str or UaString")
            else:
                raise AttributeError(f"locale={locale} has to be str or UaUInt16")
        super().__init__(val, is_pointer)
        self._locale = UaString(val=val.locale)
        self._text = UaString(val=val.text)

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, val):
        self._locale = val
        self._value.locale = val.value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val
        self._value.text = val.value

    def __str__(self):
        return ("UaLocalizedText:\n" + 
                self._locale.str_helper(1) +
                self._text.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaLocalizedText:\n" + 
                self._locale.str_helper(n+1) +
                self._text.str_helper(n+1))


# +++++++++++++++++++ UaNumericRangeDimension +++++++++++++++++++++++
class UaNumericRangeDimension(UaType):
    def __init__(self, val=ffi.new("UA_NumericRangeDimension*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._min = UaUInt32(val=val.min)
        self._max = UaUInt32(val=val.max)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, val):
        self._min = val
        self._value.min = val.value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, val):
        self._max = val
        self._value.max = val.value

    def __str__(self):
        return ("UaNumericRangeDimension:\n" + 
                self._min.str_helper(1) +
                self._max.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaNumericRangeDimension:\n" + 
                self._min.str_helper(n+1) +
                self._max.str_helper(n+1))


# +++++++++++++++++++ UaNumericRange +++++++++++++++++++++++
class UaNumericRange(UaType):
    def __init__(self, val=ffi.new("UA_NumericRange*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._dimension_size = SizeT(val=val.dimensionsSize)
        self._dimension = UaNumericRangeDimension(val=val.dimensions, is_pointer=True)

    @property
    def dimension_size(self):
        return self._dimension_size

    @dimension_size.setter
    def dimension_size(self, val):
        self._dimension_size = val
        self._value.dimensionsSize = val.value

    @property
    def dimension(self):
        return self._max

    @dimension.setter
    def dimension(self, val):
        self._dimension = val
        self._value.dimension = val.value

    def __str__(self):
        return ("UaNumericRangeDimension:\n" +
                self._dimension_size.str_helper(1) +
                self._dimension.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaNumericRangeDimension:\n" +
                self._dimension_size.str_helper(n + 1) +
                self._dimension.str_helper(n + 1))


# +++++++++++++++++++ UaVariant +++++++++++++++++++++++
class UaVariant(UaType):
    def __init__(self, val=ffi.new("UA_Variant*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._type = UaDataType(val=val.type, is_pointer=True)
        self._storage_type = UaVariantStorageType(val=val.storageType)
        self._array_length = SizeT(val=val.arrayLength)
        self._data = SizeT(val=val.data, is_pointer=True)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
    

    @property
    def type(self):
        return self._ua_data_type

    @type.setter
    def type(self, val):
        self.type = val
        self._value.type = val.value

    @property
    def storage_type(self):
        return self._storage_type

    @storage_type.setter
    def storage_type(self, val):
        self._storage_type = val
        self._value.storageType = val.value

    @property
    def array_length(self):
        return self._array_length

    @array_length.setter
    def array_length(self, val):
        self._array_length = val
        self._value.arrayLength = val.value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        self._data = val
        self._value.data = val.value

    @property
    def array_dimensions_size(self):
        return self._array_dimensions_size

    @array_dimensions_size.setter
    def array_dimensions_size(self, val):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val.value

    @property
    def array_dimensions(self):
        return self._array_dimensions

    @array_dimensions.setter
    def array_dimensions(self, val):
        self._array_dimensions = val
        self._value.arrayDimensions = val.value

    def __str__(self):
        return ("UaVariant:\n" + 
                self._ua_data_type.str_helper(1) +
                self._storage_type.str_helper(1) +
                self._array_length.str_helper(1) +
                self._data.str_helper(1) +
                self._array_dimensions_size.str_helper(1) +
                self._array_dimensions.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaVariant:\n" + 
                self._ua_data_type.str_helper(n+1) +
                self._storage_type.str_helper(n+1) +
                self._array_length.str_helper(n+1) +
                self._data.str_helper(n+1) +
                self._array_dimensions_size.str_helper(n+1) +
                self._array_dimensions.str_helper(n+1))

    def is_empty(self):
        lib.UA_Variant_isEmpty(self._value)

    def is_scalar(self):
        lib.UA_Variant_isScalar(self._value)

    def has_scalar_type(self, data_type: UaDataType):
        lib.UA_Variant_hasScalarType(self._value, data_type._ref())

    def has_scalar_type(self, data_type: UaDataType):
        lib.UA_Variant_hasArrayType(self._value, data_type._ref())

    def _set_attributes(self):
        self._type = self._value.type
        self._storage_type = self._value.storageType
        self._array_length = self._value.arrayLength
        self._data = self._value.data
        self._array_dimensions_size = self._value.arrayDimensionsSize
        self._array_dimensions = self._value.arrayDimensions

    def set_scalar(self, data, data_type: UaDataType):
        lib.UA_Variant_setScalarCopy(self.value, ffi.new_handle(data), data_type._ref())
        self._set_attributes()

    def set_array(self, array, size, data_type: UaDataType):
        if size is int:
            size = SizeT(size)
        if size is not SizeT:
            raise AttributeError(f"size={size} has to be int or SizeT")
        status_code = lib.UA_Variant_setArrayCopy(self._value, ffi.new_handle(array), size._deref(), data_type._ref())
        status_code = UaStatusCode(status_code)
        if status_code.is_good():
            self._set_attributes()
        else:
            raise Exception(f"An Error occured - {str(status_code)}")

    def copy_range_to(self, variant, num_range: UaNumericRange):
        status_code = lib.UA_Variant_copyRange(self._value, variant._ref(), num_range._deref())
        status_code = UaStatusCode(status_code)
        if status_code.is_good():
            self._set_attributes()
        else:
            raise AttributeError(f"An Error occured - {str(status_code)}")

    def set_range_copy(self, array, size, num_range: UaNumericRange):
        if size is int:
            size = SizeT(size)
        if size is not SizeT:
            raise AttributeError(f"size={size} has to be int or SizeT")
        status_code = lib.UA_Variant_setRangeCopy(self._value, ffi.new_handle(array), size, num_range._deref())
        status_code = UaStatusCode(status_code)
        if status_code.is_good():
            self._set_attributes()
        else:
            raise AttributeError(f"An Error occured - {str(status_code)}")

# +++++++++++++++++++ UaExtensionObject +++++++++++++++++++++++

# +++++++++++++++++++ UaDataValue +++++++++++++++++++++++
class UaDataValue(UaType):
    def __init__(self, val=ffi.new("UA_DataValue*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._ = UaBoolean(val=val.)
        self._status = UaStatusCode(val=val.status)
        self._has_value = UaBoolean(val=val.has_value)
        self._has_status = UaBoolean(val=val.has_status)
        self._has_source_timestamp = UaBoolean(val=val.has_source_timestamp)
        self._has_server_timestamp = UaBoolean(val=val.has_server_timestamp)
    

    @property
    def (self):
        return self._

    @.setter
    def (self, val):
        self._ = val
        self._value. = val.value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val
        self._value.status = val.value

    @property
    def has_value(self):
        return self._has_value

    @has_value.setter
    def has_value(self, val):
        self._has_value = val
        self._value.has_value = val.value

    @property
    def has_status(self):
        return self._has_status

    @has_status.setter
    def has_status(self, val):
        self._has_status = val
        self._value.has_status = val.value

    @property
    def has_source_timestamp(self):
        return self._has_source_timestamp

    @has_source_timestamp.setter
    def has_source_timestamp(self, val):
        self._has_source_timestamp = val
        self._value.has_source_timestamp = val.value

    @property
    def has_server_timestamp(self):
        return self._has_server_timestamp

    @has_server_timestamp.setter
    def has_server_timestamp(self, val):
        self._has_server_timestamp = val
        self._value.has_server_timestamp = val.value

    def __str__(self):
        return ("UaDataValue:\n" + 
                self._.str_helper(1) +
                self._status.str_helper(1) +
                self._has_value.str_helper(1) +
                self._has_status.str_helper(1) +
                self._has_source_timestamp.str_helper(1) +
                self._has_server_timestamp.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDataValue:\n" + 
                self._.str_helper(n+1) +
                self._status.str_helper(n+1) +
                self._has_value.str_helper(n+1) +
                self._has_status.str_helper(n+1) +
                self._has_source_timestamp.str_helper(n+1) +
                self._has_server_timestamp.str_helper(n+1))

# +++++++++++++++++++ UaDataType +++++++++++++++++++++++


# +++++++++++++++++++ UaDataTypeArray +++++++++++++++++++++++
class UaDataTypeArray(UaType):
    def __init__(self, val=ffi.new("UaDataTypeArray*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._next = UaDataTypeArray(val=val.next, is_pointer=True)
        self._types_size = SizeT(val=val.typesSize)
        self._types = UaDataType(val=val.types, is_pointer=True)

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, val):
        self._next = val
        self._value.next = val.value

    @property
    def types_size(self):
        return self._types_size

    @types_size.setter
    def types_size(self, val):
        self._types_size = val
        self._value.typesSize = val.value

    @property
    def types(self):
        return self._has_status

    @types.setter
    def types(self, val):
        self._types = val
        self._value.types = val.value


    def __str__(self):
        return ("UaDataValue:\n" +
                self._next.str_helper(1) +
                self._types_size.str_helper(1) +
                self._types.str_helper(1))

    def str_helper(self, n: int):
        return ("UaDataValue:\n" +
                self._next.str_helper(n+1) +
                self._types_size.str_helper(n+1) +
                self._types.str_helper(n+1))
