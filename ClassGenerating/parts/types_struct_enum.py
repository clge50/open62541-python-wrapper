

# -------------------------------------------------------------
# -------------------------- Structs --------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaString +++++++++++++++++++++++
class UaString(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_String*")
        if type(val) is Void:
            val = ffi.cast("UA_String*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._length = SizeT(val=val.length, is_pointer=False)
            self._data = UaByte(val=val.data, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_String")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._length._value[0] = _val(val.length)
            self._data._value = val.data

    @property
    def length(self):
        if self._null:
            return None
        else:
            return self._length

    @property
    def data(self):
        if self._null:
            return None
        else:
            return self._data

    @length.setter
    def length(self, val: SizeT):
        self._length = val
        self._value.length = val._val

    @data.setter
    def data(self, val: UaByte):
        self._data = val
        self._value.data = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaString) : NULL\n"
        
        return ("(UaString) :\n"
                + "\t"*(n+1) + "length" + self._length.__str__(n+1)
                + "\t"*(n+1) + "data" + self._data.__str__(n+1))


# +++++++++++++++++++ UaDateTimeStruct +++++++++++++++++++++++
class UaDateTimeStruct(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DateTimeStruct*")
        if type(val) is Void:
            val = ffi.cast("UA_DateTimeStruct*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._nano_sec = UaUInt16(val=val.nanoSec, is_pointer=False)
            self._micro_sec = UaUInt16(val=val.microSec, is_pointer=False)
            self._milli_sec = UaUInt16(val=val.milliSec, is_pointer=False)
            self._sec = UaUInt16(val=val.sec, is_pointer=False)
            self._min = UaUInt16(val=val.min, is_pointer=False)
            self._hour = UaUInt16(val=val.hour, is_pointer=False)
            self._day = UaUInt16(val=val.day, is_pointer=False)
            self._month = UaUInt16(val=val.month, is_pointer=False)
            self._year = UaUInt16(val=val.year, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DateTimeStruct")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._nano_sec._value[0] = _val(val.nanoSec)
            self._micro_sec._value[0] = _val(val.microSec)
            self._milli_sec._value[0] = _val(val.milliSec)
            self._sec._value[0] = _val(val.sec)
            self._min._value[0] = _val(val.min)
            self._hour._value[0] = _val(val.hour)
            self._day._value[0] = _val(val.day)
            self._month._value[0] = _val(val.month)
            self._year._value[0] = _val(val.year)

    @property
    def nano_sec(self):
        if self._null:
            return None
        else:
            return self._nano_sec

    @property
    def micro_sec(self):
        if self._null:
            return None
        else:
            return self._micro_sec

    @property
    def milli_sec(self):
        if self._null:
            return None
        else:
            return self._milli_sec

    @property
    def sec(self):
        if self._null:
            return None
        else:
            return self._sec

    @property
    def min(self):
        if self._null:
            return None
        else:
            return self._min

    @property
    def hour(self):
        if self._null:
            return None
        else:
            return self._hour

    @property
    def day(self):
        if self._null:
            return None
        else:
            return self._day

    @property
    def month(self):
        if self._null:
            return None
        else:
            return self._month

    @property
    def year(self):
        if self._null:
            return None
        else:
            return self._year

    @nano_sec.setter
    def nano_sec(self, val: UaUInt16):
        self._nano_sec = val
        self._value.nanoSec = val._val

    @micro_sec.setter
    def micro_sec(self, val: UaUInt16):
        self._micro_sec = val
        self._value.microSec = val._val

    @milli_sec.setter
    def milli_sec(self, val: UaUInt16):
        self._milli_sec = val
        self._value.milliSec = val._val

    @sec.setter
    def sec(self, val: UaUInt16):
        self._sec = val
        self._value.sec = val._val

    @min.setter
    def min(self, val: UaUInt16):
        self._min = val
        self._value.min = val._val

    @hour.setter
    def hour(self, val: UaUInt16):
        self._hour = val
        self._value.hour = val._val

    @day.setter
    def day(self, val: UaUInt16):
        self._day = val
        self._value.day = val._val

    @month.setter
    def month(self, val: UaUInt16):
        self._month = val
        self._value.month = val._val

    @year.setter
    def year(self, val: UaUInt16):
        self._year = val
        self._value.year = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaDateTimeStruct) : NULL\n"
        
        return ("(UaDateTimeStruct) :\n"
                + "\t"*(n+1) + "nano_sec" + self._nano_sec.__str__(n+1)
                + "\t"*(n+1) + "micro_sec" + self._micro_sec.__str__(n+1)
                + "\t"*(n+1) + "milli_sec" + self._milli_sec.__str__(n+1)
                + "\t"*(n+1) + "sec" + self._sec.__str__(n+1)
                + "\t"*(n+1) + "min" + self._min.__str__(n+1)
                + "\t"*(n+1) + "hour" + self._hour.__str__(n+1)
                + "\t"*(n+1) + "day" + self._day.__str__(n+1)
                + "\t"*(n+1) + "month" + self._month.__str__(n+1)
                + "\t"*(n+1) + "year" + self._year.__str__(n+1))


# +++++++++++++++++++ UaGuid +++++++++++++++++++++++
class UaGuid(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_Guid*")
        if type(val) is Void:
            val = ffi.cast("UA_Guid*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._data1 = UaUInt32(val=val.data1, is_pointer=False)
            self._data2 = UaUInt16(val=val.data2, is_pointer=False)
            self._data3 = UaUInt16(val=val.data3, is_pointer=False)
            self._data4 = UaByte(val=val.data4, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Guid")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._data1._value[0] = _val(val.data1)
            self._data2._value[0] = _val(val.data2)
            self._data3._value[0] = _val(val.data3)
            self._data4._value = val.data4

    @property
    def data1(self):
        if self._null:
            return None
        else:
            return self._data1

    @property
    def data2(self):
        if self._null:
            return None
        else:
            return self._data2

    @property
    def data3(self):
        if self._null:
            return None
        else:
            return self._data3

    @property
    def data4(self):
        if self._null:
            return None
        else:
            return self._data4

    @data1.setter
    def data1(self, val: UaUInt32):
        self._data1 = val
        self._value.data1 = val._val

    @data2.setter
    def data2(self, val: UaUInt16):
        self._data2 = val
        self._value.data2 = val._val

    @data3.setter
    def data3(self, val: UaUInt16):
        self._data3 = val
        self._value.data3 = val._val

    @data4.setter
    def data4(self, val: UaByte):
        self._data4 = val
        self._value.data4 = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaGuid) : NULL\n"
        
        return ("(UaGuid) :\n"
                + "\t"*(n+1) + "data1" + self._data1.__str__(n+1)
                + "\t"*(n+1) + "data2" + self._data2.__str__(n+1)
                + "\t"*(n+1) + "data3" + self._data3.__str__(n+1)
                + "\t"*(n+1) + "data4" + self._data4.__str__(n+1))


# +++++++++++++++++++ UaExpandedNodeId +++++++++++++++++++++++
class UaExpandedNodeId(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ExpandedNodeId*")
        if type(val) is Void:
            val = ffi.cast("UA_ExpandedNodeId*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
            self._namespace_uri = UaString(val=val.namespaceUri, is_pointer=False)
            self._server_index = UaUInt32(val=val.serverIndex, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ExpandedNodeId")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._node_id._value[0] = _val(val.nodeId)
            self._namespace_uri._value[0] = _val(val.namespaceUri)
            self._server_index._value[0] = _val(val.serverIndex)

    @property
    def node_id(self):
        if self._null:
            return None
        else:
            return self._node_id

    @property
    def namespace_uri(self):
        if self._null:
            return None
        else:
            return self._namespace_uri

    @property
    def server_index(self):
        if self._null:
            return None
        else:
            return self._server_index

    @node_id.setter
    def node_id(self, val: UaNodeId):
        self._node_id = val
        self._value.nodeId = val._val

    @namespace_uri.setter
    def namespace_uri(self, val: UaString):
        self._namespace_uri = val
        self._value.namespaceUri = val._val

    @server_index.setter
    def server_index(self, val: UaUInt32):
        self._server_index = val
        self._value.serverIndex = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaExpandedNodeId) : NULL\n"
        
        return ("(UaExpandedNodeId) :\n"
                + "\t"*(n+1) + "node_id" + self._node_id.__str__(n+1)
                + "\t"*(n+1) + "namespace_uri" + self._namespace_uri.__str__(n+1)
                + "\t"*(n+1) + "server_index" + self._server_index.__str__(n+1))


# +++++++++++++++++++ UaQualifiedName +++++++++++++++++++++++
class UaQualifiedName(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_QualifiedName*")
        if type(val) is Void:
            val = ffi.cast("UA_QualifiedName*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._namespace_index = UaUInt16(val=val.namespaceIndex, is_pointer=False)
            self._name = UaString(val=val.name, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_QualifiedName")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._namespace_index._value[0] = _val(val.namespaceIndex)
            self._name._value[0] = _val(val.name)

    @property
    def namespace_index(self):
        if self._null:
            return None
        else:
            return self._namespace_index

    @property
    def name(self):
        if self._null:
            return None
        else:
            return self._name

    @namespace_index.setter
    def namespace_index(self, val: UaUInt16):
        self._namespace_index = val
        self._value.namespaceIndex = val._val

    @name.setter
    def name(self, val: UaString):
        self._name = val
        self._value.name = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaQualifiedName) : NULL\n"
        
        return ("(UaQualifiedName) :\n"
                + "\t"*(n+1) + "namespace_index" + self._namespace_index.__str__(n+1)
                + "\t"*(n+1) + "name" + self._name.__str__(n+1))


# +++++++++++++++++++ UaLocalizedText +++++++++++++++++++++++
class UaLocalizedText(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_LocalizedText*")
        if type(val) is Void:
            val = ffi.cast("UA_LocalizedText*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._locale = UaString(val=val.locale, is_pointer=False)
            self._text = UaString(val=val.text, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_LocalizedText")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._locale._value[0] = _val(val.locale)
            self._text._value[0] = _val(val.text)

    @property
    def locale(self):
        if self._null:
            return None
        else:
            return self._locale

    @property
    def text(self):
        if self._null:
            return None
        else:
            return self._text

    @locale.setter
    def locale(self, val: UaString):
        self._locale = val
        self._value.locale = val._val

    @text.setter
    def text(self, val: UaString):
        self._text = val
        self._value.text = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaLocalizedText) : NULL\n"
        
        return ("(UaLocalizedText) :\n"
                + "\t"*(n+1) + "locale" + self._locale.__str__(n+1)
                + "\t"*(n+1) + "text" + self._text.__str__(n+1))


# +++++++++++++++++++ UaNumericRangeDimension +++++++++++++++++++++++
class UaNumericRangeDimension(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NumericRangeDimension*")
        if type(val) is Void:
            val = ffi.cast("UA_NumericRangeDimension*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._min = UaUInt32(val=val.min, is_pointer=False)
            self._max = UaUInt32(val=val.max, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NumericRangeDimension")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._min._value[0] = _val(val.min)
            self._max._value[0] = _val(val.max)

    @property
    def min(self):
        if self._null:
            return None
        else:
            return self._min

    @property
    def max(self):
        if self._null:
            return None
        else:
            return self._max

    @min.setter
    def min(self, val: UaUInt32):
        self._min = val
        self._value.min = val._val

    @max.setter
    def max(self, val: UaUInt32):
        self._max = val
        self._value.max = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaNumericRangeDimension) : NULL\n"
        
        return ("(UaNumericRangeDimension) :\n"
                + "\t"*(n+1) + "min" + self._min.__str__(n+1)
                + "\t"*(n+1) + "max" + self._max.__str__(n+1))


# +++++++++++++++++++ UaNumericRange +++++++++++++++++++++++
class UaNumericRange(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NumericRange*")
        if type(val) is Void:
            val = ffi.cast("UA_NumericRange*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._dimensions_size = SizeT(val=val.dimensionsSize, is_pointer=False)
            self._dimensions = UaNumericRangeDimension(val=val.dimensions, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NumericRange")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._dimensions_size._value[0] = _val(val.dimensionsSize)
            self._dimensions._value = val.dimensions

    @property
    def dimensions_size(self):
        if self._null:
            return None
        else:
            return self._dimensions_size

    @property
    def dimensions(self):
        if self._null:
            return None
        else:
            return self._dimensions

    @dimensions_size.setter
    def dimensions_size(self, val: SizeT):
        self._dimensions_size = val
        self._value.dimensionsSize = val._val

    @dimensions.setter
    def dimensions(self, val: UaNumericRangeDimension):
        self._dimensions = val
        self._value.dimensions = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaNumericRange) : NULL\n"
        
        return ("(UaNumericRange) :\n"
                + "\t"*(n+1) + "dimensions_size" + self._dimensions_size.__str__(n+1)
                + "\t"*(n+1) + "dimensions" + self._dimensions.__str__(n+1))


# +++++++++++++++++++ UaVariant +++++++++++++++++++++++
class UaVariant(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_Variant*")
        if type(val) is Void:
            val = ffi.cast("UA_Variant*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._type = UaDataType(val=val.type, is_pointer=True)
            self._storage_type = UaVariantStorageType(val=val.storageType, is_pointer=False)
            self._array_length = SizeT(val=val.arrayLength, is_pointer=False)
            self._data = Void(val=val.data, is_pointer=True)
            self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
            self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Variant")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._type._value = val.type
            self._storage_type._value[0] = _val(val.storageType)
            self._array_length._value[0] = _val(val.arrayLength)
            self._data._value = val.data
            self._array_dimensions_size._value[0] = _val(val.arrayDimensionsSize)
            self._array_dimensions._value = val.arrayDimensions

    @property
    def type(self):
        if self._null:
            return None
        else:
            return self._type

    @property
    def storage_type(self):
        if self._null:
            return None
        else:
            return self._storage_type

    @property
    def array_length(self):
        if self._null:
            return None
        else:
            return self._array_length

    @property
    def data(self):
        if self._null:
            return None
        else:
            return self._data

    @property
    def array_dimensions_size(self):
        if self._null:
            return None
        else:
            return self._array_dimensions_size

    @property
    def array_dimensions(self):
        if self._null:
            return None
        else:
            return self._array_dimensions

    @type.setter
    def type(self, val: UaDataType):
        self._type = val
        self._value.type = val._ptr

    @storage_type.setter
    def storage_type(self, val: UaVariantStorageType):
        self._storage_type = val
        self._value.storageType = val._val

    @array_length.setter
    def array_length(self, val: SizeT):
        self._array_length = val
        self._value.arrayLength = val._val

    @data.setter
    def data(self, val: Void):
        self._data = val
        self._value.data = val._ptr

    @array_dimensions_size.setter
    def array_dimensions_size(self, val: SizeT):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._val

    @array_dimensions.setter
    def array_dimensions(self, val: UaUInt32):
        self._array_dimensions = val
        self._value.arrayDimensions = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaVariant) : NULL\n"
        
        return ("(UaVariant) :\n"
                + "\t"*(n+1) + "type" + self._type.__str__(n+1)
                + "\t"*(n+1) + "storage_type" + self._storage_type.__str__(n+1)
                + "\t"*(n+1) + "array_length" + self._array_length.__str__(n+1)
                + "\t"*(n+1) + "data" + self._data.__str__(n+1)
                + "\t"*(n+1) + "array_dimensions_size" + self._array_dimensions_size.__str__(n+1)
                + "\t"*(n+1) + "array_dimensions" + self._array_dimensions.__str__(n+1))


# +++++++++++++++++++ UaDataValue +++++++++++++++++++++++
class UaDataValue(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataValue*")
        if type(val) is Void:
            val = ffi.cast("UA_DataValue*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._data_value = UaVariant(val=val.value, is_pointer=False)
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

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataValue")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._data_value._value[0] = _val(val.value)
            self._source_timestamp._value[0] = _val(val.sourceTimestamp)
            self._server_timestamp._value[0] = _val(val.serverTimestamp)
            self._source_picoseconds._value[0] = _val(val.sourcePicoseconds)
            self._server_picoseconds._value[0] = _val(val.serverPicoseconds)
            self._status._value[0] = _val(val.status)
            self._has_value._value[0] = _val(val.hasValue)
            self._has_status._value[0] = _val(val.hasStatus)
            self._has_source_timestamp._value[0] = _val(val.hasSourceTimestamp)
            self._has_server_timestamp._value[0] = _val(val.hasServerTimestamp)
            self._has_source_picoseconds._value[0] = _val(val.hasSourcePicoseconds)
            self._has_server_picoseconds._value[0] = _val(val.hasServerPicoseconds)

    @property
    def data_value(self):
        if self._null:
            return None
        else:
            return self._data_value

    @property
    def source_timestamp(self):
        if self._null:
            return None
        else:
            return self._source_timestamp

    @property
    def server_timestamp(self):
        if self._null:
            return None
        else:
            return self._server_timestamp

    @property
    def source_picoseconds(self):
        if self._null:
            return None
        else:
            return self._source_picoseconds

    @property
    def server_picoseconds(self):
        if self._null:
            return None
        else:
            return self._server_picoseconds

    @property
    def status(self):
        if self._null:
            return None
        else:
            return self._status

    @property
    def has_value(self):
        if self._null:
            return None
        else:
            return self._has_value

    @property
    def has_status(self):
        if self._null:
            return None
        else:
            return self._has_status

    @property
    def has_source_timestamp(self):
        if self._null:
            return None
        else:
            return self._has_source_timestamp

    @property
    def has_server_timestamp(self):
        if self._null:
            return None
        else:
            return self._has_server_timestamp

    @property
    def has_source_picoseconds(self):
        if self._null:
            return None
        else:
            return self._has_source_picoseconds

    @property
    def has_server_picoseconds(self):
        if self._null:
            return None
        else:
            return self._has_server_picoseconds

    @data_value.setter
    def data_value(self, val: UaVariant):
        self._data_value = val
        self._value.value = val._val

    @source_timestamp.setter
    def source_timestamp(self, val: UaDateTime):
        self._source_timestamp = val
        self._value.sourceTimestamp = val._val

    @server_timestamp.setter
    def server_timestamp(self, val: UaDateTime):
        self._server_timestamp = val
        self._value.serverTimestamp = val._val

    @source_picoseconds.setter
    def source_picoseconds(self, val: UaUInt16):
        self._source_picoseconds = val
        self._value.sourcePicoseconds = val._val

    @server_picoseconds.setter
    def server_picoseconds(self, val: UaUInt16):
        self._server_picoseconds = val
        self._value.serverPicoseconds = val._val

    @status.setter
    def status(self, val: UaStatusCode):
        self._status = val
        self._value.status = val._val

    @has_value.setter
    def has_value(self, val: UaBoolean):
        self._has_value = val
        self._value.hasValue = val._val

    @has_status.setter
    def has_status(self, val: UaBoolean):
        self._has_status = val
        self._value.hasStatus = val._val

    @has_source_timestamp.setter
    def has_source_timestamp(self, val: UaBoolean):
        self._has_source_timestamp = val
        self._value.hasSourceTimestamp = val._val

    @has_server_timestamp.setter
    def has_server_timestamp(self, val: UaBoolean):
        self._has_server_timestamp = val
        self._value.hasServerTimestamp = val._val

    @has_source_picoseconds.setter
    def has_source_picoseconds(self, val: UaBoolean):
        self._has_source_picoseconds = val
        self._value.hasSourcePicoseconds = val._val

    @has_server_picoseconds.setter
    def has_server_picoseconds(self, val: UaBoolean):
        self._has_server_picoseconds = val
        self._value.hasServerPicoseconds = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaDataValue) : NULL\n"
        
        return ("(UaDataValue) :\n"
                + "\t"*(n+1) + "data_value" + self._data_value.__str__(n+1)
                + "\t"*(n+1) + "source_timestamp" + self._source_timestamp.__str__(n+1)
                + "\t"*(n+1) + "server_timestamp" + self._server_timestamp.__str__(n+1)
                + "\t"*(n+1) + "source_picoseconds" + self._source_picoseconds.__str__(n+1)
                + "\t"*(n+1) + "server_picoseconds" + self._server_picoseconds.__str__(n+1)
                + "\t"*(n+1) + "status" + self._status.__str__(n+1)
                + "\t"*(n+1) + "has_value" + self._has_value.__str__(n+1)
                + "\t"*(n+1) + "has_status" + self._has_status.__str__(n+1)
                + "\t"*(n+1) + "has_source_timestamp" + self._has_source_timestamp.__str__(n+1)
                + "\t"*(n+1) + "has_server_timestamp" + self._has_server_timestamp.__str__(n+1)
                + "\t"*(n+1) + "has_source_picoseconds" + self._has_source_picoseconds.__str__(n+1)
                + "\t"*(n+1) + "has_server_picoseconds" + self._has_server_picoseconds.__str__(n+1))


# +++++++++++++++++++ UaDiagnosticInfo +++++++++++++++++++++++
class UaDiagnosticInfo(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DiagnosticInfo*")
        if type(val) is Void:
            val = ffi.cast("UA_DiagnosticInfo*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._has_symbolic_id = UaBoolean(val=val.hasSymbolicId, is_pointer=False)
            self._has_namespace_uri = UaBoolean(val=val.hasNamespaceUri, is_pointer=False)
            self._has_localized_text = UaBoolean(val=val.hasLocalizedText, is_pointer=False)
            self._has_locale = UaBoolean(val=val.hasLocale, is_pointer=False)
            self._has_additional_info = UaBoolean(val=val.hasAdditionalInfo, is_pointer=False)
            self._has_inner_status_code = UaBoolean(val=val.hasInnerStatusCode, is_pointer=False)
            self._has_inner_diagnostic_info = UaBoolean(val=val.hasInnerDiagnosticInfo, is_pointer=False)
            self._symbolic_id = UaInt32(val=val.symbolicId, is_pointer=False)
            self._namespace_uri = UaInt32(val=val.namespaceUri, is_pointer=False)
            self._localized_text = UaInt32(val=val.localizedText, is_pointer=False)
            self._locale = UaInt32(val=val.locale, is_pointer=False)
            self._additional_info = UaString(val=val.additionalInfo, is_pointer=False)
            self._inner_status_code = UaStatusCode(val=val.innerStatusCode, is_pointer=False)
            self._inner_diagnostic_info = UaDiagnosticInfo(val=val.innerDiagnosticInfo, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DiagnosticInfo")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._has_symbolic_id._value[0] = _val(val.hasSymbolicId)
            self._has_namespace_uri._value[0] = _val(val.hasNamespaceUri)
            self._has_localized_text._value[0] = _val(val.hasLocalizedText)
            self._has_locale._value[0] = _val(val.hasLocale)
            self._has_additional_info._value[0] = _val(val.hasAdditionalInfo)
            self._has_inner_status_code._value[0] = _val(val.hasInnerStatusCode)
            self._has_inner_diagnostic_info._value[0] = _val(val.hasInnerDiagnosticInfo)
            self._symbolic_id._value[0] = _val(val.symbolicId)
            self._namespace_uri._value[0] = _val(val.namespaceUri)
            self._localized_text._value[0] = _val(val.localizedText)
            self._locale._value[0] = _val(val.locale)
            self._additional_info._value[0] = _val(val.additionalInfo)
            self._inner_status_code._value[0] = _val(val.innerStatusCode)
            self._inner_diagnostic_info._value = val.innerDiagnosticInfo

    @property
    def has_symbolic_id(self):
        if self._null:
            return None
        else:
            return self._has_symbolic_id

    @property
    def has_namespace_uri(self):
        if self._null:
            return None
        else:
            return self._has_namespace_uri

    @property
    def has_localized_text(self):
        if self._null:
            return None
        else:
            return self._has_localized_text

    @property
    def has_locale(self):
        if self._null:
            return None
        else:
            return self._has_locale

    @property
    def has_additional_info(self):
        if self._null:
            return None
        else:
            return self._has_additional_info

    @property
    def has_inner_status_code(self):
        if self._null:
            return None
        else:
            return self._has_inner_status_code

    @property
    def has_inner_diagnostic_info(self):
        if self._null:
            return None
        else:
            return self._has_inner_diagnostic_info

    @property
    def symbolic_id(self):
        if self._null:
            return None
        else:
            return self._symbolic_id

    @property
    def namespace_uri(self):
        if self._null:
            return None
        else:
            return self._namespace_uri

    @property
    def localized_text(self):
        if self._null:
            return None
        else:
            return self._localized_text

    @property
    def locale(self):
        if self._null:
            return None
        else:
            return self._locale

    @property
    def additional_info(self):
        if self._null:
            return None
        else:
            return self._additional_info

    @property
    def inner_status_code(self):
        if self._null:
            return None
        else:
            return self._inner_status_code

    @property
    def inner_diagnostic_info(self):
        if self._null:
            return None
        else:
            return self._inner_diagnostic_info

    @has_symbolic_id.setter
    def has_symbolic_id(self, val: UaBoolean):
        self._has_symbolic_id = val
        self._value.hasSymbolicId = val._val

    @has_namespace_uri.setter
    def has_namespace_uri(self, val: UaBoolean):
        self._has_namespace_uri = val
        self._value.hasNamespaceUri = val._val

    @has_localized_text.setter
    def has_localized_text(self, val: UaBoolean):
        self._has_localized_text = val
        self._value.hasLocalizedText = val._val

    @has_locale.setter
    def has_locale(self, val: UaBoolean):
        self._has_locale = val
        self._value.hasLocale = val._val

    @has_additional_info.setter
    def has_additional_info(self, val: UaBoolean):
        self._has_additional_info = val
        self._value.hasAdditionalInfo = val._val

    @has_inner_status_code.setter
    def has_inner_status_code(self, val: UaBoolean):
        self._has_inner_status_code = val
        self._value.hasInnerStatusCode = val._val

    @has_inner_diagnostic_info.setter
    def has_inner_diagnostic_info(self, val: UaBoolean):
        self._has_inner_diagnostic_info = val
        self._value.hasInnerDiagnosticInfo = val._val

    @symbolic_id.setter
    def symbolic_id(self, val: UaInt32):
        self._symbolic_id = val
        self._value.symbolicId = val._val

    @namespace_uri.setter
    def namespace_uri(self, val: UaInt32):
        self._namespace_uri = val
        self._value.namespaceUri = val._val

    @localized_text.setter
    def localized_text(self, val: UaInt32):
        self._localized_text = val
        self._value.localizedText = val._val

    @locale.setter
    def locale(self, val: UaInt32):
        self._locale = val
        self._value.locale = val._val

    @additional_info.setter
    def additional_info(self, val: UaString):
        self._additional_info = val
        self._value.additionalInfo = val._val

    @inner_status_code.setter
    def inner_status_code(self, val: UaStatusCode):
        self._inner_status_code = val
        self._value.innerStatusCode = val._val

    @inner_diagnostic_info.setter
    def inner_diagnostic_info(self, val: UaDiagnosticInfo):
        self._inner_diagnostic_info = val
        self._value.innerDiagnosticInfo = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaDiagnosticInfo) : NULL\n"
        
        return ("(UaDiagnosticInfo) :\n"
                + "\t"*(n+1) + "has_symbolic_id" + self._has_symbolic_id.__str__(n+1)
                + "\t"*(n+1) + "has_namespace_uri" + self._has_namespace_uri.__str__(n+1)
                + "\t"*(n+1) + "has_localized_text" + self._has_localized_text.__str__(n+1)
                + "\t"*(n+1) + "has_locale" + self._has_locale.__str__(n+1)
                + "\t"*(n+1) + "has_additional_info" + self._has_additional_info.__str__(n+1)
                + "\t"*(n+1) + "has_inner_status_code" + self._has_inner_status_code.__str__(n+1)
                + "\t"*(n+1) + "has_inner_diagnostic_info" + self._has_inner_diagnostic_info.__str__(n+1)
                + "\t"*(n+1) + "symbolic_id" + self._symbolic_id.__str__(n+1)
                + "\t"*(n+1) + "namespace_uri" + self._namespace_uri.__str__(n+1)
                + "\t"*(n+1) + "localized_text" + self._localized_text.__str__(n+1)
                + "\t"*(n+1) + "locale" + self._locale.__str__(n+1)
                + "\t"*(n+1) + "additional_info" + self._additional_info.__str__(n+1)
                + "\t"*(n+1) + "inner_status_code" + self._inner_status_code.__str__(n+1)
                + "\t"*(n+1) + "inner_diagnostic_info" + self._inner_diagnostic_info.__str__(n+1))


# +++++++++++++++++++ UaDataTypeMember +++++++++++++++++++++++
class UaDataTypeMember(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataTypeMember*")
        if type(val) is Void:
            val = ffi.cast("UA_DataTypeMember*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._member_type_index = UaUInt16(val=val.memberTypeIndex, is_pointer=False)
            self._padding = UaByte(val=val.padding, is_pointer=False)
            self._namespace_zero = UaBoolean(val=val.namespaceZero, is_pointer=False)
            self._is_array = UaBoolean(val=val.isArray, is_pointer=False)
            self._is_optional = UaBoolean(val=val.isOptional, is_pointer=False)
            self._member_name = CString(val=val.memberName, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataTypeMember")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._member_type_index._value[0] = _val(val.memberTypeIndex)
            self._padding._value[0] = _val(val.padding)
            self._namespace_zero._value[0] = _val(val.namespaceZero)
            self._is_array._value[0] = _val(val.isArray)
            self._is_optional._value[0] = _val(val.isOptional)
            self._member_name._value = val.memberName

    @property
    def member_type_index(self):
        if self._null:
            return None
        else:
            return self._member_type_index

    @property
    def padding(self):
        if self._null:
            return None
        else:
            return self._padding

    @property
    def namespace_zero(self):
        if self._null:
            return None
        else:
            return self._namespace_zero

    @property
    def is_array(self):
        if self._null:
            return None
        else:
            return self._is_array

    @property
    def is_optional(self):
        if self._null:
            return None
        else:
            return self._is_optional

    @property
    def member_name(self):
        if self._null:
            return None
        else:
            return self._member_name

    @member_type_index.setter
    def member_type_index(self, val: UaUInt16):
        self._member_type_index = val
        self._value.memberTypeIndex = val._val

    @padding.setter
    def padding(self, val: UaByte):
        self._padding = val
        self._value.padding = val._val

    @namespace_zero.setter
    def namespace_zero(self, val: UaBoolean):
        self._namespace_zero = val
        self._value.namespaceZero = val._val

    @is_array.setter
    def is_array(self, val: UaBoolean):
        self._is_array = val
        self._value.isArray = val._val

    @is_optional.setter
    def is_optional(self, val: UaBoolean):
        self._is_optional = val
        self._value.isOptional = val._val

    @member_name.setter
    def member_name(self, val: CString):
        self._member_name = val
        self._value.memberName = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaDataTypeMember) : NULL\n"
        
        return ("(UaDataTypeMember) :\n"
                + "\t"*(n+1) + "member_type_index" + self._member_type_index.__str__(n+1)
                + "\t"*(n+1) + "padding" + self._padding.__str__(n+1)
                + "\t"*(n+1) + "namespace_zero" + self._namespace_zero.__str__(n+1)
                + "\t"*(n+1) + "is_array" + self._is_array.__str__(n+1)
                + "\t"*(n+1) + "is_optional" + self._is_optional.__str__(n+1)
                + "\t"*(n+1) + "member_name" + self._member_name.__str__(n+1))


# +++++++++++++++++++ UaDataType +++++++++++++++++++++++
class UaDataType(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataType*")
        if type(val) is Void:
            val = ffi.cast("UA_DataType*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
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

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataType")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._type_id._value[0] = _val(val.typeId)
            self._binary_encoding_id._value[0] = _val(val.binaryEncodingId)
            self._mem_size._value[0] = _val(val.memSize)
            self._type_index._value[0] = _val(val.typeIndex)
            self._type_kind._value[0] = _val(val.typeKind)
            self._pointer_free._value[0] = _val(val.pointerFree)
            self._overlayable._value[0] = _val(val.overlayable)
            self._members_size._value[0] = _val(val.membersSize)
            self._members._value = val.members
            self._type_name._value = val.typeName

    @property
    def type_id(self):
        if self._null:
            return None
        else:
            return self._type_id

    @property
    def binary_encoding_id(self):
        if self._null:
            return None
        else:
            return self._binary_encoding_id

    @property
    def mem_size(self):
        if self._null:
            return None
        else:
            return self._mem_size

    @property
    def type_index(self):
        if self._null:
            return None
        else:
            return self._type_index

    @property
    def type_kind(self):
        if self._null:
            return None
        else:
            return self._type_kind

    @property
    def pointer_free(self):
        if self._null:
            return None
        else:
            return self._pointer_free

    @property
    def overlayable(self):
        if self._null:
            return None
        else:
            return self._overlayable

    @property
    def members_size(self):
        if self._null:
            return None
        else:
            return self._members_size

    @property
    def members(self):
        if self._null:
            return None
        else:
            return self._members

    @property
    def type_name(self):
        if self._null:
            return None
        else:
            return self._type_name

    @type_id.setter
    def type_id(self, val: UaNodeId):
        self._type_id = val
        self._value.typeId = val._val

    @binary_encoding_id.setter
    def binary_encoding_id(self, val: UaNodeId):
        self._binary_encoding_id = val
        self._value.binaryEncodingId = val._val

    @mem_size.setter
    def mem_size(self, val: UaUInt16):
        self._mem_size = val
        self._value.memSize = val._val

    @type_index.setter
    def type_index(self, val: UaUInt16):
        self._type_index = val
        self._value.typeIndex = val._val

    @type_kind.setter
    def type_kind(self, val: UaUInt32):
        self._type_kind = val
        self._value.typeKind = val._val

    @pointer_free.setter
    def pointer_free(self, val: UaUInt32):
        self._pointer_free = val
        self._value.pointerFree = val._val

    @overlayable.setter
    def overlayable(self, val: UaUInt32):
        self._overlayable = val
        self._value.overlayable = val._val

    @members_size.setter
    def members_size(self, val: UaUInt32):
        self._members_size = val
        self._value.membersSize = val._val

    @members.setter
    def members(self, val: UaDataTypeMember):
        self._members = val
        self._value.members = val._ptr

    @type_name.setter
    def type_name(self, val: CString):
        self._type_name = val
        self._value.typeName = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaDataType) : NULL\n"
        
        return ("(UaDataType) :\n"
                + "\t"*(n+1) + "type_id" + self._type_id.__str__(n+1)
                + "\t"*(n+1) + "binary_encoding_id" + self._binary_encoding_id.__str__(n+1)
                + "\t"*(n+1) + "mem_size" + self._mem_size.__str__(n+1)
                + "\t"*(n+1) + "type_index" + self._type_index.__str__(n+1)
                + "\t"*(n+1) + "type_kind" + self._type_kind.__str__(n+1)
                + "\t"*(n+1) + "pointer_free" + self._pointer_free.__str__(n+1)
                + "\t"*(n+1) + "overlayable" + self._overlayable.__str__(n+1)
                + "\t"*(n+1) + "members_size" + self._members_size.__str__(n+1)
                + "\t"*(n+1) + "members" + self._members.__str__(n+1)
                + "\t"*(n+1) + "type_name" + self._type_name.__str__(n+1))


# +++++++++++++++++++ UaDataTypeArray +++++++++++++++++++++++
class UaDataTypeArray(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataTypeArray*")
        if type(val) is Void:
            val = ffi.cast("UA_DataTypeArray*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
            self._next = UaDataTypeArray(val=val.next, is_pointer=True)
            self._types_size = SizeT(val=val.typesSize, is_pointer=False)
            self._types = UaDataType(val=val.types, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataTypeArray")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._next._value = val.next
            self._types_size._value[0] = _val(val.typesSize)
            self._types._value = val.types

    @property
    def next(self):
        if self._null:
            return None
        else:
            return self._next

    @property
    def types_size(self):
        if self._null:
            return None
        else:
            return self._types_size

    @property
    def types(self):
        if self._null:
            return None
        else:
            return self._types

    @next.setter
    def next(self, val: UaDataTypeArray):
        self._next = val
        self._value.next = val._ptr

    @types_size.setter
    def types_size(self, val: SizeT):
        self._types_size = val
        self._value.typesSize = val._val

    @types.setter
    def types(self, val: UaDataType):
        self._types = val
        self._value.types = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaDataTypeArray) : NULL\n"
        
        return ("(UaDataTypeArray) :\n"
                + "\t"*(n+1) + "next" + self._next.__str__(n+1)
                + "\t"*(n+1) + "types_size" + self._types_size.__str__(n+1)
                + "\t"*(n+1) + "types" + self._types.__str__(n+1))


