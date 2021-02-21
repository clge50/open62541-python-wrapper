
# -------------------------------------------------------------
# --------------------------- Enums ---------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaNodeIdType +++++++++++++++++++++++
class UaNodeIdType(UaType):
    UA_NODEIDTYPE_NUMERIC = 0
    UA_NODEIDTYPE_STRING = 3
    UA_NODEIDTYPE_GUID = 4
    UA_NODEIDTYPE_BYTESTRING = 5

    val_to_string = dict([
        (0, "UA_NODEIDTYPE_NUMERIC"),
        (3, "UA_NODEIDTYPE_STRING"),
        (4, "UA_NODEIDTYPE_GUID"),
        (5, "UA_NODEIDTYPE_BYTESTRING")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_NodeIdType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_NodeIdType", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaNodeIdType): {self.val_to_string[self._value]} ({str(self._value)})\n"


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
        else:
            super().__init__(ffi.cast("UA_VariantStorageType", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaVariantStorageType): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaExtensionObjectEncoding +++++++++++++++++++++++
class UaExtensionObjectEncoding(UaType):
    UA_EXTENSIONOBJECT_ENCODED_NOBODY = 0
    UA_EXTENSIONOBJECT_ENCODED_BYTESTRING = 1
    UA_EXTENSIONOBJECT_ENCODED_XML = 2
    UA_EXTENSIONOBJECT_DECODED = 3
    UA_EXTENSIONOBJECT_DECODED_NODELETE = 4

    val_to_string = dict([
        (0, "UA_EXTENSIONOBJECT_ENCODED_NOBODY"),
        (1, "UA_EXTENSIONOBJECT_ENCODED_BYTESTRING"),
        (2, "UA_EXTENSIONOBJECT_ENCODED_XML"),
        (3, "UA_EXTENSIONOBJECT_DECODED"),
        (4, "UA_EXTENSIONOBJECT_DECODED_NODELETE")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_ExtensionObjectEncoding*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_ExtensionObjectEncoding", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaExtensionObjectEncoding): {self.val_to_string[self._value]} ({str(self._value)})\n"


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
        else:
            super().__init__(ffi.cast("UA_DataTypeKind", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaDataTypeKind): {self.val_to_string[self._value]} ({str(self._value)})\n"



# -------------------------------------------------------------
# -------------------------- Structs --------------------------
# -------------------------------------------------------------
    
# +++++++++++++++++++ UaString +++++++++++++++++++++++
class UaString(UaType):
    def __init__(self, val=ffi.new("UA_String*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._length = SizeT(val=val.length, is_pointer=False)
        self._data = UaByte(val=val.data, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._length.__value[0] = _val(val.length)
        self._data.__value[0] = _val(val.data)
    
    @property
    def length(self):
        return self._length

    @property
    def data(self):
        return self._data
    
    @length.setter
    def length(self, val):
        self._length = val
        self._value.length = val._value

    @data.setter
    def data(self, val):
        self._data = val
        self._value.data = val._value

    def __str__(self, n=0):
        return ("(UaString) :\n" +
                "\t"*(n+1) + "length" + self._length.__str__(n+1) +
                "\t"*(n+1) + "data" + self._data.__str__(n+1) + "\n")


# +++++++++++++++++++ UaDateTimeStruct +++++++++++++++++++++++
class UaDateTimeStruct(UaType):
    def __init__(self, val=ffi.new("UA_DateTimeStruct*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._nano_sec = UaUInt16(val=val.nanoSec, is_pointer=False)
        self._micro_sec = UaUInt16(val=val.microSec, is_pointer=False)
        self._milli_sec = UaUInt16(val=val.milliSec, is_pointer=False)
        self._sec = UaUInt16(val=val.sec, is_pointer=False)
        self._min = UaUInt16(val=val.min, is_pointer=False)
        self._hour = UaUInt16(val=val.hour, is_pointer=False)
        self._day = UaUInt16(val=val.day, is_pointer=False)
        self._month = UaUInt16(val=val.month, is_pointer=False)
        self._year = UaUInt16(val=val.year, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._nano_sec.__value[0] = _val(val.nanoSec)
        self._micro_sec.__value[0] = _val(val.microSec)
        self._milli_sec.__value[0] = _val(val.milliSec)
        self._sec.__value[0] = _val(val.sec)
        self._min.__value[0] = _val(val.min)
        self._hour.__value[0] = _val(val.hour)
        self._day.__value[0] = _val(val.day)
        self._month.__value[0] = _val(val.month)
        self._year.__value[0] = _val(val.year)
    
    @property
    def nano_sec(self):
        return self._nano_sec

    @property
    def micro_sec(self):
        return self._micro_sec

    @property
    def milli_sec(self):
        return self._milli_sec

    @property
    def sec(self):
        return self._sec

    @property
    def min(self):
        return self._min

    @property
    def hour(self):
        return self._hour

    @property
    def day(self):
        return self._day

    @property
    def month(self):
        return self._month

    @property
    def year(self):
        return self._year
    
    @nano_sec.setter
    def nano_sec(self, val):
        self._nano_sec = val
        self._value.nanoSec = val._value

    @micro_sec.setter
    def micro_sec(self, val):
        self._micro_sec = val
        self._value.microSec = val._value

    @milli_sec.setter
    def milli_sec(self, val):
        self._milli_sec = val
        self._value.milliSec = val._value

    @sec.setter
    def sec(self, val):
        self._sec = val
        self._value.sec = val._value

    @min.setter
    def min(self, val):
        self._min = val
        self._value.min = val._value

    @hour.setter
    def hour(self, val):
        self._hour = val
        self._value.hour = val._value

    @day.setter
    def day(self, val):
        self._day = val
        self._value.day = val._value

    @month.setter
    def month(self, val):
        self._month = val
        self._value.month = val._value

    @year.setter
    def year(self, val):
        self._year = val
        self._value.year = val._value

    def __str__(self, n=0):
        return ("(UaDateTimeStruct) :\n" +
                "\t"*(n+1) + "nano_sec" + self._nano_sec.__str__(n+1) +
                "\t"*(n+1) + "micro_sec" + self._micro_sec.__str__(n+1) +
                "\t"*(n+1) + "milli_sec" + self._milli_sec.__str__(n+1) +
                "\t"*(n+1) + "sec" + self._sec.__str__(n+1) +
                "\t"*(n+1) + "min" + self._min.__str__(n+1) +
                "\t"*(n+1) + "hour" + self._hour.__str__(n+1) +
                "\t"*(n+1) + "day" + self._day.__str__(n+1) +
                "\t"*(n+1) + "month" + self._month.__str__(n+1) +
                "\t"*(n+1) + "year" + self._year.__str__(n+1) + "\n")


# +++++++++++++++++++ UaGuid +++++++++++++++++++++++
class UaGuid(UaType):
    def __init__(self, val=ffi.new("UA_Guid*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._data1 = UaUInt32(val=val.data1, is_pointer=False)
        self._data2 = UaUInt16(val=val.data2, is_pointer=False)
        self._data3 = UaUInt16(val=val.data3, is_pointer=False)
        self._data4 = UaByte(val=val.data4, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._data1.__value[0] = _val(val.data1)
        self._data2.__value[0] = _val(val.data2)
        self._data3.__value[0] = _val(val.data3)
        self._data4.__value[0] = _val(val.data4)
    
    @property
    def data1(self):
        return self._data1

    @property
    def data2(self):
        return self._data2

    @property
    def data3(self):
        return self._data3

    @property
    def data4(self):
        return self._data4
    
    @data1.setter
    def data1(self, val):
        self._data1 = val
        self._value.data1 = val._value

    @data2.setter
    def data2(self, val):
        self._data2 = val
        self._value.data2 = val._value

    @data3.setter
    def data3(self, val):
        self._data3 = val
        self._value.data3 = val._value

    @data4.setter
    def data4(self, val):
        self._data4 = val
        self._value.data4 = val._value

    def __str__(self, n=0):
        return ("(UaGuid) :\n" +
                "\t"*(n+1) + "data1" + self._data1.__str__(n+1) +
                "\t"*(n+1) + "data2" + self._data2.__str__(n+1) +
                "\t"*(n+1) + "data3" + self._data3.__str__(n+1) +
                "\t"*(n+1) + "data4" + self._data4.__str__(n+1) + "\n")


# +++++++++++++++++++ UaExpandedNodeId +++++++++++++++++++++++
class UaExpandedNodeId(UaType):
    def __init__(self, val=ffi.new("UA_ExpandedNodeId*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
        self._namespace_uri = UaString(val=val.namespaceUri, is_pointer=False)
        self._server_index = UaUInt32(val=val.serverIndex, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._node_id.__value[0] = _val(val.nodeId)
        self._namespace_uri.__value[0] = _val(val.namespaceUri)
        self._server_index.__value[0] = _val(val.serverIndex)
    
    @property
    def node_id(self):
        return self._node_id

    @property
    def namespace_uri(self):
        return self._namespace_uri

    @property
    def server_index(self):
        return self._server_index
    
    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val._value

    @namespace_uri.setter
    def namespace_uri(self, val):
        self._namespace_uri = val
        self._value.namespaceUri = val._value

    @server_index.setter
    def server_index(self, val):
        self._server_index = val
        self._value.serverIndex = val._value

    def __str__(self, n=0):
        return ("(UaExpandedNodeId) :\n" +
                "\t"*(n+1) + "node_id" + self._node_id.__str__(n+1) +
                "\t"*(n+1) + "namespace_uri" + self._namespace_uri.__str__(n+1) +
                "\t"*(n+1) + "server_index" + self._server_index.__str__(n+1) + "\n")


# +++++++++++++++++++ UaQualifiedName +++++++++++++++++++++++
class UaQualifiedName(UaType):
    def __init__(self, val=ffi.new("UA_QualifiedName*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._namespace_index = UaUInt16(val=val.namespaceIndex, is_pointer=False)
        self._name = UaString(val=val.name, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._namespace_index.__value[0] = _val(val.namespaceIndex)
        self._name.__value[0] = _val(val.name)
    
    @property
    def namespace_index(self):
        return self._namespace_index

    @property
    def name(self):
        return self._name
    
    @namespace_index.setter
    def namespace_index(self, val):
        self._namespace_index = val
        self._value.namespaceIndex = val._value

    @name.setter
    def name(self, val):
        self._name = val
        self._value.name = val._value

    def __str__(self, n=0):
        return ("(UaQualifiedName) :\n" +
                "\t"*(n+1) + "namespace_index" + self._namespace_index.__str__(n+1) +
                "\t"*(n+1) + "name" + self._name.__str__(n+1) + "\n")


# +++++++++++++++++++ UaLocalizedText +++++++++++++++++++++++
class UaLocalizedText(UaType):
    def __init__(self, val=ffi.new("UA_LocalizedText*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._locale = UaString(val=val.locale, is_pointer=False)
        self._text = UaString(val=val.text, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._locale.__value[0] = _val(val.locale)
        self._text.__value[0] = _val(val.text)
    
    @property
    def locale(self):
        return self._locale

    @property
    def text(self):
        return self._text
    
    @locale.setter
    def locale(self, val):
        self._locale = val
        self._value.locale = val._value

    @text.setter
    def text(self, val):
        self._text = val
        self._value.text = val._value

    def __str__(self, n=0):
        return ("(UaLocalizedText) :\n" +
                "\t"*(n+1) + "locale" + self._locale.__str__(n+1) +
                "\t"*(n+1) + "text" + self._text.__str__(n+1) + "\n")


# +++++++++++++++++++ UaNumericRangeDimension +++++++++++++++++++++++
class UaNumericRangeDimension(UaType):
    def __init__(self, val=ffi.new("UA_NumericRangeDimension*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._min = UaUInt32(val=val.min, is_pointer=False)
        self._max = UaUInt32(val=val.max, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._min.__value[0] = _val(val.min)
        self._max.__value[0] = _val(val.max)
    
    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max
    
    @min.setter
    def min(self, val):
        self._min = val
        self._value.min = val._value

    @max.setter
    def max(self, val):
        self._max = val
        self._value.max = val._value

    def __str__(self, n=0):
        return ("(UaNumericRangeDimension) :\n" +
                "\t"*(n+1) + "min" + self._min.__str__(n+1) +
                "\t"*(n+1) + "max" + self._max.__str__(n+1) + "\n")


# +++++++++++++++++++ UaNumericRange +++++++++++++++++++++++
class UaNumericRange(UaType):
    def __init__(self, val=ffi.new("UA_NumericRange*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._dimensions_size = SizeT(val=val.dimensionsSize, is_pointer=False)
        self._dimensions = UaNumericRangeDimension(val=val.dimensions, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._dimensions_size.__value[0] = _val(val.dimensionsSize)
        self._dimensions.__value[0] = _val(val.dimensions)
    
    @property
    def dimensions_size(self):
        return self._dimensions_size

    @property
    def dimensions(self):
        return self._dimensions
    
    @dimensions_size.setter
    def dimensions_size(self, val):
        self._dimensions_size = val
        self._value.dimensionsSize = val._value

    @dimensions.setter
    def dimensions(self, val):
        self._dimensions = val
        self._value.dimensions = val._value

    def __str__(self, n=0):
        return ("(UaNumericRange) :\n" +
                "\t"*(n+1) + "dimensions_size" + self._dimensions_size.__str__(n+1) +
                "\t"*(n+1) + "dimensions" + self._dimensions.__str__(n+1) + "\n")


# +++++++++++++++++++ UaVariant +++++++++++++++++++++++
class UaVariant(UaType):
    def __init__(self, val=ffi.new("UA_Variant*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._type = UaDataType(val=val.type, is_pointer=True)
        self._storage_type = UaVariantStorageType(val=val.storageType, is_pointer=False)
        self._array_length = SizeT(val=val.arrayLength, is_pointer=False)
        self._data = void(val=val.data, is_pointer=True)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._type.__value[0] = _val(val.type)
        self._storage_type.__value[0] = _val(val.storageType)
        self._array_length.__value[0] = _val(val.arrayLength)
        self._data.__value[0] = _val(val.data)
        self._array_dimensions_size.__value[0] = _val(val.arrayDimensionsSize)
        self._array_dimensions.__value[0] = _val(val.arrayDimensions)
    
    @property
    def type(self):
        return self._type

    @property
    def storage_type(self):
        return self._storage_type

    @property
    def array_length(self):
        return self._array_length

    @property
    def data(self):
        return self._data

    @property
    def array_dimensions_size(self):
        return self._array_dimensions_size

    @property
    def array_dimensions(self):
        return self._array_dimensions
    
    @type.setter
    def type(self, val):
        self._type = val
        self._value.type = val._value

    @storage_type.setter
    def storage_type(self, val):
        self._storage_type = val
        self._value.storageType = val._value

    @array_length.setter
    def array_length(self, val):
        self._array_length = val
        self._value.arrayLength = val._value

    @data.setter
    def data(self, val):
        self._data = val
        self._value.data = val._value

    @array_dimensions_size.setter
    def array_dimensions_size(self, val):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._value

    @array_dimensions.setter
    def array_dimensions(self, val):
        self._array_dimensions = val
        self._value.arrayDimensions = val._value

    def __str__(self, n=0):
        return ("(UaVariant) :\n" +
                "\t"*(n+1) + "type" + self._type.__str__(n+1) +
                "\t"*(n+1) + "storage_type" + self._storage_type.__str__(n+1) +
                "\t"*(n+1) + "array_length" + self._array_length.__str__(n+1) +
                "\t"*(n+1) + "data" + self._data.__str__(n+1) +
                "\t"*(n+1) + "array_dimensions_size" + self._array_dimensions_size.__str__(n+1) +
                "\t"*(n+1) + "array_dimensions" + self._array_dimensions.__str__(n+1) + "\n")


# +++++++++++++++++++ UaDataValue +++++++++++++++++++++++
class UaDataValue(UaType):
    def __init__(self, val=ffi.new("UA_DataValue*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._value = UaVariant(val=val.value, is_pointer=False)
        self._source_timestamp = UaDateTime(val=val.sourceTimestamp, is_pointer=False)
        self._server_timestamp = UaDateTime(val=val.serverTimestamp, is_pointer=False)
        self._source_picoseconds = UaUInt16(val=val.sourcePicoseconds, is_pointer=False)
        self._server_picoseconds = UaUInt16(val=val.serverPicoseconds, is_pointer=False)
        self._status = UaStatusCode(val=val.status, is_pointer=False)
        self._has_value = UaBoolean(val=val.hasValue, is_pointer=False)
        self._has_status = UaBoolean(val=val.hasStatus, is_pointer=False)
        self._has_source_timestamp = UaBoolean(val=val.hasSourceTimestamp, is_pointer=False)
        self._has_server_timestamp = UaBoolean(val=val.hasServerTimestamp, is_pointer=False)
        self._has_source_picoseconds = UaBoolean(val=val.hasSourcePicoseconds, is_pointer=False)
        self._has_server_picoseconds = UaBoolean(val=val.hasServerPicoseconds, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._value.__value[0] = _val(val.value)
        self._source_timestamp.__value[0] = _val(val.sourceTimestamp)
        self._server_timestamp.__value[0] = _val(val.serverTimestamp)
        self._source_picoseconds.__value[0] = _val(val.sourcePicoseconds)
        self._server_picoseconds.__value[0] = _val(val.serverPicoseconds)
        self._status.__value[0] = _val(val.status)
        self._has_value.__value[0] = _val(val.hasValue)
        self._has_status.__value[0] = _val(val.hasStatus)
        self._has_source_timestamp.__value[0] = _val(val.hasSourceTimestamp)
        self._has_server_timestamp.__value[0] = _val(val.hasServerTimestamp)
        self._has_source_picoseconds.__value[0] = _val(val.hasSourcePicoseconds)
        self._has_server_picoseconds.__value[0] = _val(val.hasServerPicoseconds)
    
    @property
    def value(self):
        return self._value

    @property
    def source_timestamp(self):
        return self._source_timestamp

    @property
    def server_timestamp(self):
        return self._server_timestamp

    @property
    def source_picoseconds(self):
        return self._source_picoseconds

    @property
    def server_picoseconds(self):
        return self._server_picoseconds

    @property
    def status(self):
        return self._status

    @property
    def has_value(self):
        return self._has_value

    @property
    def has_status(self):
        return self._has_status

    @property
    def has_source_timestamp(self):
        return self._has_source_timestamp

    @property
    def has_server_timestamp(self):
        return self._has_server_timestamp

    @property
    def has_source_picoseconds(self):
        return self._has_source_picoseconds

    @property
    def has_server_picoseconds(self):
        return self._has_server_picoseconds
    
    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val._value

    @source_timestamp.setter
    def source_timestamp(self, val):
        self._source_timestamp = val
        self._value.sourceTimestamp = val._value

    @server_timestamp.setter
    def server_timestamp(self, val):
        self._server_timestamp = val
        self._value.serverTimestamp = val._value

    @source_picoseconds.setter
    def source_picoseconds(self, val):
        self._source_picoseconds = val
        self._value.sourcePicoseconds = val._value

    @server_picoseconds.setter
    def server_picoseconds(self, val):
        self._server_picoseconds = val
        self._value.serverPicoseconds = val._value

    @status.setter
    def status(self, val):
        self._status = val
        self._value.status = val._value

    @has_value.setter
    def has_value(self, val):
        self._has_value = val
        self._value.hasValue = val._value

    @has_status.setter
    def has_status(self, val):
        self._has_status = val
        self._value.hasStatus = val._value

    @has_source_timestamp.setter
    def has_source_timestamp(self, val):
        self._has_source_timestamp = val
        self._value.hasSourceTimestamp = val._value

    @has_server_timestamp.setter
    def has_server_timestamp(self, val):
        self._has_server_timestamp = val
        self._value.hasServerTimestamp = val._value

    @has_source_picoseconds.setter
    def has_source_picoseconds(self, val):
        self._has_source_picoseconds = val
        self._value.hasSourcePicoseconds = val._value

    @has_server_picoseconds.setter
    def has_server_picoseconds(self, val):
        self._has_server_picoseconds = val
        self._value.hasServerPicoseconds = val._value

    def __str__(self, n=0):
        return ("(UaDataValue) :\n" +
                "\t"*(n+1) + "value" + self._value.__str__(n+1) +
                "\t"*(n+1) + "source_timestamp" + self._source_timestamp.__str__(n+1) +
                "\t"*(n+1) + "server_timestamp" + self._server_timestamp.__str__(n+1) +
                "\t"*(n+1) + "source_picoseconds" + self._source_picoseconds.__str__(n+1) +
                "\t"*(n+1) + "server_picoseconds" + self._server_picoseconds.__str__(n+1) +
                "\t"*(n+1) + "status" + self._status.__str__(n+1) +
                "\t"*(n+1) + "has_value" + self._has_value.__str__(n+1) +
                "\t"*(n+1) + "has_status" + self._has_status.__str__(n+1) +
                "\t"*(n+1) + "has_source_timestamp" + self._has_source_timestamp.__str__(n+1) +
                "\t"*(n+1) + "has_server_timestamp" + self._has_server_timestamp.__str__(n+1) +
                "\t"*(n+1) + "has_source_picoseconds" + self._has_source_picoseconds.__str__(n+1) +
                "\t"*(n+1) + "has_server_picoseconds" + self._has_server_picoseconds.__str__(n+1) + "\n")


# +++++++++++++++++++ UaDataType +++++++++++++++++++++++
class UaDataType(UaType):
    def __init__(self, val=ffi.new("UA_DataType*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._type_id = UaNodeId(val=val.typeId, is_pointer=False)
        self._binary_encoding_id = UaNodeId(val=val.binaryEncodingId, is_pointer=False)
        self._mem_size = UaUInt16(val=val.memSize, is_pointer=False)
        self._type_index = UaUInt16(val=val.typeIndex, is_pointer=False)
        self._type_kind = UaUInt32(val=val.typeKind, is_pointer=False)
        self._pointer_free = UaUInt32(val=val.pointerFree, is_pointer=False)
        self._overlayable = UaUInt32(val=val.overlayable, is_pointer=False)
        self._members_size = UaUInt32(val=val.membersSize, is_pointer=False)
        self._members = UaDataTypeMember(val=val.members, is_pointer=True)
        self._type_name = CString(val=val.typeName, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._type_id.__value[0] = _val(val.typeId)
        self._binary_encoding_id.__value[0] = _val(val.binaryEncodingId)
        self._mem_size.__value[0] = _val(val.memSize)
        self._type_index.__value[0] = _val(val.typeIndex)
        self._type_kind.__value[0] = _val(val.typeKind)
        self._pointer_free.__value[0] = _val(val.pointerFree)
        self._overlayable.__value[0] = _val(val.overlayable)
        self._members_size.__value[0] = _val(val.membersSize)
        self._members.__value[0] = _val(val.members)
        self._type_name.__value[0] = _val(val.typeName)
    
    @property
    def type_id(self):
        return self._type_id

    @property
    def binary_encoding_id(self):
        return self._binary_encoding_id

    @property
    def mem_size(self):
        return self._mem_size

    @property
    def type_index(self):
        return self._type_index

    @property
    def type_kind(self):
        return self._type_kind

    @property
    def pointer_free(self):
        return self._pointer_free

    @property
    def overlayable(self):
        return self._overlayable

    @property
    def members_size(self):
        return self._members_size

    @property
    def members(self):
        return self._members

    @property
    def type_name(self):
        return self._type_name
    
    @type_id.setter
    def type_id(self, val):
        self._type_id = val
        self._value.typeId = val._value

    @binary_encoding_id.setter
    def binary_encoding_id(self, val):
        self._binary_encoding_id = val
        self._value.binaryEncodingId = val._value

    @mem_size.setter
    def mem_size(self, val):
        self._mem_size = val
        self._value.memSize = val._value

    @type_index.setter
    def type_index(self, val):
        self._type_index = val
        self._value.typeIndex = val._value

    @type_kind.setter
    def type_kind(self, val):
        self._type_kind = val
        self._value.typeKind = val._value

    @pointer_free.setter
    def pointer_free(self, val):
        self._pointer_free = val
        self._value.pointerFree = val._value

    @overlayable.setter
    def overlayable(self, val):
        self._overlayable = val
        self._value.overlayable = val._value

    @members_size.setter
    def members_size(self, val):
        self._members_size = val
        self._value.membersSize = val._value

    @members.setter
    def members(self, val):
        self._members = val
        self._value.members = val._value

    @type_name.setter
    def type_name(self, val):
        self._type_name = val
        self._value.typeName = val._value

    def __str__(self, n=0):
        return ("(UaDataType) :\n" +
                "\t"*(n+1) + "type_id" + self._type_id.__str__(n+1) +
                "\t"*(n+1) + "binary_encoding_id" + self._binary_encoding_id.__str__(n+1) +
                "\t"*(n+1) + "mem_size" + self._mem_size.__str__(n+1) +
                "\t"*(n+1) + "type_index" + self._type_index.__str__(n+1) +
                "\t"*(n+1) + "type_kind" + self._type_kind.__str__(n+1) +
                "\t"*(n+1) + "pointer_free" + self._pointer_free.__str__(n+1) +
                "\t"*(n+1) + "overlayable" + self._overlayable.__str__(n+1) +
                "\t"*(n+1) + "members_size" + self._members_size.__str__(n+1) +
                "\t"*(n+1) + "members" + self._members.__str__(n+1) +
                "\t"*(n+1) + "type_name" + self._type_name.__str__(n+1) + "\n")


# +++++++++++++++++++ UaDataTypeArray +++++++++++++++++++++++
class UaDataTypeArray(UaType):
    def __init__(self, val=ffi.new("UA_DataTypeArray*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
        self._ua_data_type_array = struct(val=val.UA_DataTypeArray, is_pointer=True)
        self._types_size = SizeT(val=val.typesSize, is_pointer=False)
        self._types = UaDataType(val=val.types, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._ua_data_type_array.__value[0] = _val(val.UA_DataTypeArray)
        self._types_size.__value[0] = _val(val.typesSize)
        self._types.__value[0] = _val(val.types)
    
    @property
    def ua_data_type_array(self):
        return self._ua_data_type_array

    @property
    def types_size(self):
        return self._types_size

    @property
    def types(self):
        return self._types
    
    @ua_data_type_array.setter
    def ua_data_type_array(self, val):
        self._ua_data_type_array = val
        self._value.UA_DataTypeArray = val._value

    @types_size.setter
    def types_size(self, val):
        self._types_size = val
        self._value.typesSize = val._value

    @types.setter
    def types(self, val):
        self._types = val
        self._value.types = val._value

    def __str__(self, n=0):
        return ("(UaDataTypeArray) :\n" +
                "\t"*(n+1) + "ua_data_type_array" + self._ua_data_type_array.__str__(n+1) +
                "\t"*(n+1) + "types_size" + self._types_size.__str__(n+1) +
                "\t"*(n+1) + "types" + self._types.__str__(n+1) + "\n")


