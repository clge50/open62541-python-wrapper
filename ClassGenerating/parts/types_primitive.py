# +++++++++++++++++++ UaBoolean +++++++++++++++++++++++
class UaBoolean(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Boolean*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Boolean", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_Boolean", _val(val))

    def __str__(self, n=0):
        return "(UaBoolean): " + str(self._value) + "\n"


# +++++++++++++++++++ UaSByte +++++++++++++++++++++++
class UaSByte(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_SByte*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_SByte", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_SByte", _val(val))

    def __str__(self, n=0):
        return "(UaSByte): " + str(self._value) + "\n"


# +++++++++++++++++++ UaByte +++++++++++++++++++++++
class UaByte(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Byte*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Byte", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_Byte", _val(val))

    def __str__(self, n=0):
        return "(UaByte): " + str(self._value) + "\n"


# +++++++++++++++++++ UaInt16 +++++++++++++++++++++++
class UaInt16(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Int16*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Int16", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_Int16", _val(val))

    def __str__(self, n=0):
        return "(UaInt16): " + str(self._value) + "\n"


# +++++++++++++++++++ UaUInt16 +++++++++++++++++++++++
class UaUInt16(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UInt16*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_UInt16", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_UInt16", _val(val))

    def __str__(self, n=0):
        return "(UaUInt16): " + str(self._value) + "\n"


# +++++++++++++++++++ UaInt32 +++++++++++++++++++++++
class UaInt32(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Int32*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Int32", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_Int32", _val(val))

    def __str__(self, n=0):
        return "(UaInt32): " + str(self._value) + "\n"


# +++++++++++++++++++ UaUInt32 +++++++++++++++++++++++
class UaUInt32(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UInt32*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_UInt32", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_UInt32", _val(val))

    def __str__(self, n=0):
        return "(UaUInt32): " + str(self._value) + "\n"


# +++++++++++++++++++ UaInt64 +++++++++++++++++++++++
class UaInt64(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Int64*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Int64", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_Int64", _val(val))

    def __str__(self, n=0):
        return "(UaInt64): " + str(self._value) + "\n"


# +++++++++++++++++++ UaUInt64 +++++++++++++++++++++++
class UaUInt64(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UInt64*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_UInt64", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_UInt64", _val(val))

    def __str__(self, n=0):
        return "(UaUInt64): " + str(self._value) + "\n"


# +++++++++++++++++++ UaFloat +++++++++++++++++++++++
class UaFloat(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Float*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Float", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_Float", _val(val))

    def __str__(self, n=0):
        return "(UaFloat): " + str(self._value) + "\n"


# +++++++++++++++++++ UaDouble +++++++++++++++++++++++
class UaDouble(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Double*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Double", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_Double", _val(val))

    def __str__(self, n=0):
        return "(UaDouble): " + str(self._value) + "\n"


# +++++++++++++++++++ UaStatusCode +++++++++++++++++++++++
class UaStatusCode(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_StatusCode*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_StatusCode", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_StatusCode", _val(val))

    def __str__(self, n=0):
        return "(UaStatusCode): " + str(self._value) + "\n"


# +++++++++++++++++++ UaDateTime +++++++++++++++++++++++
class UaDateTime(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_DateTime*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_DateTime", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("UA_DateTime", _val(val))

    def __str__(self, n=0):
        return "(UaDateTime): " + str(self._value) + "\n"


