from intermediateApi import ffi, lib

ffi.new("enum UA_NodeIdType*", 0)

# if val is a primitive type, then _ptr returns a pointer to a COPY of the value!!!
def _ptr(val):
    c_type = str(val).split("'")[1]
    if "&" in c_type:
        return ffi.addressof(val)
    if "*" in c_type or "[" in c_type:
        return val
    else:
        try:
            return ffi.cast(c_type + "*", ffi.addressof(val))
        except TypeError:
            return ffi.new(c_type + "*", val)


def _val(val):
    if _is_ptr(val):
        return val[0]
    else:
        return val


def _is_ptr(val):
    if "*" in str(val) or "[" in str(val):
        return True
    else:
        return False


class UaType:
    # __value should always be a pointer, so if it has to be dereferenced call ._value (for getter)
    # TODO: Idea -> free the passed memory when ever a primitive type is copied in _ptr.
    #  Then all base types hold their owner.
    def __init__(self, val, is_pointer=False):
        if not is_pointer:
            val = _ptr(val)
        self.___value = val
        self._is_pointer = is_pointer

    @property
    def _value(self):
        return self.__value[0]

    @property
    def __value(self):
        return self.___value

    @__value.setter
    def __value(self, val):
        self.___value = val

    def __str__(self, n=0):
        return str(self._value)


# +++++++++++++++++++ Void +++++++++++++++++++++++
class Void(UaType):
    def __init__(self, data=None, val=None, is_pointer=True):
        if data is not None:
            val = ffi.new_handle(data)

        super().__init__(ffi.cast("void*", _ptr(val)), is_pointer)

    # TODO: Should this be possible? Where/which references will be changed?
    @UaType._value.setter
    def _value(self, val):
        self.__value = ffi.cast("void*", _val(val))

    def data(self):
        return ffi.from_handle(self.__value)

    def __str__(self, n=0):
        return "(Void): " + str(self.data()) + "\n"


# +++++++++++++++++++ SizeT +++++++++++++++++++++++
class SizeT(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("size_t*"), is_pointer)
        else:
            super().__init__(ffi.cast("size_t", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("size_t", _val(val))

    def __str__(self, n=0):
        return "(SizeT): " + str(self._value) + "\n"


# +++++++++++++++++++ CString +++++++++++++++++++++++
class CString(UaType):
    def __init__(self, p_val: bytes = b"", is_pointer=True, val=None):
        if val is None:
            super().__init__(ffi.new("char[]", p_val), is_pointer)
            self._p_value = p_val
        else:
            super().__init__(val, is_pointer)
            self._p_value = ffi.string(val)

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val: bytes):
        self._p_value = val
        self.__value = ffi.new("char[]", self._p_value)

    @UaType._value.setter
    def _value(self, val):
        self.__value = val
        self._p_value = ffi.string(val)

    def __str__(self, n=0):
        return "(CString): " + str(self._p_value) + "\n"


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ------------------------------------ COMMON --------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

# -------------------------------------------------------------
# --------------------------- Enums ---------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaAttributeId +++++++++++++++++++++++
class UaAttributeId(UaType):
    UA_ATTRIBUTEID_NODEID = 1
    UA_ATTRIBUTEID_NODECLASS = 2
    UA_ATTRIBUTEID_BROWSENAME = 3
    UA_ATTRIBUTEID_DISPLAYNAME = 4
    UA_ATTRIBUTEID_DESCRIPTION = 5
    UA_ATTRIBUTEID_WRITEMASK = 6
    UA_ATTRIBUTEID_USERWRITEMASK = 7
    UA_ATTRIBUTEID_ISABSTRACT = 8
    UA_ATTRIBUTEID_SYMMETRIC = 9
    UA_ATTRIBUTEID_INVERSENAME = 10
    UA_ATTRIBUTEID_CONTAINSNOLOOPS = 11
    UA_ATTRIBUTEID_EVENTNOTIFIER = 12
    UA_ATTRIBUTEID_VALUE = 13
    UA_ATTRIBUTEID_DATATYPE = 14
    UA_ATTRIBUTEID_VALUERANK = 15
    UA_ATTRIBUTEID_ARRAYDIMENSIONS = 16
    UA_ATTRIBUTEID_ACCESSLEVEL = 17
    UA_ATTRIBUTEID_USERACCESSLEVEL = 18
    UA_ATTRIBUTEID_MINIMUMSAMPLINGINTERVAL = 19
    UA_ATTRIBUTEID_HISTORIZING = 20
    UA_ATTRIBUTEID_EXECUTABLE = 21
    UA_ATTRIBUTEID_USEREXECUTABLE = 22
    UA_ATTRIBUTEID_DATATYPEDEFINITION = 23
    UA_ATTRIBUTEID_ROLEPERMISSIONS = 24
    UA_ATTRIBUTEID_USERROLEPERMISSIONS = 25
    UA_ATTRIBUTEID_ACCESSRESTRICTIONS = 26
    UA_ATTRIBUTEID_ACCESSLEVELEX = 27

    val_to_string = dict([
        (1, "UA_ATTRIBUTEID_NODEID"),
        (2, "UA_ATTRIBUTEID_NODECLASS"),
        (3, "UA_ATTRIBUTEID_BROWSENAME"),
        (4, "UA_ATTRIBUTEID_DISPLAYNAME"),
        (5, "UA_ATTRIBUTEID_DESCRIPTION"),
        (6, "UA_ATTRIBUTEID_WRITEMASK"),
        (7, "UA_ATTRIBUTEID_USERWRITEMASK"),
        (8, "UA_ATTRIBUTEID_ISABSTRACT"),
        (9, "UA_ATTRIBUTEID_SYMMETRIC"),
        (10, "UA_ATTRIBUTEID_INVERSENAME"),
        (11, "UA_ATTRIBUTEID_CONTAINSNOLOOPS"),
        (12, "UA_ATTRIBUTEID_EVENTNOTIFIER"),
        (13, "UA_ATTRIBUTEID_VALUE"),
        (14, "UA_ATTRIBUTEID_DATATYPE"),
        (15, "UA_ATTRIBUTEID_VALUERANK"),
        (16, "UA_ATTRIBUTEID_ARRAYDIMENSIONS"),
        (17, "UA_ATTRIBUTEID_ACCESSLEVEL"),
        (18, "UA_ATTRIBUTEID_USERACCESSLEVEL"),
        (19, "UA_ATTRIBUTEID_MINIMUMSAMPLINGINTERVAL"),
        (20, "UA_ATTRIBUTEID_HISTORIZING"),
        (21, "UA_ATTRIBUTEID_EXECUTABLE"),
        (22, "UA_ATTRIBUTEID_USEREXECUTABLE"),
        (23, "UA_ATTRIBUTEID_DATATYPEDEFINITION"),
        (24, "UA_ATTRIBUTEID_ROLEPERMISSIONS"),
        (25, "UA_ATTRIBUTEID_USERROLEPERMISSIONS"),
        (26, "UA_ATTRIBUTEID_ACCESSRESTRICTIONS"),
        (27, "UA_ATTRIBUTEID_ACCESSLEVELEX")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_AttributeId*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_AttributeId", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaAttributeId): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaRuleHandling +++++++++++++++++++++++
class UaRuleHandling(UaType):
    UA_RULEHANDLING_DEFAULT = 0
    UA_RULEHANDLING_ABORT = 1
    UA_RULEHANDLING_WARN = 2
    UA_RULEHANDLING_ACCEPT = 3

    val_to_string = dict([
        (0, "UA_RULEHANDLING_DEFAULT"),
        (1, "UA_RULEHANDLING_ABORT"),
        (2, "UA_RULEHANDLING_WARN"),
        (3, "UA_RULEHANDLING_ACCEPT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_RuleHandling*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_RuleHandling", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaRuleHandling): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaOrder +++++++++++++++++++++++
class UaOrder(UaType):
    UA_ORDER_LESS = -1
    UA_ORDER_EQ = 0
    UA_ORDER_MORE = 1

    val_to_string = dict([
        (-1, "UA_ORDER_LESS"),
        (0, "UA_ORDER_EQ"),
        (1, "UA_ORDER_MORE")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Order*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Order", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaOrder): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaSecureChannelState +++++++++++++++++++++++
class UaSecureChannelState(UaType):
    UA_SECURECHANNELSTATE_CLOSED = 0
    UA_SECURECHANNELSTATE_HEL_SENT = 1
    UA_SECURECHANNELSTATE_HEL_RECEIVED = 2
    UA_SECURECHANNELSTATE_ACK_SENT = 3
    UA_SECURECHANNELSTATE_ACK_RECEIVED = 4
    UA_SECURECHANNELSTATE_OPN_SENT = 5
    UA_SECURECHANNELSTATE_OPEN = 6
    UA_SECURECHANNELSTATE_CLOSING = 7

    val_to_string = dict([
        (0, "UA_SECURECHANNELSTATE_CLOSED"),
        (1, "UA_SECURECHANNELSTATE_HEL_SENT"),
        (2, "UA_SECURECHANNELSTATE_HEL_RECEIVED"),
        (3, "UA_SECURECHANNELSTATE_ACK_SENT"),
        (4, "UA_SECURECHANNELSTATE_ACK_RECEIVED"),
        (5, "UA_SECURECHANNELSTATE_OPN_SENT"),
        (6, "UA_SECURECHANNELSTATE_OPEN"),
        (7, "UA_SECURECHANNELSTATE_CLOSING")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_SecureChannelState*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_SecureChannelState", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaSecureChannelState): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaSessionState +++++++++++++++++++++++
class UaSessionState(UaType):
    UA_SESSIONSTATE_CLOSED = 0
    UA_SESSIONSTATE_CREATE_REQUESTED = 1
    UA_SESSIONSTATE_CREATED = 2
    UA_SESSIONSTATE_ACTIVATE_REQUESTED = 3
    UA_SESSIONSTATE_ACTIVATED = 4
    UA_SESSIONSTATE_CLOSING = 5

    val_to_string = dict([
        (0, "UA_SESSIONSTATE_CLOSED"),
        (1, "UA_SESSIONSTATE_CREATE_REQUESTED"),
        (2, "UA_SESSIONSTATE_CREATED"),
        (3, "UA_SESSIONSTATE_ACTIVATE_REQUESTED"),
        (4, "UA_SESSIONSTATE_ACTIVATED"),
        (5, "UA_SESSIONSTATE_CLOSING")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_SessionState*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_SessionState", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaSessionState): {self.val_to_string[self._value]} ({str(self._value)})\n"


# -------------------------------------------------------------
# -------------------------- Structs --------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaNetworkStatistics +++++++++++++++++++++++
class UaNetworkStatistics(UaType):
    def __init__(self, val=ffi.new("UA_NetworkStatistics*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._current_connection_count = SizeT(val=val.currentConnectionCount, is_pointer=False)
        self._cumulated_connection_count = SizeT(val=val.cumulatedConnectionCount, is_pointer=False)
        self._rejected_connection_count = SizeT(val=val.rejectedConnectionCount, is_pointer=False)
        self._connection_timeout_count = SizeT(val=val.connectionTimeoutCount, is_pointer=False)
        self._connection_abort_count = SizeT(val=val.connectionAbortCount, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._current_connection_count.__value[0] = _val(val.currentConnectionCount)
        self._cumulated_connection_count.__value[0] = _val(val.cumulatedConnectionCount)
        self._rejected_connection_count.__value[0] = _val(val.rejectedConnectionCount)
        self._connection_timeout_count.__value[0] = _val(val.connectionTimeoutCount)
        self._connection_abort_count.__value[0] = _val(val.connectionAbortCount)

    @property
    def current_connection_count(self):
        return self._current_connection_count

    @property
    def cumulated_connection_count(self):
        return self._cumulated_connection_count

    @property
    def rejected_connection_count(self):
        return self._rejected_connection_count

    @property
    def connection_timeout_count(self):
        return self._connection_timeout_count

    @property
    def connection_abort_count(self):
        return self._connection_abort_count

    @current_connection_count.setter
    def current_connection_count(self, val):
        self._current_connection_count = val
        self._value.currentConnectionCount = val._value

    @cumulated_connection_count.setter
    def cumulated_connection_count(self, val):
        self._cumulated_connection_count = val
        self._value.cumulatedConnectionCount = val._value

    @rejected_connection_count.setter
    def rejected_connection_count(self, val):
        self._rejected_connection_count = val
        self._value.rejectedConnectionCount = val._value

    @connection_timeout_count.setter
    def connection_timeout_count(self, val):
        self._connection_timeout_count = val
        self._value.connectionTimeoutCount = val._value

    @connection_abort_count.setter
    def connection_abort_count(self, val):
        self._connection_abort_count = val
        self._value.connectionAbortCount = val._value

    def __str__(self, n=0):
        return ("(UaNetworkStatistics) :\n" +
                "\t" * (n + 1) + "current_connection_count" + self._current_connection_count.__str__(n + 1) +
                "\t" * (n + 1) + "cumulated_connection_count" + self._cumulated_connection_count.__str__(n + 1) +
                "\t" * (n + 1) + "rejected_connection_count" + self._rejected_connection_count.__str__(n + 1) +
                "\t" * (n + 1) + "connection_timeout_count" + self._connection_timeout_count.__str__(n + 1) +
                "\t" * (n + 1) + "connection_abort_count" + self._connection_abort_count.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSecureChannelStatistics +++++++++++++++++++++++
class UaSecureChannelStatistics(UaType):
    def __init__(self, val=ffi.new("UA_SecureChannelStatistics*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._current_channel_count = SizeT(val=val.currentChannelCount, is_pointer=False)
        self._cumulated_channel_count = SizeT(val=val.cumulatedChannelCount, is_pointer=False)
        self._rejected_channel_count = SizeT(val=val.rejectedChannelCount, is_pointer=False)
        self._channel_timeout_count = SizeT(val=val.channelTimeoutCount, is_pointer=False)
        self._channel_abort_count = SizeT(val=val.channelAbortCount, is_pointer=False)
        self._channel_purge_count = SizeT(val=val.channelPurgeCount, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._current_channel_count.__value[0] = _val(val.currentChannelCount)
        self._cumulated_channel_count.__value[0] = _val(val.cumulatedChannelCount)
        self._rejected_channel_count.__value[0] = _val(val.rejectedChannelCount)
        self._channel_timeout_count.__value[0] = _val(val.channelTimeoutCount)
        self._channel_abort_count.__value[0] = _val(val.channelAbortCount)
        self._channel_purge_count.__value[0] = _val(val.channelPurgeCount)

    @property
    def current_channel_count(self):
        return self._current_channel_count

    @property
    def cumulated_channel_count(self):
        return self._cumulated_channel_count

    @property
    def rejected_channel_count(self):
        return self._rejected_channel_count

    @property
    def channel_timeout_count(self):
        return self._channel_timeout_count

    @property
    def channel_abort_count(self):
        return self._channel_abort_count

    @property
    def channel_purge_count(self):
        return self._channel_purge_count

    @current_channel_count.setter
    def current_channel_count(self, val):
        self._current_channel_count = val
        self._value.currentChannelCount = val._value

    @cumulated_channel_count.setter
    def cumulated_channel_count(self, val):
        self._cumulated_channel_count = val
        self._value.cumulatedChannelCount = val._value

    @rejected_channel_count.setter
    def rejected_channel_count(self, val):
        self._rejected_channel_count = val
        self._value.rejectedChannelCount = val._value

    @channel_timeout_count.setter
    def channel_timeout_count(self, val):
        self._channel_timeout_count = val
        self._value.channelTimeoutCount = val._value

    @channel_abort_count.setter
    def channel_abort_count(self, val):
        self._channel_abort_count = val
        self._value.channelAbortCount = val._value

    @channel_purge_count.setter
    def channel_purge_count(self, val):
        self._channel_purge_count = val
        self._value.channelPurgeCount = val._value

    def __str__(self, n=0):
        return ("(UaSecureChannelStatistics) :\n" +
                "\t" * (n + 1) + "current_channel_count" + self._current_channel_count.__str__(n + 1) +
                "\t" * (n + 1) + "cumulated_channel_count" + self._cumulated_channel_count.__str__(n + 1) +
                "\t" * (n + 1) + "rejected_channel_count" + self._rejected_channel_count.__str__(n + 1) +
                "\t" * (n + 1) + "channel_timeout_count" + self._channel_timeout_count.__str__(n + 1) +
                "\t" * (n + 1) + "channel_abort_count" + self._channel_abort_count.__str__(n + 1) +
                "\t" * (n + 1) + "channel_purge_count" + self._channel_purge_count.__str__(n + 1) + "\n")


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ---------------------------------- PRIMITIVE -------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

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
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_Byte", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if self._is_pointer:
            self.__value = _ptr(val, "UA_Byte")
        else:
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
    UA_STATUSCODE_INFOTYPE_DATAVALUE = 0x00000400
    UA_STATUSCODE_INFOBITS_OVERFLOW = 0x00000080
    UA_STATUSCODE_GOOD = 0x00000000
    UA_STATUSCODE_UNCERTAIN = 0x40000000
    UA_STATUSCODE_BAD = 0x80000000
    UA_STATUSCODE_BADUNEXPECTEDERROR = 0x80010000
    UA_STATUSCODE_BADINTERNALERROR = 0x80020000
    UA_STATUSCODE_BADOUTOFMEMORY = 0x80030000
    UA_STATUSCODE_BADRESOURCEUNAVAILABLE = 0x80040000
    UA_STATUSCODE_BADCOMMUNICATIONERROR = 0x80050000
    UA_STATUSCODE_BADENCODINGERROR = 0x80060000
    UA_STATUSCODE_BADDECODINGERROR = 0x80070000
    UA_STATUSCODE_BADENCODINGLIMITSEXCEEDED = 0x80080000
    UA_STATUSCODE_BADREQUESTTOOLARGE = 0x80B80000
    UA_STATUSCODE_BADRESPONSETOOLARGE = 0x80B90000
    UA_STATUSCODE_BADUNKNOWNRESPONSE = 0x80090000
    UA_STATUSCODE_BADTIMEOUT = 0x800A0000
    UA_STATUSCODE_BADSERVICEUNSUPPORTED = 0x800B0000
    UA_STATUSCODE_BADSHUTDOWN = 0x800C0000
    UA_STATUSCODE_BADSERVERNOTCONNECTED = 0x800D0000
    UA_STATUSCODE_BADSERVERHALTED = 0x800E0000
    UA_STATUSCODE_BADNOTHINGTODO = 0x800F0000
    UA_STATUSCODE_BADTOOMANYOPERATIONS = 0x80100000
    UA_STATUSCODE_BADTOOMANYMONITOREDITEMS = 0x80DB0000
    UA_STATUSCODE_BADDATATYPEIDUNKNOWN = 0x80110000
    UA_STATUSCODE_BADCERTIFICATEINVALID = 0x80120000
    UA_STATUSCODE_BADSECURITYCHECKSFAILED = 0x80130000
    UA_STATUSCODE_BADCERTIFICATEPOLICYCHECKFAILED = 0x81140000
    UA_STATUSCODE_BADCERTIFICATETIMEINVALID = 0x80140000
    UA_STATUSCODE_BADCERTIFICATEISSUERTIMEINVALID = 0x80150000
    UA_STATUSCODE_BADCERTIFICATEHOSTNAMEINVALID = 0x80160000
    UA_STATUSCODE_BADCERTIFICATEURIINVALID = 0x80170000
    UA_STATUSCODE_BADCERTIFICATEUSENOTALLOWED = 0x80180000
    UA_STATUSCODE_BADCERTIFICATEISSUERUSENOTALLOWED = 0x80190000
    UA_STATUSCODE_BADCERTIFICATEUNTRUSTED = 0x801A0000
    UA_STATUSCODE_BADCERTIFICATEREVOCATIONUNKNOWN = 0x801B0000
    UA_STATUSCODE_BADCERTIFICATEISSUERREVOCATIONUNKNOWN = 0x801C0000
    UA_STATUSCODE_BADCERTIFICATEREVOKED = 0x801D0000
    UA_STATUSCODE_BADCERTIFICATEISSUERREVOKED = 0x801E0000
    UA_STATUSCODE_BADCERTIFICATECHAININCOMPLETE = 0x810D0000
    UA_STATUSCODE_BADUSERACCESSDENIED = 0x801F0000
    UA_STATUSCODE_BADIDENTITYTOKENINVALID = 0x80200000
    UA_STATUSCODE_BADIDENTITYTOKENREJECTED = 0x80210000
    UA_STATUSCODE_BADSECURECHANNELIDINVALID = 0x80220000
    UA_STATUSCODE_BADINVALIDTIMESTAMP = 0x80230000
    UA_STATUSCODE_BADNONCEINVALID = 0x80240000
    UA_STATUSCODE_BADSESSIONIDINVALID = 0x80250000
    UA_STATUSCODE_BADSESSIONCLOSED = 0x80260000
    UA_STATUSCODE_BADSESSIONNOTACTIVATED = 0x80270000
    UA_STATUSCODE_BADSUBSCRIPTIONIDINVALID = 0x80280000
    UA_STATUSCODE_BADREQUESTHEADERINVALID = 0x802A0000
    UA_STATUSCODE_BADTIMESTAMPSTORETURNINVALID = 0x802B0000
    UA_STATUSCODE_BADREQUESTCANCELLEDBYCLIENT = 0x802C0000
    UA_STATUSCODE_BADTOOMANYARGUMENTS = 0x80E50000
    UA_STATUSCODE_BADLICENSEEXPIRED = 0x810E0000
    UA_STATUSCODE_BADLICENSELIMITSEXCEEDED = 0x810F0000
    UA_STATUSCODE_BADLICENSENOTAVAILABLE = 0x81100000
    UA_STATUSCODE_GOODSUBSCRIPTIONTRANSFERRED = 0x002D0000
    UA_STATUSCODE_GOODCOMPLETESASYNCHRONOUSLY = 0x002E0000
    UA_STATUSCODE_GOODOVERLOAD = 0x002F0000
    UA_STATUSCODE_GOODCLAMPED = 0x00300000
    UA_STATUSCODE_BADNOCOMMUNICATION = 0x80310000
    UA_STATUSCODE_BADWAITINGFORINITIALDATA = 0x80320000
    UA_STATUSCODE_BADNODEIDINVALID = 0x80330000
    UA_STATUSCODE_BADNODEIDUNKNOWN = 0x80340000
    UA_STATUSCODE_BADATTRIBUTEIDINVALID = 0x80350000
    UA_STATUSCODE_BADINDEXRANGEINVALID = 0x80360000
    UA_STATUSCODE_BADINDEXRANGENODATA = 0x80370000
    UA_STATUSCODE_BADDATAENCODINGINVALID = 0x80380000
    UA_STATUSCODE_BADDATAENCODINGUNSUPPORTED = 0x80390000
    UA_STATUSCODE_BADNOTREADABLE = 0x803A0000
    UA_STATUSCODE_BADNOTWRITABLE = 0x803B0000
    UA_STATUSCODE_BADOUTOFRANGE = 0x803C0000
    UA_STATUSCODE_BADNOTSUPPORTED = 0x803D0000
    UA_STATUSCODE_BADNOTFOUND = 0x803E0000
    UA_STATUSCODE_BADOBJECTDELETED = 0x803F0000
    UA_STATUSCODE_BADNOTIMPLEMENTED = 0x80400000
    UA_STATUSCODE_BADMONITORINGMODEINVALID = 0x80410000
    UA_STATUSCODE_BADMONITOREDITEMIDINVALID = 0x80420000
    UA_STATUSCODE_BADMONITOREDITEMFILTERINVALID = 0x80430000
    UA_STATUSCODE_BADMONITOREDITEMFILTERUNSUPPORTED = 0x80440000
    UA_STATUSCODE_BADFILTERNOTALLOWED = 0x80450000
    UA_STATUSCODE_BADSTRUCTUREMISSING = 0x80460000
    UA_STATUSCODE_BADEVENTFILTERINVALID = 0x80470000
    UA_STATUSCODE_BADCONTENTFILTERINVALID = 0x80480000
    UA_STATUSCODE_BADFILTEROPERATORINVALID = 0x80C10000
    UA_STATUSCODE_BADFILTEROPERATORUNSUPPORTED = 0x80C20000
    UA_STATUSCODE_BADFILTEROPERANDCOUNTMISMATCH = 0x80C30000
    UA_STATUSCODE_BADFILTEROPERANDINVALID = 0x80490000
    UA_STATUSCODE_BADFILTERELEMENTINVALID = 0x80C40000
    UA_STATUSCODE_BADFILTERLITERALINVALID = 0x80C50000
    UA_STATUSCODE_BADCONTINUATIONPOINTINVALID = 0x804A0000
    UA_STATUSCODE_BADNOCONTINUATIONPOINTS = 0x804B0000
    UA_STATUSCODE_BADREFERENCETYPEIDINVALID = 0x804C0000
    UA_STATUSCODE_BADBROWSEDIRECTIONINVALID = 0x804D0000
    UA_STATUSCODE_BADNODENOTINVIEW = 0x804E0000
    UA_STATUSCODE_BADNUMERICOVERFLOW = 0x81120000
    UA_STATUSCODE_BADSERVERURIINVALID = 0x804F0000
    UA_STATUSCODE_BADSERVERNAMEMISSING = 0x80500000
    UA_STATUSCODE_BADDISCOVERYURLMISSING = 0x80510000
    UA_STATUSCODE_BADSEMPAHOREFILEMISSING = 0x80520000
    UA_STATUSCODE_BADREQUESTTYPEINVALID = 0x80530000
    UA_STATUSCODE_BADSECURITYMODEREJECTED = 0x80540000
    UA_STATUSCODE_BADSECURITYPOLICYREJECTED = 0x80550000
    UA_STATUSCODE_BADTOOMANYSESSIONS = 0x80560000
    UA_STATUSCODE_BADUSERSIGNATUREINVALID = 0x80570000
    UA_STATUSCODE_BADAPPLICATIONSIGNATUREINVALID = 0x80580000
    UA_STATUSCODE_BADNOVALIDCERTIFICATES = 0x80590000
    UA_STATUSCODE_BADIDENTITYCHANGENOTSUPPORTED = 0x80C60000
    UA_STATUSCODE_BADREQUESTCANCELLEDBYREQUEST = 0x805A0000
    UA_STATUSCODE_BADPARENTNODEIDINVALID = 0x805B0000
    UA_STATUSCODE_BADREFERENCENOTALLOWED = 0x805C0000
    UA_STATUSCODE_BADNODEIDREJECTED = 0x805D0000
    UA_STATUSCODE_BADNODEIDEXISTS = 0x805E0000
    UA_STATUSCODE_BADNODECLASSINVALID = 0x805F0000
    UA_STATUSCODE_BADBROWSENAMEINVALID = 0x80600000
    UA_STATUSCODE_BADBROWSENAMEDUPLICATED = 0x80610000
    UA_STATUSCODE_BADNODEATTRIBUTESINVALID = 0x80620000
    UA_STATUSCODE_BADTYPEDEFINITIONINVALID = 0x80630000
    UA_STATUSCODE_BADSOURCENODEIDINVALID = 0x80640000
    UA_STATUSCODE_BADTARGETNODEIDINVALID = 0x80650000
    UA_STATUSCODE_BADDUPLICATEREFERENCENOTALLOWED = 0x80660000
    UA_STATUSCODE_BADINVALIDSELFREFERENCE = 0x80670000
    UA_STATUSCODE_BADREFERENCELOCALONLY = 0x80680000
    UA_STATUSCODE_BADNODELETERIGHTS = 0x80690000
    UA_STATUSCODE_UNCERTAINREFERENCENOTDELETED = 0x40BC0000
    UA_STATUSCODE_BADSERVERINDEXINVALID = 0x806A0000
    UA_STATUSCODE_BADVIEWIDUNKNOWN = 0x806B0000
    UA_STATUSCODE_BADVIEWTIMESTAMPINVALID = 0x80C90000
    UA_STATUSCODE_BADVIEWPARAMETERMISMATCH = 0x80CA0000
    UA_STATUSCODE_BADVIEWVERSIONINVALID = 0x80CB0000
    UA_STATUSCODE_UNCERTAINNOTALLNODESAVAILABLE = 0x40C00000
    UA_STATUSCODE_GOODRESULTSMAYBEINCOMPLETE = 0x00BA0000
    UA_STATUSCODE_BADNOTTYPEDEFINITION = 0x80C80000
    UA_STATUSCODE_UNCERTAINREFERENCEOUTOFSERVER = 0x406C0000
    UA_STATUSCODE_BADTOOMANYMATCHES = 0x806D0000
    UA_STATUSCODE_BADQUERYTOOCOMPLEX = 0x806E0000
    UA_STATUSCODE_BADNOMATCH = 0x806F0000
    UA_STATUSCODE_BADMAXAGEINVALID = 0x80700000
    UA_STATUSCODE_BADSECURITYMODEINSUFFICIENT = 0x80E60000
    UA_STATUSCODE_BADHISTORYOPERATIONINVALID = 0x80710000
    UA_STATUSCODE_BADHISTORYOPERATIONUNSUPPORTED = 0x80720000
    UA_STATUSCODE_BADINVALIDTIMESTAMPARGUMENT = 0x80BD0000
    UA_STATUSCODE_BADWRITENOTSUPPORTED = 0x80730000
    UA_STATUSCODE_BADTYPEMISMATCH = 0x80740000
    UA_STATUSCODE_BADMETHODINVALID = 0x80750000
    UA_STATUSCODE_BADARGUMENTSMISSING = 0x80760000
    UA_STATUSCODE_BADNOTEXECUTABLE = 0x81110000
    UA_STATUSCODE_BADTOOMANYSUBSCRIPTIONS = 0x80770000
    UA_STATUSCODE_BADTOOMANYPUBLISHREQUESTS = 0x80780000
    UA_STATUSCODE_BADNOSUBSCRIPTION = 0x80790000
    UA_STATUSCODE_BADSEQUENCENUMBERUNKNOWN = 0x807A0000
    UA_STATUSCODE_GOODRETRANSMISSIONQUEUENOTSUPPORTED = 0x00DF0000
    UA_STATUSCODE_BADMESSAGENOTAVAILABLE = 0x807B0000
    UA_STATUSCODE_BADINSUFFICIENTCLIENTPROFILE = 0x807C0000
    UA_STATUSCODE_BADSTATENOTACTIVE = 0x80BF0000
    UA_STATUSCODE_BADALREADYEXISTS = 0x81150000
    UA_STATUSCODE_BADTCPSERVERTOOBUSY = 0x807D0000
    UA_STATUSCODE_BADTCPMESSAGETYPEINVALID = 0x807E0000
    UA_STATUSCODE_BADTCPSECURECHANNELUNKNOWN = 0x807F0000
    UA_STATUSCODE_BADTCPMESSAGETOOLARGE = 0x80800000
    UA_STATUSCODE_BADTCPNOTENOUGHRESOURCES = 0x80810000
    UA_STATUSCODE_BADTCPINTERNALERROR = 0x80820000
    UA_STATUSCODE_BADTCPENDPOINTURLINVALID = 0x80830000
    UA_STATUSCODE_BADREQUESTINTERRUPTED = 0x80840000
    UA_STATUSCODE_BADREQUESTTIMEOUT = 0x80850000
    UA_STATUSCODE_BADSECURECHANNELCLOSED = 0x80860000
    UA_STATUSCODE_BADSECURECHANNELTOKENUNKNOWN = 0x80870000
    UA_STATUSCODE_BADSEQUENCENUMBERINVALID = 0x80880000
    UA_STATUSCODE_BADPROTOCOLVERSIONUNSUPPORTED = 0x80BE0000
    UA_STATUSCODE_BADCONFIGURATIONERROR = 0x80890000
    UA_STATUSCODE_BADNOTCONNECTED = 0x808A0000
    UA_STATUSCODE_BADDEVICEFAILURE = 0x808B0000
    UA_STATUSCODE_BADSENSORFAILURE = 0x808C0000
    UA_STATUSCODE_BADOUTOFSERVICE = 0x808D0000
    UA_STATUSCODE_BADDEADBANDFILTERINVALID = 0x808E0000
    UA_STATUSCODE_UNCERTAINNOCOMMUNICATIONLASTUSABLEVALUE = 0x408F0000
    UA_STATUSCODE_UNCERTAINLASTUSABLEVALUE = 0x40900000
    UA_STATUSCODE_UNCERTAINSUBSTITUTEVALUE = 0x40910000
    UA_STATUSCODE_UNCERTAININITIALVALUE = 0x40920000
    UA_STATUSCODE_UNCERTAINSENSORNOTACCURATE = 0x40930000
    UA_STATUSCODE_UNCERTAINENGINEERINGUNITSEXCEEDED = 0x40940000
    UA_STATUSCODE_UNCERTAINSUBNORMAL = 0x40950000
    UA_STATUSCODE_GOODLOCALOVERRIDE = 0x00960000
    UA_STATUSCODE_BADREFRESHINPROGRESS = 0x80970000
    UA_STATUSCODE_BADCONDITIONALREADYDISABLED = 0x80980000
    UA_STATUSCODE_BADCONDITIONALREADYENABLED = 0x80CC0000
    UA_STATUSCODE_BADCONDITIONDISABLED = 0x80990000
    UA_STATUSCODE_BADEVENTIDUNKNOWN = 0x809A0000
    UA_STATUSCODE_BADEVENTNOTACKNOWLEDGEABLE = 0x80BB0000
    UA_STATUSCODE_BADDIALOGNOTACTIVE = 0x80CD0000
    UA_STATUSCODE_BADDIALOGRESPONSEINVALID = 0x80CE0000
    UA_STATUSCODE_BADCONDITIONBRANCHALREADYACKED = 0x80CF0000
    UA_STATUSCODE_BADCONDITIONBRANCHALREADYCONFIRMED = 0x80D00000
    UA_STATUSCODE_BADCONDITIONALREADYSHELVED = 0x80D10000
    UA_STATUSCODE_BADCONDITIONNOTSHELVED = 0x80D20000
    UA_STATUSCODE_BADSHELVINGTIMEOUTOFRANGE = 0x80D30000
    UA_STATUSCODE_BADNODATA = 0x809B0000
    UA_STATUSCODE_BADBOUNDNOTFOUND = 0x80D70000
    UA_STATUSCODE_BADBOUNDNOTSUPPORTED = 0x80D80000
    UA_STATUSCODE_BADDATALOST = 0x809D0000
    UA_STATUSCODE_BADDATAUNAVAILABLE = 0x809E0000
    UA_STATUSCODE_BADENTRYEXISTS = 0x809F0000
    UA_STATUSCODE_BADNOENTRYEXISTS = 0x80A00000
    UA_STATUSCODE_BADTIMESTAMPNOTSUPPORTED = 0x80A10000
    UA_STATUSCODE_GOODENTRYINSERTED = 0x00A20000
    UA_STATUSCODE_GOODENTRYREPLACED = 0x00A30000
    UA_STATUSCODE_UNCERTAINDATASUBNORMAL = 0x40A40000
    UA_STATUSCODE_GOODNODATA = 0x00A50000
    UA_STATUSCODE_GOODMOREDATA = 0x00A60000
    UA_STATUSCODE_BADAGGREGATELISTMISMATCH = 0x80D40000
    UA_STATUSCODE_BADAGGREGATENOTSUPPORTED = 0x80D50000
    UA_STATUSCODE_BADAGGREGATEINVALIDINPUTS = 0x80D60000
    UA_STATUSCODE_BADAGGREGATECONFIGURATIONREJECTED = 0x80DA0000
    UA_STATUSCODE_GOODDATAIGNORED = 0x00D90000
    UA_STATUSCODE_BADREQUESTNOTALLOWED = 0x80E40000
    UA_STATUSCODE_BADREQUESTNOTCOMPLETE = 0x81130000
    UA_STATUSCODE_BADTICKETREQUIRED = 0x811F0000
    UA_STATUSCODE_BADTICKETINVALID = 0x81200000
    UA_STATUSCODE_GOODEDITED = 0x00DC0000
    UA_STATUSCODE_GOODPOSTACTIONFAILED = 0x00DD0000
    UA_STATUSCODE_UNCERTAINDOMINANTVALUECHANGED = 0x40DE0000
    UA_STATUSCODE_GOODDEPENDENTVALUECHANGED = 0x00E00000
    UA_STATUSCODE_BADDOMINANTVALUECHANGED = 0x80E10000
    UA_STATUSCODE_UNCERTAINDEPENDENTVALUECHANGED = 0x40E20000
    UA_STATUSCODE_BADDEPENDENTVALUECHANGED = 0x80E30000
    UA_STATUSCODE_GOODEDITED_DEPENDENTVALUECHANGED = 0x01160000
    UA_STATUSCODE_GOODEDITED_DOMINANTVALUECHANGED = 0x01170000
    UA_STATUSCODE_GOODEDITED_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED = 0x01180000
    UA_STATUSCODE_BADEDITED_OUTOFRANGE = 0x81190000
    UA_STATUSCODE_BADINITIALVALUE_OUTOFRANGE = 0x811A0000
    UA_STATUSCODE_BADOUTOFRANGE_DOMINANTVALUECHANGED = 0x811B0000
    UA_STATUSCODE_BADEDITED_OUTOFRANGE_DOMINANTVALUECHANGED = 0x811C0000
    UA_STATUSCODE_BADOUTOFRANGE_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED = 0x811D0000
    UA_STATUSCODE_BADEDITED_OUTOFRANGE_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED = 0x811E0000
    UA_STATUSCODE_GOODCOMMUNICATIONEVENT = 0x00A70000
    UA_STATUSCODE_GOODSHUTDOWNEVENT = 0x00A80000
    UA_STATUSCODE_GOODCALLAGAIN = 0x00A90000
    UA_STATUSCODE_GOODNONCRITICALTIMEOUT = 0x00AA0000
    UA_STATUSCODE_BADINVALIDARGUMENT = 0x80AB0000
    UA_STATUSCODE_BADCONNECTIONREJECTED = 0x80AC0000
    UA_STATUSCODE_BADDISCONNECT = 0x80AD0000
    UA_STATUSCODE_BADCONNECTIONCLOSED = 0x80AE0000
    UA_STATUSCODE_BADINVALIDSTATE = 0x80AF0000
    UA_STATUSCODE_BADENDOFSTREAM = 0x80B00000
    UA_STATUSCODE_BADNODATAAVAILABLE = 0x80B10000
    UA_STATUSCODE_BADWAITINGFORRESPONSE = 0x80B20000
    UA_STATUSCODE_BADOPERATIONABANDONED = 0x80B30000
    UA_STATUSCODE_BADEXPECTEDSTREAMTOBLOCK = 0x80B40000
    UA_STATUSCODE_BADWOULDBLOCK = 0x80B50000
    UA_STATUSCODE_BADSYNTAXERROR = 0x80B60000
    UA_STATUSCODE_BADMAXCONNECTIONSREACHED = 0x80B70000

    val_to_string = dict([
        (0x00000400, "UA_STATUSCODE_INFOTYPE_DATAVALUE"),
        (0x00000080, "UA_STATUSCODE_INFOBITS_OVERFLOW"),
        (0x00000000, "UA_STATUSCODE_GOOD"),
        (0x40000000, "UA_STATUSCODE_UNCERTAIN"),
        (0x80000000, "UA_STATUSCODE_BAD"),
        (0x80010000, "UA_STATUSCODE_BADUNEXPECTEDERROR"),
        (0x80020000, "UA_STATUSCODE_BADINTERNALERROR"),
        (0x80030000, "UA_STATUSCODE_BADOUTOFMEMORY"),
        (0x80040000, "UA_STATUSCODE_BADRESOURCEUNAVAILABLE"),
        (0x80050000, "UA_STATUSCODE_BADCOMMUNICATIONERROR"),
        (0x80060000, "UA_STATUSCODE_BADENCODINGERROR"),
        (0x80070000, "UA_STATUSCODE_BADDECODINGERROR"),
        (0x80080000, "UA_STATUSCODE_BADENCODINGLIMITSEXCEEDED"),
        (0x80B80000, "UA_STATUSCODE_BADREQUESTTOOLARGE"),
        (0x80B90000, "UA_STATUSCODE_BADRESPONSETOOLARGE"),
        (0x80090000, "UA_STATUSCODE_BADUNKNOWNRESPONSE"),
        (0x800A0000, "UA_STATUSCODE_BADTIMEOUT"),
        (0x800B0000, "UA_STATUSCODE_BADSERVICEUNSUPPORTED"),
        (0x800C0000, "UA_STATUSCODE_BADSHUTDOWN"),
        (0x800D0000, "UA_STATUSCODE_BADSERVERNOTCONNECTED"),
        (0x800E0000, "UA_STATUSCODE_BADSERVERHALTED"),
        (0x800F0000, "UA_STATUSCODE_BADNOTHINGTODO"),
        (0x80100000, "UA_STATUSCODE_BADTOOMANYOPERATIONS"),
        (0x80DB0000, "UA_STATUSCODE_BADTOOMANYMONITOREDITEMS"),
        (0x80110000, "UA_STATUSCODE_BADDATATYPEIDUNKNOWN"),
        (0x80120000, "UA_STATUSCODE_BADCERTIFICATEINVALID"),
        (0x80130000, "UA_STATUSCODE_BADSECURITYCHECKSFAILED"),
        (0x81140000, "UA_STATUSCODE_BADCERTIFICATEPOLICYCHECKFAILED"),
        (0x80140000, "UA_STATUSCODE_BADCERTIFICATETIMEINVALID"),
        (0x80150000, "UA_STATUSCODE_BADCERTIFICATEISSUERTIMEINVALID"),
        (0x80160000, "UA_STATUSCODE_BADCERTIFICATEHOSTNAMEINVALID"),
        (0x80170000, "UA_STATUSCODE_BADCERTIFICATEURIINVALID"),
        (0x80180000, "UA_STATUSCODE_BADCERTIFICATEUSENOTALLOWED"),
        (0x80190000, "UA_STATUSCODE_BADCERTIFICATEISSUERUSENOTALLOWED"),
        (0x801A0000, "UA_STATUSCODE_BADCERTIFICATEUNTRUSTED"),
        (0x801B0000, "UA_STATUSCODE_BADCERTIFICATEREVOCATIONUNKNOWN"),
        (0x801C0000, "UA_STATUSCODE_BADCERTIFICATEISSUERREVOCATIONUNKNOWN"),
        (0x801D0000, "UA_STATUSCODE_BADCERTIFICATEREVOKED"),
        (0x801E0000, "UA_STATUSCODE_BADCERTIFICATEISSUERREVOKED"),
        (0x810D0000, "UA_STATUSCODE_BADCERTIFICATECHAININCOMPLETE"),
        (0x801F0000, "UA_STATUSCODE_BADUSERACCESSDENIED"),
        (0x80200000, "UA_STATUSCODE_BADIDENTITYTOKENINVALID"),
        (0x80210000, "UA_STATUSCODE_BADIDENTITYTOKENREJECTED"),
        (0x80220000, "UA_STATUSCODE_BADSECURECHANNELIDINVALID"),
        (0x80230000, "UA_STATUSCODE_BADINVALIDTIMESTAMP"),
        (0x80240000, "UA_STATUSCODE_BADNONCEINVALID"),
        (0x80250000, "UA_STATUSCODE_BADSESSIONIDINVALID"),
        (0x80260000, "UA_STATUSCODE_BADSESSIONCLOSED"),
        (0x80270000, "UA_STATUSCODE_BADSESSIONNOTACTIVATED"),
        (0x80280000, "UA_STATUSCODE_BADSUBSCRIPTIONIDINVALID"),
        (0x802A0000, "UA_STATUSCODE_BADREQUESTHEADERINVALID"),
        (0x802B0000, "UA_STATUSCODE_BADTIMESTAMPSTORETURNINVALID"),
        (0x802C0000, "UA_STATUSCODE_BADREQUESTCANCELLEDBYCLIENT"),
        (0x80E50000, "UA_STATUSCODE_BADTOOMANYARGUMENTS"),
        (0x810E0000, "UA_STATUSCODE_BADLICENSEEXPIRED"),
        (0x810F0000, "UA_STATUSCODE_BADLICENSELIMITSEXCEEDED"),
        (0x81100000, "UA_STATUSCODE_BADLICENSENOTAVAILABLE"),
        (0x002D0000, "UA_STATUSCODE_GOODSUBSCRIPTIONTRANSFERRED"),
        (0x002E0000, "UA_STATUSCODE_GOODCOMPLETESASYNCHRONOUSLY"),
        (0x002F0000, "UA_STATUSCODE_GOODOVERLOAD"),
        (0x00300000, "UA_STATUSCODE_GOODCLAMPED"),
        (0x80310000, "UA_STATUSCODE_BADNOCOMMUNICATION"),
        (0x80320000, "UA_STATUSCODE_BADWAITINGFORINITIALDATA"),
        (0x80330000, "UA_STATUSCODE_BADNODEIDINVALID"),
        (0x80340000, "UA_STATUSCODE_BADNODEIDUNKNOWN"),
        (0x80350000, "UA_STATUSCODE_BADATTRIBUTEIDINVALID"),
        (0x80360000, "UA_STATUSCODE_BADINDEXRANGEINVALID"),
        (0x80370000, "UA_STATUSCODE_BADINDEXRANGENODATA"),
        (0x80380000, "UA_STATUSCODE_BADDATAENCODINGINVALID"),
        (0x80390000, "UA_STATUSCODE_BADDATAENCODINGUNSUPPORTED"),
        (0x803A0000, "UA_STATUSCODE_BADNOTREADABLE"),
        (0x803B0000, "UA_STATUSCODE_BADNOTWRITABLE"),
        (0x803C0000, "UA_STATUSCODE_BADOUTOFRANGE"),
        (0x803D0000, "UA_STATUSCODE_BADNOTSUPPORTED"),
        (0x803E0000, "UA_STATUSCODE_BADNOTFOUND"),
        (0x803F0000, "UA_STATUSCODE_BADOBJECTDELETED"),
        (0x80400000, "UA_STATUSCODE_BADNOTIMPLEMENTED"),
        (0x80410000, "UA_STATUSCODE_BADMONITORINGMODEINVALID"),
        (0x80420000, "UA_STATUSCODE_BADMONITOREDITEMIDINVALID"),
        (0x80430000, "UA_STATUSCODE_BADMONITOREDITEMFILTERINVALID"),
        (0x80440000, "UA_STATUSCODE_BADMONITOREDITEMFILTERUNSUPPORTED"),
        (0x80450000, "UA_STATUSCODE_BADFILTERNOTALLOWED"),
        (0x80460000, "UA_STATUSCODE_BADSTRUCTUREMISSING"),
        (0x80470000, "UA_STATUSCODE_BADEVENTFILTERINVALID"),
        (0x80480000, "UA_STATUSCODE_BADCONTENTFILTERINVALID"),
        (0x80C10000, "UA_STATUSCODE_BADFILTEROPERATORINVALID"),
        (0x80C20000, "UA_STATUSCODE_BADFILTEROPERATORUNSUPPORTED"),
        (0x80C30000, "UA_STATUSCODE_BADFILTEROPERANDCOUNTMISMATCH"),
        (0x80490000, "UA_STATUSCODE_BADFILTEROPERANDINVALID"),
        (0x80C40000, "UA_STATUSCODE_BADFILTERELEMENTINVALID"),
        (0x80C50000, "UA_STATUSCODE_BADFILTERLITERALINVALID"),
        (0x804A0000, "UA_STATUSCODE_BADCONTINUATIONPOINTINVALID"),
        (0x804B0000, "UA_STATUSCODE_BADNOCONTINUATIONPOINTS"),
        (0x804C0000, "UA_STATUSCODE_BADREFERENCETYPEIDINVALID"),
        (0x804D0000, "UA_STATUSCODE_BADBROWSEDIRECTIONINVALID"),
        (0x804E0000, "UA_STATUSCODE_BADNODENOTINVIEW"),
        (0x81120000, "UA_STATUSCODE_BADNUMERICOVERFLOW"),
        (0x804F0000, "UA_STATUSCODE_BADSERVERURIINVALID"),
        (0x80500000, "UA_STATUSCODE_BADSERVERNAMEMISSING"),
        (0x80510000, "UA_STATUSCODE_BADDISCOVERYURLMISSING"),
        (0x80520000, "UA_STATUSCODE_BADSEMPAHOREFILEMISSING"),
        (0x80530000, "UA_STATUSCODE_BADREQUESTTYPEINVALID"),
        (0x80540000, "UA_STATUSCODE_BADSECURITYMODEREJECTED"),
        (0x80550000, "UA_STATUSCODE_BADSECURITYPOLICYREJECTED"),
        (0x80560000, "UA_STATUSCODE_BADTOOMANYSESSIONS"),
        (0x80570000, "UA_STATUSCODE_BADUSERSIGNATUREINVALID"),
        (0x80580000, "UA_STATUSCODE_BADAPPLICATIONSIGNATUREINVALID"),
        (0x80590000, "UA_STATUSCODE_BADNOVALIDCERTIFICATES"),
        (0x80C60000, "UA_STATUSCODE_BADIDENTITYCHANGENOTSUPPORTED"),
        (0x805A0000, "UA_STATUSCODE_BADREQUESTCANCELLEDBYREQUEST"),
        (0x805B0000, "UA_STATUSCODE_BADPARENTNODEIDINVALID"),
        (0x805C0000, "UA_STATUSCODE_BADREFERENCENOTALLOWED"),
        (0x805D0000, "UA_STATUSCODE_BADNODEIDREJECTED"),
        (0x805E0000, "UA_STATUSCODE_BADNODEIDEXISTS"),
        (0x805F0000, "UA_STATUSCODE_BADNODECLASSINVALID"),
        (0x80600000, "UA_STATUSCODE_BADBROWSENAMEINVALID"),
        (0x80610000, "UA_STATUSCODE_BADBROWSENAMEDUPLICATED"),
        (0x80620000, "UA_STATUSCODE_BADNODEATTRIBUTESINVALID"),
        (0x80630000, "UA_STATUSCODE_BADTYPEDEFINITIONINVALID"),
        (0x80640000, "UA_STATUSCODE_BADSOURCENODEIDINVALID"),
        (0x80650000, "UA_STATUSCODE_BADTARGETNODEIDINVALID"),
        (0x80660000, "UA_STATUSCODE_BADDUPLICATEREFERENCENOTALLOWED"),
        (0x80670000, "UA_STATUSCODE_BADINVALIDSELFREFERENCE"),
        (0x80680000, "UA_STATUSCODE_BADREFERENCELOCALONLY"),
        (0x80690000, "UA_STATUSCODE_BADNODELETERIGHTS"),
        (0x40BC0000, "UA_STATUSCODE_UNCERTAINREFERENCENOTDELETED"),
        (0x806A0000, "UA_STATUSCODE_BADSERVERINDEXINVALID"),
        (0x806B0000, "UA_STATUSCODE_BADVIEWIDUNKNOWN"),
        (0x80C90000, "UA_STATUSCODE_BADVIEWTIMESTAMPINVALID"),
        (0x80CA0000, "UA_STATUSCODE_BADVIEWPARAMETERMISMATCH"),
        (0x80CB0000, "UA_STATUSCODE_BADVIEWVERSIONINVALID"),
        (0x40C00000, "UA_STATUSCODE_UNCERTAINNOTALLNODESAVAILABLE"),
        (0x00BA0000, "UA_STATUSCODE_GOODRESULTSMAYBEINCOMPLETE"),
        (0x80C80000, "UA_STATUSCODE_BADNOTTYPEDEFINITION"),
        (0x406C0000, "UA_STATUSCODE_UNCERTAINREFERENCEOUTOFSERVER"),
        (0x806D0000, "UA_STATUSCODE_BADTOOMANYMATCHES"),
        (0x806E0000, "UA_STATUSCODE_BADQUERYTOOCOMPLEX"),
        (0x806F0000, "UA_STATUSCODE_BADNOMATCH"),
        (0x80700000, "UA_STATUSCODE_BADMAXAGEINVALID"),
        (0x80E60000, "UA_STATUSCODE_BADSECURITYMODEINSUFFICIENT"),
        (0x80710000, "UA_STATUSCODE_BADHISTORYOPERATIONINVALID"),
        (0x80720000, "UA_STATUSCODE_BADHISTORYOPERATIONUNSUPPORTED"),
        (0x80BD0000, "UA_STATUSCODE_BADINVALIDTIMESTAMPARGUMENT"),
        (0x80730000, "UA_STATUSCODE_BADWRITENOTSUPPORTED"),
        (0x80740000, "UA_STATUSCODE_BADTYPEMISMATCH"),
        (0x80750000, "UA_STATUSCODE_BADMETHODINVALID"),
        (0x80760000, "UA_STATUSCODE_BADARGUMENTSMISSING"),
        (0x81110000, "UA_STATUSCODE_BADNOTEXECUTABLE"),
        (0x80770000, "UA_STATUSCODE_BADTOOMANYSUBSCRIPTIONS"),
        (0x80780000, "UA_STATUSCODE_BADTOOMANYPUBLISHREQUESTS"),
        (0x80790000, "UA_STATUSCODE_BADNOSUBSCRIPTION"),
        (0x807A0000, "UA_STATUSCODE_BADSEQUENCENUMBERUNKNOWN"),
        (0x00DF0000, "UA_STATUSCODE_GOODRETRANSMISSIONQUEUENOTSUPPORTED"),
        (0x807B0000, "UA_STATUSCODE_BADMESSAGENOTAVAILABLE"),
        (0x807C0000, "UA_STATUSCODE_BADINSUFFICIENTCLIENTPROFILE"),
        (0x80BF0000, "UA_STATUSCODE_BADSTATENOTACTIVE"),
        (0x81150000, "UA_STATUSCODE_BADALREADYEXISTS"),
        (0x807D0000, "UA_STATUSCODE_BADTCPSERVERTOOBUSY"),
        (0x807E0000, "UA_STATUSCODE_BADTCPMESSAGETYPEINVALID"),
        (0x807F0000, "UA_STATUSCODE_BADTCPSECURECHANNELUNKNOWN"),
        (0x80800000, "UA_STATUSCODE_BADTCPMESSAGETOOLARGE"),
        (0x80810000, "UA_STATUSCODE_BADTCPNOTENOUGHRESOURCES"),
        (0x80820000, "UA_STATUSCODE_BADTCPINTERNALERROR"),
        (0x80830000, "UA_STATUSCODE_BADTCPENDPOINTURLINVALID"),
        (0x80840000, "UA_STATUSCODE_BADREQUESTINTERRUPTED"),
        (0x80850000, "UA_STATUSCODE_BADREQUESTTIMEOUT"),
        (0x80860000, "UA_STATUSCODE_BADSECURECHANNELCLOSED"),
        (0x80870000, "UA_STATUSCODE_BADSECURECHANNELTOKENUNKNOWN"),
        (0x80880000, "UA_STATUSCODE_BADSEQUENCENUMBERINVALID"),
        (0x80BE0000, "UA_STATUSCODE_BADPROTOCOLVERSIONUNSUPPORTED"),
        (0x80890000, "UA_STATUSCODE_BADCONFIGURATIONERROR"),
        (0x808A0000, "UA_STATUSCODE_BADNOTCONNECTED"),
        (0x808B0000, "UA_STATUSCODE_BADDEVICEFAILURE"),
        (0x808C0000, "UA_STATUSCODE_BADSENSORFAILURE"),
        (0x808D0000, "UA_STATUSCODE_BADOUTOFSERVICE"),
        (0x808E0000, "UA_STATUSCODE_BADDEADBANDFILTERINVALID"),
        (0x408F0000, "UA_STATUSCODE_UNCERTAINNOCOMMUNICATIONLASTUSABLEVALUE"),
        (0x40900000, "UA_STATUSCODE_UNCERTAINLASTUSABLEVALUE"),
        (0x40910000, "UA_STATUSCODE_UNCERTAINSUBSTITUTEVALUE"),
        (0x40920000, "UA_STATUSCODE_UNCERTAININITIALVALUE"),
        (0x40930000, "UA_STATUSCODE_UNCERTAINSENSORNOTACCURATE"),
        (0x40940000, "UA_STATUSCODE_UNCERTAINENGINEERINGUNITSEXCEEDED"),
        (0x40950000, "UA_STATUSCODE_UNCERTAINSUBNORMAL"),
        (0x00960000, "UA_STATUSCODE_GOODLOCALOVERRIDE"),
        (0x80970000, "UA_STATUSCODE_BADREFRESHINPROGRESS"),
        (0x80980000, "UA_STATUSCODE_BADCONDITIONALREADYDISABLED"),
        (0x80CC0000, "UA_STATUSCODE_BADCONDITIONALREADYENABLED"),
        (0x80990000, "UA_STATUSCODE_BADCONDITIONDISABLED"),
        (0x809A0000, "UA_STATUSCODE_BADEVENTIDUNKNOWN"),
        (0x80BB0000, "UA_STATUSCODE_BADEVENTNOTACKNOWLEDGEABLE"),
        (0x80CD0000, "UA_STATUSCODE_BADDIALOGNOTACTIVE"),
        (0x80CE0000, "UA_STATUSCODE_BADDIALOGRESPONSEINVALID"),
        (0x80CF0000, "UA_STATUSCODE_BADCONDITIONBRANCHALREADYACKED"),
        (0x80D00000, "UA_STATUSCODE_BADCONDITIONBRANCHALREADYCONFIRMED"),
        (0x80D10000, "UA_STATUSCODE_BADCONDITIONALREADYSHELVED"),
        (0x80D20000, "UA_STATUSCODE_BADCONDITIONNOTSHELVED"),
        (0x80D30000, "UA_STATUSCODE_BADSHELVINGTIMEOUTOFRANGE"),
        (0x809B0000, "UA_STATUSCODE_BADNODATA"),
        (0x80D70000, "UA_STATUSCODE_BADBOUNDNOTFOUND"),
        (0x80D80000, "UA_STATUSCODE_BADBOUNDNOTSUPPORTED"),
        (0x809D0000, "UA_STATUSCODE_BADDATALOST"),
        (0x809E0000, "UA_STATUSCODE_BADDATAUNAVAILABLE"),
        (0x809F0000, "UA_STATUSCODE_BADENTRYEXISTS"),
        (0x80A00000, "UA_STATUSCODE_BADNOENTRYEXISTS"),
        (0x80A10000, "UA_STATUSCODE_BADTIMESTAMPNOTSUPPORTED"),
        (0x00A20000, "UA_STATUSCODE_GOODENTRYINSERTED"),
        (0x00A30000, "UA_STATUSCODE_GOODENTRYREPLACED"),
        (0x40A40000, "UA_STATUSCODE_UNCERTAINDATASUBNORMAL"),
        (0x00A50000, "UA_STATUSCODE_GOODNODATA"),
        (0x00A60000, "UA_STATUSCODE_GOODMOREDATA"),
        (0x80D40000, "UA_STATUSCODE_BADAGGREGATELISTMISMATCH"),
        (0x80D50000, "UA_STATUSCODE_BADAGGREGATENOTSUPPORTED"),
        (0x80D60000, "UA_STATUSCODE_BADAGGREGATEINVALIDINPUTS"),
        (0x80DA0000, "UA_STATUSCODE_BADAGGREGATECONFIGURATIONREJECTED"),
        (0x00D90000, "UA_STATUSCODE_GOODDATAIGNORED"),
        (0x80E40000, "UA_STATUSCODE_BADREQUESTNOTALLOWED"),
        (0x81130000, "UA_STATUSCODE_BADREQUESTNOTCOMPLETE"),
        (0x811F0000, "UA_STATUSCODE_BADTICKETREQUIRED"),
        (0x81200000, "UA_STATUSCODE_BADTICKETINVALID"),
        (0x00DC0000, "UA_STATUSCODE_GOODEDITED"),
        (0x00DD0000, "UA_STATUSCODE_GOODPOSTACTIONFAILED"),
        (0x40DE0000, "UA_STATUSCODE_UNCERTAINDOMINANTVALUECHANGED"),
        (0x00E00000, "UA_STATUSCODE_GOODDEPENDENTVALUECHANGED"),
        (0x80E10000, "UA_STATUSCODE_BADDOMINANTVALUECHANGED"),
        (0x40E20000, "UA_STATUSCODE_UNCERTAINDEPENDENTVALUECHANGED"),
        (0x80E30000, "UA_STATUSCODE_BADDEPENDENTVALUECHANGED"),
        (0x01160000, "UA_STATUSCODE_GOODEDITED_DEPENDENTVALUECHANGED"),
        (0x01170000, "UA_STATUSCODE_GOODEDITED_DOMINANTVALUECHANGED"),
        (0x01180000, "UA_STATUSCODE_GOODEDITED_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED"),
        (0x81190000, "UA_STATUSCODE_BADEDITED_OUTOFRANGE"),
        (0x811A0000, "UA_STATUSCODE_BADINITIALVALUE_OUTOFRANGE"),
        (0x811B0000, "UA_STATUSCODE_BADOUTOFRANGE_DOMINANTVALUECHANGED"),
        (0x811C0000, "UA_STATUSCODE_BADEDITED_OUTOFRANGE_DOMINANTVALUECHANGED"),
        (0x811D0000, "UA_STATUSCODE_BADOUTOFRANGE_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED"),
        (0x811E0000, "UA_STATUSCODE_BADEDITED_OUTOFRANGE_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED"),
        (0x00A70000, "UA_STATUSCODE_GOODCOMMUNICATIONEVENT"),
        (0x00A80000, "UA_STATUSCODE_GOODSHUTDOWNEVENT"),
        (0x00A90000, "UA_STATUSCODE_GOODCALLAGAIN"),
        (0x00AA0000, "UA_STATUSCODE_GOODNONCRITICALTIMEOUT"),
        (0x80AB0000, "UA_STATUSCODE_BADINVALIDARGUMENT"),
        (0x80AC0000, "UA_STATUSCODE_BADCONNECTIONREJECTED"),
        (0x80AD0000, "UA_STATUSCODE_BADDISCONNECT"),
        (0x80AE0000, "UA_STATUSCODE_BADCONNECTIONCLOSED"),
        (0x80AF0000, "UA_STATUSCODE_BADINVALIDSTATE"),
        (0x80B00000, "UA_STATUSCODE_BADENDOFSTREAM"),
        (0x80B10000, "UA_STATUSCODE_BADNODATAAVAILABLE"),
        (0x80B20000, "UA_STATUSCODE_BADWAITINGFORRESPONSE"),
        (0x80B30000, "UA_STATUSCODE_BADOPERATIONABANDONED"),
        (0x80B40000, "UA_STATUSCODE_BADEXPECTEDSTREAMTOBLOCK"),
        (0x80B50000, "UA_STATUSCODE_BADWOULDBLOCK"),
        (0x80B60000, "UA_STATUSCODE_BADSYNTAXERROR"),
        (0x80B70000, "UA_STATUSCODE_BADMAXCONNECTIONSREACHED")])

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

    def is_bad(self):
        return lib.UA_StatusCode_isBad(self._value)


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

    @staticmethod
    def now():
        return UaDateTime(lib.UA_DateTime_now())

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# -------------------------------- ENUM/STRUCT -------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------


# -------------------------------------------------------------
# --------------------------- Enums ---------------------------
# -------------------------------------------------------------

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
        else:
            super().__init__(ffi.cast("enum UA_NodeIdType", _val(val)), is_pointer)

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
    def __init__(self, p_val: str = "", val=ffi.new("UA_String*"), is_pointer=False):
        if p_val != "":
            val = lib.UA_String_fromChars(bytes(p_val, 'utf-8'))
        super().__init__(val=val, is_pointer=is_pointer)
        self._length = SizeT(val=val.length, is_pointer=False)
        self._data = UaByte(val=val.data, is_pointer=True)

    # TODO: Rather make new UaString?
    #   -> not sure where the pointer is directed and if there is enough memory for evtually more bytes than befor
    #   -> memory management for alloced memory from UA_String_fromChars

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._length.__value[0] = _val(val.length)
        self._data.__value = val.data

    @property
    def length(self):
        return self._length

    @property
    def data(self):
        return self._data

    def __eq__(self, ua_string):
        return lib.UA_String_equal(self.__value, ua_string.__value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def equal_ignore_case(self, ua_string):
        return lib.UA_String_equal_ignorecase(self.__value, ua_string.__value)

    def to_string(self):
        return ffi.string(ffi.cast(f"char[{self.length._value}]", self.data._UaType__value), self.length._value).decode("utf-8")

    def __str__(self, n=0):
        return "(UaString): " + self.to_string() + "\n"


# +++++++++++++++++++ UaByteString +++++++++++++++++++++++
UaByteString = UaString

# +++++++++++++++++++ UaXmlElement +++++++++++++++++++++++
UaXmlElement = UaString


# +++++++++++++++++++ UaDateTimeStruct +++++++++++++++++++++++
# TODO: Methods from types.h
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
                "\t" * (n + 1) + "nano_sec" + self._nano_sec.__str__(n + 1) +
                "\t" * (n + 1) + "micro_sec" + self._micro_sec.__str__(n + 1) +
                "\t" * (n + 1) + "milli_sec" + self._milli_sec.__str__(n + 1) +
                "\t" * (n + 1) + "sec" + self._sec.__str__(n + 1) +
                "\t" * (n + 1) + "min" + self._min.__str__(n + 1) +
                "\t" * (n + 1) + "hour" + self._hour.__str__(n + 1) +
                "\t" * (n + 1) + "day" + self._day.__str__(n + 1) +
                "\t" * (n + 1) + "month" + self._month.__str__(n + 1) +
                "\t" * (n + 1) + "year" + self._year.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaGuid +++++++++++++++++++++++
class UaGuid(UaType):
    NULL = lib.UA_GUID_NULL

    def __init__(self, string="", val=ffi.new("UA_Guid*"), is_pointer=False):
        if string != "":
            val = lib.UA_GUID(bytes(string, 'utf-8'))
            if val == UaGuid.NULL:
                raise ValueError(
                    f""""{string}" has to be formatted like: 
        "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", with X in [0..9, A..F]""")

        super().__init__(val=val, is_pointer=is_pointer)

        self._data1 = UaUInt32(val=val.data1, is_pointer=False)
        self._data2 = UaUInt16(val=val.data2, is_pointer=False)
        self._data3 = UaUInt16(val=val.data3, is_pointer=False)
        self._data4 = UaByte(val=val.data4, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._data1.__value[0] = val.data1
        self._data2.__value[0] = val.data2
        self._data3.__value[0] = val.data3
        self._data4.__value = val.data4

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
        self._value.data4 = val.__value

    def __eq__(self, other):
        return lib.UA_Guid_equal(self._value, other._value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self, n=0):
        d1 = '{0:0{1}X}'.format(self._data1._value, 8)
        d2 = '{0:0{1}X}'.format(self._data2._value, 4)
        d3 = '{0:0{1}X}'.format(self._data3._value, 4)
        d4 = ""
        for i in range(2):
            d4 += '{0:0{1}X}'.format(self._data4.__value[i], 2)
        d5 = ""
        for i in range(2, 8):
            d5 += '{0:0{1}X}'.format(self._data4.__value[i], 2)

        return "\t" * n + "UaGuid: " + f"{d1}-{d2}-{d3}-{d4}-{d5}" + "\n"


# +++++++++++++++++++ UaNodeId +++++++++++++++++++++++
class UaNodeId(UaType):
    NULL = lib.UA_NODEID_NULL

    # TODO: refactor
    # TODO: Memory management
    def __init__(self, ns_index=None, ident=None, is_pointer=False, val=ffi.new("UA_NodeId*")):
        if ns_index is not None and ident is not None:
            if type(ns_index) is int:
                if type(ident) is int:
                    val = lib.UA_NODEID_NUMERIC(ns_index, ident)
                elif type(ident) is UaUInt32:
                    val = lib.UA_NODEID_NUMERIC(ns_index, ident._value)
                elif type(ident) is str:
                    val = lib.UA_NODEID_STRING_ALLOC(ns_index, bytes(ident, 'utf-8'))
                elif type(ident) is bytearray:
                    val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index, ident)
                elif type(ident) is UaString:
                    val = lib.UA_NODEID_STRING(ns_index, bytes(str(ident), 'utf-8'))
                elif type(ident) is UaGuid:
                    val = lib.A_NODEID_GUID(ns_index, ident._value)
                elif type(ident) is UaByteString:
                    val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
                else:
                    raise TypeError(f"ident={ident} has invalid type, must be int, UaUInt32, "
                                    f"str, bytearray, UaString, UaGuid or UaByteString")
            elif type(ns_index) is UaUInt16:
                if type(ident) is int:
                    val = lib.UA_NODEID_NUMERIC(ns_index._value, ident)
                elif type(ident) is UaUInt32:
                    val = lib.UA_NODEID_NUMERIC(ns_index._value, ident._value)
                elif type(ident) is str:
                    val = lib.UA_NODEID_STRING_ALLOC(ns_index._value, bytes(ident, 'utf-8'))
                elif type(ident) is bytearray:
                    val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index._value, ident)
                elif type(ident) is UaString:
                    val = lib.UA_NODEID_STRING_ALLOC(ns_index._value, bytes(str(ident), 'utf-8'))
                elif type(ident) is UaGuid:
                    val = lib.A_NODEID_GUID(ns_index._value, ident._value)
                elif type(ident) is UaByteString:
                    val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index._value, bytes(str(ident), 'utf-8'))
                else:
                    raise TypeError(f"ident={ident} has invalid type, must be int, UaUInt32, "
                                    f"str, bytearray, UaString, UaGuid or UaByteString")
            else:
                raise TypeError(f"ns_index={ns_index} has invalid type, must be UaUInt16 or int")

        val = ffi.new("UA_NodeId*", _val(val))

        super().__init__(val=val, is_pointer=is_pointer)
        self._namespace_index = UaUInt16(val=val.namespaceIndex, is_pointer=False)
        self._identifier_type = UaNodeIdType(val=val.identifierType, is_pointer=False)

        #TODO: refactor
        if self._identifier_type._value == 0:
            self._identifier = UaUInt32(val=val.identifier.numeric)
        elif self._identifier_type._value == 1:
            self._identifier = UaUInt32(val=val.identifier.numeric)
        elif self._identifier_type._value == 2:
            self._identifier = UaUInt32(val=val.identifier.numeric)
        elif self._identifier_type._value == 3:
            self._identifier = UaString(val=val.identifier.string)
        elif self._identifier_type._value == 4:
            self._identifier = UaGuid(val=val.identifier.guid)
        elif self._identifier_type._value == 5:
            self._identifier = UaByteString(val=val.identifier.byteString)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._namespace_index.__value[0] = _val(val.namespaceIndex)
        self._identifier_type.__value[0] = _val(val.identifierType)
        cases = {
            0: val.identifier.numeric,
            1: val.identifier.numeric,
            2: val.identifier.numeric,
            3: val.identifier.string,
            4: val.identifier.guid,
            5: val.identifier.byteString
        }
        self._identifier.__value[0] = cases[self._identifier_type._value]

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

    def __str__(self, n=0):
        return ("(UaNodeId) :\n" +
                "\t" * (n + 1) + "namespace_index" + self._namespace_index.__str__(n + 1) +
                "\t" * (n + 1) + "identifier_type" + self._identifier_type.__str__(n + 1) +
                "\t" * (n + 1) + "identifier" + self._identifier.__str__(n + 1) + "\n")

    def __eq__(self, other):
        return lib.UA_NodeId_equal(self.__value, other.__value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_null(self):
        return lib.UA_NodeId_isNull(self.__value)


# +++++++++++++++++++ UaExpandedNodeId +++++++++++++++++++++++
class UaExpandedNodeId(UaType):
    NULL = lib.UA_EXPANDEDNODEID_NULL

    # TODO: refactor
    # TODO: Memory management
    def __init__(self, ns_index=None, ident=None, is_pointer=False, val=ffi.new("UA_NodeId*")):
        if ns_index is not None and ident is not None:
            if type(ns_index) is int:
                if type(ident) is int:
                    val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index, ident)
                elif type(ident) is UaUInt32:
                    val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index, ident._value)
                elif type(ident) is str:
                    val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index, bytes(ident, 'utf-8'))
                elif type(ident) is bytearray:
                    val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index, ident)
                elif type(ident) is UaString:
                    val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
                elif type(ident) is UaGuid:
                    val = lib.A_EXPANDEDNODEID_GUID(ns_index, ident._value)
                elif type(ident) is UaByteString:
                    val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
                else:
                    raise TypeError(f"ident={ident} has invalid type, must be int, UaUInt32, "
                                    f"str, bytearray, UaString, UaGuid or UaByteString")
            elif type(ns_index) is UaUInt16:
                if type(ident) is int:
                    val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index._value, ident)
                elif type(ident) is UaUInt32:
                    val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index._value, ident._value)
                elif type(ident) is str:
                    val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index._value, bytes(ident, 'utf-8'))
                elif type(ident) is bytearray:
                    val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index._value, ident)
                elif type(ident) is UaString:
                    val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index._value, bytes(str(ident), 'utf-8'))
                elif type(ident) is UaGuid:
                    val = lib.A_EXPANDEDNODEID_GUID(ns_index._value, ident._value)
                elif type(ident) is UaByteString:
                    val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index._value, bytes(str(ident), 'utf-8'))
                else:
                    raise TypeError(f"ident={ident} has invalid type, must be int, UaUInt32, "
                                    f"str, bytearray, UaString, UaGuid or UaByteString")
            else:
                raise TypeError(f"ns_index={ns_index} has invalid type, must be UaUInt16 or int")

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
                "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1) +
                "\t" * (n + 1) + "namespace_uri" + self._namespace_uri.__str__(n + 1) +
                "\t" * (n + 1) + "server_index" + self._server_index.__str__(n + 1) + "\n")

    def is_local(self):
        return lib.UA_ExpandedNodeId_isLocal(self.__value)

    def __eq__(self, other):
        return lib.UA_ExpandedNodeId_equal(self.__value, other.__value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return lib.UA_ExpandedNodeId_order(self.__value, other.__value) == 1

    def __lt__(self, other):
        return lib.UA_ExpandedNodeId_order(self.__value, other.__value) == -1

    def __ge__(self, other):
        return lib.UA_ExpandedNodeId_order(self.__value, other.__value) in [1, 0]

    def __le__(self, other):
        return lib.UA_ExpandedNodeId_order(self.__value, other.__value) in [-1, 0]

    def __hash__(self):
        return lib.UA_ExpandedNodeId_hash(self.__value)


# +++++++++++++++++++ UaQualifiedName +++++++++++++++++++++++
class UaQualifiedName(UaType):
    def __init__(self, ns_index=None, string=None, val=ffi.new("UA_QualifiedName*"), is_pointer=False):
        # TODO: refactor
        # TODO: Memory management
        if ns_index is not None and string is not None:
            if type(ns_index) is int:
                if type(string) is str:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index, bytes(string, "utf-8"))
                elif type(string) is UaString:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index, bytes(str(string), "utf-8"))
                else:
                    raise AttributeError(f"string={type(string)} has to be str or UaString")
            elif type(ns_index) is UaUInt16:
                if type(string) is str:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index._value, bytes(string, "utf-8"))
                elif type(string) is UaString:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index._value, bytes(str(string), "utf-8"))
                else:
                    raise AttributeError(f"string={string} has to be str or UaString")
            else:
                raise AttributeError(f"ns_index={ns_index} has to be int or UaUInt16")

        val = ffi.new("UA_QualifiedName*", _val(val))

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
                "\t" * (n + 1) + "namespace_index" + self._namespace_index.__str__(n + 1) +
                "\t" * (n + 1) + "name" + self._name.__str__(n + 1) + "\n")

    def is_null(self):
        return lib.UA_QualifiedName_isNull(self.__value)

    def __hash__(self):
        return lib.UA_QualifiedName_hash(self.__value)

    def __eq__(self, other):
        return lib.UA_QualifiedName_equal(self.__value, other.__value)


# +++++++++++++++++++ UaLocalizedText +++++++++++++++++++++++
class UaLocalizedText(UaType):
    # TODO: refactor
    # TODO: Memory management
    def __init__(self, locale=None, text=None, val=ffi.new("UA_LocalizedText*"), is_pointer=False):
        if locale is not None and text is not None:
            if type(locale) is str:
                if type(text) is str:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale, "utf-8"), bytes(text, "utf-8"))
                if type(text) is UaString:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale, "utf-8"), bytes(text.to_string(), "utf-8"))
                else:
                    raise AttributeError(f"text={text} has to be str or UaString")
            if type(locale) is UaString:
                if type(text) is str:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale.to_string(), "utf-8"), bytes(text, "utf-8"))
                if type(text) is UaString:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale.to_string(), "utf-8"), bytes(text.to_string(), "utf-8"))
                else:
                    raise AttributeError(f"text={text} has to be str or UaString")
            else:
                raise AttributeError(f"locale={locale} has to be str or UaUInt16")

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
                "\t" * (n + 1) + "locale" + self._locale.__str__(n + 1) +
                "\t" * (n + 1) + "text" + self._text.__str__(n + 1) + "\n")


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
                "\t" * (n + 1) + "min" + self._min.__str__(n + 1) +
                "\t" * (n + 1) + "max" + self._max.__str__(n + 1) + "\n")


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
        self._dimensions.__value = val.dimensions

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
        self._value.dimensions = val.__value

    def __str__(self, n=0):
        return ("(UaNumericRange) :\n" +
                "\t" * (n + 1) + "dimensions_size" + self._dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "dimensions" + self._dimensions.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaVariant +++++++++++++++++++++++
class UaVariant(UaType):
    def __init__(self, val=ffi.new("UA_Variant*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._type = UaDataType(val=val.type, is_pointer=True)
        self._storage_type = UaVariantStorageType(val=val.storageType, is_pointer=False)
        self._array_length = SizeT(val=val.arrayLength, is_pointer=False)
        self._data = Void(val=val.data, is_pointer=True)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._type.__value = val.type
        self._storage_type.__value[0] = _val(val.storageType)
        self._array_length.__value[0] = _val(val.arrayLength)
        self._data.__value = val.data
        self._array_dimensions_size.__value[0] = _val(val.arrayDimensionsSize)
        self._array_dimensions.__value = val.arrayDimensions

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
        self._value.type = val.__value

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
        self._value.data = val.__value

    @array_dimensions_size.setter
    def array_dimensions_size(self, val):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._value

    @array_dimensions.setter
    def array_dimensions(self, val):
        self._array_dimensions = val
        self._value.arrayDimensions = val.__value

    def __str__(self, n=0):
        return ("(UaVariant) :\n" +
                "\t" * (n + 1) + "type" + self._type.__str__(n + 1) +
                "\t" * (n + 1) + "storage_type" + self._storage_type.__str__(n + 1) +
                "\t" * (n + 1) + "array_length" + self._array_length.__str__(n + 1) +
                "\t" * (n + 1) + "data" + self._data.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions_size" + self._array_dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions" + self._array_dimensions.__str__(n + 1) + "\n")

    def is_empty(self):
        lib.UA_Variant_isEmpty(self.__value)

    def is_scalar(self):
        lib.UA_Variant_isScalar(self.__value)

    def has_scalar_type(self, data_type):
        lib.UA_Variant_hasScalarType(self.__value, data_type._ref())

    def has_array_type(self, data_type):
        lib.UA_Variant_hasArrayType(self.__value, data_type._ref())

    # TODO: memory management
    def _set_attributes(self):
        self._type._value = self.__value.type
        self._storage_type._value = self.__value.storageType
        self._array_length._value = self.__value.arrayLength
        self._data._value = self.__value.data
        self._array_dimensions_size._value = self.__value.arrayDimensionsSize
        self._array_dimensions._value = self.__value.arrayDimensions

    def set_scalar(self, data, data_type):
        lib.UA_Variant_setScalarCopy(self.__value, ffi.new_handle(data), data_type.__value)
        self._set_attributes()

    def set_array(self, array, size, data_type):
        if size is int:
            size = SizeT(size)
        if size is not SizeT:
            raise AttributeError(f"size={size} has to be int or SizeT")
        status_code = lib.UA_Variant_setArrayCopy(self.__value, ffi.new_handle(array), size._value, data_type.__value)
        status_code = UaStatusCode(status_code)
        if not status_code.is_bad():
            self._set_attributes()
        else:
            raise Exception(f"An Error occured - {str(status_code)}")

    def copy_range_to(self, variant, num_range: UaNumericRange):
        status_code = lib.UA_Variant_copyRange(self.__value, variant.__value, num_range._value)
        status_code = UaStatusCode(status_code)
        if not status_code.is_bad():
            self._set_attributes()
        else:
            raise AttributeError(f"An Error occured - {str(status_code)}")

    def set_range_copy(self, array, size, num_range: UaNumericRange):
        if size is int:
            size = SizeT(size)
        if size is not SizeT:
            raise AttributeError(f"size={size} has to be int or SizeT")
        status_code = lib.UA_Variant_setRangeCopy(self.__value, ffi.new_handle(array), size, num_range._value)
        status_code = UaStatusCode(status_code)
        if not status_code.is_bad():
            self._set_attributes()
        else:
            raise AttributeError(f"An Error occured - {str(status_code)}")


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
                "\t" * (n + 1) + "value" + self._value.__str__(n + 1) +
                "\t" * (n + 1) + "source_timestamp" + self._source_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "server_timestamp" + self._server_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "source_picoseconds" + self._source_picoseconds.__str__(n + 1) +
                "\t" * (n + 1) + "server_picoseconds" + self._server_picoseconds.__str__(n + 1) +
                "\t" * (n + 1) + "status" + self._status.__str__(n + 1) +
                "\t" * (n + 1) + "has_value" + self._has_value.__str__(n + 1) +
                "\t" * (n + 1) + "has_status" + self._has_status.__str__(n + 1) +
                "\t" * (n + 1) + "has_source_timestamp" + self._has_source_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "has_server_timestamp" + self._has_server_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "has_source_picoseconds" + self._has_source_picoseconds.__str__(n + 1) +
                "\t" * (n + 1) + "has_server_picoseconds" + self._has_server_picoseconds.__str__(n + 1) + "\n")


class UaExtensionObject(UaType):
    def __init__(self, val=ffi.new("UA_ExtensionObject*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        self._encoding = UaExtensionObjectEncoding(val=val.encoding)
        if self._encoding._value in [0, 1, 2]:
            self._type = UaNodeId(val=val.content.encoded.typeId)
            self._data = UaByteString(val=val.content.encoded.body)
        elif self._encoding._value in [3, 4]:
            self._type = UaDataType(val=val.content.decoded.type, is_pointer=True)
            self._data = Void(val.content.encoded.body)
        else:
            raise ValueError(f"Encoding does not exist.")

    # TODO: might cause trouble since at __value[0] might not be enough memory for an other encoding type
    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._encoding.__value[0] = _val(val.encoding)
        if self._encoding in [0, 1, 2]:
            self._type = UaNodeId(val.content.encoded.typeId)
            self._data = UaByteString(val.content.encoded.body)
        elif self._encoding in [3, 4]:
            self._type = UaDataType(val.content.decoded.type, is_pointer=True)
            self._data = Void(val.content.encoded.body)
        else:
            raise ValueError(f"Encoding does not exist.")

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        if self._encoding._value in [0, 1, 2] and type(val) not in UaNodeId:
            raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaNodeId")
        if self._encoding._value in [3, 4] and type(val) not in UaDataType:
            raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaDataType")
        self._type = val
        self._value.type = val._value if self._encoding._value < 3 else val.__value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        if self._encoding._value in [0, 1, 2] and type(val) is not UaByteString:
            raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaNodeId")
        if self._encoding._value in [3, 4] and type(val) is not Void:
            val = Void(val)

        self._data = val
        self._value.data = val._value if self._encoding._value < 3 else val.__value

    def __str__(self, n=0):
        return ("(UaExtensionObject) :\n" +
                "\t" * (n + 1) + "encoding" + self._encoding.__str__(n + 1) +
                "\t" * (n + 1) + "type" + self._type.__str__(n + 1) +
                "\t" * (n + 1) + "data" + self._data.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDiagnosticInfo +++++++++++++++++++++++
class UaDiagnosticInfo(UaType):
    def __init__(self, val=ffi.new("UA_DiagnosticInfo*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

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

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._has_symbolic_id.__value[0] = _val(val.hasSymbolicId)
        self._has_namespace_uri.__value[0] = _val(val.hasNamespaceUri)
        self._has_localized_text.__value[0] = _val(val.hasLocalizedText)
        self._has_locale.__value[0] = _val(val.hasLocale)
        self._has_additional_info.__value[0] = _val(val.hasAdditionalInfo)
        self._has_inner_status_code.__value[0] = _val(val.hasInnerStatusCode)
        self._has_inner_diagnostic_info.__value[0] = _val(val.hasInnerDiagnosticInfo)
        self._symbolic_id.__value[0] = _val(val.symbolicId)
        self._namespace_uri.__value[0] = _val(val.namespaceUri)
        self._localized_text.__value[0] = _val(val.localizedText)
        self._locale.__value[0] = _val(val.locale)
        self._additional_info.__value[0] = _val(val.additionalInfo)
        self._inner_status_code.__value[0] = _val(val.innerStatusCode)
        self._inner_diagnostic_info.__value = val.innerDiagnosticInfo

    @property
    def has_symbolic_id(self):
        return self._has_symbolic_id

    @property
    def has_namespace_uri(self):
        return self._has_namespace_uri

    @property
    def has_localized_text(self):
        return self._has_localized_text

    @property
    def has_locale(self):
        return self._has_locale

    @property
    def has_additional_info(self):
        return self._has_additional_info

    @property
    def has_inner_status_code(self):
        return self._has_inner_status_code

    @property
    def has_inner_diagnostic_info(self):
        return self._has_inner_diagnostic_info

    @property
    def symbolic_id(self):
        return self._symbolic_id

    @property
    def namespace_uri(self):
        return self._namespace_uri

    @property
    def localized_text(self):
        return self._localized_text

    @property
    def locale(self):
        return self._locale

    @property
    def additional_info(self):
        return self._additional_info

    @property
    def inner_status_code(self):
        return self._inner_status_code

    @property
    def inner_diagnostic_info(self):
        return self._inner_diagnostic_info

    @has_symbolic_id.setter
    def has_symbolic_id(self, val):
        self._has_symbolic_id = val
        self._value.hasSymbolicId = val._value

    @has_namespace_uri.setter
    def has_namespace_uri(self, val):
        self._has_namespace_uri = val
        self._value.hasNamespaceUri = val._value

    @has_localized_text.setter
    def has_localized_text(self, val):
        self._has_localized_text = val
        self._value.hasLocalizedText = val._value

    @has_locale.setter
    def has_locale(self, val):
        self._has_locale = val
        self._value.hasLocale = val._value

    @has_additional_info.setter
    def has_additional_info(self, val):
        self._has_additional_info = val
        self._value.hasAdditionalInfo = val._value

    @has_inner_status_code.setter
    def has_inner_status_code(self, val):
        self._has_inner_status_code = val
        self._value.hasInnerStatusCode = val._value

    @has_inner_diagnostic_info.setter
    def has_inner_diagnostic_info(self, val):
        self._has_inner_diagnostic_info = val
        self._value.hasInnerDiagnosticInfo = val._value

    @symbolic_id.setter
    def symbolic_id(self, val):
        self._symbolic_id = val
        self._value.symbolicId = val._value

    @namespace_uri.setter
    def namespace_uri(self, val):
        self._namespace_uri = val
        self._value.namespaceUri = val._value

    @localized_text.setter
    def localized_text(self, val):
        self._localized_text = val
        self._value.localizedText = val._value

    @locale.setter
    def locale(self, val):
        self._locale = val
        self._value.locale = val._value

    @additional_info.setter
    def additional_info(self, val):
        self._additional_info = val
        self._value.additionalInfo = val._value

    @inner_status_code.setter
    def inner_status_code(self, val):
        self._inner_status_code = val
        self._value.innerStatusCode = val._value

    @inner_diagnostic_info.setter
    def inner_diagnostic_info(self, val):
        self._inner_diagnostic_info = val
        self._value.innerDiagnosticInfo = val.__value

    def __str__(self, n=0):
        return ("(UaDiagnosticInfo) :\n" +
                "\t" * (n + 1) + "has_symbolic_id" + self._has_symbolic_id.__str__(n + 1) +
                "\t" * (n + 1) + "has_namespace_uri" + self._has_namespace_uri.__str__(n + 1) +
                "\t" * (n + 1) + "has_localized_text" + self._has_localized_text.__str__(n + 1) +
                "\t" * (n + 1) + "has_locale" + self._has_locale.__str__(n + 1) +
                "\t" * (n + 1) + "has_additional_info" + self._has_additional_info.__str__(n + 1) +
                "\t" * (n + 1) + "has_inner_status_code" + self._has_inner_status_code.__str__(n + 1) +
                "\t" * (n + 1) + "has_inner_diagnostic_info" + self._has_inner_diagnostic_info.__str__(n + 1) +
                "\t" * (n + 1) + "symbolic_id" + self._symbolic_id.__str__(n + 1) +
                "\t" * (n + 1) + "namespace_uri" + self._namespace_uri.__str__(n + 1) +
                "\t" * (n + 1) + "localized_text" + self._localized_text.__str__(n + 1) +
                "\t" * (n + 1) + "locale" + self._locale.__str__(n + 1) +
                "\t" * (n + 1) + "additional_info" + self._additional_info.__str__(n + 1) +
                "\t" * (n + 1) + "inner_status_code" + self._inner_status_code.__str__(n + 1) +
                "\t" * (n + 1) + "inner_diagnostic_info" + self._inner_diagnostic_info.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDataTypeMember +++++++++++++++++++++++
class UaDataTypeMember(UaType):
    def __init__(self, val=ffi.new("UA_DataTypeMember*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._member_type_index = UaUInt16(val=val.memberTypeIndex, is_pointer=False)
        self._padding = UaByte(val=val.padding, is_pointer=False)
        self._namespace_zero = UaBoolean(val=val.namespaceZero, is_pointer=False)
        self._is_array = UaBoolean(val=val.isArray, is_pointer=False)
        self._is_optional = UaBoolean(val=val.isOptional, is_pointer=False)
        self._member_name = CString(val=val.memberName, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._member_type_index.__value[0] = _val(val.memberTypeIndex)
        self._padding.__value[0] = _val(val.padding)
        self._namespace_zero.__value[0] = _val(val.namespaceZero)
        self._is_array.__value[0] = _val(val.isArray)
        self._is_optional.__value[0] = _val(val.isOptional)
        self._member_name.__value = val.memberName

    @property
    def member_type_index(self):
        return self._member_type_index

    @property
    def padding(self):
        return self._padding

    @property
    def namespace_zero(self):
        return self._namespace_zero

    @property
    def is_array(self):
        return self._is_array

    @property
    def is_optional(self):
        return self._is_optional

    @property
    def member_name(self):
        return self._member_name

    @member_type_index.setter
    def member_type_index(self, val):
        self._member_type_index = val
        self._value.memberTypeIndex = val._value

    @padding.setter
    def padding(self, val):
        self._padding = val
        self._value.padding = val._value

    @namespace_zero.setter
    def namespace_zero(self, val):
        self._namespace_zero = val
        self._value.namespaceZero = val._value

    @is_array.setter
    def is_array(self, val):
        self._is_array = val
        self._value.isArray = val._value

    @is_optional.setter
    def is_optional(self, val):
        self._is_optional = val
        self._value.isOptional = val._value

    @member_name.setter
    def member_name(self, val):
        self._member_name = val
        self._value.memberName = val.__value

    def __str__(self, n=0):
        return ("(UaDataTypeMember) :\n" +
                "\t" * (n + 1) + "member_type_index" + self._member_type_index.__str__(n + 1) +
                "\t" * (n + 1) + "padding" + self._padding.__str__(n + 1) +
                "\t" * (n + 1) + "namespace_zero" + self._namespace_zero.__str__(n + 1) +
                "\t" * (n + 1) + "is_array" + self._is_array.__str__(n + 1) +
                "\t" * (n + 1) + "is_optional" + self._is_optional.__str__(n + 1) +
                "\t" * (n + 1) + "member_name" + self._member_name.__str__(n + 1) + "\n")


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
        self._members.__value = val.members
        self._type_name.__value = val.typeName

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
        self._value.members = val.__value

    @type_name.setter
    def type_name(self, val):
        self._type_name = val
        self._value.typeName = val.__value

    def __str__(self, n=0):
        return ("(UaDataType) :\n" +
                "\t" * (n + 1) + "type_id" + self._type_id.__str__(n + 1) +
                "\t" * (n + 1) + "binary_encoding_id" + self._binary_encoding_id.__str__(n + 1) +
                "\t" * (n + 1) + "mem_size" + self._mem_size.__str__(n + 1) +
                "\t" * (n + 1) + "type_index" + self._type_index.__str__(n + 1) +
                "\t" * (n + 1) + "type_kind" + self._type_kind.__str__(n + 1) +
                "\t" * (n + 1) + "pointer_free" + self._pointer_free.__str__(n + 1) +
                "\t" * (n + 1) + "overlayable" + self._overlayable.__str__(n + 1) +
                "\t" * (n + 1) + "members_size" + self._members_size.__str__(n + 1) +
                "\t" * (n + 1) + "members" + self._members.__str__(n + 1) +
                "\t" * (n + 1) + "type_name" + self._type_name.__str__(n + 1) + "\n")

    def is_numeric(self):
        return lib.UA_DataType_isNumeric(self.__value)

    @staticmethod
    def find_by_node_id(type_id: UaNodeId):
        return UaDataType(val=lib.UA_findDataType(type_id.__value), is_pointer=True)

    # TODO: generic type handling!!!
    # ----> init, copy, new, array_new, array_copy should be methods of a class, which represent members of an in an
    # attribute provided UaDataType
    # returns void ptr
    def new_instance(self):
        return lib.UA_new(self.__value)


# +++++++++++++++++++ UaDataTypeArray +++++++++++++++++++++++
class UaDataTypeArray(UaType):
    def __init__(self, val=ffi.new("UA_DataTypeArray*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._next = UaDataTypeArray(val=val.next, is_pointer=True)
        self._types_size = SizeT(val=val.typesSize, is_pointer=False)
        self._types = UaDataType(val=val.types, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._next.__value = val.next
        self._types_size.__value[0] = _val(val.typesSize)
        self._types.__value = val.types

    @property
    def next(self):
        return self._next

    @property
    def types_size(self):
        return self._types_size

    @property
    def types(self):
        return self._types

    @next.setter
    def next(self, val):
        self._next = val
        self._value.next = val.__value

    @types_size.setter
    def types_size(self, val):
        self._types_size = val
        self._value.typesSize = val._value

    @types.setter
    def types(self, val):
        self._types = val
        self._value.types = val.__value

    def __str__(self, n=0):
        return ("(UaDataTypeArray) :\n" +
                "\t" * (n + 1) + "next" + self._next.__str__(n + 1) +
                "\t" * (n + 1) + "types_size" + self._types_size.__str__(n + 1) +
                "\t" * (n + 1) + "types" + self._types.__str__(n + 1) + "\n")


class Randomize:
    @staticmethod
    def random_uint_32():
        return lib.UA_UInt32_random()

    @staticmethod
    def ua_random_seed(seed: int):
        lib.UA_random_seed(ffi.cast("UA_UInt64*", seed))


# -------------------------------------------------------------
# --------------------------- Enums ---------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaMessageSecurityMode +++++++++++++++++++++++
class UaMessageSecurityMode(UaType):
    UA_MESSAGESECURITYMODE_INVALID = 0
    UA_MESSAGESECURITYMODE_NONE = 1
    UA_MESSAGESECURITYMODE_SIGN = 2
    UA_MESSAGESECURITYMODE_SIGNANDENCRYPT = 3
    __UA_MESSAGESECURITYMODE_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_MESSAGESECURITYMODE_INVALID"),
        (1, "UA_MESSAGESECURITYMODE_NONE"),
        (2, "UA_MESSAGESECURITYMODE_SIGN"),
        (3, "UA_MESSAGESECURITYMODE_SIGNANDENCRYPT"),
        (2147483647, "__UA_MESSAGESECURITYMODE_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_MessageSecurityMode*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_MessageSecurityMode", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaMessageSecurityMode): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaStructureType +++++++++++++++++++++++
class UaStructureType(UaType):
    UA_STRUCTURETYPE_STRUCTURE = 0
    UA_STRUCTURETYPE_STRUCTUREWITHOPTIONALFIELDS = 1
    UA_STRUCTURETYPE_UNION = 2
    __UA_STRUCTURETYPE_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_STRUCTURETYPE_STRUCTURE"),
        (1, "UA_STRUCTURETYPE_STRUCTUREWITHOPTIONALFIELDS"),
        (2, "UA_STRUCTURETYPE_UNION"),
        (2147483647, "__UA_STRUCTURETYPE_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_StructureType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_StructureType", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaStructureType): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaMonitoringMode +++++++++++++++++++++++
class UaMonitoringMode(UaType):
    UA_MONITORINGMODE_DISABLED = 0
    UA_MONITORINGMODE_SAMPLING = 1
    UA_MONITORINGMODE_REPORTING = 2
    __UA_MONITORINGMODE_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_MONITORINGMODE_DISABLED"),
        (1, "UA_MONITORINGMODE_SAMPLING"),
        (2, "UA_MONITORINGMODE_REPORTING"),
        (2147483647, "__UA_MONITORINGMODE_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_MonitoringMode*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_MonitoringMode", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaMonitoringMode): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaBrowseResultMask +++++++++++++++++++++++
class UaBrowseResultMask(UaType):
    UA_BROWSERESULTMASK_NONE = 0
    UA_BROWSERESULTMASK_REFERENCETYPEID = 1
    UA_BROWSERESULTMASK_ISFORWARD = 2
    UA_BROWSERESULTMASK_NODECLASS = 4
    UA_BROWSERESULTMASK_BROWSENAME = 8
    UA_BROWSERESULTMASK_DISPLAYNAME = 16
    UA_BROWSERESULTMASK_TYPEDEFINITION = 32
    UA_BROWSERESULTMASK_ALL = 63
    UA_BROWSERESULTMASK_REFERENCETYPEINFO = 3
    UA_BROWSERESULTMASK_TARGETINFO = 60
    __UA_BROWSERESULTMASK_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_BROWSERESULTMASK_NONE"),
        (1, "UA_BROWSERESULTMASK_REFERENCETYPEID"),
        (2, "UA_BROWSERESULTMASK_ISFORWARD"),
        (4, "UA_BROWSERESULTMASK_NODECLASS"),
        (8, "UA_BROWSERESULTMASK_BROWSENAME"),
        (16, "UA_BROWSERESULTMASK_DISPLAYNAME"),
        (32, "UA_BROWSERESULTMASK_TYPEDEFINITION"),
        (63, "UA_BROWSERESULTMASK_ALL"),
        (3, "UA_BROWSERESULTMASK_REFERENCETYPEINFO"),
        (60, "UA_BROWSERESULTMASK_TARGETINFO"),
        (2147483647, "__UA_BROWSERESULTMASK_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_BrowseResultMask*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_BrowseResultMask", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaBrowseResultMask): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaAxisScaleEnumeration +++++++++++++++++++++++
class UaAxisScaleEnumeration(UaType):
    UA_AXISSCALEENUMERATION_LINEAR = 0
    UA_AXISSCALEENUMERATION_LOG = 1
    UA_AXISSCALEENUMERATION_LN = 2
    __UA_AXISSCALEENUMERATION_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_AXISSCALEENUMERATION_LINEAR"),
        (1, "UA_AXISSCALEENUMERATION_LOG"),
        (2, "UA_AXISSCALEENUMERATION_LN"),
        (2147483647, "__UA_AXISSCALEENUMERATION_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_AxisScaleEnumeration*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_AxisScaleEnumeration", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaAxisScaleEnumeration): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaBrowseDirection +++++++++++++++++++++++
class UaBrowseDirection(UaType):
    UA_BROWSEDIRECTION_FORWARD = 0
    UA_BROWSEDIRECTION_INVERSE = 1
    UA_BROWSEDIRECTION_BOTH = 2
    UA_BROWSEDIRECTION_INVALID = 3
    __UA_BROWSEDIRECTION_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_BROWSEDIRECTION_FORWARD"),
        (1, "UA_BROWSEDIRECTION_INVERSE"),
        (2, "UA_BROWSEDIRECTION_BOTH"),
        (3, "UA_BROWSEDIRECTION_INVALID"),
        (2147483647, "__UA_BROWSEDIRECTION_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_BrowseDirection*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_BrowseDirection", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaBrowseDirection): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaTimestampsToReturn +++++++++++++++++++++++
class UaTimestampsToReturn(UaType):
    UA_TIMESTAMPSTORETURN_SOURCE = 0
    UA_TIMESTAMPSTORETURN_SERVER = 1
    UA_TIMESTAMPSTORETURN_BOTH = 2
    UA_TIMESTAMPSTORETURN_NEITHER = 3
    UA_TIMESTAMPSTORETURN_INVALID = 4
    __UA_TIMESTAMPSTORETURN_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_TIMESTAMPSTORETURN_SOURCE"),
        (1, "UA_TIMESTAMPSTORETURN_SERVER"),
        (2, "UA_TIMESTAMPSTORETURN_BOTH"),
        (3, "UA_TIMESTAMPSTORETURN_NEITHER"),
        (4, "UA_TIMESTAMPSTORETURN_INVALID"),
        (2147483647, "__UA_TIMESTAMPSTORETURN_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_TimestampsToReturn*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_TimestampsToReturn", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaTimestampsToReturn): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaNodeClass +++++++++++++++++++++++
class UaNodeClass(UaType):
    UA_NODECLASS_UNSPECIFIED = 0
    UA_NODECLASS_OBJECT = 1
    UA_NODECLASS_VARIABLE = 2
    UA_NODECLASS_METHOD = 4
    UA_NODECLASS_OBJECTTYPE = 8
    UA_NODECLASS_VARIABLETYPE = 16
    UA_NODECLASS_REFERENCETYPE = 32
    UA_NODECLASS_DATATYPE = 64
    UA_NODECLASS_VIEW = 128
    __UA_NODECLASS_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_NODECLASS_UNSPECIFIED"),
        (1, "UA_NODECLASS_OBJECT"),
        (2, "UA_NODECLASS_VARIABLE"),
        (4, "UA_NODECLASS_METHOD"),
        (8, "UA_NODECLASS_OBJECTTYPE"),
        (16, "UA_NODECLASS_VARIABLETYPE"),
        (32, "UA_NODECLASS_REFERENCETYPE"),
        (64, "UA_NODECLASS_DATATYPE"),
        (128, "UA_NODECLASS_VIEW"),
        (2147483647, "__UA_NODECLASS_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_NodeClass*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_NodeClass", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaNodeClass): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaSecurityTokenRequestType +++++++++++++++++++++++
class UaSecurityTokenRequestType(UaType):
    UA_SECURITYTOKENREQUESTTYPE_ISSUE = 0
    UA_SECURITYTOKENREQUESTTYPE_RENEW = 1
    __UA_SECURITYTOKENREQUESTTYPE_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_SECURITYTOKENREQUESTTYPE_ISSUE"),
        (1, "UA_SECURITYTOKENREQUESTTYPE_RENEW"),
        (2147483647, "__UA_SECURITYTOKENREQUESTTYPE_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_SecurityTokenRequestType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_SecurityTokenRequestType", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaSecurityTokenRequestType): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaApplicationType +++++++++++++++++++++++
class UaApplicationType(UaType):
    UA_APPLICATIONTYPE_SERVER = 0
    UA_APPLICATIONTYPE_CLIENT = 1
    UA_APPLICATIONTYPE_CLIENTANDSERVER = 2
    UA_APPLICATIONTYPE_DISCOVERYSERVER = 3
    __UA_APPLICATIONTYPE_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_APPLICATIONTYPE_SERVER"),
        (1, "UA_APPLICATIONTYPE_CLIENT"),
        (2, "UA_APPLICATIONTYPE_CLIENTANDSERVER"),
        (3, "UA_APPLICATIONTYPE_DISCOVERYSERVER"),
        (2147483647, "__UA_APPLICATIONTYPE_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_ApplicationType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_ApplicationType", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaApplicationType): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaDeadbandType +++++++++++++++++++++++
class UaDeadbandType(UaType):
    UA_DEADBANDTYPE_NONE = 0
    UA_DEADBANDTYPE_ABSOLUTE = 1
    UA_DEADBANDTYPE_PERCENT = 2
    __UA_DEADBANDTYPE_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_DEADBANDTYPE_NONE"),
        (1, "UA_DEADBANDTYPE_ABSOLUTE"),
        (2, "UA_DEADBANDTYPE_PERCENT"),
        (2147483647, "__UA_DEADBANDTYPE_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_DeadbandType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_DeadbandType", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaDeadbandType): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaDataChangeTrigger +++++++++++++++++++++++
class UaDataChangeTrigger(UaType):
    UA_DATACHANGETRIGGER_STATUS = 0
    UA_DATACHANGETRIGGER_STATUSVALUE = 1
    UA_DATACHANGETRIGGER_STATUSVALUETIMESTAMP = 2
    __UA_DATACHANGETRIGGER_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_DATACHANGETRIGGER_STATUS"),
        (1, "UA_DATACHANGETRIGGER_STATUSVALUE"),
        (2, "UA_DATACHANGETRIGGER_STATUSVALUETIMESTAMP"),
        (2147483647, "__UA_DATACHANGETRIGGER_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_DataChangeTrigger*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_DataChangeTrigger", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaDataChangeTrigger): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaUserTokenType +++++++++++++++++++++++
class UaUserTokenType(UaType):
    UA_USERTOKENTYPE_ANONYMOUS = 0
    UA_USERTOKENTYPE_USERNAME = 1
    UA_USERTOKENTYPE_CERTIFICATE = 2
    UA_USERTOKENTYPE_ISSUEDTOKEN = 3
    __UA_USERTOKENTYPE_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_USERTOKENTYPE_ANONYMOUS"),
        (1, "UA_USERTOKENTYPE_USERNAME"),
        (2, "UA_USERTOKENTYPE_CERTIFICATE"),
        (3, "UA_USERTOKENTYPE_ISSUEDTOKEN"),
        (2147483647, "__UA_USERTOKENTYPE_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UserTokenType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_UserTokenType", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaUserTokenType): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaNodeAttributesMask +++++++++++++++++++++++
class UaNodeAttributesMask(UaType):
    UA_NODEATTRIBUTESMASK_NONE = 0
    UA_NODEATTRIBUTESMASK_ACCESSLEVEL = 1
    UA_NODEATTRIBUTESMASK_ARRAYDIMENSIONS = 2
    UA_NODEATTRIBUTESMASK_BROWSENAME = 4
    UA_NODEATTRIBUTESMASK_CONTAINSNOLOOPS = 8
    UA_NODEATTRIBUTESMASK_DATATYPE = 16
    UA_NODEATTRIBUTESMASK_DESCRIPTION = 32
    UA_NODEATTRIBUTESMASK_DISPLAYNAME = 64
    UA_NODEATTRIBUTESMASK_EVENTNOTIFIER = 128
    UA_NODEATTRIBUTESMASK_EXECUTABLE = 256
    UA_NODEATTRIBUTESMASK_HISTORIZING = 512
    UA_NODEATTRIBUTESMASK_INVERSENAME = 1024
    UA_NODEATTRIBUTESMASK_ISABSTRACT = 2048
    UA_NODEATTRIBUTESMASK_MINIMUMSAMPLINGINTERVAL = 4096
    UA_NODEATTRIBUTESMASK_NODECLASS = 8192
    UA_NODEATTRIBUTESMASK_NODEID = 16384
    UA_NODEATTRIBUTESMASK_SYMMETRIC = 32768
    UA_NODEATTRIBUTESMASK_USERACCESSLEVEL = 65536
    UA_NODEATTRIBUTESMASK_USEREXECUTABLE = 131072
    UA_NODEATTRIBUTESMASK_USERWRITEMASK = 262144
    UA_NODEATTRIBUTESMASK_VALUERANK = 524288
    UA_NODEATTRIBUTESMASK_WRITEMASK = 1048576
    UA_NODEATTRIBUTESMASK_VALUE = 2097152
    UA_NODEATTRIBUTESMASK_DATATYPEDEFINITION = 4194304
    UA_NODEATTRIBUTESMASK_ROLEPERMISSIONS = 8388608
    UA_NODEATTRIBUTESMASK_ACCESSRESTRICTIONS = 16777216
    UA_NODEATTRIBUTESMASK_ALL = 33554431
    UA_NODEATTRIBUTESMASK_BASENODE = 26501220
    UA_NODEATTRIBUTESMASK_OBJECT = 26501348
    UA_NODEATTRIBUTESMASK_OBJECTTYPE = 26503268
    UA_NODEATTRIBUTESMASK_VARIABLE = 26571383
    UA_NODEATTRIBUTESMASK_VARIABLETYPE = 28600438
    UA_NODEATTRIBUTESMASK_METHOD = 26632548
    UA_NODEATTRIBUTESMASK_REFERENCETYPE = 26537060
    UA_NODEATTRIBUTESMASK_VIEW = 26501356
    __UA_NODEATTRIBUTESMASK_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_NODEATTRIBUTESMASK_NONE"),
        (1, "UA_NODEATTRIBUTESMASK_ACCESSLEVEL"),
        (2, "UA_NODEATTRIBUTESMASK_ARRAYDIMENSIONS"),
        (4, "UA_NODEATTRIBUTESMASK_BROWSENAME"),
        (8, "UA_NODEATTRIBUTESMASK_CONTAINSNOLOOPS"),
        (16, "UA_NODEATTRIBUTESMASK_DATATYPE"),
        (32, "UA_NODEATTRIBUTESMASK_DESCRIPTION"),
        (64, "UA_NODEATTRIBUTESMASK_DISPLAYNAME"),
        (128, "UA_NODEATTRIBUTESMASK_EVENTNOTIFIER"),
        (256, "UA_NODEATTRIBUTESMASK_EXECUTABLE"),
        (512, "UA_NODEATTRIBUTESMASK_HISTORIZING"),
        (1024, "UA_NODEATTRIBUTESMASK_INVERSENAME"),
        (2048, "UA_NODEATTRIBUTESMASK_ISABSTRACT"),
        (4096, "UA_NODEATTRIBUTESMASK_MINIMUMSAMPLINGINTERVAL"),
        (8192, "UA_NODEATTRIBUTESMASK_NODECLASS"),
        (16384, "UA_NODEATTRIBUTESMASK_NODEID"),
        (32768, "UA_NODEATTRIBUTESMASK_SYMMETRIC"),
        (65536, "UA_NODEATTRIBUTESMASK_USERACCESSLEVEL"),
        (131072, "UA_NODEATTRIBUTESMASK_USEREXECUTABLE"),
        (262144, "UA_NODEATTRIBUTESMASK_USERWRITEMASK"),
        (524288, "UA_NODEATTRIBUTESMASK_VALUERANK"),
        (1048576, "UA_NODEATTRIBUTESMASK_WRITEMASK"),
        (2097152, "UA_NODEATTRIBUTESMASK_VALUE"),
        (4194304, "UA_NODEATTRIBUTESMASK_DATATYPEDEFINITION"),
        (8388608, "UA_NODEATTRIBUTESMASK_ROLEPERMISSIONS"),
        (16777216, "UA_NODEATTRIBUTESMASK_ACCESSRESTRICTIONS"),
        (33554431, "UA_NODEATTRIBUTESMASK_ALL"),
        (26501220, "UA_NODEATTRIBUTESMASK_BASENODE"),
        (26501348, "UA_NODEATTRIBUTESMASK_OBJECT"),
        (26503268, "UA_NODEATTRIBUTESMASK_OBJECTTYPE"),
        (26571383, "UA_NODEATTRIBUTESMASK_VARIABLE"),
        (28600438, "UA_NODEATTRIBUTESMASK_VARIABLETYPE"),
        (26632548, "UA_NODEATTRIBUTESMASK_METHOD"),
        (26537060, "UA_NODEATTRIBUTESMASK_REFERENCETYPE"),
        (26501356, "UA_NODEATTRIBUTESMASK_VIEW"),
        (2147483647, "__UA_NODEATTRIBUTESMASK_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_NodeAttributesMask*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_NodeAttributesMask", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaNodeAttributesMask): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaServerState +++++++++++++++++++++++
class UaServerState(UaType):
    UA_SERVERSTATE_RUNNING = 0
    UA_SERVERSTATE_FAILED = 1
    UA_SERVERSTATE_NOCONFIGURATION = 2
    UA_SERVERSTATE_SUSPENDED = 3
    UA_SERVERSTATE_SHUTDOWN = 4
    UA_SERVERSTATE_TEST = 5
    UA_SERVERSTATE_COMMUNICATIONFAULT = 6
    UA_SERVERSTATE_UNKNOWN = 7
    __UA_SERVERSTATE_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_SERVERSTATE_RUNNING"),
        (1, "UA_SERVERSTATE_FAILED"),
        (2, "UA_SERVERSTATE_NOCONFIGURATION"),
        (3, "UA_SERVERSTATE_SUSPENDED"),
        (4, "UA_SERVERSTATE_SHUTDOWN"),
        (5, "UA_SERVERSTATE_TEST"),
        (6, "UA_SERVERSTATE_COMMUNICATIONFAULT"),
        (7, "UA_SERVERSTATE_UNKNOWN"),
        (2147483647, "__UA_SERVERSTATE_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_ServerState*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_ServerState", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaServerState): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaFilterOperator +++++++++++++++++++++++
class UaFilterOperator(UaType):
    UA_FILTEROPERATOR_EQUALS = 0
    UA_FILTEROPERATOR_ISNULL = 1
    UA_FILTEROPERATOR_GREATERTHAN = 2
    UA_FILTEROPERATOR_LESSTHAN = 3
    UA_FILTEROPERATOR_GREATERTHANOREQUAL = 4
    UA_FILTEROPERATOR_LESSTHANOREQUAL = 5
    UA_FILTEROPERATOR_LIKE = 6
    UA_FILTEROPERATOR_NOT = 7
    UA_FILTEROPERATOR_BETWEEN = 8
    UA_FILTEROPERATOR_INLIST = 9
    UA_FILTEROPERATOR_AND = 10
    UA_FILTEROPERATOR_OR = 11
    UA_FILTEROPERATOR_CAST = 12
    UA_FILTEROPERATOR_INVIEW = 13
    UA_FILTEROPERATOR_OFTYPE = 14
    UA_FILTEROPERATOR_RELATEDTO = 15
    UA_FILTEROPERATOR_BITWISEAND = 16
    UA_FILTEROPERATOR_BITWISEOR = 17
    __UA_FILTEROPERATOR_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_FILTEROPERATOR_EQUALS"),
        (1, "UA_FILTEROPERATOR_ISNULL"),
        (2, "UA_FILTEROPERATOR_GREATERTHAN"),
        (3, "UA_FILTEROPERATOR_LESSTHAN"),
        (4, "UA_FILTEROPERATOR_GREATERTHANOREQUAL"),
        (5, "UA_FILTEROPERATOR_LESSTHANOREQUAL"),
        (6, "UA_FILTEROPERATOR_LIKE"),
        (7, "UA_FILTEROPERATOR_NOT"),
        (8, "UA_FILTEROPERATOR_BETWEEN"),
        (9, "UA_FILTEROPERATOR_INLIST"),
        (10, "UA_FILTEROPERATOR_AND"),
        (11, "UA_FILTEROPERATOR_OR"),
        (12, "UA_FILTEROPERATOR_CAST"),
        (13, "UA_FILTEROPERATOR_INVIEW"),
        (14, "UA_FILTEROPERATOR_OFTYPE"),
        (15, "UA_FILTEROPERATOR_RELATEDTO"),
        (16, "UA_FILTEROPERATOR_BITWISEAND"),
        (17, "UA_FILTEROPERATOR_BITWISEOR"),
        (2147483647, "__UA_FILTEROPERATOR_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_FilterOperator*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_FilterOperator", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaFilterOperator): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++++ UaRedundancySupport +++++++++++++++++++++++
class UaRedundancySupport(UaType):
    UA_REDUNDANCYSUPPORT_NONE = 0
    UA_REDUNDANCYSUPPORT_COLD = 1
    UA_REDUNDANCYSUPPORT_WARM = 2
    UA_REDUNDANCYSUPPORT_HOT = 3
    UA_REDUNDANCYSUPPORT_TRANSPARENT = 4
    UA_REDUNDANCYSUPPORT_HOTANDMIRRORED = 5
    __UA_REDUNDANCYSUPPORT_FORCE32BIT = 2147483647

    val_to_string = dict([
        (0, "UA_REDUNDANCYSUPPORT_NONE"),
        (1, "UA_REDUNDANCYSUPPORT_COLD"),
        (2, "UA_REDUNDANCYSUPPORT_WARM"),
        (3, "UA_REDUNDANCYSUPPORT_HOT"),
        (4, "UA_REDUNDANCYSUPPORT_TRANSPARENT"),
        (5, "UA_REDUNDANCYSUPPORT_HOTANDMIRRORED"),
        (2147483647, "__UA_REDUNDANCYSUPPORT_FORCE32BIT")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_RedundancySupport*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_RedundancySupport", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaRedundancySupport): {self.val_to_string[self._value]} ({str(self._value)})\n"


# -------------------------------------------------------------
# -------------------------- Structs --------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaViewAttributes +++++++++++++++++++++++
class UaViewAttributes(UaType):
    def __init__(self, val=ffi.new("UA_ViewAttributes*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
        self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
        self._contains_no_loops = UaBoolean(val=val.containsNoLoops, is_pointer=False)
        self._event_notifier = UaByte(val=val.eventNotifier, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._specified_attributes.__value[0] = _val(val.specifiedAttributes)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._write_mask.__value[0] = _val(val.writeMask)
        self._user_write_mask.__value[0] = _val(val.userWriteMask)
        self._contains_no_loops.__value[0] = _val(val.containsNoLoops)
        self._event_notifier.__value[0] = _val(val.eventNotifier)

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def write_mask(self):
        return self._write_mask

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @property
    def contains_no_loops(self):
        return self._contains_no_loops

    @property
    def event_notifier(self):
        return self._event_notifier

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val._value

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val._value

    @contains_no_loops.setter
    def contains_no_loops(self, val):
        self._contains_no_loops = val
        self._value.containsNoLoops = val._value

    @event_notifier.setter
    def event_notifier(self, val):
        self._event_notifier = val
        self._value.eventNotifier = val._value

    def __str__(self, n=0):
        return ("(UaViewAttributes) :\n" +
                "\t" * (n + 1) + "specified_attributes" + self._specified_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "user_write_mask" + self._user_write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "contains_no_loops" + self._contains_no_loops.__str__(n + 1) +
                "\t" * (n + 1) + "event_notifier" + self._event_notifier.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaXVType +++++++++++++++++++++++
class UaXVType(UaType):
    def __init__(self, val=ffi.new("UA_XVType*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._x = UaDouble(val=val.x, is_pointer=False)
        self._value = UaFloat(val=val.value, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._x.__value[0] = _val(val.x)
        self._value.__value[0] = _val(val.value)

    @property
    def x(self):
        return self._x

    @property
    def value(self):
        return self._value

    @x.setter
    def x(self, val):
        self._x = val
        self._value.x = val._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val._value

    def __str__(self, n=0):
        return ("(UaXVType) :\n" +
                "\t" * (n + 1) + "x" + self._x.__str__(n + 1) +
                "\t" * (n + 1) + "value" + self._value.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaElementOperand +++++++++++++++++++++++
class UaElementOperand(UaType):
    def __init__(self, val=ffi.new("UA_ElementOperand*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._index = UaUInt32(val=val.index, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._index.__value[0] = _val(val.index)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val
        self._value.index = val._value

    def __str__(self, n=0):
        return ("(UaElementOperand) :\n" +
                "\t" * (n + 1) + "index" + self._index.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaVariableAttributes +++++++++++++++++++++++
class UaVariableAttributes(UaType):
    def __init__(self, val=ffi.new("UA_VariableAttributes*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
        self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
        self._value = UaVariant(val=val.value, is_pointer=False)
        self._data_type = UaNodeId(val=val.dataType, is_pointer=False)
        self._value_rank = UaInt32(val=val.valueRank, is_pointer=False)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
        self._access_level = UaByte(val=val.accessLevel, is_pointer=False)
        self._user_access_level = UaByte(val=val.userAccessLevel, is_pointer=False)
        self._minimum_sampling_interval = UaDouble(val=val.minimumSamplingInterval, is_pointer=False)
        self._historizing = UaBoolean(val=val.historizing, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._specified_attributes.__value[0] = _val(val.specifiedAttributes)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._write_mask.__value[0] = _val(val.writeMask)
        self._user_write_mask.__value[0] = _val(val.userWriteMask)
        self._value.__value[0] = _val(val.value)
        self._data_type.__value[0] = _val(val.dataType)
        self._value_rank.__value[0] = _val(val.valueRank)
        self._array_dimensions_size.__value[0] = _val(val.arrayDimensionsSize)
        self._array_dimensions.__value = val.arrayDimensions
        self._access_level.__value[0] = _val(val.accessLevel)
        self._user_access_level.__value[0] = _val(val.userAccessLevel)
        self._minimum_sampling_interval.__value[0] = _val(val.minimumSamplingInterval)
        self._historizing.__value[0] = _val(val.historizing)

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def write_mask(self):
        return self._write_mask

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @property
    def value(self):
        return self._value

    @property
    def data_type(self):
        return self._data_type

    @property
    def value_rank(self):
        return self._value_rank

    @property
    def array_dimensions_size(self):
        return self._array_dimensions_size

    @property
    def array_dimensions(self):
        return self._array_dimensions

    @property
    def access_level(self):
        return self._access_level

    @property
    def user_access_level(self):
        return self._user_access_level

    @property
    def minimum_sampling_interval(self):
        return self._minimum_sampling_interval

    @property
    def historizing(self):
        return self._historizing

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val._value

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val._value

    @data_type.setter
    def data_type(self, val):
        self._data_type = val
        self._value.dataType = val._value

    @value_rank.setter
    def value_rank(self, val):
        self._value_rank = val
        self._value.valueRank = val._value

    @array_dimensions_size.setter
    def array_dimensions_size(self, val):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._value

    @array_dimensions.setter
    def array_dimensions(self, val):
        self._array_dimensions = val
        self._value.arrayDimensions = val.__value

    @access_level.setter
    def access_level(self, val):
        self._access_level = val
        self._value.accessLevel = val._value

    @user_access_level.setter
    def user_access_level(self, val):
        self._user_access_level = val
        self._value.userAccessLevel = val._value

    @minimum_sampling_interval.setter
    def minimum_sampling_interval(self, val):
        self._minimum_sampling_interval = val
        self._value.minimumSamplingInterval = val._value

    @historizing.setter
    def historizing(self, val):
        self._historizing = val
        self._value.historizing = val._value

    def __str__(self, n=0):
        return ("(UaVariableAttributes) :\n" +
                "\t" * (n + 1) + "specified_attributes" + self._specified_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "user_write_mask" + self._user_write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "value" + self._value.__str__(n + 1) +
                "\t" * (n + 1) + "data_type" + self._data_type.__str__(n + 1) +
                "\t" * (n + 1) + "value_rank" + self._value_rank.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions_size" + self._array_dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions" + self._array_dimensions.__str__(n + 1) +
                "\t" * (n + 1) + "access_level" + self._access_level.__str__(n + 1) +
                "\t" * (n + 1) + "user_access_level" + self._user_access_level.__str__(n + 1) +
                "\t" * (n + 1) + "minimum_sampling_interval" + self._minimum_sampling_interval.__str__(n + 1) +
                "\t" * (n + 1) + "historizing" + self._historizing.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaEnumValueType +++++++++++++++++++++++
class UaEnumValueType(UaType):
    def __init__(self, val=ffi.new("UA_EnumValueType*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._value = UaInt64(val=val.value, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._value.__value[0] = _val(val.value)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)

    @property
    def value(self):
        return self._value

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    def __str__(self, n=0):
        return ("(UaEnumValueType) :\n" +
                "\t" * (n + 1) + "value" + self._value.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaEventFieldList +++++++++++++++++++++++
class UaEventFieldList(UaType):
    def __init__(self, val=ffi.new("UA_EventFieldList*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._client_handle = UaUInt32(val=val.clientHandle, is_pointer=False)
        self._event_fields_size = SizeT(val=val.eventFieldsSize, is_pointer=False)
        self._event_fields = UaVariant(val=val.eventFields, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._client_handle.__value[0] = _val(val.clientHandle)
        self._event_fields_size.__value[0] = _val(val.eventFieldsSize)
        self._event_fields.__value = val.eventFields

    @property
    def client_handle(self):
        return self._client_handle

    @property
    def event_fields_size(self):
        return self._event_fields_size

    @property
    def event_fields(self):
        return self._event_fields

    @client_handle.setter
    def client_handle(self, val):
        self._client_handle = val
        self._value.clientHandle = val._value

    @event_fields_size.setter
    def event_fields_size(self, val):
        self._event_fields_size = val
        self._value.eventFieldsSize = val._value

    @event_fields.setter
    def event_fields(self, val):
        self._event_fields = val
        self._value.eventFields = val.__value

    def __str__(self, n=0):
        return ("(UaEventFieldList) :\n" +
                "\t" * (n + 1) + "client_handle" + self._client_handle.__str__(n + 1) +
                "\t" * (n + 1) + "event_fields_size" + self._event_fields_size.__str__(n + 1) +
                "\t" * (n + 1) + "event_fields" + self._event_fields.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaMonitoredItemCreateResult +++++++++++++++++++++++
class UaMonitoredItemCreateResult(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemCreateResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
        self._monitored_item_id = UaUInt32(val=val.monitoredItemId, is_pointer=False)
        self._revised_sampling_interval = UaDouble(val=val.revisedSamplingInterval, is_pointer=False)
        self._revised_queue_size = UaUInt32(val=val.revisedQueueSize, is_pointer=False)
        self._filter_result = UaExtensionObject(val=val.filterResult, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._status_code.__value[0] = _val(val.statusCode)
        self._monitored_item_id.__value[0] = _val(val.monitoredItemId)
        self._revised_sampling_interval.__value[0] = _val(val.revisedSamplingInterval)
        self._revised_queue_size.__value[0] = _val(val.revisedQueueSize)
        self._filter_result.__value[0] = _val(val.filterResult)

    @property
    def status_code(self):
        return self._status_code

    @property
    def monitored_item_id(self):
        return self._monitored_item_id

    @property
    def revised_sampling_interval(self):
        return self._revised_sampling_interval

    @property
    def revised_queue_size(self):
        return self._revised_queue_size

    @property
    def filter_result(self):
        return self._filter_result

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val._value

    @monitored_item_id.setter
    def monitored_item_id(self, val):
        self._monitored_item_id = val
        self._value.monitoredItemId = val._value

    @revised_sampling_interval.setter
    def revised_sampling_interval(self, val):
        self._revised_sampling_interval = val
        self._value.revisedSamplingInterval = val._value

    @revised_queue_size.setter
    def revised_queue_size(self, val):
        self._revised_queue_size = val
        self._value.revisedQueueSize = val._value

    @filter_result.setter
    def filter_result(self, val):
        self._filter_result = val
        self._value.filterResult = val._value

    def __str__(self, n=0):
        return ("(UaMonitoredItemCreateResult) :\n" +
                "\t" * (n + 1) + "status_code" + self._status_code.__str__(n + 1) +
                "\t" * (n + 1) + "monitored_item_id" + self._monitored_item_id.__str__(n + 1) +
                "\t" * (n + 1) + "revised_sampling_interval" + self._revised_sampling_interval.__str__(n + 1) +
                "\t" * (n + 1) + "revised_queue_size" + self._revised_queue_size.__str__(n + 1) +
                "\t" * (n + 1) + "filter_result" + self._filter_result.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaEUInformation +++++++++++++++++++++++
class UaEUInformation(UaType):
    def __init__(self, val=ffi.new("UA_EUInformation*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._namespace_uri = UaString(val=val.namespaceUri, is_pointer=False)
        self._unit_id = UaInt32(val=val.unitId, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._namespace_uri.__value[0] = _val(val.namespaceUri)
        self._unit_id.__value[0] = _val(val.unitId)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)

    @property
    def namespace_uri(self):
        return self._namespace_uri

    @property
    def unit_id(self):
        return self._unit_id

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @namespace_uri.setter
    def namespace_uri(self, val):
        self._namespace_uri = val
        self._value.namespaceUri = val._value

    @unit_id.setter
    def unit_id(self, val):
        self._unit_id = val
        self._value.unitId = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    def __str__(self, n=0):
        return ("(UaEUInformation) :\n" +
                "\t" * (n + 1) + "namespace_uri" + self._namespace_uri.__str__(n + 1) +
                "\t" * (n + 1) + "unit_id" + self._unit_id.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaServerDiagnosticsSummaryDataType +++++++++++++++++++++++
class UaServerDiagnosticsSummaryDataType(UaType):
    def __init__(self, val=ffi.new("UA_ServerDiagnosticsSummaryDataType*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._server_view_count = UaUInt32(val=val.serverViewCount, is_pointer=False)
        self._current_session_count = UaUInt32(val=val.currentSessionCount, is_pointer=False)
        self._cumulated_session_count = UaUInt32(val=val.cumulatedSessionCount, is_pointer=False)
        self._security_rejected_session_count = UaUInt32(val=val.securityRejectedSessionCount, is_pointer=False)
        self._rejected_session_count = UaUInt32(val=val.rejectedSessionCount, is_pointer=False)
        self._session_timeout_count = UaUInt32(val=val.sessionTimeoutCount, is_pointer=False)
        self._session_abort_count = UaUInt32(val=val.sessionAbortCount, is_pointer=False)
        self._current_subscription_count = UaUInt32(val=val.currentSubscriptionCount, is_pointer=False)
        self._cumulated_subscription_count = UaUInt32(val=val.cumulatedSubscriptionCount, is_pointer=False)
        self._publishing_interval_count = UaUInt32(val=val.publishingIntervalCount, is_pointer=False)
        self._security_rejected_requests_count = UaUInt32(val=val.securityRejectedRequestsCount, is_pointer=False)
        self._rejected_requests_count = UaUInt32(val=val.rejectedRequestsCount, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._server_view_count.__value[0] = _val(val.serverViewCount)
        self._current_session_count.__value[0] = _val(val.currentSessionCount)
        self._cumulated_session_count.__value[0] = _val(val.cumulatedSessionCount)
        self._security_rejected_session_count.__value[0] = _val(val.securityRejectedSessionCount)
        self._rejected_session_count.__value[0] = _val(val.rejectedSessionCount)
        self._session_timeout_count.__value[0] = _val(val.sessionTimeoutCount)
        self._session_abort_count.__value[0] = _val(val.sessionAbortCount)
        self._current_subscription_count.__value[0] = _val(val.currentSubscriptionCount)
        self._cumulated_subscription_count.__value[0] = _val(val.cumulatedSubscriptionCount)
        self._publishing_interval_count.__value[0] = _val(val.publishingIntervalCount)
        self._security_rejected_requests_count.__value[0] = _val(val.securityRejectedRequestsCount)
        self._rejected_requests_count.__value[0] = _val(val.rejectedRequestsCount)

    @property
    def server_view_count(self):
        return self._server_view_count

    @property
    def current_session_count(self):
        return self._current_session_count

    @property
    def cumulated_session_count(self):
        return self._cumulated_session_count

    @property
    def security_rejected_session_count(self):
        return self._security_rejected_session_count

    @property
    def rejected_session_count(self):
        return self._rejected_session_count

    @property
    def session_timeout_count(self):
        return self._session_timeout_count

    @property
    def session_abort_count(self):
        return self._session_abort_count

    @property
    def current_subscription_count(self):
        return self._current_subscription_count

    @property
    def cumulated_subscription_count(self):
        return self._cumulated_subscription_count

    @property
    def publishing_interval_count(self):
        return self._publishing_interval_count

    @property
    def security_rejected_requests_count(self):
        return self._security_rejected_requests_count

    @property
    def rejected_requests_count(self):
        return self._rejected_requests_count

    @server_view_count.setter
    def server_view_count(self, val):
        self._server_view_count = val
        self._value.serverViewCount = val._value

    @current_session_count.setter
    def current_session_count(self, val):
        self._current_session_count = val
        self._value.currentSessionCount = val._value

    @cumulated_session_count.setter
    def cumulated_session_count(self, val):
        self._cumulated_session_count = val
        self._value.cumulatedSessionCount = val._value

    @security_rejected_session_count.setter
    def security_rejected_session_count(self, val):
        self._security_rejected_session_count = val
        self._value.securityRejectedSessionCount = val._value

    @rejected_session_count.setter
    def rejected_session_count(self, val):
        self._rejected_session_count = val
        self._value.rejectedSessionCount = val._value

    @session_timeout_count.setter
    def session_timeout_count(self, val):
        self._session_timeout_count = val
        self._value.sessionTimeoutCount = val._value

    @session_abort_count.setter
    def session_abort_count(self, val):
        self._session_abort_count = val
        self._value.sessionAbortCount = val._value

    @current_subscription_count.setter
    def current_subscription_count(self, val):
        self._current_subscription_count = val
        self._value.currentSubscriptionCount = val._value

    @cumulated_subscription_count.setter
    def cumulated_subscription_count(self, val):
        self._cumulated_subscription_count = val
        self._value.cumulatedSubscriptionCount = val._value

    @publishing_interval_count.setter
    def publishing_interval_count(self, val):
        self._publishing_interval_count = val
        self._value.publishingIntervalCount = val._value

    @security_rejected_requests_count.setter
    def security_rejected_requests_count(self, val):
        self._security_rejected_requests_count = val
        self._value.securityRejectedRequestsCount = val._value

    @rejected_requests_count.setter
    def rejected_requests_count(self, val):
        self._rejected_requests_count = val
        self._value.rejectedRequestsCount = val._value

    def __str__(self, n=0):
        return ("(UaServerDiagnosticsSummaryDataType) :\n" +
                "\t" * (n + 1) + "server_view_count" + self._server_view_count.__str__(n + 1) +
                "\t" * (n + 1) + "current_session_count" + self._current_session_count.__str__(n + 1) +
                "\t" * (n + 1) + "cumulated_session_count" + self._cumulated_session_count.__str__(n + 1) +
                "\t" * (n + 1) + "security_rejected_session_count" + self._security_rejected_session_count.__str__(
                    n + 1) +
                "\t" * (n + 1) + "rejected_session_count" + self._rejected_session_count.__str__(n + 1) +
                "\t" * (n + 1) + "session_timeout_count" + self._session_timeout_count.__str__(n + 1) +
                "\t" * (n + 1) + "session_abort_count" + self._session_abort_count.__str__(n + 1) +
                "\t" * (n + 1) + "current_subscription_count" + self._current_subscription_count.__str__(n + 1) +
                "\t" * (n + 1) + "cumulated_subscription_count" + self._cumulated_subscription_count.__str__(n + 1) +
                "\t" * (n + 1) + "publishing_interval_count" + self._publishing_interval_count.__str__(n + 1) +
                "\t" * (n + 1) + "security_rejected_requests_count" + self._security_rejected_requests_count.__str__(
                    n + 1) +
                "\t" * (n + 1) + "rejected_requests_count" + self._rejected_requests_count.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaContentFilterElementResult +++++++++++++++++++++++
class UaContentFilterElementResult(UaType):
    def __init__(self, val=ffi.new("UA_ContentFilterElementResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
        self._operand_status_codes_size = SizeT(val=val.operandStatusCodesSize, is_pointer=False)
        self._operand_status_codes = UaStatusCode(val=val.operandStatusCodes, is_pointer=True)
        self._operand_diagnostic_infos_size = SizeT(val=val.operandDiagnosticInfosSize, is_pointer=False)
        self._operand_diagnostic_infos = UaDiagnosticInfo(val=val.operandDiagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._status_code.__value[0] = _val(val.statusCode)
        self._operand_status_codes_size.__value[0] = _val(val.operandStatusCodesSize)
        self._operand_status_codes.__value = val.operandStatusCodes
        self._operand_diagnostic_infos_size.__value[0] = _val(val.operandDiagnosticInfosSize)
        self._operand_diagnostic_infos.__value = val.operandDiagnosticInfos

    @property
    def status_code(self):
        return self._status_code

    @property
    def operand_status_codes_size(self):
        return self._operand_status_codes_size

    @property
    def operand_status_codes(self):
        return self._operand_status_codes

    @property
    def operand_diagnostic_infos_size(self):
        return self._operand_diagnostic_infos_size

    @property
    def operand_diagnostic_infos(self):
        return self._operand_diagnostic_infos

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val._value

    @operand_status_codes_size.setter
    def operand_status_codes_size(self, val):
        self._operand_status_codes_size = val
        self._value.operandStatusCodesSize = val._value

    @operand_status_codes.setter
    def operand_status_codes(self, val):
        self._operand_status_codes = val
        self._value.operandStatusCodes = val.__value

    @operand_diagnostic_infos_size.setter
    def operand_diagnostic_infos_size(self, val):
        self._operand_diagnostic_infos_size = val
        self._value.operandDiagnosticInfosSize = val._value

    @operand_diagnostic_infos.setter
    def operand_diagnostic_infos(self, val):
        self._operand_diagnostic_infos = val
        self._value.operandDiagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaContentFilterElementResult) :\n" +
                "\t" * (n + 1) + "status_code" + self._status_code.__str__(n + 1) +
                "\t" * (n + 1) + "operand_status_codes_size" + self._operand_status_codes_size.__str__(n + 1) +
                "\t" * (n + 1) + "operand_status_codes" + self._operand_status_codes.__str__(n + 1) +
                "\t" * (n + 1) + "operand_diagnostic_infos_size" + self._operand_diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "operand_diagnostic_infos" + self._operand_diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaLiteralOperand +++++++++++++++++++++++
class UaLiteralOperand(UaType):
    def __init__(self, val=ffi.new("UA_LiteralOperand*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._value = UaVariant(val=val.value, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._value.__value[0] = _val(val.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val._value

    def __str__(self, n=0):
        return ("(UaLiteralOperand) :\n" +
                "\t" * (n + 1) + "value" + self._value.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaUserIdentityToken +++++++++++++++++++++++
class UaUserIdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_UserIdentityToken*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._policy_id = UaString(val=val.policyId, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._policy_id.__value[0] = _val(val.policyId)

    @property
    def policy_id(self):
        return self._policy_id

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val._value

    def __str__(self, n=0):
        return ("(UaUserIdentityToken) :\n" +
                "\t" * (n + 1) + "policy_id" + self._policy_id.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaX509IdentityToken +++++++++++++++++++++++
class UaX509IdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_X509IdentityToken*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._policy_id = UaString(val=val.policyId, is_pointer=False)
        self._certificate_data = UaByteString(val=val.certificateData, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._policy_id.__value[0] = _val(val.policyId)
        self._certificate_data.__value[0] = _val(val.certificateData)

    @property
    def policy_id(self):
        return self._policy_id

    @property
    def certificate_data(self):
        return self._certificate_data

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val._value

    @certificate_data.setter
    def certificate_data(self, val):
        self._certificate_data = val
        self._value.certificateData = val._value

    def __str__(self, n=0):
        return ("(UaX509IdentityToken) :\n" +
                "\t" * (n + 1) + "policy_id" + self._policy_id.__str__(n + 1) +
                "\t" * (n + 1) + "certificate_data" + self._certificate_data.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaMonitoredItemNotification +++++++++++++++++++++++
class UaMonitoredItemNotification(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemNotification*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._client_handle = UaUInt32(val=val.clientHandle, is_pointer=False)
        self._value = UaDataValue(val=val.value, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._client_handle.__value[0] = _val(val.clientHandle)
        self._value.__value[0] = _val(val.value)

    @property
    def client_handle(self):
        return self._client_handle

    @property
    def value(self):
        return self._value

    @client_handle.setter
    def client_handle(self, val):
        self._client_handle = val
        self._value.clientHandle = val._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val._value

    def __str__(self, n=0):
        return ("(UaMonitoredItemNotification) :\n" +
                "\t" * (n + 1) + "client_handle" + self._client_handle.__str__(n + 1) +
                "\t" * (n + 1) + "value" + self._value.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaResponseHeader +++++++++++++++++++++++
class UaResponseHeader(UaType):
    def __init__(self, val=ffi.new("UA_ResponseHeader*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._timestamp = UaDateTime(val=val.timestamp, is_pointer=False)
        self._request_handle = UaUInt32(val=val.requestHandle, is_pointer=False)
        self._service_result = UaStatusCode(val=val.serviceResult, is_pointer=False)
        self._service_diagnostics = UaDiagnosticInfo(val=val.serviceDiagnostics, is_pointer=False)
        self._string_table_size = SizeT(val=val.stringTableSize, is_pointer=False)
        self._string_table = UaString(val=val.stringTable, is_pointer=True)
        self._additional_header = UaExtensionObject(val=val.additionalHeader, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._timestamp.__value[0] = _val(val.timestamp)
        self._request_handle.__value[0] = _val(val.requestHandle)
        self._service_result.__value[0] = _val(val.serviceResult)
        self._service_diagnostics.__value[0] = _val(val.serviceDiagnostics)
        self._string_table_size.__value[0] = _val(val.stringTableSize)
        self._string_table.__value = val.stringTable
        self._additional_header.__value[0] = _val(val.additionalHeader)

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def request_handle(self):
        return self._request_handle

    @property
    def service_result(self):
        return self._service_result

    @property
    def service_diagnostics(self):
        return self._service_diagnostics

    @property
    def string_table_size(self):
        return self._string_table_size

    @property
    def string_table(self):
        return self._string_table

    @property
    def additional_header(self):
        return self._additional_header

    @timestamp.setter
    def timestamp(self, val):
        self._timestamp = val
        self._value.timestamp = val._value

    @request_handle.setter
    def request_handle(self, val):
        self._request_handle = val
        self._value.requestHandle = val._value

    @service_result.setter
    def service_result(self, val):
        self._service_result = val
        self._value.serviceResult = val._value

    @service_diagnostics.setter
    def service_diagnostics(self, val):
        self._service_diagnostics = val
        self._value.serviceDiagnostics = val._value

    @string_table_size.setter
    def string_table_size(self, val):
        self._string_table_size = val
        self._value.stringTableSize = val._value

    @string_table.setter
    def string_table(self, val):
        self._string_table = val
        self._value.stringTable = val.__value

    @additional_header.setter
    def additional_header(self, val):
        self._additional_header = val
        self._value.additionalHeader = val._value

    def __str__(self, n=0):
        return ("(UaResponseHeader) :\n" +
                "\t" * (n + 1) + "timestamp" + self._timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "request_handle" + self._request_handle.__str__(n + 1) +
                "\t" * (n + 1) + "service_result" + self._service_result.__str__(n + 1) +
                "\t" * (n + 1) + "service_diagnostics" + self._service_diagnostics.__str__(n + 1) +
                "\t" * (n + 1) + "string_table_size" + self._string_table_size.__str__(n + 1) +
                "\t" * (n + 1) + "string_table" + self._string_table.__str__(n + 1) +
                "\t" * (n + 1) + "additional_header" + self._additional_header.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSignatureData +++++++++++++++++++++++
class UaSignatureData(UaType):
    def __init__(self, val=ffi.new("UA_SignatureData*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._algorithm = UaString(val=val.algorithm, is_pointer=False)
        self._signature = UaByteString(val=val.signature, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._algorithm.__value[0] = _val(val.algorithm)
        self._signature.__value[0] = _val(val.signature)

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def signature(self):
        return self._signature

    @algorithm.setter
    def algorithm(self, val):
        self._algorithm = val
        self._value.algorithm = val._value

    @signature.setter
    def signature(self, val):
        self._signature = val
        self._value.signature = val._value

    def __str__(self, n=0):
        return ("(UaSignatureData) :\n" +
                "\t" * (n + 1) + "algorithm" + self._algorithm.__str__(n + 1) +
                "\t" * (n + 1) + "signature" + self._signature.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaModifySubscriptionResponse +++++++++++++++++++++++
class UaModifySubscriptionResponse(UaType):
    def __init__(self, val=ffi.new("UA_ModifySubscriptionResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._revised_publishing_interval = UaDouble(val=val.revisedPublishingInterval, is_pointer=False)
        self._revised_lifetime_count = UaUInt32(val=val.revisedLifetimeCount, is_pointer=False)
        self._revised_max_keep_alive_count = UaUInt32(val=val.revisedMaxKeepAliveCount, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._revised_publishing_interval.__value[0] = _val(val.revisedPublishingInterval)
        self._revised_lifetime_count.__value[0] = _val(val.revisedLifetimeCount)
        self._revised_max_keep_alive_count.__value[0] = _val(val.revisedMaxKeepAliveCount)

    @property
    def response_header(self):
        return self._response_header

    @property
    def revised_publishing_interval(self):
        return self._revised_publishing_interval

    @property
    def revised_lifetime_count(self):
        return self._revised_lifetime_count

    @property
    def revised_max_keep_alive_count(self):
        return self._revised_max_keep_alive_count

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @revised_publishing_interval.setter
    def revised_publishing_interval(self, val):
        self._revised_publishing_interval = val
        self._value.revisedPublishingInterval = val._value

    @revised_lifetime_count.setter
    def revised_lifetime_count(self, val):
        self._revised_lifetime_count = val
        self._value.revisedLifetimeCount = val._value

    @revised_max_keep_alive_count.setter
    def revised_max_keep_alive_count(self, val):
        self._revised_max_keep_alive_count = val
        self._value.revisedMaxKeepAliveCount = val._value

    def __str__(self, n=0):
        return ("(UaModifySubscriptionResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "revised_publishing_interval" + self._revised_publishing_interval.__str__(n + 1) +
                "\t" * (n + 1) + "revised_lifetime_count" + self._revised_lifetime_count.__str__(n + 1) +
                "\t" * (n + 1) + "revised_max_keep_alive_count" + self._revised_max_keep_alive_count.__str__(
                    n + 1) + "\n")


# +++++++++++++++++++ UaNodeAttributes +++++++++++++++++++++++
class UaNodeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_NodeAttributes*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
        self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._specified_attributes.__value[0] = _val(val.specifiedAttributes)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._write_mask.__value[0] = _val(val.writeMask)
        self._user_write_mask.__value[0] = _val(val.userWriteMask)

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def write_mask(self):
        return self._write_mask

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val._value

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val._value

    def __str__(self, n=0):
        return ("(UaNodeAttributes) :\n" +
                "\t" * (n + 1) + "specified_attributes" + self._specified_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "user_write_mask" + self._user_write_mask.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaActivateSessionResponse +++++++++++++++++++++++
class UaActivateSessionResponse(UaType):
    def __init__(self, val=ffi.new("UA_ActivateSessionResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._server_nonce = UaByteString(val=val.serverNonce, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._server_nonce.__value[0] = _val(val.serverNonce)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def server_nonce(self):
        return self._server_nonce

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @server_nonce.setter
    def server_nonce(self, val):
        self._server_nonce = val
        self._value.serverNonce = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaActivateSessionResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "server_nonce" + self._server_nonce.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaEnumField +++++++++++++++++++++++
class UaEnumField(UaType):
    def __init__(self, val=ffi.new("UA_EnumField*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._value = UaInt64(val=val.value, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._name = UaString(val=val.name, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._value.__value[0] = _val(val.value)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._name.__value[0] = _val(val.name)

    @property
    def value(self):
        return self._value

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def name(self):
        return self._name

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @name.setter
    def name(self, val):
        self._name = val
        self._value.name = val._value

    def __str__(self, n=0):
        return ("(UaEnumField) :\n" +
                "\t" * (n + 1) + "value" + self._value.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "name" + self._name.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaVariableTypeAttributes +++++++++++++++++++++++
class UaVariableTypeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_VariableTypeAttributes*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
        self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
        self._value = UaVariant(val=val.value, is_pointer=False)
        self._data_type = UaNodeId(val=val.dataType, is_pointer=False)
        self._value_rank = UaInt32(val=val.valueRank, is_pointer=False)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
        self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._specified_attributes.__value[0] = _val(val.specifiedAttributes)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._write_mask.__value[0] = _val(val.writeMask)
        self._user_write_mask.__value[0] = _val(val.userWriteMask)
        self._value.__value[0] = _val(val.value)
        self._data_type.__value[0] = _val(val.dataType)
        self._value_rank.__value[0] = _val(val.valueRank)
        self._array_dimensions_size.__value[0] = _val(val.arrayDimensionsSize)
        self._array_dimensions.__value = val.arrayDimensions
        self._is_abstract.__value[0] = _val(val.isAbstract)

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def write_mask(self):
        return self._write_mask

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @property
    def value(self):
        return self._value

    @property
    def data_type(self):
        return self._data_type

    @property
    def value_rank(self):
        return self._value_rank

    @property
    def array_dimensions_size(self):
        return self._array_dimensions_size

    @property
    def array_dimensions(self):
        return self._array_dimensions

    @property
    def is_abstract(self):
        return self._is_abstract

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val._value

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val._value

    @data_type.setter
    def data_type(self, val):
        self._data_type = val
        self._value.dataType = val._value

    @value_rank.setter
    def value_rank(self, val):
        self._value_rank = val
        self._value.valueRank = val._value

    @array_dimensions_size.setter
    def array_dimensions_size(self, val):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._value

    @array_dimensions.setter
    def array_dimensions(self, val):
        self._array_dimensions = val
        self._value.arrayDimensions = val.__value

    @is_abstract.setter
    def is_abstract(self, val):
        self._is_abstract = val
        self._value.isAbstract = val._value

    def __str__(self, n=0):
        return ("(UaVariableTypeAttributes) :\n" +
                "\t" * (n + 1) + "specified_attributes" + self._specified_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "user_write_mask" + self._user_write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "value" + self._value.__str__(n + 1) +
                "\t" * (n + 1) + "data_type" + self._data_type.__str__(n + 1) +
                "\t" * (n + 1) + "value_rank" + self._value_rank.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions_size" + self._array_dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions" + self._array_dimensions.__str__(n + 1) +
                "\t" * (n + 1) + "is_abstract" + self._is_abstract.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCallMethodResult +++++++++++++++++++++++
class UaCallMethodResult(UaType):
    def __init__(self, val=ffi.new("UA_CallMethodResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
        self._input_argument_results_size = SizeT(val=val.inputArgumentResultsSize, is_pointer=False)
        self._input_argument_results = UaStatusCode(val=val.inputArgumentResults, is_pointer=True)
        self._input_argument_diagnostic_infos_size = SizeT(val=val.inputArgumentDiagnosticInfosSize, is_pointer=False)
        self._input_argument_diagnostic_infos = UaDiagnosticInfo(val=val.inputArgumentDiagnosticInfos, is_pointer=True)
        self._output_arguments_size = SizeT(val=val.outputArgumentsSize, is_pointer=False)
        self._output_arguments = UaVariant(val=val.outputArguments, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._status_code.__value[0] = _val(val.statusCode)
        self._input_argument_results_size.__value[0] = _val(val.inputArgumentResultsSize)
        self._input_argument_results.__value = val.inputArgumentResults
        self._input_argument_diagnostic_infos_size.__value[0] = _val(val.inputArgumentDiagnosticInfosSize)
        self._input_argument_diagnostic_infos.__value = val.inputArgumentDiagnosticInfos
        self._output_arguments_size.__value[0] = _val(val.outputArgumentsSize)
        self._output_arguments.__value = val.outputArguments

    @property
    def status_code(self):
        return self._status_code

    @property
    def input_argument_results_size(self):
        return self._input_argument_results_size

    @property
    def input_argument_results(self):
        return self._input_argument_results

    @property
    def input_argument_diagnostic_infos_size(self):
        return self._input_argument_diagnostic_infos_size

    @property
    def input_argument_diagnostic_infos(self):
        return self._input_argument_diagnostic_infos

    @property
    def output_arguments_size(self):
        return self._output_arguments_size

    @property
    def output_arguments(self):
        return self._output_arguments

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val._value

    @input_argument_results_size.setter
    def input_argument_results_size(self, val):
        self._input_argument_results_size = val
        self._value.inputArgumentResultsSize = val._value

    @input_argument_results.setter
    def input_argument_results(self, val):
        self._input_argument_results = val
        self._value.inputArgumentResults = val.__value

    @input_argument_diagnostic_infos_size.setter
    def input_argument_diagnostic_infos_size(self, val):
        self._input_argument_diagnostic_infos_size = val
        self._value.inputArgumentDiagnosticInfosSize = val._value

    @input_argument_diagnostic_infos.setter
    def input_argument_diagnostic_infos(self, val):
        self._input_argument_diagnostic_infos = val
        self._value.inputArgumentDiagnosticInfos = val.__value

    @output_arguments_size.setter
    def output_arguments_size(self, val):
        self._output_arguments_size = val
        self._value.outputArgumentsSize = val._value

    @output_arguments.setter
    def output_arguments(self, val):
        self._output_arguments = val
        self._value.outputArguments = val.__value

    def __str__(self, n=0):
        return ("(UaCallMethodResult) :\n" +
                "\t" * (n + 1) + "status_code" + self._status_code.__str__(n + 1) +
                "\t" * (n + 1) + "input_argument_results_size" + self._input_argument_results_size.__str__(n + 1) +
                "\t" * (n + 1) + "input_argument_results" + self._input_argument_results.__str__(n + 1) +
                "\t" * (
                            n + 1) + "input_argument_diagnostic_infos_size" + self._input_argument_diagnostic_infos_size.__str__(
                    n + 1) +
                "\t" * (n + 1) + "input_argument_diagnostic_infos" + self._input_argument_diagnostic_infos.__str__(
                    n + 1) +
                "\t" * (n + 1) + "output_arguments_size" + self._output_arguments_size.__str__(n + 1) +
                "\t" * (n + 1) + "output_arguments" + self._output_arguments.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSetMonitoringModeResponse +++++++++++++++++++++++
class UaSetMonitoringModeResponse(UaType):
    def __init__(self, val=ffi.new("UA_SetMonitoringModeResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaSetMonitoringModeResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaRequestHeader +++++++++++++++++++++++
class UaRequestHeader(UaType):
    def __init__(self, val=ffi.new("UA_RequestHeader*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._authentication_token = UaNodeId(val=val.authenticationToken, is_pointer=False)
        self._timestamp = UaDateTime(val=val.timestamp, is_pointer=False)
        self._request_handle = UaUInt32(val=val.requestHandle, is_pointer=False)
        self._return_diagnostics = UaUInt32(val=val.returnDiagnostics, is_pointer=False)
        self._audit_entry_id = UaString(val=val.auditEntryId, is_pointer=False)
        self._timeout_hint = UaUInt32(val=val.timeoutHint, is_pointer=False)
        self._additional_header = UaExtensionObject(val=val.additionalHeader, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._authentication_token.__value[0] = _val(val.authenticationToken)
        self._timestamp.__value[0] = _val(val.timestamp)
        self._request_handle.__value[0] = _val(val.requestHandle)
        self._return_diagnostics.__value[0] = _val(val.returnDiagnostics)
        self._audit_entry_id.__value[0] = _val(val.auditEntryId)
        self._timeout_hint.__value[0] = _val(val.timeoutHint)
        self._additional_header.__value[0] = _val(val.additionalHeader)

    @property
    def authentication_token(self):
        return self._authentication_token

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def request_handle(self):
        return self._request_handle

    @property
    def return_diagnostics(self):
        return self._return_diagnostics

    @property
    def audit_entry_id(self):
        return self._audit_entry_id

    @property
    def timeout_hint(self):
        return self._timeout_hint

    @property
    def additional_header(self):
        return self._additional_header

    @authentication_token.setter
    def authentication_token(self, val):
        self._authentication_token = val
        self._value.authenticationToken = val._value

    @timestamp.setter
    def timestamp(self, val):
        self._timestamp = val
        self._value.timestamp = val._value

    @request_handle.setter
    def request_handle(self, val):
        self._request_handle = val
        self._value.requestHandle = val._value

    @return_diagnostics.setter
    def return_diagnostics(self, val):
        self._return_diagnostics = val
        self._value.returnDiagnostics = val._value

    @audit_entry_id.setter
    def audit_entry_id(self, val):
        self._audit_entry_id = val
        self._value.auditEntryId = val._value

    @timeout_hint.setter
    def timeout_hint(self, val):
        self._timeout_hint = val
        self._value.timeoutHint = val._value

    @additional_header.setter
    def additional_header(self, val):
        self._additional_header = val
        self._value.additionalHeader = val._value

    def __str__(self, n=0):
        return ("(UaRequestHeader) :\n" +
                "\t" * (n + 1) + "authentication_token" + self._authentication_token.__str__(n + 1) +
                "\t" * (n + 1) + "timestamp" + self._timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "request_handle" + self._request_handle.__str__(n + 1) +
                "\t" * (n + 1) + "return_diagnostics" + self._return_diagnostics.__str__(n + 1) +
                "\t" * (n + 1) + "audit_entry_id" + self._audit_entry_id.__str__(n + 1) +
                "\t" * (n + 1) + "timeout_hint" + self._timeout_hint.__str__(n + 1) +
                "\t" * (n + 1) + "additional_header" + self._additional_header.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaMonitoredItemModifyResult +++++++++++++++++++++++
class UaMonitoredItemModifyResult(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemModifyResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
        self._revised_sampling_interval = UaDouble(val=val.revisedSamplingInterval, is_pointer=False)
        self._revised_queue_size = UaUInt32(val=val.revisedQueueSize, is_pointer=False)
        self._filter_result = UaExtensionObject(val=val.filterResult, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._status_code.__value[0] = _val(val.statusCode)
        self._revised_sampling_interval.__value[0] = _val(val.revisedSamplingInterval)
        self._revised_queue_size.__value[0] = _val(val.revisedQueueSize)
        self._filter_result.__value[0] = _val(val.filterResult)

    @property
    def status_code(self):
        return self._status_code

    @property
    def revised_sampling_interval(self):
        return self._revised_sampling_interval

    @property
    def revised_queue_size(self):
        return self._revised_queue_size

    @property
    def filter_result(self):
        return self._filter_result

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val._value

    @revised_sampling_interval.setter
    def revised_sampling_interval(self, val):
        self._revised_sampling_interval = val
        self._value.revisedSamplingInterval = val._value

    @revised_queue_size.setter
    def revised_queue_size(self, val):
        self._revised_queue_size = val
        self._value.revisedQueueSize = val._value

    @filter_result.setter
    def filter_result(self, val):
        self._filter_result = val
        self._value.filterResult = val._value

    def __str__(self, n=0):
        return ("(UaMonitoredItemModifyResult) :\n" +
                "\t" * (n + 1) + "status_code" + self._status_code.__str__(n + 1) +
                "\t" * (n + 1) + "revised_sampling_interval" + self._revised_sampling_interval.__str__(n + 1) +
                "\t" * (n + 1) + "revised_queue_size" + self._revised_queue_size.__str__(n + 1) +
                "\t" * (n + 1) + "filter_result" + self._filter_result.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCloseSecureChannelRequest +++++++++++++++++++++++
class UaCloseSecureChannelRequest(UaType):
    def __init__(self, val=ffi.new("UA_CloseSecureChannelRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    def __str__(self, n=0):
        return ("(UaCloseSecureChannelRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaNotificationMessage +++++++++++++++++++++++
class UaNotificationMessage(UaType):
    def __init__(self, val=ffi.new("UA_NotificationMessage*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._sequence_number = UaUInt32(val=val.sequenceNumber, is_pointer=False)
        self._publish_time = UaDateTime(val=val.publishTime, is_pointer=False)
        self._notification_data_size = SizeT(val=val.notificationDataSize, is_pointer=False)
        self._notification_data = UaExtensionObject(val=val.notificationData, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._sequence_number.__value[0] = _val(val.sequenceNumber)
        self._publish_time.__value[0] = _val(val.publishTime)
        self._notification_data_size.__value[0] = _val(val.notificationDataSize)
        self._notification_data.__value = val.notificationData

    @property
    def sequence_number(self):
        return self._sequence_number

    @property
    def publish_time(self):
        return self._publish_time

    @property
    def notification_data_size(self):
        return self._notification_data_size

    @property
    def notification_data(self):
        return self._notification_data

    @sequence_number.setter
    def sequence_number(self, val):
        self._sequence_number = val
        self._value.sequenceNumber = val._value

    @publish_time.setter
    def publish_time(self, val):
        self._publish_time = val
        self._value.publishTime = val._value

    @notification_data_size.setter
    def notification_data_size(self, val):
        self._notification_data_size = val
        self._value.notificationDataSize = val._value

    @notification_data.setter
    def notification_data(self, val):
        self._notification_data = val
        self._value.notificationData = val.__value

    def __str__(self, n=0):
        return ("(UaNotificationMessage) :\n" +
                "\t" * (n + 1) + "sequence_number" + self._sequence_number.__str__(n + 1) +
                "\t" * (n + 1) + "publish_time" + self._publish_time.__str__(n + 1) +
                "\t" * (n + 1) + "notification_data_size" + self._notification_data_size.__str__(n + 1) +
                "\t" * (n + 1) + "notification_data" + self._notification_data.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCreateSubscriptionResponse +++++++++++++++++++++++
class UaCreateSubscriptionResponse(UaType):
    def __init__(self, val=ffi.new("UA_CreateSubscriptionResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._revised_publishing_interval = UaDouble(val=val.revisedPublishingInterval, is_pointer=False)
        self._revised_lifetime_count = UaUInt32(val=val.revisedLifetimeCount, is_pointer=False)
        self._revised_max_keep_alive_count = UaUInt32(val=val.revisedMaxKeepAliveCount, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._revised_publishing_interval.__value[0] = _val(val.revisedPublishingInterval)
        self._revised_lifetime_count.__value[0] = _val(val.revisedLifetimeCount)
        self._revised_max_keep_alive_count.__value[0] = _val(val.revisedMaxKeepAliveCount)

    @property
    def response_header(self):
        return self._response_header

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def revised_publishing_interval(self):
        return self._revised_publishing_interval

    @property
    def revised_lifetime_count(self):
        return self._revised_lifetime_count

    @property
    def revised_max_keep_alive_count(self):
        return self._revised_max_keep_alive_count

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @revised_publishing_interval.setter
    def revised_publishing_interval(self, val):
        self._revised_publishing_interval = val
        self._value.revisedPublishingInterval = val._value

    @revised_lifetime_count.setter
    def revised_lifetime_count(self, val):
        self._revised_lifetime_count = val
        self._value.revisedLifetimeCount = val._value

    @revised_max_keep_alive_count.setter
    def revised_max_keep_alive_count(self, val):
        self._revised_max_keep_alive_count = val
        self._value.revisedMaxKeepAliveCount = val._value

    def __str__(self, n=0):
        return ("(UaCreateSubscriptionResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "revised_publishing_interval" + self._revised_publishing_interval.__str__(n + 1) +
                "\t" * (n + 1) + "revised_lifetime_count" + self._revised_lifetime_count.__str__(n + 1) +
                "\t" * (n + 1) + "revised_max_keep_alive_count" + self._revised_max_keep_alive_count.__str__(
                    n + 1) + "\n")


# +++++++++++++++++++ UaEnumDefinition +++++++++++++++++++++++
class UaEnumDefinition(UaType):
    def __init__(self, val=ffi.new("UA_EnumDefinition*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._fields_size = SizeT(val=val.fieldsSize, is_pointer=False)
        self._fields = UaEnumField(val=val.fields, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._fields_size.__value[0] = _val(val.fieldsSize)
        self._fields.__value = val.fields

    @property
    def fields_size(self):
        return self._fields_size

    @property
    def fields(self):
        return self._fields

    @fields_size.setter
    def fields_size(self, val):
        self._fields_size = val
        self._value.fieldsSize = val._value

    @fields.setter
    def fields(self, val):
        self._fields = val
        self._value.fields = val.__value

    def __str__(self, n=0):
        return ("(UaEnumDefinition) :\n" +
                "\t" * (n + 1) + "fields_size" + self._fields_size.__str__(n + 1) +
                "\t" * (n + 1) + "fields" + self._fields.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCallMethodRequest +++++++++++++++++++++++
class UaCallMethodRequest(UaType):
    def __init__(self, val=ffi.new("UA_CallMethodRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._object_id = UaNodeId(val=val.objectId, is_pointer=False)
        self._method_id = UaNodeId(val=val.methodId, is_pointer=False)
        self._input_arguments_size = SizeT(val=val.inputArgumentsSize, is_pointer=False)
        self._input_arguments = UaVariant(val=val.inputArguments, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._object_id.__value[0] = _val(val.objectId)
        self._method_id.__value[0] = _val(val.methodId)
        self._input_arguments_size.__value[0] = _val(val.inputArgumentsSize)
        self._input_arguments.__value = val.inputArguments

    @property
    def object_id(self):
        return self._object_id

    @property
    def method_id(self):
        return self._method_id

    @property
    def input_arguments_size(self):
        return self._input_arguments_size

    @property
    def input_arguments(self):
        return self._input_arguments

    @object_id.setter
    def object_id(self, val):
        self._object_id = val
        self._value.objectId = val._value

    @method_id.setter
    def method_id(self, val):
        self._method_id = val
        self._value.methodId = val._value

    @input_arguments_size.setter
    def input_arguments_size(self, val):
        self._input_arguments_size = val
        self._value.inputArgumentsSize = val._value

    @input_arguments.setter
    def input_arguments(self, val):
        self._input_arguments = val
        self._value.inputArguments = val.__value

    def __str__(self, n=0):
        return ("(UaCallMethodRequest) :\n" +
                "\t" * (n + 1) + "object_id" + self._object_id.__str__(n + 1) +
                "\t" * (n + 1) + "method_id" + self._method_id.__str__(n + 1) +
                "\t" * (n + 1) + "input_arguments_size" + self._input_arguments_size.__str__(n + 1) +
                "\t" * (n + 1) + "input_arguments" + self._input_arguments.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaReadResponse +++++++++++++++++++++++
class UaReadResponse(UaType):
    def __init__(self, val=ffi.new("UA_ReadResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaDataValue(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaReadResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaObjectTypeAttributes +++++++++++++++++++++++
class UaObjectTypeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_ObjectTypeAttributes*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
        self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
        self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._specified_attributes.__value[0] = _val(val.specifiedAttributes)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._write_mask.__value[0] = _val(val.writeMask)
        self._user_write_mask.__value[0] = _val(val.userWriteMask)
        self._is_abstract.__value[0] = _val(val.isAbstract)

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def write_mask(self):
        return self._write_mask

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @property
    def is_abstract(self):
        return self._is_abstract

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val._value

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val._value

    @is_abstract.setter
    def is_abstract(self, val):
        self._is_abstract = val
        self._value.isAbstract = val._value

    def __str__(self, n=0):
        return ("(UaObjectTypeAttributes) :\n" +
                "\t" * (n + 1) + "specified_attributes" + self._specified_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "user_write_mask" + self._user_write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "is_abstract" + self._is_abstract.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCloseSessionResponse +++++++++++++++++++++++
class UaCloseSessionResponse(UaType):
    def __init__(self, val=ffi.new("UA_CloseSessionResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    def __str__(self, n=0):
        return ("(UaCloseSessionResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSetPublishingModeRequest +++++++++++++++++++++++
class UaSetPublishingModeRequest(UaType):
    def __init__(self, val=ffi.new("UA_SetPublishingModeRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._publishing_enabled = UaBoolean(val=val.publishingEnabled, is_pointer=False)
        self._subscription_ids_size = SizeT(val=val.subscriptionIdsSize, is_pointer=False)
        self._subscription_ids = UaUInt32(val=val.subscriptionIds, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._publishing_enabled.__value[0] = _val(val.publishingEnabled)
        self._subscription_ids_size.__value[0] = _val(val.subscriptionIdsSize)
        self._subscription_ids.__value = val.subscriptionIds

    @property
    def request_header(self):
        return self._request_header

    @property
    def publishing_enabled(self):
        return self._publishing_enabled

    @property
    def subscription_ids_size(self):
        return self._subscription_ids_size

    @property
    def subscription_ids(self):
        return self._subscription_ids

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @publishing_enabled.setter
    def publishing_enabled(self, val):
        self._publishing_enabled = val
        self._value.publishingEnabled = val._value

    @subscription_ids_size.setter
    def subscription_ids_size(self, val):
        self._subscription_ids_size = val
        self._value.subscriptionIdsSize = val._value

    @subscription_ids.setter
    def subscription_ids(self, val):
        self._subscription_ids = val
        self._value.subscriptionIds = val.__value

    def __str__(self, n=0):
        return ("(UaSetPublishingModeRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "publishing_enabled" + self._publishing_enabled.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_ids_size" + self._subscription_ids_size.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_ids" + self._subscription_ids.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaIssuedIdentityToken +++++++++++++++++++++++
class UaIssuedIdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_IssuedIdentityToken*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._policy_id = UaString(val=val.policyId, is_pointer=False)
        self._token_data = UaByteString(val=val.tokenData, is_pointer=False)
        self._encryption_algorithm = UaString(val=val.encryptionAlgorithm, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._policy_id.__value[0] = _val(val.policyId)
        self._token_data.__value[0] = _val(val.tokenData)
        self._encryption_algorithm.__value[0] = _val(val.encryptionAlgorithm)

    @property
    def policy_id(self):
        return self._policy_id

    @property
    def token_data(self):
        return self._token_data

    @property
    def encryption_algorithm(self):
        return self._encryption_algorithm

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val._value

    @token_data.setter
    def token_data(self, val):
        self._token_data = val
        self._value.tokenData = val._value

    @encryption_algorithm.setter
    def encryption_algorithm(self, val):
        self._encryption_algorithm = val
        self._value.encryptionAlgorithm = val._value

    def __str__(self, n=0):
        return ("(UaIssuedIdentityToken) :\n" +
                "\t" * (n + 1) + "policy_id" + self._policy_id.__str__(n + 1) +
                "\t" * (n + 1) + "token_data" + self._token_data.__str__(n + 1) +
                "\t" * (n + 1) + "encryption_algorithm" + self._encryption_algorithm.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteMonitoredItemsResponse +++++++++++++++++++++++
class UaDeleteMonitoredItemsResponse(UaType):
    def __init__(self, val=ffi.new("UA_DeleteMonitoredItemsResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaDeleteMonitoredItemsResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBrowseNextRequest +++++++++++++++++++++++
class UaBrowseNextRequest(UaType):
    def __init__(self, val=ffi.new("UA_BrowseNextRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._release_continuation_points = UaBoolean(val=val.releaseContinuationPoints, is_pointer=False)
        self._continuation_points_size = SizeT(val=val.continuationPointsSize, is_pointer=False)
        self._continuation_points = UaByteString(val=val.continuationPoints, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._release_continuation_points.__value[0] = _val(val.releaseContinuationPoints)
        self._continuation_points_size.__value[0] = _val(val.continuationPointsSize)
        self._continuation_points.__value = val.continuationPoints

    @property
    def request_header(self):
        return self._request_header

    @property
    def release_continuation_points(self):
        return self._release_continuation_points

    @property
    def continuation_points_size(self):
        return self._continuation_points_size

    @property
    def continuation_points(self):
        return self._continuation_points

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @release_continuation_points.setter
    def release_continuation_points(self, val):
        self._release_continuation_points = val
        self._value.releaseContinuationPoints = val._value

    @continuation_points_size.setter
    def continuation_points_size(self, val):
        self._continuation_points_size = val
        self._value.continuationPointsSize = val._value

    @continuation_points.setter
    def continuation_points(self, val):
        self._continuation_points = val
        self._value.continuationPoints = val.__value

    def __str__(self, n=0):
        return ("(UaBrowseNextRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "release_continuation_points" + self._release_continuation_points.__str__(n + 1) +
                "\t" * (n + 1) + "continuation_points_size" + self._continuation_points_size.__str__(n + 1) +
                "\t" * (n + 1) + "continuation_points" + self._continuation_points.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaModifySubscriptionRequest +++++++++++++++++++++++
class UaModifySubscriptionRequest(UaType):
    def __init__(self, val=ffi.new("UA_ModifySubscriptionRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._requested_publishing_interval = UaDouble(val=val.requestedPublishingInterval, is_pointer=False)
        self._requested_lifetime_count = UaUInt32(val=val.requestedLifetimeCount, is_pointer=False)
        self._requested_max_keep_alive_count = UaUInt32(val=val.requestedMaxKeepAliveCount, is_pointer=False)
        self._max_notifications_per_publish = UaUInt32(val=val.maxNotificationsPerPublish, is_pointer=False)
        self._priority = UaByte(val=val.priority, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._requested_publishing_interval.__value[0] = _val(val.requestedPublishingInterval)
        self._requested_lifetime_count.__value[0] = _val(val.requestedLifetimeCount)
        self._requested_max_keep_alive_count.__value[0] = _val(val.requestedMaxKeepAliveCount)
        self._max_notifications_per_publish.__value[0] = _val(val.maxNotificationsPerPublish)
        self._priority.__value[0] = _val(val.priority)

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def requested_publishing_interval(self):
        return self._requested_publishing_interval

    @property
    def requested_lifetime_count(self):
        return self._requested_lifetime_count

    @property
    def requested_max_keep_alive_count(self):
        return self._requested_max_keep_alive_count

    @property
    def max_notifications_per_publish(self):
        return self._max_notifications_per_publish

    @property
    def priority(self):
        return self._priority

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @requested_publishing_interval.setter
    def requested_publishing_interval(self, val):
        self._requested_publishing_interval = val
        self._value.requestedPublishingInterval = val._value

    @requested_lifetime_count.setter
    def requested_lifetime_count(self, val):
        self._requested_lifetime_count = val
        self._value.requestedLifetimeCount = val._value

    @requested_max_keep_alive_count.setter
    def requested_max_keep_alive_count(self, val):
        self._requested_max_keep_alive_count = val
        self._value.requestedMaxKeepAliveCount = val._value

    @max_notifications_per_publish.setter
    def max_notifications_per_publish(self, val):
        self._max_notifications_per_publish = val
        self._value.maxNotificationsPerPublish = val._value

    @priority.setter
    def priority(self, val):
        self._priority = val
        self._value.priority = val._value

    def __str__(self, n=0):
        return ("(UaModifySubscriptionRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "requested_publishing_interval" + self._requested_publishing_interval.__str__(n + 1) +
                "\t" * (n + 1) + "requested_lifetime_count" + self._requested_lifetime_count.__str__(n + 1) +
                "\t" * (n + 1) + "requested_max_keep_alive_count" + self._requested_max_keep_alive_count.__str__(
                    n + 1) +
                "\t" * (n + 1) + "max_notifications_per_publish" + self._max_notifications_per_publish.__str__(n + 1) +
                "\t" * (n + 1) + "priority" + self._priority.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBrowseDescription +++++++++++++++++++++++
class UaBrowseDescription(UaType):
    def __init__(self, val=ffi.new("UA_BrowseDescription*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
        self._browse_direction = UaBrowseDirection(val=val.browseDirection, is_pointer=False)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
        self._include_subtypes = UaBoolean(val=val.includeSubtypes, is_pointer=False)
        self._node_class_mask = UaUInt32(val=val.nodeClassMask, is_pointer=False)
        self._result_mask = UaUInt32(val=val.resultMask, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._node_id.__value[0] = _val(val.nodeId)
        self._browse_direction.__value[0] = _val(val.browseDirection)
        self._reference_type_id.__value[0] = _val(val.referenceTypeId)
        self._include_subtypes.__value[0] = _val(val.includeSubtypes)
        self._node_class_mask.__value[0] = _val(val.nodeClassMask)
        self._result_mask.__value[0] = _val(val.resultMask)

    @property
    def node_id(self):
        return self._node_id

    @property
    def browse_direction(self):
        return self._browse_direction

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @property
    def include_subtypes(self):
        return self._include_subtypes

    @property
    def node_class_mask(self):
        return self._node_class_mask

    @property
    def result_mask(self):
        return self._result_mask

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val._value

    @browse_direction.setter
    def browse_direction(self, val):
        self._browse_direction = val
        self._value.browseDirection = val._value

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val._value

    @include_subtypes.setter
    def include_subtypes(self, val):
        self._include_subtypes = val
        self._value.includeSubtypes = val._value

    @node_class_mask.setter
    def node_class_mask(self, val):
        self._node_class_mask = val
        self._value.nodeClassMask = val._value

    @result_mask.setter
    def result_mask(self, val):
        self._result_mask = val
        self._value.resultMask = val._value

    def __str__(self, n=0):
        return ("(UaBrowseDescription) :\n" +
                "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1) +
                "\t" * (n + 1) + "browse_direction" + self._browse_direction.__str__(n + 1) +
                "\t" * (n + 1) + "reference_type_id" + self._reference_type_id.__str__(n + 1) +
                "\t" * (n + 1) + "include_subtypes" + self._include_subtypes.__str__(n + 1) +
                "\t" * (n + 1) + "node_class_mask" + self._node_class_mask.__str__(n + 1) +
                "\t" * (n + 1) + "result_mask" + self._result_mask.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSignedSoftwareCertificate +++++++++++++++++++++++
class UaSignedSoftwareCertificate(UaType):
    def __init__(self, val=ffi.new("UA_SignedSoftwareCertificate*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._certificate_data = UaByteString(val=val.certificateData, is_pointer=False)
        self._signature = UaByteString(val=val.signature, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._certificate_data.__value[0] = _val(val.certificateData)
        self._signature.__value[0] = _val(val.signature)

    @property
    def certificate_data(self):
        return self._certificate_data

    @property
    def signature(self):
        return self._signature

    @certificate_data.setter
    def certificate_data(self, val):
        self._certificate_data = val
        self._value.certificateData = val._value

    @signature.setter
    def signature(self, val):
        self._signature = val
        self._value.signature = val._value

    def __str__(self, n=0):
        return ("(UaSignedSoftwareCertificate) :\n" +
                "\t" * (n + 1) + "certificate_data" + self._certificate_data.__str__(n + 1) +
                "\t" * (n + 1) + "signature" + self._signature.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBrowsePathTarget +++++++++++++++++++++++
class UaBrowsePathTarget(UaType):
    def __init__(self, val=ffi.new("UA_BrowsePathTarget*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._target_id = UaExpandedNodeId(val=val.targetId, is_pointer=False)
        self._remaining_path_index = UaUInt32(val=val.remainingPathIndex, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._target_id.__value[0] = _val(val.targetId)
        self._remaining_path_index.__value[0] = _val(val.remainingPathIndex)

    @property
    def target_id(self):
        return self._target_id

    @property
    def remaining_path_index(self):
        return self._remaining_path_index

    @target_id.setter
    def target_id(self, val):
        self._target_id = val
        self._value.targetId = val._value

    @remaining_path_index.setter
    def remaining_path_index(self, val):
        self._remaining_path_index = val
        self._value.remainingPathIndex = val._value

    def __str__(self, n=0):
        return ("(UaBrowsePathTarget) :\n" +
                "\t" * (n + 1) + "target_id" + self._target_id.__str__(n + 1) +
                "\t" * (n + 1) + "remaining_path_index" + self._remaining_path_index.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaWriteResponse +++++++++++++++++++++++
class UaWriteResponse(UaType):
    def __init__(self, val=ffi.new("UA_WriteResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaWriteResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAddNodesResult +++++++++++++++++++++++
class UaAddNodesResult(UaType):
    def __init__(self, val=ffi.new("UA_AddNodesResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
        self._added_node_id = UaNodeId(val=val.addedNodeId, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._status_code.__value[0] = _val(val.statusCode)
        self._added_node_id.__value[0] = _val(val.addedNodeId)

    @property
    def status_code(self):
        return self._status_code

    @property
    def added_node_id(self):
        return self._added_node_id

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val._value

    @added_node_id.setter
    def added_node_id(self, val):
        self._added_node_id = val
        self._value.addedNodeId = val._value

    def __str__(self, n=0):
        return ("(UaAddNodesResult) :\n" +
                "\t" * (n + 1) + "status_code" + self._status_code.__str__(n + 1) +
                "\t" * (n + 1) + "added_node_id" + self._added_node_id.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAddReferencesItem +++++++++++++++++++++++
class UaAddReferencesItem(UaType):
    def __init__(self, val=ffi.new("UA_AddReferencesItem*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._source_node_id = UaNodeId(val=val.sourceNodeId, is_pointer=False)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
        self._is_forward = UaBoolean(val=val.isForward, is_pointer=False)
        self._target_server_uri = UaString(val=val.targetServerUri, is_pointer=False)
        self._target_node_id = UaExpandedNodeId(val=val.targetNodeId, is_pointer=False)
        self._target_node_class = UaNodeClass(val=val.targetNodeClass, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._source_node_id.__value[0] = _val(val.sourceNodeId)
        self._reference_type_id.__value[0] = _val(val.referenceTypeId)
        self._is_forward.__value[0] = _val(val.isForward)
        self._target_server_uri.__value[0] = _val(val.targetServerUri)
        self._target_node_id.__value[0] = _val(val.targetNodeId)
        self._target_node_class.__value[0] = _val(val.targetNodeClass)

    @property
    def source_node_id(self):
        return self._source_node_id

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @property
    def is_forward(self):
        return self._is_forward

    @property
    def target_server_uri(self):
        return self._target_server_uri

    @property
    def target_node_id(self):
        return self._target_node_id

    @property
    def target_node_class(self):
        return self._target_node_class

    @source_node_id.setter
    def source_node_id(self, val):
        self._source_node_id = val
        self._value.sourceNodeId = val._value

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val._value

    @is_forward.setter
    def is_forward(self, val):
        self._is_forward = val
        self._value.isForward = val._value

    @target_server_uri.setter
    def target_server_uri(self, val):
        self._target_server_uri = val
        self._value.targetServerUri = val._value

    @target_node_id.setter
    def target_node_id(self, val):
        self._target_node_id = val
        self._value.targetNodeId = val._value

    @target_node_class.setter
    def target_node_class(self, val):
        self._target_node_class = val
        self._value.targetNodeClass = val._value

    def __str__(self, n=0):
        return ("(UaAddReferencesItem) :\n" +
                "\t" * (n + 1) + "source_node_id" + self._source_node_id.__str__(n + 1) +
                "\t" * (n + 1) + "reference_type_id" + self._reference_type_id.__str__(n + 1) +
                "\t" * (n + 1) + "is_forward" + self._is_forward.__str__(n + 1) +
                "\t" * (n + 1) + "target_server_uri" + self._target_server_uri.__str__(n + 1) +
                "\t" * (n + 1) + "target_node_id" + self._target_node_id.__str__(n + 1) +
                "\t" * (n + 1) + "target_node_class" + self._target_node_class.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteReferencesResponse +++++++++++++++++++++++
class UaDeleteReferencesResponse(UaType):
    def __init__(self, val=ffi.new("UA_DeleteReferencesResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaDeleteReferencesResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaRelativePathElement +++++++++++++++++++++++
class UaRelativePathElement(UaType):
    def __init__(self, val=ffi.new("UA_RelativePathElement*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
        self._is_inverse = UaBoolean(val=val.isInverse, is_pointer=False)
        self._include_subtypes = UaBoolean(val=val.includeSubtypes, is_pointer=False)
        self._target_name = UaQualifiedName(val=val.targetName, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._reference_type_id.__value[0] = _val(val.referenceTypeId)
        self._is_inverse.__value[0] = _val(val.isInverse)
        self._include_subtypes.__value[0] = _val(val.includeSubtypes)
        self._target_name.__value[0] = _val(val.targetName)

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @property
    def is_inverse(self):
        return self._is_inverse

    @property
    def include_subtypes(self):
        return self._include_subtypes

    @property
    def target_name(self):
        return self._target_name

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val._value

    @is_inverse.setter
    def is_inverse(self, val):
        self._is_inverse = val
        self._value.isInverse = val._value

    @include_subtypes.setter
    def include_subtypes(self, val):
        self._include_subtypes = val
        self._value.includeSubtypes = val._value

    @target_name.setter
    def target_name(self, val):
        self._target_name = val
        self._value.targetName = val._value

    def __str__(self, n=0):
        return ("(UaRelativePathElement) :\n" +
                "\t" * (n + 1) + "reference_type_id" + self._reference_type_id.__str__(n + 1) +
                "\t" * (n + 1) + "is_inverse" + self._is_inverse.__str__(n + 1) +
                "\t" * (n + 1) + "include_subtypes" + self._include_subtypes.__str__(n + 1) +
                "\t" * (n + 1) + "target_name" + self._target_name.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSubscriptionAcknowledgement +++++++++++++++++++++++
class UaSubscriptionAcknowledgement(UaType):
    def __init__(self, val=ffi.new("UA_SubscriptionAcknowledgement*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._sequence_number = UaUInt32(val=val.sequenceNumber, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._sequence_number.__value[0] = _val(val.sequenceNumber)

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def sequence_number(self):
        return self._sequence_number

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @sequence_number.setter
    def sequence_number(self, val):
        self._sequence_number = val
        self._value.sequenceNumber = val._value

    def __str__(self, n=0):
        return ("(UaSubscriptionAcknowledgement) :\n" +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "sequence_number" + self._sequence_number.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaTransferResult +++++++++++++++++++++++
class UaTransferResult(UaType):
    def __init__(self, val=ffi.new("UA_TransferResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
        self._available_sequence_numbers_size = SizeT(val=val.availableSequenceNumbersSize, is_pointer=False)
        self._available_sequence_numbers = UaUInt32(val=val.availableSequenceNumbers, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._status_code.__value[0] = _val(val.statusCode)
        self._available_sequence_numbers_size.__value[0] = _val(val.availableSequenceNumbersSize)
        self._available_sequence_numbers.__value = val.availableSequenceNumbers

    @property
    def status_code(self):
        return self._status_code

    @property
    def available_sequence_numbers_size(self):
        return self._available_sequence_numbers_size

    @property
    def available_sequence_numbers(self):
        return self._available_sequence_numbers

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val._value

    @available_sequence_numbers_size.setter
    def available_sequence_numbers_size(self, val):
        self._available_sequence_numbers_size = val
        self._value.availableSequenceNumbersSize = val._value

    @available_sequence_numbers.setter
    def available_sequence_numbers(self, val):
        self._available_sequence_numbers = val
        self._value.availableSequenceNumbers = val.__value

    def __str__(self, n=0):
        return ("(UaTransferResult) :\n" +
                "\t" * (n + 1) + "status_code" + self._status_code.__str__(n + 1) +
                "\t" * (n + 1) + "available_sequence_numbers_size" + self._available_sequence_numbers_size.__str__(
                    n + 1) +
                "\t" * (n + 1) + "available_sequence_numbers" + self._available_sequence_numbers.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCreateMonitoredItemsResponse +++++++++++++++++++++++
class UaCreateMonitoredItemsResponse(UaType):
    def __init__(self, val=ffi.new("UA_CreateMonitoredItemsResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaMonitoredItemCreateResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaCreateMonitoredItemsResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteReferencesItem +++++++++++++++++++++++
class UaDeleteReferencesItem(UaType):
    def __init__(self, val=ffi.new("UA_DeleteReferencesItem*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._source_node_id = UaNodeId(val=val.sourceNodeId, is_pointer=False)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
        self._is_forward = UaBoolean(val=val.isForward, is_pointer=False)
        self._target_node_id = UaExpandedNodeId(val=val.targetNodeId, is_pointer=False)
        self._delete_bidirectional = UaBoolean(val=val.deleteBidirectional, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._source_node_id.__value[0] = _val(val.sourceNodeId)
        self._reference_type_id.__value[0] = _val(val.referenceTypeId)
        self._is_forward.__value[0] = _val(val.isForward)
        self._target_node_id.__value[0] = _val(val.targetNodeId)
        self._delete_bidirectional.__value[0] = _val(val.deleteBidirectional)

    @property
    def source_node_id(self):
        return self._source_node_id

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @property
    def is_forward(self):
        return self._is_forward

    @property
    def target_node_id(self):
        return self._target_node_id

    @property
    def delete_bidirectional(self):
        return self._delete_bidirectional

    @source_node_id.setter
    def source_node_id(self, val):
        self._source_node_id = val
        self._value.sourceNodeId = val._value

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val._value

    @is_forward.setter
    def is_forward(self, val):
        self._is_forward = val
        self._value.isForward = val._value

    @target_node_id.setter
    def target_node_id(self, val):
        self._target_node_id = val
        self._value.targetNodeId = val._value

    @delete_bidirectional.setter
    def delete_bidirectional(self, val):
        self._delete_bidirectional = val
        self._value.deleteBidirectional = val._value

    def __str__(self, n=0):
        return ("(UaDeleteReferencesItem) :\n" +
                "\t" * (n + 1) + "source_node_id" + self._source_node_id.__str__(n + 1) +
                "\t" * (n + 1) + "reference_type_id" + self._reference_type_id.__str__(n + 1) +
                "\t" * (n + 1) + "is_forward" + self._is_forward.__str__(n + 1) +
                "\t" * (n + 1) + "target_node_id" + self._target_node_id.__str__(n + 1) +
                "\t" * (n + 1) + "delete_bidirectional" + self._delete_bidirectional.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaWriteValue +++++++++++++++++++++++
class UaWriteValue(UaType):
    def __init__(self, val=ffi.new("UA_WriteValue*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
        self._attribute_id = UaUInt32(val=val.attributeId, is_pointer=False)
        self._index_range = UaString(val=val.indexRange, is_pointer=False)
        self._value = UaDataValue(val=val.value, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._node_id.__value[0] = _val(val.nodeId)
        self._attribute_id.__value[0] = _val(val.attributeId)
        self._index_range.__value[0] = _val(val.indexRange)
        self._value.__value[0] = _val(val.value)

    @property
    def node_id(self):
        return self._node_id

    @property
    def attribute_id(self):
        return self._attribute_id

    @property
    def index_range(self):
        return self._index_range

    @property
    def value(self):
        return self._value

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val._value

    @attribute_id.setter
    def attribute_id(self, val):
        self._attribute_id = val
        self._value.attributeId = val._value

    @index_range.setter
    def index_range(self, val):
        self._index_range = val
        self._value.indexRange = val._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val._value

    def __str__(self, n=0):
        return ("(UaWriteValue) :\n" +
                "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1) +
                "\t" * (n + 1) + "attribute_id" + self._attribute_id.__str__(n + 1) +
                "\t" * (n + 1) + "index_range" + self._index_range.__str__(n + 1) +
                "\t" * (n + 1) + "value" + self._value.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDataTypeAttributes +++++++++++++++++++++++
class UaDataTypeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_DataTypeAttributes*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
        self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
        self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._specified_attributes.__value[0] = _val(val.specifiedAttributes)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._write_mask.__value[0] = _val(val.writeMask)
        self._user_write_mask.__value[0] = _val(val.userWriteMask)
        self._is_abstract.__value[0] = _val(val.isAbstract)

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def write_mask(self):
        return self._write_mask

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @property
    def is_abstract(self):
        return self._is_abstract

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val._value

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val._value

    @is_abstract.setter
    def is_abstract(self, val):
        self._is_abstract = val
        self._value.isAbstract = val._value

    def __str__(self, n=0):
        return ("(UaDataTypeAttributes) :\n" +
                "\t" * (n + 1) + "specified_attributes" + self._specified_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "user_write_mask" + self._user_write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "is_abstract" + self._is_abstract.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaTransferSubscriptionsResponse +++++++++++++++++++++++
class UaTransferSubscriptionsResponse(UaType):
    def __init__(self, val=ffi.new("UA_TransferSubscriptionsResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaTransferResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaTransferSubscriptionsResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAddReferencesResponse +++++++++++++++++++++++
class UaAddReferencesResponse(UaType):
    def __init__(self, val=ffi.new("UA_AddReferencesResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaAddReferencesResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBuildInfo +++++++++++++++++++++++
class UaBuildInfo(UaType):
    def __init__(self, val=ffi.new("UA_BuildInfo*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._product_uri = UaString(val=val.productUri, is_pointer=False)
        self._manufacturer_name = UaString(val=val.manufacturerName, is_pointer=False)
        self._product_name = UaString(val=val.productName, is_pointer=False)
        self._software_version = UaString(val=val.softwareVersion, is_pointer=False)
        self._build_number = UaString(val=val.buildNumber, is_pointer=False)
        self._build_date = UaDateTime(val=val.buildDate, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._product_uri.__value[0] = _val(val.productUri)
        self._manufacturer_name.__value[0] = _val(val.manufacturerName)
        self._product_name.__value[0] = _val(val.productName)
        self._software_version.__value[0] = _val(val.softwareVersion)
        self._build_number.__value[0] = _val(val.buildNumber)
        self._build_date.__value[0] = _val(val.buildDate)

    @property
    def product_uri(self):
        return self._product_uri

    @property
    def manufacturer_name(self):
        return self._manufacturer_name

    @property
    def product_name(self):
        return self._product_name

    @property
    def software_version(self):
        return self._software_version

    @property
    def build_number(self):
        return self._build_number

    @property
    def build_date(self):
        return self._build_date

    @product_uri.setter
    def product_uri(self, val):
        self._product_uri = val
        self._value.productUri = val._value

    @manufacturer_name.setter
    def manufacturer_name(self, val):
        self._manufacturer_name = val
        self._value.manufacturerName = val._value

    @product_name.setter
    def product_name(self, val):
        self._product_name = val
        self._value.productName = val._value

    @software_version.setter
    def software_version(self, val):
        self._software_version = val
        self._value.softwareVersion = val._value

    @build_number.setter
    def build_number(self, val):
        self._build_number = val
        self._value.buildNumber = val._value

    @build_date.setter
    def build_date(self, val):
        self._build_date = val
        self._value.buildDate = val._value

    def __str__(self, n=0):
        return ("(UaBuildInfo) :\n" +
                "\t" * (n + 1) + "product_uri" + self._product_uri.__str__(n + 1) +
                "\t" * (n + 1) + "manufacturer_name" + self._manufacturer_name.__str__(n + 1) +
                "\t" * (n + 1) + "product_name" + self._product_name.__str__(n + 1) +
                "\t" * (n + 1) + "software_version" + self._software_version.__str__(n + 1) +
                "\t" * (n + 1) + "build_number" + self._build_number.__str__(n + 1) +
                "\t" * (n + 1) + "build_date" + self._build_date.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaMonitoringParameters +++++++++++++++++++++++
class UaMonitoringParameters(UaType):
    def __init__(self, val=ffi.new("UA_MonitoringParameters*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._client_handle = UaUInt32(val=val.clientHandle, is_pointer=False)
        self._sampling_interval = UaDouble(val=val.samplingInterval, is_pointer=False)
        self._filter = UaExtensionObject(val=val.filter, is_pointer=False)
        self._queue_size = UaUInt32(val=val.queueSize, is_pointer=False)
        self._discard_oldest = UaBoolean(val=val.discardOldest, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._client_handle.__value[0] = _val(val.clientHandle)
        self._sampling_interval.__value[0] = _val(val.samplingInterval)
        self._filter.__value[0] = _val(val.filter)
        self._queue_size.__value[0] = _val(val.queueSize)
        self._discard_oldest.__value[0] = _val(val.discardOldest)

    @property
    def client_handle(self):
        return self._client_handle

    @property
    def sampling_interval(self):
        return self._sampling_interval

    @property
    def filter(self):
        return self._filter

    @property
    def queue_size(self):
        return self._queue_size

    @property
    def discard_oldest(self):
        return self._discard_oldest

    @client_handle.setter
    def client_handle(self, val):
        self._client_handle = val
        self._value.clientHandle = val._value

    @sampling_interval.setter
    def sampling_interval(self, val):
        self._sampling_interval = val
        self._value.samplingInterval = val._value

    @filter.setter
    def filter(self, val):
        self._filter = val
        self._value.filter = val._value

    @queue_size.setter
    def queue_size(self, val):
        self._queue_size = val
        self._value.queueSize = val._value

    @discard_oldest.setter
    def discard_oldest(self, val):
        self._discard_oldest = val
        self._value.discardOldest = val._value

    def __str__(self, n=0):
        return ("(UaMonitoringParameters) :\n" +
                "\t" * (n + 1) + "client_handle" + self._client_handle.__str__(n + 1) +
                "\t" * (n + 1) + "sampling_interval" + self._sampling_interval.__str__(n + 1) +
                "\t" * (n + 1) + "filter" + self._filter.__str__(n + 1) +
                "\t" * (n + 1) + "queue_size" + self._queue_size.__str__(n + 1) +
                "\t" * (n + 1) + "discard_oldest" + self._discard_oldest.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDoubleComplexNumberType +++++++++++++++++++++++
class UaDoubleComplexNumberType(UaType):
    def __init__(self, val=ffi.new("UA_DoubleComplexNumberType*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._real = UaDouble(val=val.real, is_pointer=False)
        self._imaginary = UaDouble(val=val.imaginary, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._real.__value[0] = _val(val.real)
        self._imaginary.__value[0] = _val(val.imaginary)

    @property
    def real(self):
        return self._real

    @property
    def imaginary(self):
        return self._imaginary

    @real.setter
    def real(self, val):
        self._real = val
        self._value.real = val._value

    @imaginary.setter
    def imaginary(self, val):
        self._imaginary = val
        self._value.imaginary = val._value

    def __str__(self, n=0):
        return ("(UaDoubleComplexNumberType) :\n" +
                "\t" * (n + 1) + "real" + self._real.__str__(n + 1) +
                "\t" * (n + 1) + "imaginary" + self._imaginary.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteNodesItem +++++++++++++++++++++++
class UaDeleteNodesItem(UaType):
    def __init__(self, val=ffi.new("UA_DeleteNodesItem*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
        self._delete_target_references = UaBoolean(val=val.deleteTargetReferences, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._node_id.__value[0] = _val(val.nodeId)
        self._delete_target_references.__value[0] = _val(val.deleteTargetReferences)

    @property
    def node_id(self):
        return self._node_id

    @property
    def delete_target_references(self):
        return self._delete_target_references

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val._value

    @delete_target_references.setter
    def delete_target_references(self, val):
        self._delete_target_references = val
        self._value.deleteTargetReferences = val._value

    def __str__(self, n=0):
        return ("(UaDeleteNodesItem) :\n" +
                "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1) +
                "\t" * (n + 1) + "delete_target_references" + self._delete_target_references.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaReadValueId +++++++++++++++++++++++
class UaReadValueId(UaType):
    def __init__(self, val=ffi.new("UA_ReadValueId*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
        self._attribute_id = UaUInt32(val=val.attributeId, is_pointer=False)
        self._index_range = UaString(val=val.indexRange, is_pointer=False)
        self._data_encoding = UaQualifiedName(val=val.dataEncoding, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._node_id.__value[0] = _val(val.nodeId)
        self._attribute_id.__value[0] = _val(val.attributeId)
        self._index_range.__value[0] = _val(val.indexRange)
        self._data_encoding.__value[0] = _val(val.dataEncoding)

    @property
    def node_id(self):
        return self._node_id

    @property
    def attribute_id(self):
        return self._attribute_id

    @property
    def index_range(self):
        return self._index_range

    @property
    def data_encoding(self):
        return self._data_encoding

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val._value

    @attribute_id.setter
    def attribute_id(self, val):
        self._attribute_id = val
        self._value.attributeId = val._value

    @index_range.setter
    def index_range(self, val):
        self._index_range = val
        self._value.indexRange = val._value

    @data_encoding.setter
    def data_encoding(self, val):
        self._data_encoding = val
        self._value.dataEncoding = val._value

    def __str__(self, n=0):
        return ("(UaReadValueId) :\n" +
                "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1) +
                "\t" * (n + 1) + "attribute_id" + self._attribute_id.__str__(n + 1) +
                "\t" * (n + 1) + "index_range" + self._index_range.__str__(n + 1) +
                "\t" * (n + 1) + "data_encoding" + self._data_encoding.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCallRequest +++++++++++++++++++++++
class UaCallRequest(UaType):
    def __init__(self, val=ffi.new("UA_CallRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._methods_to_call_size = SizeT(val=val.methodsToCallSize, is_pointer=False)
        self._methods_to_call = UaCallMethodRequest(val=val.methodsToCall, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._methods_to_call_size.__value[0] = _val(val.methodsToCallSize)
        self._methods_to_call.__value = val.methodsToCall

    @property
    def request_header(self):
        return self._request_header

    @property
    def methods_to_call_size(self):
        return self._methods_to_call_size

    @property
    def methods_to_call(self):
        return self._methods_to_call

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @methods_to_call_size.setter
    def methods_to_call_size(self, val):
        self._methods_to_call_size = val
        self._value.methodsToCallSize = val._value

    @methods_to_call.setter
    def methods_to_call(self, val):
        self._methods_to_call = val
        self._value.methodsToCall = val.__value

    def __str__(self, n=0):
        return ("(UaCallRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "methods_to_call_size" + self._methods_to_call_size.__str__(n + 1) +
                "\t" * (n + 1) + "methods_to_call" + self._methods_to_call.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaRelativePath +++++++++++++++++++++++
class UaRelativePath(UaType):
    def __init__(self, val=ffi.new("UA_RelativePath*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._elements_size = SizeT(val=val.elementsSize, is_pointer=False)
        self._elements = UaRelativePathElement(val=val.elements, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._elements_size.__value[0] = _val(val.elementsSize)
        self._elements.__value = val.elements

    @property
    def elements_size(self):
        return self._elements_size

    @property
    def elements(self):
        return self._elements

    @elements_size.setter
    def elements_size(self, val):
        self._elements_size = val
        self._value.elementsSize = val._value

    @elements.setter
    def elements(self, val):
        self._elements = val
        self._value.elements = val.__value

    def __str__(self, n=0):
        return ("(UaRelativePath) :\n" +
                "\t" * (n + 1) + "elements_size" + self._elements_size.__str__(n + 1) +
                "\t" * (n + 1) + "elements" + self._elements.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteNodesRequest +++++++++++++++++++++++
class UaDeleteNodesRequest(UaType):
    def __init__(self, val=ffi.new("UA_DeleteNodesRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._nodes_to_delete_size = SizeT(val=val.nodesToDeleteSize, is_pointer=False)
        self._nodes_to_delete = UaDeleteNodesItem(val=val.nodesToDelete, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._nodes_to_delete_size.__value[0] = _val(val.nodesToDeleteSize)
        self._nodes_to_delete.__value = val.nodesToDelete

    @property
    def request_header(self):
        return self._request_header

    @property
    def nodes_to_delete_size(self):
        return self._nodes_to_delete_size

    @property
    def nodes_to_delete(self):
        return self._nodes_to_delete

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @nodes_to_delete_size.setter
    def nodes_to_delete_size(self, val):
        self._nodes_to_delete_size = val
        self._value.nodesToDeleteSize = val._value

    @nodes_to_delete.setter
    def nodes_to_delete(self, val):
        self._nodes_to_delete = val
        self._value.nodesToDelete = val.__value

    def __str__(self, n=0):
        return ("(UaDeleteNodesRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_delete_size" + self._nodes_to_delete_size.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_delete" + self._nodes_to_delete.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaMonitoredItemModifyRequest +++++++++++++++++++++++
class UaMonitoredItemModifyRequest(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemModifyRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._monitored_item_id = UaUInt32(val=val.monitoredItemId, is_pointer=False)
        self._requested_parameters = UaMonitoringParameters(val=val.requestedParameters, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._monitored_item_id.__value[0] = _val(val.monitoredItemId)
        self._requested_parameters.__value[0] = _val(val.requestedParameters)

    @property
    def monitored_item_id(self):
        return self._monitored_item_id

    @property
    def requested_parameters(self):
        return self._requested_parameters

    @monitored_item_id.setter
    def monitored_item_id(self, val):
        self._monitored_item_id = val
        self._value.monitoredItemId = val._value

    @requested_parameters.setter
    def requested_parameters(self, val):
        self._requested_parameters = val
        self._value.requestedParameters = val._value

    def __str__(self, n=0):
        return ("(UaMonitoredItemModifyRequest) :\n" +
                "\t" * (n + 1) + "monitored_item_id" + self._monitored_item_id.__str__(n + 1) +
                "\t" * (n + 1) + "requested_parameters" + self._requested_parameters.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAggregateConfiguration +++++++++++++++++++++++
class UaAggregateConfiguration(UaType):
    def __init__(self, val=ffi.new("UA_AggregateConfiguration*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._use_server_capabilities_defaults = UaBoolean(val=val.useServerCapabilitiesDefaults, is_pointer=False)
        self._treat_uncertain_as_bad = UaBoolean(val=val.treatUncertainAsBad, is_pointer=False)
        self._percent_data_bad = UaByte(val=val.percentDataBad, is_pointer=False)
        self._percent_data_good = UaByte(val=val.percentDataGood, is_pointer=False)
        self._use_sloped_extrapolation = UaBoolean(val=val.useSlopedExtrapolation, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._use_server_capabilities_defaults.__value[0] = _val(val.useServerCapabilitiesDefaults)
        self._treat_uncertain_as_bad.__value[0] = _val(val.treatUncertainAsBad)
        self._percent_data_bad.__value[0] = _val(val.percentDataBad)
        self._percent_data_good.__value[0] = _val(val.percentDataGood)
        self._use_sloped_extrapolation.__value[0] = _val(val.useSlopedExtrapolation)

    @property
    def use_server_capabilities_defaults(self):
        return self._use_server_capabilities_defaults

    @property
    def treat_uncertain_as_bad(self):
        return self._treat_uncertain_as_bad

    @property
    def percent_data_bad(self):
        return self._percent_data_bad

    @property
    def percent_data_good(self):
        return self._percent_data_good

    @property
    def use_sloped_extrapolation(self):
        return self._use_sloped_extrapolation

    @use_server_capabilities_defaults.setter
    def use_server_capabilities_defaults(self, val):
        self._use_server_capabilities_defaults = val
        self._value.useServerCapabilitiesDefaults = val._value

    @treat_uncertain_as_bad.setter
    def treat_uncertain_as_bad(self, val):
        self._treat_uncertain_as_bad = val
        self._value.treatUncertainAsBad = val._value

    @percent_data_bad.setter
    def percent_data_bad(self, val):
        self._percent_data_bad = val
        self._value.percentDataBad = val._value

    @percent_data_good.setter
    def percent_data_good(self, val):
        self._percent_data_good = val
        self._value.percentDataGood = val._value

    @use_sloped_extrapolation.setter
    def use_sloped_extrapolation(self, val):
        self._use_sloped_extrapolation = val
        self._value.useSlopedExtrapolation = val._value

    def __str__(self, n=0):
        return ("(UaAggregateConfiguration) :\n" +
                "\t" * (n + 1) + "use_server_capabilities_defaults" + self._use_server_capabilities_defaults.__str__(
                    n + 1) +
                "\t" * (n + 1) + "treat_uncertain_as_bad" + self._treat_uncertain_as_bad.__str__(n + 1) +
                "\t" * (n + 1) + "percent_data_bad" + self._percent_data_bad.__str__(n + 1) +
                "\t" * (n + 1) + "percent_data_good" + self._percent_data_good.__str__(n + 1) +
                "\t" * (n + 1) + "use_sloped_extrapolation" + self._use_sloped_extrapolation.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaUnregisterNodesResponse +++++++++++++++++++++++
class UaUnregisterNodesResponse(UaType):
    def __init__(self, val=ffi.new("UA_UnregisterNodesResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    def __str__(self, n=0):
        return ("(UaUnregisterNodesResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaContentFilterResult +++++++++++++++++++++++
class UaContentFilterResult(UaType):
    def __init__(self, val=ffi.new("UA_ContentFilterResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._element_results_size = SizeT(val=val.elementResultsSize, is_pointer=False)
        self._element_results = UaContentFilterElementResult(val=val.elementResults, is_pointer=True)
        self._element_diagnostic_infos_size = SizeT(val=val.elementDiagnosticInfosSize, is_pointer=False)
        self._element_diagnostic_infos = UaDiagnosticInfo(val=val.elementDiagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._element_results_size.__value[0] = _val(val.elementResultsSize)
        self._element_results.__value = val.elementResults
        self._element_diagnostic_infos_size.__value[0] = _val(val.elementDiagnosticInfosSize)
        self._element_diagnostic_infos.__value = val.elementDiagnosticInfos

    @property
    def element_results_size(self):
        return self._element_results_size

    @property
    def element_results(self):
        return self._element_results

    @property
    def element_diagnostic_infos_size(self):
        return self._element_diagnostic_infos_size

    @property
    def element_diagnostic_infos(self):
        return self._element_diagnostic_infos

    @element_results_size.setter
    def element_results_size(self, val):
        self._element_results_size = val
        self._value.elementResultsSize = val._value

    @element_results.setter
    def element_results(self, val):
        self._element_results = val
        self._value.elementResults = val.__value

    @element_diagnostic_infos_size.setter
    def element_diagnostic_infos_size(self, val):
        self._element_diagnostic_infos_size = val
        self._value.elementDiagnosticInfosSize = val._value

    @element_diagnostic_infos.setter
    def element_diagnostic_infos(self, val):
        self._element_diagnostic_infos = val
        self._value.elementDiagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaContentFilterResult) :\n" +
                "\t" * (n + 1) + "element_results_size" + self._element_results_size.__str__(n + 1) +
                "\t" * (n + 1) + "element_results" + self._element_results.__str__(n + 1) +
                "\t" * (n + 1) + "element_diagnostic_infos_size" + self._element_diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "element_diagnostic_infos" + self._element_diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaUserTokenPolicy +++++++++++++++++++++++
class UaUserTokenPolicy(UaType):
    def __init__(self, val=ffi.new("UA_UserTokenPolicy*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._policy_id = UaString(val=val.policyId, is_pointer=False)
        self._token_type = UaUserTokenType(val=val.tokenType, is_pointer=False)
        self._issued_token_type = UaString(val=val.issuedTokenType, is_pointer=False)
        self._issuer_endpoint_url = UaString(val=val.issuerEndpointUrl, is_pointer=False)
        self._security_policy_uri = UaString(val=val.securityPolicyUri, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._policy_id.__value[0] = _val(val.policyId)
        self._token_type.__value[0] = _val(val.tokenType)
        self._issued_token_type.__value[0] = _val(val.issuedTokenType)
        self._issuer_endpoint_url.__value[0] = _val(val.issuerEndpointUrl)
        self._security_policy_uri.__value[0] = _val(val.securityPolicyUri)

    @property
    def policy_id(self):
        return self._policy_id

    @property
    def token_type(self):
        return self._token_type

    @property
    def issued_token_type(self):
        return self._issued_token_type

    @property
    def issuer_endpoint_url(self):
        return self._issuer_endpoint_url

    @property
    def security_policy_uri(self):
        return self._security_policy_uri

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val._value

    @token_type.setter
    def token_type(self, val):
        self._token_type = val
        self._value.tokenType = val._value

    @issued_token_type.setter
    def issued_token_type(self, val):
        self._issued_token_type = val
        self._value.issuedTokenType = val._value

    @issuer_endpoint_url.setter
    def issuer_endpoint_url(self, val):
        self._issuer_endpoint_url = val
        self._value.issuerEndpointUrl = val._value

    @security_policy_uri.setter
    def security_policy_uri(self, val):
        self._security_policy_uri = val
        self._value.securityPolicyUri = val._value

    def __str__(self, n=0):
        return ("(UaUserTokenPolicy) :\n" +
                "\t" * (n + 1) + "policy_id" + self._policy_id.__str__(n + 1) +
                "\t" * (n + 1) + "token_type" + self._token_type.__str__(n + 1) +
                "\t" * (n + 1) + "issued_token_type" + self._issued_token_type.__str__(n + 1) +
                "\t" * (n + 1) + "issuer_endpoint_url" + self._issuer_endpoint_url.__str__(n + 1) +
                "\t" * (n + 1) + "security_policy_uri" + self._security_policy_uri.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteMonitoredItemsRequest +++++++++++++++++++++++
class UaDeleteMonitoredItemsRequest(UaType):
    def __init__(self, val=ffi.new("UA_DeleteMonitoredItemsRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._monitored_item_ids_size = SizeT(val=val.monitoredItemIdsSize, is_pointer=False)
        self._monitored_item_ids = UaUInt32(val=val.monitoredItemIds, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._monitored_item_ids_size.__value[0] = _val(val.monitoredItemIdsSize)
        self._monitored_item_ids.__value = val.monitoredItemIds

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def monitored_item_ids_size(self):
        return self._monitored_item_ids_size

    @property
    def monitored_item_ids(self):
        return self._monitored_item_ids

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @monitored_item_ids_size.setter
    def monitored_item_ids_size(self, val):
        self._monitored_item_ids_size = val
        self._value.monitoredItemIdsSize = val._value

    @monitored_item_ids.setter
    def monitored_item_ids(self, val):
        self._monitored_item_ids = val
        self._value.monitoredItemIds = val.__value

    def __str__(self, n=0):
        return ("(UaDeleteMonitoredItemsRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "monitored_item_ids_size" + self._monitored_item_ids_size.__str__(n + 1) +
                "\t" * (n + 1) + "monitored_item_ids" + self._monitored_item_ids.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSetMonitoringModeRequest +++++++++++++++++++++++
class UaSetMonitoringModeRequest(UaType):
    def __init__(self, val=ffi.new("UA_SetMonitoringModeRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._monitoring_mode = UaMonitoringMode(val=val.monitoringMode, is_pointer=False)
        self._monitored_item_ids_size = SizeT(val=val.monitoredItemIdsSize, is_pointer=False)
        self._monitored_item_ids = UaUInt32(val=val.monitoredItemIds, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._monitoring_mode.__value[0] = _val(val.monitoringMode)
        self._monitored_item_ids_size.__value[0] = _val(val.monitoredItemIdsSize)
        self._monitored_item_ids.__value = val.monitoredItemIds

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def monitoring_mode(self):
        return self._monitoring_mode

    @property
    def monitored_item_ids_size(self):
        return self._monitored_item_ids_size

    @property
    def monitored_item_ids(self):
        return self._monitored_item_ids

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @monitoring_mode.setter
    def monitoring_mode(self, val):
        self._monitoring_mode = val
        self._value.monitoringMode = val._value

    @monitored_item_ids_size.setter
    def monitored_item_ids_size(self, val):
        self._monitored_item_ids_size = val
        self._value.monitoredItemIdsSize = val._value

    @monitored_item_ids.setter
    def monitored_item_ids(self, val):
        self._monitored_item_ids = val
        self._value.monitoredItemIds = val.__value

    def __str__(self, n=0):
        return ("(UaSetMonitoringModeRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "monitoring_mode" + self._monitoring_mode.__str__(n + 1) +
                "\t" * (n + 1) + "monitored_item_ids_size" + self._monitored_item_ids_size.__str__(n + 1) +
                "\t" * (n + 1) + "monitored_item_ids" + self._monitored_item_ids.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaReferenceTypeAttributes +++++++++++++++++++++++
class UaReferenceTypeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_ReferenceTypeAttributes*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
        self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
        self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)
        self._symmetric = UaBoolean(val=val.symmetric, is_pointer=False)
        self._inverse_name = UaLocalizedText(val=val.inverseName, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._specified_attributes.__value[0] = _val(val.specifiedAttributes)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._write_mask.__value[0] = _val(val.writeMask)
        self._user_write_mask.__value[0] = _val(val.userWriteMask)
        self._is_abstract.__value[0] = _val(val.isAbstract)
        self._symmetric.__value[0] = _val(val.symmetric)
        self._inverse_name.__value[0] = _val(val.inverseName)

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def write_mask(self):
        return self._write_mask

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @property
    def is_abstract(self):
        return self._is_abstract

    @property
    def symmetric(self):
        return self._symmetric

    @property
    def inverse_name(self):
        return self._inverse_name

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val._value

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val._value

    @is_abstract.setter
    def is_abstract(self, val):
        self._is_abstract = val
        self._value.isAbstract = val._value

    @symmetric.setter
    def symmetric(self, val):
        self._symmetric = val
        self._value.symmetric = val._value

    @inverse_name.setter
    def inverse_name(self, val):
        self._inverse_name = val
        self._value.inverseName = val._value

    def __str__(self, n=0):
        return ("(UaReferenceTypeAttributes) :\n" +
                "\t" * (n + 1) + "specified_attributes" + self._specified_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "user_write_mask" + self._user_write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "is_abstract" + self._is_abstract.__str__(n + 1) +
                "\t" * (n + 1) + "symmetric" + self._symmetric.__str__(n + 1) +
                "\t" * (n + 1) + "inverse_name" + self._inverse_name.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaGetEndpointsRequest +++++++++++++++++++++++
class UaGetEndpointsRequest(UaType):
    def __init__(self, val=ffi.new("UA_GetEndpointsRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._endpoint_url = UaString(val=val.endpointUrl, is_pointer=False)
        self._locale_ids_size = SizeT(val=val.localeIdsSize, is_pointer=False)
        self._locale_ids = UaString(val=val.localeIds, is_pointer=True)
        self._profile_uris_size = SizeT(val=val.profileUrisSize, is_pointer=False)
        self._profile_uris = UaString(val=val.profileUris, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._endpoint_url.__value[0] = _val(val.endpointUrl)
        self._locale_ids_size.__value[0] = _val(val.localeIdsSize)
        self._locale_ids.__value = val.localeIds
        self._profile_uris_size.__value[0] = _val(val.profileUrisSize)
        self._profile_uris.__value = val.profileUris

    @property
    def request_header(self):
        return self._request_header

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @property
    def locale_ids_size(self):
        return self._locale_ids_size

    @property
    def locale_ids(self):
        return self._locale_ids

    @property
    def profile_uris_size(self):
        return self._profile_uris_size

    @property
    def profile_uris(self):
        return self._profile_uris

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @endpoint_url.setter
    def endpoint_url(self, val):
        self._endpoint_url = val
        self._value.endpointUrl = val._value

    @locale_ids_size.setter
    def locale_ids_size(self, val):
        self._locale_ids_size = val
        self._value.localeIdsSize = val._value

    @locale_ids.setter
    def locale_ids(self, val):
        self._locale_ids = val
        self._value.localeIds = val.__value

    @profile_uris_size.setter
    def profile_uris_size(self, val):
        self._profile_uris_size = val
        self._value.profileUrisSize = val._value

    @profile_uris.setter
    def profile_uris(self, val):
        self._profile_uris = val
        self._value.profileUris = val.__value

    def __str__(self, n=0):
        return ("(UaGetEndpointsRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "endpoint_url" + self._endpoint_url.__str__(n + 1) +
                "\t" * (n + 1) + "locale_ids_size" + self._locale_ids_size.__str__(n + 1) +
                "\t" * (n + 1) + "locale_ids" + self._locale_ids.__str__(n + 1) +
                "\t" * (n + 1) + "profile_uris_size" + self._profile_uris_size.__str__(n + 1) +
                "\t" * (n + 1) + "profile_uris" + self._profile_uris.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCloseSecureChannelResponse +++++++++++++++++++++++
class UaCloseSecureChannelResponse(UaType):
    def __init__(self, val=ffi.new("UA_CloseSecureChannelResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    def __str__(self, n=0):
        return ("(UaCloseSecureChannelResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaViewDescription +++++++++++++++++++++++
class UaViewDescription(UaType):
    def __init__(self, val=ffi.new("UA_ViewDescription*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._view_id = UaNodeId(val=val.viewId, is_pointer=False)
        self._timestamp = UaDateTime(val=val.timestamp, is_pointer=False)
        self._view_version = UaUInt32(val=val.viewVersion, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._view_id.__value[0] = _val(val.viewId)
        self._timestamp.__value[0] = _val(val.timestamp)
        self._view_version.__value[0] = _val(val.viewVersion)

    @property
    def view_id(self):
        return self._view_id

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def view_version(self):
        return self._view_version

    @view_id.setter
    def view_id(self, val):
        self._view_id = val
        self._value.viewId = val._value

    @timestamp.setter
    def timestamp(self, val):
        self._timestamp = val
        self._value.timestamp = val._value

    @view_version.setter
    def view_version(self, val):
        self._view_version = val
        self._value.viewVersion = val._value

    def __str__(self, n=0):
        return ("(UaViewDescription) :\n" +
                "\t" * (n + 1) + "view_id" + self._view_id.__str__(n + 1) +
                "\t" * (n + 1) + "timestamp" + self._timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "view_version" + self._view_version.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSetPublishingModeResponse +++++++++++++++++++++++
class UaSetPublishingModeResponse(UaType):
    def __init__(self, val=ffi.new("UA_SetPublishingModeResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaSetPublishingModeResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaStatusChangeNotification +++++++++++++++++++++++
class UaStatusChangeNotification(UaType):
    def __init__(self, val=ffi.new("UA_StatusChangeNotification*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._status = UaStatusCode(val=val.status, is_pointer=False)
        self._diagnostic_info = UaDiagnosticInfo(val=val.diagnosticInfo, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._status.__value[0] = _val(val.status)
        self._diagnostic_info.__value[0] = _val(val.diagnosticInfo)

    @property
    def status(self):
        return self._status

    @property
    def diagnostic_info(self):
        return self._diagnostic_info

    @status.setter
    def status(self, val):
        self._status = val
        self._value.status = val._value

    @diagnostic_info.setter
    def diagnostic_info(self, val):
        self._diagnostic_info = val
        self._value.diagnosticInfo = val._value

    def __str__(self, n=0):
        return ("(UaStatusChangeNotification) :\n" +
                "\t" * (n + 1) + "status" + self._status.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_info" + self._diagnostic_info.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaStructureField +++++++++++++++++++++++
class UaStructureField(UaType):
    def __init__(self, val=ffi.new("UA_StructureField*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._name = UaString(val=val.name, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._data_type = UaNodeId(val=val.dataType, is_pointer=False)
        self._value_rank = UaInt32(val=val.valueRank, is_pointer=False)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
        self._max_string_length = UaUInt32(val=val.maxStringLength, is_pointer=False)
        self._is_optional = UaBoolean(val=val.isOptional, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._name.__value[0] = _val(val.name)
        self._description.__value[0] = _val(val.description)
        self._data_type.__value[0] = _val(val.dataType)
        self._value_rank.__value[0] = _val(val.valueRank)
        self._array_dimensions_size.__value[0] = _val(val.arrayDimensionsSize)
        self._array_dimensions.__value = val.arrayDimensions
        self._max_string_length.__value[0] = _val(val.maxStringLength)
        self._is_optional.__value[0] = _val(val.isOptional)

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def data_type(self):
        return self._data_type

    @property
    def value_rank(self):
        return self._value_rank

    @property
    def array_dimensions_size(self):
        return self._array_dimensions_size

    @property
    def array_dimensions(self):
        return self._array_dimensions

    @property
    def max_string_length(self):
        return self._max_string_length

    @property
    def is_optional(self):
        return self._is_optional

    @name.setter
    def name(self, val):
        self._name = val
        self._value.name = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @data_type.setter
    def data_type(self, val):
        self._data_type = val
        self._value.dataType = val._value

    @value_rank.setter
    def value_rank(self, val):
        self._value_rank = val
        self._value.valueRank = val._value

    @array_dimensions_size.setter
    def array_dimensions_size(self, val):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._value

    @array_dimensions.setter
    def array_dimensions(self, val):
        self._array_dimensions = val
        self._value.arrayDimensions = val.__value

    @max_string_length.setter
    def max_string_length(self, val):
        self._max_string_length = val
        self._value.maxStringLength = val._value

    @is_optional.setter
    def is_optional(self, val):
        self._is_optional = val
        self._value.isOptional = val._value

    def __str__(self, n=0):
        return ("(UaStructureField) :\n" +
                "\t" * (n + 1) + "name" + self._name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "data_type" + self._data_type.__str__(n + 1) +
                "\t" * (n + 1) + "value_rank" + self._value_rank.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions_size" + self._array_dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions" + self._array_dimensions.__str__(n + 1) +
                "\t" * (n + 1) + "max_string_length" + self._max_string_length.__str__(n + 1) +
                "\t" * (n + 1) + "is_optional" + self._is_optional.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaEventFilterResult +++++++++++++++++++++++
class UaEventFilterResult(UaType):
    def __init__(self, val=ffi.new("UA_EventFilterResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._select_clause_results_size = SizeT(val=val.selectClauseResultsSize, is_pointer=False)
        self._select_clause_results = UaStatusCode(val=val.selectClauseResults, is_pointer=True)
        self._select_clause_diagnostic_infos_size = SizeT(val=val.selectClauseDiagnosticInfosSize, is_pointer=False)
        self._select_clause_diagnostic_infos = UaDiagnosticInfo(val=val.selectClauseDiagnosticInfos, is_pointer=True)
        self._where_clause_result = UaContentFilterResult(val=val.whereClauseResult, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._select_clause_results_size.__value[0] = _val(val.selectClauseResultsSize)
        self._select_clause_results.__value = val.selectClauseResults
        self._select_clause_diagnostic_infos_size.__value[0] = _val(val.selectClauseDiagnosticInfosSize)
        self._select_clause_diagnostic_infos.__value = val.selectClauseDiagnosticInfos
        self._where_clause_result.__value[0] = _val(val.whereClauseResult)

    @property
    def select_clause_results_size(self):
        return self._select_clause_results_size

    @property
    def select_clause_results(self):
        return self._select_clause_results

    @property
    def select_clause_diagnostic_infos_size(self):
        return self._select_clause_diagnostic_infos_size

    @property
    def select_clause_diagnostic_infos(self):
        return self._select_clause_diagnostic_infos

    @property
    def where_clause_result(self):
        return self._where_clause_result

    @select_clause_results_size.setter
    def select_clause_results_size(self, val):
        self._select_clause_results_size = val
        self._value.selectClauseResultsSize = val._value

    @select_clause_results.setter
    def select_clause_results(self, val):
        self._select_clause_results = val
        self._value.selectClauseResults = val.__value

    @select_clause_diagnostic_infos_size.setter
    def select_clause_diagnostic_infos_size(self, val):
        self._select_clause_diagnostic_infos_size = val
        self._value.selectClauseDiagnosticInfosSize = val._value

    @select_clause_diagnostic_infos.setter
    def select_clause_diagnostic_infos(self, val):
        self._select_clause_diagnostic_infos = val
        self._value.selectClauseDiagnosticInfos = val.__value

    @where_clause_result.setter
    def where_clause_result(self, val):
        self._where_clause_result = val
        self._value.whereClauseResult = val._value

    def __str__(self, n=0):
        return ("(UaEventFilterResult) :\n" +
                "\t" * (n + 1) + "select_clause_results_size" + self._select_clause_results_size.__str__(n + 1) +
                "\t" * (n + 1) + "select_clause_results" + self._select_clause_results.__str__(n + 1) +
                "\t" * (
                            n + 1) + "select_clause_diagnostic_infos_size" + self._select_clause_diagnostic_infos_size.__str__(
                    n + 1) +
                "\t" * (n + 1) + "select_clause_diagnostic_infos" + self._select_clause_diagnostic_infos.__str__(
                    n + 1) +
                "\t" * (n + 1) + "where_clause_result" + self._where_clause_result.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaMonitoredItemCreateRequest +++++++++++++++++++++++
class UaMonitoredItemCreateRequest(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemCreateRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._item_to_monitor = UaReadValueId(val=val.itemToMonitor, is_pointer=False)
        self._monitoring_mode = UaMonitoringMode(val=val.monitoringMode, is_pointer=False)
        self._requested_parameters = UaMonitoringParameters(val=val.requestedParameters, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._item_to_monitor.__value[0] = _val(val.itemToMonitor)
        self._monitoring_mode.__value[0] = _val(val.monitoringMode)
        self._requested_parameters.__value[0] = _val(val.requestedParameters)

    @property
    def item_to_monitor(self):
        return self._item_to_monitor

    @property
    def monitoring_mode(self):
        return self._monitoring_mode

    @property
    def requested_parameters(self):
        return self._requested_parameters

    @item_to_monitor.setter
    def item_to_monitor(self, val):
        self._item_to_monitor = val
        self._value.itemToMonitor = val._value

    @monitoring_mode.setter
    def monitoring_mode(self, val):
        self._monitoring_mode = val
        self._value.monitoringMode = val._value

    @requested_parameters.setter
    def requested_parameters(self, val):
        self._requested_parameters = val
        self._value.requestedParameters = val._value

    def __str__(self, n=0):
        return ("(UaMonitoredItemCreateRequest) :\n" +
                "\t" * (n + 1) + "item_to_monitor" + self._item_to_monitor.__str__(n + 1) +
                "\t" * (n + 1) + "monitoring_mode" + self._monitoring_mode.__str__(n + 1) +
                "\t" * (n + 1) + "requested_parameters" + self._requested_parameters.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaComplexNumberType +++++++++++++++++++++++
class UaComplexNumberType(UaType):
    def __init__(self, val=ffi.new("UA_ComplexNumberType*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._real = UaFloat(val=val.real, is_pointer=False)
        self._imaginary = UaFloat(val=val.imaginary, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._real.__value[0] = _val(val.real)
        self._imaginary.__value[0] = _val(val.imaginary)

    @property
    def real(self):
        return self._real

    @property
    def imaginary(self):
        return self._imaginary

    @real.setter
    def real(self, val):
        self._real = val
        self._value.real = val._value

    @imaginary.setter
    def imaginary(self, val):
        self._imaginary = val
        self._value.imaginary = val._value

    def __str__(self, n=0):
        return ("(UaComplexNumberType) :\n" +
                "\t" * (n + 1) + "real" + self._real.__str__(n + 1) +
                "\t" * (n + 1) + "imaginary" + self._imaginary.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaRange +++++++++++++++++++++++
class UaRange(UaType):
    def __init__(self, val=ffi.new("UA_Range*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._low = UaDouble(val=val.low, is_pointer=False)
        self._high = UaDouble(val=val.high, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._low.__value[0] = _val(val.low)
        self._high.__value[0] = _val(val.high)

    @property
    def low(self):
        return self._low

    @property
    def high(self):
        return self._high

    @low.setter
    def low(self, val):
        self._low = val
        self._value.low = val._value

    @high.setter
    def high(self, val):
        self._high = val
        self._value.high = val._value

    def __str__(self, n=0):
        return ("(UaRange) :\n" +
                "\t" * (n + 1) + "low" + self._low.__str__(n + 1) +
                "\t" * (n + 1) + "high" + self._high.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDataChangeNotification +++++++++++++++++++++++
class UaDataChangeNotification(UaType):
    def __init__(self, val=ffi.new("UA_DataChangeNotification*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._monitored_items_size = SizeT(val=val.monitoredItemsSize, is_pointer=False)
        self._monitored_items = UaMonitoredItemNotification(val=val.monitoredItems, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._monitored_items_size.__value[0] = _val(val.monitoredItemsSize)
        self._monitored_items.__value = val.monitoredItems
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def monitored_items_size(self):
        return self._monitored_items_size

    @property
    def monitored_items(self):
        return self._monitored_items

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @monitored_items_size.setter
    def monitored_items_size(self, val):
        self._monitored_items_size = val
        self._value.monitoredItemsSize = val._value

    @monitored_items.setter
    def monitored_items(self, val):
        self._monitored_items = val
        self._value.monitoredItems = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaDataChangeNotification) :\n" +
                "\t" * (n + 1) + "monitored_items_size" + self._monitored_items_size.__str__(n + 1) +
                "\t" * (n + 1) + "monitored_items" + self._monitored_items.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaArgument +++++++++++++++++++++++
class UaArgument(UaType):
    def __init__(self, val=ffi.new("UA_Argument*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._name = UaString(val=val.name, is_pointer=False)
        self._data_type = UaNodeId(val=val.dataType, is_pointer=False)
        self._value_rank = UaInt32(val=val.valueRank, is_pointer=False)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._name.__value[0] = _val(val.name)
        self._data_type.__value[0] = _val(val.dataType)
        self._value_rank.__value[0] = _val(val.valueRank)
        self._array_dimensions_size.__value[0] = _val(val.arrayDimensionsSize)
        self._array_dimensions.__value = val.arrayDimensions
        self._description.__value[0] = _val(val.description)

    @property
    def name(self):
        return self._name

    @property
    def data_type(self):
        return self._data_type

    @property
    def value_rank(self):
        return self._value_rank

    @property
    def array_dimensions_size(self):
        return self._array_dimensions_size

    @property
    def array_dimensions(self):
        return self._array_dimensions

    @property
    def description(self):
        return self._description

    @name.setter
    def name(self, val):
        self._name = val
        self._value.name = val._value

    @data_type.setter
    def data_type(self, val):
        self._data_type = val
        self._value.dataType = val._value

    @value_rank.setter
    def value_rank(self, val):
        self._value_rank = val
        self._value.valueRank = val._value

    @array_dimensions_size.setter
    def array_dimensions_size(self, val):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._value

    @array_dimensions.setter
    def array_dimensions(self, val):
        self._array_dimensions = val
        self._value.arrayDimensions = val.__value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    def __str__(self, n=0):
        return ("(UaArgument) :\n" +
                "\t" * (n + 1) + "name" + self._name.__str__(n + 1) +
                "\t" * (n + 1) + "data_type" + self._data_type.__str__(n + 1) +
                "\t" * (n + 1) + "value_rank" + self._value_rank.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions_size" + self._array_dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions" + self._array_dimensions.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaTransferSubscriptionsRequest +++++++++++++++++++++++
class UaTransferSubscriptionsRequest(UaType):
    def __init__(self, val=ffi.new("UA_TransferSubscriptionsRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_ids_size = SizeT(val=val.subscriptionIdsSize, is_pointer=False)
        self._subscription_ids = UaUInt32(val=val.subscriptionIds, is_pointer=True)
        self._send_initial_values = UaBoolean(val=val.sendInitialValues, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_ids_size.__value[0] = _val(val.subscriptionIdsSize)
        self._subscription_ids.__value = val.subscriptionIds
        self._send_initial_values.__value[0] = _val(val.sendInitialValues)

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_ids_size(self):
        return self._subscription_ids_size

    @property
    def subscription_ids(self):
        return self._subscription_ids

    @property
    def send_initial_values(self):
        return self._send_initial_values

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_ids_size.setter
    def subscription_ids_size(self, val):
        self._subscription_ids_size = val
        self._value.subscriptionIdsSize = val._value

    @subscription_ids.setter
    def subscription_ids(self, val):
        self._subscription_ids = val
        self._value.subscriptionIds = val.__value

    @send_initial_values.setter
    def send_initial_values(self, val):
        self._send_initial_values = val
        self._value.sendInitialValues = val._value

    def __str__(self, n=0):
        return ("(UaTransferSubscriptionsRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_ids_size" + self._subscription_ids_size.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_ids" + self._subscription_ids.__str__(n + 1) +
                "\t" * (n + 1) + "send_initial_values" + self._send_initial_values.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaChannelSecurityToken +++++++++++++++++++++++
class UaChannelSecurityToken(UaType):
    def __init__(self, val=ffi.new("UA_ChannelSecurityToken*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._channel_id = UaUInt32(val=val.channelId, is_pointer=False)
        self._token_id = UaUInt32(val=val.tokenId, is_pointer=False)
        self._created_at = UaDateTime(val=val.createdAt, is_pointer=False)
        self._revised_lifetime = UaUInt32(val=val.revisedLifetime, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._channel_id.__value[0] = _val(val.channelId)
        self._token_id.__value[0] = _val(val.tokenId)
        self._created_at.__value[0] = _val(val.createdAt)
        self._revised_lifetime.__value[0] = _val(val.revisedLifetime)

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def token_id(self):
        return self._token_id

    @property
    def created_at(self):
        return self._created_at

    @property
    def revised_lifetime(self):
        return self._revised_lifetime

    @channel_id.setter
    def channel_id(self, val):
        self._channel_id = val
        self._value.channelId = val._value

    @token_id.setter
    def token_id(self, val):
        self._token_id = val
        self._value.tokenId = val._value

    @created_at.setter
    def created_at(self, val):
        self._created_at = val
        self._value.createdAt = val._value

    @revised_lifetime.setter
    def revised_lifetime(self, val):
        self._revised_lifetime = val
        self._value.revisedLifetime = val._value

    def __str__(self, n=0):
        return ("(UaChannelSecurityToken) :\n" +
                "\t" * (n + 1) + "channel_id" + self._channel_id.__str__(n + 1) +
                "\t" * (n + 1) + "token_id" + self._token_id.__str__(n + 1) +
                "\t" * (n + 1) + "created_at" + self._created_at.__str__(n + 1) +
                "\t" * (n + 1) + "revised_lifetime" + self._revised_lifetime.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaEventNotificationList +++++++++++++++++++++++
class UaEventNotificationList(UaType):
    def __init__(self, val=ffi.new("UA_EventNotificationList*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._events_size = SizeT(val=val.eventsSize, is_pointer=False)
        self._events = UaEventFieldList(val=val.events, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._events_size.__value[0] = _val(val.eventsSize)
        self._events.__value = val.events

    @property
    def events_size(self):
        return self._events_size

    @property
    def events(self):
        return self._events

    @events_size.setter
    def events_size(self, val):
        self._events_size = val
        self._value.eventsSize = val._value

    @events.setter
    def events(self, val):
        self._events = val
        self._value.events = val.__value

    def __str__(self, n=0):
        return ("(UaEventNotificationList) :\n" +
                "\t" * (n + 1) + "events_size" + self._events_size.__str__(n + 1) +
                "\t" * (n + 1) + "events" + self._events.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAnonymousIdentityToken +++++++++++++++++++++++
class UaAnonymousIdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_AnonymousIdentityToken*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._policy_id = UaString(val=val.policyId, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._policy_id.__value[0] = _val(val.policyId)

    @property
    def policy_id(self):
        return self._policy_id

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val._value

    def __str__(self, n=0):
        return ("(UaAnonymousIdentityToken) :\n" +
                "\t" * (n + 1) + "policy_id" + self._policy_id.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAggregateFilter +++++++++++++++++++++++
class UaAggregateFilter(UaType):
    def __init__(self, val=ffi.new("UA_AggregateFilter*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._start_time = UaDateTime(val=val.startTime, is_pointer=False)
        self._aggregate_type = UaNodeId(val=val.aggregateType, is_pointer=False)
        self._processing_interval = UaDouble(val=val.processingInterval, is_pointer=False)
        self._aggregate_configuration = UaAggregateConfiguration(val=val.aggregateConfiguration, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._start_time.__value[0] = _val(val.startTime)
        self._aggregate_type.__value[0] = _val(val.aggregateType)
        self._processing_interval.__value[0] = _val(val.processingInterval)
        self._aggregate_configuration.__value[0] = _val(val.aggregateConfiguration)

    @property
    def start_time(self):
        return self._start_time

    @property
    def aggregate_type(self):
        return self._aggregate_type

    @property
    def processing_interval(self):
        return self._processing_interval

    @property
    def aggregate_configuration(self):
        return self._aggregate_configuration

    @start_time.setter
    def start_time(self, val):
        self._start_time = val
        self._value.startTime = val._value

    @aggregate_type.setter
    def aggregate_type(self, val):
        self._aggregate_type = val
        self._value.aggregateType = val._value

    @processing_interval.setter
    def processing_interval(self, val):
        self._processing_interval = val
        self._value.processingInterval = val._value

    @aggregate_configuration.setter
    def aggregate_configuration(self, val):
        self._aggregate_configuration = val
        self._value.aggregateConfiguration = val._value

    def __str__(self, n=0):
        return ("(UaAggregateFilter) :\n" +
                "\t" * (n + 1) + "start_time" + self._start_time.__str__(n + 1) +
                "\t" * (n + 1) + "aggregate_type" + self._aggregate_type.__str__(n + 1) +
                "\t" * (n + 1) + "processing_interval" + self._processing_interval.__str__(n + 1) +
                "\t" * (n + 1) + "aggregate_configuration" + self._aggregate_configuration.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaRepublishResponse +++++++++++++++++++++++
class UaRepublishResponse(UaType):
    def __init__(self, val=ffi.new("UA_RepublishResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._notification_message = UaNotificationMessage(val=val.notificationMessage, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._notification_message.__value[0] = _val(val.notificationMessage)

    @property
    def response_header(self):
        return self._response_header

    @property
    def notification_message(self):
        return self._notification_message

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @notification_message.setter
    def notification_message(self, val):
        self._notification_message = val
        self._value.notificationMessage = val._value

    def __str__(self, n=0):
        return ("(UaRepublishResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "notification_message" + self._notification_message.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteSubscriptionsResponse +++++++++++++++++++++++
class UaDeleteSubscriptionsResponse(UaType):
    def __init__(self, val=ffi.new("UA_DeleteSubscriptionsResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaDeleteSubscriptionsResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaRegisterNodesRequest +++++++++++++++++++++++
class UaRegisterNodesRequest(UaType):
    def __init__(self, val=ffi.new("UA_RegisterNodesRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._nodes_to_register_size = SizeT(val=val.nodesToRegisterSize, is_pointer=False)
        self._nodes_to_register = UaNodeId(val=val.nodesToRegister, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._nodes_to_register_size.__value[0] = _val(val.nodesToRegisterSize)
        self._nodes_to_register.__value = val.nodesToRegister

    @property
    def request_header(self):
        return self._request_header

    @property
    def nodes_to_register_size(self):
        return self._nodes_to_register_size

    @property
    def nodes_to_register(self):
        return self._nodes_to_register

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @nodes_to_register_size.setter
    def nodes_to_register_size(self, val):
        self._nodes_to_register_size = val
        self._value.nodesToRegisterSize = val._value

    @nodes_to_register.setter
    def nodes_to_register(self, val):
        self._nodes_to_register = val
        self._value.nodesToRegister = val.__value

    def __str__(self, n=0):
        return ("(UaRegisterNodesRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_register_size" + self._nodes_to_register_size.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_register" + self._nodes_to_register.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaStructureDefinition +++++++++++++++++++++++
class UaStructureDefinition(UaType):
    def __init__(self, val=ffi.new("UA_StructureDefinition*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._default_encoding_id = UaNodeId(val=val.defaultEncodingId, is_pointer=False)
        self._base_data_type = UaNodeId(val=val.baseDataType, is_pointer=False)
        self._structure_type = UaStructureType(val=val.structureType, is_pointer=False)
        self._fields_size = SizeT(val=val.fieldsSize, is_pointer=False)
        self._fields = UaStructureField(val=val.fields, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._default_encoding_id.__value[0] = _val(val.defaultEncodingId)
        self._base_data_type.__value[0] = _val(val.baseDataType)
        self._structure_type.__value[0] = _val(val.structureType)
        self._fields_size.__value[0] = _val(val.fieldsSize)
        self._fields.__value = val.fields

    @property
    def default_encoding_id(self):
        return self._default_encoding_id

    @property
    def base_data_type(self):
        return self._base_data_type

    @property
    def structure_type(self):
        return self._structure_type

    @property
    def fields_size(self):
        return self._fields_size

    @property
    def fields(self):
        return self._fields

    @default_encoding_id.setter
    def default_encoding_id(self, val):
        self._default_encoding_id = val
        self._value.defaultEncodingId = val._value

    @base_data_type.setter
    def base_data_type(self, val):
        self._base_data_type = val
        self._value.baseDataType = val._value

    @structure_type.setter
    def structure_type(self, val):
        self._structure_type = val
        self._value.structureType = val._value

    @fields_size.setter
    def fields_size(self, val):
        self._fields_size = val
        self._value.fieldsSize = val._value

    @fields.setter
    def fields(self, val):
        self._fields = val
        self._value.fields = val.__value

    def __str__(self, n=0):
        return ("(UaStructureDefinition) :\n" +
                "\t" * (n + 1) + "default_encoding_id" + self._default_encoding_id.__str__(n + 1) +
                "\t" * (n + 1) + "base_data_type" + self._base_data_type.__str__(n + 1) +
                "\t" * (n + 1) + "structure_type" + self._structure_type.__str__(n + 1) +
                "\t" * (n + 1) + "fields_size" + self._fields_size.__str__(n + 1) +
                "\t" * (n + 1) + "fields" + self._fields.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaMethodAttributes +++++++++++++++++++++++
class UaMethodAttributes(UaType):
    def __init__(self, val=ffi.new("UA_MethodAttributes*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
        self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
        self._executable = UaBoolean(val=val.executable, is_pointer=False)
        self._user_executable = UaBoolean(val=val.userExecutable, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._specified_attributes.__value[0] = _val(val.specifiedAttributes)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._write_mask.__value[0] = _val(val.writeMask)
        self._user_write_mask.__value[0] = _val(val.userWriteMask)
        self._executable.__value[0] = _val(val.executable)
        self._user_executable.__value[0] = _val(val.userExecutable)

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def write_mask(self):
        return self._write_mask

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @property
    def executable(self):
        return self._executable

    @property
    def user_executable(self):
        return self._user_executable

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val._value

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val._value

    @executable.setter
    def executable(self, val):
        self._executable = val
        self._value.executable = val._value

    @user_executable.setter
    def user_executable(self, val):
        self._user_executable = val
        self._value.userExecutable = val._value

    def __str__(self, n=0):
        return ("(UaMethodAttributes) :\n" +
                "\t" * (n + 1) + "specified_attributes" + self._specified_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "user_write_mask" + self._user_write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "executable" + self._executable.__str__(n + 1) +
                "\t" * (n + 1) + "user_executable" + self._user_executable.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaUserNameIdentityToken +++++++++++++++++++++++
class UaUserNameIdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_UserNameIdentityToken*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._policy_id = UaString(val=val.policyId, is_pointer=False)
        self._user_name = UaString(val=val.userName, is_pointer=False)
        self._password = UaByteString(val=val.password, is_pointer=False)
        self._encryption_algorithm = UaString(val=val.encryptionAlgorithm, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._policy_id.__value[0] = _val(val.policyId)
        self._user_name.__value[0] = _val(val.userName)
        self._password.__value[0] = _val(val.password)
        self._encryption_algorithm.__value[0] = _val(val.encryptionAlgorithm)

    @property
    def policy_id(self):
        return self._policy_id

    @property
    def user_name(self):
        return self._user_name

    @property
    def password(self):
        return self._password

    @property
    def encryption_algorithm(self):
        return self._encryption_algorithm

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val._value

    @user_name.setter
    def user_name(self, val):
        self._user_name = val
        self._value.userName = val._value

    @password.setter
    def password(self, val):
        self._password = val
        self._value.password = val._value

    @encryption_algorithm.setter
    def encryption_algorithm(self, val):
        self._encryption_algorithm = val
        self._value.encryptionAlgorithm = val._value

    def __str__(self, n=0):
        return ("(UaUserNameIdentityToken) :\n" +
                "\t" * (n + 1) + "policy_id" + self._policy_id.__str__(n + 1) +
                "\t" * (n + 1) + "user_name" + self._user_name.__str__(n + 1) +
                "\t" * (n + 1) + "password" + self._password.__str__(n + 1) +
                "\t" * (n + 1) + "encryption_algorithm" + self._encryption_algorithm.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaUnregisterNodesRequest +++++++++++++++++++++++
class UaUnregisterNodesRequest(UaType):
    def __init__(self, val=ffi.new("UA_UnregisterNodesRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._nodes_to_unregister_size = SizeT(val=val.nodesToUnregisterSize, is_pointer=False)
        self._nodes_to_unregister = UaNodeId(val=val.nodesToUnregister, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._nodes_to_unregister_size.__value[0] = _val(val.nodesToUnregisterSize)
        self._nodes_to_unregister.__value = val.nodesToUnregister

    @property
    def request_header(self):
        return self._request_header

    @property
    def nodes_to_unregister_size(self):
        return self._nodes_to_unregister_size

    @property
    def nodes_to_unregister(self):
        return self._nodes_to_unregister

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @nodes_to_unregister_size.setter
    def nodes_to_unregister_size(self, val):
        self._nodes_to_unregister_size = val
        self._value.nodesToUnregisterSize = val._value

    @nodes_to_unregister.setter
    def nodes_to_unregister(self, val):
        self._nodes_to_unregister = val
        self._value.nodesToUnregister = val.__value

    def __str__(self, n=0):
        return ("(UaUnregisterNodesRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_unregister_size" + self._nodes_to_unregister_size.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_unregister" + self._nodes_to_unregister.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaOpenSecureChannelResponse +++++++++++++++++++++++
class UaOpenSecureChannelResponse(UaType):
    def __init__(self, val=ffi.new("UA_OpenSecureChannelResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._server_protocol_version = UaUInt32(val=val.serverProtocolVersion, is_pointer=False)
        self._security_token = UaChannelSecurityToken(val=val.securityToken, is_pointer=False)
        self._server_nonce = UaByteString(val=val.serverNonce, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._server_protocol_version.__value[0] = _val(val.serverProtocolVersion)
        self._security_token.__value[0] = _val(val.securityToken)
        self._server_nonce.__value[0] = _val(val.serverNonce)

    @property
    def response_header(self):
        return self._response_header

    @property
    def server_protocol_version(self):
        return self._server_protocol_version

    @property
    def security_token(self):
        return self._security_token

    @property
    def server_nonce(self):
        return self._server_nonce

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @server_protocol_version.setter
    def server_protocol_version(self, val):
        self._server_protocol_version = val
        self._value.serverProtocolVersion = val._value

    @security_token.setter
    def security_token(self, val):
        self._security_token = val
        self._value.securityToken = val._value

    @server_nonce.setter
    def server_nonce(self, val):
        self._server_nonce = val
        self._value.serverNonce = val._value

    def __str__(self, n=0):
        return ("(UaOpenSecureChannelResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "server_protocol_version" + self._server_protocol_version.__str__(n + 1) +
                "\t" * (n + 1) + "security_token" + self._security_token.__str__(n + 1) +
                "\t" * (n + 1) + "server_nonce" + self._server_nonce.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSetTriggeringResponse +++++++++++++++++++++++
class UaSetTriggeringResponse(UaType):
    def __init__(self, val=ffi.new("UA_SetTriggeringResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._add_results_size = SizeT(val=val.addResultsSize, is_pointer=False)
        self._add_results = UaStatusCode(val=val.addResults, is_pointer=True)
        self._add_diagnostic_infos_size = SizeT(val=val.addDiagnosticInfosSize, is_pointer=False)
        self._add_diagnostic_infos = UaDiagnosticInfo(val=val.addDiagnosticInfos, is_pointer=True)
        self._remove_results_size = SizeT(val=val.removeResultsSize, is_pointer=False)
        self._remove_results = UaStatusCode(val=val.removeResults, is_pointer=True)
        self._remove_diagnostic_infos_size = SizeT(val=val.removeDiagnosticInfosSize, is_pointer=False)
        self._remove_diagnostic_infos = UaDiagnosticInfo(val=val.removeDiagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._add_results_size.__value[0] = _val(val.addResultsSize)
        self._add_results.__value = val.addResults
        self._add_diagnostic_infos_size.__value[0] = _val(val.addDiagnosticInfosSize)
        self._add_diagnostic_infos.__value = val.addDiagnosticInfos
        self._remove_results_size.__value[0] = _val(val.removeResultsSize)
        self._remove_results.__value = val.removeResults
        self._remove_diagnostic_infos_size.__value[0] = _val(val.removeDiagnosticInfosSize)
        self._remove_diagnostic_infos.__value = val.removeDiagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def add_results_size(self):
        return self._add_results_size

    @property
    def add_results(self):
        return self._add_results

    @property
    def add_diagnostic_infos_size(self):
        return self._add_diagnostic_infos_size

    @property
    def add_diagnostic_infos(self):
        return self._add_diagnostic_infos

    @property
    def remove_results_size(self):
        return self._remove_results_size

    @property
    def remove_results(self):
        return self._remove_results

    @property
    def remove_diagnostic_infos_size(self):
        return self._remove_diagnostic_infos_size

    @property
    def remove_diagnostic_infos(self):
        return self._remove_diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @add_results_size.setter
    def add_results_size(self, val):
        self._add_results_size = val
        self._value.addResultsSize = val._value

    @add_results.setter
    def add_results(self, val):
        self._add_results = val
        self._value.addResults = val.__value

    @add_diagnostic_infos_size.setter
    def add_diagnostic_infos_size(self, val):
        self._add_diagnostic_infos_size = val
        self._value.addDiagnosticInfosSize = val._value

    @add_diagnostic_infos.setter
    def add_diagnostic_infos(self, val):
        self._add_diagnostic_infos = val
        self._value.addDiagnosticInfos = val.__value

    @remove_results_size.setter
    def remove_results_size(self, val):
        self._remove_results_size = val
        self._value.removeResultsSize = val._value

    @remove_results.setter
    def remove_results(self, val):
        self._remove_results = val
        self._value.removeResults = val.__value

    @remove_diagnostic_infos_size.setter
    def remove_diagnostic_infos_size(self, val):
        self._remove_diagnostic_infos_size = val
        self._value.removeDiagnosticInfosSize = val._value

    @remove_diagnostic_infos.setter
    def remove_diagnostic_infos(self, val):
        self._remove_diagnostic_infos = val
        self._value.removeDiagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaSetTriggeringResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "add_results_size" + self._add_results_size.__str__(n + 1) +
                "\t" * (n + 1) + "add_results" + self._add_results.__str__(n + 1) +
                "\t" * (n + 1) + "add_diagnostic_infos_size" + self._add_diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "add_diagnostic_infos" + self._add_diagnostic_infos.__str__(n + 1) +
                "\t" * (n + 1) + "remove_results_size" + self._remove_results_size.__str__(n + 1) +
                "\t" * (n + 1) + "remove_results" + self._remove_results.__str__(n + 1) +
                "\t" * (n + 1) + "remove_diagnostic_infos_size" + self._remove_diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "remove_diagnostic_infos" + self._remove_diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSimpleAttributeOperand +++++++++++++++++++++++
class UaSimpleAttributeOperand(UaType):
    def __init__(self, val=ffi.new("UA_SimpleAttributeOperand*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._type_definition_id = UaNodeId(val=val.typeDefinitionId, is_pointer=False)
        self._browse_path_size = SizeT(val=val.browsePathSize, is_pointer=False)
        self._browse_path = UaQualifiedName(val=val.browsePath, is_pointer=True)
        self._attribute_id = UaUInt32(val=val.attributeId, is_pointer=False)
        self._index_range = UaString(val=val.indexRange, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._type_definition_id.__value[0] = _val(val.typeDefinitionId)
        self._browse_path_size.__value[0] = _val(val.browsePathSize)
        self._browse_path.__value = val.browsePath
        self._attribute_id.__value[0] = _val(val.attributeId)
        self._index_range.__value[0] = _val(val.indexRange)

    @property
    def type_definition_id(self):
        return self._type_definition_id

    @property
    def browse_path_size(self):
        return self._browse_path_size

    @property
    def browse_path(self):
        return self._browse_path

    @property
    def attribute_id(self):
        return self._attribute_id

    @property
    def index_range(self):
        return self._index_range

    @type_definition_id.setter
    def type_definition_id(self, val):
        self._type_definition_id = val
        self._value.typeDefinitionId = val._value

    @browse_path_size.setter
    def browse_path_size(self, val):
        self._browse_path_size = val
        self._value.browsePathSize = val._value

    @browse_path.setter
    def browse_path(self, val):
        self._browse_path = val
        self._value.browsePath = val.__value

    @attribute_id.setter
    def attribute_id(self, val):
        self._attribute_id = val
        self._value.attributeId = val._value

    @index_range.setter
    def index_range(self, val):
        self._index_range = val
        self._value.indexRange = val._value

    def __str__(self, n=0):
        return ("(UaSimpleAttributeOperand) :\n" +
                "\t" * (n + 1) + "type_definition_id" + self._type_definition_id.__str__(n + 1) +
                "\t" * (n + 1) + "browse_path_size" + self._browse_path_size.__str__(n + 1) +
                "\t" * (n + 1) + "browse_path" + self._browse_path.__str__(n + 1) +
                "\t" * (n + 1) + "attribute_id" + self._attribute_id.__str__(n + 1) +
                "\t" * (n + 1) + "index_range" + self._index_range.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaRepublishRequest +++++++++++++++++++++++
class UaRepublishRequest(UaType):
    def __init__(self, val=ffi.new("UA_RepublishRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._retransmit_sequence_number = UaUInt32(val=val.retransmitSequenceNumber, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._retransmit_sequence_number.__value[0] = _val(val.retransmitSequenceNumber)

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def retransmit_sequence_number(self):
        return self._retransmit_sequence_number

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @retransmit_sequence_number.setter
    def retransmit_sequence_number(self, val):
        self._retransmit_sequence_number = val
        self._value.retransmitSequenceNumber = val._value

    def __str__(self, n=0):
        return ("(UaRepublishRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "retransmit_sequence_number" + self._retransmit_sequence_number.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaRegisterNodesResponse +++++++++++++++++++++++
class UaRegisterNodesResponse(UaType):
    def __init__(self, val=ffi.new("UA_RegisterNodesResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._registered_node_ids_size = SizeT(val=val.registeredNodeIdsSize, is_pointer=False)
        self._registered_node_ids = UaNodeId(val=val.registeredNodeIds, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._registered_node_ids_size.__value[0] = _val(val.registeredNodeIdsSize)
        self._registered_node_ids.__value = val.registeredNodeIds

    @property
    def response_header(self):
        return self._response_header

    @property
    def registered_node_ids_size(self):
        return self._registered_node_ids_size

    @property
    def registered_node_ids(self):
        return self._registered_node_ids

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @registered_node_ids_size.setter
    def registered_node_ids_size(self, val):
        self._registered_node_ids_size = val
        self._value.registeredNodeIdsSize = val._value

    @registered_node_ids.setter
    def registered_node_ids(self, val):
        self._registered_node_ids = val
        self._value.registeredNodeIds = val.__value

    def __str__(self, n=0):
        return ("(UaRegisterNodesResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "registered_node_ids_size" + self._registered_node_ids_size.__str__(n + 1) +
                "\t" * (n + 1) + "registered_node_ids" + self._registered_node_ids.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaModifyMonitoredItemsResponse +++++++++++++++++++++++
class UaModifyMonitoredItemsResponse(UaType):
    def __init__(self, val=ffi.new("UA_ModifyMonitoredItemsResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaMonitoredItemModifyResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaModifyMonitoredItemsResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteSubscriptionsRequest +++++++++++++++++++++++
class UaDeleteSubscriptionsRequest(UaType):
    def __init__(self, val=ffi.new("UA_DeleteSubscriptionsRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_ids_size = SizeT(val=val.subscriptionIdsSize, is_pointer=False)
        self._subscription_ids = UaUInt32(val=val.subscriptionIds, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_ids_size.__value[0] = _val(val.subscriptionIdsSize)
        self._subscription_ids.__value = val.subscriptionIds

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_ids_size(self):
        return self._subscription_ids_size

    @property
    def subscription_ids(self):
        return self._subscription_ids

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_ids_size.setter
    def subscription_ids_size(self, val):
        self._subscription_ids_size = val
        self._value.subscriptionIdsSize = val._value

    @subscription_ids.setter
    def subscription_ids(self, val):
        self._subscription_ids = val
        self._value.subscriptionIds = val.__value

    def __str__(self, n=0):
        return ("(UaDeleteSubscriptionsRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_ids_size" + self._subscription_ids_size.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_ids" + self._subscription_ids.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBrowsePath +++++++++++++++++++++++
class UaBrowsePath(UaType):
    def __init__(self, val=ffi.new("UA_BrowsePath*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._starting_node = UaNodeId(val=val.startingNode, is_pointer=False)
        self._relative_path = UaRelativePath(val=val.relativePath, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._starting_node.__value[0] = _val(val.startingNode)
        self._relative_path.__value[0] = _val(val.relativePath)

    @property
    def starting_node(self):
        return self._starting_node

    @property
    def relative_path(self):
        return self._relative_path

    @starting_node.setter
    def starting_node(self, val):
        self._starting_node = val
        self._value.startingNode = val._value

    @relative_path.setter
    def relative_path(self, val):
        self._relative_path = val
        self._value.relativePath = val._value

    def __str__(self, n=0):
        return ("(UaBrowsePath) :\n" +
                "\t" * (n + 1) + "starting_node" + self._starting_node.__str__(n + 1) +
                "\t" * (n + 1) + "relative_path" + self._relative_path.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaObjectAttributes +++++++++++++++++++++++
class UaObjectAttributes(UaType):
    def __init__(self, val=ffi.new("UA_ObjectAttributes*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._description = UaLocalizedText(val=val.description, is_pointer=False)
        self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
        self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
        self._event_notifier = UaByte(val=val.eventNotifier, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._specified_attributes.__value[0] = _val(val.specifiedAttributes)
        self._display_name.__value[0] = _val(val.displayName)
        self._description.__value[0] = _val(val.description)
        self._write_mask.__value[0] = _val(val.writeMask)
        self._user_write_mask.__value[0] = _val(val.userWriteMask)
        self._event_notifier.__value[0] = _val(val.eventNotifier)

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def write_mask(self):
        return self._write_mask

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @property
    def event_notifier(self):
        return self._event_notifier

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val._value

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val._value

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val._value

    @event_notifier.setter
    def event_notifier(self, val):
        self._event_notifier = val
        self._value.eventNotifier = val._value

    def __str__(self, n=0):
        return ("(UaObjectAttributes) :\n" +
                "\t" * (n + 1) + "specified_attributes" + self._specified_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "description" + self._description.__str__(n + 1) +
                "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "user_write_mask" + self._user_write_mask.__str__(n + 1) +
                "\t" * (n + 1) + "event_notifier" + self._event_notifier.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaPublishRequest +++++++++++++++++++++++
class UaPublishRequest(UaType):
    def __init__(self, val=ffi.new("UA_PublishRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_acknowledgements_size = SizeT(val=val.subscriptionAcknowledgementsSize, is_pointer=False)
        self._subscription_acknowledgements = UaSubscriptionAcknowledgement(val=val.subscriptionAcknowledgements,
                                                                            is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_acknowledgements_size.__value[0] = _val(val.subscriptionAcknowledgementsSize)
        self._subscription_acknowledgements.__value = val.subscriptionAcknowledgements

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_acknowledgements_size(self):
        return self._subscription_acknowledgements_size

    @property
    def subscription_acknowledgements(self):
        return self._subscription_acknowledgements

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_acknowledgements_size.setter
    def subscription_acknowledgements_size(self, val):
        self._subscription_acknowledgements_size = val
        self._value.subscriptionAcknowledgementsSize = val._value

    @subscription_acknowledgements.setter
    def subscription_acknowledgements(self, val):
        self._subscription_acknowledgements = val
        self._value.subscriptionAcknowledgements = val.__value

    def __str__(self, n=0):
        return ("(UaPublishRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (
                            n + 1) + "subscription_acknowledgements_size" + self._subscription_acknowledgements_size.__str__(
                    n + 1) +
                "\t" * (n + 1) + "subscription_acknowledgements" + self._subscription_acknowledgements.__str__(
                    n + 1) + "\n")


# +++++++++++++++++++ UaFindServersRequest +++++++++++++++++++++++
class UaFindServersRequest(UaType):
    def __init__(self, val=ffi.new("UA_FindServersRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._endpoint_url = UaString(val=val.endpointUrl, is_pointer=False)
        self._locale_ids_size = SizeT(val=val.localeIdsSize, is_pointer=False)
        self._locale_ids = UaString(val=val.localeIds, is_pointer=True)
        self._server_uris_size = SizeT(val=val.serverUrisSize, is_pointer=False)
        self._server_uris = UaString(val=val.serverUris, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._endpoint_url.__value[0] = _val(val.endpointUrl)
        self._locale_ids_size.__value[0] = _val(val.localeIdsSize)
        self._locale_ids.__value = val.localeIds
        self._server_uris_size.__value[0] = _val(val.serverUrisSize)
        self._server_uris.__value = val.serverUris

    @property
    def request_header(self):
        return self._request_header

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @property
    def locale_ids_size(self):
        return self._locale_ids_size

    @property
    def locale_ids(self):
        return self._locale_ids

    @property
    def server_uris_size(self):
        return self._server_uris_size

    @property
    def server_uris(self):
        return self._server_uris

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @endpoint_url.setter
    def endpoint_url(self, val):
        self._endpoint_url = val
        self._value.endpointUrl = val._value

    @locale_ids_size.setter
    def locale_ids_size(self, val):
        self._locale_ids_size = val
        self._value.localeIdsSize = val._value

    @locale_ids.setter
    def locale_ids(self, val):
        self._locale_ids = val
        self._value.localeIds = val.__value

    @server_uris_size.setter
    def server_uris_size(self, val):
        self._server_uris_size = val
        self._value.serverUrisSize = val._value

    @server_uris.setter
    def server_uris(self, val):
        self._server_uris = val
        self._value.serverUris = val.__value

    def __str__(self, n=0):
        return ("(UaFindServersRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "endpoint_url" + self._endpoint_url.__str__(n + 1) +
                "\t" * (n + 1) + "locale_ids_size" + self._locale_ids_size.__str__(n + 1) +
                "\t" * (n + 1) + "locale_ids" + self._locale_ids.__str__(n + 1) +
                "\t" * (n + 1) + "server_uris_size" + self._server_uris_size.__str__(n + 1) +
                "\t" * (n + 1) + "server_uris" + self._server_uris.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaReferenceDescription +++++++++++++++++++++++
class UaReferenceDescription(UaType):
    def __init__(self, val=ffi.new("UA_ReferenceDescription*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
        self._is_forward = UaBoolean(val=val.isForward, is_pointer=False)
        self._node_id = UaExpandedNodeId(val=val.nodeId, is_pointer=False)
        self._browse_name = UaQualifiedName(val=val.browseName, is_pointer=False)
        self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
        self._node_class = UaNodeClass(val=val.nodeClass, is_pointer=False)
        self._type_definition = UaExpandedNodeId(val=val.typeDefinition, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._reference_type_id.__value[0] = _val(val.referenceTypeId)
        self._is_forward.__value[0] = _val(val.isForward)
        self._node_id.__value[0] = _val(val.nodeId)
        self._browse_name.__value[0] = _val(val.browseName)
        self._display_name.__value[0] = _val(val.displayName)
        self._node_class.__value[0] = _val(val.nodeClass)
        self._type_definition.__value[0] = _val(val.typeDefinition)

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @property
    def is_forward(self):
        return self._is_forward

    @property
    def node_id(self):
        return self._node_id

    @property
    def browse_name(self):
        return self._browse_name

    @property
    def display_name(self):
        return self._display_name

    @property
    def node_class(self):
        return self._node_class

    @property
    def type_definition(self):
        return self._type_definition

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val._value

    @is_forward.setter
    def is_forward(self, val):
        self._is_forward = val
        self._value.isForward = val._value

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val._value

    @browse_name.setter
    def browse_name(self, val):
        self._browse_name = val
        self._value.browseName = val._value

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val._value

    @node_class.setter
    def node_class(self, val):
        self._node_class = val
        self._value.nodeClass = val._value

    @type_definition.setter
    def type_definition(self, val):
        self._type_definition = val
        self._value.typeDefinition = val._value

    def __str__(self, n=0):
        return ("(UaReferenceDescription) :\n" +
                "\t" * (n + 1) + "reference_type_id" + self._reference_type_id.__str__(n + 1) +
                "\t" * (n + 1) + "is_forward" + self._is_forward.__str__(n + 1) +
                "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1) +
                "\t" * (n + 1) + "browse_name" + self._browse_name.__str__(n + 1) +
                "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1) +
                "\t" * (n + 1) + "node_class" + self._node_class.__str__(n + 1) +
                "\t" * (n + 1) + "type_definition" + self._type_definition.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCreateSubscriptionRequest +++++++++++++++++++++++
class UaCreateSubscriptionRequest(UaType):
    def __init__(self, val=ffi.new("UA_CreateSubscriptionRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._requested_publishing_interval = UaDouble(val=val.requestedPublishingInterval, is_pointer=False)
        self._requested_lifetime_count = UaUInt32(val=val.requestedLifetimeCount, is_pointer=False)
        self._requested_max_keep_alive_count = UaUInt32(val=val.requestedMaxKeepAliveCount, is_pointer=False)
        self._max_notifications_per_publish = UaUInt32(val=val.maxNotificationsPerPublish, is_pointer=False)
        self._publishing_enabled = UaBoolean(val=val.publishingEnabled, is_pointer=False)
        self._priority = UaByte(val=val.priority, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._requested_publishing_interval.__value[0] = _val(val.requestedPublishingInterval)
        self._requested_lifetime_count.__value[0] = _val(val.requestedLifetimeCount)
        self._requested_max_keep_alive_count.__value[0] = _val(val.requestedMaxKeepAliveCount)
        self._max_notifications_per_publish.__value[0] = _val(val.maxNotificationsPerPublish)
        self._publishing_enabled.__value[0] = _val(val.publishingEnabled)
        self._priority.__value[0] = _val(val.priority)

    @property
    def request_header(self):
        return self._request_header

    @property
    def requested_publishing_interval(self):
        return self._requested_publishing_interval

    @property
    def requested_lifetime_count(self):
        return self._requested_lifetime_count

    @property
    def requested_max_keep_alive_count(self):
        return self._requested_max_keep_alive_count

    @property
    def max_notifications_per_publish(self):
        return self._max_notifications_per_publish

    @property
    def publishing_enabled(self):
        return self._publishing_enabled

    @property
    def priority(self):
        return self._priority

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @requested_publishing_interval.setter
    def requested_publishing_interval(self, val):
        self._requested_publishing_interval = val
        self._value.requestedPublishingInterval = val._value

    @requested_lifetime_count.setter
    def requested_lifetime_count(self, val):
        self._requested_lifetime_count = val
        self._value.requestedLifetimeCount = val._value

    @requested_max_keep_alive_count.setter
    def requested_max_keep_alive_count(self, val):
        self._requested_max_keep_alive_count = val
        self._value.requestedMaxKeepAliveCount = val._value

    @max_notifications_per_publish.setter
    def max_notifications_per_publish(self, val):
        self._max_notifications_per_publish = val
        self._value.maxNotificationsPerPublish = val._value

    @publishing_enabled.setter
    def publishing_enabled(self, val):
        self._publishing_enabled = val
        self._value.publishingEnabled = val._value

    @priority.setter
    def priority(self, val):
        self._priority = val
        self._value.priority = val._value

    def __str__(self, n=0):
        return ("(UaCreateSubscriptionRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "requested_publishing_interval" + self._requested_publishing_interval.__str__(n + 1) +
                "\t" * (n + 1) + "requested_lifetime_count" + self._requested_lifetime_count.__str__(n + 1) +
                "\t" * (n + 1) + "requested_max_keep_alive_count" + self._requested_max_keep_alive_count.__str__(
                    n + 1) +
                "\t" * (n + 1) + "max_notifications_per_publish" + self._max_notifications_per_publish.__str__(n + 1) +
                "\t" * (n + 1) + "publishing_enabled" + self._publishing_enabled.__str__(n + 1) +
                "\t" * (n + 1) + "priority" + self._priority.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCallResponse +++++++++++++++++++++++
class UaCallResponse(UaType):
    def __init__(self, val=ffi.new("UA_CallResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaCallMethodResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaCallResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteNodesResponse +++++++++++++++++++++++
class UaDeleteNodesResponse(UaType):
    def __init__(self, val=ffi.new("UA_DeleteNodesResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaDeleteNodesResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaModifyMonitoredItemsRequest +++++++++++++++++++++++
class UaModifyMonitoredItemsRequest(UaType):
    def __init__(self, val=ffi.new("UA_ModifyMonitoredItemsRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._timestamps_to_return = UaTimestampsToReturn(val=val.timestampsToReturn, is_pointer=False)
        self._items_to_modify_size = SizeT(val=val.itemsToModifySize, is_pointer=False)
        self._items_to_modify = UaMonitoredItemModifyRequest(val=val.itemsToModify, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._timestamps_to_return.__value[0] = _val(val.timestampsToReturn)
        self._items_to_modify_size.__value[0] = _val(val.itemsToModifySize)
        self._items_to_modify.__value = val.itemsToModify

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def timestamps_to_return(self):
        return self._timestamps_to_return

    @property
    def items_to_modify_size(self):
        return self._items_to_modify_size

    @property
    def items_to_modify(self):
        return self._items_to_modify

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @timestamps_to_return.setter
    def timestamps_to_return(self, val):
        self._timestamps_to_return = val
        self._value.timestampsToReturn = val._value

    @items_to_modify_size.setter
    def items_to_modify_size(self, val):
        self._items_to_modify_size = val
        self._value.itemsToModifySize = val._value

    @items_to_modify.setter
    def items_to_modify(self, val):
        self._items_to_modify = val
        self._value.itemsToModify = val.__value

    def __str__(self, n=0):
        return ("(UaModifyMonitoredItemsRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "timestamps_to_return" + self._timestamps_to_return.__str__(n + 1) +
                "\t" * (n + 1) + "items_to_modify_size" + self._items_to_modify_size.__str__(n + 1) +
                "\t" * (n + 1) + "items_to_modify" + self._items_to_modify.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaServiceFault +++++++++++++++++++++++
class UaServiceFault(UaType):
    def __init__(self, val=ffi.new("UA_ServiceFault*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    def __str__(self, n=0):
        return ("(UaServiceFault) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaPublishResponse +++++++++++++++++++++++
class UaPublishResponse(UaType):
    def __init__(self, val=ffi.new("UA_PublishResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._available_sequence_numbers_size = SizeT(val=val.availableSequenceNumbersSize, is_pointer=False)
        self._available_sequence_numbers = UaUInt32(val=val.availableSequenceNumbers, is_pointer=True)
        self._more_notifications = UaBoolean(val=val.moreNotifications, is_pointer=False)
        self._notification_message = UaNotificationMessage(val=val.notificationMessage, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._available_sequence_numbers_size.__value[0] = _val(val.availableSequenceNumbersSize)
        self._available_sequence_numbers.__value = val.availableSequenceNumbers
        self._more_notifications.__value[0] = _val(val.moreNotifications)
        self._notification_message.__value[0] = _val(val.notificationMessage)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def available_sequence_numbers_size(self):
        return self._available_sequence_numbers_size

    @property
    def available_sequence_numbers(self):
        return self._available_sequence_numbers

    @property
    def more_notifications(self):
        return self._more_notifications

    @property
    def notification_message(self):
        return self._notification_message

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @available_sequence_numbers_size.setter
    def available_sequence_numbers_size(self, val):
        self._available_sequence_numbers_size = val
        self._value.availableSequenceNumbersSize = val._value

    @available_sequence_numbers.setter
    def available_sequence_numbers(self, val):
        self._available_sequence_numbers = val
        self._value.availableSequenceNumbers = val.__value

    @more_notifications.setter
    def more_notifications(self, val):
        self._more_notifications = val
        self._value.moreNotifications = val._value

    @notification_message.setter
    def notification_message(self, val):
        self._notification_message = val
        self._value.notificationMessage = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaPublishResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "available_sequence_numbers_size" + self._available_sequence_numbers_size.__str__(
                    n + 1) +
                "\t" * (n + 1) + "available_sequence_numbers" + self._available_sequence_numbers.__str__(n + 1) +
                "\t" * (n + 1) + "more_notifications" + self._more_notifications.__str__(n + 1) +
                "\t" * (n + 1) + "notification_message" + self._notification_message.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCreateMonitoredItemsRequest +++++++++++++++++++++++
class UaCreateMonitoredItemsRequest(UaType):
    def __init__(self, val=ffi.new("UA_CreateMonitoredItemsRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._timestamps_to_return = UaTimestampsToReturn(val=val.timestampsToReturn, is_pointer=False)
        self._items_to_create_size = SizeT(val=val.itemsToCreateSize, is_pointer=False)
        self._items_to_create = UaMonitoredItemCreateRequest(val=val.itemsToCreate, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._timestamps_to_return.__value[0] = _val(val.timestampsToReturn)
        self._items_to_create_size.__value[0] = _val(val.itemsToCreateSize)
        self._items_to_create.__value = val.itemsToCreate

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def timestamps_to_return(self):
        return self._timestamps_to_return

    @property
    def items_to_create_size(self):
        return self._items_to_create_size

    @property
    def items_to_create(self):
        return self._items_to_create

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @timestamps_to_return.setter
    def timestamps_to_return(self, val):
        self._timestamps_to_return = val
        self._value.timestampsToReturn = val._value

    @items_to_create_size.setter
    def items_to_create_size(self, val):
        self._items_to_create_size = val
        self._value.itemsToCreateSize = val._value

    @items_to_create.setter
    def items_to_create(self, val):
        self._items_to_create = val
        self._value.itemsToCreate = val.__value

    def __str__(self, n=0):
        return ("(UaCreateMonitoredItemsRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "timestamps_to_return" + self._timestamps_to_return.__str__(n + 1) +
                "\t" * (n + 1) + "items_to_create_size" + self._items_to_create_size.__str__(n + 1) +
                "\t" * (n + 1) + "items_to_create" + self._items_to_create.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaOpenSecureChannelRequest +++++++++++++++++++++++
class UaOpenSecureChannelRequest(UaType):
    def __init__(self, val=ffi.new("UA_OpenSecureChannelRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._client_protocol_version = UaUInt32(val=val.clientProtocolVersion, is_pointer=False)
        self._request_type = UaSecurityTokenRequestType(val=val.requestType, is_pointer=False)
        self._security_mode = UaMessageSecurityMode(val=val.securityMode, is_pointer=False)
        self._client_nonce = UaByteString(val=val.clientNonce, is_pointer=False)
        self._requested_lifetime = UaUInt32(val=val.requestedLifetime, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._client_protocol_version.__value[0] = _val(val.clientProtocolVersion)
        self._request_type.__value[0] = _val(val.requestType)
        self._security_mode.__value[0] = _val(val.securityMode)
        self._client_nonce.__value[0] = _val(val.clientNonce)
        self._requested_lifetime.__value[0] = _val(val.requestedLifetime)

    @property
    def request_header(self):
        return self._request_header

    @property
    def client_protocol_version(self):
        return self._client_protocol_version

    @property
    def request_type(self):
        return self._request_type

    @property
    def security_mode(self):
        return self._security_mode

    @property
    def client_nonce(self):
        return self._client_nonce

    @property
    def requested_lifetime(self):
        return self._requested_lifetime

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @client_protocol_version.setter
    def client_protocol_version(self, val):
        self._client_protocol_version = val
        self._value.clientProtocolVersion = val._value

    @request_type.setter
    def request_type(self, val):
        self._request_type = val
        self._value.requestType = val._value

    @security_mode.setter
    def security_mode(self, val):
        self._security_mode = val
        self._value.securityMode = val._value

    @client_nonce.setter
    def client_nonce(self, val):
        self._client_nonce = val
        self._value.clientNonce = val._value

    @requested_lifetime.setter
    def requested_lifetime(self, val):
        self._requested_lifetime = val
        self._value.requestedLifetime = val._value

    def __str__(self, n=0):
        return ("(UaOpenSecureChannelRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "client_protocol_version" + self._client_protocol_version.__str__(n + 1) +
                "\t" * (n + 1) + "request_type" + self._request_type.__str__(n + 1) +
                "\t" * (n + 1) + "security_mode" + self._security_mode.__str__(n + 1) +
                "\t" * (n + 1) + "client_nonce" + self._client_nonce.__str__(n + 1) +
                "\t" * (n + 1) + "requested_lifetime" + self._requested_lifetime.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCloseSessionRequest +++++++++++++++++++++++
class UaCloseSessionRequest(UaType):
    def __init__(self, val=ffi.new("UA_CloseSessionRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._delete_subscriptions = UaBoolean(val=val.deleteSubscriptions, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._delete_subscriptions.__value[0] = _val(val.deleteSubscriptions)

    @property
    def request_header(self):
        return self._request_header

    @property
    def delete_subscriptions(self):
        return self._delete_subscriptions

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @delete_subscriptions.setter
    def delete_subscriptions(self, val):
        self._delete_subscriptions = val
        self._value.deleteSubscriptions = val._value

    def __str__(self, n=0):
        return ("(UaCloseSessionRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "delete_subscriptions" + self._delete_subscriptions.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaSetTriggeringRequest +++++++++++++++++++++++
class UaSetTriggeringRequest(UaType):
    def __init__(self, val=ffi.new("UA_SetTriggeringRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
        self._triggering_item_id = UaUInt32(val=val.triggeringItemId, is_pointer=False)
        self._links_to_add_size = SizeT(val=val.linksToAddSize, is_pointer=False)
        self._links_to_add = UaUInt32(val=val.linksToAdd, is_pointer=True)
        self._links_to_remove_size = SizeT(val=val.linksToRemoveSize, is_pointer=False)
        self._links_to_remove = UaUInt32(val=val.linksToRemove, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._subscription_id.__value[0] = _val(val.subscriptionId)
        self._triggering_item_id.__value[0] = _val(val.triggeringItemId)
        self._links_to_add_size.__value[0] = _val(val.linksToAddSize)
        self._links_to_add.__value = val.linksToAdd
        self._links_to_remove_size.__value[0] = _val(val.linksToRemoveSize)
        self._links_to_remove.__value = val.linksToRemove

    @property
    def request_header(self):
        return self._request_header

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def triggering_item_id(self):
        return self._triggering_item_id

    @property
    def links_to_add_size(self):
        return self._links_to_add_size

    @property
    def links_to_add(self):
        return self._links_to_add

    @property
    def links_to_remove_size(self):
        return self._links_to_remove_size

    @property
    def links_to_remove(self):
        return self._links_to_remove

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val._value

    @triggering_item_id.setter
    def triggering_item_id(self, val):
        self._triggering_item_id = val
        self._value.triggeringItemId = val._value

    @links_to_add_size.setter
    def links_to_add_size(self, val):
        self._links_to_add_size = val
        self._value.linksToAddSize = val._value

    @links_to_add.setter
    def links_to_add(self, val):
        self._links_to_add = val
        self._value.linksToAdd = val.__value

    @links_to_remove_size.setter
    def links_to_remove_size(self, val):
        self._links_to_remove_size = val
        self._value.linksToRemoveSize = val._value

    @links_to_remove.setter
    def links_to_remove(self, val):
        self._links_to_remove = val
        self._value.linksToRemove = val.__value

    def __str__(self, n=0):
        return ("(UaSetTriggeringRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "subscription_id" + self._subscription_id.__str__(n + 1) +
                "\t" * (n + 1) + "triggering_item_id" + self._triggering_item_id.__str__(n + 1) +
                "\t" * (n + 1) + "links_to_add_size" + self._links_to_add_size.__str__(n + 1) +
                "\t" * (n + 1) + "links_to_add" + self._links_to_add.__str__(n + 1) +
                "\t" * (n + 1) + "links_to_remove_size" + self._links_to_remove_size.__str__(n + 1) +
                "\t" * (n + 1) + "links_to_remove" + self._links_to_remove.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBrowseResult +++++++++++++++++++++++
class UaBrowseResult(UaType):
    def __init__(self, val=ffi.new("UA_BrowseResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
        self._continuation_point = UaByteString(val=val.continuationPoint, is_pointer=False)
        self._references_size = SizeT(val=val.referencesSize, is_pointer=False)
        self._references = UaReferenceDescription(val=val.references, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._status_code.__value[0] = _val(val.statusCode)
        self._continuation_point.__value[0] = _val(val.continuationPoint)
        self._references_size.__value[0] = _val(val.referencesSize)
        self._references.__value = val.references

    @property
    def status_code(self):
        return self._status_code

    @property
    def continuation_point(self):
        return self._continuation_point

    @property
    def references_size(self):
        return self._references_size

    @property
    def references(self):
        return self._references

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val._value

    @continuation_point.setter
    def continuation_point(self, val):
        self._continuation_point = val
        self._value.continuationPoint = val._value

    @references_size.setter
    def references_size(self, val):
        self._references_size = val
        self._value.referencesSize = val._value

    @references.setter
    def references(self, val):
        self._references = val
        self._value.references = val.__value

    def __str__(self, n=0):
        return ("(UaBrowseResult) :\n" +
                "\t" * (n + 1) + "status_code" + self._status_code.__str__(n + 1) +
                "\t" * (n + 1) + "continuation_point" + self._continuation_point.__str__(n + 1) +
                "\t" * (n + 1) + "references_size" + self._references_size.__str__(n + 1) +
                "\t" * (n + 1) + "references" + self._references.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAddReferencesRequest +++++++++++++++++++++++
class UaAddReferencesRequest(UaType):
    def __init__(self, val=ffi.new("UA_AddReferencesRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._references_to_add_size = SizeT(val=val.referencesToAddSize, is_pointer=False)
        self._references_to_add = UaAddReferencesItem(val=val.referencesToAdd, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._references_to_add_size.__value[0] = _val(val.referencesToAddSize)
        self._references_to_add.__value = val.referencesToAdd

    @property
    def request_header(self):
        return self._request_header

    @property
    def references_to_add_size(self):
        return self._references_to_add_size

    @property
    def references_to_add(self):
        return self._references_to_add

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @references_to_add_size.setter
    def references_to_add_size(self, val):
        self._references_to_add_size = val
        self._value.referencesToAddSize = val._value

    @references_to_add.setter
    def references_to_add(self, val):
        self._references_to_add = val
        self._value.referencesToAdd = val.__value

    def __str__(self, n=0):
        return ("(UaAddReferencesRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "references_to_add_size" + self._references_to_add_size.__str__(n + 1) +
                "\t" * (n + 1) + "references_to_add" + self._references_to_add.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAddNodesItem +++++++++++++++++++++++
class UaAddNodesItem(UaType):
    def __init__(self, val=ffi.new("UA_AddNodesItem*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._parent_node_id = UaExpandedNodeId(val=val.parentNodeId, is_pointer=False)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
        self._requested_new_node_id = UaExpandedNodeId(val=val.requestedNewNodeId, is_pointer=False)
        self._browse_name = UaQualifiedName(val=val.browseName, is_pointer=False)
        self._node_class = UaNodeClass(val=val.nodeClass, is_pointer=False)
        self._node_attributes = UaExtensionObject(val=val.nodeAttributes, is_pointer=False)
        self._type_definition = UaExpandedNodeId(val=val.typeDefinition, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._parent_node_id.__value[0] = _val(val.parentNodeId)
        self._reference_type_id.__value[0] = _val(val.referenceTypeId)
        self._requested_new_node_id.__value[0] = _val(val.requestedNewNodeId)
        self._browse_name.__value[0] = _val(val.browseName)
        self._node_class.__value[0] = _val(val.nodeClass)
        self._node_attributes.__value[0] = _val(val.nodeAttributes)
        self._type_definition.__value[0] = _val(val.typeDefinition)

    @property
    def parent_node_id(self):
        return self._parent_node_id

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @property
    def requested_new_node_id(self):
        return self._requested_new_node_id

    @property
    def browse_name(self):
        return self._browse_name

    @property
    def node_class(self):
        return self._node_class

    @property
    def node_attributes(self):
        return self._node_attributes

    @property
    def type_definition(self):
        return self._type_definition

    @parent_node_id.setter
    def parent_node_id(self, val):
        self._parent_node_id = val
        self._value.parentNodeId = val._value

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val._value

    @requested_new_node_id.setter
    def requested_new_node_id(self, val):
        self._requested_new_node_id = val
        self._value.requestedNewNodeId = val._value

    @browse_name.setter
    def browse_name(self, val):
        self._browse_name = val
        self._value.browseName = val._value

    @node_class.setter
    def node_class(self, val):
        self._node_class = val
        self._value.nodeClass = val._value

    @node_attributes.setter
    def node_attributes(self, val):
        self._node_attributes = val
        self._value.nodeAttributes = val._value

    @type_definition.setter
    def type_definition(self, val):
        self._type_definition = val
        self._value.typeDefinition = val._value

    def __str__(self, n=0):
        return ("(UaAddNodesItem) :\n" +
                "\t" * (n + 1) + "parent_node_id" + self._parent_node_id.__str__(n + 1) +
                "\t" * (n + 1) + "reference_type_id" + self._reference_type_id.__str__(n + 1) +
                "\t" * (n + 1) + "requested_new_node_id" + self._requested_new_node_id.__str__(n + 1) +
                "\t" * (n + 1) + "browse_name" + self._browse_name.__str__(n + 1) +
                "\t" * (n + 1) + "node_class" + self._node_class.__str__(n + 1) +
                "\t" * (n + 1) + "node_attributes" + self._node_attributes.__str__(n + 1) +
                "\t" * (n + 1) + "type_definition" + self._type_definition.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaServerStatusDataType +++++++++++++++++++++++
class UaServerStatusDataType(UaType):
    def __init__(self, val=ffi.new("UA_ServerStatusDataType*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._start_time = UaDateTime(val=val.startTime, is_pointer=False)
        self._current_time = UaDateTime(val=val.currentTime, is_pointer=False)
        self._state = UaServerState(val=val.state, is_pointer=False)
        self._build_info = UaBuildInfo(val=val.buildInfo, is_pointer=False)
        self._seconds_till_shutdown = UaUInt32(val=val.secondsTillShutdown, is_pointer=False)
        self._shutdown_reason = UaLocalizedText(val=val.shutdownReason, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._start_time.__value[0] = _val(val.startTime)
        self._current_time.__value[0] = _val(val.currentTime)
        self._state.__value[0] = _val(val.state)
        self._build_info.__value[0] = _val(val.buildInfo)
        self._seconds_till_shutdown.__value[0] = _val(val.secondsTillShutdown)
        self._shutdown_reason.__value[0] = _val(val.shutdownReason)

    @property
    def start_time(self):
        return self._start_time

    @property
    def current_time(self):
        return self._current_time

    @property
    def state(self):
        return self._state

    @property
    def build_info(self):
        return self._build_info

    @property
    def seconds_till_shutdown(self):
        return self._seconds_till_shutdown

    @property
    def shutdown_reason(self):
        return self._shutdown_reason

    @start_time.setter
    def start_time(self, val):
        self._start_time = val
        self._value.startTime = val._value

    @current_time.setter
    def current_time(self, val):
        self._current_time = val
        self._value.currentTime = val._value

    @state.setter
    def state(self, val):
        self._state = val
        self._value.state = val._value

    @build_info.setter
    def build_info(self, val):
        self._build_info = val
        self._value.buildInfo = val._value

    @seconds_till_shutdown.setter
    def seconds_till_shutdown(self, val):
        self._seconds_till_shutdown = val
        self._value.secondsTillShutdown = val._value

    @shutdown_reason.setter
    def shutdown_reason(self, val):
        self._shutdown_reason = val
        self._value.shutdownReason = val._value

    def __str__(self, n=0):
        return ("(UaServerStatusDataType) :\n" +
                "\t" * (n + 1) + "start_time" + self._start_time.__str__(n + 1) +
                "\t" * (n + 1) + "current_time" + self._current_time.__str__(n + 1) +
                "\t" * (n + 1) + "state" + self._state.__str__(n + 1) +
                "\t" * (n + 1) + "build_info" + self._build_info.__str__(n + 1) +
                "\t" * (n + 1) + "seconds_till_shutdown" + self._seconds_till_shutdown.__str__(n + 1) +
                "\t" * (n + 1) + "shutdown_reason" + self._shutdown_reason.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBrowseNextResponse +++++++++++++++++++++++
class UaBrowseNextResponse(UaType):
    def __init__(self, val=ffi.new("UA_BrowseNextResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaBrowseResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaBrowseNextResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAxisInformation +++++++++++++++++++++++
class UaAxisInformation(UaType):
    def __init__(self, val=ffi.new("UA_AxisInformation*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._engineering_units = UaEUInformation(val=val.engineeringUnits, is_pointer=False)
        self._e_u_range = UaRange(val=val.eURange, is_pointer=False)
        self._title = UaLocalizedText(val=val.title, is_pointer=False)
        self._axis_scale_type = UaAxisScaleEnumeration(val=val.axisScaleType, is_pointer=False)
        self._axis_steps_size = SizeT(val=val.axisStepsSize, is_pointer=False)
        self._axis_steps = UaDouble(val=val.axisSteps, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._engineering_units.__value[0] = _val(val.engineeringUnits)
        self._e_u_range.__value[0] = _val(val.eURange)
        self._title.__value[0] = _val(val.title)
        self._axis_scale_type.__value[0] = _val(val.axisScaleType)
        self._axis_steps_size.__value[0] = _val(val.axisStepsSize)
        self._axis_steps.__value = val.axisSteps

    @property
    def engineering_units(self):
        return self._engineering_units

    @property
    def e_u_range(self):
        return self._e_u_range

    @property
    def title(self):
        return self._title

    @property
    def axis_scale_type(self):
        return self._axis_scale_type

    @property
    def axis_steps_size(self):
        return self._axis_steps_size

    @property
    def axis_steps(self):
        return self._axis_steps

    @engineering_units.setter
    def engineering_units(self, val):
        self._engineering_units = val
        self._value.engineeringUnits = val._value

    @e_u_range.setter
    def e_u_range(self, val):
        self._e_u_range = val
        self._value.eURange = val._value

    @title.setter
    def title(self, val):
        self._title = val
        self._value.title = val._value

    @axis_scale_type.setter
    def axis_scale_type(self, val):
        self._axis_scale_type = val
        self._value.axisScaleType = val._value

    @axis_steps_size.setter
    def axis_steps_size(self, val):
        self._axis_steps_size = val
        self._value.axisStepsSize = val._value

    @axis_steps.setter
    def axis_steps(self, val):
        self._axis_steps = val
        self._value.axisSteps = val.__value

    def __str__(self, n=0):
        return ("(UaAxisInformation) :\n" +
                "\t" * (n + 1) + "engineering_units" + self._engineering_units.__str__(n + 1) +
                "\t" * (n + 1) + "e_u_range" + self._e_u_range.__str__(n + 1) +
                "\t" * (n + 1) + "title" + self._title.__str__(n + 1) +
                "\t" * (n + 1) + "axis_scale_type" + self._axis_scale_type.__str__(n + 1) +
                "\t" * (n + 1) + "axis_steps_size" + self._axis_steps_size.__str__(n + 1) +
                "\t" * (n + 1) + "axis_steps" + self._axis_steps.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaApplicationDescription +++++++++++++++++++++++
class UaApplicationDescription(UaType):
    def __init__(self, val=ffi.new("UA_ApplicationDescription*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._application_uri = UaString(val=val.applicationUri, is_pointer=False)
        self._product_uri = UaString(val=val.productUri, is_pointer=False)
        self._application_name = UaLocalizedText(val=val.applicationName, is_pointer=False)
        self._application_type = UaApplicationType(val=val.applicationType, is_pointer=False)
        self._gateway_server_uri = UaString(val=val.gatewayServerUri, is_pointer=False)
        self._discovery_profile_uri = UaString(val=val.discoveryProfileUri, is_pointer=False)
        self._discovery_urls_size = SizeT(val=val.discoveryUrlsSize, is_pointer=False)
        self._discovery_urls = UaString(val=val.discoveryUrls, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._application_uri.__value[0] = _val(val.applicationUri)
        self._product_uri.__value[0] = _val(val.productUri)
        self._application_name.__value[0] = _val(val.applicationName)
        self._application_type.__value[0] = _val(val.applicationType)
        self._gateway_server_uri.__value[0] = _val(val.gatewayServerUri)
        self._discovery_profile_uri.__value[0] = _val(val.discoveryProfileUri)
        self._discovery_urls_size.__value[0] = _val(val.discoveryUrlsSize)
        self._discovery_urls.__value = val.discoveryUrls

    @property
    def application_uri(self):
        return self._application_uri

    @property
    def product_uri(self):
        return self._product_uri

    @property
    def application_name(self):
        return self._application_name

    @property
    def application_type(self):
        return self._application_type

    @property
    def gateway_server_uri(self):
        return self._gateway_server_uri

    @property
    def discovery_profile_uri(self):
        return self._discovery_profile_uri

    @property
    def discovery_urls_size(self):
        return self._discovery_urls_size

    @property
    def discovery_urls(self):
        return self._discovery_urls

    @application_uri.setter
    def application_uri(self, val):
        self._application_uri = val
        self._value.applicationUri = val._value

    @product_uri.setter
    def product_uri(self, val):
        self._product_uri = val
        self._value.productUri = val._value

    @application_name.setter
    def application_name(self, val):
        self._application_name = val
        self._value.applicationName = val._value

    @application_type.setter
    def application_type(self, val):
        self._application_type = val
        self._value.applicationType = val._value

    @gateway_server_uri.setter
    def gateway_server_uri(self, val):
        self._gateway_server_uri = val
        self._value.gatewayServerUri = val._value

    @discovery_profile_uri.setter
    def discovery_profile_uri(self, val):
        self._discovery_profile_uri = val
        self._value.discoveryProfileUri = val._value

    @discovery_urls_size.setter
    def discovery_urls_size(self, val):
        self._discovery_urls_size = val
        self._value.discoveryUrlsSize = val._value

    @discovery_urls.setter
    def discovery_urls(self, val):
        self._discovery_urls = val
        self._value.discoveryUrls = val.__value

    def __str__(self, n=0):
        return ("(UaApplicationDescription) :\n" +
                "\t" * (n + 1) + "application_uri" + self._application_uri.__str__(n + 1) +
                "\t" * (n + 1) + "product_uri" + self._product_uri.__str__(n + 1) +
                "\t" * (n + 1) + "application_name" + self._application_name.__str__(n + 1) +
                "\t" * (n + 1) + "application_type" + self._application_type.__str__(n + 1) +
                "\t" * (n + 1) + "gateway_server_uri" + self._gateway_server_uri.__str__(n + 1) +
                "\t" * (n + 1) + "discovery_profile_uri" + self._discovery_profile_uri.__str__(n + 1) +
                "\t" * (n + 1) + "discovery_urls_size" + self._discovery_urls_size.__str__(n + 1) +
                "\t" * (n + 1) + "discovery_urls" + self._discovery_urls.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaReadRequest +++++++++++++++++++++++
class UaReadRequest(UaType):
    def __init__(self, val=ffi.new("UA_ReadRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._max_age = UaDouble(val=val.maxAge, is_pointer=False)
        self._timestamps_to_return = UaTimestampsToReturn(val=val.timestampsToReturn, is_pointer=False)
        self._nodes_to_read_size = SizeT(val=val.nodesToReadSize, is_pointer=False)
        self._nodes_to_read = UaReadValueId(val=val.nodesToRead, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._max_age.__value[0] = _val(val.maxAge)
        self._timestamps_to_return.__value[0] = _val(val.timestampsToReturn)
        self._nodes_to_read_size.__value[0] = _val(val.nodesToReadSize)
        self._nodes_to_read.__value = val.nodesToRead

    @property
    def request_header(self):
        return self._request_header

    @property
    def max_age(self):
        return self._max_age

    @property
    def timestamps_to_return(self):
        return self._timestamps_to_return

    @property
    def nodes_to_read_size(self):
        return self._nodes_to_read_size

    @property
    def nodes_to_read(self):
        return self._nodes_to_read

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @max_age.setter
    def max_age(self, val):
        self._max_age = val
        self._value.maxAge = val._value

    @timestamps_to_return.setter
    def timestamps_to_return(self, val):
        self._timestamps_to_return = val
        self._value.timestampsToReturn = val._value

    @nodes_to_read_size.setter
    def nodes_to_read_size(self, val):
        self._nodes_to_read_size = val
        self._value.nodesToReadSize = val._value

    @nodes_to_read.setter
    def nodes_to_read(self, val):
        self._nodes_to_read = val
        self._value.nodesToRead = val.__value

    def __str__(self, n=0):
        return ("(UaReadRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "max_age" + self._max_age.__str__(n + 1) +
                "\t" * (n + 1) + "timestamps_to_return" + self._timestamps_to_return.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_read_size" + self._nodes_to_read_size.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_read" + self._nodes_to_read.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaActivateSessionRequest +++++++++++++++++++++++
class UaActivateSessionRequest(UaType):
    def __init__(self, val=ffi.new("UA_ActivateSessionRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._client_signature = UaSignatureData(val=val.clientSignature, is_pointer=False)
        self._client_software_certificates_size = SizeT(val=val.clientSoftwareCertificatesSize, is_pointer=False)
        self._client_software_certificates = UaSignedSoftwareCertificate(val=val.clientSoftwareCertificates,
                                                                         is_pointer=True)
        self._locale_ids_size = SizeT(val=val.localeIdsSize, is_pointer=False)
        self._locale_ids = UaString(val=val.localeIds, is_pointer=True)
        self._user_identity_token = UaExtensionObject(val=val.userIdentityToken, is_pointer=False)
        self._user_token_signature = UaSignatureData(val=val.userTokenSignature, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._client_signature.__value[0] = _val(val.clientSignature)
        self._client_software_certificates_size.__value[0] = _val(val.clientSoftwareCertificatesSize)
        self._client_software_certificates.__value = val.clientSoftwareCertificates
        self._locale_ids_size.__value[0] = _val(val.localeIdsSize)
        self._locale_ids.__value = val.localeIds
        self._user_identity_token.__value[0] = _val(val.userIdentityToken)
        self._user_token_signature.__value[0] = _val(val.userTokenSignature)

    @property
    def request_header(self):
        return self._request_header

    @property
    def client_signature(self):
        return self._client_signature

    @property
    def client_software_certificates_size(self):
        return self._client_software_certificates_size

    @property
    def client_software_certificates(self):
        return self._client_software_certificates

    @property
    def locale_ids_size(self):
        return self._locale_ids_size

    @property
    def locale_ids(self):
        return self._locale_ids

    @property
    def user_identity_token(self):
        return self._user_identity_token

    @property
    def user_token_signature(self):
        return self._user_token_signature

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @client_signature.setter
    def client_signature(self, val):
        self._client_signature = val
        self._value.clientSignature = val._value

    @client_software_certificates_size.setter
    def client_software_certificates_size(self, val):
        self._client_software_certificates_size = val
        self._value.clientSoftwareCertificatesSize = val._value

    @client_software_certificates.setter
    def client_software_certificates(self, val):
        self._client_software_certificates = val
        self._value.clientSoftwareCertificates = val.__value

    @locale_ids_size.setter
    def locale_ids_size(self, val):
        self._locale_ids_size = val
        self._value.localeIdsSize = val._value

    @locale_ids.setter
    def locale_ids(self, val):
        self._locale_ids = val
        self._value.localeIds = val.__value

    @user_identity_token.setter
    def user_identity_token(self, val):
        self._user_identity_token = val
        self._value.userIdentityToken = val._value

    @user_token_signature.setter
    def user_token_signature(self, val):
        self._user_token_signature = val
        self._value.userTokenSignature = val._value

    def __str__(self, n=0):
        return ("(UaActivateSessionRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "client_signature" + self._client_signature.__str__(n + 1) +
                "\t" * (n + 1) + "client_software_certificates_size" + self._client_software_certificates_size.__str__(
                    n + 1) +
                "\t" * (n + 1) + "client_software_certificates" + self._client_software_certificates.__str__(n + 1) +
                "\t" * (n + 1) + "locale_ids_size" + self._locale_ids_size.__str__(n + 1) +
                "\t" * (n + 1) + "locale_ids" + self._locale_ids.__str__(n + 1) +
                "\t" * (n + 1) + "user_identity_token" + self._user_identity_token.__str__(n + 1) +
                "\t" * (n + 1) + "user_token_signature" + self._user_token_signature.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBrowsePathResult +++++++++++++++++++++++
class UaBrowsePathResult(UaType):
    def __init__(self, val=ffi.new("UA_BrowsePathResult*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
        self._targets_size = SizeT(val=val.targetsSize, is_pointer=False)
        self._targets = UaBrowsePathTarget(val=val.targets, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._status_code.__value[0] = _val(val.statusCode)
        self._targets_size.__value[0] = _val(val.targetsSize)
        self._targets.__value = val.targets

    @property
    def status_code(self):
        return self._status_code

    @property
    def targets_size(self):
        return self._targets_size

    @property
    def targets(self):
        return self._targets

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val._value

    @targets_size.setter
    def targets_size(self, val):
        self._targets_size = val
        self._value.targetsSize = val._value

    @targets.setter
    def targets(self, val):
        self._targets = val
        self._value.targets = val.__value

    def __str__(self, n=0):
        return ("(UaBrowsePathResult) :\n" +
                "\t" * (n + 1) + "status_code" + self._status_code.__str__(n + 1) +
                "\t" * (n + 1) + "targets_size" + self._targets_size.__str__(n + 1) +
                "\t" * (n + 1) + "targets" + self._targets.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAddNodesRequest +++++++++++++++++++++++
class UaAddNodesRequest(UaType):
    def __init__(self, val=ffi.new("UA_AddNodesRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._nodes_to_add_size = SizeT(val=val.nodesToAddSize, is_pointer=False)
        self._nodes_to_add = UaAddNodesItem(val=val.nodesToAdd, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._nodes_to_add_size.__value[0] = _val(val.nodesToAddSize)
        self._nodes_to_add.__value = val.nodesToAdd

    @property
    def request_header(self):
        return self._request_header

    @property
    def nodes_to_add_size(self):
        return self._nodes_to_add_size

    @property
    def nodes_to_add(self):
        return self._nodes_to_add

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @nodes_to_add_size.setter
    def nodes_to_add_size(self, val):
        self._nodes_to_add_size = val
        self._value.nodesToAddSize = val._value

    @nodes_to_add.setter
    def nodes_to_add(self, val):
        self._nodes_to_add = val
        self._value.nodesToAdd = val.__value

    def __str__(self, n=0):
        return ("(UaAddNodesRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_add_size" + self._nodes_to_add_size.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_add" + self._nodes_to_add.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBrowseRequest +++++++++++++++++++++++
class UaBrowseRequest(UaType):
    def __init__(self, val=ffi.new("UA_BrowseRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._view = UaViewDescription(val=val.view, is_pointer=False)
        self._requested_max_references_per_node = UaUInt32(val=val.requestedMaxReferencesPerNode, is_pointer=False)
        self._nodes_to_browse_size = SizeT(val=val.nodesToBrowseSize, is_pointer=False)
        self._nodes_to_browse = UaBrowseDescription(val=val.nodesToBrowse, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._view.__value[0] = _val(val.view)
        self._requested_max_references_per_node.__value[0] = _val(val.requestedMaxReferencesPerNode)
        self._nodes_to_browse_size.__value[0] = _val(val.nodesToBrowseSize)
        self._nodes_to_browse.__value = val.nodesToBrowse

    @property
    def request_header(self):
        return self._request_header

    @property
    def view(self):
        return self._view

    @property
    def requested_max_references_per_node(self):
        return self._requested_max_references_per_node

    @property
    def nodes_to_browse_size(self):
        return self._nodes_to_browse_size

    @property
    def nodes_to_browse(self):
        return self._nodes_to_browse

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @view.setter
    def view(self, val):
        self._view = val
        self._value.view = val._value

    @requested_max_references_per_node.setter
    def requested_max_references_per_node(self, val):
        self._requested_max_references_per_node = val
        self._value.requestedMaxReferencesPerNode = val._value

    @nodes_to_browse_size.setter
    def nodes_to_browse_size(self, val):
        self._nodes_to_browse_size = val
        self._value.nodesToBrowseSize = val._value

    @nodes_to_browse.setter
    def nodes_to_browse(self, val):
        self._nodes_to_browse = val
        self._value.nodesToBrowse = val.__value

    def __str__(self, n=0):
        return ("(UaBrowseRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "view" + self._view.__str__(n + 1) +
                "\t" * (n + 1) + "requested_max_references_per_node" + self._requested_max_references_per_node.__str__(
                    n + 1) +
                "\t" * (n + 1) + "nodes_to_browse_size" + self._nodes_to_browse_size.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_browse" + self._nodes_to_browse.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaWriteRequest +++++++++++++++++++++++
class UaWriteRequest(UaType):
    def __init__(self, val=ffi.new("UA_WriteRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._nodes_to_write_size = SizeT(val=val.nodesToWriteSize, is_pointer=False)
        self._nodes_to_write = UaWriteValue(val=val.nodesToWrite, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._nodes_to_write_size.__value[0] = _val(val.nodesToWriteSize)
        self._nodes_to_write.__value = val.nodesToWrite

    @property
    def request_header(self):
        return self._request_header

    @property
    def nodes_to_write_size(self):
        return self._nodes_to_write_size

    @property
    def nodes_to_write(self):
        return self._nodes_to_write

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @nodes_to_write_size.setter
    def nodes_to_write_size(self, val):
        self._nodes_to_write_size = val
        self._value.nodesToWriteSize = val._value

    @nodes_to_write.setter
    def nodes_to_write(self, val):
        self._nodes_to_write = val
        self._value.nodesToWrite = val.__value

    def __str__(self, n=0):
        return ("(UaWriteRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_write_size" + self._nodes_to_write_size.__str__(n + 1) +
                "\t" * (n + 1) + "nodes_to_write" + self._nodes_to_write.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAddNodesResponse +++++++++++++++++++++++
class UaAddNodesResponse(UaType):
    def __init__(self, val=ffi.new("UA_AddNodesResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaAddNodesResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaAddNodesResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaAttributeOperand +++++++++++++++++++++++
class UaAttributeOperand(UaType):
    def __init__(self, val=ffi.new("UA_AttributeOperand*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
        self._alias = UaString(val=val.alias, is_pointer=False)
        self._browse_path = UaRelativePath(val=val.browsePath, is_pointer=False)
        self._attribute_id = UaUInt32(val=val.attributeId, is_pointer=False)
        self._index_range = UaString(val=val.indexRange, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._node_id.__value[0] = _val(val.nodeId)
        self._alias.__value[0] = _val(val.alias)
        self._browse_path.__value[0] = _val(val.browsePath)
        self._attribute_id.__value[0] = _val(val.attributeId)
        self._index_range.__value[0] = _val(val.indexRange)

    @property
    def node_id(self):
        return self._node_id

    @property
    def alias(self):
        return self._alias

    @property
    def browse_path(self):
        return self._browse_path

    @property
    def attribute_id(self):
        return self._attribute_id

    @property
    def index_range(self):
        return self._index_range

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val._value

    @alias.setter
    def alias(self, val):
        self._alias = val
        self._value.alias = val._value

    @browse_path.setter
    def browse_path(self, val):
        self._browse_path = val
        self._value.browsePath = val._value

    @attribute_id.setter
    def attribute_id(self, val):
        self._attribute_id = val
        self._value.attributeId = val._value

    @index_range.setter
    def index_range(self, val):
        self._index_range = val
        self._value.indexRange = val._value

    def __str__(self, n=0):
        return ("(UaAttributeOperand) :\n" +
                "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1) +
                "\t" * (n + 1) + "alias" + self._alias.__str__(n + 1) +
                "\t" * (n + 1) + "browse_path" + self._browse_path.__str__(n + 1) +
                "\t" * (n + 1) + "attribute_id" + self._attribute_id.__str__(n + 1) +
                "\t" * (n + 1) + "index_range" + self._index_range.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDataChangeFilter +++++++++++++++++++++++
class UaDataChangeFilter(UaType):
    def __init__(self, val=ffi.new("UA_DataChangeFilter*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._trigger = UaDataChangeTrigger(val=val.trigger, is_pointer=False)
        self._deadband_type = UaUInt32(val=val.deadbandType, is_pointer=False)
        self._deadband_value = UaDouble(val=val.deadbandValue, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._trigger.__value[0] = _val(val.trigger)
        self._deadband_type.__value[0] = _val(val.deadbandType)
        self._deadband_value.__value[0] = _val(val.deadbandValue)

    @property
    def trigger(self):
        return self._trigger

    @property
    def deadband_type(self):
        return self._deadband_type

    @property
    def deadband_value(self):
        return self._deadband_value

    @trigger.setter
    def trigger(self, val):
        self._trigger = val
        self._value.trigger = val._value

    @deadband_type.setter
    def deadband_type(self, val):
        self._deadband_type = val
        self._value.deadbandType = val._value

    @deadband_value.setter
    def deadband_value(self, val):
        self._deadband_value = val
        self._value.deadbandValue = val._value

    def __str__(self, n=0):
        return ("(UaDataChangeFilter) :\n" +
                "\t" * (n + 1) + "trigger" + self._trigger.__str__(n + 1) +
                "\t" * (n + 1) + "deadband_type" + self._deadband_type.__str__(n + 1) +
                "\t" * (n + 1) + "deadband_value" + self._deadband_value.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaEndpointDescription +++++++++++++++++++++++
class UaEndpointDescription(UaType):
    def __init__(self, val=ffi.new("UA_EndpointDescription*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._endpoint_url = UaString(val=val.endpointUrl, is_pointer=False)
        self._server = UaApplicationDescription(val=val.server, is_pointer=False)
        self._server_certificate = UaByteString(val=val.serverCertificate, is_pointer=False)
        self._security_mode = UaMessageSecurityMode(val=val.securityMode, is_pointer=False)
        self._security_policy_uri = UaString(val=val.securityPolicyUri, is_pointer=False)
        self._user_identity_tokens_size = SizeT(val=val.userIdentityTokensSize, is_pointer=False)
        self._user_identity_tokens = UaUserTokenPolicy(val=val.userIdentityTokens, is_pointer=True)
        self._transport_profile_uri = UaString(val=val.transportProfileUri, is_pointer=False)
        self._security_level = UaByte(val=val.securityLevel, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._endpoint_url.__value[0] = _val(val.endpointUrl)
        self._server.__value[0] = _val(val.server)
        self._server_certificate.__value[0] = _val(val.serverCertificate)
        self._security_mode.__value[0] = _val(val.securityMode)
        self._security_policy_uri.__value[0] = _val(val.securityPolicyUri)
        self._user_identity_tokens_size.__value[0] = _val(val.userIdentityTokensSize)
        self._user_identity_tokens.__value = val.userIdentityTokens
        self._transport_profile_uri.__value[0] = _val(val.transportProfileUri)
        self._security_level.__value[0] = _val(val.securityLevel)

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @property
    def server(self):
        return self._server

    @property
    def server_certificate(self):
        return self._server_certificate

    @property
    def security_mode(self):
        return self._security_mode

    @property
    def security_policy_uri(self):
        return self._security_policy_uri

    @property
    def user_identity_tokens_size(self):
        return self._user_identity_tokens_size

    @property
    def user_identity_tokens(self):
        return self._user_identity_tokens

    @property
    def transport_profile_uri(self):
        return self._transport_profile_uri

    @property
    def security_level(self):
        return self._security_level

    @endpoint_url.setter
    def endpoint_url(self, val):
        self._endpoint_url = val
        self._value.endpointUrl = val._value

    @server.setter
    def server(self, val):
        self._server = val
        self._value.server = val._value

    @server_certificate.setter
    def server_certificate(self, val):
        self._server_certificate = val
        self._value.serverCertificate = val._value

    @security_mode.setter
    def security_mode(self, val):
        self._security_mode = val
        self._value.securityMode = val._value

    @security_policy_uri.setter
    def security_policy_uri(self, val):
        self._security_policy_uri = val
        self._value.securityPolicyUri = val._value

    @user_identity_tokens_size.setter
    def user_identity_tokens_size(self, val):
        self._user_identity_tokens_size = val
        self._value.userIdentityTokensSize = val._value

    @user_identity_tokens.setter
    def user_identity_tokens(self, val):
        self._user_identity_tokens = val
        self._value.userIdentityTokens = val.__value

    @transport_profile_uri.setter
    def transport_profile_uri(self, val):
        self._transport_profile_uri = val
        self._value.transportProfileUri = val._value

    @security_level.setter
    def security_level(self, val):
        self._security_level = val
        self._value.securityLevel = val._value

    def __str__(self, n=0):
        return ("(UaEndpointDescription) :\n" +
                "\t" * (n + 1) + "endpoint_url" + self._endpoint_url.__str__(n + 1) +
                "\t" * (n + 1) + "server" + self._server.__str__(n + 1) +
                "\t" * (n + 1) + "server_certificate" + self._server_certificate.__str__(n + 1) +
                "\t" * (n + 1) + "security_mode" + self._security_mode.__str__(n + 1) +
                "\t" * (n + 1) + "security_policy_uri" + self._security_policy_uri.__str__(n + 1) +
                "\t" * (n + 1) + "user_identity_tokens_size" + self._user_identity_tokens_size.__str__(n + 1) +
                "\t" * (n + 1) + "user_identity_tokens" + self._user_identity_tokens.__str__(n + 1) +
                "\t" * (n + 1) + "transport_profile_uri" + self._transport_profile_uri.__str__(n + 1) +
                "\t" * (n + 1) + "security_level" + self._security_level.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaDeleteReferencesRequest +++++++++++++++++++++++
class UaDeleteReferencesRequest(UaType):
    def __init__(self, val=ffi.new("UA_DeleteReferencesRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._references_to_delete_size = SizeT(val=val.referencesToDeleteSize, is_pointer=False)
        self._references_to_delete = UaDeleteReferencesItem(val=val.referencesToDelete, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._references_to_delete_size.__value[0] = _val(val.referencesToDeleteSize)
        self._references_to_delete.__value = val.referencesToDelete

    @property
    def request_header(self):
        return self._request_header

    @property
    def references_to_delete_size(self):
        return self._references_to_delete_size

    @property
    def references_to_delete(self):
        return self._references_to_delete

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @references_to_delete_size.setter
    def references_to_delete_size(self, val):
        self._references_to_delete_size = val
        self._value.referencesToDeleteSize = val._value

    @references_to_delete.setter
    def references_to_delete(self, val):
        self._references_to_delete = val
        self._value.referencesToDelete = val.__value

    def __str__(self, n=0):
        return ("(UaDeleteReferencesRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "references_to_delete_size" + self._references_to_delete_size.__str__(n + 1) +
                "\t" * (n + 1) + "references_to_delete" + self._references_to_delete.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaTranslateBrowsePathsToNodeIdsRequest +++++++++++++++++++++++
class UaTranslateBrowsePathsToNodeIdsRequest(UaType):
    def __init__(self, val=ffi.new("UA_TranslateBrowsePathsToNodeIdsRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._browse_paths_size = SizeT(val=val.browsePathsSize, is_pointer=False)
        self._browse_paths = UaBrowsePath(val=val.browsePaths, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._browse_paths_size.__value[0] = _val(val.browsePathsSize)
        self._browse_paths.__value = val.browsePaths

    @property
    def request_header(self):
        return self._request_header

    @property
    def browse_paths_size(self):
        return self._browse_paths_size

    @property
    def browse_paths(self):
        return self._browse_paths

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @browse_paths_size.setter
    def browse_paths_size(self, val):
        self._browse_paths_size = val
        self._value.browsePathsSize = val._value

    @browse_paths.setter
    def browse_paths(self, val):
        self._browse_paths = val
        self._value.browsePaths = val.__value

    def __str__(self, n=0):
        return ("(UaTranslateBrowsePathsToNodeIdsRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "browse_paths_size" + self._browse_paths_size.__str__(n + 1) +
                "\t" * (n + 1) + "browse_paths" + self._browse_paths.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaFindServersResponse +++++++++++++++++++++++
class UaFindServersResponse(UaType):
    def __init__(self, val=ffi.new("UA_FindServersResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._servers_size = SizeT(val=val.serversSize, is_pointer=False)
        self._servers = UaApplicationDescription(val=val.servers, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._servers_size.__value[0] = _val(val.serversSize)
        self._servers.__value = val.servers

    @property
    def response_header(self):
        return self._response_header

    @property
    def servers_size(self):
        return self._servers_size

    @property
    def servers(self):
        return self._servers

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @servers_size.setter
    def servers_size(self, val):
        self._servers_size = val
        self._value.serversSize = val._value

    @servers.setter
    def servers(self, val):
        self._servers = val
        self._value.servers = val.__value

    def __str__(self, n=0):
        return ("(UaFindServersResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "servers_size" + self._servers_size.__str__(n + 1) +
                "\t" * (n + 1) + "servers" + self._servers.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCreateSessionRequest +++++++++++++++++++++++
class UaCreateSessionRequest(UaType):
    def __init__(self, val=ffi.new("UA_CreateSessionRequest*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
        self._client_description = UaApplicationDescription(val=val.clientDescription, is_pointer=False)
        self._server_uri = UaString(val=val.serverUri, is_pointer=False)
        self._endpoint_url = UaString(val=val.endpointUrl, is_pointer=False)
        self._session_name = UaString(val=val.sessionName, is_pointer=False)
        self._client_nonce = UaByteString(val=val.clientNonce, is_pointer=False)
        self._client_certificate = UaByteString(val=val.clientCertificate, is_pointer=False)
        self._requested_session_timeout = UaDouble(val=val.requestedSessionTimeout, is_pointer=False)
        self._max_response_message_size = UaUInt32(val=val.maxResponseMessageSize, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._request_header.__value[0] = _val(val.requestHeader)
        self._client_description.__value[0] = _val(val.clientDescription)
        self._server_uri.__value[0] = _val(val.serverUri)
        self._endpoint_url.__value[0] = _val(val.endpointUrl)
        self._session_name.__value[0] = _val(val.sessionName)
        self._client_nonce.__value[0] = _val(val.clientNonce)
        self._client_certificate.__value[0] = _val(val.clientCertificate)
        self._requested_session_timeout.__value[0] = _val(val.requestedSessionTimeout)
        self._max_response_message_size.__value[0] = _val(val.maxResponseMessageSize)

    @property
    def request_header(self):
        return self._request_header

    @property
    def client_description(self):
        return self._client_description

    @property
    def server_uri(self):
        return self._server_uri

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @property
    def session_name(self):
        return self._session_name

    @property
    def client_nonce(self):
        return self._client_nonce

    @property
    def client_certificate(self):
        return self._client_certificate

    @property
    def requested_session_timeout(self):
        return self._requested_session_timeout

    @property
    def max_response_message_size(self):
        return self._max_response_message_size

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val._value

    @client_description.setter
    def client_description(self, val):
        self._client_description = val
        self._value.clientDescription = val._value

    @server_uri.setter
    def server_uri(self, val):
        self._server_uri = val
        self._value.serverUri = val._value

    @endpoint_url.setter
    def endpoint_url(self, val):
        self._endpoint_url = val
        self._value.endpointUrl = val._value

    @session_name.setter
    def session_name(self, val):
        self._session_name = val
        self._value.sessionName = val._value

    @client_nonce.setter
    def client_nonce(self, val):
        self._client_nonce = val
        self._value.clientNonce = val._value

    @client_certificate.setter
    def client_certificate(self, val):
        self._client_certificate = val
        self._value.clientCertificate = val._value

    @requested_session_timeout.setter
    def requested_session_timeout(self, val):
        self._requested_session_timeout = val
        self._value.requestedSessionTimeout = val._value

    @max_response_message_size.setter
    def max_response_message_size(self, val):
        self._max_response_message_size = val
        self._value.maxResponseMessageSize = val._value

    def __str__(self, n=0):
        return ("(UaCreateSessionRequest) :\n" +
                "\t" * (n + 1) + "request_header" + self._request_header.__str__(n + 1) +
                "\t" * (n + 1) + "client_description" + self._client_description.__str__(n + 1) +
                "\t" * (n + 1) + "server_uri" + self._server_uri.__str__(n + 1) +
                "\t" * (n + 1) + "endpoint_url" + self._endpoint_url.__str__(n + 1) +
                "\t" * (n + 1) + "session_name" + self._session_name.__str__(n + 1) +
                "\t" * (n + 1) + "client_nonce" + self._client_nonce.__str__(n + 1) +
                "\t" * (n + 1) + "client_certificate" + self._client_certificate.__str__(n + 1) +
                "\t" * (n + 1) + "requested_session_timeout" + self._requested_session_timeout.__str__(n + 1) +
                "\t" * (n + 1) + "max_response_message_size" + self._max_response_message_size.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaContentFilterElement +++++++++++++++++++++++
class UaContentFilterElement(UaType):
    def __init__(self, val=ffi.new("UA_ContentFilterElement*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._filter_operator = UaFilterOperator(val=val.filterOperator, is_pointer=False)
        self._filter_operands_size = SizeT(val=val.filterOperandsSize, is_pointer=False)
        self._filter_operands = UaExtensionObject(val=val.filterOperands, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._filter_operator.__value[0] = _val(val.filterOperator)
        self._filter_operands_size.__value[0] = _val(val.filterOperandsSize)
        self._filter_operands.__value = val.filterOperands

    @property
    def filter_operator(self):
        return self._filter_operator

    @property
    def filter_operands_size(self):
        return self._filter_operands_size

    @property
    def filter_operands(self):
        return self._filter_operands

    @filter_operator.setter
    def filter_operator(self, val):
        self._filter_operator = val
        self._value.filterOperator = val._value

    @filter_operands_size.setter
    def filter_operands_size(self, val):
        self._filter_operands_size = val
        self._value.filterOperandsSize = val._value

    @filter_operands.setter
    def filter_operands(self, val):
        self._filter_operands = val
        self._value.filterOperands = val.__value

    def __str__(self, n=0):
        return ("(UaContentFilterElement) :\n" +
                "\t" * (n + 1) + "filter_operator" + self._filter_operator.__str__(n + 1) +
                "\t" * (n + 1) + "filter_operands_size" + self._filter_operands_size.__str__(n + 1) +
                "\t" * (n + 1) + "filter_operands" + self._filter_operands.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaTranslateBrowsePathsToNodeIdsResponse +++++++++++++++++++++++
class UaTranslateBrowsePathsToNodeIdsResponse(UaType):
    def __init__(self, val=ffi.new("UA_TranslateBrowsePathsToNodeIdsResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaBrowsePathResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaTranslateBrowsePathsToNodeIdsResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaBrowseResponse +++++++++++++++++++++++
class UaBrowseResponse(UaType):
    def __init__(self, val=ffi.new("UA_BrowseResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
        self._results = UaBrowseResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._results_size.__value[0] = _val(val.resultsSize)
        self._results.__value = val.results
        self._diagnostic_infos_size.__value[0] = _val(val.diagnosticInfosSize)
        self._diagnostic_infos.__value = val.diagnosticInfos

    @property
    def response_header(self):
        return self._response_header

    @property
    def results_size(self):
        return self._results_size

    @property
    def results(self):
        return self._results

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val._value

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.__value

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._value

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.__value

    def __str__(self, n=0):
        return ("(UaBrowseResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "results_size" + self._results_size.__str__(n + 1) +
                "\t" * (n + 1) + "results" + self._results.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos_size" + self._diagnostic_infos_size.__str__(n + 1) +
                "\t" * (n + 1) + "diagnostic_infos" + self._diagnostic_infos.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaCreateSessionResponse +++++++++++++++++++++++
class UaCreateSessionResponse(UaType):
    def __init__(self, val=ffi.new("UA_CreateSessionResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._session_id = UaNodeId(val=val.sessionId, is_pointer=False)
        self._authentication_token = UaNodeId(val=val.authenticationToken, is_pointer=False)
        self._revised_session_timeout = UaDouble(val=val.revisedSessionTimeout, is_pointer=False)
        self._server_nonce = UaByteString(val=val.serverNonce, is_pointer=False)
        self._server_certificate = UaByteString(val=val.serverCertificate, is_pointer=False)
        self._server_endpoints_size = SizeT(val=val.serverEndpointsSize, is_pointer=False)
        self._server_endpoints = UaEndpointDescription(val=val.serverEndpoints, is_pointer=True)
        self._server_software_certificates_size = SizeT(val=val.serverSoftwareCertificatesSize, is_pointer=False)
        self._server_software_certificates = UaSignedSoftwareCertificate(val=val.serverSoftwareCertificates,
                                                                         is_pointer=True)
        self._server_signature = UaSignatureData(val=val.serverSignature, is_pointer=False)
        self._max_request_message_size = UaUInt32(val=val.maxRequestMessageSize, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._session_id.__value[0] = _val(val.sessionId)
        self._authentication_token.__value[0] = _val(val.authenticationToken)
        self._revised_session_timeout.__value[0] = _val(val.revisedSessionTimeout)
        self._server_nonce.__value[0] = _val(val.serverNonce)
        self._server_certificate.__value[0] = _val(val.serverCertificate)
        self._server_endpoints_size.__value[0] = _val(val.serverEndpointsSize)
        self._server_endpoints.__value = val.serverEndpoints
        self._server_software_certificates_size.__value[0] = _val(val.serverSoftwareCertificatesSize)
        self._server_software_certificates.__value = val.serverSoftwareCertificates
        self._server_signature.__value[0] = _val(val.serverSignature)
        self._max_request_message_size.__value[0] = _val(val.maxRequestMessageSize)

    @property
    def response_header(self):
        return self._response_header

    @property
    def session_id(self):
        return self._session_id

    @property
    def authentication_token(self):
        return self._authentication_token

    @property
    def revised_session_timeout(self):
        return self._revised_session_timeout

    @property
    def server_nonce(self):
        return self._server_nonce

    @property
    def server_certificate(self):
        return self._server_certificate

    @property
    def server_endpoints_size(self):
        return self._server_endpoints_size

    @property
    def server_endpoints(self):
        return self._server_endpoints

    @property
    def server_software_certificates_size(self):
        return self._server_software_certificates_size

    @property
    def server_software_certificates(self):
        return self._server_software_certificates

    @property
    def server_signature(self):
        return self._server_signature

    @property
    def max_request_message_size(self):
        return self._max_request_message_size

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @session_id.setter
    def session_id(self, val):
        self._session_id = val
        self._value.sessionId = val._value

    @authentication_token.setter
    def authentication_token(self, val):
        self._authentication_token = val
        self._value.authenticationToken = val._value

    @revised_session_timeout.setter
    def revised_session_timeout(self, val):
        self._revised_session_timeout = val
        self._value.revisedSessionTimeout = val._value

    @server_nonce.setter
    def server_nonce(self, val):
        self._server_nonce = val
        self._value.serverNonce = val._value

    @server_certificate.setter
    def server_certificate(self, val):
        self._server_certificate = val
        self._value.serverCertificate = val._value

    @server_endpoints_size.setter
    def server_endpoints_size(self, val):
        self._server_endpoints_size = val
        self._value.serverEndpointsSize = val._value

    @server_endpoints.setter
    def server_endpoints(self, val):
        self._server_endpoints = val
        self._value.serverEndpoints = val.__value

    @server_software_certificates_size.setter
    def server_software_certificates_size(self, val):
        self._server_software_certificates_size = val
        self._value.serverSoftwareCertificatesSize = val._value

    @server_software_certificates.setter
    def server_software_certificates(self, val):
        self._server_software_certificates = val
        self._value.serverSoftwareCertificates = val.__value

    @server_signature.setter
    def server_signature(self, val):
        self._server_signature = val
        self._value.serverSignature = val._value

    @max_request_message_size.setter
    def max_request_message_size(self, val):
        self._max_request_message_size = val
        self._value.maxRequestMessageSize = val._value

    def __str__(self, n=0):
        return ("(UaCreateSessionResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "session_id" + self._session_id.__str__(n + 1) +
                "\t" * (n + 1) + "authentication_token" + self._authentication_token.__str__(n + 1) +
                "\t" * (n + 1) + "revised_session_timeout" + self._revised_session_timeout.__str__(n + 1) +
                "\t" * (n + 1) + "server_nonce" + self._server_nonce.__str__(n + 1) +
                "\t" * (n + 1) + "server_certificate" + self._server_certificate.__str__(n + 1) +
                "\t" * (n + 1) + "server_endpoints_size" + self._server_endpoints_size.__str__(n + 1) +
                "\t" * (n + 1) + "server_endpoints" + self._server_endpoints.__str__(n + 1) +
                "\t" * (n + 1) + "server_software_certificates_size" + self._server_software_certificates_size.__str__(
                    n + 1) +
                "\t" * (n + 1) + "server_software_certificates" + self._server_software_certificates.__str__(n + 1) +
                "\t" * (n + 1) + "server_signature" + self._server_signature.__str__(n + 1) +
                "\t" * (n + 1) + "max_request_message_size" + self._max_request_message_size.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaContentFilter +++++++++++++++++++++++
class UaContentFilter(UaType):
    def __init__(self, val=ffi.new("UA_ContentFilter*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._elements_size = SizeT(val=val.elementsSize, is_pointer=False)
        self._elements = UaContentFilterElement(val=val.elements, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._elements_size.__value[0] = _val(val.elementsSize)
        self._elements.__value = val.elements

    @property
    def elements_size(self):
        return self._elements_size

    @property
    def elements(self):
        return self._elements

    @elements_size.setter
    def elements_size(self, val):
        self._elements_size = val
        self._value.elementsSize = val._value

    @elements.setter
    def elements(self, val):
        self._elements = val
        self._value.elements = val.__value

    def __str__(self, n=0):
        return ("(UaContentFilter) :\n" +
                "\t" * (n + 1) + "elements_size" + self._elements_size.__str__(n + 1) +
                "\t" * (n + 1) + "elements" + self._elements.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaGetEndpointsResponse +++++++++++++++++++++++
class UaGetEndpointsResponse(UaType):
    def __init__(self, val=ffi.new("UA_GetEndpointsResponse*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
        self._endpoints_size = SizeT(val=val.endpointsSize, is_pointer=False)
        self._endpoints = UaEndpointDescription(val=val.endpoints, is_pointer=True)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._response_header.__value[0] = _val(val.responseHeader)
        self._endpoints_size.__value[0] = _val(val.endpointsSize)
        self._endpoints.__value = val.endpoints

    @property
    def response_header(self):
        return self._response_header

    @property
    def endpoints_size(self):
        return self._endpoints_size

    @property
    def endpoints(self):
        return self._endpoints

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val._value

    @endpoints_size.setter
    def endpoints_size(self, val):
        self._endpoints_size = val
        self._value.endpointsSize = val._value

    @endpoints.setter
    def endpoints(self, val):
        self._endpoints = val
        self._value.endpoints = val.__value

    def __str__(self, n=0):
        return ("(UaGetEndpointsResponse) :\n" +
                "\t" * (n + 1) + "response_header" + self._response_header.__str__(n + 1) +
                "\t" * (n + 1) + "endpoints_size" + self._endpoints_size.__str__(n + 1) +
                "\t" * (n + 1) + "endpoints" + self._endpoints.__str__(n + 1) + "\n")


# +++++++++++++++++++ UaEventFilter +++++++++++++++++++++++
class UaEventFilter(UaType):
    def __init__(self, val=ffi.new("UA_EventFilter*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._select_clauses_size = SizeT(val=val.selectClausesSize, is_pointer=False)
        self._select_clauses = UaSimpleAttributeOperand(val=val.selectClauses, is_pointer=True)
        self._where_clause = UaContentFilter(val=val.whereClause, is_pointer=False)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
        self._select_clauses_size.__value[0] = _val(val.selectClausesSize)
        self._select_clauses.__value = val.selectClauses
        self._where_clause.__value[0] = _val(val.whereClause)

    @property
    def select_clauses_size(self):
        return self._select_clauses_size

    @property
    def select_clauses(self):
        return self._select_clauses

    @property
    def where_clause(self):
        return self._where_clause

    @select_clauses_size.setter
    def select_clauses_size(self, val):
        self._select_clauses_size = val
        self._value.selectClausesSize = val._value

    @select_clauses.setter
    def select_clauses(self, val):
        self._select_clauses = val
        self._value.selectClauses = val.__value

    @where_clause.setter
    def where_clause(self, val):
        self._where_clause = val
        self._value.whereClause = val._value

    def __str__(self, n=0):
        return ("(UaEventFilter) :\n" +
                "\t" * (n + 1) + "select_clauses_size" + self._select_clauses_size.__str__(n + 1) +
                "\t" * (n + 1) + "select_clauses" + self._select_clauses.__str__(n + 1) +
                "\t" * (n + 1) + "where_clause" + self._where_clause.__str__(n + 1) + "\n")
