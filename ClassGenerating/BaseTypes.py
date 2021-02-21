from intermediateApi import ffi, lib

# if val is a primitive type, then _ptr returns a pointer to a COPY of the value!!!
def _ptr(val):
    c_type = str(val).split("'")[1]
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
    if "*" or "[" in str(val):
        return True
    else:
        return False


class UaType:
    # __value should always be a pointer, so if it has to be dereferenced call ._value (for getter)
    # TODO: Idea -> free the passed memory when ever a primitive type is copied in _ptr.
    #  Then all base types hold their owner.
    def __init__(self, val, is_pointer=False):
        val = _ptr(val)
        self.__value = val
        self._is_pointer = is_pointer

    @property
    def _value(self):
        return self.__value[0]

    def __str__(self, n=0):
        return str(self.__value[0])


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


# +++++++++++++++++++ Char +++++++++++++++++++++++
class Char(UaType):
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
        return "(string): " + str(self._p_value) + "\n"


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
        self._data.__value[0] = _val(val.data)

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
        return ffi.string(ffi.cast(f"char[{self.length}]", self.data), self.length).decode("utf-8")

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
                    val = lib.UA_NODEID_STRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
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

        super().__init__(val=val, is_pointer=is_pointer)
        self._namespace_index = UaUInt16(val=val.namespaceIndex, is_pointer=False)
        self._identifier_type = UaNodeIdType(val=val.identifierType, is_pointer=False)
        cases = {
            0: UaUInt32(val=val.identifier.numeric),
            1: UaUInt32(val=val.identifier.numeric),
            2: UaUInt32(val=val.identifier.numeric),
            3: UaString(val=val.identifier.string),
            4: UaGuid(val=val.identifier.guid),
            5: UaByteString(val=val.identifier.byteString)
        }
        self._identifier = cases[self._identifier_type._value]

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
                "\t" * (n + 1) + "dimensions_size" + self._dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "dimensions" + self._dimensions.__str__(n + 1) + "\n")


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

    def _set_attributes(self):
        self._type = self.__value.type
        self._storage_type = self.__value.storageType
        self._array_length = self.__value.arrayLength
        self._data = self.__value.data
        self._array_dimensions_size = self.__value.arrayDimensionsSize
        self._array_dimensions = self.__value.arrayDimensions

    def set_scalar(self, data, data_type):
        lib.UA_Variant_setScalarCopy(self.value, ffi.new_handle(data), data_type._ref())
        self._set_attributes()

    def set_array(self, array, size, data_type):
        if size is int:
            size = SizeT(size)
        if size is not SizeT:
            raise AttributeError(f"size={size} has to be int or SizeT")
        status_code = lib.UA_Variant_setArrayCopy(self.__value, ffi.new_handle(array), size._deref(), data_type._ref())
        status_code = UaStatusCode(status_code)
        if not status_code.is_bad():
            self._set_attributes()
        else:
            raise Exception(f"An Error occured - {str(status_code)}")

    def copy_range_to(self, variant, num_range: UaNumericRange):
        status_code = lib.UA_Variant_copyRange(self.__value, variant._ref(), num_range._deref())
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
        status_code = lib.UA_Variant_setRangeCopy(self.__value, ffi.new_handle(array), size, num_range._deref())
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
                "\t" * (n + 1) + "ua_data_type_array" + self._ua_data_type_array.__str__(n + 1) +
                "\t" * (n + 1) + "types_size" + self._types_size.__str__(n + 1) +
                "\t" * (n + 1) + "types" + self._types.__str__(n + 1) + "\n")


