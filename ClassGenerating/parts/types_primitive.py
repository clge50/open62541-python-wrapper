# +++++++++++++++++++ UaBoolean +++++++++++++++++++++++
class UaBoolean(UaType):
    UA_TYPE = UA_TYPES.BOOLEAN
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Boolean*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Boolean[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Boolean*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Boolean")
        else:
            self._value[0] = ffi.cast("UA_Boolean", _val(val))

    def __str__(self, n=0):
        return "(UaBoolean): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaSByte +++++++++++++++++++++++
class UaSByte(UaType):
    UA_TYPE = UA_TYPES.SBYTE
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_SByte*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_SByte[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_SByte*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SByte")
        else:
            self._value[0] = ffi.cast("UA_SByte", _val(val))

    def __str__(self, n=0):
        return "(UaSByte): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaByte +++++++++++++++++++++++
class UaByte(UaType):
    UA_TYPE = UA_TYPES.BYTE
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Byte*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Byte[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Byte*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Byte")
        else:
            self._value[0] = ffi.cast("UA_Byte", _val(val))

    def __str__(self, n=0):
        return "(UaByte): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaInt16 +++++++++++++++++++++++
class UaInt16(UaType):
    UA_TYPE = UA_TYPES.INT16
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Int16*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Int16[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Int16*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int16")
        else:
            self._value[0] = ffi.cast("UA_Int16", _val(val))

    def __str__(self, n=0):
        return "(UaInt16): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaUInt16 +++++++++++++++++++++++
class UaUInt16(UaType):
    UA_TYPE = UA_TYPES.INT16
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UInt16*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_UInt16[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_UInt16*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt16")
        else:
            self._value[0] = ffi.cast("UA_UInt16", _val(val))

    def __str__(self, n=0):
        return "(UaUInt16): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaInt32 +++++++++++++++++++++++
class UaInt32(UaType):
    UA_TYPE = UA_TYPES.INT32
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Int32*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Int32[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Int32*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int32")
        else:
            self._value[0] = ffi.cast("UA_Int32", _val(val))

    def __str__(self, n=0):
        return "(UaInt32): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaUInt32 +++++++++++++++++++++++
class UaUInt32(UaType):
    UA_TYPE = UA_TYPES.INT32
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UInt32*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_UInt32[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_UInt32*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt32")
        else:
            self._value[0] = ffi.cast("UA_UInt32", _val(val))

    def __str__(self, n=0):
        return "(UaUInt32): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaInt64 +++++++++++++++++++++++
class UaInt64(UaType):
    UA_TYPE = UA_TYPES.INT64
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Int64*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Int64[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Int64*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int64")
        else:
            self._value[0] = ffi.cast("UA_Int64", _val(val))

    def __str__(self, n=0):
        return "(UaInt64): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaUInt64 +++++++++++++++++++++++
class UaUInt64(UaType):
    UA_TYPE = UA_TYPES.INT64
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UInt64*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_UInt64[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_UInt64*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt64")
        else:
            self._value[0] = ffi.cast("UA_UInt64", _val(val))

    def __str__(self, n=0):
        return "(UaUInt64): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaFloat +++++++++++++++++++++++
class UaFloat(UaType):
    UA_TYPE = UA_TYPES.FLOAT
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Float*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Float[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Float*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Float")
        else:
            self._value[0] = ffi.cast("UA_Float", _val(val))

    def __str__(self, n=0):
        return "(UaFloat): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaDouble +++++++++++++++++++++++
class UaDouble(UaType):
    UA_TYPE = UA_TYPES.DOUBLE
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Double*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Double[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Double*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Double")
        else:
            self._value[0] = ffi.cast("UA_Double", _val(val))

    def __str__(self, n=0):
        return "(UaDouble): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaStatusCode +++++++++++++++++++++++
class UaStatusCode(UaType):
    UA_TYPE = UA_TYPES.STATUSCODE
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_StatusCode*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_StatusCode[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_StatusCode*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_StatusCode")
        else:
            self._value[0] = ffi.cast("UA_StatusCode", _val(val))

    def __str__(self, n=0):
        return "(UaStatusCode): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaDateTime +++++++++++++++++++++++
class UaDateTime(UaType):
    UA_TYPE = UA_TYPES.DATETIME
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_DateTime*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_DateTime[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_DateTime*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DateTime")
        else:
            self._value[0] = ffi.cast("UA_DateTime", _val(val))

    def __str__(self, n=0):
        return "(UaDateTime): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


