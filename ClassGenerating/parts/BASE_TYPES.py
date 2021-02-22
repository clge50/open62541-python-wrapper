from intermediateApi import ffi, lib


# if val is a primitive type, then _ptr returns a pointer to a COPY of the value!!!
def _ptr(val, c_type=""):
    if c_type == "":
        c_type = str(val).split("'")[1]
    if "&" in str(val):
        return ffi.addressof(val)
    if "*" in str(val) or "[" in str(val):
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


    # _value should always be a pointer
    # to get a pointer call ._ptr to get the value call ._val
    # TODO: Idea -> free the passed memory when ever a primitive type is copied in _ptr.
    #  Then all base types hold their owner.
class UaType:
    def __init__(self, val, is_pointer=False):
        if not is_pointer:
            val = _ptr(val)
        self._value = val
        self._is_pointer = is_pointer

    @property
    def value(self):
        return self._value

    @property
    def _val(self):
        return self._value[0]

    @property
    def _ptr(self):
        return self._value

    def __str__(self, n=0):
        return str(self._val)


# +++++++++++++++++++ Void +++++++++++++++++++++++
class Void(UaType):
    def __init__(self, data=None, val=None, is_pointer=True):
        if data is not None:
            val = ffi.new_handle(data)

        super().__init__(ffi.cast("void*", _ptr(val)), is_pointer)

    # TODO: Should this be possible? Where/which references will be changed?
    @UaType.value.setter
    def _value(self, val):
        self._value = ffi.cast("void*", _val(val))

    @property
    def data(self):
        return ffi.from_handle(self._ptr)

    def __str__(self, n=0):
        return "(Void): " + str(self.data) + "\n"


# +++++++++++++++++++ SizeT +++++++++++++++++++++++
class SizeT(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("size_t*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("size_t", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = ffi.cast("size_t", _val(val))

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
        self._value = ffi.new("char[]", self._p_value)

    def _set_value(self, val):
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

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_AttributeId")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaAttributeId): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_RuleHandling")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaRuleHandling): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_Order")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaOrder): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_SecureChannelState")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaSecureChannelState): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_SessionState")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaSessionState): {self.val_to_string[self._val]} ({str(self._val)})\n"



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

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NetworkStatistics")
        else:
            self._value[0] = _val(val)

        self._current_connection_count._value[0] = _val(val.currentConnectionCount)
        self._cumulated_connection_count._value[0] = _val(val.cumulatedConnectionCount)
        self._rejected_connection_count._value[0] = _val(val.rejectedConnectionCount)
        self._connection_timeout_count._value[0] = _val(val.connectionTimeoutCount)
        self._connection_abort_count._value[0] = _val(val.connectionAbortCount)

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
        self._value.currentConnectionCount = val._val

    @cumulated_connection_count.setter
    def cumulated_connection_count(self, val):
        self._cumulated_connection_count = val
        self._value.cumulatedConnectionCount = val._val

    @rejected_connection_count.setter
    def rejected_connection_count(self, val):
        self._rejected_connection_count = val
        self._value.rejectedConnectionCount = val._val

    @connection_timeout_count.setter
    def connection_timeout_count(self, val):
        self._connection_timeout_count = val
        self._value.connectionTimeoutCount = val._val

    @connection_abort_count.setter
    def connection_abort_count(self, val):
        self._connection_abort_count = val
        self._value.connectionAbortCount = val._val

    def __str__(self, n=0):
        return ("(UaNetworkStatistics) :\n" +
                "\t"*(n+1) + "current_connection_count" + self._current_connection_count.__str__(n+1) +
                "\t"*(n+1) + "cumulated_connection_count" + self._cumulated_connection_count.__str__(n+1) +
                "\t"*(n+1) + "rejected_connection_count" + self._rejected_connection_count.__str__(n+1) +
                "\t"*(n+1) + "connection_timeout_count" + self._connection_timeout_count.__str__(n+1) +
                "\t"*(n+1) + "connection_abort_count" + self._connection_abort_count.__str__(n+1) + "\n")


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

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SecureChannelStatistics")
        else:
            self._value[0] = _val(val)

        self._current_channel_count._value[0] = _val(val.currentChannelCount)
        self._cumulated_channel_count._value[0] = _val(val.cumulatedChannelCount)
        self._rejected_channel_count._value[0] = _val(val.rejectedChannelCount)
        self._channel_timeout_count._value[0] = _val(val.channelTimeoutCount)
        self._channel_abort_count._value[0] = _val(val.channelAbortCount)
        self._channel_purge_count._value[0] = _val(val.channelPurgeCount)

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
        self._value.currentChannelCount = val._val

    @cumulated_channel_count.setter
    def cumulated_channel_count(self, val):
        self._cumulated_channel_count = val
        self._value.cumulatedChannelCount = val._val

    @rejected_channel_count.setter
    def rejected_channel_count(self, val):
        self._rejected_channel_count = val
        self._value.rejectedChannelCount = val._val

    @channel_timeout_count.setter
    def channel_timeout_count(self, val):
        self._channel_timeout_count = val
        self._value.channelTimeoutCount = val._val

    @channel_abort_count.setter
    def channel_abort_count(self, val):
        self._channel_abort_count = val
        self._value.channelAbortCount = val._val

    @channel_purge_count.setter
    def channel_purge_count(self, val):
        self._channel_purge_count = val
        self._value.channelPurgeCount = val._val

    def __str__(self, n=0):
        return ("(UaSecureChannelStatistics) :\n" +
                "\t"*(n+1) + "current_channel_count" + self._current_channel_count.__str__(n+1) +
                "\t"*(n+1) + "cumulated_channel_count" + self._cumulated_channel_count.__str__(n+1) +
                "\t"*(n+1) + "rejected_channel_count" + self._rejected_channel_count.__str__(n+1) +
                "\t"*(n+1) + "channel_timeout_count" + self._channel_timeout_count.__str__(n+1) +
                "\t"*(n+1) + "channel_abort_count" + self._channel_abort_count.__str__(n+1) +
                "\t"*(n+1) + "channel_purge_count" + self._channel_purge_count.__str__(n+1) + "\n")


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
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_Boolean", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Boolean")
        else:
            self._value[0] = ffi.cast("UA_Boolean", _val(val))

    def __str__(self, n=0):
        return "(UaBoolean): " + str(self._val) + "\n"


# +++++++++++++++++++ UaSByte +++++++++++++++++++++++
class UaSByte(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_SByte*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_SByte", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SByte")
        else:
            self._value[0] = ffi.cast("UA_SByte", _val(val))

    def __str__(self, n=0):
        return "(UaSByte): " + str(self._val) + "\n"


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

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Byte")
        else:
            self._value[0] = ffi.cast("UA_Byte", _val(val))

    def __str__(self, n=0):
        return "(UaByte): " + str(self._val) + "\n"


# +++++++++++++++++++ UaInt16 +++++++++++++++++++++++
class UaInt16(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Int16*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_Int16", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int16")
        else:
            self._value[0] = ffi.cast("UA_Int16", _val(val))

    def __str__(self, n=0):
        return "(UaInt16): " + str(self._val) + "\n"


# +++++++++++++++++++ UaUInt16 +++++++++++++++++++++++
class UaUInt16(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UInt16*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_UInt16", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt16")
        else:
            self._value[0] = ffi.cast("UA_UInt16", _val(val))

    def __str__(self, n=0):
        return "(UaUInt16): " + str(self._val) + "\n"


# +++++++++++++++++++ UaInt32 +++++++++++++++++++++++
class UaInt32(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Int32*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_Int32", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int32")
        else:
            self._value[0] = ffi.cast("UA_Int32", _val(val))

    def __str__(self, n=0):
        return "(UaInt32): " + str(self._val) + "\n"


# +++++++++++++++++++ UaUInt32 +++++++++++++++++++++++
class UaUInt32(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UInt32*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_UInt32", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt32")
        else:
            self._value[0] = ffi.cast("UA_UInt32", _val(val))

    def __str__(self, n=0):
        return "(UaUInt32): " + str(self._val) + "\n"


# +++++++++++++++++++ UaInt64 +++++++++++++++++++++++
class UaInt64(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Int64*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_Int64", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int64")
        else:
            self._value[0] = ffi.cast("UA_Int64", _val(val))

    def __str__(self, n=0):
        return "(UaInt64): " + str(self._val) + "\n"


# +++++++++++++++++++ UaUInt64 +++++++++++++++++++++++
class UaUInt64(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_UInt64*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_UInt64", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt64")
        else:
            self._value[0] = ffi.cast("UA_UInt64", _val(val))

    def __str__(self, n=0):
        return "(UaUInt64): " + str(self._val) + "\n"


# +++++++++++++++++++ UaFloat +++++++++++++++++++++++
class UaFloat(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Float*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_Float", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Float")
        else:
            self._value[0] = ffi.cast("UA_Float", _val(val))

    def __str__(self, n=0):
        return "(UaFloat): " + str(self._val) + "\n"


# +++++++++++++++++++ UaDouble +++++++++++++++++++++++
class UaDouble(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Double*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_Double", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Double")
        else:
            self._value[0] = ffi.cast("UA_Double", _val(val))

    def __str__(self, n=0):
        return "(UaDouble): " + str(self._val) + "\n"

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
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_StatusCode", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_StatusCode")
        else:
            self._value[0] = ffi.cast("UA_StatusCode", _val(val))

    def __str__(self, n=0):
        return "(UaStatusCode): " + str(self._val) + "\n"

    def is_bad(self):
        return lib.UA_StatusCode_isBad(self._val)


# +++++++++++++++++++ UaDateTime +++++++++++++++++++++++
class UaDateTime(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_DateTime*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.cast("UA_DateTime", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DateTime")
        else:
            self._value[0] = ffi.cast("UA_DateTime", _val(val))

    def __str__(self, n=0):
        return "(UaDateTime): " + str(self._val) + "\n"

    @staticmethod
    def now():
        return UaDateTime(val=lib.UA_DateTime_now())

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
            super().__init__(ffi.new("enum UA_NodeIdType*"), is_pointer)
        else:
            super().__init__(ffi.cast("enum UA_NodeIdType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "enum UA_NodeIdType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaNodeIdType): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_VariantStorageType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaVariantStorageType): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_ExtensionObjectEncoding")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaExtensionObjectEncoding): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_DataTypeKind")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaDataTypeKind): {self.val_to_string[self._val]} ({str(self._val)})\n"


# -------------------------------------------------------------
# -------------------------- Structs --------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaString +++++++++++++++++++++++
class UaString(UaType):
    def __init__(self, p_val: str = "", val=ffi.new("UA_String*"), is_pointer=False):
        if p_val != "":
            val = ffi.new("UA_String*", lib.UA_String_fromChars(bytes(p_val, 'utf-8')))
        super().__init__(val=val, is_pointer=is_pointer)
        self._length = SizeT(val=val.length, is_pointer=False)
        self._data = UaByte(val=val.data, is_pointer=True)

    # TODO: Rather make new UaString?
    #   -> not sure where the pointer is directed and if there is enough memory for evtually more bytes than befor
    #   -> memory management for alloced memory from UA_String_fromChars

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_String")
        else:
            self._value[0] = _val(val)
        self._length._value[0] = _val(val.length)
        self._data._value = val.data

    @property
    def length(self):
        return self._length

    @property
    def data(self):
        return self._data

    def __eq__(self, ua_string):
        return lib.UA_String_equal(self._ptr, ua_string._ptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def equal_ignore_case(self, ua_string):
        return lib.UA_String_equal_ignorecase(self._ptr, ua_string._ptr)

    def to_string(self):
        return ffi.string(ffi.cast(f"char[{self.length._val}]", self.data._ptr), self.length._val).decode("utf-8")

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

    def _set_value(self, val):
        if self._is_pointer:
            self.__value = _ptr(val, "UA_DateTimeStruct")
        else:
            self.__value[0] = _val(val)
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
        self._value.nanoSec = val._val

    @micro_sec.setter
    def micro_sec(self, val):
        self._micro_sec = val
        self._value.microSec = val._val

    @milli_sec.setter
    def milli_sec(self, val):
        self._milli_sec = val
        self._value.milliSec = val._val

    @sec.setter
    def sec(self, val):
        self._sec = val
        self._value.sec = val._val

    @min.setter
    def min(self, val):
        self._min = val
        self._value.min = val._val

    @hour.setter
    def hour(self, val):
        self._hour = val
        self._value.hour = val._val

    @day.setter
    def day(self, val):
        self._day = val
        self._value.day = val._val

    @month.setter
    def month(self, val):
        self._month = val
        self._value.month = val._val

    @year.setter
    def year(self, val):
        self._year = val
        self._value.year = val._val

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
            val = ffi.new("UA_Guid*", lib.UA_GUID(bytes(string, 'utf-8')))
            if val == UaGuid.NULL:
                raise ValueError(
                    f""""{string}" has to be formatted like: 
        "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", with X in [0..9, A..F]""")

        super().__init__(val=val, is_pointer=is_pointer)

        self._data1 = UaUInt32(val=val.data1, is_pointer=False)
        self._data2 = UaUInt16(val=val.data2, is_pointer=False)
        self._data3 = UaUInt16(val=val.data3, is_pointer=False)
        self._data4 = UaByte(val=val.data4, is_pointer=True)

    def _set_value(self, val):
        if self._is_pointer:
            self.__value = _ptr(val, "")
        else:
            self.__value[0] = _val(val)
        self._data1._value[0] = val.data1
        self._data2._value[0] = val.data2
        self._data3._value[0] = val.data3
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

    # @data1.setter
    # def data1(self, val):
    #     self._data1 = val
    #     self._value.data1 = val._val
    #
    # @data2.setter
    # def data2(self, val):
    #     self._data2 = val
    #     self._value.data2 = val._val
    #
    # @data3.setter
    # def data3(self, val):
    #     self._data3 = val
    #     self._value.data3 = val._val
    #
    # @data4.setter
    # def data4(self, val):
    #     self._data4 = val
    #     self._value.data4 = val._ptr

    def __eq__(self, other):
        return lib.UA_Guid_equal(self._ptr, other._ptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self, n=0):
        d1 = '{0:0{1}X}'.format(self._data1._val, 8)
        d2 = '{0:0{1}X}'.format(self._data2._val, 4)
        d3 = '{0:0{1}X}'.format(self._data3._val, 4)
        d4 = ""
        for i in range(2):
            d4 += '{0:0{1}X}'.format(self._data4._ptr[i], 2)
        d5 = ""
        for i in range(2, 8):
            d5 += '{0:0{1}X}'.format(self._data4._ptr[i], 2)

        return "\t" * n + "UaGuid: " + f"{d1}-{d2}-{d3}-{d4}-{d5}" + "\n"


# +++++++++++++++++++ UaNodeId +++++++++++++++++++++++
class UaNodeId(UaType):
    NULL = lib.UA_NODEID_NULL

    UA_NS0ID_BOOLEAN = 1
    UA_NS0ID_SBYTE = 2
    UA_NS0ID_BYTE = 3
    UA_NS0ID_INT16 = 4
    UA_NS0ID_UINT16 = 5
    UA_NS0ID_INT32 = 6
    UA_NS0ID_UINT32 = 7
    UA_NS0ID_INT64 = 8
    UA_NS0ID_UINT64 = 9
    UA_NS0ID_FLOAT = 10
    UA_NS0ID_DOUBLE = 11
    UA_NS0ID_STRING = 12
    UA_NS0ID_DATETIME = 13
    UA_NS0ID_GUID = 14
    UA_NS0ID_BYTESTRING = 15
    UA_NS0ID_XMLELEMENT = 16
    UA_NS0ID_NODEID = 17
    UA_NS0ID_EXPANDEDNODEID = 18
    UA_NS0ID_STATUSCODE = 19
    UA_NS0ID_QUALIFIEDNAME = 20
    UA_NS0ID_LOCALIZEDTEXT = 21
    UA_NS0ID_STRUCTURE = 22
    UA_NS0ID_DATAVALUE = 23
    UA_NS0ID_BASEDATATYPE = 24
    UA_NS0ID_DIAGNOSTICINFO = 25
    UA_NS0ID_NUMBER = 26
    UA_NS0ID_INTEGER = 27
    UA_NS0ID_UINTEGER = 28
    UA_NS0ID_ENUMERATION = 29
    UA_NS0ID_IMAGE = 30
    UA_NS0ID_REFERENCES = 31
    UA_NS0ID_NONHIERARCHICALREFERENCES = 32
    UA_NS0ID_HIERARCHICALREFERENCES = 33
    UA_NS0ID_HASCHILD = 34
    UA_NS0ID_ORGANIZES = 35
    UA_NS0ID_HASEVENTSOURCE = 36
    UA_NS0ID_HASMODELLINGRULE = 37
    UA_NS0ID_HASENCODING = 38
    UA_NS0ID_HASDESCRIPTION = 39
    UA_NS0ID_HASTYPEDEFINITION = 40
    UA_NS0ID_GENERATESEVENT = 41
    UA_NS0ID_AGGREGATES = 44
    UA_NS0ID_HASSUBTYPE = 45
    UA_NS0ID_HASPROPERTY = 46
    UA_NS0ID_HASCOMPONENT = 47
    UA_NS0ID_HASNOTIFIER = 48
    UA_NS0ID_HASORDEREDCOMPONENT = 49
    UA_NS0ID_DECIMAL = 50
    UA_NS0ID_FROMSTATE = 51
    UA_NS0ID_TOSTATE = 52
    UA_NS0ID_HASCAUSE = 53
    UA_NS0ID_HASEFFECT = 54
    UA_NS0ID_HASHISTORICALCONFIGURATION = 56
    UA_NS0ID_BASEOBJECTTYPE = 58
    UA_NS0ID_FOLDERTYPE = 61
    UA_NS0ID_BASEVARIABLETYPE = 62
    UA_NS0ID_BASEDATAVARIABLETYPE = 63
    UA_NS0ID_PROPERTYTYPE = 68
    UA_NS0ID_DATATYPEDESCRIPTIONTYPE = 69
    UA_NS0ID_DATATYPEDICTIONARYTYPE = 72
    UA_NS0ID_DATATYPESYSTEMTYPE = 75
    UA_NS0ID_DATATYPEENCODINGTYPE = 76
    UA_NS0ID_MODELLINGRULETYPE = 77
    UA_NS0ID_MODELLINGRULE_MANDATORY = 78
    UA_NS0ID_MODELLINGRULE_OPTIONAL = 80
    UA_NS0ID_MODELLINGRULE_EXPOSESITSARRAY = 83
    UA_NS0ID_ROOTFOLDER = 84
    UA_NS0ID_OBJECTSFOLDER = 85
    UA_NS0ID_TYPESFOLDER = 86
    UA_NS0ID_VIEWSFOLDER = 87
    UA_NS0ID_OBJECTTYPESFOLDER = 88
    UA_NS0ID_VARIABLETYPESFOLDER = 89
    UA_NS0ID_DATATYPESFOLDER = 90
    UA_NS0ID_REFERENCETYPESFOLDER = 91
    UA_NS0ID_XMLSCHEMA_TYPESYSTEM = 92
    UA_NS0ID_OPCBINARYSCHEMA_TYPESYSTEM = 93
    UA_NS0ID_PERMISSIONTYPE = 94
    UA_NS0ID_ACCESSRESTRICTIONTYPE = 95
    UA_NS0ID_ROLEPERMISSIONTYPE = 96
    UA_NS0ID_DATATYPEDEFINITION = 97
    UA_NS0ID_STRUCTURETYPE = 98
    UA_NS0ID_STRUCTUREDEFINITION = 99
    UA_NS0ID_ENUMDEFINITION = 100
    UA_NS0ID_STRUCTUREFIELD = 101
    UA_NS0ID_ENUMFIELD = 102
    UA_NS0ID_DATATYPEDESCRIPTIONTYPE_DATATYPEVERSION = 104
    UA_NS0ID_DATATYPEDESCRIPTIONTYPE_DICTIONARYFRAGMENT = 105
    UA_NS0ID_DATATYPEDICTIONARYTYPE_DATATYPEVERSION = 106
    UA_NS0ID_DATATYPEDICTIONARYTYPE_NAMESPACEURI = 107
    UA_NS0ID_MODELLINGRULETYPE_NAMINGRULE = 111
    UA_NS0ID_MODELLINGRULE_MANDATORY_NAMINGRULE = 112
    UA_NS0ID_MODELLINGRULE_OPTIONAL_NAMINGRULE = 113
    UA_NS0ID_MODELLINGRULE_EXPOSESITSARRAY_NAMINGRULE = 114
    UA_NS0ID_HASSUBSTATEMACHINE = 117
    UA_NS0ID_NAMINGRULETYPE = 120
    UA_NS0ID_DATATYPEDEFINITION_ENCODING_DEFAULTBINARY = 121
    UA_NS0ID_STRUCTUREDEFINITION_ENCODING_DEFAULTBINARY = 122
    UA_NS0ID_ENUMDEFINITION_ENCODING_DEFAULTBINARY = 123
    UA_NS0ID_DATASETMETADATATYPE_ENCODING_DEFAULTBINARY = 124
    UA_NS0ID_DATATYPEDESCRIPTION_ENCODING_DEFAULTBINARY = 125
    UA_NS0ID_STRUCTUREDESCRIPTION_ENCODING_DEFAULTBINARY = 126
    UA_NS0ID_ENUMDESCRIPTION_ENCODING_DEFAULTBINARY = 127
    UA_NS0ID_ROLEPERMISSIONTYPE_ENCODING_DEFAULTBINARY = 128
    UA_NS0ID_HASARGUMENTDESCRIPTION = 129
    UA_NS0ID_HASOPTIONALINPUTARGUMENTDESCRIPTION = 131
    UA_NS0ID_IDTYPE = 256
    UA_NS0ID_NODECLASS = 257
    UA_NS0ID_NODE = 258
    UA_NS0ID_NODE_ENCODING_DEFAULTXML = 259
    UA_NS0ID_NODE_ENCODING_DEFAULTBINARY = 260
    UA_NS0ID_OBJECTNODE = 261
    UA_NS0ID_OBJECTNODE_ENCODING_DEFAULTXML = 262
    UA_NS0ID_OBJECTNODE_ENCODING_DEFAULTBINARY = 263
    UA_NS0ID_OBJECTTYPENODE = 264
    UA_NS0ID_OBJECTTYPENODE_ENCODING_DEFAULTXML = 265
    UA_NS0ID_OBJECTTYPENODE_ENCODING_DEFAULTBINARY = 266
    UA_NS0ID_VARIABLENODE = 267
    UA_NS0ID_VARIABLENODE_ENCODING_DEFAULTXML = 268
    UA_NS0ID_VARIABLENODE_ENCODING_DEFAULTBINARY = 269
    UA_NS0ID_VARIABLETYPENODE = 270
    UA_NS0ID_VARIABLETYPENODE_ENCODING_DEFAULTXML = 271
    UA_NS0ID_VARIABLETYPENODE_ENCODING_DEFAULTBINARY = 272
    UA_NS0ID_REFERENCETYPENODE = 273
    UA_NS0ID_REFERENCETYPENODE_ENCODING_DEFAULTXML = 274
    UA_NS0ID_REFERENCETYPENODE_ENCODING_DEFAULTBINARY = 275
    UA_NS0ID_METHODNODE = 276
    UA_NS0ID_METHODNODE_ENCODING_DEFAULTXML = 277
    UA_NS0ID_METHODNODE_ENCODING_DEFAULTBINARY = 278
    UA_NS0ID_VIEWNODE = 279
    UA_NS0ID_VIEWNODE_ENCODING_DEFAULTXML = 280
    UA_NS0ID_VIEWNODE_ENCODING_DEFAULTBINARY = 281
    UA_NS0ID_DATATYPENODE = 282
    UA_NS0ID_DATATYPENODE_ENCODING_DEFAULTXML = 283
    UA_NS0ID_DATATYPENODE_ENCODING_DEFAULTBINARY = 284
    UA_NS0ID_REFERENCENODE = 285
    UA_NS0ID_REFERENCENODE_ENCODING_DEFAULTXML = 286
    UA_NS0ID_REFERENCENODE_ENCODING_DEFAULTBINARY = 287
    UA_NS0ID_INTEGERID = 288
    UA_NS0ID_COUNTER = 289
    UA_NS0ID_DURATION = 290
    UA_NS0ID_NUMERICRANGE = 291
    UA_NS0ID_UTCTIME = 294
    UA_NS0ID_LOCALEID = 295
    UA_NS0ID_ARGUMENT = 296
    UA_NS0ID_ARGUMENT_ENCODING_DEFAULTXML = 297
    UA_NS0ID_ARGUMENT_ENCODING_DEFAULTBINARY = 298
    UA_NS0ID_STATUSRESULT = 299
    UA_NS0ID_STATUSRESULT_ENCODING_DEFAULTXML = 300
    UA_NS0ID_STATUSRESULT_ENCODING_DEFAULTBINARY = 301
    UA_NS0ID_MESSAGESECURITYMODE = 302
    UA_NS0ID_USERTOKENTYPE = 303
    UA_NS0ID_USERTOKENPOLICY = 304
    UA_NS0ID_USERTOKENPOLICY_ENCODING_DEFAULTXML = 305
    UA_NS0ID_USERTOKENPOLICY_ENCODING_DEFAULTBINARY = 306
    UA_NS0ID_APPLICATIONTYPE = 307
    UA_NS0ID_APPLICATIONDESCRIPTION = 308
    UA_NS0ID_APPLICATIONDESCRIPTION_ENCODING_DEFAULTXML = 309
    UA_NS0ID_APPLICATIONDESCRIPTION_ENCODING_DEFAULTBINARY = 310
    UA_NS0ID_APPLICATIONINSTANCECERTIFICATE = 311
    UA_NS0ID_ENDPOINTDESCRIPTION = 312
    UA_NS0ID_ENDPOINTDESCRIPTION_ENCODING_DEFAULTXML = 313
    UA_NS0ID_ENDPOINTDESCRIPTION_ENCODING_DEFAULTBINARY = 314
    UA_NS0ID_SECURITYTOKENREQUESTTYPE = 315
    UA_NS0ID_USERIDENTITYTOKEN = 316
    UA_NS0ID_USERIDENTITYTOKEN_ENCODING_DEFAULTXML = 317
    UA_NS0ID_USERIDENTITYTOKEN_ENCODING_DEFAULTBINARY = 318
    UA_NS0ID_ANONYMOUSIDENTITYTOKEN = 319
    UA_NS0ID_ANONYMOUSIDENTITYTOKEN_ENCODING_DEFAULTXML = 320
    UA_NS0ID_ANONYMOUSIDENTITYTOKEN_ENCODING_DEFAULTBINARY = 321
    UA_NS0ID_USERNAMEIDENTITYTOKEN = 322
    UA_NS0ID_USERNAMEIDENTITYTOKEN_ENCODING_DEFAULTXML = 323
    UA_NS0ID_USERNAMEIDENTITYTOKEN_ENCODING_DEFAULTBINARY = 324
    UA_NS0ID_X509IDENTITYTOKEN = 325
    UA_NS0ID_X509IDENTITYTOKEN_ENCODING_DEFAULTXML = 326
    UA_NS0ID_X509IDENTITYTOKEN_ENCODING_DEFAULTBINARY = 327
    UA_NS0ID_ENDPOINTCONFIGURATION = 331
    UA_NS0ID_ENDPOINTCONFIGURATION_ENCODING_DEFAULTXML = 332
    UA_NS0ID_ENDPOINTCONFIGURATION_ENCODING_DEFAULTBINARY = 333
    UA_NS0ID_BUILDINFO = 338
    UA_NS0ID_BUILDINFO_ENCODING_DEFAULTXML = 339
    UA_NS0ID_BUILDINFO_ENCODING_DEFAULTBINARY = 340
    UA_NS0ID_SIGNEDSOFTWARECERTIFICATE = 344
    UA_NS0ID_SIGNEDSOFTWARECERTIFICATE_ENCODING_DEFAULTXML = 345
    UA_NS0ID_SIGNEDSOFTWARECERTIFICATE_ENCODING_DEFAULTBINARY = 346
    UA_NS0ID_ATTRIBUTEWRITEMASK = 347
    UA_NS0ID_NODEATTRIBUTESMASK = 348
    UA_NS0ID_NODEATTRIBUTES = 349
    UA_NS0ID_NODEATTRIBUTES_ENCODING_DEFAULTXML = 350
    UA_NS0ID_NODEATTRIBUTES_ENCODING_DEFAULTBINARY = 351
    UA_NS0ID_OBJECTATTRIBUTES = 352
    UA_NS0ID_OBJECTATTRIBUTES_ENCODING_DEFAULTXML = 353
    UA_NS0ID_OBJECTATTRIBUTES_ENCODING_DEFAULTBINARY = 354
    UA_NS0ID_VARIABLEATTRIBUTES = 355
    UA_NS0ID_VARIABLEATTRIBUTES_ENCODING_DEFAULTXML = 356
    UA_NS0ID_VARIABLEATTRIBUTES_ENCODING_DEFAULTBINARY = 357
    UA_NS0ID_METHODATTRIBUTES = 358
    UA_NS0ID_METHODATTRIBUTES_ENCODING_DEFAULTXML = 359
    UA_NS0ID_METHODATTRIBUTES_ENCODING_DEFAULTBINARY = 360
    UA_NS0ID_OBJECTTYPEATTRIBUTES = 361
    UA_NS0ID_OBJECTTYPEATTRIBUTES_ENCODING_DEFAULTXML = 362
    UA_NS0ID_OBJECTTYPEATTRIBUTES_ENCODING_DEFAULTBINARY = 363
    UA_NS0ID_VARIABLETYPEATTRIBUTES = 364
    UA_NS0ID_VARIABLETYPEATTRIBUTES_ENCODING_DEFAULTXML = 365
    UA_NS0ID_VARIABLETYPEATTRIBUTES_ENCODING_DEFAULTBINARY = 366
    UA_NS0ID_REFERENCETYPEATTRIBUTES = 367
    UA_NS0ID_REFERENCETYPEATTRIBUTES_ENCODING_DEFAULTXML = 368
    UA_NS0ID_REFERENCETYPEATTRIBUTES_ENCODING_DEFAULTBINARY = 369
    UA_NS0ID_DATATYPEATTRIBUTES = 370
    UA_NS0ID_DATATYPEATTRIBUTES_ENCODING_DEFAULTXML = 371
    UA_NS0ID_DATATYPEATTRIBUTES_ENCODING_DEFAULTBINARY = 372
    UA_NS0ID_VIEWATTRIBUTES = 373
    UA_NS0ID_VIEWATTRIBUTES_ENCODING_DEFAULTXML = 374
    UA_NS0ID_VIEWATTRIBUTES_ENCODING_DEFAULTBINARY = 375
    UA_NS0ID_ADDNODESITEM = 376
    UA_NS0ID_ADDNODESITEM_ENCODING_DEFAULTXML = 377
    UA_NS0ID_ADDNODESITEM_ENCODING_DEFAULTBINARY = 378
    UA_NS0ID_ADDREFERENCESITEM = 379
    UA_NS0ID_ADDREFERENCESITEM_ENCODING_DEFAULTXML = 380
    UA_NS0ID_ADDREFERENCESITEM_ENCODING_DEFAULTBINARY = 381
    UA_NS0ID_DELETENODESITEM = 382
    UA_NS0ID_DELETENODESITEM_ENCODING_DEFAULTXML = 383
    UA_NS0ID_DELETENODESITEM_ENCODING_DEFAULTBINARY = 384
    UA_NS0ID_DELETEREFERENCESITEM = 385
    UA_NS0ID_DELETEREFERENCESITEM_ENCODING_DEFAULTXML = 386
    UA_NS0ID_DELETEREFERENCESITEM_ENCODING_DEFAULTBINARY = 387
    UA_NS0ID_SESSIONAUTHENTICATIONTOKEN = 388
    UA_NS0ID_REQUESTHEADER = 389
    UA_NS0ID_REQUESTHEADER_ENCODING_DEFAULTXML = 390
    UA_NS0ID_REQUESTHEADER_ENCODING_DEFAULTBINARY = 391
    UA_NS0ID_RESPONSEHEADER = 392
    UA_NS0ID_RESPONSEHEADER_ENCODING_DEFAULTXML = 393
    UA_NS0ID_RESPONSEHEADER_ENCODING_DEFAULTBINARY = 394
    UA_NS0ID_SERVICEFAULT = 395
    UA_NS0ID_SERVICEFAULT_ENCODING_DEFAULTXML = 396
    UA_NS0ID_SERVICEFAULT_ENCODING_DEFAULTBINARY = 397
    UA_NS0ID_FINDSERVERSREQUEST = 420
    UA_NS0ID_FINDSERVERSREQUEST_ENCODING_DEFAULTXML = 421
    UA_NS0ID_FINDSERVERSREQUEST_ENCODING_DEFAULTBINARY = 422
    UA_NS0ID_FINDSERVERSRESPONSE = 423
    UA_NS0ID_FINDSERVERSRESPONSE_ENCODING_DEFAULTXML = 424
    UA_NS0ID_FINDSERVERSRESPONSE_ENCODING_DEFAULTBINARY = 425
    UA_NS0ID_GETENDPOINTSREQUEST = 426
    UA_NS0ID_GETENDPOINTSREQUEST_ENCODING_DEFAULTXML = 427
    UA_NS0ID_GETENDPOINTSREQUEST_ENCODING_DEFAULTBINARY = 428
    UA_NS0ID_GETENDPOINTSRESPONSE = 429
    UA_NS0ID_GETENDPOINTSRESPONSE_ENCODING_DEFAULTXML = 430
    UA_NS0ID_GETENDPOINTSRESPONSE_ENCODING_DEFAULTBINARY = 431
    UA_NS0ID_REGISTEREDSERVER = 432
    UA_NS0ID_REGISTEREDSERVER_ENCODING_DEFAULTXML = 433
    UA_NS0ID_REGISTEREDSERVER_ENCODING_DEFAULTBINARY = 434
    UA_NS0ID_REGISTERSERVERREQUEST = 435
    UA_NS0ID_REGISTERSERVERREQUEST_ENCODING_DEFAULTXML = 436
    UA_NS0ID_REGISTERSERVERREQUEST_ENCODING_DEFAULTBINARY = 437
    UA_NS0ID_REGISTERSERVERRESPONSE = 438
    UA_NS0ID_REGISTERSERVERRESPONSE_ENCODING_DEFAULTXML = 439
    UA_NS0ID_REGISTERSERVERRESPONSE_ENCODING_DEFAULTBINARY = 440
    UA_NS0ID_CHANNELSECURITYTOKEN = 441
    UA_NS0ID_CHANNELSECURITYTOKEN_ENCODING_DEFAULTXML = 442
    UA_NS0ID_CHANNELSECURITYTOKEN_ENCODING_DEFAULTBINARY = 443
    UA_NS0ID_OPENSECURECHANNELREQUEST = 444
    UA_NS0ID_OPENSECURECHANNELREQUEST_ENCODING_DEFAULTXML = 445
    UA_NS0ID_OPENSECURECHANNELREQUEST_ENCODING_DEFAULTBINARY = 446
    UA_NS0ID_OPENSECURECHANNELRESPONSE = 447
    UA_NS0ID_OPENSECURECHANNELRESPONSE_ENCODING_DEFAULTXML = 448
    UA_NS0ID_OPENSECURECHANNELRESPONSE_ENCODING_DEFAULTBINARY = 449
    UA_NS0ID_CLOSESECURECHANNELREQUEST = 450
    UA_NS0ID_CLOSESECURECHANNELREQUEST_ENCODING_DEFAULTXML = 451
    UA_NS0ID_CLOSESECURECHANNELREQUEST_ENCODING_DEFAULTBINARY = 452
    UA_NS0ID_CLOSESECURECHANNELRESPONSE = 453
    UA_NS0ID_CLOSESECURECHANNELRESPONSE_ENCODING_DEFAULTXML = 454
    UA_NS0ID_CLOSESECURECHANNELRESPONSE_ENCODING_DEFAULTBINARY = 455
    UA_NS0ID_SIGNATUREDATA = 456
    UA_NS0ID_SIGNATUREDATA_ENCODING_DEFAULTXML = 457
    UA_NS0ID_SIGNATUREDATA_ENCODING_DEFAULTBINARY = 458
    UA_NS0ID_CREATESESSIONREQUEST = 459
    UA_NS0ID_CREATESESSIONREQUEST_ENCODING_DEFAULTXML = 460
    UA_NS0ID_CREATESESSIONREQUEST_ENCODING_DEFAULTBINARY = 461
    UA_NS0ID_CREATESESSIONRESPONSE = 462
    UA_NS0ID_CREATESESSIONRESPONSE_ENCODING_DEFAULTXML = 463
    UA_NS0ID_CREATESESSIONRESPONSE_ENCODING_DEFAULTBINARY = 464
    UA_NS0ID_ACTIVATESESSIONREQUEST = 465
    UA_NS0ID_ACTIVATESESSIONREQUEST_ENCODING_DEFAULTXML = 466
    UA_NS0ID_ACTIVATESESSIONREQUEST_ENCODING_DEFAULTBINARY = 467
    UA_NS0ID_ACTIVATESESSIONRESPONSE = 468
    UA_NS0ID_ACTIVATESESSIONRESPONSE_ENCODING_DEFAULTXML = 469
    UA_NS0ID_ACTIVATESESSIONRESPONSE_ENCODING_DEFAULTBINARY = 470
    UA_NS0ID_CLOSESESSIONREQUEST = 471
    UA_NS0ID_CLOSESESSIONREQUEST_ENCODING_DEFAULTXML = 472
    UA_NS0ID_CLOSESESSIONREQUEST_ENCODING_DEFAULTBINARY = 473
    UA_NS0ID_CLOSESESSIONRESPONSE = 474
    UA_NS0ID_CLOSESESSIONRESPONSE_ENCODING_DEFAULTXML = 475
    UA_NS0ID_CLOSESESSIONRESPONSE_ENCODING_DEFAULTBINARY = 476
    UA_NS0ID_CANCELREQUEST = 477
    UA_NS0ID_CANCELREQUEST_ENCODING_DEFAULTXML = 478
    UA_NS0ID_CANCELREQUEST_ENCODING_DEFAULTBINARY = 479
    UA_NS0ID_CANCELRESPONSE = 480
    UA_NS0ID_CANCELRESPONSE_ENCODING_DEFAULTXML = 481
    UA_NS0ID_CANCELRESPONSE_ENCODING_DEFAULTBINARY = 482
    UA_NS0ID_ADDNODESRESULT = 483
    UA_NS0ID_ADDNODESRESULT_ENCODING_DEFAULTXML = 484
    UA_NS0ID_ADDNODESRESULT_ENCODING_DEFAULTBINARY = 485
    UA_NS0ID_ADDNODESREQUEST = 486
    UA_NS0ID_ADDNODESREQUEST_ENCODING_DEFAULTXML = 487
    UA_NS0ID_ADDNODESREQUEST_ENCODING_DEFAULTBINARY = 488
    UA_NS0ID_ADDNODESRESPONSE = 489
    UA_NS0ID_ADDNODESRESPONSE_ENCODING_DEFAULTXML = 490
    UA_NS0ID_ADDNODESRESPONSE_ENCODING_DEFAULTBINARY = 491
    UA_NS0ID_ADDREFERENCESREQUEST = 492
    UA_NS0ID_ADDREFERENCESREQUEST_ENCODING_DEFAULTXML = 493
    UA_NS0ID_ADDREFERENCESREQUEST_ENCODING_DEFAULTBINARY = 494
    UA_NS0ID_ADDREFERENCESRESPONSE = 495
    UA_NS0ID_ADDREFERENCESRESPONSE_ENCODING_DEFAULTXML = 496
    UA_NS0ID_ADDREFERENCESRESPONSE_ENCODING_DEFAULTBINARY = 497
    UA_NS0ID_DELETENODESREQUEST = 498
    UA_NS0ID_DELETENODESREQUEST_ENCODING_DEFAULTXML = 499
    UA_NS0ID_DELETENODESREQUEST_ENCODING_DEFAULTBINARY = 500
    UA_NS0ID_DELETENODESRESPONSE = 501
    UA_NS0ID_DELETENODESRESPONSE_ENCODING_DEFAULTXML = 502
    UA_NS0ID_DELETENODESRESPONSE_ENCODING_DEFAULTBINARY = 503
    UA_NS0ID_DELETEREFERENCESREQUEST = 504
    UA_NS0ID_DELETEREFERENCESREQUEST_ENCODING_DEFAULTXML = 505
    UA_NS0ID_DELETEREFERENCESREQUEST_ENCODING_DEFAULTBINARY = 506
    UA_NS0ID_DELETEREFERENCESRESPONSE = 507
    UA_NS0ID_DELETEREFERENCESRESPONSE_ENCODING_DEFAULTXML = 508
    UA_NS0ID_DELETEREFERENCESRESPONSE_ENCODING_DEFAULTBINARY = 509
    UA_NS0ID_BROWSEDIRECTION = 510
    UA_NS0ID_VIEWDESCRIPTION = 511
    UA_NS0ID_VIEWDESCRIPTION_ENCODING_DEFAULTXML = 512
    UA_NS0ID_VIEWDESCRIPTION_ENCODING_DEFAULTBINARY = 513
    UA_NS0ID_BROWSEDESCRIPTION = 514
    UA_NS0ID_BROWSEDESCRIPTION_ENCODING_DEFAULTXML = 515
    UA_NS0ID_BROWSEDESCRIPTION_ENCODING_DEFAULTBINARY = 516
    UA_NS0ID_BROWSERESULTMASK = 517
    UA_NS0ID_REFERENCEDESCRIPTION = 518
    UA_NS0ID_REFERENCEDESCRIPTION_ENCODING_DEFAULTXML = 519
    UA_NS0ID_REFERENCEDESCRIPTION_ENCODING_DEFAULTBINARY = 520
    UA_NS0ID_CONTINUATIONPOINT = 521
    UA_NS0ID_BROWSERESULT = 522
    UA_NS0ID_BROWSERESULT_ENCODING_DEFAULTXML = 523
    UA_NS0ID_BROWSERESULT_ENCODING_DEFAULTBINARY = 524
    UA_NS0ID_BROWSEREQUEST = 525
    UA_NS0ID_BROWSEREQUEST_ENCODING_DEFAULTXML = 526
    UA_NS0ID_BROWSEREQUEST_ENCODING_DEFAULTBINARY = 527
    UA_NS0ID_BROWSERESPONSE = 528
    UA_NS0ID_BROWSERESPONSE_ENCODING_DEFAULTXML = 529
    UA_NS0ID_BROWSERESPONSE_ENCODING_DEFAULTBINARY = 530
    UA_NS0ID_BROWSENEXTREQUEST = 531
    UA_NS0ID_BROWSENEXTREQUEST_ENCODING_DEFAULTXML = 532
    UA_NS0ID_BROWSENEXTREQUEST_ENCODING_DEFAULTBINARY = 533
    UA_NS0ID_BROWSENEXTRESPONSE = 534
    UA_NS0ID_BROWSENEXTRESPONSE_ENCODING_DEFAULTXML = 535
    UA_NS0ID_BROWSENEXTRESPONSE_ENCODING_DEFAULTBINARY = 536
    UA_NS0ID_RELATIVEPATHELEMENT = 537
    UA_NS0ID_RELATIVEPATHELEMENT_ENCODING_DEFAULTXML = 538
    UA_NS0ID_RELATIVEPATHELEMENT_ENCODING_DEFAULTBINARY = 539
    UA_NS0ID_RELATIVEPATH = 540
    UA_NS0ID_RELATIVEPATH_ENCODING_DEFAULTXML = 541
    UA_NS0ID_RELATIVEPATH_ENCODING_DEFAULTBINARY = 542
    UA_NS0ID_BROWSEPATH = 543
    UA_NS0ID_BROWSEPATH_ENCODING_DEFAULTXML = 544
    UA_NS0ID_BROWSEPATH_ENCODING_DEFAULTBINARY = 545
    UA_NS0ID_BROWSEPATHTARGET = 546
    UA_NS0ID_BROWSEPATHTARGET_ENCODING_DEFAULTXML = 547
    UA_NS0ID_BROWSEPATHTARGET_ENCODING_DEFAULTBINARY = 548
    UA_NS0ID_BROWSEPATHRESULT = 549
    UA_NS0ID_BROWSEPATHRESULT_ENCODING_DEFAULTXML = 550
    UA_NS0ID_BROWSEPATHRESULT_ENCODING_DEFAULTBINARY = 551
    UA_NS0ID_TRANSLATEBROWSEPATHSTONODEIDSREQUEST = 552
    UA_NS0ID_TRANSLATEBROWSEPATHSTONODEIDSREQUEST_ENCODING_DEFAULTXML = 553
    UA_NS0ID_TRANSLATEBROWSEPATHSTONODEIDSREQUEST_ENCODING_DEFAULTBINARY = 554
    UA_NS0ID_TRANSLATEBROWSEPATHSTONODEIDSRESPONSE = 555
    UA_NS0ID_TRANSLATEBROWSEPATHSTONODEIDSRESPONSE_ENCODING_DEFAULTXML = 556
    UA_NS0ID_TRANSLATEBROWSEPATHSTONODEIDSRESPONSE_ENCODING_DEFAULTBINARY = 557
    UA_NS0ID_REGISTERNODESREQUEST = 558
    UA_NS0ID_REGISTERNODESREQUEST_ENCODING_DEFAULTXML = 559
    UA_NS0ID_REGISTERNODESREQUEST_ENCODING_DEFAULTBINARY = 560
    UA_NS0ID_REGISTERNODESRESPONSE = 561
    UA_NS0ID_REGISTERNODESRESPONSE_ENCODING_DEFAULTXML = 562
    UA_NS0ID_REGISTERNODESRESPONSE_ENCODING_DEFAULTBINARY = 563
    UA_NS0ID_UNREGISTERNODESREQUEST = 564
    UA_NS0ID_UNREGISTERNODESREQUEST_ENCODING_DEFAULTXML = 565
    UA_NS0ID_UNREGISTERNODESREQUEST_ENCODING_DEFAULTBINARY = 566
    UA_NS0ID_UNREGISTERNODESRESPONSE = 567
    UA_NS0ID_UNREGISTERNODESRESPONSE_ENCODING_DEFAULTXML = 568
    UA_NS0ID_UNREGISTERNODESRESPONSE_ENCODING_DEFAULTBINARY = 569
    UA_NS0ID_QUERYDATADESCRIPTION = 570
    UA_NS0ID_QUERYDATADESCRIPTION_ENCODING_DEFAULTXML = 571
    UA_NS0ID_QUERYDATADESCRIPTION_ENCODING_DEFAULTBINARY = 572
    UA_NS0ID_NODETYPEDESCRIPTION = 573
    UA_NS0ID_NODETYPEDESCRIPTION_ENCODING_DEFAULTXML = 574
    UA_NS0ID_NODETYPEDESCRIPTION_ENCODING_DEFAULTBINARY = 575
    UA_NS0ID_FILTEROPERATOR = 576
    UA_NS0ID_QUERYDATASET = 577
    UA_NS0ID_QUERYDATASET_ENCODING_DEFAULTXML = 578
    UA_NS0ID_QUERYDATASET_ENCODING_DEFAULTBINARY = 579
    UA_NS0ID_NODEREFERENCE = 580
    UA_NS0ID_NODEREFERENCE_ENCODING_DEFAULTXML = 581
    UA_NS0ID_NODEREFERENCE_ENCODING_DEFAULTBINARY = 582
    UA_NS0ID_CONTENTFILTERELEMENT = 583
    UA_NS0ID_CONTENTFILTERELEMENT_ENCODING_DEFAULTXML = 584
    UA_NS0ID_CONTENTFILTERELEMENT_ENCODING_DEFAULTBINARY = 585
    UA_NS0ID_CONTENTFILTER = 586
    UA_NS0ID_CONTENTFILTER_ENCODING_DEFAULTXML = 587
    UA_NS0ID_CONTENTFILTER_ENCODING_DEFAULTBINARY = 588
    UA_NS0ID_FILTEROPERAND = 589
    UA_NS0ID_FILTEROPERAND_ENCODING_DEFAULTXML = 590
    UA_NS0ID_FILTEROPERAND_ENCODING_DEFAULTBINARY = 591
    UA_NS0ID_ELEMENTOPERAND = 592
    UA_NS0ID_ELEMENTOPERAND_ENCODING_DEFAULTXML = 593
    UA_NS0ID_ELEMENTOPERAND_ENCODING_DEFAULTBINARY = 594
    UA_NS0ID_LITERALOPERAND = 595
    UA_NS0ID_LITERALOPERAND_ENCODING_DEFAULTXML = 596
    UA_NS0ID_LITERALOPERAND_ENCODING_DEFAULTBINARY = 597
    UA_NS0ID_ATTRIBUTEOPERAND = 598
    UA_NS0ID_ATTRIBUTEOPERAND_ENCODING_DEFAULTXML = 599
    UA_NS0ID_ATTRIBUTEOPERAND_ENCODING_DEFAULTBINARY = 600
    UA_NS0ID_SIMPLEATTRIBUTEOPERAND = 601
    UA_NS0ID_SIMPLEATTRIBUTEOPERAND_ENCODING_DEFAULTXML = 602
    UA_NS0ID_SIMPLEATTRIBUTEOPERAND_ENCODING_DEFAULTBINARY = 603
    UA_NS0ID_CONTENTFILTERELEMENTRESULT = 604
    UA_NS0ID_CONTENTFILTERELEMENTRESULT_ENCODING_DEFAULTXML = 605
    UA_NS0ID_CONTENTFILTERELEMENTRESULT_ENCODING_DEFAULTBINARY = 606
    UA_NS0ID_CONTENTFILTERRESULT = 607
    UA_NS0ID_CONTENTFILTERRESULT_ENCODING_DEFAULTXML = 608
    UA_NS0ID_CONTENTFILTERRESULT_ENCODING_DEFAULTBINARY = 609
    UA_NS0ID_PARSINGRESULT = 610
    UA_NS0ID_PARSINGRESULT_ENCODING_DEFAULTXML = 611
    UA_NS0ID_PARSINGRESULT_ENCODING_DEFAULTBINARY = 612
    UA_NS0ID_QUERYFIRSTREQUEST = 613
    UA_NS0ID_QUERYFIRSTREQUEST_ENCODING_DEFAULTXML = 614
    UA_NS0ID_QUERYFIRSTREQUEST_ENCODING_DEFAULTBINARY = 615
    UA_NS0ID_QUERYFIRSTRESPONSE = 616
    UA_NS0ID_QUERYFIRSTRESPONSE_ENCODING_DEFAULTXML = 617
    UA_NS0ID_QUERYFIRSTRESPONSE_ENCODING_DEFAULTBINARY = 618
    UA_NS0ID_QUERYNEXTREQUEST = 619
    UA_NS0ID_QUERYNEXTREQUEST_ENCODING_DEFAULTXML = 620
    UA_NS0ID_QUERYNEXTREQUEST_ENCODING_DEFAULTBINARY = 621
    UA_NS0ID_QUERYNEXTRESPONSE = 622
    UA_NS0ID_QUERYNEXTRESPONSE_ENCODING_DEFAULTXML = 623
    UA_NS0ID_QUERYNEXTRESPONSE_ENCODING_DEFAULTBINARY = 624
    UA_NS0ID_TIMESTAMPSTORETURN = 625
    UA_NS0ID_READVALUEID = 626
    UA_NS0ID_READVALUEID_ENCODING_DEFAULTXML = 627
    UA_NS0ID_READVALUEID_ENCODING_DEFAULTBINARY = 628
    UA_NS0ID_READREQUEST = 629
    UA_NS0ID_READREQUEST_ENCODING_DEFAULTXML = 630
    UA_NS0ID_READREQUEST_ENCODING_DEFAULTBINARY = 631
    UA_NS0ID_READRESPONSE = 632
    UA_NS0ID_READRESPONSE_ENCODING_DEFAULTXML = 633
    UA_NS0ID_READRESPONSE_ENCODING_DEFAULTBINARY = 634
    UA_NS0ID_HISTORYREADVALUEID = 635
    UA_NS0ID_HISTORYREADVALUEID_ENCODING_DEFAULTXML = 636
    UA_NS0ID_HISTORYREADVALUEID_ENCODING_DEFAULTBINARY = 637
    UA_NS0ID_HISTORYREADRESULT = 638
    UA_NS0ID_HISTORYREADRESULT_ENCODING_DEFAULTXML = 639
    UA_NS0ID_HISTORYREADRESULT_ENCODING_DEFAULTBINARY = 640
    UA_NS0ID_HISTORYREADDETAILS = 641
    UA_NS0ID_HISTORYREADDETAILS_ENCODING_DEFAULTXML = 642
    UA_NS0ID_HISTORYREADDETAILS_ENCODING_DEFAULTBINARY = 643
    UA_NS0ID_READEVENTDETAILS = 644
    UA_NS0ID_READEVENTDETAILS_ENCODING_DEFAULTXML = 645
    UA_NS0ID_READEVENTDETAILS_ENCODING_DEFAULTBINARY = 646
    UA_NS0ID_READRAWMODIFIEDDETAILS = 647
    UA_NS0ID_READRAWMODIFIEDDETAILS_ENCODING_DEFAULTXML = 648
    UA_NS0ID_READRAWMODIFIEDDETAILS_ENCODING_DEFAULTBINARY = 649
    UA_NS0ID_READPROCESSEDDETAILS = 650
    UA_NS0ID_READPROCESSEDDETAILS_ENCODING_DEFAULTXML = 651
    UA_NS0ID_READPROCESSEDDETAILS_ENCODING_DEFAULTBINARY = 652
    UA_NS0ID_READATTIMEDETAILS = 653
    UA_NS0ID_READATTIMEDETAILS_ENCODING_DEFAULTXML = 654
    UA_NS0ID_READATTIMEDETAILS_ENCODING_DEFAULTBINARY = 655
    UA_NS0ID_HISTORYDATA = 656
    UA_NS0ID_HISTORYDATA_ENCODING_DEFAULTXML = 657
    UA_NS0ID_HISTORYDATA_ENCODING_DEFAULTBINARY = 658
    UA_NS0ID_HISTORYEVENT = 659
    UA_NS0ID_HISTORYEVENT_ENCODING_DEFAULTXML = 660
    UA_NS0ID_HISTORYEVENT_ENCODING_DEFAULTBINARY = 661
    UA_NS0ID_HISTORYREADREQUEST = 662
    UA_NS0ID_HISTORYREADREQUEST_ENCODING_DEFAULTXML = 663
    UA_NS0ID_HISTORYREADREQUEST_ENCODING_DEFAULTBINARY = 664
    UA_NS0ID_HISTORYREADRESPONSE = 665
    UA_NS0ID_HISTORYREADRESPONSE_ENCODING_DEFAULTXML = 666
    UA_NS0ID_HISTORYREADRESPONSE_ENCODING_DEFAULTBINARY = 667
    UA_NS0ID_WRITEVALUE = 668
    UA_NS0ID_WRITEVALUE_ENCODING_DEFAULTXML = 669
    UA_NS0ID_WRITEVALUE_ENCODING_DEFAULTBINARY = 670
    UA_NS0ID_WRITEREQUEST = 671
    UA_NS0ID_WRITEREQUEST_ENCODING_DEFAULTXML = 672
    UA_NS0ID_WRITEREQUEST_ENCODING_DEFAULTBINARY = 673
    UA_NS0ID_WRITERESPONSE = 674
    UA_NS0ID_WRITERESPONSE_ENCODING_DEFAULTXML = 675
    UA_NS0ID_WRITERESPONSE_ENCODING_DEFAULTBINARY = 676
    UA_NS0ID_HISTORYUPDATEDETAILS = 677
    UA_NS0ID_HISTORYUPDATEDETAILS_ENCODING_DEFAULTXML = 678
    UA_NS0ID_HISTORYUPDATEDETAILS_ENCODING_DEFAULTBINARY = 679
    UA_NS0ID_UPDATEDATADETAILS = 680
    UA_NS0ID_UPDATEDATADETAILS_ENCODING_DEFAULTXML = 681
    UA_NS0ID_UPDATEDATADETAILS_ENCODING_DEFAULTBINARY = 682
    UA_NS0ID_UPDATEEVENTDETAILS = 683
    UA_NS0ID_UPDATEEVENTDETAILS_ENCODING_DEFAULTXML = 684
    UA_NS0ID_UPDATEEVENTDETAILS_ENCODING_DEFAULTBINARY = 685
    UA_NS0ID_DELETERAWMODIFIEDDETAILS = 686
    UA_NS0ID_DELETERAWMODIFIEDDETAILS_ENCODING_DEFAULTXML = 687
    UA_NS0ID_DELETERAWMODIFIEDDETAILS_ENCODING_DEFAULTBINARY = 688
    UA_NS0ID_DELETEATTIMEDETAILS = 689
    UA_NS0ID_DELETEATTIMEDETAILS_ENCODING_DEFAULTXML = 690
    UA_NS0ID_DELETEATTIMEDETAILS_ENCODING_DEFAULTBINARY = 691
    UA_NS0ID_DELETEEVENTDETAILS = 692
    UA_NS0ID_DELETEEVENTDETAILS_ENCODING_DEFAULTXML = 693
    UA_NS0ID_DELETEEVENTDETAILS_ENCODING_DEFAULTBINARY = 694
    UA_NS0ID_HISTORYUPDATERESULT = 695
    UA_NS0ID_HISTORYUPDATERESULT_ENCODING_DEFAULTXML = 696
    UA_NS0ID_HISTORYUPDATERESULT_ENCODING_DEFAULTBINARY = 697
    UA_NS0ID_HISTORYUPDATEREQUEST = 698
    UA_NS0ID_HISTORYUPDATEREQUEST_ENCODING_DEFAULTXML = 699
    UA_NS0ID_HISTORYUPDATEREQUEST_ENCODING_DEFAULTBINARY = 700
    UA_NS0ID_HISTORYUPDATERESPONSE = 701
    UA_NS0ID_HISTORYUPDATERESPONSE_ENCODING_DEFAULTXML = 702
    UA_NS0ID_HISTORYUPDATERESPONSE_ENCODING_DEFAULTBINARY = 703
    UA_NS0ID_CALLMETHODREQUEST = 704
    UA_NS0ID_CALLMETHODREQUEST_ENCODING_DEFAULTXML = 705
    UA_NS0ID_CALLMETHODREQUEST_ENCODING_DEFAULTBINARY = 706
    UA_NS0ID_CALLMETHODRESULT = 707
    UA_NS0ID_CALLMETHODRESULT_ENCODING_DEFAULTXML = 708
    UA_NS0ID_CALLMETHODRESULT_ENCODING_DEFAULTBINARY = 709
    UA_NS0ID_CALLREQUEST = 710
    UA_NS0ID_CALLREQUEST_ENCODING_DEFAULTXML = 711
    UA_NS0ID_CALLREQUEST_ENCODING_DEFAULTBINARY = 712
    UA_NS0ID_CALLRESPONSE = 713
    UA_NS0ID_CALLRESPONSE_ENCODING_DEFAULTXML = 714
    UA_NS0ID_CALLRESPONSE_ENCODING_DEFAULTBINARY = 715
    UA_NS0ID_MONITORINGMODE = 716
    UA_NS0ID_DATACHANGETRIGGER = 717
    UA_NS0ID_DEADBANDTYPE = 718
    UA_NS0ID_MONITORINGFILTER = 719
    UA_NS0ID_MONITORINGFILTER_ENCODING_DEFAULTXML = 720
    UA_NS0ID_MONITORINGFILTER_ENCODING_DEFAULTBINARY = 721
    UA_NS0ID_DATACHANGEFILTER = 722
    UA_NS0ID_DATACHANGEFILTER_ENCODING_DEFAULTXML = 723
    UA_NS0ID_DATACHANGEFILTER_ENCODING_DEFAULTBINARY = 724
    UA_NS0ID_EVENTFILTER = 725
    UA_NS0ID_EVENTFILTER_ENCODING_DEFAULTXML = 726
    UA_NS0ID_EVENTFILTER_ENCODING_DEFAULTBINARY = 727
    UA_NS0ID_AGGREGATEFILTER = 728
    UA_NS0ID_AGGREGATEFILTER_ENCODING_DEFAULTXML = 729
    UA_NS0ID_AGGREGATEFILTER_ENCODING_DEFAULTBINARY = 730
    UA_NS0ID_MONITORINGFILTERRESULT = 731
    UA_NS0ID_MONITORINGFILTERRESULT_ENCODING_DEFAULTXML = 732
    UA_NS0ID_MONITORINGFILTERRESULT_ENCODING_DEFAULTBINARY = 733
    UA_NS0ID_EVENTFILTERRESULT = 734
    UA_NS0ID_EVENTFILTERRESULT_ENCODING_DEFAULTXML = 735
    UA_NS0ID_EVENTFILTERRESULT_ENCODING_DEFAULTBINARY = 736
    UA_NS0ID_AGGREGATEFILTERRESULT = 737
    UA_NS0ID_AGGREGATEFILTERRESULT_ENCODING_DEFAULTXML = 738
    UA_NS0ID_AGGREGATEFILTERRESULT_ENCODING_DEFAULTBINARY = 739
    UA_NS0ID_MONITORINGPARAMETERS = 740
    UA_NS0ID_MONITORINGPARAMETERS_ENCODING_DEFAULTXML = 741
    UA_NS0ID_MONITORINGPARAMETERS_ENCODING_DEFAULTBINARY = 742
    UA_NS0ID_MONITOREDITEMCREATEREQUEST = 743
    UA_NS0ID_MONITOREDITEMCREATEREQUEST_ENCODING_DEFAULTXML = 744
    UA_NS0ID_MONITOREDITEMCREATEREQUEST_ENCODING_DEFAULTBINARY = 745
    UA_NS0ID_MONITOREDITEMCREATERESULT = 746
    UA_NS0ID_MONITOREDITEMCREATERESULT_ENCODING_DEFAULTXML = 747
    UA_NS0ID_MONITOREDITEMCREATERESULT_ENCODING_DEFAULTBINARY = 748
    UA_NS0ID_CREATEMONITOREDITEMSREQUEST = 749
    UA_NS0ID_CREATEMONITOREDITEMSREQUEST_ENCODING_DEFAULTXML = 750
    UA_NS0ID_CREATEMONITOREDITEMSREQUEST_ENCODING_DEFAULTBINARY = 751
    UA_NS0ID_CREATEMONITOREDITEMSRESPONSE = 752
    UA_NS0ID_CREATEMONITOREDITEMSRESPONSE_ENCODING_DEFAULTXML = 753
    UA_NS0ID_CREATEMONITOREDITEMSRESPONSE_ENCODING_DEFAULTBINARY = 754
    UA_NS0ID_MONITOREDITEMMODIFYREQUEST = 755
    UA_NS0ID_MONITOREDITEMMODIFYREQUEST_ENCODING_DEFAULTXML = 756
    UA_NS0ID_MONITOREDITEMMODIFYREQUEST_ENCODING_DEFAULTBINARY = 757
    UA_NS0ID_MONITOREDITEMMODIFYRESULT = 758
    UA_NS0ID_MONITOREDITEMMODIFYRESULT_ENCODING_DEFAULTXML = 759
    UA_NS0ID_MONITOREDITEMMODIFYRESULT_ENCODING_DEFAULTBINARY = 760
    UA_NS0ID_MODIFYMONITOREDITEMSREQUEST = 761
    UA_NS0ID_MODIFYMONITOREDITEMSREQUEST_ENCODING_DEFAULTXML = 762
    UA_NS0ID_MODIFYMONITOREDITEMSREQUEST_ENCODING_DEFAULTBINARY = 763
    UA_NS0ID_MODIFYMONITOREDITEMSRESPONSE = 764
    UA_NS0ID_MODIFYMONITOREDITEMSRESPONSE_ENCODING_DEFAULTXML = 765
    UA_NS0ID_MODIFYMONITOREDITEMSRESPONSE_ENCODING_DEFAULTBINARY = 766
    UA_NS0ID_SETMONITORINGMODEREQUEST = 767
    UA_NS0ID_SETMONITORINGMODEREQUEST_ENCODING_DEFAULTXML = 768
    UA_NS0ID_SETMONITORINGMODEREQUEST_ENCODING_DEFAULTBINARY = 769
    UA_NS0ID_SETMONITORINGMODERESPONSE = 770
    UA_NS0ID_SETMONITORINGMODERESPONSE_ENCODING_DEFAULTXML = 771
    UA_NS0ID_SETMONITORINGMODERESPONSE_ENCODING_DEFAULTBINARY = 772
    UA_NS0ID_SETTRIGGERINGREQUEST = 773
    UA_NS0ID_SETTRIGGERINGREQUEST_ENCODING_DEFAULTXML = 774
    UA_NS0ID_SETTRIGGERINGREQUEST_ENCODING_DEFAULTBINARY = 775
    UA_NS0ID_SETTRIGGERINGRESPONSE = 776
    UA_NS0ID_SETTRIGGERINGRESPONSE_ENCODING_DEFAULTXML = 777
    UA_NS0ID_SETTRIGGERINGRESPONSE_ENCODING_DEFAULTBINARY = 778
    UA_NS0ID_DELETEMONITOREDITEMSREQUEST = 779
    UA_NS0ID_DELETEMONITOREDITEMSREQUEST_ENCODING_DEFAULTXML = 780
    UA_NS0ID_DELETEMONITOREDITEMSREQUEST_ENCODING_DEFAULTBINARY = 781
    UA_NS0ID_DELETEMONITOREDITEMSRESPONSE = 782
    UA_NS0ID_DELETEMONITOREDITEMSRESPONSE_ENCODING_DEFAULTXML = 783
    UA_NS0ID_DELETEMONITOREDITEMSRESPONSE_ENCODING_DEFAULTBINARY = 784
    UA_NS0ID_CREATESUBSCRIPTIONREQUEST = 785
    UA_NS0ID_CREATESUBSCRIPTIONREQUEST_ENCODING_DEFAULTXML = 786
    UA_NS0ID_CREATESUBSCRIPTIONREQUEST_ENCODING_DEFAULTBINARY = 787
    UA_NS0ID_CREATESUBSCRIPTIONRESPONSE = 788
    UA_NS0ID_CREATESUBSCRIPTIONRESPONSE_ENCODING_DEFAULTXML = 789
    UA_NS0ID_CREATESUBSCRIPTIONRESPONSE_ENCODING_DEFAULTBINARY = 790
    UA_NS0ID_MODIFYSUBSCRIPTIONREQUEST = 791
    UA_NS0ID_MODIFYSUBSCRIPTIONREQUEST_ENCODING_DEFAULTXML = 792
    UA_NS0ID_MODIFYSUBSCRIPTIONREQUEST_ENCODING_DEFAULTBINARY = 793
    UA_NS0ID_MODIFYSUBSCRIPTIONRESPONSE = 794
    UA_NS0ID_MODIFYSUBSCRIPTIONRESPONSE_ENCODING_DEFAULTXML = 795
    UA_NS0ID_MODIFYSUBSCRIPTIONRESPONSE_ENCODING_DEFAULTBINARY = 796
    UA_NS0ID_SETPUBLISHINGMODEREQUEST = 797
    UA_NS0ID_SETPUBLISHINGMODEREQUEST_ENCODING_DEFAULTXML = 798
    UA_NS0ID_SETPUBLISHINGMODEREQUEST_ENCODING_DEFAULTBINARY = 799
    UA_NS0ID_SETPUBLISHINGMODERESPONSE = 800
    UA_NS0ID_SETPUBLISHINGMODERESPONSE_ENCODING_DEFAULTXML = 801
    UA_NS0ID_SETPUBLISHINGMODERESPONSE_ENCODING_DEFAULTBINARY = 802
    UA_NS0ID_NOTIFICATIONMESSAGE = 803
    UA_NS0ID_NOTIFICATIONMESSAGE_ENCODING_DEFAULTXML = 804
    UA_NS0ID_NOTIFICATIONMESSAGE_ENCODING_DEFAULTBINARY = 805
    UA_NS0ID_MONITOREDITEMNOTIFICATION = 806
    UA_NS0ID_MONITOREDITEMNOTIFICATION_ENCODING_DEFAULTXML = 807
    UA_NS0ID_MONITOREDITEMNOTIFICATION_ENCODING_DEFAULTBINARY = 808
    UA_NS0ID_DATACHANGENOTIFICATION = 809
    UA_NS0ID_DATACHANGENOTIFICATION_ENCODING_DEFAULTXML = 810
    UA_NS0ID_DATACHANGENOTIFICATION_ENCODING_DEFAULTBINARY = 811
    UA_NS0ID_STATUSCHANGENOTIFICATION = 818
    UA_NS0ID_STATUSCHANGENOTIFICATION_ENCODING_DEFAULTXML = 819
    UA_NS0ID_STATUSCHANGENOTIFICATION_ENCODING_DEFAULTBINARY = 820
    UA_NS0ID_SUBSCRIPTIONACKNOWLEDGEMENT = 821
    UA_NS0ID_SUBSCRIPTIONACKNOWLEDGEMENT_ENCODING_DEFAULTXML = 822
    UA_NS0ID_SUBSCRIPTIONACKNOWLEDGEMENT_ENCODING_DEFAULTBINARY = 823
    UA_NS0ID_PUBLISHREQUEST = 824
    UA_NS0ID_PUBLISHREQUEST_ENCODING_DEFAULTXML = 825
    UA_NS0ID_PUBLISHREQUEST_ENCODING_DEFAULTBINARY = 826
    UA_NS0ID_PUBLISHRESPONSE = 827
    UA_NS0ID_PUBLISHRESPONSE_ENCODING_DEFAULTXML = 828
    UA_NS0ID_PUBLISHRESPONSE_ENCODING_DEFAULTBINARY = 829
    UA_NS0ID_REPUBLISHREQUEST = 830
    UA_NS0ID_REPUBLISHREQUEST_ENCODING_DEFAULTXML = 831
    UA_NS0ID_REPUBLISHREQUEST_ENCODING_DEFAULTBINARY = 832
    UA_NS0ID_REPUBLISHRESPONSE = 833
    UA_NS0ID_REPUBLISHRESPONSE_ENCODING_DEFAULTXML = 834
    UA_NS0ID_REPUBLISHRESPONSE_ENCODING_DEFAULTBINARY = 835
    UA_NS0ID_TRANSFERRESULT = 836
    UA_NS0ID_TRANSFERRESULT_ENCODING_DEFAULTXML = 837
    UA_NS0ID_TRANSFERRESULT_ENCODING_DEFAULTBINARY = 838
    UA_NS0ID_TRANSFERSUBSCRIPTIONSREQUEST = 839
    UA_NS0ID_TRANSFERSUBSCRIPTIONSREQUEST_ENCODING_DEFAULTXML = 840
    UA_NS0ID_TRANSFERSUBSCRIPTIONSREQUEST_ENCODING_DEFAULTBINARY = 841
    UA_NS0ID_TRANSFERSUBSCRIPTIONSRESPONSE = 842
    UA_NS0ID_TRANSFERSUBSCRIPTIONSRESPONSE_ENCODING_DEFAULTXML = 843
    UA_NS0ID_TRANSFERSUBSCRIPTIONSRESPONSE_ENCODING_DEFAULTBINARY = 844
    UA_NS0ID_DELETESUBSCRIPTIONSREQUEST = 845
    UA_NS0ID_DELETESUBSCRIPTIONSREQUEST_ENCODING_DEFAULTXML = 846
    UA_NS0ID_DELETESUBSCRIPTIONSREQUEST_ENCODING_DEFAULTBINARY = 847
    UA_NS0ID_DELETESUBSCRIPTIONSRESPONSE = 848
    UA_NS0ID_DELETESUBSCRIPTIONSRESPONSE_ENCODING_DEFAULTXML = 849
    UA_NS0ID_DELETESUBSCRIPTIONSRESPONSE_ENCODING_DEFAULTBINARY = 850
    UA_NS0ID_REDUNDANCYSUPPORT = 851
    UA_NS0ID_SERVERSTATE = 852
    UA_NS0ID_REDUNDANTSERVERDATATYPE = 853
    UA_NS0ID_REDUNDANTSERVERDATATYPE_ENCODING_DEFAULTXML = 854
    UA_NS0ID_REDUNDANTSERVERDATATYPE_ENCODING_DEFAULTBINARY = 855
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSDATATYPE = 856
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSDATATYPE_ENCODING_DEFAULTXML = 857
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSDATATYPE_ENCODING_DEFAULTBINARY = 858
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYDATATYPE = 859
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYDATATYPE_ENCODING_DEFAULTXML = 860
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYDATATYPE_ENCODING_DEFAULTBINARY = 861
    UA_NS0ID_SERVERSTATUSDATATYPE = 862
    UA_NS0ID_SERVERSTATUSDATATYPE_ENCODING_DEFAULTXML = 863
    UA_NS0ID_SERVERSTATUSDATATYPE_ENCODING_DEFAULTBINARY = 864
    UA_NS0ID_SESSIONDIAGNOSTICSDATATYPE = 865
    UA_NS0ID_SESSIONDIAGNOSTICSDATATYPE_ENCODING_DEFAULTXML = 866
    UA_NS0ID_SESSIONDIAGNOSTICSDATATYPE_ENCODING_DEFAULTBINARY = 867
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSDATATYPE = 868
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSDATATYPE_ENCODING_DEFAULTXML = 869
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSDATATYPE_ENCODING_DEFAULTBINARY = 870
    UA_NS0ID_SERVICECOUNTERDATATYPE = 871
    UA_NS0ID_SERVICECOUNTERDATATYPE_ENCODING_DEFAULTXML = 872
    UA_NS0ID_SERVICECOUNTERDATATYPE_ENCODING_DEFAULTBINARY = 873
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSDATATYPE = 874
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSDATATYPE_ENCODING_DEFAULTXML = 875
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSDATATYPE_ENCODING_DEFAULTBINARY = 876
    UA_NS0ID_MODELCHANGESTRUCTUREDATATYPE = 877
    UA_NS0ID_MODELCHANGESTRUCTUREDATATYPE_ENCODING_DEFAULTXML = 878
    UA_NS0ID_MODELCHANGESTRUCTUREDATATYPE_ENCODING_DEFAULTBINARY = 879
    UA_NS0ID_RANGE = 884
    UA_NS0ID_RANGE_ENCODING_DEFAULTXML = 885
    UA_NS0ID_RANGE_ENCODING_DEFAULTBINARY = 886
    UA_NS0ID_EUINFORMATION = 887
    UA_NS0ID_EUINFORMATION_ENCODING_DEFAULTXML = 888
    UA_NS0ID_EUINFORMATION_ENCODING_DEFAULTBINARY = 889
    UA_NS0ID_EXCEPTIONDEVIATIONFORMAT = 890
    UA_NS0ID_ANNOTATION = 891
    UA_NS0ID_ANNOTATION_ENCODING_DEFAULTXML = 892
    UA_NS0ID_ANNOTATION_ENCODING_DEFAULTBINARY = 893
    UA_NS0ID_PROGRAMDIAGNOSTICDATATYPE = 894
    UA_NS0ID_PROGRAMDIAGNOSTICDATATYPE_ENCODING_DEFAULTXML = 895
    UA_NS0ID_PROGRAMDIAGNOSTICDATATYPE_ENCODING_DEFAULTBINARY = 896
    UA_NS0ID_SEMANTICCHANGESTRUCTUREDATATYPE = 897
    UA_NS0ID_SEMANTICCHANGESTRUCTUREDATATYPE_ENCODING_DEFAULTXML = 898
    UA_NS0ID_SEMANTICCHANGESTRUCTUREDATATYPE_ENCODING_DEFAULTBINARY = 899
    UA_NS0ID_EVENTNOTIFICATIONLIST = 914
    UA_NS0ID_EVENTNOTIFICATIONLIST_ENCODING_DEFAULTXML = 915
    UA_NS0ID_EVENTNOTIFICATIONLIST_ENCODING_DEFAULTBINARY = 916
    UA_NS0ID_EVENTFIELDLIST = 917
    UA_NS0ID_EVENTFIELDLIST_ENCODING_DEFAULTXML = 918
    UA_NS0ID_EVENTFIELDLIST_ENCODING_DEFAULTBINARY = 919
    UA_NS0ID_HISTORYEVENTFIELDLIST = 920
    UA_NS0ID_HISTORYEVENTFIELDLIST_ENCODING_DEFAULTXML = 921
    UA_NS0ID_HISTORYEVENTFIELDLIST_ENCODING_DEFAULTBINARY = 922
    UA_NS0ID_ISSUEDIDENTITYTOKEN = 938
    UA_NS0ID_ISSUEDIDENTITYTOKEN_ENCODING_DEFAULTXML = 939
    UA_NS0ID_ISSUEDIDENTITYTOKEN_ENCODING_DEFAULTBINARY = 940
    UA_NS0ID_NOTIFICATIONDATA = 945
    UA_NS0ID_NOTIFICATIONDATA_ENCODING_DEFAULTXML = 946
    UA_NS0ID_NOTIFICATIONDATA_ENCODING_DEFAULTBINARY = 947
    UA_NS0ID_AGGREGATECONFIGURATION = 948
    UA_NS0ID_AGGREGATECONFIGURATION_ENCODING_DEFAULTXML = 949
    UA_NS0ID_AGGREGATECONFIGURATION_ENCODING_DEFAULTBINARY = 950
    UA_NS0ID_IMAGEBMP = 2000
    UA_NS0ID_IMAGEGIF = 2001
    UA_NS0ID_IMAGEJPG = 2002
    UA_NS0ID_IMAGEPNG = 2003
    UA_NS0ID_SERVERTYPE = 2004
    UA_NS0ID_SERVERTYPE_SERVERARRAY = 2005
    UA_NS0ID_SERVERTYPE_NAMESPACEARRAY = 2006
    UA_NS0ID_SERVERTYPE_SERVERSTATUS = 2007
    UA_NS0ID_SERVERTYPE_SERVICELEVEL = 2008
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES = 2009
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS = 2010
    UA_NS0ID_SERVERTYPE_VENDORSERVERINFO = 2011
    UA_NS0ID_SERVERTYPE_SERVERREDUNDANCY = 2012
    UA_NS0ID_SERVERCAPABILITIESTYPE = 2013
    UA_NS0ID_SERVERCAPABILITIESTYPE_SERVERPROFILEARRAY = 2014
    UA_NS0ID_SERVERCAPABILITIESTYPE_LOCALEIDARRAY = 2016
    UA_NS0ID_SERVERCAPABILITIESTYPE_MINSUPPORTEDSAMPLERATE = 2017
    UA_NS0ID_SERVERCAPABILITIESTYPE_MODELLINGRULES = 2019
    UA_NS0ID_SERVERDIAGNOSTICSTYPE = 2020
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY = 2021
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SAMPLINGINTERVALDIAGNOSTICSARRAY = 2022
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SUBSCRIPTIONDIAGNOSTICSARRAY = 2023
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_ENABLEDFLAG = 2025
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE = 2026
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_SESSIONDIAGNOSTICSARRAY = 2027
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_SESSIONSECURITYDIAGNOSTICSARRAY = 2028
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE = 2029
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS = 2030
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS = 2031
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SUBSCRIPTIONDIAGNOSTICSARRAY = 2032
    UA_NS0ID_VENDORSERVERINFOTYPE = 2033
    UA_NS0ID_SERVERREDUNDANCYTYPE = 2034
    UA_NS0ID_SERVERREDUNDANCYTYPE_REDUNDANCYSUPPORT = 2035
    UA_NS0ID_TRANSPARENTREDUNDANCYTYPE = 2036
    UA_NS0ID_TRANSPARENTREDUNDANCYTYPE_CURRENTSERVERID = 2037
    UA_NS0ID_TRANSPARENTREDUNDANCYTYPE_REDUNDANTSERVERARRAY = 2038
    UA_NS0ID_NONTRANSPARENTREDUNDANCYTYPE = 2039
    UA_NS0ID_NONTRANSPARENTREDUNDANCYTYPE_SERVERURIARRAY = 2040
    UA_NS0ID_BASEEVENTTYPE = 2041
    UA_NS0ID_BASEEVENTTYPE_EVENTID = 2042
    UA_NS0ID_BASEEVENTTYPE_EVENTTYPE = 2043
    UA_NS0ID_BASEEVENTTYPE_SOURCENODE = 2044
    UA_NS0ID_BASEEVENTTYPE_SOURCENAME = 2045
    UA_NS0ID_BASEEVENTTYPE_TIME = 2046
    UA_NS0ID_BASEEVENTTYPE_RECEIVETIME = 2047
    UA_NS0ID_BASEEVENTTYPE_MESSAGE = 2050
    UA_NS0ID_BASEEVENTTYPE_SEVERITY = 2051
    UA_NS0ID_AUDITEVENTTYPE = 2052
    UA_NS0ID_AUDITEVENTTYPE_ACTIONTIMESTAMP = 2053
    UA_NS0ID_AUDITEVENTTYPE_STATUS = 2054
    UA_NS0ID_AUDITEVENTTYPE_SERVERID = 2055
    UA_NS0ID_AUDITEVENTTYPE_CLIENTAUDITENTRYID = 2056
    UA_NS0ID_AUDITEVENTTYPE_CLIENTUSERID = 2057
    UA_NS0ID_AUDITSECURITYEVENTTYPE = 2058
    UA_NS0ID_AUDITCHANNELEVENTTYPE = 2059
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE = 2060
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_CLIENTCERTIFICATE = 2061
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_REQUESTTYPE = 2062
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_SECURITYPOLICYURI = 2063
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_SECURITYMODE = 2065
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_REQUESTEDLIFETIME = 2066
    UA_NS0ID_AUDITSESSIONEVENTTYPE = 2069
    UA_NS0ID_AUDITSESSIONEVENTTYPE_SESSIONID = 2070
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE = 2071
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_SECURECHANNELID = 2072
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_CLIENTCERTIFICATE = 2073
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_REVISEDSESSIONTIMEOUT = 2074
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE = 2075
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_CLIENTSOFTWARECERTIFICATES = 2076
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_USERIDENTITYTOKEN = 2077
    UA_NS0ID_AUDITCANCELEVENTTYPE = 2078
    UA_NS0ID_AUDITCANCELEVENTTYPE_REQUESTHANDLE = 2079
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE = 2080
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_CERTIFICATE = 2081
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE = 2082
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_INVALIDHOSTNAME = 2083
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_INVALIDURI = 2084
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE = 2085
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE = 2086
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE = 2087
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE = 2088
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE = 2089
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE = 2090
    UA_NS0ID_AUDITADDNODESEVENTTYPE = 2091
    UA_NS0ID_AUDITADDNODESEVENTTYPE_NODESTOADD = 2092
    UA_NS0ID_AUDITDELETENODESEVENTTYPE = 2093
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_NODESTODELETE = 2094
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE = 2095
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_REFERENCESTOADD = 2096
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE = 2097
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_REFERENCESTODELETE = 2098
    UA_NS0ID_AUDITUPDATEEVENTTYPE = 2099
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE = 2100
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_INDEXRANGE = 2101
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_OLDVALUE = 2102
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_NEWVALUE = 2103
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE = 2104
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE = 2127
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_METHODID = 2128
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_INPUTARGUMENTS = 2129
    UA_NS0ID_SYSTEMEVENTTYPE = 2130
    UA_NS0ID_DEVICEFAILUREEVENTTYPE = 2131
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE = 2132
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE = 2133
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_CHANGES = 2134
    UA_NS0ID_SERVERVENDORCAPABILITYTYPE = 2137
    UA_NS0ID_SERVERSTATUSTYPE = 2138
    UA_NS0ID_SERVERSTATUSTYPE_STARTTIME = 2139
    UA_NS0ID_SERVERSTATUSTYPE_CURRENTTIME = 2140
    UA_NS0ID_SERVERSTATUSTYPE_STATE = 2141
    UA_NS0ID_SERVERSTATUSTYPE_BUILDINFO = 2142
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE = 2150
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_SERVERVIEWCOUNT = 2151
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_CURRENTSESSIONCOUNT = 2152
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_CUMULATEDSESSIONCOUNT = 2153
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_SECURITYREJECTEDSESSIONCOUNT = 2154
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_REJECTEDSESSIONCOUNT = 2155
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_SESSIONTIMEOUTCOUNT = 2156
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_SESSIONABORTCOUNT = 2157
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_PUBLISHINGINTERVALCOUNT = 2159
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_CURRENTSUBSCRIPTIONCOUNT = 2160
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_CUMULATEDSUBSCRIPTIONCOUNT = 2161
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_SECURITYREJECTEDREQUESTSCOUNT = 2162
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYTYPE_REJECTEDREQUESTSCOUNT = 2163
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSARRAYTYPE = 2164
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSTYPE = 2165
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSTYPE_SAMPLINGINTERVAL = 2166
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE = 2171
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE = 2172
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_SESSIONID = 2173
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_SUBSCRIPTIONID = 2174
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_PRIORITY = 2175
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_PUBLISHINGINTERVAL = 2176
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_MAXKEEPALIVECOUNT = 2177
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_MAXNOTIFICATIONSPERPUBLISH = 2179
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_PUBLISHINGENABLED = 2180
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_MODIFYCOUNT = 2181
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_ENABLECOUNT = 2182
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_DISABLECOUNT = 2183
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_REPUBLISHREQUESTCOUNT = 2184
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_REPUBLISHMESSAGEREQUESTCOUNT = 2185
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_REPUBLISHMESSAGECOUNT = 2186
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_TRANSFERREQUESTCOUNT = 2187
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_TRANSFERREDTOALTCLIENTCOUNT = 2188
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_TRANSFERREDTOSAMECLIENTCOUNT = 2189
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_PUBLISHREQUESTCOUNT = 2190
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_DATACHANGENOTIFICATIONSCOUNT = 2191
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_NOTIFICATIONSCOUNT = 2193
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE = 2196
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE = 2197
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_SESSIONID = 2198
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_SESSIONNAME = 2199
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_CLIENTDESCRIPTION = 2200
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_SERVERURI = 2201
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_ENDPOINTURL = 2202
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_LOCALEIDS = 2203
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_ACTUALSESSIONTIMEOUT = 2204
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_CLIENTCONNECTIONTIME = 2205
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_CLIENTLASTCONTACTTIME = 2206
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_CURRENTSUBSCRIPTIONSCOUNT = 2207
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_CURRENTMONITOREDITEMSCOUNT = 2208
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_CURRENTPUBLISHREQUESTSINQUEUE = 2209
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_READCOUNT = 2217
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_HISTORYREADCOUNT = 2218
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_WRITECOUNT = 2219
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_HISTORYUPDATECOUNT = 2220
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_CALLCOUNT = 2221
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_CREATEMONITOREDITEMSCOUNT = 2222
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_MODIFYMONITOREDITEMSCOUNT = 2223
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_SETMONITORINGMODECOUNT = 2224
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_SETTRIGGERINGCOUNT = 2225
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_DELETEMONITOREDITEMSCOUNT = 2226
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_CREATESUBSCRIPTIONCOUNT = 2227
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_MODIFYSUBSCRIPTIONCOUNT = 2228
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_SETPUBLISHINGMODECOUNT = 2229
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_PUBLISHCOUNT = 2230
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_REPUBLISHCOUNT = 2231
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_TRANSFERSUBSCRIPTIONSCOUNT = 2232
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_DELETESUBSCRIPTIONSCOUNT = 2233
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_ADDNODESCOUNT = 2234
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_ADDREFERENCESCOUNT = 2235
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_DELETENODESCOUNT = 2236
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_DELETEREFERENCESCOUNT = 2237
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_BROWSECOUNT = 2238
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_BROWSENEXTCOUNT = 2239
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_TRANSLATEBROWSEPATHSTONODEIDSCOUNT = 2240
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_QUERYFIRSTCOUNT = 2241
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_QUERYNEXTCOUNT = 2242
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE = 2243
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE = 2244
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE_SESSIONID = 2245
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE_CLIENTUSERIDOFSESSION = 2246
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE_CLIENTUSERIDHISTORY = 2247
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE_AUTHENTICATIONMECHANISM = 2248
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE_ENCODING = 2249
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE_TRANSPORTPROTOCOL = 2250
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE_SECURITYMODE = 2251
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE_SECURITYPOLICYURI = 2252
    UA_NS0ID_SERVER = 2253
    UA_NS0ID_SERVER_SERVERARRAY = 2254
    UA_NS0ID_SERVER_NAMESPACEARRAY = 2255
    UA_NS0ID_SERVER_SERVERSTATUS = 2256
    UA_NS0ID_SERVER_SERVERSTATUS_STARTTIME = 2257
    UA_NS0ID_SERVER_SERVERSTATUS_CURRENTTIME = 2258
    UA_NS0ID_SERVER_SERVERSTATUS_STATE = 2259
    UA_NS0ID_SERVER_SERVERSTATUS_BUILDINFO = 2260
    UA_NS0ID_SERVER_SERVERSTATUS_BUILDINFO_PRODUCTNAME = 2261
    UA_NS0ID_SERVER_SERVERSTATUS_BUILDINFO_PRODUCTURI = 2262
    UA_NS0ID_SERVER_SERVERSTATUS_BUILDINFO_MANUFACTURERNAME = 2263
    UA_NS0ID_SERVER_SERVERSTATUS_BUILDINFO_SOFTWAREVERSION = 2264
    UA_NS0ID_SERVER_SERVERSTATUS_BUILDINFO_BUILDNUMBER = 2265
    UA_NS0ID_SERVER_SERVERSTATUS_BUILDINFO_BUILDDATE = 2266
    UA_NS0ID_SERVER_SERVICELEVEL = 2267
    UA_NS0ID_SERVER_SERVERCAPABILITIES = 2268
    UA_NS0ID_SERVER_SERVERCAPABILITIES_SERVERPROFILEARRAY = 2269
    UA_NS0ID_SERVER_SERVERCAPABILITIES_LOCALEIDARRAY = 2271
    UA_NS0ID_SERVER_SERVERCAPABILITIES_MINSUPPORTEDSAMPLERATE = 2272
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS = 2274
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY = 2275
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SERVERVIEWCOUNT = 2276
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_CURRENTSESSIONCOUNT = 2277
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_CUMULATEDSESSIONCOUNT = 2278
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SECURITYREJECTEDSESSIONCOUNT = 2279
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SESSIONTIMEOUTCOUNT = 2281
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SESSIONABORTCOUNT = 2282
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_PUBLISHINGINTERVALCOUNT = 2284
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_CURRENTSUBSCRIPTIONCOUNT = 2285
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_CUMULATEDSUBSCRIPTIONCOUNT = 2286
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SECURITYREJECTEDREQUESTSCOUNT = 2287
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_REJECTEDREQUESTSCOUNT = 2288
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SAMPLINGINTERVALDIAGNOSTICSARRAY = 2289
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SUBSCRIPTIONDIAGNOSTICSARRAY = 2290
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_ENABLEDFLAG = 2294
    UA_NS0ID_SERVER_VENDORSERVERINFO = 2295
    UA_NS0ID_SERVER_SERVERREDUNDANCY = 2296
    UA_NS0ID_STATEMACHINETYPE = 2299
    UA_NS0ID_STATETYPE = 2307
    UA_NS0ID_STATETYPE_STATENUMBER = 2308
    UA_NS0ID_INITIALSTATETYPE = 2309
    UA_NS0ID_TRANSITIONTYPE = 2310
    UA_NS0ID_TRANSITIONEVENTTYPE = 2311
    UA_NS0ID_TRANSITIONTYPE_TRANSITIONNUMBER = 2312
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE = 2315
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE = 2318
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_STEPPED = 2323
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_DEFINITION = 2324
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_MAXTIMEINTERVAL = 2325
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_MINTIMEINTERVAL = 2326
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_EXCEPTIONDEVIATION = 2327
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_EXCEPTIONDEVIATIONFORMAT = 2328
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE = 2330
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_ACCESSHISTORYDATACAPABILITY = 2331
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_ACCESSHISTORYEVENTSCAPABILITY = 2332
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_INSERTDATACAPABILITY = 2334
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_REPLACEDATACAPABILITY = 2335
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_UPDATEDATACAPABILITY = 2336
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_DELETERAWCAPABILITY = 2337
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_DELETEATTIMECAPABILITY = 2338
    UA_NS0ID_AGGREGATEFUNCTIONTYPE = 2340
    UA_NS0ID_AGGREGATEFUNCTION_INTERPOLATIVE = 2341
    UA_NS0ID_AGGREGATEFUNCTION_AVERAGE = 2342
    UA_NS0ID_AGGREGATEFUNCTION_TIMEAVERAGE = 2343
    UA_NS0ID_AGGREGATEFUNCTION_TOTAL = 2344
    UA_NS0ID_AGGREGATEFUNCTION_MINIMUM = 2346
    UA_NS0ID_AGGREGATEFUNCTION_MAXIMUM = 2347
    UA_NS0ID_AGGREGATEFUNCTION_MINIMUMACTUALTIME = 2348
    UA_NS0ID_AGGREGATEFUNCTION_MAXIMUMACTUALTIME = 2349
    UA_NS0ID_AGGREGATEFUNCTION_RANGE = 2350
    UA_NS0ID_AGGREGATEFUNCTION_ANNOTATIONCOUNT = 2351
    UA_NS0ID_AGGREGATEFUNCTION_COUNT = 2352
    UA_NS0ID_AGGREGATEFUNCTION_NUMBEROFTRANSITIONS = 2355
    UA_NS0ID_AGGREGATEFUNCTION_START = 2357
    UA_NS0ID_AGGREGATEFUNCTION_END = 2358
    UA_NS0ID_AGGREGATEFUNCTION_DELTA = 2359
    UA_NS0ID_AGGREGATEFUNCTION_DURATIONGOOD = 2360
    UA_NS0ID_AGGREGATEFUNCTION_DURATIONBAD = 2361
    UA_NS0ID_AGGREGATEFUNCTION_PERCENTGOOD = 2362
    UA_NS0ID_AGGREGATEFUNCTION_PERCENTBAD = 2363
    UA_NS0ID_AGGREGATEFUNCTION_WORSTQUALITY = 2364
    UA_NS0ID_DATAITEMTYPE = 2365
    UA_NS0ID_DATAITEMTYPE_DEFINITION = 2366
    UA_NS0ID_DATAITEMTYPE_VALUEPRECISION = 2367
    UA_NS0ID_ANALOGITEMTYPE = 2368
    UA_NS0ID_ANALOGITEMTYPE_EURANGE = 2369
    UA_NS0ID_ANALOGITEMTYPE_INSTRUMENTRANGE = 2370
    UA_NS0ID_ANALOGITEMTYPE_ENGINEERINGUNITS = 2371
    UA_NS0ID_DISCRETEITEMTYPE = 2372
    UA_NS0ID_TWOSTATEDISCRETETYPE = 2373
    UA_NS0ID_TWOSTATEDISCRETETYPE_FALSESTATE = 2374
    UA_NS0ID_TWOSTATEDISCRETETYPE_TRUESTATE = 2375
    UA_NS0ID_MULTISTATEDISCRETETYPE = 2376
    UA_NS0ID_MULTISTATEDISCRETETYPE_ENUMSTRINGS = 2377
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE = 2378
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_INTERMEDIATERESULT = 2379
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE = 2380
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_CREATESESSIONID = 2381
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_CREATECLIENTNAME = 2382
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_INVOCATIONCREATIONTIME = 2383
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_LASTTRANSITIONTIME = 2384
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_LASTMETHODCALL = 2385
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_LASTMETHODSESSIONID = 2386
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_LASTMETHODINPUTARGUMENTS = 2387
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_LASTMETHODOUTPUTARGUMENTS = 2388
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_LASTMETHODCALLTIME = 2389
    UA_NS0ID_PROGRAMDIAGNOSTICTYPE_LASTMETHODRETURNSTATUS = 2390
    UA_NS0ID_PROGRAMSTATEMACHINETYPE = 2391
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_CREATABLE = 2392
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_DELETABLE = 2393
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_AUTODELETE = 2394
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RECYCLECOUNT = 2395
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_INSTANCECOUNT = 2396
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_MAXINSTANCECOUNT = 2397
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_MAXRECYCLECOUNT = 2398
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC = 2399
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_READY = 2400
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_READY_STATENUMBER = 2401
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RUNNING = 2402
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RUNNING_STATENUMBER = 2403
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_SUSPENDED = 2404
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_SUSPENDED_STATENUMBER = 2405
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_HALTED = 2406
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_HALTED_STATENUMBER = 2407
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_HALTEDTOREADY = 2408
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_HALTEDTOREADY_TRANSITIONNUMBER = 2409
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_READYTORUNNING = 2410
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_READYTORUNNING_TRANSITIONNUMBER = 2411
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RUNNINGTOHALTED = 2412
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RUNNINGTOHALTED_TRANSITIONNUMBER = 2413
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RUNNINGTOREADY = 2414
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RUNNINGTOREADY_TRANSITIONNUMBER = 2415
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RUNNINGTOSUSPENDED = 2416
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RUNNINGTOSUSPENDED_TRANSITIONNUMBER = 2417
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_SUSPENDEDTORUNNING = 2418
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_SUSPENDEDTORUNNING_TRANSITIONNUMBER = 2419
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_SUSPENDEDTOHALTED = 2420
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_SUSPENDEDTOHALTED_TRANSITIONNUMBER = 2421
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_SUSPENDEDTOREADY = 2422
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_SUSPENDEDTOREADY_TRANSITIONNUMBER = 2423
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_READYTOHALTED = 2424
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_READYTOHALTED_TRANSITIONNUMBER = 2425
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_START = 2426
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_SUSPEND = 2427
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RESUME = 2428
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_HALT = 2429
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_RESET = 2430
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_REGISTERNODESCOUNT = 2730
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_UNREGISTERNODESCOUNT = 2731
    UA_NS0ID_SERVERCAPABILITIESTYPE_MAXBROWSECONTINUATIONPOINTS = 2732
    UA_NS0ID_SERVERCAPABILITIESTYPE_MAXQUERYCONTINUATIONPOINTS = 2733
    UA_NS0ID_SERVERCAPABILITIESTYPE_MAXHISTORYCONTINUATIONPOINTS = 2734
    UA_NS0ID_SERVER_SERVERCAPABILITIES_MAXBROWSECONTINUATIONPOINTS = 2735
    UA_NS0ID_SERVER_SERVERCAPABILITIES_MAXQUERYCONTINUATIONPOINTS = 2736
    UA_NS0ID_SERVER_SERVERCAPABILITIES_MAXHISTORYCONTINUATIONPOINTS = 2737
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE = 2738
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_CHANGES = 2739
    UA_NS0ID_SERVERTYPE_AUDITING = 2742
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SESSIONSDIAGNOSTICSSUMMARY = 2744
    UA_NS0ID_AUDITCHANNELEVENTTYPE_SECURECHANNELID = 2745
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_CLIENTCERTIFICATETHUMBPRINT = 2746
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_CLIENTCERTIFICATETHUMBPRINT = 2747
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE = 2748
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_ENDPOINTURL = 2749
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_ATTRIBUTEID = 2750
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_PARAMETERDATATYPEID = 2751
    UA_NS0ID_SERVERSTATUSTYPE_SECONDSTILLSHUTDOWN = 2752
    UA_NS0ID_SERVERSTATUSTYPE_SHUTDOWNREASON = 2753
    UA_NS0ID_SERVERCAPABILITIESTYPE_AGGREGATEFUNCTIONS = 2754
    UA_NS0ID_STATEVARIABLETYPE = 2755
    UA_NS0ID_STATEVARIABLETYPE_ID = 2756
    UA_NS0ID_STATEVARIABLETYPE_NAME = 2757
    UA_NS0ID_STATEVARIABLETYPE_NUMBER = 2758
    UA_NS0ID_STATEVARIABLETYPE_EFFECTIVEDISPLAYNAME = 2759
    UA_NS0ID_FINITESTATEVARIABLETYPE = 2760
    UA_NS0ID_FINITESTATEVARIABLETYPE_ID = 2761
    UA_NS0ID_TRANSITIONVARIABLETYPE = 2762
    UA_NS0ID_TRANSITIONVARIABLETYPE_ID = 2763
    UA_NS0ID_TRANSITIONVARIABLETYPE_NAME = 2764
    UA_NS0ID_TRANSITIONVARIABLETYPE_NUMBER = 2765
    UA_NS0ID_TRANSITIONVARIABLETYPE_TRANSITIONTIME = 2766
    UA_NS0ID_FINITETRANSITIONVARIABLETYPE = 2767
    UA_NS0ID_FINITETRANSITIONVARIABLETYPE_ID = 2768
    UA_NS0ID_STATEMACHINETYPE_CURRENTSTATE = 2769
    UA_NS0ID_STATEMACHINETYPE_LASTTRANSITION = 2770
    UA_NS0ID_FINITESTATEMACHINETYPE = 2771
    UA_NS0ID_FINITESTATEMACHINETYPE_CURRENTSTATE = 2772
    UA_NS0ID_FINITESTATEMACHINETYPE_LASTTRANSITION = 2773
    UA_NS0ID_TRANSITIONEVENTTYPE_TRANSITION = 2774
    UA_NS0ID_TRANSITIONEVENTTYPE_FROMSTATE = 2775
    UA_NS0ID_TRANSITIONEVENTTYPE_TOSTATE = 2776
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_OLDSTATEID = 2777
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_NEWSTATEID = 2778
    UA_NS0ID_CONDITIONTYPE = 2782
    UA_NS0ID_REFRESHSTARTEVENTTYPE = 2787
    UA_NS0ID_REFRESHENDEVENTTYPE = 2788
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE = 2789
    UA_NS0ID_AUDITCONDITIONEVENTTYPE = 2790
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE = 2803
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE = 2829
    UA_NS0ID_DIALOGCONDITIONTYPE = 2830
    UA_NS0ID_DIALOGCONDITIONTYPE_PROMPT = 2831
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE = 2881
    UA_NS0ID_ALARMCONDITIONTYPE = 2915
    UA_NS0ID_SHELVEDSTATEMACHINETYPE = 2929
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_UNSHELVED = 2930
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_TIMEDSHELVED = 2932
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_ONESHOTSHELVED = 2933
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_UNSHELVEDTOTIMEDSHELVED = 2935
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_UNSHELVEDTOONESHOTSHELVED = 2936
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_TIMEDSHELVEDTOUNSHELVED = 2940
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_TIMEDSHELVEDTOONESHOTSHELVED = 2942
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_ONESHOTSHELVEDTOUNSHELVED = 2943
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_ONESHOTSHELVEDTOTIMEDSHELVED = 2945
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_UNSHELVE = 2947
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_ONESHOTSHELVE = 2948
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_TIMEDSHELVE = 2949
    UA_NS0ID_LIMITALARMTYPE = 2955
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_TIMEDSHELVE_INPUTARGUMENTS = 2991
    UA_NS0ID_SERVER_SERVERSTATUS_SECONDSTILLSHUTDOWN = 2992
    UA_NS0ID_SERVER_SERVERSTATUS_SHUTDOWNREASON = 2993
    UA_NS0ID_SERVER_AUDITING = 2994
    UA_NS0ID_SERVER_SERVERCAPABILITIES_MODELLINGRULES = 2996
    UA_NS0ID_SERVER_SERVERCAPABILITIES_AGGREGATEFUNCTIONS = 2997
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_EVENTNOTIFICATIONSCOUNT = 2998
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE = 2999
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_FILTER = 3003
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE = 3006
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE = 3012
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE = 3014
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_ISDELETEMODIFIED = 3015
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_STARTTIME = 3016
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_ENDTIME = 3017
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE = 3019
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_REQTIMES = 3020
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_OLDVALUES = 3021
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE = 3022
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_EVENTIDS = 3023
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_OLDVALUES = 3024
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_UPDATEDNODE = 3025
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_UPDATEDNODE = 3026
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_UPDATEDNODE = 3027
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_PERFORMINSERTREPLACE = 3028
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_NEWVALUES = 3029
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_OLDVALUES = 3030
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_PERFORMINSERTREPLACE = 3031
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_NEWVALUES = 3032
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_OLDVALUES = 3033
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_OLDVALUES = 3034
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE = 3035
    UA_NS0ID_EVENTTYPESFOLDER = 3048
    UA_NS0ID_SERVERCAPABILITIESTYPE_SOFTWARECERTIFICATES = 3049
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_MAXRESPONSEMESSAGESIZE = 3050
    UA_NS0ID_BUILDINFOTYPE = 3051
    UA_NS0ID_BUILDINFOTYPE_PRODUCTURI = 3052
    UA_NS0ID_BUILDINFOTYPE_MANUFACTURERNAME = 3053
    UA_NS0ID_BUILDINFOTYPE_PRODUCTNAME = 3054
    UA_NS0ID_BUILDINFOTYPE_SOFTWAREVERSION = 3055
    UA_NS0ID_BUILDINFOTYPE_BUILDNUMBER = 3056
    UA_NS0ID_BUILDINFOTYPE_BUILDDATE = 3057
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSTYPE_CLIENTCERTIFICATE = 3058
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_AGGREGATECONFIGURATION = 3059
    UA_NS0ID_DEFAULTBINARY = 3062
    UA_NS0ID_DEFAULTXML = 3063
    UA_NS0ID_ALWAYSGENERATESEVENT = 3065
    UA_NS0ID_ICON = 3067
    UA_NS0ID_NODEVERSION = 3068
    UA_NS0ID_LOCALTIME = 3069
    UA_NS0ID_ALLOWNULLS = 3070
    UA_NS0ID_ENUMVALUES = 3071
    UA_NS0ID_INPUTARGUMENTS = 3072
    UA_NS0ID_OUTPUTARGUMENTS = 3073
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_STARTTIME = 3074
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_CURRENTTIME = 3075
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_STATE = 3076
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_BUILDINFO = 3077
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_BUILDINFO_PRODUCTURI = 3078
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_BUILDINFO_MANUFACTURERNAME = 3079
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_BUILDINFO_PRODUCTNAME = 3080
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_BUILDINFO_SOFTWAREVERSION = 3081
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_BUILDINFO_BUILDNUMBER = 3082
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_BUILDINFO_BUILDDATE = 3083
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_SECONDSTILLSHUTDOWN = 3084
    UA_NS0ID_SERVERTYPE_SERVERSTATUS_SHUTDOWNREASON = 3085
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_SERVERPROFILEARRAY = 3086
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_LOCALEIDARRAY = 3087
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_MINSUPPORTEDSAMPLERATE = 3088
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_MAXBROWSECONTINUATIONPOINTS = 3089
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_MAXQUERYCONTINUATIONPOINTS = 3090
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_MAXHISTORYCONTINUATIONPOINTS = 3091
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_SOFTWARECERTIFICATES = 3092
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_MODELLINGRULES = 3093
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_AGGREGATEFUNCTIONS = 3094
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY = 3095
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SERVERVIEWCOUNT = 3096
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_CURRENTSESSIONCOUNT = 3097
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_CUMULATEDSESSIONCOUNT = 3098
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SECURITYREJECTEDSESSIONCOUNT = 3099
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_REJECTEDSESSIONCOUNT = 3100
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SESSIONTIMEOUTCOUNT = 3101
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SESSIONABORTCOUNT = 3102
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_PUBLISHINGINTERVALCOUNT = 3104
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_CURRENTSUBSCRIPTIONCOUNT = 3105
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_CUMULATEDSUBSCRIPTIONCOUNT = 3106
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_SECURITYREJECTEDREQUESTSCOUNT = 3107
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_REJECTEDREQUESTSCOUNT = 3108
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SAMPLINGINTERVALDIAGNOSTICSARRAY = 3109
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SUBSCRIPTIONDIAGNOSTICSARRAY = 3110
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SESSIONSDIAGNOSTICSSUMMARY = 3111
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SESSIONSDIAGNOSTICSSUMMARY_SESSIONDIAGNOSTICSARRAY = 3112
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_SESSIONSDIAGNOSTICSSUMMARY_SESSIONSECURITYDIAGNOSTICSARRAY = 3113
    UA_NS0ID_SERVERTYPE_SERVERDIAGNOSTICS_ENABLEDFLAG = 3114
    UA_NS0ID_SERVERTYPE_SERVERREDUNDANCY_REDUNDANCYSUPPORT = 3115
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_SERVERVIEWCOUNT = 3116
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_CURRENTSESSIONCOUNT = 3117
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_CUMULATEDSESSIONCOUNT = 3118
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_SECURITYREJECTEDSESSIONCOUNT = 3119
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_REJECTEDSESSIONCOUNT = 3120
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_SESSIONTIMEOUTCOUNT = 3121
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_SESSIONABORTCOUNT = 3122
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_PUBLISHINGINTERVALCOUNT = 3124
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_CURRENTSUBSCRIPTIONCOUNT = 3125
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_CUMULATEDSUBSCRIPTIONCOUNT = 3126
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_SECURITYREJECTEDREQUESTSCOUNT = 3127
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SERVERDIAGNOSTICSSUMMARY_REJECTEDREQUESTSCOUNT = 3128
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SESSIONSDIAGNOSTICSSUMMARY_SESSIONDIAGNOSTICSARRAY = 3129
    UA_NS0ID_SERVERDIAGNOSTICSTYPE_SESSIONSDIAGNOSTICSSUMMARY_SESSIONSECURITYDIAGNOSTICSARRAY = 3130
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_SESSIONID = 3131
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_SESSIONNAME = 3132
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_CLIENTDESCRIPTION = 3133
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_SERVERURI = 3134
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_ENDPOINTURL = 3135
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_LOCALEIDS = 3136
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_ACTUALSESSIONTIMEOUT = 3137
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_MAXRESPONSEMESSAGESIZE = 3138
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_CLIENTCONNECTIONTIME = 3139
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_CLIENTLASTCONTACTTIME = 3140
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_CURRENTSUBSCRIPTIONSCOUNT = 3141
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_CURRENTMONITOREDITEMSCOUNT = 3142
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_CURRENTPUBLISHREQUESTSINQUEUE = 3143
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_READCOUNT = 3151
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_HISTORYREADCOUNT = 3152
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_WRITECOUNT = 3153
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_HISTORYUPDATECOUNT = 3154
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_CALLCOUNT = 3155
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_CREATEMONITOREDITEMSCOUNT = 3156
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_MODIFYMONITOREDITEMSCOUNT = 3157
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_SETMONITORINGMODECOUNT = 3158
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_SETTRIGGERINGCOUNT = 3159
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_DELETEMONITOREDITEMSCOUNT = 3160
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_CREATESUBSCRIPTIONCOUNT = 3161
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_MODIFYSUBSCRIPTIONCOUNT = 3162
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_SETPUBLISHINGMODECOUNT = 3163
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_PUBLISHCOUNT = 3164
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_REPUBLISHCOUNT = 3165
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_TRANSFERSUBSCRIPTIONSCOUNT = 3166
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_DELETESUBSCRIPTIONSCOUNT = 3167
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_ADDNODESCOUNT = 3168
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_ADDREFERENCESCOUNT = 3169
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_DELETENODESCOUNT = 3170
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_DELETEREFERENCESCOUNT = 3171
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_BROWSECOUNT = 3172
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_BROWSENEXTCOUNT = 3173
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_TRANSLATEBROWSEPATHSTONODEIDSCOUNT = 3174
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_QUERYFIRSTCOUNT = 3175
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_QUERYNEXTCOUNT = 3176
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_REGISTERNODESCOUNT = 3177
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_UNREGISTERNODESCOUNT = 3178
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS_SESSIONID = 3179
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS_CLIENTUSERIDOFSESSION = 3180
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS_CLIENTUSERIDHISTORY = 3181
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS_AUTHENTICATIONMECHANISM = 3182
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS_ENCODING = 3183
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS_TRANSPORTPROTOCOL = 3184
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS_SECURITYMODE = 3185
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS_SECURITYPOLICYURI = 3186
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONSECURITYDIAGNOSTICS_CLIENTCERTIFICATE = 3187
    UA_NS0ID_TRANSPARENTREDUNDANCYTYPE_REDUNDANCYSUPPORT = 3188
    UA_NS0ID_NONTRANSPARENTREDUNDANCYTYPE_REDUNDANCYSUPPORT = 3189
    UA_NS0ID_BASEEVENTTYPE_LOCALTIME = 3190
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE_EVENTID = 3191
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE_EVENTTYPE = 3192
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE_SOURCENODE = 3193
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE_SOURCENAME = 3194
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE_TIME = 3195
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE_RECEIVETIME = 3196
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE_LOCALTIME = 3197
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE_MESSAGE = 3198
    UA_NS0ID_EVENTQUEUEOVERFLOWEVENTTYPE_SEVERITY = 3199
    UA_NS0ID_AUDITEVENTTYPE_EVENTID = 3200
    UA_NS0ID_AUDITEVENTTYPE_EVENTTYPE = 3201
    UA_NS0ID_AUDITEVENTTYPE_SOURCENODE = 3202
    UA_NS0ID_AUDITEVENTTYPE_SOURCENAME = 3203
    UA_NS0ID_AUDITEVENTTYPE_TIME = 3204
    UA_NS0ID_AUDITEVENTTYPE_RECEIVETIME = 3205
    UA_NS0ID_AUDITEVENTTYPE_LOCALTIME = 3206
    UA_NS0ID_AUDITEVENTTYPE_MESSAGE = 3207
    UA_NS0ID_AUDITEVENTTYPE_SEVERITY = 3208
    UA_NS0ID_AUDITSECURITYEVENTTYPE_EVENTID = 3209
    UA_NS0ID_AUDITSECURITYEVENTTYPE_EVENTTYPE = 3210
    UA_NS0ID_AUDITSECURITYEVENTTYPE_SOURCENODE = 3211
    UA_NS0ID_AUDITSECURITYEVENTTYPE_SOURCENAME = 3212
    UA_NS0ID_AUDITSECURITYEVENTTYPE_TIME = 3213
    UA_NS0ID_AUDITSECURITYEVENTTYPE_RECEIVETIME = 3214
    UA_NS0ID_AUDITSECURITYEVENTTYPE_LOCALTIME = 3215
    UA_NS0ID_AUDITSECURITYEVENTTYPE_MESSAGE = 3216
    UA_NS0ID_AUDITSECURITYEVENTTYPE_SEVERITY = 3217
    UA_NS0ID_AUDITSECURITYEVENTTYPE_ACTIONTIMESTAMP = 3218
    UA_NS0ID_AUDITSECURITYEVENTTYPE_STATUS = 3219
    UA_NS0ID_AUDITSECURITYEVENTTYPE_SERVERID = 3220
    UA_NS0ID_AUDITSECURITYEVENTTYPE_CLIENTAUDITENTRYID = 3221
    UA_NS0ID_AUDITSECURITYEVENTTYPE_CLIENTUSERID = 3222
    UA_NS0ID_AUDITCHANNELEVENTTYPE_EVENTID = 3223
    UA_NS0ID_AUDITCHANNELEVENTTYPE_EVENTTYPE = 3224
    UA_NS0ID_AUDITCHANNELEVENTTYPE_SOURCENODE = 3225
    UA_NS0ID_AUDITCHANNELEVENTTYPE_SOURCENAME = 3226
    UA_NS0ID_AUDITCHANNELEVENTTYPE_TIME = 3227
    UA_NS0ID_AUDITCHANNELEVENTTYPE_RECEIVETIME = 3228
    UA_NS0ID_AUDITCHANNELEVENTTYPE_LOCALTIME = 3229
    UA_NS0ID_AUDITCHANNELEVENTTYPE_MESSAGE = 3230
    UA_NS0ID_AUDITCHANNELEVENTTYPE_SEVERITY = 3231
    UA_NS0ID_AUDITCHANNELEVENTTYPE_ACTIONTIMESTAMP = 3232
    UA_NS0ID_AUDITCHANNELEVENTTYPE_STATUS = 3233
    UA_NS0ID_AUDITCHANNELEVENTTYPE_SERVERID = 3234
    UA_NS0ID_AUDITCHANNELEVENTTYPE_CLIENTAUDITENTRYID = 3235
    UA_NS0ID_AUDITCHANNELEVENTTYPE_CLIENTUSERID = 3236
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_EVENTID = 3237
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_EVENTTYPE = 3238
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_SOURCENODE = 3239
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_SOURCENAME = 3240
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_TIME = 3241
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_RECEIVETIME = 3242
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_LOCALTIME = 3243
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_MESSAGE = 3244
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_SEVERITY = 3245
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_ACTIONTIMESTAMP = 3246
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_STATUS = 3247
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_SERVERID = 3248
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_CLIENTAUDITENTRYID = 3249
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_CLIENTUSERID = 3250
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_SECURECHANNELID = 3251
    UA_NS0ID_AUDITSESSIONEVENTTYPE_EVENTID = 3252
    UA_NS0ID_AUDITSESSIONEVENTTYPE_EVENTTYPE = 3253
    UA_NS0ID_AUDITSESSIONEVENTTYPE_SOURCENODE = 3254
    UA_NS0ID_AUDITSESSIONEVENTTYPE_SOURCENAME = 3255
    UA_NS0ID_AUDITSESSIONEVENTTYPE_TIME = 3256
    UA_NS0ID_AUDITSESSIONEVENTTYPE_RECEIVETIME = 3257
    UA_NS0ID_AUDITSESSIONEVENTTYPE_LOCALTIME = 3258
    UA_NS0ID_AUDITSESSIONEVENTTYPE_MESSAGE = 3259
    UA_NS0ID_AUDITSESSIONEVENTTYPE_SEVERITY = 3260
    UA_NS0ID_AUDITSESSIONEVENTTYPE_ACTIONTIMESTAMP = 3261
    UA_NS0ID_AUDITSESSIONEVENTTYPE_STATUS = 3262
    UA_NS0ID_AUDITSESSIONEVENTTYPE_SERVERID = 3263
    UA_NS0ID_AUDITSESSIONEVENTTYPE_CLIENTAUDITENTRYID = 3264
    UA_NS0ID_AUDITSESSIONEVENTTYPE_CLIENTUSERID = 3265
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_EVENTID = 3266
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_EVENTTYPE = 3267
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_SOURCENODE = 3268
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_SOURCENAME = 3269
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_TIME = 3270
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_RECEIVETIME = 3271
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_LOCALTIME = 3272
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_MESSAGE = 3273
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_SEVERITY = 3274
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_ACTIONTIMESTAMP = 3275
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_STATUS = 3276
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_SERVERID = 3277
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_CLIENTAUDITENTRYID = 3278
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_CLIENTUSERID = 3279
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_EVENTID = 3281
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_EVENTTYPE = 3282
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_SOURCENODE = 3283
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_SOURCENAME = 3284
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_TIME = 3285
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_RECEIVETIME = 3286
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_LOCALTIME = 3287
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_MESSAGE = 3288
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_SEVERITY = 3289
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_ACTIONTIMESTAMP = 3290
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_STATUS = 3291
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_SERVERID = 3292
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_CLIENTAUDITENTRYID = 3293
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_CLIENTUSERID = 3294
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_SECURECHANNELID = 3296
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_CLIENTCERTIFICATE = 3297
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_CLIENTCERTIFICATETHUMBPRINT = 3298
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_REVISEDSESSIONTIMEOUT = 3299
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_EVENTID = 3300
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_EVENTTYPE = 3301
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_SOURCENODE = 3302
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_SOURCENAME = 3303
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_TIME = 3304
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_RECEIVETIME = 3305
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_LOCALTIME = 3306
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_MESSAGE = 3307
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_SEVERITY = 3308
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_ACTIONTIMESTAMP = 3309
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_STATUS = 3310
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_SERVERID = 3311
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_CLIENTAUDITENTRYID = 3312
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_CLIENTUSERID = 3313
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_SESSIONID = 3314
    UA_NS0ID_AUDITCANCELEVENTTYPE_EVENTID = 3315
    UA_NS0ID_AUDITCANCELEVENTTYPE_EVENTTYPE = 3316
    UA_NS0ID_AUDITCANCELEVENTTYPE_SOURCENODE = 3317
    UA_NS0ID_AUDITCANCELEVENTTYPE_SOURCENAME = 3318
    UA_NS0ID_AUDITCANCELEVENTTYPE_TIME = 3319
    UA_NS0ID_AUDITCANCELEVENTTYPE_RECEIVETIME = 3320
    UA_NS0ID_AUDITCANCELEVENTTYPE_LOCALTIME = 3321
    UA_NS0ID_AUDITCANCELEVENTTYPE_MESSAGE = 3322
    UA_NS0ID_AUDITCANCELEVENTTYPE_SEVERITY = 3323
    UA_NS0ID_AUDITCANCELEVENTTYPE_ACTIONTIMESTAMP = 3324
    UA_NS0ID_AUDITCANCELEVENTTYPE_STATUS = 3325
    UA_NS0ID_AUDITCANCELEVENTTYPE_SERVERID = 3326
    UA_NS0ID_AUDITCANCELEVENTTYPE_CLIENTAUDITENTRYID = 3327
    UA_NS0ID_AUDITCANCELEVENTTYPE_CLIENTUSERID = 3328
    UA_NS0ID_AUDITCANCELEVENTTYPE_SESSIONID = 3329
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_EVENTID = 3330
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_EVENTTYPE = 3331
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_SOURCENODE = 3332
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_SOURCENAME = 3333
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_TIME = 3334
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_RECEIVETIME = 3335
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_LOCALTIME = 3336
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_MESSAGE = 3337
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_SEVERITY = 3338
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_ACTIONTIMESTAMP = 3339
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_STATUS = 3340
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_SERVERID = 3341
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_CLIENTAUDITENTRYID = 3342
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_CLIENTUSERID = 3343
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_EVENTID = 3344
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_EVENTTYPE = 3345
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_SOURCENODE = 3346
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_SOURCENAME = 3347
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_TIME = 3348
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_RECEIVETIME = 3349
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_LOCALTIME = 3350
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_MESSAGE = 3351
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_SEVERITY = 3352
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_ACTIONTIMESTAMP = 3353
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_STATUS = 3354
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_SERVERID = 3355
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_CLIENTAUDITENTRYID = 3356
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_CLIENTUSERID = 3357
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_CERTIFICATE = 3358
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_EVENTID = 3359
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_EVENTTYPE = 3360
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_SOURCENODE = 3361
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_SOURCENAME = 3362
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_TIME = 3363
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_RECEIVETIME = 3364
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_LOCALTIME = 3365
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_MESSAGE = 3366
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_SEVERITY = 3367
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_ACTIONTIMESTAMP = 3368
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_STATUS = 3369
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_SERVERID = 3370
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_CLIENTAUDITENTRYID = 3371
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_CLIENTUSERID = 3372
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_CERTIFICATE = 3373
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_EVENTID = 3374
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_EVENTTYPE = 3375
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_SOURCENODE = 3376
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_SOURCENAME = 3377
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_TIME = 3378
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_RECEIVETIME = 3379
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_LOCALTIME = 3380
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_MESSAGE = 3381
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_SEVERITY = 3382
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_ACTIONTIMESTAMP = 3383
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_STATUS = 3384
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_SERVERID = 3385
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_CLIENTAUDITENTRYID = 3386
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_CLIENTUSERID = 3387
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_CERTIFICATE = 3388
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_EVENTID = 3389
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_EVENTTYPE = 3390
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_SOURCENODE = 3391
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_SOURCENAME = 3392
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_TIME = 3393
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_RECEIVETIME = 3394
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_LOCALTIME = 3395
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_MESSAGE = 3396
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_SEVERITY = 3397
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_ACTIONTIMESTAMP = 3398
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_STATUS = 3399
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_SERVERID = 3400
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_CLIENTAUDITENTRYID = 3401
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_CLIENTUSERID = 3402
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_CERTIFICATE = 3403
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_EVENTID = 3404
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_EVENTTYPE = 3405
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_SOURCENODE = 3406
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_SOURCENAME = 3407
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_TIME = 3408
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_RECEIVETIME = 3409
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_LOCALTIME = 3410
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_MESSAGE = 3411
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_SEVERITY = 3412
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_ACTIONTIMESTAMP = 3413
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_STATUS = 3414
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_SERVERID = 3415
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_CLIENTAUDITENTRYID = 3416
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_CLIENTUSERID = 3417
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_CERTIFICATE = 3418
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_EVENTID = 3419
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_EVENTTYPE = 3420
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_SOURCENODE = 3421
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_SOURCENAME = 3422
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_TIME = 3423
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_RECEIVETIME = 3424
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_LOCALTIME = 3425
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_MESSAGE = 3426
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_SEVERITY = 3427
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_ACTIONTIMESTAMP = 3428
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_STATUS = 3429
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_SERVERID = 3430
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_CLIENTAUDITENTRYID = 3431
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_CLIENTUSERID = 3432
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_CERTIFICATE = 3433
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_EVENTID = 3434
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_EVENTTYPE = 3435
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_SOURCENODE = 3436
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_SOURCENAME = 3437
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_TIME = 3438
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_RECEIVETIME = 3439
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_LOCALTIME = 3440
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_MESSAGE = 3441
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_SEVERITY = 3442
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_ACTIONTIMESTAMP = 3443
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_STATUS = 3444
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_SERVERID = 3445
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_CLIENTAUDITENTRYID = 3446
    UA_NS0ID_AUDITNODEMANAGEMENTEVENTTYPE_CLIENTUSERID = 3447
    UA_NS0ID_AUDITADDNODESEVENTTYPE_EVENTID = 3448
    UA_NS0ID_AUDITADDNODESEVENTTYPE_EVENTTYPE = 3449
    UA_NS0ID_AUDITADDNODESEVENTTYPE_SOURCENODE = 3450
    UA_NS0ID_AUDITADDNODESEVENTTYPE_SOURCENAME = 3451
    UA_NS0ID_AUDITADDNODESEVENTTYPE_TIME = 3452
    UA_NS0ID_AUDITADDNODESEVENTTYPE_RECEIVETIME = 3453
    UA_NS0ID_AUDITADDNODESEVENTTYPE_LOCALTIME = 3454
    UA_NS0ID_AUDITADDNODESEVENTTYPE_MESSAGE = 3455
    UA_NS0ID_AUDITADDNODESEVENTTYPE_SEVERITY = 3456
    UA_NS0ID_AUDITADDNODESEVENTTYPE_ACTIONTIMESTAMP = 3457
    UA_NS0ID_AUDITADDNODESEVENTTYPE_STATUS = 3458
    UA_NS0ID_AUDITADDNODESEVENTTYPE_SERVERID = 3459
    UA_NS0ID_AUDITADDNODESEVENTTYPE_CLIENTAUDITENTRYID = 3460
    UA_NS0ID_AUDITADDNODESEVENTTYPE_CLIENTUSERID = 3461
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_EVENTID = 3462
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_EVENTTYPE = 3463
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_SOURCENODE = 3464
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_SOURCENAME = 3465
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_TIME = 3466
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_RECEIVETIME = 3467
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_LOCALTIME = 3468
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_MESSAGE = 3469
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_SEVERITY = 3470
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_ACTIONTIMESTAMP = 3471
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_STATUS = 3472
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_SERVERID = 3473
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_CLIENTAUDITENTRYID = 3474
    UA_NS0ID_AUDITDELETENODESEVENTTYPE_CLIENTUSERID = 3475
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_EVENTID = 3476
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_EVENTTYPE = 3477
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_SOURCENODE = 3478
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_SOURCENAME = 3479
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_TIME = 3480
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_RECEIVETIME = 3481
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_LOCALTIME = 3482
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_MESSAGE = 3483
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_SEVERITY = 3484
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_ACTIONTIMESTAMP = 3485
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_STATUS = 3486
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_SERVERID = 3487
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_CLIENTAUDITENTRYID = 3488
    UA_NS0ID_AUDITADDREFERENCESEVENTTYPE_CLIENTUSERID = 3489
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_EVENTID = 3490
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_EVENTTYPE = 3491
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_SOURCENODE = 3492
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_SOURCENAME = 3493
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_TIME = 3494
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_RECEIVETIME = 3495
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_LOCALTIME = 3496
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_MESSAGE = 3497
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_SEVERITY = 3498
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_ACTIONTIMESTAMP = 3499
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_STATUS = 3500
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_SERVERID = 3501
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_CLIENTAUDITENTRYID = 3502
    UA_NS0ID_AUDITDELETEREFERENCESEVENTTYPE_CLIENTUSERID = 3503
    UA_NS0ID_AUDITUPDATEEVENTTYPE_EVENTID = 3504
    UA_NS0ID_AUDITUPDATEEVENTTYPE_EVENTTYPE = 3505
    UA_NS0ID_AUDITUPDATEEVENTTYPE_SOURCENODE = 3506
    UA_NS0ID_AUDITUPDATEEVENTTYPE_SOURCENAME = 3507
    UA_NS0ID_AUDITUPDATEEVENTTYPE_TIME = 3508
    UA_NS0ID_AUDITUPDATEEVENTTYPE_RECEIVETIME = 3509
    UA_NS0ID_AUDITUPDATEEVENTTYPE_LOCALTIME = 3510
    UA_NS0ID_AUDITUPDATEEVENTTYPE_MESSAGE = 3511
    UA_NS0ID_AUDITUPDATEEVENTTYPE_SEVERITY = 3512
    UA_NS0ID_AUDITUPDATEEVENTTYPE_ACTIONTIMESTAMP = 3513
    UA_NS0ID_AUDITUPDATEEVENTTYPE_STATUS = 3514
    UA_NS0ID_AUDITUPDATEEVENTTYPE_SERVERID = 3515
    UA_NS0ID_AUDITUPDATEEVENTTYPE_CLIENTAUDITENTRYID = 3516
    UA_NS0ID_AUDITUPDATEEVENTTYPE_CLIENTUSERID = 3517
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_EVENTID = 3518
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_EVENTTYPE = 3519
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_SOURCENODE = 3520
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_SOURCENAME = 3521
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_TIME = 3522
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_RECEIVETIME = 3523
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_LOCALTIME = 3524
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_MESSAGE = 3525
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_SEVERITY = 3526
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_ACTIONTIMESTAMP = 3527
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_STATUS = 3528
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_SERVERID = 3529
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_CLIENTAUDITENTRYID = 3530
    UA_NS0ID_AUDITWRITEUPDATEEVENTTYPE_CLIENTUSERID = 3531
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_EVENTID = 3532
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_EVENTTYPE = 3533
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_SOURCENODE = 3534
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_SOURCENAME = 3535
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_TIME = 3536
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_RECEIVETIME = 3537
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_LOCALTIME = 3538
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_MESSAGE = 3539
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_SEVERITY = 3540
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_ACTIONTIMESTAMP = 3541
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_STATUS = 3542
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_SERVERID = 3543
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_CLIENTAUDITENTRYID = 3544
    UA_NS0ID_AUDITHISTORYUPDATEEVENTTYPE_CLIENTUSERID = 3545
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_EVENTID = 3546
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_EVENTTYPE = 3547
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_SOURCENODE = 3548
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_SOURCENAME = 3549
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_TIME = 3550
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_RECEIVETIME = 3551
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_LOCALTIME = 3552
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_MESSAGE = 3553
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_SEVERITY = 3554
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_ACTIONTIMESTAMP = 3555
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_STATUS = 3556
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_SERVERID = 3557
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_CLIENTAUDITENTRYID = 3558
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_CLIENTUSERID = 3559
    UA_NS0ID_AUDITHISTORYEVENTUPDATEEVENTTYPE_PARAMETERDATATYPEID = 3560
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_EVENTID = 3561
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_EVENTTYPE = 3562
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_SOURCENODE = 3563
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_SOURCENAME = 3564
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_TIME = 3565
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_RECEIVETIME = 3566
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_LOCALTIME = 3567
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_MESSAGE = 3568
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_SEVERITY = 3569
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_ACTIONTIMESTAMP = 3570
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_STATUS = 3571
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_SERVERID = 3572
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_CLIENTAUDITENTRYID = 3573
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_CLIENTUSERID = 3574
    UA_NS0ID_AUDITHISTORYVALUEUPDATEEVENTTYPE_PARAMETERDATATYPEID = 3575
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_EVENTID = 3576
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_EVENTTYPE = 3577
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_SOURCENODE = 3578
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_SOURCENAME = 3579
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_TIME = 3580
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_RECEIVETIME = 3581
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_LOCALTIME = 3582
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_MESSAGE = 3583
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_SEVERITY = 3584
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_ACTIONTIMESTAMP = 3585
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_STATUS = 3586
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_SERVERID = 3587
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_CLIENTAUDITENTRYID = 3588
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_CLIENTUSERID = 3589
    UA_NS0ID_AUDITHISTORYDELETEEVENTTYPE_PARAMETERDATATYPEID = 3590
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_EVENTID = 3591
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_EVENTTYPE = 3592
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_SOURCENODE = 3593
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_SOURCENAME = 3594
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_TIME = 3595
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_RECEIVETIME = 3596
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_LOCALTIME = 3597
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_MESSAGE = 3598
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_SEVERITY = 3599
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_ACTIONTIMESTAMP = 3600
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_STATUS = 3601
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_SERVERID = 3602
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_CLIENTAUDITENTRYID = 3603
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_CLIENTUSERID = 3604
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_PARAMETERDATATYPEID = 3605
    UA_NS0ID_AUDITHISTORYRAWMODIFYDELETEEVENTTYPE_UPDATEDNODE = 3606
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_EVENTID = 3607
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_EVENTTYPE = 3608
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_SOURCENODE = 3609
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_SOURCENAME = 3610
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_TIME = 3611
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_RECEIVETIME = 3612
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_LOCALTIME = 3613
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_MESSAGE = 3614
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_SEVERITY = 3615
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_ACTIONTIMESTAMP = 3616
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_STATUS = 3617
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_SERVERID = 3618
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_CLIENTAUDITENTRYID = 3619
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_CLIENTUSERID = 3620
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_PARAMETERDATATYPEID = 3621
    UA_NS0ID_AUDITHISTORYATTIMEDELETEEVENTTYPE_UPDATEDNODE = 3622
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_EVENTID = 3623
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_EVENTTYPE = 3624
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_SOURCENODE = 3625
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_SOURCENAME = 3626
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_TIME = 3627
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_RECEIVETIME = 3628
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_LOCALTIME = 3629
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_MESSAGE = 3630
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_SEVERITY = 3631
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_ACTIONTIMESTAMP = 3632
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_STATUS = 3633
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_SERVERID = 3634
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_CLIENTAUDITENTRYID = 3635
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_CLIENTUSERID = 3636
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_PARAMETERDATATYPEID = 3637
    UA_NS0ID_AUDITHISTORYEVENTDELETEEVENTTYPE_UPDATEDNODE = 3638
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_EVENTID = 3639
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_EVENTTYPE = 3640
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_SOURCENODE = 3641
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_SOURCENAME = 3642
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_TIME = 3643
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_RECEIVETIME = 3644
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_LOCALTIME = 3645
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_MESSAGE = 3646
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_SEVERITY = 3647
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_ACTIONTIMESTAMP = 3648
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_STATUS = 3649
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_SERVERID = 3650
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_CLIENTAUDITENTRYID = 3651
    UA_NS0ID_AUDITUPDATEMETHODEVENTTYPE_CLIENTUSERID = 3652
    UA_NS0ID_SYSTEMEVENTTYPE_EVENTID = 3653
    UA_NS0ID_SYSTEMEVENTTYPE_EVENTTYPE = 3654
    UA_NS0ID_SYSTEMEVENTTYPE_SOURCENODE = 3655
    UA_NS0ID_SYSTEMEVENTTYPE_SOURCENAME = 3656
    UA_NS0ID_SYSTEMEVENTTYPE_TIME = 3657
    UA_NS0ID_SYSTEMEVENTTYPE_RECEIVETIME = 3658
    UA_NS0ID_SYSTEMEVENTTYPE_LOCALTIME = 3659
    UA_NS0ID_SYSTEMEVENTTYPE_MESSAGE = 3660
    UA_NS0ID_SYSTEMEVENTTYPE_SEVERITY = 3661
    UA_NS0ID_DEVICEFAILUREEVENTTYPE_EVENTID = 3662
    UA_NS0ID_DEVICEFAILUREEVENTTYPE_EVENTTYPE = 3663
    UA_NS0ID_DEVICEFAILUREEVENTTYPE_SOURCENODE = 3664
    UA_NS0ID_DEVICEFAILUREEVENTTYPE_SOURCENAME = 3665
    UA_NS0ID_DEVICEFAILUREEVENTTYPE_TIME = 3666
    UA_NS0ID_DEVICEFAILUREEVENTTYPE_RECEIVETIME = 3667
    UA_NS0ID_DEVICEFAILUREEVENTTYPE_LOCALTIME = 3668
    UA_NS0ID_DEVICEFAILUREEVENTTYPE_MESSAGE = 3669
    UA_NS0ID_DEVICEFAILUREEVENTTYPE_SEVERITY = 3670
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE_EVENTID = 3671
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE_EVENTTYPE = 3672
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE_SOURCENODE = 3673
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE_SOURCENAME = 3674
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE_TIME = 3675
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE_RECEIVETIME = 3676
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE_LOCALTIME = 3677
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE_MESSAGE = 3678
    UA_NS0ID_BASEMODELCHANGEEVENTTYPE_SEVERITY = 3679
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_EVENTID = 3680
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_EVENTTYPE = 3681
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_SOURCENODE = 3682
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_SOURCENAME = 3683
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_TIME = 3684
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_RECEIVETIME = 3685
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_LOCALTIME = 3686
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_MESSAGE = 3687
    UA_NS0ID_GENERALMODELCHANGEEVENTTYPE_SEVERITY = 3688
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_EVENTID = 3689
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_EVENTTYPE = 3690
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_SOURCENODE = 3691
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_SOURCENAME = 3692
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_TIME = 3693
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_RECEIVETIME = 3694
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_LOCALTIME = 3695
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_MESSAGE = 3696
    UA_NS0ID_SEMANTICCHANGEEVENTTYPE_SEVERITY = 3697
    UA_NS0ID_SERVERSTATUSTYPE_BUILDINFO_PRODUCTURI = 3698
    UA_NS0ID_SERVERSTATUSTYPE_BUILDINFO_MANUFACTURERNAME = 3699
    UA_NS0ID_SERVERSTATUSTYPE_BUILDINFO_PRODUCTNAME = 3700
    UA_NS0ID_SERVERSTATUSTYPE_BUILDINFO_SOFTWAREVERSION = 3701
    UA_NS0ID_SERVERSTATUSTYPE_BUILDINFO_BUILDNUMBER = 3702
    UA_NS0ID_SERVERSTATUSTYPE_BUILDINFO_BUILDDATE = 3703
    UA_NS0ID_SERVER_SERVERCAPABILITIES_SOFTWARECERTIFICATES = 3704
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SERVERDIAGNOSTICSSUMMARY_REJECTEDSESSIONCOUNT = 3705
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SESSIONSDIAGNOSTICSSUMMARY = 3706
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SESSIONSDIAGNOSTICSSUMMARY_SESSIONDIAGNOSTICSARRAY = 3707
    UA_NS0ID_SERVER_SERVERDIAGNOSTICS_SESSIONSDIAGNOSTICSSUMMARY_SESSIONSECURITYDIAGNOSTICSARRAY = 3708
    UA_NS0ID_SERVER_SERVERREDUNDANCY_REDUNDANCYSUPPORT = 3709
    UA_NS0ID_FINITESTATEVARIABLETYPE_NAME = 3714
    UA_NS0ID_FINITESTATEVARIABLETYPE_NUMBER = 3715
    UA_NS0ID_FINITESTATEVARIABLETYPE_EFFECTIVEDISPLAYNAME = 3716
    UA_NS0ID_FINITETRANSITIONVARIABLETYPE_NAME = 3717
    UA_NS0ID_FINITETRANSITIONVARIABLETYPE_NUMBER = 3718
    UA_NS0ID_FINITETRANSITIONVARIABLETYPE_TRANSITIONTIME = 3719
    UA_NS0ID_STATEMACHINETYPE_CURRENTSTATE_ID = 3720
    UA_NS0ID_STATEMACHINETYPE_CURRENTSTATE_NAME = 3721
    UA_NS0ID_STATEMACHINETYPE_CURRENTSTATE_NUMBER = 3722
    UA_NS0ID_STATEMACHINETYPE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 3723
    UA_NS0ID_STATEMACHINETYPE_LASTTRANSITION_ID = 3724
    UA_NS0ID_STATEMACHINETYPE_LASTTRANSITION_NAME = 3725
    UA_NS0ID_STATEMACHINETYPE_LASTTRANSITION_NUMBER = 3726
    UA_NS0ID_STATEMACHINETYPE_LASTTRANSITION_TRANSITIONTIME = 3727
    UA_NS0ID_FINITESTATEMACHINETYPE_CURRENTSTATE_ID = 3728
    UA_NS0ID_FINITESTATEMACHINETYPE_CURRENTSTATE_NAME = 3729
    UA_NS0ID_FINITESTATEMACHINETYPE_CURRENTSTATE_NUMBER = 3730
    UA_NS0ID_FINITESTATEMACHINETYPE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 3731
    UA_NS0ID_FINITESTATEMACHINETYPE_LASTTRANSITION_ID = 3732
    UA_NS0ID_FINITESTATEMACHINETYPE_LASTTRANSITION_NAME = 3733
    UA_NS0ID_FINITESTATEMACHINETYPE_LASTTRANSITION_NUMBER = 3734
    UA_NS0ID_FINITESTATEMACHINETYPE_LASTTRANSITION_TRANSITIONTIME = 3735
    UA_NS0ID_INITIALSTATETYPE_STATENUMBER = 3736
    UA_NS0ID_TRANSITIONEVENTTYPE_EVENTID = 3737
    UA_NS0ID_TRANSITIONEVENTTYPE_EVENTTYPE = 3738
    UA_NS0ID_TRANSITIONEVENTTYPE_SOURCENODE = 3739
    UA_NS0ID_TRANSITIONEVENTTYPE_SOURCENAME = 3740
    UA_NS0ID_TRANSITIONEVENTTYPE_TIME = 3741
    UA_NS0ID_TRANSITIONEVENTTYPE_RECEIVETIME = 3742
    UA_NS0ID_TRANSITIONEVENTTYPE_LOCALTIME = 3743
    UA_NS0ID_TRANSITIONEVENTTYPE_MESSAGE = 3744
    UA_NS0ID_TRANSITIONEVENTTYPE_SEVERITY = 3745
    UA_NS0ID_TRANSITIONEVENTTYPE_FROMSTATE_ID = 3746
    UA_NS0ID_TRANSITIONEVENTTYPE_FROMSTATE_NAME = 3747
    UA_NS0ID_TRANSITIONEVENTTYPE_FROMSTATE_NUMBER = 3748
    UA_NS0ID_TRANSITIONEVENTTYPE_FROMSTATE_EFFECTIVEDISPLAYNAME = 3749
    UA_NS0ID_TRANSITIONEVENTTYPE_TOSTATE_ID = 3750
    UA_NS0ID_TRANSITIONEVENTTYPE_TOSTATE_NAME = 3751
    UA_NS0ID_TRANSITIONEVENTTYPE_TOSTATE_NUMBER = 3752
    UA_NS0ID_TRANSITIONEVENTTYPE_TOSTATE_EFFECTIVEDISPLAYNAME = 3753
    UA_NS0ID_TRANSITIONEVENTTYPE_TRANSITION_ID = 3754
    UA_NS0ID_TRANSITIONEVENTTYPE_TRANSITION_NAME = 3755
    UA_NS0ID_TRANSITIONEVENTTYPE_TRANSITION_NUMBER = 3756
    UA_NS0ID_TRANSITIONEVENTTYPE_TRANSITION_TRANSITIONTIME = 3757
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_EVENTID = 3758
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_EVENTTYPE = 3759
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_SOURCENODE = 3760
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_SOURCENAME = 3761
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_TIME = 3762
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_RECEIVETIME = 3763
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_LOCALTIME = 3764
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_MESSAGE = 3765
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_SEVERITY = 3766
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_ACTIONTIMESTAMP = 3767
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_STATUS = 3768
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_SERVERID = 3769
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_CLIENTAUDITENTRYID = 3770
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_CLIENTUSERID = 3771
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_METHODID = 3772
    UA_NS0ID_AUDITUPDATESTATEEVENTTYPE_INPUTARGUMENTS = 3773
    UA_NS0ID_ANALOGITEMTYPE_DEFINITION = 3774
    UA_NS0ID_ANALOGITEMTYPE_VALUEPRECISION = 3775
    UA_NS0ID_DISCRETEITEMTYPE_DEFINITION = 3776
    UA_NS0ID_DISCRETEITEMTYPE_VALUEPRECISION = 3777
    UA_NS0ID_TWOSTATEDISCRETETYPE_DEFINITION = 3778
    UA_NS0ID_TWOSTATEDISCRETETYPE_VALUEPRECISION = 3779
    UA_NS0ID_MULTISTATEDISCRETETYPE_DEFINITION = 3780
    UA_NS0ID_MULTISTATEDISCRETETYPE_VALUEPRECISION = 3781
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_EVENTID = 3782
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_EVENTTYPE = 3783
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_SOURCENODE = 3784
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_SOURCENAME = 3785
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TIME = 3786
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_RECEIVETIME = 3787
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_LOCALTIME = 3788
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_MESSAGE = 3789
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_SEVERITY = 3790
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_FROMSTATE = 3791
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_FROMSTATE_ID = 3792
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_FROMSTATE_NAME = 3793
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_FROMSTATE_NUMBER = 3794
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_FROMSTATE_EFFECTIVEDISPLAYNAME = 3795
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TOSTATE = 3796
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TOSTATE_ID = 3797
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TOSTATE_NAME = 3798
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TOSTATE_NUMBER = 3799
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TOSTATE_EFFECTIVEDISPLAYNAME = 3800
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TRANSITION = 3801
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TRANSITION_ID = 3802
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TRANSITION_NAME = 3803
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TRANSITION_NUMBER = 3804
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TRANSITION_TRANSITIONTIME = 3805
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE = 3806
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_EVENTID = 3807
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_EVENTTYPE = 3808
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_SOURCENODE = 3809
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_SOURCENAME = 3810
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_TIME = 3811
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_RECEIVETIME = 3812
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_LOCALTIME = 3813
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_MESSAGE = 3814
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_SEVERITY = 3815
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_ACTIONTIMESTAMP = 3816
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_STATUS = 3817
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_SERVERID = 3818
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_CLIENTAUDITENTRYID = 3819
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_CLIENTUSERID = 3820
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_METHODID = 3821
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_INPUTARGUMENTS = 3822
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_OLDSTATEID = 3823
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_NEWSTATEID = 3824
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_TRANSITION = 3825
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_TRANSITION_ID = 3826
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_TRANSITION_NAME = 3827
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_TRANSITION_NUMBER = 3828
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_TRANSITION_TRANSITIONTIME = 3829
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_CURRENTSTATE = 3830
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_CURRENTSTATE_ID = 3831
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_CURRENTSTATE_NAME = 3832
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_CURRENTSTATE_NUMBER = 3833
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 3834
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_LASTTRANSITION = 3835
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_LASTTRANSITION_ID = 3836
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_LASTTRANSITION_NAME = 3837
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_LASTTRANSITION_NUMBER = 3838
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_LASTTRANSITION_TRANSITIONTIME = 3839
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_CREATESESSIONID = 3840
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_CREATECLIENTNAME = 3841
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_INVOCATIONCREATIONTIME = 3842
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_LASTTRANSITIONTIME = 3843
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_LASTMETHODCALL = 3844
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_LASTMETHODSESSIONID = 3845
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_LASTMETHODINPUTARGUMENTS = 3846
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_LASTMETHODOUTPUTARGUMENTS = 3847
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_LASTMETHODCALLTIME = 3848
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_LASTMETHODRETURNSTATUS = 3849
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_FINALRESULTDATA = 3850
    UA_NS0ID_ADDCOMMENTMETHODTYPE = 3863
    UA_NS0ID_ADDCOMMENTMETHODTYPE_INPUTARGUMENTS = 3864
    UA_NS0ID_CONDITIONTYPE_EVENTID = 3865
    UA_NS0ID_CONDITIONTYPE_EVENTTYPE = 3866
    UA_NS0ID_CONDITIONTYPE_SOURCENODE = 3867
    UA_NS0ID_CONDITIONTYPE_SOURCENAME = 3868
    UA_NS0ID_CONDITIONTYPE_TIME = 3869
    UA_NS0ID_CONDITIONTYPE_RECEIVETIME = 3870
    UA_NS0ID_CONDITIONTYPE_LOCALTIME = 3871
    UA_NS0ID_CONDITIONTYPE_MESSAGE = 3872
    UA_NS0ID_CONDITIONTYPE_SEVERITY = 3873
    UA_NS0ID_CONDITIONTYPE_RETAIN = 3874
    UA_NS0ID_CONDITIONTYPE_CONDITIONREFRESH = 3875
    UA_NS0ID_CONDITIONTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 3876
    UA_NS0ID_REFRESHSTARTEVENTTYPE_EVENTID = 3969
    UA_NS0ID_REFRESHSTARTEVENTTYPE_EVENTTYPE = 3970
    UA_NS0ID_REFRESHSTARTEVENTTYPE_SOURCENODE = 3971
    UA_NS0ID_REFRESHSTARTEVENTTYPE_SOURCENAME = 3972
    UA_NS0ID_REFRESHSTARTEVENTTYPE_TIME = 3973
    UA_NS0ID_REFRESHSTARTEVENTTYPE_RECEIVETIME = 3974
    UA_NS0ID_REFRESHSTARTEVENTTYPE_LOCALTIME = 3975
    UA_NS0ID_REFRESHSTARTEVENTTYPE_MESSAGE = 3976
    UA_NS0ID_REFRESHSTARTEVENTTYPE_SEVERITY = 3977
    UA_NS0ID_REFRESHENDEVENTTYPE_EVENTID = 3978
    UA_NS0ID_REFRESHENDEVENTTYPE_EVENTTYPE = 3979
    UA_NS0ID_REFRESHENDEVENTTYPE_SOURCENODE = 3980
    UA_NS0ID_REFRESHENDEVENTTYPE_SOURCENAME = 3981
    UA_NS0ID_REFRESHENDEVENTTYPE_TIME = 3982
    UA_NS0ID_REFRESHENDEVENTTYPE_RECEIVETIME = 3983
    UA_NS0ID_REFRESHENDEVENTTYPE_LOCALTIME = 3984
    UA_NS0ID_REFRESHENDEVENTTYPE_MESSAGE = 3985
    UA_NS0ID_REFRESHENDEVENTTYPE_SEVERITY = 3986
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE_EVENTID = 3987
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE_EVENTTYPE = 3988
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE_SOURCENODE = 3989
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE_SOURCENAME = 3990
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE_TIME = 3991
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE_RECEIVETIME = 3992
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE_LOCALTIME = 3993
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE_MESSAGE = 3994
    UA_NS0ID_REFRESHREQUIREDEVENTTYPE_SEVERITY = 3995
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_EVENTID = 3996
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_EVENTTYPE = 3997
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_SOURCENODE = 3998
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_SOURCENAME = 3999
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_TIME = 4000
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_RECEIVETIME = 4001
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_LOCALTIME = 4002
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_MESSAGE = 4003
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_SEVERITY = 4004
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_ACTIONTIMESTAMP = 4005
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_STATUS = 4006
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_SERVERID = 4007
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_CLIENTAUDITENTRYID = 4008
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_CLIENTUSERID = 4009
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_METHODID = 4010
    UA_NS0ID_AUDITCONDITIONEVENTTYPE_INPUTARGUMENTS = 4011
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_EVENTID = 4106
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_EVENTTYPE = 4107
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_SOURCENODE = 4108
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_SOURCENAME = 4109
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_TIME = 4110
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_RECEIVETIME = 4111
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_LOCALTIME = 4112
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_MESSAGE = 4113
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_SEVERITY = 4114
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_ACTIONTIMESTAMP = 4115
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_STATUS = 4116
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_SERVERID = 4117
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_CLIENTAUDITENTRYID = 4118
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_CLIENTUSERID = 4119
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_METHODID = 4120
    UA_NS0ID_AUDITCONDITIONENABLEEVENTTYPE_INPUTARGUMENTS = 4121
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_EVENTID = 4170
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_EVENTTYPE = 4171
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_SOURCENODE = 4172
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_SOURCENAME = 4173
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_TIME = 4174
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_RECEIVETIME = 4175
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_LOCALTIME = 4176
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_MESSAGE = 4177
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_SEVERITY = 4178
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_ACTIONTIMESTAMP = 4179
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_STATUS = 4180
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_SERVERID = 4181
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_CLIENTAUDITENTRYID = 4182
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_CLIENTUSERID = 4183
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_METHODID = 4184
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_INPUTARGUMENTS = 4185
    UA_NS0ID_DIALOGCONDITIONTYPE_EVENTID = 4188
    UA_NS0ID_DIALOGCONDITIONTYPE_EVENTTYPE = 4189
    UA_NS0ID_DIALOGCONDITIONTYPE_SOURCENODE = 4190
    UA_NS0ID_DIALOGCONDITIONTYPE_SOURCENAME = 4191
    UA_NS0ID_DIALOGCONDITIONTYPE_TIME = 4192
    UA_NS0ID_DIALOGCONDITIONTYPE_RECEIVETIME = 4193
    UA_NS0ID_DIALOGCONDITIONTYPE_LOCALTIME = 4194
    UA_NS0ID_DIALOGCONDITIONTYPE_MESSAGE = 4195
    UA_NS0ID_DIALOGCONDITIONTYPE_SEVERITY = 4196
    UA_NS0ID_DIALOGCONDITIONTYPE_RETAIN = 4197
    UA_NS0ID_DIALOGCONDITIONTYPE_CONDITIONREFRESH = 4198
    UA_NS0ID_DIALOGCONDITIONTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 4199
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_EVENTID = 5113
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_EVENTTYPE = 5114
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_SOURCENODE = 5115
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_SOURCENAME = 5116
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_TIME = 5117
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_RECEIVETIME = 5118
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_LOCALTIME = 5119
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_MESSAGE = 5120
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_SEVERITY = 5121
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_RETAIN = 5122
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONDITIONREFRESH = 5123
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 5124
    UA_NS0ID_ALARMCONDITIONTYPE_EVENTID = 5540
    UA_NS0ID_ALARMCONDITIONTYPE_EVENTTYPE = 5541
    UA_NS0ID_ALARMCONDITIONTYPE_SOURCENODE = 5542
    UA_NS0ID_ALARMCONDITIONTYPE_SOURCENAME = 5543
    UA_NS0ID_ALARMCONDITIONTYPE_TIME = 5544
    UA_NS0ID_ALARMCONDITIONTYPE_RECEIVETIME = 5545
    UA_NS0ID_ALARMCONDITIONTYPE_LOCALTIME = 5546
    UA_NS0ID_ALARMCONDITIONTYPE_MESSAGE = 5547
    UA_NS0ID_ALARMCONDITIONTYPE_SEVERITY = 5548
    UA_NS0ID_ALARMCONDITIONTYPE_RETAIN = 5549
    UA_NS0ID_ALARMCONDITIONTYPE_CONDITIONREFRESH = 5550
    UA_NS0ID_ALARMCONDITIONTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 5551
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_CURRENTSTATE = 6088
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_CURRENTSTATE_ID = 6089
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_CURRENTSTATE_NAME = 6090
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_CURRENTSTATE_NUMBER = 6091
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 6092
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_LASTTRANSITION = 6093
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_LASTTRANSITION_ID = 6094
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_LASTTRANSITION_NAME = 6095
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_LASTTRANSITION_NUMBER = 6096
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_LASTTRANSITION_TRANSITIONTIME = 6097
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_UNSHELVED_STATENUMBER = 6098
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_TIMEDSHELVED_STATENUMBER = 6100
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_ONESHOTSHELVED_STATENUMBER = 6101
    UA_NS0ID_TIMEDSHELVEMETHODTYPE = 6102
    UA_NS0ID_TIMEDSHELVEMETHODTYPE_INPUTARGUMENTS = 6103
    UA_NS0ID_LIMITALARMTYPE_EVENTID = 6116
    UA_NS0ID_LIMITALARMTYPE_EVENTTYPE = 6117
    UA_NS0ID_LIMITALARMTYPE_SOURCENODE = 6118
    UA_NS0ID_LIMITALARMTYPE_SOURCENAME = 6119
    UA_NS0ID_LIMITALARMTYPE_TIME = 6120
    UA_NS0ID_LIMITALARMTYPE_RECEIVETIME = 6121
    UA_NS0ID_LIMITALARMTYPE_LOCALTIME = 6122
    UA_NS0ID_LIMITALARMTYPE_MESSAGE = 6123
    UA_NS0ID_LIMITALARMTYPE_SEVERITY = 6124
    UA_NS0ID_LIMITALARMTYPE_RETAIN = 6125
    UA_NS0ID_LIMITALARMTYPE_CONDITIONREFRESH = 6126
    UA_NS0ID_LIMITALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 6127
    UA_NS0ID_IDTYPE_ENUMSTRINGS = 7591
    UA_NS0ID_ENUMVALUETYPE = 7594
    UA_NS0ID_MESSAGESECURITYMODE_ENUMSTRINGS = 7595
    UA_NS0ID_USERTOKENTYPE_ENUMSTRINGS = 7596
    UA_NS0ID_APPLICATIONTYPE_ENUMSTRINGS = 7597
    UA_NS0ID_SECURITYTOKENREQUESTTYPE_ENUMSTRINGS = 7598
    UA_NS0ID_BROWSEDIRECTION_ENUMSTRINGS = 7603
    UA_NS0ID_FILTEROPERATOR_ENUMSTRINGS = 7605
    UA_NS0ID_TIMESTAMPSTORETURN_ENUMSTRINGS = 7606
    UA_NS0ID_MONITORINGMODE_ENUMSTRINGS = 7608
    UA_NS0ID_DATACHANGETRIGGER_ENUMSTRINGS = 7609
    UA_NS0ID_DEADBANDTYPE_ENUMSTRINGS = 7610
    UA_NS0ID_REDUNDANCYSUPPORT_ENUMSTRINGS = 7611
    UA_NS0ID_SERVERSTATE_ENUMSTRINGS = 7612
    UA_NS0ID_EXCEPTIONDEVIATIONFORMAT_ENUMSTRINGS = 7614
    UA_NS0ID_ENUMVALUETYPE_ENCODING_DEFAULTXML = 7616
    UA_NS0ID_OPCUA_BINARYSCHEMA = 7617
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPEVERSION = 7618
    UA_NS0ID_OPCUA_BINARYSCHEMA_NAMESPACEURI = 7619
    UA_NS0ID_OPCUA_BINARYSCHEMA_ARGUMENT = 7650
    UA_NS0ID_OPCUA_BINARYSCHEMA_ARGUMENT_DATATYPEVERSION = 7651
    UA_NS0ID_OPCUA_BINARYSCHEMA_ARGUMENT_DICTIONARYFRAGMENT = 7652
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMVALUETYPE = 7656
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMVALUETYPE_DATATYPEVERSION = 7657
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMVALUETYPE_DICTIONARYFRAGMENT = 7658
    UA_NS0ID_OPCUA_BINARYSCHEMA_STATUSRESULT = 7659
    UA_NS0ID_OPCUA_BINARYSCHEMA_STATUSRESULT_DATATYPEVERSION = 7660
    UA_NS0ID_OPCUA_BINARYSCHEMA_STATUSRESULT_DICTIONARYFRAGMENT = 7661
    UA_NS0ID_OPCUA_BINARYSCHEMA_USERTOKENPOLICY = 7662
    UA_NS0ID_OPCUA_BINARYSCHEMA_USERTOKENPOLICY_DATATYPEVERSION = 7663
    UA_NS0ID_OPCUA_BINARYSCHEMA_USERTOKENPOLICY_DICTIONARYFRAGMENT = 7664
    UA_NS0ID_OPCUA_BINARYSCHEMA_APPLICATIONDESCRIPTION = 7665
    UA_NS0ID_OPCUA_BINARYSCHEMA_APPLICATIONDESCRIPTION_DATATYPEVERSION = 7666
    UA_NS0ID_OPCUA_BINARYSCHEMA_APPLICATIONDESCRIPTION_DICTIONARYFRAGMENT = 7667
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTDESCRIPTION = 7668
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTDESCRIPTION_DATATYPEVERSION = 7669
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTDESCRIPTION_DICTIONARYFRAGMENT = 7670
    UA_NS0ID_OPCUA_BINARYSCHEMA_USERIDENTITYTOKEN = 7671
    UA_NS0ID_OPCUA_BINARYSCHEMA_USERIDENTITYTOKEN_DATATYPEVERSION = 7672
    UA_NS0ID_OPCUA_BINARYSCHEMA_USERIDENTITYTOKEN_DICTIONARYFRAGMENT = 7673
    UA_NS0ID_OPCUA_BINARYSCHEMA_ANONYMOUSIDENTITYTOKEN = 7674
    UA_NS0ID_OPCUA_BINARYSCHEMA_ANONYMOUSIDENTITYTOKEN_DATATYPEVERSION = 7675
    UA_NS0ID_OPCUA_BINARYSCHEMA_ANONYMOUSIDENTITYTOKEN_DICTIONARYFRAGMENT = 7676
    UA_NS0ID_OPCUA_BINARYSCHEMA_USERNAMEIDENTITYTOKEN = 7677
    UA_NS0ID_OPCUA_BINARYSCHEMA_USERNAMEIDENTITYTOKEN_DATATYPEVERSION = 7678
    UA_NS0ID_OPCUA_BINARYSCHEMA_USERNAMEIDENTITYTOKEN_DICTIONARYFRAGMENT = 7679
    UA_NS0ID_OPCUA_BINARYSCHEMA_X509IDENTITYTOKEN = 7680
    UA_NS0ID_OPCUA_BINARYSCHEMA_X509IDENTITYTOKEN_DATATYPEVERSION = 7681
    UA_NS0ID_OPCUA_BINARYSCHEMA_X509IDENTITYTOKEN_DICTIONARYFRAGMENT = 7682
    UA_NS0ID_OPCUA_BINARYSCHEMA_ISSUEDIDENTITYTOKEN = 7683
    UA_NS0ID_OPCUA_BINARYSCHEMA_ISSUEDIDENTITYTOKEN_DATATYPEVERSION = 7684
    UA_NS0ID_OPCUA_BINARYSCHEMA_ISSUEDIDENTITYTOKEN_DICTIONARYFRAGMENT = 7685
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTCONFIGURATION = 7686
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTCONFIGURATION_DATATYPEVERSION = 7687
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTCONFIGURATION_DICTIONARYFRAGMENT = 7688
    UA_NS0ID_OPCUA_BINARYSCHEMA_BUILDINFO = 7692
    UA_NS0ID_OPCUA_BINARYSCHEMA_BUILDINFO_DATATYPEVERSION = 7693
    UA_NS0ID_OPCUA_BINARYSCHEMA_BUILDINFO_DICTIONARYFRAGMENT = 7694
    UA_NS0ID_OPCUA_BINARYSCHEMA_SIGNEDSOFTWARECERTIFICATE = 7698
    UA_NS0ID_OPCUA_BINARYSCHEMA_SIGNEDSOFTWARECERTIFICATE_DATATYPEVERSION = 7699
    UA_NS0ID_OPCUA_BINARYSCHEMA_SIGNEDSOFTWARECERTIFICATE_DICTIONARYFRAGMENT = 7700
    UA_NS0ID_OPCUA_BINARYSCHEMA_ADDNODESITEM = 7728
    UA_NS0ID_OPCUA_BINARYSCHEMA_ADDNODESITEM_DATATYPEVERSION = 7729
    UA_NS0ID_OPCUA_BINARYSCHEMA_ADDNODESITEM_DICTIONARYFRAGMENT = 7730
    UA_NS0ID_OPCUA_BINARYSCHEMA_ADDREFERENCESITEM = 7731
    UA_NS0ID_OPCUA_BINARYSCHEMA_ADDREFERENCESITEM_DATATYPEVERSION = 7732
    UA_NS0ID_OPCUA_BINARYSCHEMA_ADDREFERENCESITEM_DICTIONARYFRAGMENT = 7733
    UA_NS0ID_OPCUA_BINARYSCHEMA_DELETENODESITEM = 7734
    UA_NS0ID_OPCUA_BINARYSCHEMA_DELETENODESITEM_DATATYPEVERSION = 7735
    UA_NS0ID_OPCUA_BINARYSCHEMA_DELETENODESITEM_DICTIONARYFRAGMENT = 7736
    UA_NS0ID_OPCUA_BINARYSCHEMA_DELETEREFERENCESITEM = 7737
    UA_NS0ID_OPCUA_BINARYSCHEMA_DELETEREFERENCESITEM_DATATYPEVERSION = 7738
    UA_NS0ID_OPCUA_BINARYSCHEMA_DELETEREFERENCESITEM_DICTIONARYFRAGMENT = 7739
    UA_NS0ID_OPCUA_BINARYSCHEMA_REGISTEREDSERVER = 7782
    UA_NS0ID_OPCUA_BINARYSCHEMA_REGISTEREDSERVER_DATATYPEVERSION = 7783
    UA_NS0ID_OPCUA_BINARYSCHEMA_REGISTEREDSERVER_DICTIONARYFRAGMENT = 7784
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONTENTFILTERELEMENT = 7929
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONTENTFILTERELEMENT_DATATYPEVERSION = 7930
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONTENTFILTERELEMENT_DICTIONARYFRAGMENT = 7931
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONTENTFILTER = 7932
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONTENTFILTER_DATATYPEVERSION = 7933
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONTENTFILTER_DICTIONARYFRAGMENT = 7934
    UA_NS0ID_OPCUA_BINARYSCHEMA_FILTEROPERAND = 7935
    UA_NS0ID_OPCUA_BINARYSCHEMA_FILTEROPERAND_DATATYPEVERSION = 7936
    UA_NS0ID_OPCUA_BINARYSCHEMA_FILTEROPERAND_DICTIONARYFRAGMENT = 7937
    UA_NS0ID_OPCUA_BINARYSCHEMA_ELEMENTOPERAND = 7938
    UA_NS0ID_OPCUA_BINARYSCHEMA_ELEMENTOPERAND_DATATYPEVERSION = 7939
    UA_NS0ID_OPCUA_BINARYSCHEMA_ELEMENTOPERAND_DICTIONARYFRAGMENT = 7940
    UA_NS0ID_OPCUA_BINARYSCHEMA_LITERALOPERAND = 7941
    UA_NS0ID_OPCUA_BINARYSCHEMA_LITERALOPERAND_DATATYPEVERSION = 7942
    UA_NS0ID_OPCUA_BINARYSCHEMA_LITERALOPERAND_DICTIONARYFRAGMENT = 7943
    UA_NS0ID_OPCUA_BINARYSCHEMA_ATTRIBUTEOPERAND = 7944
    UA_NS0ID_OPCUA_BINARYSCHEMA_ATTRIBUTEOPERAND_DATATYPEVERSION = 7945
    UA_NS0ID_OPCUA_BINARYSCHEMA_ATTRIBUTEOPERAND_DICTIONARYFRAGMENT = 7946
    UA_NS0ID_OPCUA_BINARYSCHEMA_SIMPLEATTRIBUTEOPERAND = 7947
    UA_NS0ID_OPCUA_BINARYSCHEMA_SIMPLEATTRIBUTEOPERAND_DATATYPEVERSION = 7948
    UA_NS0ID_OPCUA_BINARYSCHEMA_SIMPLEATTRIBUTEOPERAND_DICTIONARYFRAGMENT = 7949
    UA_NS0ID_OPCUA_BINARYSCHEMA_HISTORYEVENT = 8004
    UA_NS0ID_OPCUA_BINARYSCHEMA_HISTORYEVENT_DATATYPEVERSION = 8005
    UA_NS0ID_OPCUA_BINARYSCHEMA_HISTORYEVENT_DICTIONARYFRAGMENT = 8006
    UA_NS0ID_OPCUA_BINARYSCHEMA_MONITORINGFILTER = 8067
    UA_NS0ID_OPCUA_BINARYSCHEMA_MONITORINGFILTER_DATATYPEVERSION = 8068
    UA_NS0ID_OPCUA_BINARYSCHEMA_MONITORINGFILTER_DICTIONARYFRAGMENT = 8069
    UA_NS0ID_OPCUA_BINARYSCHEMA_EVENTFILTER = 8073
    UA_NS0ID_OPCUA_BINARYSCHEMA_EVENTFILTER_DATATYPEVERSION = 8074
    UA_NS0ID_OPCUA_BINARYSCHEMA_EVENTFILTER_DICTIONARYFRAGMENT = 8075
    UA_NS0ID_OPCUA_BINARYSCHEMA_AGGREGATECONFIGURATION = 8076
    UA_NS0ID_OPCUA_BINARYSCHEMA_AGGREGATECONFIGURATION_DATATYPEVERSION = 8077
    UA_NS0ID_OPCUA_BINARYSCHEMA_AGGREGATECONFIGURATION_DICTIONARYFRAGMENT = 8078
    UA_NS0ID_OPCUA_BINARYSCHEMA_HISTORYEVENTFIELDLIST = 8172
    UA_NS0ID_OPCUA_BINARYSCHEMA_HISTORYEVENTFIELDLIST_DATATYPEVERSION = 8173
    UA_NS0ID_OPCUA_BINARYSCHEMA_HISTORYEVENTFIELDLIST_DICTIONARYFRAGMENT = 8174
    UA_NS0ID_OPCUA_BINARYSCHEMA_REDUNDANTSERVERDATATYPE = 8208
    UA_NS0ID_OPCUA_BINARYSCHEMA_REDUNDANTSERVERDATATYPE_DATATYPEVERSION = 8209
    UA_NS0ID_OPCUA_BINARYSCHEMA_REDUNDANTSERVERDATATYPE_DICTIONARYFRAGMENT = 8210
    UA_NS0ID_OPCUA_BINARYSCHEMA_SAMPLINGINTERVALDIAGNOSTICSDATATYPE = 8211
    UA_NS0ID_OPCUA_BINARYSCHEMA_SAMPLINGINTERVALDIAGNOSTICSDATATYPE_DATATYPEVERSION = 8212
    UA_NS0ID_OPCUA_BINARYSCHEMA_SAMPLINGINTERVALDIAGNOSTICSDATATYPE_DICTIONARYFRAGMENT = 8213
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVERDIAGNOSTICSSUMMARYDATATYPE = 8214
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVERDIAGNOSTICSSUMMARYDATATYPE_DATATYPEVERSION = 8215
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVERDIAGNOSTICSSUMMARYDATATYPE_DICTIONARYFRAGMENT = 8216
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVERSTATUSDATATYPE = 8217
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVERSTATUSDATATYPE_DATATYPEVERSION = 8218
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVERSTATUSDATATYPE_DICTIONARYFRAGMENT = 8219
    UA_NS0ID_OPCUA_BINARYSCHEMA_SESSIONDIAGNOSTICSDATATYPE = 8220
    UA_NS0ID_OPCUA_BINARYSCHEMA_SESSIONDIAGNOSTICSDATATYPE_DATATYPEVERSION = 8221
    UA_NS0ID_OPCUA_BINARYSCHEMA_SESSIONDIAGNOSTICSDATATYPE_DICTIONARYFRAGMENT = 8222
    UA_NS0ID_OPCUA_BINARYSCHEMA_SESSIONSECURITYDIAGNOSTICSDATATYPE = 8223
    UA_NS0ID_OPCUA_BINARYSCHEMA_SESSIONSECURITYDIAGNOSTICSDATATYPE_DATATYPEVERSION = 8224
    UA_NS0ID_OPCUA_BINARYSCHEMA_SESSIONSECURITYDIAGNOSTICSDATATYPE_DICTIONARYFRAGMENT = 8225
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVICECOUNTERDATATYPE = 8226
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVICECOUNTERDATATYPE_DATATYPEVERSION = 8227
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVICECOUNTERDATATYPE_DICTIONARYFRAGMENT = 8228
    UA_NS0ID_OPCUA_BINARYSCHEMA_SUBSCRIPTIONDIAGNOSTICSDATATYPE = 8229
    UA_NS0ID_OPCUA_BINARYSCHEMA_SUBSCRIPTIONDIAGNOSTICSDATATYPE_DATATYPEVERSION = 8230
    UA_NS0ID_OPCUA_BINARYSCHEMA_SUBSCRIPTIONDIAGNOSTICSDATATYPE_DICTIONARYFRAGMENT = 8231
    UA_NS0ID_OPCUA_BINARYSCHEMA_MODELCHANGESTRUCTUREDATATYPE = 8232
    UA_NS0ID_OPCUA_BINARYSCHEMA_MODELCHANGESTRUCTUREDATATYPE_DATATYPEVERSION = 8233
    UA_NS0ID_OPCUA_BINARYSCHEMA_MODELCHANGESTRUCTUREDATATYPE_DICTIONARYFRAGMENT = 8234
    UA_NS0ID_OPCUA_BINARYSCHEMA_SEMANTICCHANGESTRUCTUREDATATYPE = 8235
    UA_NS0ID_OPCUA_BINARYSCHEMA_SEMANTICCHANGESTRUCTUREDATATYPE_DATATYPEVERSION = 8236
    UA_NS0ID_OPCUA_BINARYSCHEMA_SEMANTICCHANGESTRUCTUREDATATYPE_DICTIONARYFRAGMENT = 8237
    UA_NS0ID_OPCUA_BINARYSCHEMA_RANGE = 8238
    UA_NS0ID_OPCUA_BINARYSCHEMA_RANGE_DATATYPEVERSION = 8239
    UA_NS0ID_OPCUA_BINARYSCHEMA_RANGE_DICTIONARYFRAGMENT = 8240
    UA_NS0ID_OPCUA_BINARYSCHEMA_EUINFORMATION = 8241
    UA_NS0ID_OPCUA_BINARYSCHEMA_EUINFORMATION_DATATYPEVERSION = 8242
    UA_NS0ID_OPCUA_BINARYSCHEMA_EUINFORMATION_DICTIONARYFRAGMENT = 8243
    UA_NS0ID_OPCUA_BINARYSCHEMA_ANNOTATION = 8244
    UA_NS0ID_OPCUA_BINARYSCHEMA_ANNOTATION_DATATYPEVERSION = 8245
    UA_NS0ID_OPCUA_BINARYSCHEMA_ANNOTATION_DICTIONARYFRAGMENT = 8246
    UA_NS0ID_OPCUA_BINARYSCHEMA_PROGRAMDIAGNOSTICDATATYPE = 8247
    UA_NS0ID_OPCUA_BINARYSCHEMA_PROGRAMDIAGNOSTICDATATYPE_DATATYPEVERSION = 8248
    UA_NS0ID_OPCUA_BINARYSCHEMA_PROGRAMDIAGNOSTICDATATYPE_DICTIONARYFRAGMENT = 8249
    UA_NS0ID_ENUMVALUETYPE_ENCODING_DEFAULTBINARY = 8251
    UA_NS0ID_OPCUA_XMLSCHEMA = 8252
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPEVERSION = 8253
    UA_NS0ID_OPCUA_XMLSCHEMA_NAMESPACEURI = 8254
    UA_NS0ID_OPCUA_XMLSCHEMA_ARGUMENT = 8285
    UA_NS0ID_OPCUA_XMLSCHEMA_ARGUMENT_DATATYPEVERSION = 8286
    UA_NS0ID_OPCUA_XMLSCHEMA_ARGUMENT_DICTIONARYFRAGMENT = 8287
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMVALUETYPE = 8291
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMVALUETYPE_DATATYPEVERSION = 8292
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMVALUETYPE_DICTIONARYFRAGMENT = 8293
    UA_NS0ID_OPCUA_XMLSCHEMA_STATUSRESULT = 8294
    UA_NS0ID_OPCUA_XMLSCHEMA_STATUSRESULT_DATATYPEVERSION = 8295
    UA_NS0ID_OPCUA_XMLSCHEMA_STATUSRESULT_DICTIONARYFRAGMENT = 8296
    UA_NS0ID_OPCUA_XMLSCHEMA_USERTOKENPOLICY = 8297
    UA_NS0ID_OPCUA_XMLSCHEMA_USERTOKENPOLICY_DATATYPEVERSION = 8298
    UA_NS0ID_OPCUA_XMLSCHEMA_USERTOKENPOLICY_DICTIONARYFRAGMENT = 8299
    UA_NS0ID_OPCUA_XMLSCHEMA_APPLICATIONDESCRIPTION = 8300
    UA_NS0ID_OPCUA_XMLSCHEMA_APPLICATIONDESCRIPTION_DATATYPEVERSION = 8301
    UA_NS0ID_OPCUA_XMLSCHEMA_APPLICATIONDESCRIPTION_DICTIONARYFRAGMENT = 8302
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTDESCRIPTION = 8303
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTDESCRIPTION_DATATYPEVERSION = 8304
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTDESCRIPTION_DICTIONARYFRAGMENT = 8305
    UA_NS0ID_OPCUA_XMLSCHEMA_USERIDENTITYTOKEN = 8306
    UA_NS0ID_OPCUA_XMLSCHEMA_USERIDENTITYTOKEN_DATATYPEVERSION = 8307
    UA_NS0ID_OPCUA_XMLSCHEMA_USERIDENTITYTOKEN_DICTIONARYFRAGMENT = 8308
    UA_NS0ID_OPCUA_XMLSCHEMA_ANONYMOUSIDENTITYTOKEN = 8309
    UA_NS0ID_OPCUA_XMLSCHEMA_ANONYMOUSIDENTITYTOKEN_DATATYPEVERSION = 8310
    UA_NS0ID_OPCUA_XMLSCHEMA_ANONYMOUSIDENTITYTOKEN_DICTIONARYFRAGMENT = 8311
    UA_NS0ID_OPCUA_XMLSCHEMA_USERNAMEIDENTITYTOKEN = 8312
    UA_NS0ID_OPCUA_XMLSCHEMA_USERNAMEIDENTITYTOKEN_DATATYPEVERSION = 8313
    UA_NS0ID_OPCUA_XMLSCHEMA_USERNAMEIDENTITYTOKEN_DICTIONARYFRAGMENT = 8314
    UA_NS0ID_OPCUA_XMLSCHEMA_X509IDENTITYTOKEN = 8315
    UA_NS0ID_OPCUA_XMLSCHEMA_X509IDENTITYTOKEN_DATATYPEVERSION = 8316
    UA_NS0ID_OPCUA_XMLSCHEMA_X509IDENTITYTOKEN_DICTIONARYFRAGMENT = 8317
    UA_NS0ID_OPCUA_XMLSCHEMA_ISSUEDIDENTITYTOKEN = 8318
    UA_NS0ID_OPCUA_XMLSCHEMA_ISSUEDIDENTITYTOKEN_DATATYPEVERSION = 8319
    UA_NS0ID_OPCUA_XMLSCHEMA_ISSUEDIDENTITYTOKEN_DICTIONARYFRAGMENT = 8320
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTCONFIGURATION = 8321
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTCONFIGURATION_DATATYPEVERSION = 8322
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTCONFIGURATION_DICTIONARYFRAGMENT = 8323
    UA_NS0ID_OPCUA_XMLSCHEMA_BUILDINFO = 8327
    UA_NS0ID_OPCUA_XMLSCHEMA_BUILDINFO_DATATYPEVERSION = 8328
    UA_NS0ID_OPCUA_XMLSCHEMA_BUILDINFO_DICTIONARYFRAGMENT = 8329
    UA_NS0ID_OPCUA_XMLSCHEMA_SIGNEDSOFTWARECERTIFICATE = 8333
    UA_NS0ID_OPCUA_XMLSCHEMA_SIGNEDSOFTWARECERTIFICATE_DATATYPEVERSION = 8334
    UA_NS0ID_OPCUA_XMLSCHEMA_SIGNEDSOFTWARECERTIFICATE_DICTIONARYFRAGMENT = 8335
    UA_NS0ID_OPCUA_XMLSCHEMA_ADDNODESITEM = 8363
    UA_NS0ID_OPCUA_XMLSCHEMA_ADDNODESITEM_DATATYPEVERSION = 8364
    UA_NS0ID_OPCUA_XMLSCHEMA_ADDNODESITEM_DICTIONARYFRAGMENT = 8365
    UA_NS0ID_OPCUA_XMLSCHEMA_ADDREFERENCESITEM = 8366
    UA_NS0ID_OPCUA_XMLSCHEMA_ADDREFERENCESITEM_DATATYPEVERSION = 8367
    UA_NS0ID_OPCUA_XMLSCHEMA_ADDREFERENCESITEM_DICTIONARYFRAGMENT = 8368
    UA_NS0ID_OPCUA_XMLSCHEMA_DELETENODESITEM = 8369
    UA_NS0ID_OPCUA_XMLSCHEMA_DELETENODESITEM_DATATYPEVERSION = 8370
    UA_NS0ID_OPCUA_XMLSCHEMA_DELETENODESITEM_DICTIONARYFRAGMENT = 8371
    UA_NS0ID_OPCUA_XMLSCHEMA_DELETEREFERENCESITEM = 8372
    UA_NS0ID_OPCUA_XMLSCHEMA_DELETEREFERENCESITEM_DATATYPEVERSION = 8373
    UA_NS0ID_OPCUA_XMLSCHEMA_DELETEREFERENCESITEM_DICTIONARYFRAGMENT = 8374
    UA_NS0ID_OPCUA_XMLSCHEMA_REGISTEREDSERVER = 8417
    UA_NS0ID_OPCUA_XMLSCHEMA_REGISTEREDSERVER_DATATYPEVERSION = 8418
    UA_NS0ID_OPCUA_XMLSCHEMA_REGISTEREDSERVER_DICTIONARYFRAGMENT = 8419
    UA_NS0ID_OPCUA_XMLSCHEMA_CONTENTFILTERELEMENT = 8564
    UA_NS0ID_OPCUA_XMLSCHEMA_CONTENTFILTERELEMENT_DATATYPEVERSION = 8565
    UA_NS0ID_OPCUA_XMLSCHEMA_CONTENTFILTERELEMENT_DICTIONARYFRAGMENT = 8566
    UA_NS0ID_OPCUA_XMLSCHEMA_CONTENTFILTER = 8567
    UA_NS0ID_OPCUA_XMLSCHEMA_CONTENTFILTER_DATATYPEVERSION = 8568
    UA_NS0ID_OPCUA_XMLSCHEMA_CONTENTFILTER_DICTIONARYFRAGMENT = 8569
    UA_NS0ID_OPCUA_XMLSCHEMA_FILTEROPERAND = 8570
    UA_NS0ID_OPCUA_XMLSCHEMA_FILTEROPERAND_DATATYPEVERSION = 8571
    UA_NS0ID_OPCUA_XMLSCHEMA_FILTEROPERAND_DICTIONARYFRAGMENT = 8572
    UA_NS0ID_OPCUA_XMLSCHEMA_ELEMENTOPERAND = 8573
    UA_NS0ID_OPCUA_XMLSCHEMA_ELEMENTOPERAND_DATATYPEVERSION = 8574
    UA_NS0ID_OPCUA_XMLSCHEMA_ELEMENTOPERAND_DICTIONARYFRAGMENT = 8575
    UA_NS0ID_OPCUA_XMLSCHEMA_LITERALOPERAND = 8576
    UA_NS0ID_OPCUA_XMLSCHEMA_LITERALOPERAND_DATATYPEVERSION = 8577
    UA_NS0ID_OPCUA_XMLSCHEMA_LITERALOPERAND_DICTIONARYFRAGMENT = 8578
    UA_NS0ID_OPCUA_XMLSCHEMA_ATTRIBUTEOPERAND = 8579
    UA_NS0ID_OPCUA_XMLSCHEMA_ATTRIBUTEOPERAND_DATATYPEVERSION = 8580
    UA_NS0ID_OPCUA_XMLSCHEMA_ATTRIBUTEOPERAND_DICTIONARYFRAGMENT = 8581
    UA_NS0ID_OPCUA_XMLSCHEMA_SIMPLEATTRIBUTEOPERAND = 8582
    UA_NS0ID_OPCUA_XMLSCHEMA_SIMPLEATTRIBUTEOPERAND_DATATYPEVERSION = 8583
    UA_NS0ID_OPCUA_XMLSCHEMA_SIMPLEATTRIBUTEOPERAND_DICTIONARYFRAGMENT = 8584
    UA_NS0ID_OPCUA_XMLSCHEMA_HISTORYEVENT = 8639
    UA_NS0ID_OPCUA_XMLSCHEMA_HISTORYEVENT_DATATYPEVERSION = 8640
    UA_NS0ID_OPCUA_XMLSCHEMA_HISTORYEVENT_DICTIONARYFRAGMENT = 8641
    UA_NS0ID_OPCUA_XMLSCHEMA_MONITORINGFILTER = 8702
    UA_NS0ID_OPCUA_XMLSCHEMA_MONITORINGFILTER_DATATYPEVERSION = 8703
    UA_NS0ID_OPCUA_XMLSCHEMA_MONITORINGFILTER_DICTIONARYFRAGMENT = 8704
    UA_NS0ID_OPCUA_XMLSCHEMA_EVENTFILTER = 8708
    UA_NS0ID_OPCUA_XMLSCHEMA_EVENTFILTER_DATATYPEVERSION = 8709
    UA_NS0ID_OPCUA_XMLSCHEMA_EVENTFILTER_DICTIONARYFRAGMENT = 8710
    UA_NS0ID_OPCUA_XMLSCHEMA_AGGREGATECONFIGURATION = 8711
    UA_NS0ID_OPCUA_XMLSCHEMA_AGGREGATECONFIGURATION_DATATYPEVERSION = 8712
    UA_NS0ID_OPCUA_XMLSCHEMA_AGGREGATECONFIGURATION_DICTIONARYFRAGMENT = 8713
    UA_NS0ID_OPCUA_XMLSCHEMA_HISTORYEVENTFIELDLIST = 8807
    UA_NS0ID_OPCUA_XMLSCHEMA_HISTORYEVENTFIELDLIST_DATATYPEVERSION = 8808
    UA_NS0ID_OPCUA_XMLSCHEMA_HISTORYEVENTFIELDLIST_DICTIONARYFRAGMENT = 8809
    UA_NS0ID_OPCUA_XMLSCHEMA_REDUNDANTSERVERDATATYPE = 8843
    UA_NS0ID_OPCUA_XMLSCHEMA_REDUNDANTSERVERDATATYPE_DATATYPEVERSION = 8844
    UA_NS0ID_OPCUA_XMLSCHEMA_REDUNDANTSERVERDATATYPE_DICTIONARYFRAGMENT = 8845
    UA_NS0ID_OPCUA_XMLSCHEMA_SAMPLINGINTERVALDIAGNOSTICSDATATYPE = 8846
    UA_NS0ID_OPCUA_XMLSCHEMA_SAMPLINGINTERVALDIAGNOSTICSDATATYPE_DATATYPEVERSION = 8847
    UA_NS0ID_OPCUA_XMLSCHEMA_SAMPLINGINTERVALDIAGNOSTICSDATATYPE_DICTIONARYFRAGMENT = 8848
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVERDIAGNOSTICSSUMMARYDATATYPE = 8849
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVERDIAGNOSTICSSUMMARYDATATYPE_DATATYPEVERSION = 8850
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVERDIAGNOSTICSSUMMARYDATATYPE_DICTIONARYFRAGMENT = 8851
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVERSTATUSDATATYPE = 8852
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVERSTATUSDATATYPE_DATATYPEVERSION = 8853
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVERSTATUSDATATYPE_DICTIONARYFRAGMENT = 8854
    UA_NS0ID_OPCUA_XMLSCHEMA_SESSIONDIAGNOSTICSDATATYPE = 8855
    UA_NS0ID_OPCUA_XMLSCHEMA_SESSIONDIAGNOSTICSDATATYPE_DATATYPEVERSION = 8856
    UA_NS0ID_OPCUA_XMLSCHEMA_SESSIONDIAGNOSTICSDATATYPE_DICTIONARYFRAGMENT = 8857
    UA_NS0ID_OPCUA_XMLSCHEMA_SESSIONSECURITYDIAGNOSTICSDATATYPE = 8858
    UA_NS0ID_OPCUA_XMLSCHEMA_SESSIONSECURITYDIAGNOSTICSDATATYPE_DATATYPEVERSION = 8859
    UA_NS0ID_OPCUA_XMLSCHEMA_SESSIONSECURITYDIAGNOSTICSDATATYPE_DICTIONARYFRAGMENT = 8860
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVICECOUNTERDATATYPE = 8861
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVICECOUNTERDATATYPE_DATATYPEVERSION = 8862
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVICECOUNTERDATATYPE_DICTIONARYFRAGMENT = 8863
    UA_NS0ID_OPCUA_XMLSCHEMA_SUBSCRIPTIONDIAGNOSTICSDATATYPE = 8864
    UA_NS0ID_OPCUA_XMLSCHEMA_SUBSCRIPTIONDIAGNOSTICSDATATYPE_DATATYPEVERSION = 8865
    UA_NS0ID_OPCUA_XMLSCHEMA_SUBSCRIPTIONDIAGNOSTICSDATATYPE_DICTIONARYFRAGMENT = 8866
    UA_NS0ID_OPCUA_XMLSCHEMA_MODELCHANGESTRUCTUREDATATYPE = 8867
    UA_NS0ID_OPCUA_XMLSCHEMA_MODELCHANGESTRUCTUREDATATYPE_DATATYPEVERSION = 8868
    UA_NS0ID_OPCUA_XMLSCHEMA_MODELCHANGESTRUCTUREDATATYPE_DICTIONARYFRAGMENT = 8869
    UA_NS0ID_OPCUA_XMLSCHEMA_SEMANTICCHANGESTRUCTUREDATATYPE = 8870
    UA_NS0ID_OPCUA_XMLSCHEMA_SEMANTICCHANGESTRUCTUREDATATYPE_DATATYPEVERSION = 8871
    UA_NS0ID_OPCUA_XMLSCHEMA_SEMANTICCHANGESTRUCTUREDATATYPE_DICTIONARYFRAGMENT = 8872
    UA_NS0ID_OPCUA_XMLSCHEMA_RANGE = 8873
    UA_NS0ID_OPCUA_XMLSCHEMA_RANGE_DATATYPEVERSION = 8874
    UA_NS0ID_OPCUA_XMLSCHEMA_RANGE_DICTIONARYFRAGMENT = 8875
    UA_NS0ID_OPCUA_XMLSCHEMA_EUINFORMATION = 8876
    UA_NS0ID_OPCUA_XMLSCHEMA_EUINFORMATION_DATATYPEVERSION = 8877
    UA_NS0ID_OPCUA_XMLSCHEMA_EUINFORMATION_DICTIONARYFRAGMENT = 8878
    UA_NS0ID_OPCUA_XMLSCHEMA_ANNOTATION = 8879
    UA_NS0ID_OPCUA_XMLSCHEMA_ANNOTATION_DATATYPEVERSION = 8880
    UA_NS0ID_OPCUA_XMLSCHEMA_ANNOTATION_DICTIONARYFRAGMENT = 8881
    UA_NS0ID_OPCUA_XMLSCHEMA_PROGRAMDIAGNOSTICDATATYPE = 8882
    UA_NS0ID_OPCUA_XMLSCHEMA_PROGRAMDIAGNOSTICDATATYPE_DATATYPEVERSION = 8883
    UA_NS0ID_OPCUA_XMLSCHEMA_PROGRAMDIAGNOSTICDATATYPE_DICTIONARYFRAGMENT = 8884
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_MAXLIFETIMECOUNT = 8888
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_LATEPUBLISHREQUESTCOUNT = 8889
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_CURRENTKEEPALIVECOUNT = 8890
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_CURRENTLIFETIMECOUNT = 8891
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_UNACKNOWLEDGEDMESSAGECOUNT = 8892
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_DISCARDEDMESSAGECOUNT = 8893
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_MONITOREDITEMCOUNT = 8894
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_DISABLEDMONITOREDITEMCOUNT = 8895
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_MONITORINGQUEUEOVERFLOWCOUNT = 8896
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_NEXTSEQUENCENUMBER = 8897
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_TOTALREQUESTCOUNT = 8898
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_TOTALREQUESTCOUNT = 8900
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSTYPE_EVENTQUEUEOVERFLOWCOUNT = 8902
    UA_NS0ID_TIMEZONEDATATYPE = 8912
    UA_NS0ID_TIMEZONEDATATYPE_ENCODING_DEFAULTXML = 8913
    UA_NS0ID_OPCUA_BINARYSCHEMA_TIMEZONEDATATYPE = 8914
    UA_NS0ID_OPCUA_BINARYSCHEMA_TIMEZONEDATATYPE_DATATYPEVERSION = 8915
    UA_NS0ID_OPCUA_BINARYSCHEMA_TIMEZONEDATATYPE_DICTIONARYFRAGMENT = 8916
    UA_NS0ID_TIMEZONEDATATYPE_ENCODING_DEFAULTBINARY = 8917
    UA_NS0ID_OPCUA_XMLSCHEMA_TIMEZONEDATATYPE = 8918
    UA_NS0ID_OPCUA_XMLSCHEMA_TIMEZONEDATATYPE_DATATYPEVERSION = 8919
    UA_NS0ID_OPCUA_XMLSCHEMA_TIMEZONEDATATYPE_DICTIONARYFRAGMENT = 8920
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE = 8927
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_EVENTID = 8928
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_EVENTTYPE = 8929
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_SOURCENODE = 8930
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_SOURCENAME = 8931
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_TIME = 8932
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_RECEIVETIME = 8933
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_LOCALTIME = 8934
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_MESSAGE = 8935
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_SEVERITY = 8936
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_ACTIONTIMESTAMP = 8937
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_STATUS = 8938
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_SERVERID = 8939
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_CLIENTAUDITENTRYID = 8940
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_CLIENTUSERID = 8941
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_METHODID = 8942
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_INPUTARGUMENTS = 8943
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE = 8944
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_EVENTID = 8945
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_EVENTTYPE = 8946
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_SOURCENODE = 8947
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_SOURCENAME = 8948
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_TIME = 8949
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_RECEIVETIME = 8950
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_LOCALTIME = 8951
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_MESSAGE = 8952
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_SEVERITY = 8953
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_ACTIONTIMESTAMP = 8954
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_STATUS = 8955
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_SERVERID = 8956
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_CLIENTAUDITENTRYID = 8957
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_CLIENTUSERID = 8958
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_METHODID = 8959
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_INPUTARGUMENTS = 8960
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE = 8961
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_EVENTID = 8962
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_EVENTTYPE = 8963
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_SOURCENODE = 8964
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_SOURCENAME = 8965
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_TIME = 8966
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_RECEIVETIME = 8967
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_LOCALTIME = 8968
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_MESSAGE = 8969
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_SEVERITY = 8970
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_ACTIONTIMESTAMP = 8971
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_STATUS = 8972
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_SERVERID = 8973
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_CLIENTAUDITENTRYID = 8974
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_CLIENTUSERID = 8975
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_METHODID = 8976
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_INPUTARGUMENTS = 8977
    UA_NS0ID_TWOSTATEVARIABLETYPE = 8995
    UA_NS0ID_TWOSTATEVARIABLETYPE_ID = 8996
    UA_NS0ID_TWOSTATEVARIABLETYPE_NAME = 8997
    UA_NS0ID_TWOSTATEVARIABLETYPE_NUMBER = 8998
    UA_NS0ID_TWOSTATEVARIABLETYPE_EFFECTIVEDISPLAYNAME = 8999
    UA_NS0ID_TWOSTATEVARIABLETYPE_TRANSITIONTIME = 9000
    UA_NS0ID_TWOSTATEVARIABLETYPE_EFFECTIVETRANSITIONTIME = 9001
    UA_NS0ID_CONDITIONVARIABLETYPE = 9002
    UA_NS0ID_CONDITIONVARIABLETYPE_SOURCETIMESTAMP = 9003
    UA_NS0ID_HASTRUESUBSTATE = 9004
    UA_NS0ID_HASFALSESUBSTATE = 9005
    UA_NS0ID_HASCONDITION = 9006
    UA_NS0ID_CONDITIONREFRESHMETHODTYPE = 9007
    UA_NS0ID_CONDITIONREFRESHMETHODTYPE_INPUTARGUMENTS = 9008
    UA_NS0ID_CONDITIONTYPE_CONDITIONNAME = 9009
    UA_NS0ID_CONDITIONTYPE_BRANCHID = 9010
    UA_NS0ID_CONDITIONTYPE_ENABLEDSTATE = 9011
    UA_NS0ID_CONDITIONTYPE_ENABLEDSTATE_ID = 9012
    UA_NS0ID_CONDITIONTYPE_ENABLEDSTATE_NAME = 9013
    UA_NS0ID_CONDITIONTYPE_ENABLEDSTATE_NUMBER = 9014
    UA_NS0ID_CONDITIONTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9015
    UA_NS0ID_CONDITIONTYPE_ENABLEDSTATE_TRANSITIONTIME = 9016
    UA_NS0ID_CONDITIONTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9017
    UA_NS0ID_CONDITIONTYPE_ENABLEDSTATE_TRUESTATE = 9018
    UA_NS0ID_CONDITIONTYPE_ENABLEDSTATE_FALSESTATE = 9019
    UA_NS0ID_CONDITIONTYPE_QUALITY = 9020
    UA_NS0ID_CONDITIONTYPE_QUALITY_SOURCETIMESTAMP = 9021
    UA_NS0ID_CONDITIONTYPE_LASTSEVERITY = 9022
    UA_NS0ID_CONDITIONTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9023
    UA_NS0ID_CONDITIONTYPE_COMMENT = 9024
    UA_NS0ID_CONDITIONTYPE_COMMENT_SOURCETIMESTAMP = 9025
    UA_NS0ID_CONDITIONTYPE_CLIENTUSERID = 9026
    UA_NS0ID_CONDITIONTYPE_ENABLE = 9027
    UA_NS0ID_CONDITIONTYPE_DISABLE = 9028
    UA_NS0ID_CONDITIONTYPE_ADDCOMMENT = 9029
    UA_NS0ID_CONDITIONTYPE_ADDCOMMENT_INPUTARGUMENTS = 9030
    UA_NS0ID_DIALOGRESPONSEMETHODTYPE = 9031
    UA_NS0ID_DIALOGRESPONSEMETHODTYPE_INPUTARGUMENTS = 9032
    UA_NS0ID_DIALOGCONDITIONTYPE_CONDITIONNAME = 9033
    UA_NS0ID_DIALOGCONDITIONTYPE_BRANCHID = 9034
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLEDSTATE = 9035
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLEDSTATE_ID = 9036
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLEDSTATE_NAME = 9037
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLEDSTATE_NUMBER = 9038
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9039
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLEDSTATE_TRANSITIONTIME = 9040
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9041
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLEDSTATE_TRUESTATE = 9042
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLEDSTATE_FALSESTATE = 9043
    UA_NS0ID_DIALOGCONDITIONTYPE_QUALITY = 9044
    UA_NS0ID_DIALOGCONDITIONTYPE_QUALITY_SOURCETIMESTAMP = 9045
    UA_NS0ID_DIALOGCONDITIONTYPE_LASTSEVERITY = 9046
    UA_NS0ID_DIALOGCONDITIONTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9047
    UA_NS0ID_DIALOGCONDITIONTYPE_COMMENT = 9048
    UA_NS0ID_DIALOGCONDITIONTYPE_COMMENT_SOURCETIMESTAMP = 9049
    UA_NS0ID_DIALOGCONDITIONTYPE_CLIENTUSERID = 9050
    UA_NS0ID_DIALOGCONDITIONTYPE_ENABLE = 9051
    UA_NS0ID_DIALOGCONDITIONTYPE_DISABLE = 9052
    UA_NS0ID_DIALOGCONDITIONTYPE_ADDCOMMENT = 9053
    UA_NS0ID_DIALOGCONDITIONTYPE_ADDCOMMENT_INPUTARGUMENTS = 9054
    UA_NS0ID_DIALOGCONDITIONTYPE_DIALOGSTATE = 9055
    UA_NS0ID_DIALOGCONDITIONTYPE_DIALOGSTATE_ID = 9056
    UA_NS0ID_DIALOGCONDITIONTYPE_DIALOGSTATE_NAME = 9057
    UA_NS0ID_DIALOGCONDITIONTYPE_DIALOGSTATE_NUMBER = 9058
    UA_NS0ID_DIALOGCONDITIONTYPE_DIALOGSTATE_EFFECTIVEDISPLAYNAME = 9059
    UA_NS0ID_DIALOGCONDITIONTYPE_DIALOGSTATE_TRANSITIONTIME = 9060
    UA_NS0ID_DIALOGCONDITIONTYPE_DIALOGSTATE_EFFECTIVETRANSITIONTIME = 9061
    UA_NS0ID_DIALOGCONDITIONTYPE_DIALOGSTATE_TRUESTATE = 9062
    UA_NS0ID_DIALOGCONDITIONTYPE_DIALOGSTATE_FALSESTATE = 9063
    UA_NS0ID_DIALOGCONDITIONTYPE_RESPONSEOPTIONSET = 9064
    UA_NS0ID_DIALOGCONDITIONTYPE_DEFAULTRESPONSE = 9065
    UA_NS0ID_DIALOGCONDITIONTYPE_OKRESPONSE = 9066
    UA_NS0ID_DIALOGCONDITIONTYPE_CANCELRESPONSE = 9067
    UA_NS0ID_DIALOGCONDITIONTYPE_LASTRESPONSE = 9068
    UA_NS0ID_DIALOGCONDITIONTYPE_RESPOND = 9069
    UA_NS0ID_DIALOGCONDITIONTYPE_RESPOND_INPUTARGUMENTS = 9070
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONDITIONNAME = 9071
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_BRANCHID = 9072
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLEDSTATE = 9073
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLEDSTATE_ID = 9074
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLEDSTATE_NAME = 9075
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLEDSTATE_NUMBER = 9076
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9077
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLEDSTATE_TRANSITIONTIME = 9078
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9079
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLEDSTATE_TRUESTATE = 9080
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLEDSTATE_FALSESTATE = 9081
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_QUALITY = 9082
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_QUALITY_SOURCETIMESTAMP = 9083
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_LASTSEVERITY = 9084
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9085
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_COMMENT = 9086
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_COMMENT_SOURCETIMESTAMP = 9087
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CLIENTUSERID = 9088
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ENABLE = 9089
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_DISABLE = 9090
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ADDCOMMENT = 9091
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ADDCOMMENT_INPUTARGUMENTS = 9092
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKEDSTATE = 9093
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKEDSTATE_ID = 9094
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKEDSTATE_NAME = 9095
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKEDSTATE_NUMBER = 9096
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 9097
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKEDSTATE_TRANSITIONTIME = 9098
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 9099
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKEDSTATE_TRUESTATE = 9100
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKEDSTATE_FALSESTATE = 9101
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRMEDSTATE = 9102
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRMEDSTATE_ID = 9103
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRMEDSTATE_NAME = 9104
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRMEDSTATE_NUMBER = 9105
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 9106
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 9107
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 9108
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRMEDSTATE_TRUESTATE = 9109
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRMEDSTATE_FALSESTATE = 9110
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKNOWLEDGE = 9111
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 9112
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRM = 9113
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONFIRM_INPUTARGUMENTS = 9114
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_UNSHELVETIME = 9115
    UA_NS0ID_ALARMCONDITIONTYPE_CONDITIONNAME = 9116
    UA_NS0ID_ALARMCONDITIONTYPE_BRANCHID = 9117
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLEDSTATE = 9118
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLEDSTATE_ID = 9119
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLEDSTATE_NAME = 9120
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLEDSTATE_NUMBER = 9121
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9122
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLEDSTATE_TRANSITIONTIME = 9123
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9124
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLEDSTATE_TRUESTATE = 9125
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLEDSTATE_FALSESTATE = 9126
    UA_NS0ID_ALARMCONDITIONTYPE_QUALITY = 9127
    UA_NS0ID_ALARMCONDITIONTYPE_QUALITY_SOURCETIMESTAMP = 9128
    UA_NS0ID_ALARMCONDITIONTYPE_LASTSEVERITY = 9129
    UA_NS0ID_ALARMCONDITIONTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9130
    UA_NS0ID_ALARMCONDITIONTYPE_COMMENT = 9131
    UA_NS0ID_ALARMCONDITIONTYPE_COMMENT_SOURCETIMESTAMP = 9132
    UA_NS0ID_ALARMCONDITIONTYPE_CLIENTUSERID = 9133
    UA_NS0ID_ALARMCONDITIONTYPE_ENABLE = 9134
    UA_NS0ID_ALARMCONDITIONTYPE_DISABLE = 9135
    UA_NS0ID_ALARMCONDITIONTYPE_ADDCOMMENT = 9136
    UA_NS0ID_ALARMCONDITIONTYPE_ADDCOMMENT_INPUTARGUMENTS = 9137
    UA_NS0ID_ALARMCONDITIONTYPE_ACKEDSTATE = 9138
    UA_NS0ID_ALARMCONDITIONTYPE_ACKEDSTATE_ID = 9139
    UA_NS0ID_ALARMCONDITIONTYPE_ACKEDSTATE_NAME = 9140
    UA_NS0ID_ALARMCONDITIONTYPE_ACKEDSTATE_NUMBER = 9141
    UA_NS0ID_ALARMCONDITIONTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 9142
    UA_NS0ID_ALARMCONDITIONTYPE_ACKEDSTATE_TRANSITIONTIME = 9143
    UA_NS0ID_ALARMCONDITIONTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 9144
    UA_NS0ID_ALARMCONDITIONTYPE_ACKEDSTATE_TRUESTATE = 9145
    UA_NS0ID_ALARMCONDITIONTYPE_ACKEDSTATE_FALSESTATE = 9146
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRMEDSTATE = 9147
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRMEDSTATE_ID = 9148
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRMEDSTATE_NAME = 9149
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRMEDSTATE_NUMBER = 9150
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 9151
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 9152
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 9153
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRMEDSTATE_TRUESTATE = 9154
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRMEDSTATE_FALSESTATE = 9155
    UA_NS0ID_ALARMCONDITIONTYPE_ACKNOWLEDGE = 9156
    UA_NS0ID_ALARMCONDITIONTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 9157
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRM = 9158
    UA_NS0ID_ALARMCONDITIONTYPE_CONFIRM_INPUTARGUMENTS = 9159
    UA_NS0ID_ALARMCONDITIONTYPE_ACTIVESTATE = 9160
    UA_NS0ID_ALARMCONDITIONTYPE_ACTIVESTATE_ID = 9161
    UA_NS0ID_ALARMCONDITIONTYPE_ACTIVESTATE_NAME = 9162
    UA_NS0ID_ALARMCONDITIONTYPE_ACTIVESTATE_NUMBER = 9163
    UA_NS0ID_ALARMCONDITIONTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 9164
    UA_NS0ID_ALARMCONDITIONTYPE_ACTIVESTATE_TRANSITIONTIME = 9165
    UA_NS0ID_ALARMCONDITIONTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 9166
    UA_NS0ID_ALARMCONDITIONTYPE_ACTIVESTATE_TRUESTATE = 9167
    UA_NS0ID_ALARMCONDITIONTYPE_ACTIVESTATE_FALSESTATE = 9168
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDSTATE = 9169
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDSTATE_ID = 9170
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDSTATE_NAME = 9171
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDSTATE_NUMBER = 9172
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 9173
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 9174
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 9175
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDSTATE_TRUESTATE = 9176
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDSTATE_FALSESTATE = 9177
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE = 9178
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_CURRENTSTATE = 9179
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 9180
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 9181
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 9182
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9183
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_LASTTRANSITION = 9184
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 9185
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 9186
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 9187
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 9188
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_UNSHELVETIME = 9189
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_UNSHELVE = 9211
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_ONESHOTSHELVE = 9212
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_TIMEDSHELVE = 9213
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 9214
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESSEDORSHELVED = 9215
    UA_NS0ID_ALARMCONDITIONTYPE_MAXTIMESHELVED = 9216
    UA_NS0ID_LIMITALARMTYPE_CONDITIONNAME = 9217
    UA_NS0ID_LIMITALARMTYPE_BRANCHID = 9218
    UA_NS0ID_LIMITALARMTYPE_ENABLEDSTATE = 9219
    UA_NS0ID_LIMITALARMTYPE_ENABLEDSTATE_ID = 9220
    UA_NS0ID_LIMITALARMTYPE_ENABLEDSTATE_NAME = 9221
    UA_NS0ID_LIMITALARMTYPE_ENABLEDSTATE_NUMBER = 9222
    UA_NS0ID_LIMITALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9223
    UA_NS0ID_LIMITALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 9224
    UA_NS0ID_LIMITALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9225
    UA_NS0ID_LIMITALARMTYPE_ENABLEDSTATE_TRUESTATE = 9226
    UA_NS0ID_LIMITALARMTYPE_ENABLEDSTATE_FALSESTATE = 9227
    UA_NS0ID_LIMITALARMTYPE_QUALITY = 9228
    UA_NS0ID_LIMITALARMTYPE_QUALITY_SOURCETIMESTAMP = 9229
    UA_NS0ID_LIMITALARMTYPE_LASTSEVERITY = 9230
    UA_NS0ID_LIMITALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9231
    UA_NS0ID_LIMITALARMTYPE_COMMENT = 9232
    UA_NS0ID_LIMITALARMTYPE_COMMENT_SOURCETIMESTAMP = 9233
    UA_NS0ID_LIMITALARMTYPE_CLIENTUSERID = 9234
    UA_NS0ID_LIMITALARMTYPE_ENABLE = 9235
    UA_NS0ID_LIMITALARMTYPE_DISABLE = 9236
    UA_NS0ID_LIMITALARMTYPE_ADDCOMMENT = 9237
    UA_NS0ID_LIMITALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 9238
    UA_NS0ID_LIMITALARMTYPE_ACKEDSTATE = 9239
    UA_NS0ID_LIMITALARMTYPE_ACKEDSTATE_ID = 9240
    UA_NS0ID_LIMITALARMTYPE_ACKEDSTATE_NAME = 9241
    UA_NS0ID_LIMITALARMTYPE_ACKEDSTATE_NUMBER = 9242
    UA_NS0ID_LIMITALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 9243
    UA_NS0ID_LIMITALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 9244
    UA_NS0ID_LIMITALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 9245
    UA_NS0ID_LIMITALARMTYPE_ACKEDSTATE_TRUESTATE = 9246
    UA_NS0ID_LIMITALARMTYPE_ACKEDSTATE_FALSESTATE = 9247
    UA_NS0ID_LIMITALARMTYPE_CONFIRMEDSTATE = 9248
    UA_NS0ID_LIMITALARMTYPE_CONFIRMEDSTATE_ID = 9249
    UA_NS0ID_LIMITALARMTYPE_CONFIRMEDSTATE_NAME = 9250
    UA_NS0ID_LIMITALARMTYPE_CONFIRMEDSTATE_NUMBER = 9251
    UA_NS0ID_LIMITALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 9252
    UA_NS0ID_LIMITALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 9253
    UA_NS0ID_LIMITALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 9254
    UA_NS0ID_LIMITALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 9255
    UA_NS0ID_LIMITALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 9256
    UA_NS0ID_LIMITALARMTYPE_ACKNOWLEDGE = 9257
    UA_NS0ID_LIMITALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 9258
    UA_NS0ID_LIMITALARMTYPE_CONFIRM = 9259
    UA_NS0ID_LIMITALARMTYPE_CONFIRM_INPUTARGUMENTS = 9260
    UA_NS0ID_LIMITALARMTYPE_ACTIVESTATE = 9261
    UA_NS0ID_LIMITALARMTYPE_ACTIVESTATE_ID = 9262
    UA_NS0ID_LIMITALARMTYPE_ACTIVESTATE_NAME = 9263
    UA_NS0ID_LIMITALARMTYPE_ACTIVESTATE_NUMBER = 9264
    UA_NS0ID_LIMITALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 9265
    UA_NS0ID_LIMITALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 9266
    UA_NS0ID_LIMITALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 9267
    UA_NS0ID_LIMITALARMTYPE_ACTIVESTATE_TRUESTATE = 9268
    UA_NS0ID_LIMITALARMTYPE_ACTIVESTATE_FALSESTATE = 9269
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDSTATE = 9270
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDSTATE_ID = 9271
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDSTATE_NAME = 9272
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDSTATE_NUMBER = 9273
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 9274
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 9275
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 9276
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 9277
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 9278
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE = 9279
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 9280
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 9281
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 9282
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 9283
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9284
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 9285
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 9286
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 9287
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 9288
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 9289
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 9290
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_UNSHELVE = 9312
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 9313
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 9314
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 9315
    UA_NS0ID_LIMITALARMTYPE_SUPPRESSEDORSHELVED = 9316
    UA_NS0ID_LIMITALARMTYPE_MAXTIMESHELVED = 9317
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE = 9318
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_CURRENTSTATE = 9319
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_CURRENTSTATE_ID = 9320
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_CURRENTSTATE_NAME = 9321
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_CURRENTSTATE_NUMBER = 9322
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9323
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LASTTRANSITION = 9324
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LASTTRANSITION_ID = 9325
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LASTTRANSITION_NAME = 9326
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LASTTRANSITION_NUMBER = 9327
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LASTTRANSITION_TRANSITIONTIME = 9328
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_HIGHHIGH = 9329
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_HIGHHIGH_STATENUMBER = 9330
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_HIGH = 9331
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_HIGH_STATENUMBER = 9332
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LOW = 9333
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LOW_STATENUMBER = 9334
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LOWLOW = 9335
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LOWLOW_STATENUMBER = 9336
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LOWLOWTOLOW = 9337
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LOWTOLOWLOW = 9338
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_HIGHHIGHTOHIGH = 9339
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_HIGHTOHIGHHIGH = 9340
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE = 9341
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_EVENTID = 9342
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_EVENTTYPE = 9343
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SOURCENODE = 9344
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SOURCENAME = 9345
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_TIME = 9346
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_RECEIVETIME = 9347
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LOCALTIME = 9348
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_MESSAGE = 9349
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SEVERITY = 9350
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONDITIONNAME = 9351
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_BRANCHID = 9352
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_RETAIN = 9353
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLEDSTATE = 9354
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_ID = 9355
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_NAME = 9356
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_NUMBER = 9357
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9358
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 9359
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9360
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_TRUESTATE = 9361
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_FALSESTATE = 9362
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_QUALITY = 9363
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_QUALITY_SOURCETIMESTAMP = 9364
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LASTSEVERITY = 9365
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9366
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_COMMENT = 9367
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_COMMENT_SOURCETIMESTAMP = 9368
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CLIENTUSERID = 9369
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ENABLE = 9370
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_DISABLE = 9371
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ADDCOMMENT = 9372
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 9373
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONDITIONREFRESH = 9374
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 9375
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKEDSTATE = 9376
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKEDSTATE_ID = 9377
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKEDSTATE_NAME = 9378
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKEDSTATE_NUMBER = 9379
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 9380
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 9381
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 9382
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKEDSTATE_TRUESTATE = 9383
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKEDSTATE_FALSESTATE = 9384
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE = 9385
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_ID = 9386
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_NAME = 9387
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_NUMBER = 9388
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 9389
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 9390
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 9391
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 9392
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 9393
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKNOWLEDGE = 9394
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 9395
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRM = 9396
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONFIRM_INPUTARGUMENTS = 9397
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACTIVESTATE = 9398
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACTIVESTATE_ID = 9399
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACTIVESTATE_NAME = 9400
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACTIVESTATE_NUMBER = 9401
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 9402
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 9403
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 9404
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACTIVESTATE_TRUESTATE = 9405
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ACTIVESTATE_FALSESTATE = 9406
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE = 9407
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_ID = 9408
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_NAME = 9409
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_NUMBER = 9410
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 9411
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 9412
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 9413
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 9414
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 9415
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE = 9416
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 9417
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 9418
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 9419
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 9420
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9421
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 9422
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 9423
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 9424
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 9425
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 9426
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 9427
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_UNSHELVE = 9449
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 9450
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 9451
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 9452
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESSEDORSHELVED = 9453
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_MAXTIMESHELVED = 9454
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE = 9455
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_CURRENTSTATE = 9456
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_CURRENTSTATE_ID = 9457
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_CURRENTSTATE_NAME = 9458
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_CURRENTSTATE_NUMBER = 9459
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9460
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_LASTTRANSITION = 9461
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_LASTTRANSITION_ID = 9462
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_LASTTRANSITION_NAME = 9463
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_LASTTRANSITION_NUMBER = 9464
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_LASTTRANSITION_TRANSITIONTIME = 9465
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_HIGHHIGHLIMIT = 9478
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_HIGHLIMIT = 9479
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LOWLIMIT = 9480
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LOWLOWLIMIT = 9481
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE = 9482
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_EVENTID = 9483
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_EVENTTYPE = 9484
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SOURCENODE = 9485
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SOURCENAME = 9486
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_TIME = 9487
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_RECEIVETIME = 9488
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LOCALTIME = 9489
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_MESSAGE = 9490
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SEVERITY = 9491
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONDITIONNAME = 9492
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_BRANCHID = 9493
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_RETAIN = 9494
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLEDSTATE = 9495
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_ID = 9496
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_NAME = 9497
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_NUMBER = 9498
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9499
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 9500
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9501
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_TRUESTATE = 9502
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_FALSESTATE = 9503
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_QUALITY = 9504
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_QUALITY_SOURCETIMESTAMP = 9505
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LASTSEVERITY = 9506
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9507
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_COMMENT = 9508
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_COMMENT_SOURCETIMESTAMP = 9509
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CLIENTUSERID = 9510
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ENABLE = 9511
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_DISABLE = 9512
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ADDCOMMENT = 9513
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 9514
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONDITIONREFRESH = 9515
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 9516
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKEDSTATE = 9517
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKEDSTATE_ID = 9518
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKEDSTATE_NAME = 9519
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKEDSTATE_NUMBER = 9520
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 9521
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 9522
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 9523
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKEDSTATE_TRUESTATE = 9524
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKEDSTATE_FALSESTATE = 9525
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE = 9526
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_ID = 9527
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_NAME = 9528
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_NUMBER = 9529
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 9530
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 9531
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 9532
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 9533
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 9534
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKNOWLEDGE = 9535
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 9536
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRM = 9537
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONFIRM_INPUTARGUMENTS = 9538
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACTIVESTATE = 9539
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACTIVESTATE_ID = 9540
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACTIVESTATE_NAME = 9541
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACTIVESTATE_NUMBER = 9542
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 9543
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 9544
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 9545
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACTIVESTATE_TRUESTATE = 9546
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ACTIVESTATE_FALSESTATE = 9547
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE = 9548
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_ID = 9549
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_NAME = 9550
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_NUMBER = 9551
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 9552
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 9553
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 9554
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 9555
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 9556
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE = 9557
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 9558
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 9559
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 9560
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 9561
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9562
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 9563
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 9564
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 9565
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 9566
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 9567
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 9568
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_UNSHELVE = 9590
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 9591
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 9592
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 9593
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESSEDORSHELVED = 9594
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_MAXTIMESHELVED = 9595
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE = 9596
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_CURRENTSTATE = 9597
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_CURRENTSTATE_ID = 9598
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_CURRENTSTATE_NAME = 9599
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_CURRENTSTATE_NUMBER = 9600
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9601
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_LASTTRANSITION = 9602
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_LASTTRANSITION_ID = 9603
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_LASTTRANSITION_NAME = 9604
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_LASTTRANSITION_NUMBER = 9605
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_LASTTRANSITION_TRANSITIONTIME = 9606
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_HIGHHIGHLIMIT = 9619
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_HIGHLIMIT = 9620
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LOWLIMIT = 9621
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LOWLOWLIMIT = 9622
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE = 9623
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_EVENTID = 9624
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_EVENTTYPE = 9625
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SOURCENODE = 9626
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SOURCENAME = 9627
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_TIME = 9628
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_RECEIVETIME = 9629
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LOCALTIME = 9630
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_MESSAGE = 9631
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SEVERITY = 9632
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONNAME = 9633
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_BRANCHID = 9634
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_RETAIN = 9635
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE = 9636
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_ID = 9637
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_NAME = 9638
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_NUMBER = 9639
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9640
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 9641
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9642
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_TRUESTATE = 9643
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_FALSESTATE = 9644
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_QUALITY = 9645
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_QUALITY_SOURCETIMESTAMP = 9646
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LASTSEVERITY = 9647
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9648
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_COMMENT = 9649
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_COMMENT_SOURCETIMESTAMP = 9650
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CLIENTUSERID = 9651
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENABLE = 9652
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_DISABLE = 9653
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ADDCOMMENT = 9654
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 9655
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONREFRESH = 9656
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 9657
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE = 9658
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_ID = 9659
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_NAME = 9660
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_NUMBER = 9661
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 9662
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 9663
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 9664
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_TRUESTATE = 9665
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_FALSESTATE = 9666
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE = 9667
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_ID = 9668
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_NAME = 9669
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_NUMBER = 9670
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 9671
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 9672
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 9673
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 9674
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 9675
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKNOWLEDGE = 9676
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 9677
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRM = 9678
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRM_INPUTARGUMENTS = 9679
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE = 9680
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_ID = 9681
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_NAME = 9682
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_NUMBER = 9683
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 9684
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 9685
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 9686
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_TRUESTATE = 9687
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_FALSESTATE = 9688
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE = 9689
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_ID = 9690
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_NAME = 9691
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_NUMBER = 9692
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 9693
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 9694
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 9695
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 9696
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 9697
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE = 9698
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 9699
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 9700
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 9701
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 9702
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9703
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 9704
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 9705
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 9706
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 9707
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 9708
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 9709
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_UNSHELVE = 9731
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 9732
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 9733
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 9734
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDORSHELVED = 9735
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_MAXTIMESHELVED = 9736
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE = 9737
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_CURRENTSTATE = 9738
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_CURRENTSTATE_ID = 9739
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_CURRENTSTATE_NAME = 9740
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_CURRENTSTATE_NUMBER = 9741
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9742
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_LASTTRANSITION = 9743
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_LASTTRANSITION_ID = 9744
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_LASTTRANSITION_NAME = 9745
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_LASTTRANSITION_NUMBER = 9746
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_LASTTRANSITION_TRANSITIONTIME = 9747
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHLIMIT = 9760
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_HIGHLIMIT = 9761
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LOWLIMIT = 9762
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWLIMIT = 9763
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE = 9764
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_EVENTID = 9765
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_EVENTTYPE = 9766
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SOURCENODE = 9767
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SOURCENAME = 9768
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_TIME = 9769
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_RECEIVETIME = 9770
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LOCALTIME = 9771
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_MESSAGE = 9772
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SEVERITY = 9773
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONDITIONNAME = 9774
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_BRANCHID = 9775
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_RETAIN = 9776
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE = 9777
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_ID = 9778
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_NAME = 9779
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_NUMBER = 9780
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9781
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 9782
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9783
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_TRUESTATE = 9784
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_FALSESTATE = 9785
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_QUALITY = 9786
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_QUALITY_SOURCETIMESTAMP = 9787
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LASTSEVERITY = 9788
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9789
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_COMMENT = 9790
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_COMMENT_SOURCETIMESTAMP = 9791
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CLIENTUSERID = 9792
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ENABLE = 9793
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_DISABLE = 9794
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ADDCOMMENT = 9795
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 9796
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONDITIONREFRESH = 9797
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 9798
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE = 9799
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_ID = 9800
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_NAME = 9801
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_NUMBER = 9802
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 9803
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 9804
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 9805
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_TRUESTATE = 9806
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_FALSESTATE = 9807
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE = 9808
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_ID = 9809
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_NAME = 9810
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_NUMBER = 9811
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 9812
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 9813
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 9814
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 9815
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 9816
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKNOWLEDGE = 9817
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 9818
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRM = 9819
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONFIRM_INPUTARGUMENTS = 9820
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE = 9821
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_ID = 9822
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_NAME = 9823
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_NUMBER = 9824
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 9825
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 9826
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 9827
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_TRUESTATE = 9828
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_FALSESTATE = 9829
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE = 9830
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_ID = 9831
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_NAME = 9832
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_NUMBER = 9833
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 9834
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 9835
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 9836
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 9837
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 9838
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE = 9839
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 9840
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 9841
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 9842
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 9843
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9844
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 9845
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 9846
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 9847
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 9848
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 9849
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 9850
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_UNSHELVE = 9872
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 9873
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 9874
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 9875
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDORSHELVED = 9876
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_MAXTIMESHELVED = 9877
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE = 9878
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_CURRENTSTATE = 9879
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_CURRENTSTATE_ID = 9880
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_CURRENTSTATE_NAME = 9881
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_CURRENTSTATE_NUMBER = 9882
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9883
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_LASTTRANSITION = 9884
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_LASTTRANSITION_ID = 9885
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_LASTTRANSITION_NAME = 9886
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_LASTTRANSITION_NUMBER = 9887
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_LASTTRANSITION_TRANSITIONTIME = 9888
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHLIMIT = 9901
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_HIGHLIMIT = 9902
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LOWLIMIT = 9903
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LOWLOWLIMIT = 9904
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SETPOINTNODE = 9905
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE = 9906
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_EVENTID = 9907
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_EVENTTYPE = 9908
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SOURCENODE = 9909
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SOURCENAME = 9910
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_TIME = 9911
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_RECEIVETIME = 9912
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOCALTIME = 9913
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_MESSAGE = 9914
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SEVERITY = 9915
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONDITIONNAME = 9916
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_BRANCHID = 9917
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_RETAIN = 9918
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLEDSTATE = 9919
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_ID = 9920
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_NAME = 9921
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_NUMBER = 9922
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 9923
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 9924
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 9925
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_TRUESTATE = 9926
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLEDSTATE_FALSESTATE = 9927
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_QUALITY = 9928
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_QUALITY_SOURCETIMESTAMP = 9929
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LASTSEVERITY = 9930
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 9931
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_COMMENT = 9932
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_COMMENT_SOURCETIMESTAMP = 9933
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CLIENTUSERID = 9934
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ENABLE = 9935
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_DISABLE = 9936
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ADDCOMMENT = 9937
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 9938
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONDITIONREFRESH = 9939
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 9940
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKEDSTATE = 9941
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKEDSTATE_ID = 9942
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKEDSTATE_NAME = 9943
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKEDSTATE_NUMBER = 9944
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 9945
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 9946
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 9947
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKEDSTATE_TRUESTATE = 9948
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKEDSTATE_FALSESTATE = 9949
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE = 9950
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_ID = 9951
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_NAME = 9952
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_NUMBER = 9953
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 9954
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 9955
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 9956
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 9957
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 9958
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKNOWLEDGE = 9959
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 9960
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRM = 9961
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONFIRM_INPUTARGUMENTS = 9962
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACTIVESTATE = 9963
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACTIVESTATE_ID = 9964
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACTIVESTATE_NAME = 9965
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACTIVESTATE_NUMBER = 9966
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 9967
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 9968
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 9969
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACTIVESTATE_TRUESTATE = 9970
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ACTIVESTATE_FALSESTATE = 9971
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE = 9972
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_ID = 9973
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_NAME = 9974
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_NUMBER = 9975
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 9976
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 9977
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 9978
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 9979
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 9980
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE = 9981
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 9982
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 9983
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 9984
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 9985
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 9986
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 9987
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 9988
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 9989
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 9990
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 9991
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 9992
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_UNSHELVE = 10014
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 10015
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 10016
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 10017
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESSEDORSHELVED = 10018
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_MAXTIMESHELVED = 10019
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHSTATE = 10020
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHSTATE_ID = 10021
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHSTATE_NAME = 10022
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHSTATE_NUMBER = 10023
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHSTATE_EFFECTIVEDISPLAYNAME = 10024
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHSTATE_TRANSITIONTIME = 10025
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHSTATE_EFFECTIVETRANSITIONTIME = 10026
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHSTATE_TRUESTATE = 10027
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHSTATE_FALSESTATE = 10028
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHSTATE = 10029
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHSTATE_ID = 10030
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHSTATE_NAME = 10031
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHSTATE_NUMBER = 10032
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHSTATE_EFFECTIVEDISPLAYNAME = 10033
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHSTATE_TRANSITIONTIME = 10034
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHSTATE_EFFECTIVETRANSITIONTIME = 10035
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHSTATE_TRUESTATE = 10036
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHSTATE_FALSESTATE = 10037
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWSTATE = 10038
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWSTATE_ID = 10039
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWSTATE_NAME = 10040
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWSTATE_NUMBER = 10041
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWSTATE_EFFECTIVEDISPLAYNAME = 10042
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWSTATE_TRANSITIONTIME = 10043
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWSTATE_EFFECTIVETRANSITIONTIME = 10044
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWSTATE_TRUESTATE = 10045
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWSTATE_FALSESTATE = 10046
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWSTATE = 10047
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWSTATE_ID = 10048
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWSTATE_NAME = 10049
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWSTATE_NUMBER = 10050
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWSTATE_EFFECTIVEDISPLAYNAME = 10051
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWSTATE_TRANSITIONTIME = 10052
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWSTATE_EFFECTIVETRANSITIONTIME = 10053
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWSTATE_TRUESTATE = 10054
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWSTATE_FALSESTATE = 10055
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHHIGHLIMIT = 10056
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_HIGHLIMIT = 10057
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLIMIT = 10058
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LOWLOWLIMIT = 10059
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE = 10060
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_EVENTID = 10061
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_EVENTTYPE = 10062
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SOURCENODE = 10063
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SOURCENAME = 10064
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_TIME = 10065
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_RECEIVETIME = 10066
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOCALTIME = 10067
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_MESSAGE = 10068
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SEVERITY = 10069
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONDITIONNAME = 10070
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_BRANCHID = 10071
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_RETAIN = 10072
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLEDSTATE = 10073
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_ID = 10074
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_NAME = 10075
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_NUMBER = 10076
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 10077
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 10078
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 10079
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_TRUESTATE = 10080
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLEDSTATE_FALSESTATE = 10081
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_QUALITY = 10082
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_QUALITY_SOURCETIMESTAMP = 10083
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LASTSEVERITY = 10084
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 10085
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_COMMENT = 10086
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_COMMENT_SOURCETIMESTAMP = 10087
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CLIENTUSERID = 10088
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ENABLE = 10089
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_DISABLE = 10090
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ADDCOMMENT = 10091
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 10092
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONDITIONREFRESH = 10093
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 10094
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKEDSTATE = 10095
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKEDSTATE_ID = 10096
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKEDSTATE_NAME = 10097
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKEDSTATE_NUMBER = 10098
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 10099
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 10100
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 10101
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKEDSTATE_TRUESTATE = 10102
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKEDSTATE_FALSESTATE = 10103
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE = 10104
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_ID = 10105
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_NAME = 10106
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_NUMBER = 10107
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 10108
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 10109
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 10110
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 10111
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 10112
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKNOWLEDGE = 10113
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 10114
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRM = 10115
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONFIRM_INPUTARGUMENTS = 10116
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACTIVESTATE = 10117
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACTIVESTATE_ID = 10118
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACTIVESTATE_NAME = 10119
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACTIVESTATE_NUMBER = 10120
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 10121
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 10122
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 10123
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACTIVESTATE_TRUESTATE = 10124
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ACTIVESTATE_FALSESTATE = 10125
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE = 10126
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_ID = 10127
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_NAME = 10128
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_NUMBER = 10129
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 10130
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 10131
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 10132
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 10133
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 10134
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE = 10135
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 10136
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 10137
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 10138
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 10139
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 10140
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 10141
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 10142
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 10143
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 10144
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 10145
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 10146
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_UNSHELVE = 10168
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 10169
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 10170
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 10171
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESSEDORSHELVED = 10172
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_MAXTIMESHELVED = 10173
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHSTATE = 10174
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHSTATE_ID = 10175
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHSTATE_NAME = 10176
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHSTATE_NUMBER = 10177
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHSTATE_EFFECTIVEDISPLAYNAME = 10178
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHSTATE_TRANSITIONTIME = 10179
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHSTATE_EFFECTIVETRANSITIONTIME = 10180
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHSTATE_TRUESTATE = 10181
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHSTATE_FALSESTATE = 10182
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHSTATE = 10183
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHSTATE_ID = 10184
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHSTATE_NAME = 10185
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHSTATE_NUMBER = 10186
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHSTATE_EFFECTIVEDISPLAYNAME = 10187
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHSTATE_TRANSITIONTIME = 10188
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHSTATE_EFFECTIVETRANSITIONTIME = 10189
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHSTATE_TRUESTATE = 10190
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHSTATE_FALSESTATE = 10191
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWSTATE = 10192
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWSTATE_ID = 10193
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWSTATE_NAME = 10194
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWSTATE_NUMBER = 10195
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWSTATE_EFFECTIVEDISPLAYNAME = 10196
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWSTATE_TRANSITIONTIME = 10197
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWSTATE_EFFECTIVETRANSITIONTIME = 10198
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWSTATE_TRUESTATE = 10199
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWSTATE_FALSESTATE = 10200
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWSTATE = 10201
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWSTATE_ID = 10202
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWSTATE_NAME = 10203
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWSTATE_NUMBER = 10204
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWSTATE_EFFECTIVEDISPLAYNAME = 10205
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWSTATE_TRANSITIONTIME = 10206
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWSTATE_EFFECTIVETRANSITIONTIME = 10207
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWSTATE_TRUESTATE = 10208
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWSTATE_FALSESTATE = 10209
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHHIGHLIMIT = 10210
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_HIGHLIMIT = 10211
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLIMIT = 10212
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LOWLOWLIMIT = 10213
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE = 10214
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_EVENTID = 10215
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_EVENTTYPE = 10216
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SOURCENODE = 10217
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SOURCENAME = 10218
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_TIME = 10219
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_RECEIVETIME = 10220
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOCALTIME = 10221
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_MESSAGE = 10222
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SEVERITY = 10223
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONNAME = 10224
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_BRANCHID = 10225
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_RETAIN = 10226
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE = 10227
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_ID = 10228
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_NAME = 10229
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_NUMBER = 10230
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 10231
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 10232
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 10233
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_TRUESTATE = 10234
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLEDSTATE_FALSESTATE = 10235
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_QUALITY = 10236
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_QUALITY_SOURCETIMESTAMP = 10237
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LASTSEVERITY = 10238
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 10239
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_COMMENT = 10240
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_COMMENT_SOURCETIMESTAMP = 10241
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CLIENTUSERID = 10242
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENABLE = 10243
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_DISABLE = 10244
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ADDCOMMENT = 10245
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 10246
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONREFRESH = 10247
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 10248
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE = 10249
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_ID = 10250
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_NAME = 10251
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_NUMBER = 10252
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 10253
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 10254
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 10255
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_TRUESTATE = 10256
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKEDSTATE_FALSESTATE = 10257
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE = 10258
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_ID = 10259
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_NAME = 10260
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_NUMBER = 10261
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 10262
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 10263
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 10264
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 10265
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 10266
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKNOWLEDGE = 10267
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 10268
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRM = 10269
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONFIRM_INPUTARGUMENTS = 10270
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE = 10271
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_ID = 10272
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_NAME = 10273
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_NUMBER = 10274
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 10275
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 10276
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 10277
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_TRUESTATE = 10278
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ACTIVESTATE_FALSESTATE = 10279
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE = 10280
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_ID = 10281
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_NAME = 10282
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_NUMBER = 10283
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 10284
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 10285
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 10286
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 10287
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 10288
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE = 10289
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 10290
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 10291
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 10292
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 10293
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 10294
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 10295
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 10296
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 10297
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 10298
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 10299
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 10300
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_UNSHELVE = 10322
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 10323
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 10324
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 10325
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESSEDORSHELVED = 10326
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_MAXTIMESHELVED = 10327
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHSTATE = 10328
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHSTATE_ID = 10329
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHSTATE_NAME = 10330
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHSTATE_NUMBER = 10331
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHSTATE_EFFECTIVEDISPLAYNAME = 10332
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHSTATE_TRANSITIONTIME = 10333
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHSTATE_EFFECTIVETRANSITIONTIME = 10334
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHSTATE_TRUESTATE = 10335
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHSTATE_FALSESTATE = 10336
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHSTATE = 10337
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHSTATE_ID = 10338
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHSTATE_NAME = 10339
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHSTATE_NUMBER = 10340
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHSTATE_EFFECTIVEDISPLAYNAME = 10341
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHSTATE_TRANSITIONTIME = 10342
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHSTATE_EFFECTIVETRANSITIONTIME = 10343
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHSTATE_TRUESTATE = 10344
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHSTATE_FALSESTATE = 10345
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWSTATE = 10346
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWSTATE_ID = 10347
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWSTATE_NAME = 10348
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWSTATE_NUMBER = 10349
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWSTATE_EFFECTIVEDISPLAYNAME = 10350
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWSTATE_TRANSITIONTIME = 10351
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWSTATE_EFFECTIVETRANSITIONTIME = 10352
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWSTATE_TRUESTATE = 10353
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWSTATE_FALSESTATE = 10354
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWSTATE = 10355
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWSTATE_ID = 10356
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWSTATE_NAME = 10357
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWSTATE_NUMBER = 10358
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWSTATE_EFFECTIVEDISPLAYNAME = 10359
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWSTATE_TRANSITIONTIME = 10360
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWSTATE_EFFECTIVETRANSITIONTIME = 10361
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWSTATE_TRUESTATE = 10362
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWSTATE_FALSESTATE = 10363
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHHIGHLIMIT = 10364
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_HIGHLIMIT = 10365
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLIMIT = 10366
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LOWLOWLIMIT = 10367
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE = 10368
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_EVENTID = 10369
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_EVENTTYPE = 10370
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SOURCENODE = 10371
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SOURCENAME = 10372
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_TIME = 10373
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_RECEIVETIME = 10374
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOCALTIME = 10375
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_MESSAGE = 10376
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SEVERITY = 10377
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONDITIONNAME = 10378
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_BRANCHID = 10379
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_RETAIN = 10380
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE = 10381
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_ID = 10382
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_NAME = 10383
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_NUMBER = 10384
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 10385
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 10386
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 10387
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_TRUESTATE = 10388
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLEDSTATE_FALSESTATE = 10389
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_QUALITY = 10390
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_QUALITY_SOURCETIMESTAMP = 10391
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LASTSEVERITY = 10392
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 10393
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_COMMENT = 10394
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_COMMENT_SOURCETIMESTAMP = 10395
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CLIENTUSERID = 10396
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ENABLE = 10397
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_DISABLE = 10398
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ADDCOMMENT = 10399
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 10400
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONDITIONREFRESH = 10401
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 10402
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE = 10403
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_ID = 10404
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_NAME = 10405
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_NUMBER = 10406
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 10407
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 10408
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 10409
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_TRUESTATE = 10410
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKEDSTATE_FALSESTATE = 10411
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE = 10412
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_ID = 10413
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_NAME = 10414
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_NUMBER = 10415
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 10416
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 10417
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 10418
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 10419
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 10420
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKNOWLEDGE = 10421
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 10422
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRM = 10423
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONFIRM_INPUTARGUMENTS = 10424
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE = 10425
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_ID = 10426
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_NAME = 10427
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_NUMBER = 10428
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 10429
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 10430
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 10431
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_TRUESTATE = 10432
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ACTIVESTATE_FALSESTATE = 10433
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE = 10434
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_ID = 10435
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_NAME = 10436
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_NUMBER = 10437
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 10438
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 10439
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 10440
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 10441
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 10442
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE = 10443
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 10444
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 10445
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 10446
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 10447
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 10448
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 10449
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 10450
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 10451
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 10452
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 10453
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 10454
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_UNSHELVE = 10476
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 10477
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 10478
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 10479
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESSEDORSHELVED = 10480
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_MAXTIMESHELVED = 10481
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHSTATE = 10482
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHSTATE_ID = 10483
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHSTATE_NAME = 10484
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHSTATE_NUMBER = 10485
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHSTATE_EFFECTIVEDISPLAYNAME = 10486
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHSTATE_TRANSITIONTIME = 10487
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHSTATE_EFFECTIVETRANSITIONTIME = 10488
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHSTATE_TRUESTATE = 10489
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHSTATE_FALSESTATE = 10490
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHSTATE = 10491
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHSTATE_ID = 10492
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHSTATE_NAME = 10493
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHSTATE_NUMBER = 10494
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHSTATE_EFFECTIVEDISPLAYNAME = 10495
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHSTATE_TRANSITIONTIME = 10496
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHSTATE_EFFECTIVETRANSITIONTIME = 10497
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHSTATE_TRUESTATE = 10498
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHSTATE_FALSESTATE = 10499
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWSTATE = 10500
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWSTATE_ID = 10501
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWSTATE_NAME = 10502
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWSTATE_NUMBER = 10503
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWSTATE_EFFECTIVEDISPLAYNAME = 10504
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWSTATE_TRANSITIONTIME = 10505
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWSTATE_EFFECTIVETRANSITIONTIME = 10506
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWSTATE_TRUESTATE = 10507
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWSTATE_FALSESTATE = 10508
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWSTATE = 10509
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWSTATE_ID = 10510
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWSTATE_NAME = 10511
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWSTATE_NUMBER = 10512
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWSTATE_EFFECTIVEDISPLAYNAME = 10513
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWSTATE_TRANSITIONTIME = 10514
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWSTATE_EFFECTIVETRANSITIONTIME = 10515
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWSTATE_TRUESTATE = 10516
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWSTATE_FALSESTATE = 10517
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHHIGHLIMIT = 10518
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_HIGHLIMIT = 10519
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLIMIT = 10520
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LOWLOWLIMIT = 10521
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SETPOINTNODE = 10522
    UA_NS0ID_DISCRETEALARMTYPE = 10523
    UA_NS0ID_DISCRETEALARMTYPE_EVENTID = 10524
    UA_NS0ID_DISCRETEALARMTYPE_EVENTTYPE = 10525
    UA_NS0ID_DISCRETEALARMTYPE_SOURCENODE = 10526
    UA_NS0ID_DISCRETEALARMTYPE_SOURCENAME = 10527
    UA_NS0ID_DISCRETEALARMTYPE_TIME = 10528
    UA_NS0ID_DISCRETEALARMTYPE_RECEIVETIME = 10529
    UA_NS0ID_DISCRETEALARMTYPE_LOCALTIME = 10530
    UA_NS0ID_DISCRETEALARMTYPE_MESSAGE = 10531
    UA_NS0ID_DISCRETEALARMTYPE_SEVERITY = 10532
    UA_NS0ID_DISCRETEALARMTYPE_CONDITIONNAME = 10533
    UA_NS0ID_DISCRETEALARMTYPE_BRANCHID = 10534
    UA_NS0ID_DISCRETEALARMTYPE_RETAIN = 10535
    UA_NS0ID_DISCRETEALARMTYPE_ENABLEDSTATE = 10536
    UA_NS0ID_DISCRETEALARMTYPE_ENABLEDSTATE_ID = 10537
    UA_NS0ID_DISCRETEALARMTYPE_ENABLEDSTATE_NAME = 10538
    UA_NS0ID_DISCRETEALARMTYPE_ENABLEDSTATE_NUMBER = 10539
    UA_NS0ID_DISCRETEALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 10540
    UA_NS0ID_DISCRETEALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 10541
    UA_NS0ID_DISCRETEALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 10542
    UA_NS0ID_DISCRETEALARMTYPE_ENABLEDSTATE_TRUESTATE = 10543
    UA_NS0ID_DISCRETEALARMTYPE_ENABLEDSTATE_FALSESTATE = 10544
    UA_NS0ID_DISCRETEALARMTYPE_QUALITY = 10545
    UA_NS0ID_DISCRETEALARMTYPE_QUALITY_SOURCETIMESTAMP = 10546
    UA_NS0ID_DISCRETEALARMTYPE_LASTSEVERITY = 10547
    UA_NS0ID_DISCRETEALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 10548
    UA_NS0ID_DISCRETEALARMTYPE_COMMENT = 10549
    UA_NS0ID_DISCRETEALARMTYPE_COMMENT_SOURCETIMESTAMP = 10550
    UA_NS0ID_DISCRETEALARMTYPE_CLIENTUSERID = 10551
    UA_NS0ID_DISCRETEALARMTYPE_ENABLE = 10552
    UA_NS0ID_DISCRETEALARMTYPE_DISABLE = 10553
    UA_NS0ID_DISCRETEALARMTYPE_ADDCOMMENT = 10554
    UA_NS0ID_DISCRETEALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 10555
    UA_NS0ID_DISCRETEALARMTYPE_CONDITIONREFRESH = 10556
    UA_NS0ID_DISCRETEALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 10557
    UA_NS0ID_DISCRETEALARMTYPE_ACKEDSTATE = 10558
    UA_NS0ID_DISCRETEALARMTYPE_ACKEDSTATE_ID = 10559
    UA_NS0ID_DISCRETEALARMTYPE_ACKEDSTATE_NAME = 10560
    UA_NS0ID_DISCRETEALARMTYPE_ACKEDSTATE_NUMBER = 10561
    UA_NS0ID_DISCRETEALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 10562
    UA_NS0ID_DISCRETEALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 10563
    UA_NS0ID_DISCRETEALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 10564
    UA_NS0ID_DISCRETEALARMTYPE_ACKEDSTATE_TRUESTATE = 10565
    UA_NS0ID_DISCRETEALARMTYPE_ACKEDSTATE_FALSESTATE = 10566
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRMEDSTATE = 10567
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRMEDSTATE_ID = 10568
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRMEDSTATE_NAME = 10569
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRMEDSTATE_NUMBER = 10570
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 10571
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 10572
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 10573
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 10574
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 10575
    UA_NS0ID_DISCRETEALARMTYPE_ACKNOWLEDGE = 10576
    UA_NS0ID_DISCRETEALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 10577
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRM = 10578
    UA_NS0ID_DISCRETEALARMTYPE_CONFIRM_INPUTARGUMENTS = 10579
    UA_NS0ID_DISCRETEALARMTYPE_ACTIVESTATE = 10580
    UA_NS0ID_DISCRETEALARMTYPE_ACTIVESTATE_ID = 10581
    UA_NS0ID_DISCRETEALARMTYPE_ACTIVESTATE_NAME = 10582
    UA_NS0ID_DISCRETEALARMTYPE_ACTIVESTATE_NUMBER = 10583
    UA_NS0ID_DISCRETEALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 10584
    UA_NS0ID_DISCRETEALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 10585
    UA_NS0ID_DISCRETEALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 10586
    UA_NS0ID_DISCRETEALARMTYPE_ACTIVESTATE_TRUESTATE = 10587
    UA_NS0ID_DISCRETEALARMTYPE_ACTIVESTATE_FALSESTATE = 10588
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDSTATE = 10589
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDSTATE_ID = 10590
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDSTATE_NAME = 10591
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDSTATE_NUMBER = 10592
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 10593
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 10594
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 10595
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 10596
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 10597
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE = 10598
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 10599
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 10600
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 10601
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 10602
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 10603
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 10604
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 10605
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 10606
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 10607
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 10608
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 10609
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_UNSHELVE = 10631
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 10632
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 10633
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 10634
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESSEDORSHELVED = 10635
    UA_NS0ID_DISCRETEALARMTYPE_MAXTIMESHELVED = 10636
    UA_NS0ID_OFFNORMALALARMTYPE = 10637
    UA_NS0ID_OFFNORMALALARMTYPE_EVENTID = 10638
    UA_NS0ID_OFFNORMALALARMTYPE_EVENTTYPE = 10639
    UA_NS0ID_OFFNORMALALARMTYPE_SOURCENODE = 10640
    UA_NS0ID_OFFNORMALALARMTYPE_SOURCENAME = 10641
    UA_NS0ID_OFFNORMALALARMTYPE_TIME = 10642
    UA_NS0ID_OFFNORMALALARMTYPE_RECEIVETIME = 10643
    UA_NS0ID_OFFNORMALALARMTYPE_LOCALTIME = 10644
    UA_NS0ID_OFFNORMALALARMTYPE_MESSAGE = 10645
    UA_NS0ID_OFFNORMALALARMTYPE_SEVERITY = 10646
    UA_NS0ID_OFFNORMALALARMTYPE_CONDITIONNAME = 10647
    UA_NS0ID_OFFNORMALALARMTYPE_BRANCHID = 10648
    UA_NS0ID_OFFNORMALALARMTYPE_RETAIN = 10649
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLEDSTATE = 10650
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLEDSTATE_ID = 10651
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLEDSTATE_NAME = 10652
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLEDSTATE_NUMBER = 10653
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 10654
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 10655
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 10656
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLEDSTATE_TRUESTATE = 10657
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLEDSTATE_FALSESTATE = 10658
    UA_NS0ID_OFFNORMALALARMTYPE_QUALITY = 10659
    UA_NS0ID_OFFNORMALALARMTYPE_QUALITY_SOURCETIMESTAMP = 10660
    UA_NS0ID_OFFNORMALALARMTYPE_LASTSEVERITY = 10661
    UA_NS0ID_OFFNORMALALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 10662
    UA_NS0ID_OFFNORMALALARMTYPE_COMMENT = 10663
    UA_NS0ID_OFFNORMALALARMTYPE_COMMENT_SOURCETIMESTAMP = 10664
    UA_NS0ID_OFFNORMALALARMTYPE_CLIENTUSERID = 10665
    UA_NS0ID_OFFNORMALALARMTYPE_ENABLE = 10666
    UA_NS0ID_OFFNORMALALARMTYPE_DISABLE = 10667
    UA_NS0ID_OFFNORMALALARMTYPE_ADDCOMMENT = 10668
    UA_NS0ID_OFFNORMALALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 10669
    UA_NS0ID_OFFNORMALALARMTYPE_CONDITIONREFRESH = 10670
    UA_NS0ID_OFFNORMALALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 10671
    UA_NS0ID_OFFNORMALALARMTYPE_ACKEDSTATE = 10672
    UA_NS0ID_OFFNORMALALARMTYPE_ACKEDSTATE_ID = 10673
    UA_NS0ID_OFFNORMALALARMTYPE_ACKEDSTATE_NAME = 10674
    UA_NS0ID_OFFNORMALALARMTYPE_ACKEDSTATE_NUMBER = 10675
    UA_NS0ID_OFFNORMALALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 10676
    UA_NS0ID_OFFNORMALALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 10677
    UA_NS0ID_OFFNORMALALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 10678
    UA_NS0ID_OFFNORMALALARMTYPE_ACKEDSTATE_TRUESTATE = 10679
    UA_NS0ID_OFFNORMALALARMTYPE_ACKEDSTATE_FALSESTATE = 10680
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRMEDSTATE = 10681
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRMEDSTATE_ID = 10682
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRMEDSTATE_NAME = 10683
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRMEDSTATE_NUMBER = 10684
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 10685
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 10686
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 10687
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 10688
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 10689
    UA_NS0ID_OFFNORMALALARMTYPE_ACKNOWLEDGE = 10690
    UA_NS0ID_OFFNORMALALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 10691
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRM = 10692
    UA_NS0ID_OFFNORMALALARMTYPE_CONFIRM_INPUTARGUMENTS = 10693
    UA_NS0ID_OFFNORMALALARMTYPE_ACTIVESTATE = 10694
    UA_NS0ID_OFFNORMALALARMTYPE_ACTIVESTATE_ID = 10695
    UA_NS0ID_OFFNORMALALARMTYPE_ACTIVESTATE_NAME = 10696
    UA_NS0ID_OFFNORMALALARMTYPE_ACTIVESTATE_NUMBER = 10697
    UA_NS0ID_OFFNORMALALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 10698
    UA_NS0ID_OFFNORMALALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 10699
    UA_NS0ID_OFFNORMALALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 10700
    UA_NS0ID_OFFNORMALALARMTYPE_ACTIVESTATE_TRUESTATE = 10701
    UA_NS0ID_OFFNORMALALARMTYPE_ACTIVESTATE_FALSESTATE = 10702
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDSTATE = 10703
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDSTATE_ID = 10704
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDSTATE_NAME = 10705
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDSTATE_NUMBER = 10706
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 10707
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 10708
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 10709
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 10710
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 10711
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE = 10712
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 10713
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 10714
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 10715
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 10716
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 10717
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 10718
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 10719
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 10720
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 10721
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 10722
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 10723
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_UNSHELVE = 10745
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 10746
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 10747
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 10748
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESSEDORSHELVED = 10749
    UA_NS0ID_OFFNORMALALARMTYPE_MAXTIMESHELVED = 10750
    UA_NS0ID_TRIPALARMTYPE = 10751
    UA_NS0ID_TRIPALARMTYPE_EVENTID = 10752
    UA_NS0ID_TRIPALARMTYPE_EVENTTYPE = 10753
    UA_NS0ID_TRIPALARMTYPE_SOURCENODE = 10754
    UA_NS0ID_TRIPALARMTYPE_SOURCENAME = 10755
    UA_NS0ID_TRIPALARMTYPE_TIME = 10756
    UA_NS0ID_TRIPALARMTYPE_RECEIVETIME = 10757
    UA_NS0ID_TRIPALARMTYPE_LOCALTIME = 10758
    UA_NS0ID_TRIPALARMTYPE_MESSAGE = 10759
    UA_NS0ID_TRIPALARMTYPE_SEVERITY = 10760
    UA_NS0ID_TRIPALARMTYPE_CONDITIONNAME = 10761
    UA_NS0ID_TRIPALARMTYPE_BRANCHID = 10762
    UA_NS0ID_TRIPALARMTYPE_RETAIN = 10763
    UA_NS0ID_TRIPALARMTYPE_ENABLEDSTATE = 10764
    UA_NS0ID_TRIPALARMTYPE_ENABLEDSTATE_ID = 10765
    UA_NS0ID_TRIPALARMTYPE_ENABLEDSTATE_NAME = 10766
    UA_NS0ID_TRIPALARMTYPE_ENABLEDSTATE_NUMBER = 10767
    UA_NS0ID_TRIPALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 10768
    UA_NS0ID_TRIPALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 10769
    UA_NS0ID_TRIPALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 10770
    UA_NS0ID_TRIPALARMTYPE_ENABLEDSTATE_TRUESTATE = 10771
    UA_NS0ID_TRIPALARMTYPE_ENABLEDSTATE_FALSESTATE = 10772
    UA_NS0ID_TRIPALARMTYPE_QUALITY = 10773
    UA_NS0ID_TRIPALARMTYPE_QUALITY_SOURCETIMESTAMP = 10774
    UA_NS0ID_TRIPALARMTYPE_LASTSEVERITY = 10775
    UA_NS0ID_TRIPALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 10776
    UA_NS0ID_TRIPALARMTYPE_COMMENT = 10777
    UA_NS0ID_TRIPALARMTYPE_COMMENT_SOURCETIMESTAMP = 10778
    UA_NS0ID_TRIPALARMTYPE_CLIENTUSERID = 10779
    UA_NS0ID_TRIPALARMTYPE_ENABLE = 10780
    UA_NS0ID_TRIPALARMTYPE_DISABLE = 10781
    UA_NS0ID_TRIPALARMTYPE_ADDCOMMENT = 10782
    UA_NS0ID_TRIPALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 10783
    UA_NS0ID_TRIPALARMTYPE_CONDITIONREFRESH = 10784
    UA_NS0ID_TRIPALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 10785
    UA_NS0ID_TRIPALARMTYPE_ACKEDSTATE = 10786
    UA_NS0ID_TRIPALARMTYPE_ACKEDSTATE_ID = 10787
    UA_NS0ID_TRIPALARMTYPE_ACKEDSTATE_NAME = 10788
    UA_NS0ID_TRIPALARMTYPE_ACKEDSTATE_NUMBER = 10789
    UA_NS0ID_TRIPALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 10790
    UA_NS0ID_TRIPALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 10791
    UA_NS0ID_TRIPALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 10792
    UA_NS0ID_TRIPALARMTYPE_ACKEDSTATE_TRUESTATE = 10793
    UA_NS0ID_TRIPALARMTYPE_ACKEDSTATE_FALSESTATE = 10794
    UA_NS0ID_TRIPALARMTYPE_CONFIRMEDSTATE = 10795
    UA_NS0ID_TRIPALARMTYPE_CONFIRMEDSTATE_ID = 10796
    UA_NS0ID_TRIPALARMTYPE_CONFIRMEDSTATE_NAME = 10797
    UA_NS0ID_TRIPALARMTYPE_CONFIRMEDSTATE_NUMBER = 10798
    UA_NS0ID_TRIPALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 10799
    UA_NS0ID_TRIPALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 10800
    UA_NS0ID_TRIPALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 10801
    UA_NS0ID_TRIPALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 10802
    UA_NS0ID_TRIPALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 10803
    UA_NS0ID_TRIPALARMTYPE_ACKNOWLEDGE = 10804
    UA_NS0ID_TRIPALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 10805
    UA_NS0ID_TRIPALARMTYPE_CONFIRM = 10806
    UA_NS0ID_TRIPALARMTYPE_CONFIRM_INPUTARGUMENTS = 10807
    UA_NS0ID_TRIPALARMTYPE_ACTIVESTATE = 10808
    UA_NS0ID_TRIPALARMTYPE_ACTIVESTATE_ID = 10809
    UA_NS0ID_TRIPALARMTYPE_ACTIVESTATE_NAME = 10810
    UA_NS0ID_TRIPALARMTYPE_ACTIVESTATE_NUMBER = 10811
    UA_NS0ID_TRIPALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 10812
    UA_NS0ID_TRIPALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 10813
    UA_NS0ID_TRIPALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 10814
    UA_NS0ID_TRIPALARMTYPE_ACTIVESTATE_TRUESTATE = 10815
    UA_NS0ID_TRIPALARMTYPE_ACTIVESTATE_FALSESTATE = 10816
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDSTATE = 10817
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDSTATE_ID = 10818
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDSTATE_NAME = 10819
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDSTATE_NUMBER = 10820
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 10821
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 10822
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 10823
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 10824
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 10825
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE = 10826
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 10827
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 10828
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 10829
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 10830
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 10831
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 10832
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 10833
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 10834
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 10835
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 10836
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 10837
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_UNSHELVE = 10859
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 10860
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 10861
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 10862
    UA_NS0ID_TRIPALARMTYPE_SUPPRESSEDORSHELVED = 10863
    UA_NS0ID_TRIPALARMTYPE_MAXTIMESHELVED = 10864
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE = 11093
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_EVENTID = 11094
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_EVENTTYPE = 11095
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_SOURCENODE = 11096
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_SOURCENAME = 11097
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_TIME = 11098
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_RECEIVETIME = 11099
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_LOCALTIME = 11100
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_MESSAGE = 11101
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_SEVERITY = 11102
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_ACTIONTIMESTAMP = 11103
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_STATUS = 11104
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_SERVERID = 11105
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_CLIENTAUDITENTRYID = 11106
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_CLIENTUSERID = 11107
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_METHODID = 11108
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_INPUTARGUMENTS = 11109
    UA_NS0ID_TWOSTATEVARIABLETYPE_TRUESTATE = 11110
    UA_NS0ID_TWOSTATEVARIABLETYPE_FALSESTATE = 11111
    UA_NS0ID_CONDITIONTYPE_CONDITIONCLASSID = 11112
    UA_NS0ID_CONDITIONTYPE_CONDITIONCLASSNAME = 11113
    UA_NS0ID_DIALOGCONDITIONTYPE_CONDITIONCLASSID = 11114
    UA_NS0ID_DIALOGCONDITIONTYPE_CONDITIONCLASSNAME = 11115
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONDITIONCLASSID = 11116
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONDITIONCLASSNAME = 11117
    UA_NS0ID_ALARMCONDITIONTYPE_CONDITIONCLASSID = 11118
    UA_NS0ID_ALARMCONDITIONTYPE_CONDITIONCLASSNAME = 11119
    UA_NS0ID_ALARMCONDITIONTYPE_INPUTNODE = 11120
    UA_NS0ID_LIMITALARMTYPE_CONDITIONCLASSID = 11121
    UA_NS0ID_LIMITALARMTYPE_CONDITIONCLASSNAME = 11122
    UA_NS0ID_LIMITALARMTYPE_INPUTNODE = 11123
    UA_NS0ID_LIMITALARMTYPE_HIGHHIGHLIMIT = 11124
    UA_NS0ID_LIMITALARMTYPE_HIGHLIMIT = 11125
    UA_NS0ID_LIMITALARMTYPE_LOWLIMIT = 11126
    UA_NS0ID_LIMITALARMTYPE_LOWLOWLIMIT = 11127
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONDITIONCLASSID = 11128
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONDITIONCLASSNAME = 11129
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_INPUTNODE = 11130
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONDITIONCLASSID = 11131
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONDITIONCLASSNAME = 11132
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_INPUTNODE = 11133
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONCLASSID = 11134
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONCLASSNAME = 11135
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_INPUTNODE = 11136
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONDITIONCLASSID = 11137
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONDITIONCLASSNAME = 11138
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_INPUTNODE = 11139
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONDITIONCLASSID = 11140
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONDITIONCLASSNAME = 11141
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_INPUTNODE = 11142
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONDITIONCLASSID = 11143
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONDITIONCLASSNAME = 11144
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_INPUTNODE = 11145
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONCLASSID = 11146
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONCLASSNAME = 11147
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_INPUTNODE = 11148
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONDITIONCLASSID = 11149
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONDITIONCLASSNAME = 11150
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_INPUTNODE = 11151
    UA_NS0ID_DISCRETEALARMTYPE_CONDITIONCLASSID = 11152
    UA_NS0ID_DISCRETEALARMTYPE_CONDITIONCLASSNAME = 11153
    UA_NS0ID_DISCRETEALARMTYPE_INPUTNODE = 11154
    UA_NS0ID_OFFNORMALALARMTYPE_CONDITIONCLASSID = 11155
    UA_NS0ID_OFFNORMALALARMTYPE_CONDITIONCLASSNAME = 11156
    UA_NS0ID_OFFNORMALALARMTYPE_INPUTNODE = 11157
    UA_NS0ID_OFFNORMALALARMTYPE_NORMALSTATE = 11158
    UA_NS0ID_TRIPALARMTYPE_CONDITIONCLASSID = 11159
    UA_NS0ID_TRIPALARMTYPE_CONDITIONCLASSNAME = 11160
    UA_NS0ID_TRIPALARMTYPE_INPUTNODE = 11161
    UA_NS0ID_TRIPALARMTYPE_NORMALSTATE = 11162
    UA_NS0ID_BASECONDITIONCLASSTYPE = 11163
    UA_NS0ID_PROCESSCONDITIONCLASSTYPE = 11164
    UA_NS0ID_MAINTENANCECONDITIONCLASSTYPE = 11165
    UA_NS0ID_SYSTEMCONDITIONCLASSTYPE = 11166
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_AGGREGATECONFIGURATION_TREATUNCERTAINASBAD = 11168
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_AGGREGATECONFIGURATION_PERCENTDATABAD = 11169
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_AGGREGATECONFIGURATION_PERCENTDATAGOOD = 11170
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_AGGREGATECONFIGURATION_USESLOPEDEXTRAPOLATION = 11171
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_AGGREGATEFUNCTIONS = 11172
    UA_NS0ID_AGGREGATECONFIGURATIONTYPE = 11187
    UA_NS0ID_AGGREGATECONFIGURATIONTYPE_TREATUNCERTAINASBAD = 11188
    UA_NS0ID_AGGREGATECONFIGURATIONTYPE_PERCENTDATABAD = 11189
    UA_NS0ID_AGGREGATECONFIGURATIONTYPE_PERCENTDATAGOOD = 11190
    UA_NS0ID_AGGREGATECONFIGURATIONTYPE_USESLOPEDEXTRAPOLATION = 11191
    UA_NS0ID_HISTORYSERVERCAPABILITIES = 11192
    UA_NS0ID_HISTORYSERVERCAPABILITIES_ACCESSHISTORYDATACAPABILITY = 11193
    UA_NS0ID_HISTORYSERVERCAPABILITIES_INSERTDATACAPABILITY = 11196
    UA_NS0ID_HISTORYSERVERCAPABILITIES_REPLACEDATACAPABILITY = 11197
    UA_NS0ID_HISTORYSERVERCAPABILITIES_UPDATEDATACAPABILITY = 11198
    UA_NS0ID_HISTORYSERVERCAPABILITIES_DELETERAWCAPABILITY = 11199
    UA_NS0ID_HISTORYSERVERCAPABILITIES_DELETEATTIMECAPABILITY = 11200
    UA_NS0ID_HISTORYSERVERCAPABILITIES_AGGREGATEFUNCTIONS = 11201
    UA_NS0ID_HACONFIGURATION = 11202
    UA_NS0ID_HACONFIGURATION_AGGREGATECONFIGURATION = 11203
    UA_NS0ID_HACONFIGURATION_AGGREGATECONFIGURATION_TREATUNCERTAINASBAD = 11204
    UA_NS0ID_HACONFIGURATION_AGGREGATECONFIGURATION_PERCENTDATABAD = 11205
    UA_NS0ID_HACONFIGURATION_AGGREGATECONFIGURATION_PERCENTDATAGOOD = 11206
    UA_NS0ID_HACONFIGURATION_AGGREGATECONFIGURATION_USESLOPEDEXTRAPOLATION = 11207
    UA_NS0ID_HACONFIGURATION_STEPPED = 11208
    UA_NS0ID_HACONFIGURATION_DEFINITION = 11209
    UA_NS0ID_HACONFIGURATION_MAXTIMEINTERVAL = 11210
    UA_NS0ID_HACONFIGURATION_MINTIMEINTERVAL = 11211
    UA_NS0ID_HACONFIGURATION_EXCEPTIONDEVIATION = 11212
    UA_NS0ID_HACONFIGURATION_EXCEPTIONDEVIATIONFORMAT = 11213
    UA_NS0ID_ANNOTATIONS = 11214
    UA_NS0ID_HISTORICALEVENTFILTER = 11215
    UA_NS0ID_MODIFICATIONINFO = 11216
    UA_NS0ID_HISTORYMODIFIEDDATA = 11217
    UA_NS0ID_MODIFICATIONINFO_ENCODING_DEFAULTXML = 11218
    UA_NS0ID_HISTORYMODIFIEDDATA_ENCODING_DEFAULTXML = 11219
    UA_NS0ID_MODIFICATIONINFO_ENCODING_DEFAULTBINARY = 11226
    UA_NS0ID_HISTORYMODIFIEDDATA_ENCODING_DEFAULTBINARY = 11227
    UA_NS0ID_HISTORYUPDATETYPE = 11234
    UA_NS0ID_MULTISTATEVALUEDISCRETETYPE = 11238
    UA_NS0ID_MULTISTATEVALUEDISCRETETYPE_DEFINITION = 11239
    UA_NS0ID_MULTISTATEVALUEDISCRETETYPE_VALUEPRECISION = 11240
    UA_NS0ID_MULTISTATEVALUEDISCRETETYPE_ENUMVALUES = 11241
    UA_NS0ID_HISTORYSERVERCAPABILITIES_ACCESSHISTORYEVENTSCAPABILITY = 11242
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_MAXRETURNDATAVALUES = 11268
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_MAXRETURNEVENTVALUES = 11269
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_INSERTANNOTATIONCAPABILITY = 11270
    UA_NS0ID_HISTORYSERVERCAPABILITIES_MAXRETURNDATAVALUES = 11273
    UA_NS0ID_HISTORYSERVERCAPABILITIES_MAXRETURNEVENTVALUES = 11274
    UA_NS0ID_HISTORYSERVERCAPABILITIES_INSERTANNOTATIONCAPABILITY = 11275
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_INSERTEVENTCAPABILITY = 11278
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_REPLACEEVENTCAPABILITY = 11279
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_UPDATEEVENTCAPABILITY = 11280
    UA_NS0ID_HISTORYSERVERCAPABILITIES_INSERTEVENTCAPABILITY = 11281
    UA_NS0ID_HISTORYSERVERCAPABILITIES_REPLACEEVENTCAPABILITY = 11282
    UA_NS0ID_HISTORYSERVERCAPABILITIES_UPDATEEVENTCAPABILITY = 11283
    UA_NS0ID_AGGREGATEFUNCTION_TIMEAVERAGE2 = 11285
    UA_NS0ID_AGGREGATEFUNCTION_MINIMUM2 = 11286
    UA_NS0ID_AGGREGATEFUNCTION_MAXIMUM2 = 11287
    UA_NS0ID_AGGREGATEFUNCTION_RANGE2 = 11288
    UA_NS0ID_AGGREGATEFUNCTION_WORSTQUALITY2 = 11292
    UA_NS0ID_PERFORMUPDATETYPE = 11293
    UA_NS0ID_UPDATESTRUCTUREDATADETAILS = 11295
    UA_NS0ID_UPDATESTRUCTUREDATADETAILS_ENCODING_DEFAULTXML = 11296
    UA_NS0ID_UPDATESTRUCTUREDATADETAILS_ENCODING_DEFAULTBINARY = 11300
    UA_NS0ID_AGGREGATEFUNCTION_TOTAL2 = 11304
    UA_NS0ID_AGGREGATEFUNCTION_MINIMUMACTUALTIME2 = 11305
    UA_NS0ID_AGGREGATEFUNCTION_MAXIMUMACTUALTIME2 = 11306
    UA_NS0ID_AGGREGATEFUNCTION_DURATIONINSTATEZERO = 11307
    UA_NS0ID_AGGREGATEFUNCTION_DURATIONINSTATENONZERO = 11308
    UA_NS0ID_SERVER_SERVERREDUNDANCY_CURRENTSERVERID = 11312
    UA_NS0ID_SERVER_SERVERREDUNDANCY_REDUNDANTSERVERARRAY = 11313
    UA_NS0ID_SERVER_SERVERREDUNDANCY_SERVERURIARRAY = 11314
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_UNSHELVEDTOTIMEDSHELVED_TRANSITIONNUMBER = 11322
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_UNSHELVEDTOONESHOTSHELVED_TRANSITIONNUMBER = 11323
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_TIMEDSHELVEDTOUNSHELVED_TRANSITIONNUMBER = 11324
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_TIMEDSHELVEDTOONESHOTSHELVED_TRANSITIONNUMBER = 11325
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_ONESHOTSHELVEDTOUNSHELVED_TRANSITIONNUMBER = 11326
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_ONESHOTSHELVEDTOTIMEDSHELVED_TRANSITIONNUMBER = 11327
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LOWLOWTOLOW_TRANSITIONNUMBER = 11340
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LOWTOLOWLOW_TRANSITIONNUMBER = 11341
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_HIGHHIGHTOHIGH_TRANSITIONNUMBER = 11342
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_HIGHTOHIGHHIGH_TRANSITIONNUMBER = 11343
    UA_NS0ID_AGGREGATEFUNCTION_STANDARDDEVIATIONSAMPLE = 11426
    UA_NS0ID_AGGREGATEFUNCTION_STANDARDDEVIATIONPOPULATION = 11427
    UA_NS0ID_AGGREGATEFUNCTION_VARIANCESAMPLE = 11428
    UA_NS0ID_AGGREGATEFUNCTION_VARIANCEPOPULATION = 11429
    UA_NS0ID_ENUMSTRINGS = 11432
    UA_NS0ID_VALUEASTEXT = 11433
    UA_NS0ID_PROGRESSEVENTTYPE = 11436
    UA_NS0ID_PROGRESSEVENTTYPE_EVENTID = 11437
    UA_NS0ID_PROGRESSEVENTTYPE_EVENTTYPE = 11438
    UA_NS0ID_PROGRESSEVENTTYPE_SOURCENODE = 11439
    UA_NS0ID_PROGRESSEVENTTYPE_SOURCENAME = 11440
    UA_NS0ID_PROGRESSEVENTTYPE_TIME = 11441
    UA_NS0ID_PROGRESSEVENTTYPE_RECEIVETIME = 11442
    UA_NS0ID_PROGRESSEVENTTYPE_LOCALTIME = 11443
    UA_NS0ID_PROGRESSEVENTTYPE_MESSAGE = 11444
    UA_NS0ID_PROGRESSEVENTTYPE_SEVERITY = 11445
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE = 11446
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_EVENTID = 11447
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_EVENTTYPE = 11448
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_SOURCENODE = 11449
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_SOURCENAME = 11450
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_TIME = 11451
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_RECEIVETIME = 11452
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_LOCALTIME = 11453
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_MESSAGE = 11454
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_SEVERITY = 11455
    UA_NS0ID_TRANSITIONVARIABLETYPE_EFFECTIVETRANSITIONTIME = 11456
    UA_NS0ID_FINITETRANSITIONVARIABLETYPE_EFFECTIVETRANSITIONTIME = 11457
    UA_NS0ID_STATEMACHINETYPE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11458
    UA_NS0ID_FINITESTATEMACHINETYPE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11459
    UA_NS0ID_TRANSITIONEVENTTYPE_TRANSITION_EFFECTIVETRANSITIONTIME = 11460
    UA_NS0ID_MULTISTATEVALUEDISCRETETYPE_VALUEASTEXT = 11461
    UA_NS0ID_PROGRAMTRANSITIONEVENTTYPE_TRANSITION_EFFECTIVETRANSITIONTIME = 11462
    UA_NS0ID_PROGRAMTRANSITIONAUDITEVENTTYPE_TRANSITION_EFFECTIVETRANSITIONTIME = 11463
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11464
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11465
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11466
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11467
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11468
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11469
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11470
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11471
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11472
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11473
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11474
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11475
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11476
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11477
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11478
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11479
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11480
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11481
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11482
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11483
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_SECURECHANNELID = 11485
    UA_NS0ID_OPTIONSETTYPE = 11487
    UA_NS0ID_OPTIONSETTYPE_OPTIONSETVALUES = 11488
    UA_NS0ID_SERVERTYPE_GETMONITOREDITEMS = 11489
    UA_NS0ID_SERVERTYPE_GETMONITOREDITEMS_INPUTARGUMENTS = 11490
    UA_NS0ID_SERVERTYPE_GETMONITOREDITEMS_OUTPUTARGUMENTS = 11491
    UA_NS0ID_SERVER_GETMONITOREDITEMS = 11492
    UA_NS0ID_SERVER_GETMONITOREDITEMS_INPUTARGUMENTS = 11493
    UA_NS0ID_SERVER_GETMONITOREDITEMS_OUTPUTARGUMENTS = 11494
    UA_NS0ID_GETMONITOREDITEMSMETHODTYPE = 11495
    UA_NS0ID_GETMONITOREDITEMSMETHODTYPE_INPUTARGUMENTS = 11496
    UA_NS0ID_GETMONITOREDITEMSMETHODTYPE_OUTPUTARGUMENTS = 11497
    UA_NS0ID_MAXSTRINGLENGTH = 11498
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_STARTOFARCHIVE = 11499
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_STARTOFONLINEARCHIVE = 11500
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_DELETEEVENTCAPABILITY = 11501
    UA_NS0ID_HISTORYSERVERCAPABILITIES_DELETEEVENTCAPABILITY = 11502
    UA_NS0ID_HACONFIGURATION_STARTOFARCHIVE = 11503
    UA_NS0ID_HACONFIGURATION_STARTOFONLINEARCHIVE = 11504
    UA_NS0ID_AGGREGATEFUNCTION_STARTBOUND = 11505
    UA_NS0ID_AGGREGATEFUNCTION_ENDBOUND = 11506
    UA_NS0ID_AGGREGATEFUNCTION_DELTABOUNDS = 11507
    UA_NS0ID_MODELLINGRULE_OPTIONALPLACEHOLDER = 11508
    UA_NS0ID_MODELLINGRULE_OPTIONALPLACEHOLDER_NAMINGRULE = 11509
    UA_NS0ID_MODELLINGRULE_MANDATORYPLACEHOLDER = 11510
    UA_NS0ID_MODELLINGRULE_MANDATORYPLACEHOLDER_NAMINGRULE = 11511
    UA_NS0ID_MAXARRAYLENGTH = 11512
    UA_NS0ID_ENGINEERINGUNITS = 11513
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_MAXARRAYLENGTH = 11514
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_MAXSTRINGLENGTH = 11515
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS = 11516
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERREAD = 11517
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERWRITE = 11519
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERMETHODCALL = 11521
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERBROWSE = 11522
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERREGISTERNODES = 11523
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERTRANSLATEBROWSEPATHSTONODEIDS = 11524
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERNODEMANAGEMENT = 11525
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXMONITOREDITEMSPERCALL = 11526
    UA_NS0ID_SERVERTYPE_NAMESPACES = 11527
    UA_NS0ID_SERVERCAPABILITIESTYPE_MAXARRAYLENGTH = 11549
    UA_NS0ID_SERVERCAPABILITIESTYPE_MAXSTRINGLENGTH = 11550
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS = 11551
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERREAD = 11552
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERWRITE = 11554
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERMETHODCALL = 11556
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERBROWSE = 11557
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERREGISTERNODES = 11558
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERTRANSLATEBROWSEPATHSTONODEIDS = 11559
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERNODEMANAGEMENT = 11560
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXMONITOREDITEMSPERCALL = 11561
    UA_NS0ID_SERVERCAPABILITIESTYPE_VENDORCAPABILITY_PLACEHOLDER = 11562
    UA_NS0ID_OPERATIONLIMITSTYPE = 11564
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERREAD = 11565
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERWRITE = 11567
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERMETHODCALL = 11569
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERBROWSE = 11570
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERREGISTERNODES = 11571
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERTRANSLATEBROWSEPATHSTONODEIDS = 11572
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERNODEMANAGEMENT = 11573
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXMONITOREDITEMSPERCALL = 11574
    UA_NS0ID_FILETYPE = 11575
    UA_NS0ID_FILETYPE_SIZE = 11576
    UA_NS0ID_FILETYPE_OPENCOUNT = 11579
    UA_NS0ID_FILETYPE_OPEN = 11580
    UA_NS0ID_FILETYPE_OPEN_INPUTARGUMENTS = 11581
    UA_NS0ID_FILETYPE_OPEN_OUTPUTARGUMENTS = 11582
    UA_NS0ID_FILETYPE_CLOSE = 11583
    UA_NS0ID_FILETYPE_CLOSE_INPUTARGUMENTS = 11584
    UA_NS0ID_FILETYPE_READ = 11585
    UA_NS0ID_FILETYPE_READ_INPUTARGUMENTS = 11586
    UA_NS0ID_FILETYPE_READ_OUTPUTARGUMENTS = 11587
    UA_NS0ID_FILETYPE_WRITE = 11588
    UA_NS0ID_FILETYPE_WRITE_INPUTARGUMENTS = 11589
    UA_NS0ID_FILETYPE_GETPOSITION = 11590
    UA_NS0ID_FILETYPE_GETPOSITION_INPUTARGUMENTS = 11591
    UA_NS0ID_FILETYPE_GETPOSITION_OUTPUTARGUMENTS = 11592
    UA_NS0ID_FILETYPE_SETPOSITION = 11593
    UA_NS0ID_FILETYPE_SETPOSITION_INPUTARGUMENTS = 11594
    UA_NS0ID_ADDRESSSPACEFILETYPE = 11595
    UA_NS0ID_ADDRESSSPACEFILETYPE_SIZE = 11596
    UA_NS0ID_ADDRESSSPACEFILETYPE_OPENCOUNT = 11599
    UA_NS0ID_ADDRESSSPACEFILETYPE_OPEN = 11600
    UA_NS0ID_ADDRESSSPACEFILETYPE_OPEN_INPUTARGUMENTS = 11601
    UA_NS0ID_ADDRESSSPACEFILETYPE_OPEN_OUTPUTARGUMENTS = 11602
    UA_NS0ID_ADDRESSSPACEFILETYPE_CLOSE = 11603
    UA_NS0ID_ADDRESSSPACEFILETYPE_CLOSE_INPUTARGUMENTS = 11604
    UA_NS0ID_ADDRESSSPACEFILETYPE_READ = 11605
    UA_NS0ID_ADDRESSSPACEFILETYPE_READ_INPUTARGUMENTS = 11606
    UA_NS0ID_ADDRESSSPACEFILETYPE_READ_OUTPUTARGUMENTS = 11607
    UA_NS0ID_ADDRESSSPACEFILETYPE_WRITE = 11608
    UA_NS0ID_ADDRESSSPACEFILETYPE_WRITE_INPUTARGUMENTS = 11609
    UA_NS0ID_ADDRESSSPACEFILETYPE_GETPOSITION = 11610
    UA_NS0ID_ADDRESSSPACEFILETYPE_GETPOSITION_INPUTARGUMENTS = 11611
    UA_NS0ID_ADDRESSSPACEFILETYPE_GETPOSITION_OUTPUTARGUMENTS = 11612
    UA_NS0ID_ADDRESSSPACEFILETYPE_SETPOSITION = 11613
    UA_NS0ID_ADDRESSSPACEFILETYPE_SETPOSITION_INPUTARGUMENTS = 11614
    UA_NS0ID_ADDRESSSPACEFILETYPE_EXPORTNAMESPACE = 11615
    UA_NS0ID_NAMESPACEMETADATATYPE = 11616
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEURI = 11617
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEVERSION = 11618
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEPUBLICATIONDATE = 11619
    UA_NS0ID_NAMESPACEMETADATATYPE_ISNAMESPACESUBSET = 11620
    UA_NS0ID_NAMESPACEMETADATATYPE_STATICNODEIDTYPES = 11621
    UA_NS0ID_NAMESPACEMETADATATYPE_STATICNUMERICNODEIDRANGE = 11622
    UA_NS0ID_NAMESPACEMETADATATYPE_STATICSTRINGNODEIDPATTERN = 11623
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE = 11624
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_SIZE = 11625
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_OPENCOUNT = 11628
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_OPEN = 11629
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_OPEN_INPUTARGUMENTS = 11630
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_OPEN_OUTPUTARGUMENTS = 11631
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_CLOSE = 11632
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_CLOSE_INPUTARGUMENTS = 11633
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_READ = 11634
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_READ_INPUTARGUMENTS = 11635
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_READ_OUTPUTARGUMENTS = 11636
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_WRITE = 11637
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_WRITE_INPUTARGUMENTS = 11638
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_GETPOSITION = 11639
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_GETPOSITION_INPUTARGUMENTS = 11640
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_GETPOSITION_OUTPUTARGUMENTS = 11641
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_SETPOSITION = 11642
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_SETPOSITION_INPUTARGUMENTS = 11643
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_EXPORTNAMESPACE = 11644
    UA_NS0ID_NAMESPACESTYPE = 11645
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER = 11646
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEURI = 11647
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEVERSION = 11648
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEPUBLICATIONDATE = 11649
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_ISNAMESPACESUBSET = 11650
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_STATICNODEIDTYPES = 11651
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_STATICNUMERICNODEIDRANGE = 11652
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_STATICSTRINGNODEIDPATTERN = 11653
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE = 11654
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_SIZE = 11655
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_OPENCOUNT = 11658
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_OPEN = 11659
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_OPEN_INPUTARGUMENTS = 11660
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_OPEN_OUTPUTARGUMENTS = 11661
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_CLOSE = 11662
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_CLOSE_INPUTARGUMENTS = 11663
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_READ = 11664
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_READ_INPUTARGUMENTS = 11665
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_READ_OUTPUTARGUMENTS = 11666
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_WRITE = 11667
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_WRITE_INPUTARGUMENTS = 11668
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_GETPOSITION = 11669
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_GETPOSITION_INPUTARGUMENTS = 11670
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_GETPOSITION_OUTPUTARGUMENTS = 11671
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_SETPOSITION = 11672
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_SETPOSITION_INPUTARGUMENTS = 11673
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_EXPORTNAMESPACE = 11674
    UA_NS0ID_SYSTEMSTATUSCHANGEEVENTTYPE_SYSTEMSTATE = 11696
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSTYPE_SAMPLEDMONITOREDITEMSCOUNT = 11697
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSTYPE_MAXSAMPLEDMONITOREDITEMSCOUNT = 11698
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSTYPE_DISABLEDMONITOREDITEMSSAMPLINGCOUNT = 11699
    UA_NS0ID_OPTIONSETTYPE_BITMASK = 11701
    UA_NS0ID_SERVER_SERVERCAPABILITIES_MAXARRAYLENGTH = 11702
    UA_NS0ID_SERVER_SERVERCAPABILITIES_MAXSTRINGLENGTH = 11703
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS = 11704
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERREAD = 11705
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERWRITE = 11707
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERMETHODCALL = 11709
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERBROWSE = 11710
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERREGISTERNODES = 11711
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERTRANSLATEBROWSEPATHSTONODEIDS = 11712
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERNODEMANAGEMENT = 11713
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXMONITOREDITEMSPERCALL = 11714
    UA_NS0ID_SERVER_NAMESPACES = 11715
    UA_NS0ID_BITFIELDMASKDATATYPE = 11737
    UA_NS0ID_OPENMETHODTYPE = 11738
    UA_NS0ID_OPENMETHODTYPE_INPUTARGUMENTS = 11739
    UA_NS0ID_OPENMETHODTYPE_OUTPUTARGUMENTS = 11740
    UA_NS0ID_CLOSEMETHODTYPE = 11741
    UA_NS0ID_CLOSEMETHODTYPE_INPUTARGUMENTS = 11742
    UA_NS0ID_READMETHODTYPE = 11743
    UA_NS0ID_READMETHODTYPE_INPUTARGUMENTS = 11744
    UA_NS0ID_READMETHODTYPE_OUTPUTARGUMENTS = 11745
    UA_NS0ID_WRITEMETHODTYPE = 11746
    UA_NS0ID_WRITEMETHODTYPE_INPUTARGUMENTS = 11747
    UA_NS0ID_GETPOSITIONMETHODTYPE = 11748
    UA_NS0ID_GETPOSITIONMETHODTYPE_INPUTARGUMENTS = 11749
    UA_NS0ID_GETPOSITIONMETHODTYPE_OUTPUTARGUMENTS = 11750
    UA_NS0ID_SETPOSITIONMETHODTYPE = 11751
    UA_NS0ID_SETPOSITIONMETHODTYPE_INPUTARGUMENTS = 11752
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE = 11753
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_EVENTID = 11754
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_EVENTTYPE = 11755
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SOURCENODE = 11756
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SOURCENAME = 11757
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_TIME = 11758
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_RECEIVETIME = 11759
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LOCALTIME = 11760
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_MESSAGE = 11761
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SEVERITY = 11762
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONDITIONCLASSID = 11763
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONDITIONCLASSNAME = 11764
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONDITIONNAME = 11765
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_BRANCHID = 11766
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_RETAIN = 11767
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLEDSTATE = 11768
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLEDSTATE_ID = 11769
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLEDSTATE_NAME = 11770
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLEDSTATE_NUMBER = 11771
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 11772
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 11773
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 11774
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLEDSTATE_TRUESTATE = 11775
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLEDSTATE_FALSESTATE = 11776
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_QUALITY = 11777
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_QUALITY_SOURCETIMESTAMP = 11778
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LASTSEVERITY = 11779
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 11780
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_COMMENT = 11781
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_COMMENT_SOURCETIMESTAMP = 11782
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CLIENTUSERID = 11783
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_DISABLE = 11784
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ENABLE = 11785
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ADDCOMMENT = 11786
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 11787
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONDITIONREFRESH = 11788
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 11789
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKEDSTATE = 11790
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKEDSTATE_ID = 11791
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKEDSTATE_NAME = 11792
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKEDSTATE_NUMBER = 11793
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 11794
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 11795
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 11796
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKEDSTATE_TRUESTATE = 11797
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKEDSTATE_FALSESTATE = 11798
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRMEDSTATE = 11799
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRMEDSTATE_ID = 11800
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRMEDSTATE_NAME = 11801
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRMEDSTATE_NUMBER = 11802
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 11803
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 11804
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 11805
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 11806
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 11807
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKNOWLEDGE = 11808
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 11809
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRM = 11810
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONFIRM_INPUTARGUMENTS = 11811
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACTIVESTATE = 11812
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACTIVESTATE_ID = 11813
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACTIVESTATE_NAME = 11814
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACTIVESTATE_NUMBER = 11815
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 11816
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 11817
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 11818
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACTIVESTATE_TRUESTATE = 11819
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ACTIVESTATE_FALSESTATE = 11820
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_INPUTNODE = 11821
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDSTATE = 11822
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDSTATE_ID = 11823
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDSTATE_NAME = 11824
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDSTATE_NUMBER = 11825
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 11826
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 11827
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 11828
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 11829
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 11830
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE = 11831
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 11832
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 11833
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 11834
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 11835
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 11836
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 11837
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 11838
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 11839
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 11840
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 11841
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 11842
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 11843
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_UNSHELVE = 11844
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 11845
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 11846
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 11847
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESSEDORSHELVED = 11848
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_MAXTIMESHELVED = 11849
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_NORMALSTATE = 11850
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_COMMENT = 11851
    UA_NS0ID_AUDITCONDITIONRESPONDEVENTTYPE_SELECTEDRESPONSE = 11852
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_COMMENT = 11853
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_COMMENT = 11854
    UA_NS0ID_AUDITCONDITIONSHELVINGEVENTTYPE_SHELVINGTIME = 11855
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE = 11856
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_EVENTID = 11857
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_EVENTTYPE = 11858
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_SOURCENODE = 11859
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_SOURCENAME = 11860
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_TIME = 11861
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_RECEIVETIME = 11862
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_LOCALTIME = 11863
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_MESSAGE = 11864
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_SEVERITY = 11865
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_ACTIONTIMESTAMP = 11866
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_STATUS = 11867
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_SERVERID = 11868
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_CLIENTAUDITENTRYID = 11869
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_CLIENTUSERID = 11870
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_METHODID = 11871
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_INPUTARGUMENTS = 11872
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_OLDSTATEID = 11873
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_NEWSTATEID = 11874
    UA_NS0ID_AUDITPROGRAMTRANSITIONEVENTTYPE_TRANSITIONNUMBER = 11875
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_AGGREGATEFUNCTIONS = 11876
    UA_NS0ID_HACONFIGURATION_AGGREGATEFUNCTIONS = 11877
    UA_NS0ID_NODECLASS_ENUMVALUES = 11878
    UA_NS0ID_INSTANCENODE = 11879
    UA_NS0ID_TYPENODE = 11880
    UA_NS0ID_NODEATTRIBUTESMASK_ENUMVALUES = 11881
    UA_NS0ID_BROWSERESULTMASK_ENUMVALUES = 11883
    UA_NS0ID_HISTORYUPDATETYPE_ENUMVALUES = 11884
    UA_NS0ID_PERFORMUPDATETYPE_ENUMVALUES = 11885
    UA_NS0ID_INSTANCENODE_ENCODING_DEFAULTXML = 11887
    UA_NS0ID_TYPENODE_ENCODING_DEFAULTXML = 11888
    UA_NS0ID_INSTANCENODE_ENCODING_DEFAULTBINARY = 11889
    UA_NS0ID_TYPENODE_ENCODING_DEFAULTBINARY = 11890
    UA_NS0ID_SESSIONDIAGNOSTICSOBJECTTYPE_SESSIONDIAGNOSTICS_UNAUTHORIZEDREQUESTCOUNT = 11891
    UA_NS0ID_SESSIONDIAGNOSTICSVARIABLETYPE_UNAUTHORIZEDREQUESTCOUNT = 11892
    UA_NS0ID_OPENFILEMODE = 11939
    UA_NS0ID_OPENFILEMODE_ENUMVALUES = 11940
    UA_NS0ID_MODELCHANGESTRUCTUREVERBMASK = 11941
    UA_NS0ID_MODELCHANGESTRUCTUREVERBMASK_ENUMVALUES = 11942
    UA_NS0ID_ENDPOINTURLLISTDATATYPE = 11943
    UA_NS0ID_NETWORKGROUPDATATYPE = 11944
    UA_NS0ID_NONTRANSPARENTNETWORKREDUNDANCYTYPE = 11945
    UA_NS0ID_NONTRANSPARENTNETWORKREDUNDANCYTYPE_REDUNDANCYSUPPORT = 11946
    UA_NS0ID_NONTRANSPARENTNETWORKREDUNDANCYTYPE_SERVERURIARRAY = 11947
    UA_NS0ID_NONTRANSPARENTNETWORKREDUNDANCYTYPE_SERVERNETWORKGROUPS = 11948
    UA_NS0ID_ENDPOINTURLLISTDATATYPE_ENCODING_DEFAULTXML = 11949
    UA_NS0ID_NETWORKGROUPDATATYPE_ENCODING_DEFAULTXML = 11950
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTURLLISTDATATYPE = 11951
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTURLLISTDATATYPE_DATATYPEVERSION = 11952
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTURLLISTDATATYPE_DICTIONARYFRAGMENT = 11953
    UA_NS0ID_OPCUA_XMLSCHEMA_NETWORKGROUPDATATYPE = 11954
    UA_NS0ID_OPCUA_XMLSCHEMA_NETWORKGROUPDATATYPE_DATATYPEVERSION = 11955
    UA_NS0ID_OPCUA_XMLSCHEMA_NETWORKGROUPDATATYPE_DICTIONARYFRAGMENT = 11956
    UA_NS0ID_ENDPOINTURLLISTDATATYPE_ENCODING_DEFAULTBINARY = 11957
    UA_NS0ID_NETWORKGROUPDATATYPE_ENCODING_DEFAULTBINARY = 11958
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTURLLISTDATATYPE = 11959
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTURLLISTDATATYPE_DATATYPEVERSION = 11960
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTURLLISTDATATYPE_DICTIONARYFRAGMENT = 11961
    UA_NS0ID_OPCUA_BINARYSCHEMA_NETWORKGROUPDATATYPE = 11962
    UA_NS0ID_OPCUA_BINARYSCHEMA_NETWORKGROUPDATATYPE_DATATYPEVERSION = 11963
    UA_NS0ID_OPCUA_BINARYSCHEMA_NETWORKGROUPDATATYPE_DICTIONARYFRAGMENT = 11964
    UA_NS0ID_ARRAYITEMTYPE = 12021
    UA_NS0ID_ARRAYITEMTYPE_DEFINITION = 12022
    UA_NS0ID_ARRAYITEMTYPE_VALUEPRECISION = 12023
    UA_NS0ID_ARRAYITEMTYPE_INSTRUMENTRANGE = 12024
    UA_NS0ID_ARRAYITEMTYPE_EURANGE = 12025
    UA_NS0ID_ARRAYITEMTYPE_ENGINEERINGUNITS = 12026
    UA_NS0ID_ARRAYITEMTYPE_TITLE = 12027
    UA_NS0ID_ARRAYITEMTYPE_AXISSCALETYPE = 12028
    UA_NS0ID_YARRAYITEMTYPE = 12029
    UA_NS0ID_YARRAYITEMTYPE_DEFINITION = 12030
    UA_NS0ID_YARRAYITEMTYPE_VALUEPRECISION = 12031
    UA_NS0ID_YARRAYITEMTYPE_INSTRUMENTRANGE = 12032
    UA_NS0ID_YARRAYITEMTYPE_EURANGE = 12033
    UA_NS0ID_YARRAYITEMTYPE_ENGINEERINGUNITS = 12034
    UA_NS0ID_YARRAYITEMTYPE_TITLE = 12035
    UA_NS0ID_YARRAYITEMTYPE_AXISSCALETYPE = 12036
    UA_NS0ID_YARRAYITEMTYPE_XAXISDEFINITION = 12037
    UA_NS0ID_XYARRAYITEMTYPE = 12038
    UA_NS0ID_XYARRAYITEMTYPE_DEFINITION = 12039
    UA_NS0ID_XYARRAYITEMTYPE_VALUEPRECISION = 12040
    UA_NS0ID_XYARRAYITEMTYPE_INSTRUMENTRANGE = 12041
    UA_NS0ID_XYARRAYITEMTYPE_EURANGE = 12042
    UA_NS0ID_XYARRAYITEMTYPE_ENGINEERINGUNITS = 12043
    UA_NS0ID_XYARRAYITEMTYPE_TITLE = 12044
    UA_NS0ID_XYARRAYITEMTYPE_AXISSCALETYPE = 12045
    UA_NS0ID_XYARRAYITEMTYPE_XAXISDEFINITION = 12046
    UA_NS0ID_IMAGEITEMTYPE = 12047
    UA_NS0ID_IMAGEITEMTYPE_DEFINITION = 12048
    UA_NS0ID_IMAGEITEMTYPE_VALUEPRECISION = 12049
    UA_NS0ID_IMAGEITEMTYPE_INSTRUMENTRANGE = 12050
    UA_NS0ID_IMAGEITEMTYPE_EURANGE = 12051
    UA_NS0ID_IMAGEITEMTYPE_ENGINEERINGUNITS = 12052
    UA_NS0ID_IMAGEITEMTYPE_TITLE = 12053
    UA_NS0ID_IMAGEITEMTYPE_AXISSCALETYPE = 12054
    UA_NS0ID_IMAGEITEMTYPE_XAXISDEFINITION = 12055
    UA_NS0ID_IMAGEITEMTYPE_YAXISDEFINITION = 12056
    UA_NS0ID_CUBEITEMTYPE = 12057
    UA_NS0ID_CUBEITEMTYPE_DEFINITION = 12058
    UA_NS0ID_CUBEITEMTYPE_VALUEPRECISION = 12059
    UA_NS0ID_CUBEITEMTYPE_INSTRUMENTRANGE = 12060
    UA_NS0ID_CUBEITEMTYPE_EURANGE = 12061
    UA_NS0ID_CUBEITEMTYPE_ENGINEERINGUNITS = 12062
    UA_NS0ID_CUBEITEMTYPE_TITLE = 12063
    UA_NS0ID_CUBEITEMTYPE_AXISSCALETYPE = 12064
    UA_NS0ID_CUBEITEMTYPE_XAXISDEFINITION = 12065
    UA_NS0ID_CUBEITEMTYPE_YAXISDEFINITION = 12066
    UA_NS0ID_CUBEITEMTYPE_ZAXISDEFINITION = 12067
    UA_NS0ID_NDIMENSIONARRAYITEMTYPE = 12068
    UA_NS0ID_NDIMENSIONARRAYITEMTYPE_DEFINITION = 12069
    UA_NS0ID_NDIMENSIONARRAYITEMTYPE_VALUEPRECISION = 12070
    UA_NS0ID_NDIMENSIONARRAYITEMTYPE_INSTRUMENTRANGE = 12071
    UA_NS0ID_NDIMENSIONARRAYITEMTYPE_EURANGE = 12072
    UA_NS0ID_NDIMENSIONARRAYITEMTYPE_ENGINEERINGUNITS = 12073
    UA_NS0ID_NDIMENSIONARRAYITEMTYPE_TITLE = 12074
    UA_NS0ID_NDIMENSIONARRAYITEMTYPE_AXISSCALETYPE = 12075
    UA_NS0ID_NDIMENSIONARRAYITEMTYPE_AXISDEFINITION = 12076
    UA_NS0ID_AXISSCALEENUMERATION = 12077
    UA_NS0ID_AXISSCALEENUMERATION_ENUMSTRINGS = 12078
    UA_NS0ID_AXISINFORMATION = 12079
    UA_NS0ID_XVTYPE = 12080
    UA_NS0ID_AXISINFORMATION_ENCODING_DEFAULTXML = 12081
    UA_NS0ID_XVTYPE_ENCODING_DEFAULTXML = 12082
    UA_NS0ID_OPCUA_XMLSCHEMA_AXISINFORMATION = 12083
    UA_NS0ID_OPCUA_XMLSCHEMA_AXISINFORMATION_DATATYPEVERSION = 12084
    UA_NS0ID_OPCUA_XMLSCHEMA_AXISINFORMATION_DICTIONARYFRAGMENT = 12085
    UA_NS0ID_OPCUA_XMLSCHEMA_XVTYPE = 12086
    UA_NS0ID_OPCUA_XMLSCHEMA_XVTYPE_DATATYPEVERSION = 12087
    UA_NS0ID_OPCUA_XMLSCHEMA_XVTYPE_DICTIONARYFRAGMENT = 12088
    UA_NS0ID_AXISINFORMATION_ENCODING_DEFAULTBINARY = 12089
    UA_NS0ID_XVTYPE_ENCODING_DEFAULTBINARY = 12090
    UA_NS0ID_OPCUA_BINARYSCHEMA_AXISINFORMATION = 12091
    UA_NS0ID_OPCUA_BINARYSCHEMA_AXISINFORMATION_DATATYPEVERSION = 12092
    UA_NS0ID_OPCUA_BINARYSCHEMA_AXISINFORMATION_DICTIONARYFRAGMENT = 12093
    UA_NS0ID_OPCUA_BINARYSCHEMA_XVTYPE = 12094
    UA_NS0ID_OPCUA_BINARYSCHEMA_XVTYPE_DATATYPEVERSION = 12095
    UA_NS0ID_OPCUA_BINARYSCHEMA_XVTYPE_DICTIONARYFRAGMENT = 12096
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER = 12097
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS = 12098
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_SESSIONID = 12099
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_SESSIONNAME = 12100
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_CLIENTDESCRIPTION = 12101
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_SERVERURI = 12102
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_ENDPOINTURL = 12103
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_LOCALEIDS = 12104
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_ACTUALSESSIONTIMEOUT = 12105
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_MAXRESPONSEMESSAGESIZE = 12106
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_CLIENTCONNECTIONTIME = 12107
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_CLIENTLASTCONTACTTIME = 12108
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_CURRENTSUBSCRIPTIONSCOUNT = 12109
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_CURRENTMONITOREDITEMSCOUNT = 12110
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_CURRENTPUBLISHREQUESTSINQUEUE = 12111
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_TOTALREQUESTCOUNT = 12112
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_UNAUTHORIZEDREQUESTCOUNT = 12113
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_READCOUNT = 12114
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_HISTORYREADCOUNT = 12115
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_WRITECOUNT = 12116
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_HISTORYUPDATECOUNT = 12117
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_CALLCOUNT = 12118
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_CREATEMONITOREDITEMSCOUNT = 12119
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_MODIFYMONITOREDITEMSCOUNT = 12120
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_SETMONITORINGMODECOUNT = 12121
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_SETTRIGGERINGCOUNT = 12122
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_DELETEMONITOREDITEMSCOUNT = 12123
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_CREATESUBSCRIPTIONCOUNT = 12124
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_MODIFYSUBSCRIPTIONCOUNT = 12125
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_SETPUBLISHINGMODECOUNT = 12126
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_PUBLISHCOUNT = 12127
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_REPUBLISHCOUNT = 12128
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_TRANSFERSUBSCRIPTIONSCOUNT = 12129
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_DELETESUBSCRIPTIONSCOUNT = 12130
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_ADDNODESCOUNT = 12131
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_ADDREFERENCESCOUNT = 12132
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_DELETENODESCOUNT = 12133
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_DELETEREFERENCESCOUNT = 12134
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_BROWSECOUNT = 12135
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_BROWSENEXTCOUNT = 12136
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_TRANSLATEBROWSEPATHSTONODEIDSCOUNT = 12137
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_QUERYFIRSTCOUNT = 12138
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_QUERYNEXTCOUNT = 12139
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_REGISTERNODESCOUNT = 12140
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONDIAGNOSTICS_UNREGISTERNODESCOUNT = 12141
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS = 12142
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS_SESSIONID = 12143
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS_CLIENTUSERIDOFSESSION = 12144
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS_CLIENTUSERIDHISTORY = 12145
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS_AUTHENTICATIONMECHANISM = 12146
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS_ENCODING = 12147
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS_TRANSPORTPROTOCOL = 12148
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS_SECURITYMODE = 12149
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS_SECURITYPOLICYURI = 12150
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SESSIONSECURITYDIAGNOSTICS_CLIENTCERTIFICATE = 12151
    UA_NS0ID_SESSIONSDIAGNOSTICSSUMMARYTYPE_CLIENTNAME_PLACEHOLDER_SUBSCRIPTIONDIAGNOSTICSARRAY = 12152
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERHISTORYREADDATA = 12153
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERHISTORYREADEVENTS = 12154
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERHISTORYUPDATEDATA = 12155
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERHISTORYUPDATEEVENTS = 12156
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERHISTORYREADDATA = 12157
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERHISTORYREADEVENTS = 12158
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERHISTORYUPDATEDATA = 12159
    UA_NS0ID_SERVERCAPABILITIESTYPE_OPERATIONLIMITS_MAXNODESPERHISTORYUPDATEEVENTS = 12160
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERHISTORYREADDATA = 12161
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERHISTORYREADEVENTS = 12162
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERHISTORYUPDATEDATA = 12163
    UA_NS0ID_OPERATIONLIMITSTYPE_MAXNODESPERHISTORYUPDATEEVENTS = 12164
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERHISTORYREADDATA = 12165
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERHISTORYREADEVENTS = 12166
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERHISTORYUPDATEDATA = 12167
    UA_NS0ID_SERVER_SERVERCAPABILITIES_OPERATIONLIMITS_MAXNODESPERHISTORYUPDATEEVENTS = 12168
    UA_NS0ID_NAMINGRULETYPE_ENUMVALUES = 12169
    UA_NS0ID_VIEWVERSION = 12170
    UA_NS0ID_COMPLEXNUMBERTYPE = 12171
    UA_NS0ID_DOUBLECOMPLEXNUMBERTYPE = 12172
    UA_NS0ID_COMPLEXNUMBERTYPE_ENCODING_DEFAULTXML = 12173
    UA_NS0ID_DOUBLECOMPLEXNUMBERTYPE_ENCODING_DEFAULTXML = 12174
    UA_NS0ID_OPCUA_XMLSCHEMA_COMPLEXNUMBERTYPE = 12175
    UA_NS0ID_OPCUA_XMLSCHEMA_COMPLEXNUMBERTYPE_DATATYPEVERSION = 12176
    UA_NS0ID_OPCUA_XMLSCHEMA_COMPLEXNUMBERTYPE_DICTIONARYFRAGMENT = 12177
    UA_NS0ID_OPCUA_XMLSCHEMA_DOUBLECOMPLEXNUMBERTYPE = 12178
    UA_NS0ID_OPCUA_XMLSCHEMA_DOUBLECOMPLEXNUMBERTYPE_DATATYPEVERSION = 12179
    UA_NS0ID_OPCUA_XMLSCHEMA_DOUBLECOMPLEXNUMBERTYPE_DICTIONARYFRAGMENT = 12180
    UA_NS0ID_COMPLEXNUMBERTYPE_ENCODING_DEFAULTBINARY = 12181
    UA_NS0ID_DOUBLECOMPLEXNUMBERTYPE_ENCODING_DEFAULTBINARY = 12182
    UA_NS0ID_OPCUA_BINARYSCHEMA_COMPLEXNUMBERTYPE = 12183
    UA_NS0ID_OPCUA_BINARYSCHEMA_COMPLEXNUMBERTYPE_DATATYPEVERSION = 12184
    UA_NS0ID_OPCUA_BINARYSCHEMA_COMPLEXNUMBERTYPE_DICTIONARYFRAGMENT = 12185
    UA_NS0ID_OPCUA_BINARYSCHEMA_DOUBLECOMPLEXNUMBERTYPE = 12186
    UA_NS0ID_OPCUA_BINARYSCHEMA_DOUBLECOMPLEXNUMBERTYPE_DATATYPEVERSION = 12187
    UA_NS0ID_OPCUA_BINARYSCHEMA_DOUBLECOMPLEXNUMBERTYPE_DICTIONARYFRAGMENT = 12188
    UA_NS0ID_SERVERONNETWORK = 12189
    UA_NS0ID_FINDSERVERSONNETWORKREQUEST = 12190
    UA_NS0ID_FINDSERVERSONNETWORKRESPONSE = 12191
    UA_NS0ID_REGISTERSERVER2REQUEST = 12193
    UA_NS0ID_REGISTERSERVER2RESPONSE = 12194
    UA_NS0ID_SERVERONNETWORK_ENCODING_DEFAULTXML = 12195
    UA_NS0ID_FINDSERVERSONNETWORKREQUEST_ENCODING_DEFAULTXML = 12196
    UA_NS0ID_FINDSERVERSONNETWORKRESPONSE_ENCODING_DEFAULTXML = 12197
    UA_NS0ID_REGISTERSERVER2REQUEST_ENCODING_DEFAULTXML = 12199
    UA_NS0ID_REGISTERSERVER2RESPONSE_ENCODING_DEFAULTXML = 12200
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVERONNETWORK = 12201
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVERONNETWORK_DATATYPEVERSION = 12202
    UA_NS0ID_OPCUA_XMLSCHEMA_SERVERONNETWORK_DICTIONARYFRAGMENT = 12203
    UA_NS0ID_SERVERONNETWORK_ENCODING_DEFAULTBINARY = 12207
    UA_NS0ID_FINDSERVERSONNETWORKREQUEST_ENCODING_DEFAULTBINARY = 12208
    UA_NS0ID_FINDSERVERSONNETWORKRESPONSE_ENCODING_DEFAULTBINARY = 12209
    UA_NS0ID_REGISTERSERVER2REQUEST_ENCODING_DEFAULTBINARY = 12211
    UA_NS0ID_REGISTERSERVER2RESPONSE_ENCODING_DEFAULTBINARY = 12212
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVERONNETWORK = 12213
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVERONNETWORK_DATATYPEVERSION = 12214
    UA_NS0ID_OPCUA_BINARYSCHEMA_SERVERONNETWORK_DICTIONARYFRAGMENT = 12215
    UA_NS0ID_PROGRESSEVENTTYPE_CONTEXT = 12502
    UA_NS0ID_PROGRESSEVENTTYPE_PROGRESS = 12503
    UA_NS0ID_OPENWITHMASKSMETHODTYPE = 12513
    UA_NS0ID_OPENWITHMASKSMETHODTYPE_INPUTARGUMENTS = 12514
    UA_NS0ID_OPENWITHMASKSMETHODTYPE_OUTPUTARGUMENTS = 12515
    UA_NS0ID_CLOSEANDUPDATEMETHODTYPE = 12516
    UA_NS0ID_CLOSEANDUPDATEMETHODTYPE_OUTPUTARGUMENTS = 12517
    UA_NS0ID_ADDCERTIFICATEMETHODTYPE = 12518
    UA_NS0ID_ADDCERTIFICATEMETHODTYPE_INPUTARGUMENTS = 12519
    UA_NS0ID_REMOVECERTIFICATEMETHODTYPE = 12520
    UA_NS0ID_REMOVECERTIFICATEMETHODTYPE_INPUTARGUMENTS = 12521
    UA_NS0ID_TRUSTLISTTYPE = 12522
    UA_NS0ID_TRUSTLISTTYPE_SIZE = 12523
    UA_NS0ID_TRUSTLISTTYPE_OPENCOUNT = 12526
    UA_NS0ID_TRUSTLISTTYPE_OPEN = 12527
    UA_NS0ID_TRUSTLISTTYPE_OPEN_INPUTARGUMENTS = 12528
    UA_NS0ID_TRUSTLISTTYPE_OPEN_OUTPUTARGUMENTS = 12529
    UA_NS0ID_TRUSTLISTTYPE_CLOSE = 12530
    UA_NS0ID_TRUSTLISTTYPE_CLOSE_INPUTARGUMENTS = 12531
    UA_NS0ID_TRUSTLISTTYPE_READ = 12532
    UA_NS0ID_TRUSTLISTTYPE_READ_INPUTARGUMENTS = 12533
    UA_NS0ID_TRUSTLISTTYPE_READ_OUTPUTARGUMENTS = 12534
    UA_NS0ID_TRUSTLISTTYPE_WRITE = 12535
    UA_NS0ID_TRUSTLISTTYPE_WRITE_INPUTARGUMENTS = 12536
    UA_NS0ID_TRUSTLISTTYPE_GETPOSITION = 12537
    UA_NS0ID_TRUSTLISTTYPE_GETPOSITION_INPUTARGUMENTS = 12538
    UA_NS0ID_TRUSTLISTTYPE_GETPOSITION_OUTPUTARGUMENTS = 12539
    UA_NS0ID_TRUSTLISTTYPE_SETPOSITION = 12540
    UA_NS0ID_TRUSTLISTTYPE_SETPOSITION_INPUTARGUMENTS = 12541
    UA_NS0ID_TRUSTLISTTYPE_LASTUPDATETIME = 12542
    UA_NS0ID_TRUSTLISTTYPE_OPENWITHMASKS = 12543
    UA_NS0ID_TRUSTLISTTYPE_OPENWITHMASKS_INPUTARGUMENTS = 12544
    UA_NS0ID_TRUSTLISTTYPE_OPENWITHMASKS_OUTPUTARGUMENTS = 12545
    UA_NS0ID_TRUSTLISTTYPE_CLOSEANDUPDATE = 12546
    UA_NS0ID_TRUSTLISTTYPE_CLOSEANDUPDATE_OUTPUTARGUMENTS = 12547
    UA_NS0ID_TRUSTLISTTYPE_ADDCERTIFICATE = 12548
    UA_NS0ID_TRUSTLISTTYPE_ADDCERTIFICATE_INPUTARGUMENTS = 12549
    UA_NS0ID_TRUSTLISTTYPE_REMOVECERTIFICATE = 12550
    UA_NS0ID_TRUSTLISTTYPE_REMOVECERTIFICATE_INPUTARGUMENTS = 12551
    UA_NS0ID_TRUSTLISTMASKS = 12552
    UA_NS0ID_TRUSTLISTMASKS_ENUMVALUES = 12553
    UA_NS0ID_TRUSTLISTDATATYPE = 12554
    UA_NS0ID_CERTIFICATEGROUPTYPE = 12555
    UA_NS0ID_CERTIFICATETYPE = 12556
    UA_NS0ID_APPLICATIONCERTIFICATETYPE = 12557
    UA_NS0ID_HTTPSCERTIFICATETYPE = 12558
    UA_NS0ID_RSAMINAPPLICATIONCERTIFICATETYPE = 12559
    UA_NS0ID_RSASHA256APPLICATIONCERTIFICATETYPE = 12560
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE = 12561
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_EVENTID = 12562
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_EVENTTYPE = 12563
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_SOURCENODE = 12564
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_SOURCENAME = 12565
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_TIME = 12566
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_RECEIVETIME = 12567
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_LOCALTIME = 12568
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_MESSAGE = 12569
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_SEVERITY = 12570
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_ACTIONTIMESTAMP = 12571
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_STATUS = 12572
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_SERVERID = 12573
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_CLIENTAUDITENTRYID = 12574
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_CLIENTUSERID = 12575
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_METHODID = 12576
    UA_NS0ID_TRUSTLISTUPDATEDAUDITEVENTTYPE_INPUTARGUMENTS = 12577
    UA_NS0ID_UPDATECERTIFICATEMETHODTYPE = 12578
    UA_NS0ID_UPDATECERTIFICATEMETHODTYPE_INPUTARGUMENTS = 12579
    UA_NS0ID_UPDATECERTIFICATEMETHODTYPE_OUTPUTARGUMENTS = 12580
    UA_NS0ID_SERVERCONFIGURATIONTYPE = 12581
    UA_NS0ID_SERVERCONFIGURATIONTYPE_SUPPORTEDPRIVATEKEYFORMATS = 12583
    UA_NS0ID_SERVERCONFIGURATIONTYPE_MAXTRUSTLISTSIZE = 12584
    UA_NS0ID_SERVERCONFIGURATIONTYPE_MULTICASTDNSENABLED = 12585
    UA_NS0ID_SERVERCONFIGURATIONTYPE_UPDATECERTIFICATE = 12616
    UA_NS0ID_SERVERCONFIGURATIONTYPE_UPDATECERTIFICATE_INPUTARGUMENTS = 12617
    UA_NS0ID_SERVERCONFIGURATIONTYPE_UPDATECERTIFICATE_OUTPUTARGUMENTS = 12618
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE = 12620
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_EVENTID = 12621
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_EVENTTYPE = 12622
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_SOURCENODE = 12623
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_SOURCENAME = 12624
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_TIME = 12625
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_RECEIVETIME = 12626
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_LOCALTIME = 12627
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_MESSAGE = 12628
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_SEVERITY = 12629
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_ACTIONTIMESTAMP = 12630
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_STATUS = 12631
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_SERVERID = 12632
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_CLIENTAUDITENTRYID = 12633
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_CLIENTUSERID = 12634
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_METHODID = 12635
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_INPUTARGUMENTS = 12636
    UA_NS0ID_SERVERCONFIGURATION = 12637
    UA_NS0ID_SERVERCONFIGURATION_SUPPORTEDPRIVATEKEYFORMATS = 12639
    UA_NS0ID_SERVERCONFIGURATION_MAXTRUSTLISTSIZE = 12640
    UA_NS0ID_SERVERCONFIGURATION_MULTICASTDNSENABLED = 12641
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST = 12642
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_SIZE = 12643
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENCOUNT = 12646
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPEN = 12647
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPEN_INPUTARGUMENTS = 12648
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 12649
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSE = 12650
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSE_INPUTARGUMENTS = 12651
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_READ = 12652
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_READ_INPUTARGUMENTS = 12653
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_READ_OUTPUTARGUMENTS = 12654
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_WRITE = 12655
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_WRITE_INPUTARGUMENTS = 12656
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_GETPOSITION = 12657
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 12658
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 12659
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_SETPOSITION = 12660
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 12661
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_LASTUPDATETIME = 12662
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENWITHMASKS = 12663
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 12664
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 12665
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSEANDUPDATE = 12666
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 12667
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_ADDCERTIFICATE = 12668
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 12669
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_REMOVECERTIFICATE = 12670
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 12671
    UA_NS0ID_TRUSTLISTDATATYPE_ENCODING_DEFAULTXML = 12676
    UA_NS0ID_OPCUA_XMLSCHEMA_TRUSTLISTDATATYPE = 12677
    UA_NS0ID_OPCUA_XMLSCHEMA_TRUSTLISTDATATYPE_DATATYPEVERSION = 12678
    UA_NS0ID_OPCUA_XMLSCHEMA_TRUSTLISTDATATYPE_DICTIONARYFRAGMENT = 12679
    UA_NS0ID_TRUSTLISTDATATYPE_ENCODING_DEFAULTBINARY = 12680
    UA_NS0ID_OPCUA_BINARYSCHEMA_TRUSTLISTDATATYPE = 12681
    UA_NS0ID_OPCUA_BINARYSCHEMA_TRUSTLISTDATATYPE_DATATYPEVERSION = 12682
    UA_NS0ID_OPCUA_BINARYSCHEMA_TRUSTLISTDATATYPE_DICTIONARYFRAGMENT = 12683
    UA_NS0ID_FILETYPE_WRITABLE = 12686
    UA_NS0ID_FILETYPE_USERWRITABLE = 12687
    UA_NS0ID_ADDRESSSPACEFILETYPE_WRITABLE = 12688
    UA_NS0ID_ADDRESSSPACEFILETYPE_USERWRITABLE = 12689
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_WRITABLE = 12690
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_USERWRITABLE = 12691
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_WRITABLE = 12692
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_USERWRITABLE = 12693
    UA_NS0ID_TRUSTLISTTYPE_WRITABLE = 12698
    UA_NS0ID_TRUSTLISTTYPE_USERWRITABLE = 12699
    UA_NS0ID_CLOSEANDUPDATEMETHODTYPE_INPUTARGUMENTS = 12704
    UA_NS0ID_TRUSTLISTTYPE_CLOSEANDUPDATE_INPUTARGUMENTS = 12705
    UA_NS0ID_SERVERCONFIGURATIONTYPE_SERVERCAPABILITIES = 12708
    UA_NS0ID_SERVERCONFIGURATION_SERVERCAPABILITIES = 12710
    UA_NS0ID_OPCUA_XMLSCHEMA_RELATIVEPATHELEMENT = 12712
    UA_NS0ID_OPCUA_XMLSCHEMA_RELATIVEPATHELEMENT_DATATYPEVERSION = 12713
    UA_NS0ID_OPCUA_XMLSCHEMA_RELATIVEPATHELEMENT_DICTIONARYFRAGMENT = 12714
    UA_NS0ID_OPCUA_XMLSCHEMA_RELATIVEPATH = 12715
    UA_NS0ID_OPCUA_XMLSCHEMA_RELATIVEPATH_DATATYPEVERSION = 12716
    UA_NS0ID_OPCUA_XMLSCHEMA_RELATIVEPATH_DICTIONARYFRAGMENT = 12717
    UA_NS0ID_OPCUA_BINARYSCHEMA_RELATIVEPATHELEMENT = 12718
    UA_NS0ID_OPCUA_BINARYSCHEMA_RELATIVEPATHELEMENT_DATATYPEVERSION = 12719
    UA_NS0ID_OPCUA_BINARYSCHEMA_RELATIVEPATHELEMENT_DICTIONARYFRAGMENT = 12720
    UA_NS0ID_OPCUA_BINARYSCHEMA_RELATIVEPATH = 12721
    UA_NS0ID_OPCUA_BINARYSCHEMA_RELATIVEPATH_DATATYPEVERSION = 12722
    UA_NS0ID_OPCUA_BINARYSCHEMA_RELATIVEPATH_DICTIONARYFRAGMENT = 12723
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CREATESIGNINGREQUEST = 12731
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CREATESIGNINGREQUEST_INPUTARGUMENTS = 12732
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CREATESIGNINGREQUEST_OUTPUTARGUMENTS = 12733
    UA_NS0ID_SERVERCONFIGURATIONTYPE_APPLYCHANGES = 12734
    UA_NS0ID_SERVERCONFIGURATION_CREATESIGNINGREQUEST = 12737
    UA_NS0ID_SERVERCONFIGURATION_CREATESIGNINGREQUEST_INPUTARGUMENTS = 12738
    UA_NS0ID_SERVERCONFIGURATION_CREATESIGNINGREQUEST_OUTPUTARGUMENTS = 12739
    UA_NS0ID_SERVERCONFIGURATION_APPLYCHANGES = 12740
    UA_NS0ID_CREATESIGNINGREQUESTMETHODTYPE = 12741
    UA_NS0ID_CREATESIGNINGREQUESTMETHODTYPE_INPUTARGUMENTS = 12742
    UA_NS0ID_CREATESIGNINGREQUESTMETHODTYPE_OUTPUTARGUMENTS = 12743
    UA_NS0ID_OPTIONSETVALUES = 12745
    UA_NS0ID_SERVERTYPE_SETSUBSCRIPTIONDURABLE = 12746
    UA_NS0ID_SERVERTYPE_SETSUBSCRIPTIONDURABLE_INPUTARGUMENTS = 12747
    UA_NS0ID_SERVERTYPE_SETSUBSCRIPTIONDURABLE_OUTPUTARGUMENTS = 12748
    UA_NS0ID_SERVER_SETSUBSCRIPTIONDURABLE = 12749
    UA_NS0ID_SERVER_SETSUBSCRIPTIONDURABLE_INPUTARGUMENTS = 12750
    UA_NS0ID_SERVER_SETSUBSCRIPTIONDURABLE_OUTPUTARGUMENTS = 12751
    UA_NS0ID_SETSUBSCRIPTIONDURABLEMETHODTYPE = 12752
    UA_NS0ID_SETSUBSCRIPTIONDURABLEMETHODTYPE_INPUTARGUMENTS = 12753
    UA_NS0ID_SETSUBSCRIPTIONDURABLEMETHODTYPE_OUTPUTARGUMENTS = 12754
    UA_NS0ID_OPTIONSET = 12755
    UA_NS0ID_UNION = 12756
    UA_NS0ID_OPTIONSET_ENCODING_DEFAULTXML = 12757
    UA_NS0ID_UNION_ENCODING_DEFAULTXML = 12758
    UA_NS0ID_OPCUA_XMLSCHEMA_OPTIONSET = 12759
    UA_NS0ID_OPCUA_XMLSCHEMA_OPTIONSET_DATATYPEVERSION = 12760
    UA_NS0ID_OPCUA_XMLSCHEMA_OPTIONSET_DICTIONARYFRAGMENT = 12761
    UA_NS0ID_OPCUA_XMLSCHEMA_UNION = 12762
    UA_NS0ID_OPCUA_XMLSCHEMA_UNION_DATATYPEVERSION = 12763
    UA_NS0ID_OPCUA_XMLSCHEMA_UNION_DICTIONARYFRAGMENT = 12764
    UA_NS0ID_OPTIONSET_ENCODING_DEFAULTBINARY = 12765
    UA_NS0ID_UNION_ENCODING_DEFAULTBINARY = 12766
    UA_NS0ID_OPCUA_BINARYSCHEMA_OPTIONSET = 12767
    UA_NS0ID_OPCUA_BINARYSCHEMA_OPTIONSET_DATATYPEVERSION = 12768
    UA_NS0ID_OPCUA_BINARYSCHEMA_OPTIONSET_DICTIONARYFRAGMENT = 12769
    UA_NS0ID_OPCUA_BINARYSCHEMA_UNION = 12770
    UA_NS0ID_OPCUA_BINARYSCHEMA_UNION_DATATYPEVERSION = 12771
    UA_NS0ID_OPCUA_BINARYSCHEMA_UNION_DICTIONARYFRAGMENT = 12772
    UA_NS0ID_GETREJECTEDLISTMETHODTYPE = 12773
    UA_NS0ID_GETREJECTEDLISTMETHODTYPE_OUTPUTARGUMENTS = 12774
    UA_NS0ID_SERVERCONFIGURATIONTYPE_GETREJECTEDLIST = 12775
    UA_NS0ID_SERVERCONFIGURATIONTYPE_GETREJECTEDLIST_OUTPUTARGUMENTS = 12776
    UA_NS0ID_SERVERCONFIGURATION_GETREJECTEDLIST = 12777
    UA_NS0ID_SERVERCONFIGURATION_GETREJECTEDLIST_OUTPUTARGUMENTS = 12778
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSARRAYTYPE_SAMPLINGINTERVALDIAGNOSTICS = 12779
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSARRAYTYPE_SAMPLINGINTERVALDIAGNOSTICS_SAMPLINGINTERVAL = 12780
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSARRAYTYPE_SAMPLINGINTERVALDIAGNOSTICS_SAMPLEDMONITOREDITEMSCOUNT = 12781
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSARRAYTYPE_SAMPLINGINTERVALDIAGNOSTICS_MAXSAMPLEDMONITOREDITEMSCOUNT = 12782
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSARRAYTYPE_SAMPLINGINTERVALDIAGNOSTICS_DISABLEDMONITOREDITEMSSAMPLINGCOUNT = 12783
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS = 12784
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_SESSIONID = 12785
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_SUBSCRIPTIONID = 12786
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_PRIORITY = 12787
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_PUBLISHINGINTERVAL = 12788
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_MAXKEEPALIVECOUNT = 12789
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_MAXLIFETIMECOUNT = 12790
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_MAXNOTIFICATIONSPERPUBLISH = 12791
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_PUBLISHINGENABLED = 12792
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_MODIFYCOUNT = 12793
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_ENABLECOUNT = 12794
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_DISABLECOUNT = 12795
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_REPUBLISHREQUESTCOUNT = 12796
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_REPUBLISHMESSAGEREQUESTCOUNT = 12797
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_REPUBLISHMESSAGECOUNT = 12798
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_TRANSFERREQUESTCOUNT = 12799
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_TRANSFERREDTOALTCLIENTCOUNT = 12800
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_TRANSFERREDTOSAMECLIENTCOUNT = 12801
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_PUBLISHREQUESTCOUNT = 12802
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_DATACHANGENOTIFICATIONSCOUNT = 12803
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_EVENTNOTIFICATIONSCOUNT = 12804
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_NOTIFICATIONSCOUNT = 12805
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_LATEPUBLISHREQUESTCOUNT = 12806
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_CURRENTKEEPALIVECOUNT = 12807
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_CURRENTLIFETIMECOUNT = 12808
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_UNACKNOWLEDGEDMESSAGECOUNT = 12809
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_DISCARDEDMESSAGECOUNT = 12810
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_MONITOREDITEMCOUNT = 12811
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_DISABLEDMONITOREDITEMCOUNT = 12812
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_MONITORINGQUEUEOVERFLOWCOUNT = 12813
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_NEXTSEQUENCENUMBER = 12814
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSARRAYTYPE_SUBSCRIPTIONDIAGNOSTICS_EVENTQUEUEOVERFLOWCOUNT = 12815
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS = 12816
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_SESSIONID = 12817
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_SESSIONNAME = 12818
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_CLIENTDESCRIPTION = 12819
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_SERVERURI = 12820
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_ENDPOINTURL = 12821
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_LOCALEIDS = 12822
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_ACTUALSESSIONTIMEOUT = 12823
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_MAXRESPONSEMESSAGESIZE = 12824
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_CLIENTCONNECTIONTIME = 12825
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_CLIENTLASTCONTACTTIME = 12826
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_CURRENTSUBSCRIPTIONSCOUNT = 12827
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_CURRENTMONITOREDITEMSCOUNT = 12828
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_CURRENTPUBLISHREQUESTSINQUEUE = 12829
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_TOTALREQUESTCOUNT = 12830
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_UNAUTHORIZEDREQUESTCOUNT = 12831
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_READCOUNT = 12832
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_HISTORYREADCOUNT = 12833
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_WRITECOUNT = 12834
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_HISTORYUPDATECOUNT = 12835
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_CALLCOUNT = 12836
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_CREATEMONITOREDITEMSCOUNT = 12837
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_MODIFYMONITOREDITEMSCOUNT = 12838
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_SETMONITORINGMODECOUNT = 12839
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_SETTRIGGERINGCOUNT = 12840
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_DELETEMONITOREDITEMSCOUNT = 12841
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_CREATESUBSCRIPTIONCOUNT = 12842
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_MODIFYSUBSCRIPTIONCOUNT = 12843
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_SETPUBLISHINGMODECOUNT = 12844
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_PUBLISHCOUNT = 12845
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_REPUBLISHCOUNT = 12846
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_TRANSFERSUBSCRIPTIONSCOUNT = 12847
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_DELETESUBSCRIPTIONSCOUNT = 12848
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_ADDNODESCOUNT = 12849
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_ADDREFERENCESCOUNT = 12850
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_DELETENODESCOUNT = 12851
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_DELETEREFERENCESCOUNT = 12852
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_BROWSECOUNT = 12853
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_BROWSENEXTCOUNT = 12854
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_TRANSLATEBROWSEPATHSTONODEIDSCOUNT = 12855
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_QUERYFIRSTCOUNT = 12856
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_QUERYNEXTCOUNT = 12857
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_REGISTERNODESCOUNT = 12858
    UA_NS0ID_SESSIONDIAGNOSTICSARRAYTYPE_SESSIONDIAGNOSTICS_UNREGISTERNODESCOUNT = 12859
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS = 12860
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS_SESSIONID = 12861
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS_CLIENTUSERIDOFSESSION = 12862
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS_CLIENTUSERIDHISTORY = 12863
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS_AUTHENTICATIONMECHANISM = 12864
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS_ENCODING = 12865
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS_TRANSPORTPROTOCOL = 12866
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS_SECURITYMODE = 12867
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS_SECURITYPOLICYURI = 12868
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSARRAYTYPE_SESSIONSECURITYDIAGNOSTICS_CLIENTCERTIFICATE = 12869
    UA_NS0ID_SERVERTYPE_RESENDDATA = 12871
    UA_NS0ID_SERVERTYPE_RESENDDATA_INPUTARGUMENTS = 12872
    UA_NS0ID_SERVER_RESENDDATA = 12873
    UA_NS0ID_SERVER_RESENDDATA_INPUTARGUMENTS = 12874
    UA_NS0ID_RESENDDATAMETHODTYPE = 12875
    UA_NS0ID_RESENDDATAMETHODTYPE_INPUTARGUMENTS = 12876
    UA_NS0ID_NORMALIZEDSTRING = 12877
    UA_NS0ID_DECIMALSTRING = 12878
    UA_NS0ID_DURATIONSTRING = 12879
    UA_NS0ID_TIMESTRING = 12880
    UA_NS0ID_DATESTRING = 12881
    UA_NS0ID_SERVERTYPE_ESTIMATEDRETURNTIME = 12882
    UA_NS0ID_SERVERTYPE_REQUESTSERVERSTATECHANGE = 12883
    UA_NS0ID_SERVERTYPE_REQUESTSERVERSTATECHANGE_INPUTARGUMENTS = 12884
    UA_NS0ID_SERVER_ESTIMATEDRETURNTIME = 12885
    UA_NS0ID_SERVER_REQUESTSERVERSTATECHANGE = 12886
    UA_NS0ID_SERVER_REQUESTSERVERSTATECHANGE_INPUTARGUMENTS = 12887
    UA_NS0ID_REQUESTSERVERSTATECHANGEMETHODTYPE = 12888
    UA_NS0ID_REQUESTSERVERSTATECHANGEMETHODTYPE_INPUTARGUMENTS = 12889
    UA_NS0ID_DISCOVERYCONFIGURATION = 12890
    UA_NS0ID_MDNSDISCOVERYCONFIGURATION = 12891
    UA_NS0ID_DISCOVERYCONFIGURATION_ENCODING_DEFAULTXML = 12892
    UA_NS0ID_MDNSDISCOVERYCONFIGURATION_ENCODING_DEFAULTXML = 12893
    UA_NS0ID_OPCUA_XMLSCHEMA_DISCOVERYCONFIGURATION = 12894
    UA_NS0ID_OPCUA_XMLSCHEMA_DISCOVERYCONFIGURATION_DATATYPEVERSION = 12895
    UA_NS0ID_OPCUA_XMLSCHEMA_DISCOVERYCONFIGURATION_DICTIONARYFRAGMENT = 12896
    UA_NS0ID_OPCUA_XMLSCHEMA_MDNSDISCOVERYCONFIGURATION = 12897
    UA_NS0ID_OPCUA_XMLSCHEMA_MDNSDISCOVERYCONFIGURATION_DATATYPEVERSION = 12898
    UA_NS0ID_OPCUA_XMLSCHEMA_MDNSDISCOVERYCONFIGURATION_DICTIONARYFRAGMENT = 12899
    UA_NS0ID_DISCOVERYCONFIGURATION_ENCODING_DEFAULTBINARY = 12900
    UA_NS0ID_MDNSDISCOVERYCONFIGURATION_ENCODING_DEFAULTBINARY = 12901
    UA_NS0ID_OPCUA_BINARYSCHEMA_DISCOVERYCONFIGURATION = 12902
    UA_NS0ID_OPCUA_BINARYSCHEMA_DISCOVERYCONFIGURATION_DATATYPEVERSION = 12903
    UA_NS0ID_OPCUA_BINARYSCHEMA_DISCOVERYCONFIGURATION_DICTIONARYFRAGMENT = 12904
    UA_NS0ID_OPCUA_BINARYSCHEMA_MDNSDISCOVERYCONFIGURATION = 12905
    UA_NS0ID_OPCUA_BINARYSCHEMA_MDNSDISCOVERYCONFIGURATION_DATATYPEVERSION = 12906
    UA_NS0ID_OPCUA_BINARYSCHEMA_MDNSDISCOVERYCONFIGURATION_DICTIONARYFRAGMENT = 12907
    UA_NS0ID_MAXBYTESTRINGLENGTH = 12908
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_MAXBYTESTRINGLENGTH = 12909
    UA_NS0ID_SERVERCAPABILITIESTYPE_MAXBYTESTRINGLENGTH = 12910
    UA_NS0ID_SERVER_SERVERCAPABILITIES_MAXBYTESTRINGLENGTH = 12911
    UA_NS0ID_CONDITIONTYPE_CONDITIONREFRESH2 = 12912
    UA_NS0ID_CONDITIONTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12913
    UA_NS0ID_CONDITIONREFRESH2METHODTYPE = 12914
    UA_NS0ID_CONDITIONREFRESH2METHODTYPE_INPUTARGUMENTS = 12915
    UA_NS0ID_DIALOGCONDITIONTYPE_CONDITIONREFRESH2 = 12916
    UA_NS0ID_DIALOGCONDITIONTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12917
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONDITIONREFRESH2 = 12918
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12919
    UA_NS0ID_ALARMCONDITIONTYPE_CONDITIONREFRESH2 = 12984
    UA_NS0ID_ALARMCONDITIONTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12985
    UA_NS0ID_LIMITALARMTYPE_CONDITIONREFRESH2 = 12986
    UA_NS0ID_LIMITALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12987
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONDITIONREFRESH2 = 12988
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12989
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONDITIONREFRESH2 = 12990
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12991
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONDITIONREFRESH2 = 12992
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12993
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONDITIONREFRESH2 = 12994
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12995
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONDITIONREFRESH2 = 12996
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12997
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONDITIONREFRESH2 = 12998
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 12999
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONREFRESH2 = 13000
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 13001
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONREFRESH2 = 13002
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 13003
    UA_NS0ID_DISCRETEALARMTYPE_CONDITIONREFRESH2 = 13004
    UA_NS0ID_DISCRETEALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 13005
    UA_NS0ID_OFFNORMALALARMTYPE_CONDITIONREFRESH2 = 13006
    UA_NS0ID_OFFNORMALALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 13007
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONDITIONREFRESH2 = 13008
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 13009
    UA_NS0ID_TRIPALARMTYPE_CONDITIONREFRESH2 = 13010
    UA_NS0ID_TRIPALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 13011
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE = 13225
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_EVENTID = 13226
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_EVENTTYPE = 13227
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SOURCENODE = 13228
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SOURCENAME = 13229
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_TIME = 13230
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_RECEIVETIME = 13231
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LOCALTIME = 13232
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_MESSAGE = 13233
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SEVERITY = 13234
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONDITIONCLASSID = 13235
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONDITIONCLASSNAME = 13236
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONDITIONNAME = 13237
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_BRANCHID = 13238
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_RETAIN = 13239
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLEDSTATE = 13240
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLEDSTATE_ID = 13241
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLEDSTATE_NAME = 13242
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLEDSTATE_NUMBER = 13243
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 13244
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 13245
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 13246
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLEDSTATE_TRUESTATE = 13247
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLEDSTATE_FALSESTATE = 13248
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_QUALITY = 13249
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_QUALITY_SOURCETIMESTAMP = 13250
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LASTSEVERITY = 13251
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 13252
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_COMMENT = 13253
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_COMMENT_SOURCETIMESTAMP = 13254
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CLIENTUSERID = 13255
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_DISABLE = 13256
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ENABLE = 13257
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ADDCOMMENT = 13258
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 13259
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONDITIONREFRESH = 13260
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 13261
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONDITIONREFRESH2 = 13262
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 13263
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKEDSTATE = 13264
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKEDSTATE_ID = 13265
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKEDSTATE_NAME = 13266
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKEDSTATE_NUMBER = 13267
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 13268
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 13269
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 13270
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKEDSTATE_TRUESTATE = 13271
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKEDSTATE_FALSESTATE = 13272
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRMEDSTATE = 13273
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRMEDSTATE_ID = 13274
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRMEDSTATE_NAME = 13275
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRMEDSTATE_NUMBER = 13276
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 13277
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 13278
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 13279
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 13280
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 13281
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKNOWLEDGE = 13282
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 13283
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRM = 13284
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONFIRM_INPUTARGUMENTS = 13285
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACTIVESTATE = 13286
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACTIVESTATE_ID = 13287
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACTIVESTATE_NAME = 13288
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACTIVESTATE_NUMBER = 13289
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 13290
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 13291
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 13292
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACTIVESTATE_TRUESTATE = 13293
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ACTIVESTATE_FALSESTATE = 13294
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_INPUTNODE = 13295
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDSTATE = 13296
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDSTATE_ID = 13297
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDSTATE_NAME = 13298
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDSTATE_NUMBER = 13299
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 13300
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 13301
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 13302
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 13303
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 13304
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE = 13305
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 13306
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 13307
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 13308
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 13309
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 13310
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 13311
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 13312
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 13313
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 13314
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 13315
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 13316
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 13317
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_UNSHELVE = 13318
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 13319
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 13320
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 13321
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESSEDORSHELVED = 13322
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_MAXTIMESHELVED = 13323
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_NORMALSTATE = 13324
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_EXPIRATIONDATE = 13325
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CERTIFICATETYPE = 13326
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CERTIFICATE = 13327
    UA_NS0ID_FILETYPE_MIMETYPE = 13341
    UA_NS0ID_CREATEDIRECTORYMETHODTYPE = 13342
    UA_NS0ID_CREATEDIRECTORYMETHODTYPE_INPUTARGUMENTS = 13343
    UA_NS0ID_CREATEDIRECTORYMETHODTYPE_OUTPUTARGUMENTS = 13344
    UA_NS0ID_CREATEFILEMETHODTYPE = 13345
    UA_NS0ID_CREATEFILEMETHODTYPE_INPUTARGUMENTS = 13346
    UA_NS0ID_CREATEFILEMETHODTYPE_OUTPUTARGUMENTS = 13347
    UA_NS0ID_DELETEFILEMETHODTYPE = 13348
    UA_NS0ID_DELETEFILEMETHODTYPE_INPUTARGUMENTS = 13349
    UA_NS0ID_MOVEORCOPYMETHODTYPE = 13350
    UA_NS0ID_MOVEORCOPYMETHODTYPE_INPUTARGUMENTS = 13351
    UA_NS0ID_MOVEORCOPYMETHODTYPE_OUTPUTARGUMENTS = 13352
    UA_NS0ID_FILEDIRECTORYTYPE = 13353
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER = 13354
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_CREATEDIRECTORY = 13355
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_CREATEDIRECTORY_INPUTARGUMENTS = 13356
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_CREATEDIRECTORY_OUTPUTARGUMENTS = 13357
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_CREATEFILE = 13358
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_CREATEFILE_INPUTARGUMENTS = 13359
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_CREATEFILE_OUTPUTARGUMENTS = 13360
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_MOVEORCOPY = 13363
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_MOVEORCOPY_INPUTARGUMENTS = 13364
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_MOVEORCOPY_OUTPUTARGUMENTS = 13365
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER = 13366
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_SIZE = 13367
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_WRITABLE = 13368
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_USERWRITABLE = 13369
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_OPENCOUNT = 13370
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_MIMETYPE = 13371
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_OPEN = 13372
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_OPEN_INPUTARGUMENTS = 13373
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_OPEN_OUTPUTARGUMENTS = 13374
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_CLOSE = 13375
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_CLOSE_INPUTARGUMENTS = 13376
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_READ = 13377
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_READ_INPUTARGUMENTS = 13378
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_READ_OUTPUTARGUMENTS = 13379
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_WRITE = 13380
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_WRITE_INPUTARGUMENTS = 13381
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_GETPOSITION = 13382
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_GETPOSITION_INPUTARGUMENTS = 13383
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_GETPOSITION_OUTPUTARGUMENTS = 13384
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_SETPOSITION = 13385
    UA_NS0ID_FILEDIRECTORYTYPE_FILENAME_PLACEHOLDER_SETPOSITION_INPUTARGUMENTS = 13386
    UA_NS0ID_FILEDIRECTORYTYPE_CREATEDIRECTORY = 13387
    UA_NS0ID_FILEDIRECTORYTYPE_CREATEDIRECTORY_INPUTARGUMENTS = 13388
    UA_NS0ID_FILEDIRECTORYTYPE_CREATEDIRECTORY_OUTPUTARGUMENTS = 13389
    UA_NS0ID_FILEDIRECTORYTYPE_CREATEFILE = 13390
    UA_NS0ID_FILEDIRECTORYTYPE_CREATEFILE_INPUTARGUMENTS = 13391
    UA_NS0ID_FILEDIRECTORYTYPE_CREATEFILE_OUTPUTARGUMENTS = 13392
    UA_NS0ID_FILEDIRECTORYTYPE_DELETEFILESYSTEMOBJECT = 13393
    UA_NS0ID_FILEDIRECTORYTYPE_DELETEFILESYSTEMOBJECT_INPUTARGUMENTS = 13394
    UA_NS0ID_FILEDIRECTORYTYPE_MOVEORCOPY = 13395
    UA_NS0ID_FILEDIRECTORYTYPE_MOVEORCOPY_INPUTARGUMENTS = 13396
    UA_NS0ID_FILEDIRECTORYTYPE_MOVEORCOPY_OUTPUTARGUMENTS = 13397
    UA_NS0ID_ADDRESSSPACEFILETYPE_MIMETYPE = 13398
    UA_NS0ID_NAMESPACEMETADATATYPE_NAMESPACEFILE_MIMETYPE = 13399
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_NAMESPACEFILE_MIMETYPE = 13400
    UA_NS0ID_TRUSTLISTTYPE_MIMETYPE = 13403
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST = 13599
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_SIZE = 13600
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_WRITABLE = 13601
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_USERWRITABLE = 13602
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_OPENCOUNT = 13603
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_MIMETYPE = 13604
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_OPEN = 13605
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_OPEN_INPUTARGUMENTS = 13606
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 13607
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_CLOSE = 13608
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_CLOSE_INPUTARGUMENTS = 13609
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_READ = 13610
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_READ_INPUTARGUMENTS = 13611
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_READ_OUTPUTARGUMENTS = 13612
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_WRITE = 13613
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_WRITE_INPUTARGUMENTS = 13614
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_GETPOSITION = 13615
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 13616
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 13617
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_SETPOSITION = 13618
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 13619
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_LASTUPDATETIME = 13620
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_OPENWITHMASKS = 13621
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 13622
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 13623
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_CLOSEANDUPDATE = 13624
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 13625
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 13626
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_ADDCERTIFICATE = 13627
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 13628
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_REMOVECERTIFICATE = 13629
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 13630
    UA_NS0ID_CERTIFICATEGROUPTYPE_CERTIFICATETYPES = 13631
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_CERTIFICATEGROUP = 13735
    UA_NS0ID_CERTIFICATEUPDATEDAUDITEVENTTYPE_CERTIFICATETYPE = 13736
    UA_NS0ID_SERVERCONFIGURATION_UPDATECERTIFICATE = 13737
    UA_NS0ID_SERVERCONFIGURATION_UPDATECERTIFICATE_INPUTARGUMENTS = 13738
    UA_NS0ID_SERVERCONFIGURATION_UPDATECERTIFICATE_OUTPUTARGUMENTS = 13739
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE = 13813
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP = 13814
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST = 13815
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_SIZE = 13816
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_WRITABLE = 13817
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_USERWRITABLE = 13818
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENCOUNT = 13819
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_MIMETYPE = 13820
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPEN = 13821
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPEN_INPUTARGUMENTS = 13822
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 13823
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSE = 13824
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSE_INPUTARGUMENTS = 13825
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_READ = 13826
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_READ_INPUTARGUMENTS = 13827
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_READ_OUTPUTARGUMENTS = 13828
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_WRITE = 13829
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_WRITE_INPUTARGUMENTS = 13830
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_GETPOSITION = 13831
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 13832
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 13833
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_SETPOSITION = 13834
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 13835
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_LASTUPDATETIME = 13836
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENWITHMASKS = 13837
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 13838
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 13839
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSEANDUPDATE = 13840
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 13841
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 13842
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_ADDCERTIFICATE = 13843
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 13844
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_REMOVECERTIFICATE = 13845
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 13846
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_CERTIFICATETYPES = 13847
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP = 13848
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST = 13849
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_SIZE = 13850
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_WRITABLE = 13851
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_USERWRITABLE = 13852
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_OPENCOUNT = 13853
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_MIMETYPE = 13854
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_OPEN = 13855
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_OPEN_INPUTARGUMENTS = 13856
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 13857
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSE = 13858
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSE_INPUTARGUMENTS = 13859
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_READ = 13860
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_READ_INPUTARGUMENTS = 13861
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_READ_OUTPUTARGUMENTS = 13862
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_WRITE = 13863
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_WRITE_INPUTARGUMENTS = 13864
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_GETPOSITION = 13865
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 13866
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 13867
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_SETPOSITION = 13868
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 13869
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_LASTUPDATETIME = 13870
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_OPENWITHMASKS = 13871
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 13872
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 13873
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSEANDUPDATE = 13874
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 13875
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 13876
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_ADDCERTIFICATE = 13877
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 13878
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_REMOVECERTIFICATE = 13879
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 13880
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_CERTIFICATETYPES = 13881
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP = 13882
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST = 13883
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_SIZE = 13884
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_WRITABLE = 13885
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_USERWRITABLE = 13886
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENCOUNT = 13887
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_MIMETYPE = 13888
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPEN = 13889
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPEN_INPUTARGUMENTS = 13890
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 13891
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSE = 13892
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSE_INPUTARGUMENTS = 13893
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_READ = 13894
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_READ_INPUTARGUMENTS = 13895
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_READ_OUTPUTARGUMENTS = 13896
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_WRITE = 13897
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_WRITE_INPUTARGUMENTS = 13898
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_GETPOSITION = 13899
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 13900
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 13901
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_SETPOSITION = 13902
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 13903
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_LASTUPDATETIME = 13904
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENWITHMASKS = 13905
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 13906
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 13907
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSEANDUPDATE = 13908
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 13909
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 13910
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_ADDCERTIFICATE = 13911
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 13912
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_REMOVECERTIFICATE = 13913
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 13914
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_CERTIFICATETYPES = 13915
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER = 13916
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST = 13917
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_SIZE = 13918
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_WRITABLE = 13919
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_USERWRITABLE = 13920
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_OPENCOUNT = 13921
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_MIMETYPE = 13922
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_OPEN = 13923
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_OPEN_INPUTARGUMENTS = 13924
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 13925
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_CLOSE = 13926
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_CLOSE_INPUTARGUMENTS = 13927
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_READ = 13928
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_READ_INPUTARGUMENTS = 13929
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_READ_OUTPUTARGUMENTS = 13930
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_WRITE = 13931
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_WRITE_INPUTARGUMENTS = 13932
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_GETPOSITION = 13933
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 13934
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 13935
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_SETPOSITION = 13936
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 13937
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_LASTUPDATETIME = 13938
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_OPENWITHMASKS = 13939
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 13940
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 13941
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_CLOSEANDUPDATE = 13942
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 13943
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 13944
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_ADDCERTIFICATE = 13945
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 13946
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_REMOVECERTIFICATE = 13947
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 13948
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_CERTIFICATETYPES = 13949
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS = 13950
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP = 13951
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST = 13952
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_SIZE = 13953
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_WRITABLE = 13954
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_USERWRITABLE = 13955
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENCOUNT = 13956
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_MIMETYPE = 13957
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPEN = 13958
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPEN_INPUTARGUMENTS = 13959
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 13960
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSE = 13961
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSE_INPUTARGUMENTS = 13962
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_READ = 13963
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_READ_INPUTARGUMENTS = 13964
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_READ_OUTPUTARGUMENTS = 13965
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_WRITE = 13966
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_WRITE_INPUTARGUMENTS = 13967
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_GETPOSITION = 13968
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 13969
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 13970
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_SETPOSITION = 13971
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 13972
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_LASTUPDATETIME = 13973
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENWITHMASKS = 13974
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 13975
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 13976
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSEANDUPDATE = 13977
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 13978
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 13979
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_ADDCERTIFICATE = 13980
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 13981
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_REMOVECERTIFICATE = 13982
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 13983
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_CERTIFICATETYPES = 13984
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP = 13985
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST = 13986
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_SIZE = 13987
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_WRITABLE = 13988
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_USERWRITABLE = 13989
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPENCOUNT = 13990
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_MIMETYPE = 13991
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPEN = 13992
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPEN_INPUTARGUMENTS = 13993
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 13994
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSE = 13995
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSE_INPUTARGUMENTS = 13996
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_READ = 13997
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_READ_INPUTARGUMENTS = 13998
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_READ_OUTPUTARGUMENTS = 13999
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_WRITE = 14000
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_WRITE_INPUTARGUMENTS = 14001
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_GETPOSITION = 14002
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 14003
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 14004
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_SETPOSITION = 14005
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 14006
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_LASTUPDATETIME = 14007
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPENWITHMASKS = 14008
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 14009
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 14010
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSEANDUPDATE = 14011
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 14012
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 14013
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_ADDCERTIFICATE = 14014
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 14015
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_REMOVECERTIFICATE = 14016
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 14017
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_CERTIFICATETYPES = 14018
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP = 14019
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST = 14020
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_SIZE = 14021
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_WRITABLE = 14022
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_USERWRITABLE = 14023
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENCOUNT = 14024
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_MIMETYPE = 14025
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPEN = 14026
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPEN_INPUTARGUMENTS = 14027
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 14028
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSE = 14029
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSE_INPUTARGUMENTS = 14030
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_READ = 14031
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_READ_INPUTARGUMENTS = 14032
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_READ_OUTPUTARGUMENTS = 14033
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_WRITE = 14034
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_WRITE_INPUTARGUMENTS = 14035
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_GETPOSITION = 14036
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 14037
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 14038
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_SETPOSITION = 14039
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 14040
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_LASTUPDATETIME = 14041
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENWITHMASKS = 14042
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 14043
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 14044
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSEANDUPDATE = 14045
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 14046
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 14047
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_ADDCERTIFICATE = 14048
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 14049
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_REMOVECERTIFICATE = 14050
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 14051
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_CERTIFICATETYPES = 14052
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS = 14053
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP = 14088
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST = 14089
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_SIZE = 14090
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_WRITABLE = 14091
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_USERWRITABLE = 14092
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPENCOUNT = 14093
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_MIMETYPE = 14094
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPEN = 14095
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPEN_INPUTARGUMENTS = 14096
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 14097
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSE = 14098
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSE_INPUTARGUMENTS = 14099
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_READ = 14100
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_READ_INPUTARGUMENTS = 14101
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_READ_OUTPUTARGUMENTS = 14102
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_WRITE = 14103
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_WRITE_INPUTARGUMENTS = 14104
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_GETPOSITION = 14105
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 14106
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 14107
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_SETPOSITION = 14108
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 14109
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_LASTUPDATETIME = 14110
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPENWITHMASKS = 14111
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 14112
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 14113
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSEANDUPDATE = 14114
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 14115
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 14116
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_ADDCERTIFICATE = 14117
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 14118
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_REMOVECERTIFICATE = 14119
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 14120
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_CERTIFICATETYPES = 14121
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP = 14122
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST = 14123
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_SIZE = 14124
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_WRITABLE = 14125
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_USERWRITABLE = 14126
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENCOUNT = 14127
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_MIMETYPE = 14128
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPEN = 14129
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPEN_INPUTARGUMENTS = 14130
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPEN_OUTPUTARGUMENTS = 14131
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSE = 14132
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSE_INPUTARGUMENTS = 14133
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_READ = 14134
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_READ_INPUTARGUMENTS = 14135
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_READ_OUTPUTARGUMENTS = 14136
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_WRITE = 14137
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_WRITE_INPUTARGUMENTS = 14138
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_GETPOSITION = 14139
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_GETPOSITION_INPUTARGUMENTS = 14140
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_GETPOSITION_OUTPUTARGUMENTS = 14141
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_SETPOSITION = 14142
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_SETPOSITION_INPUTARGUMENTS = 14143
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_LASTUPDATETIME = 14144
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENWITHMASKS = 14145
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENWITHMASKS_INPUTARGUMENTS = 14146
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_OPENWITHMASKS_OUTPUTARGUMENTS = 14147
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSEANDUPDATE = 14148
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 14149
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_CLOSEANDUPDATE_OUTPUTARGUMENTS = 14150
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_ADDCERTIFICATE = 14151
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_ADDCERTIFICATE_INPUTARGUMENTS = 14152
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_REMOVECERTIFICATE = 14153
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_REMOVECERTIFICATE_INPUTARGUMENTS = 14154
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_CERTIFICATETYPES = 14155
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP = 14156
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_WRITABLE = 14157
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_USERWRITABLE = 14158
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_MIMETYPE = 14159
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_CLOSEANDUPDATE_INPUTARGUMENTS = 14160
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_CERTIFICATETYPES = 14161
    UA_NS0ID_REMOVECONNECTIONMETHODTYPE = 14183
    UA_NS0ID_REMOVECONNECTIONMETHODTYPE_INPUTARGUMENTS = 14184
    UA_NS0ID_PUBSUBCONNECTIONTYPE = 14209
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDRESS = 14221
    UA_NS0ID_PUBSUBCONNECTIONTYPE_REMOVEGROUP = 14225
    UA_NS0ID_PUBSUBCONNECTIONTYPE_REMOVEGROUP_INPUTARGUMENTS = 14226
    UA_NS0ID_PUBSUBGROUPTYPE = 14232
    UA_NS0ID_PUBLISHEDVARIABLEDATATYPE = 14273
    UA_NS0ID_PUBLISHEDVARIABLEDATATYPE_ENCODING_DEFAULTXML = 14319
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDVARIABLEDATATYPE = 14320
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDVARIABLEDATATYPE_DATATYPEVERSION = 14321
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDVARIABLEDATATYPE_DICTIONARYFRAGMENT = 14322
    UA_NS0ID_PUBLISHEDVARIABLEDATATYPE_ENCODING_DEFAULTBINARY = 14323
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDVARIABLEDATATYPE = 14324
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDVARIABLEDATATYPE_DATATYPEVERSION = 14325
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDVARIABLEDATATYPE_DICTIONARYFRAGMENT = 14326
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_SESSIONID = 14413
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_SESSIONID = 14414
    UA_NS0ID_SERVER_SERVERREDUNDANCY_SERVERNETWORKGROUPS = 14415
    UA_NS0ID_PUBLISHSUBSCRIBETYPE = 14416
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER = 14417
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_PUBLISHERID = 14418
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_STATUS = 14419
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_STATUS_STATE = 14420
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_STATUS_ENABLE = 14421
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_STATUS_DISABLE = 14422
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDRESS = 14423
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_REMOVEGROUP = 14424
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_REMOVEGROUP_INPUTARGUMENTS = 14425
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_REMOVECONNECTION = 14432
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_REMOVECONNECTION_INPUTARGUMENTS = 14433
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS = 14434
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMS = 14435
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMS_INPUTARGUMENTS = 14436
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMS_OUTPUTARGUMENTS = 14437
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTS = 14438
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTS_INPUTARGUMENTS = 14439
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTS_OUTPUTARGUMENTS = 14440
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_REMOVEPUBLISHEDDATASET = 14441
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_REMOVEPUBLISHEDDATASET_INPUTARGUMENTS = 14442
    UA_NS0ID_PUBLISHSUBSCRIBE = 14443
    UA_NS0ID_HASPUBSUBCONNECTION = 14476
    UA_NS0ID_DATASETFOLDERTYPE = 14477
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER = 14478
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDDATAITEMS = 14479
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDDATAITEMS_INPUTARGUMENTS = 14480
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDDATAITEMS_OUTPUTARGUMENTS = 14481
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDEVENTS = 14482
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDEVENTS_INPUTARGUMENTS = 14483
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDEVENTS_OUTPUTARGUMENTS = 14484
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_REMOVEPUBLISHEDDATASET = 14485
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_REMOVEPUBLISHEDDATASET_INPUTARGUMENTS = 14486
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER = 14487
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER_CONFIGURATIONVERSION = 14489
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDDATAITEMS = 14493
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDDATAITEMS_INPUTARGUMENTS = 14494
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDDATAITEMS_OUTPUTARGUMENTS = 14495
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDEVENTS = 14496
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDEVENTS_INPUTARGUMENTS = 14497
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDEVENTS_OUTPUTARGUMENTS = 14498
    UA_NS0ID_DATASETFOLDERTYPE_REMOVEPUBLISHEDDATASET = 14499
    UA_NS0ID_DATASETFOLDERTYPE_REMOVEPUBLISHEDDATASET_INPUTARGUMENTS = 14500
    UA_NS0ID_ADDPUBLISHEDDATAITEMSMETHODTYPE = 14501
    UA_NS0ID_ADDPUBLISHEDDATAITEMSMETHODTYPE_INPUTARGUMENTS = 14502
    UA_NS0ID_ADDPUBLISHEDDATAITEMSMETHODTYPE_OUTPUTARGUMENTS = 14503
    UA_NS0ID_ADDPUBLISHEDEVENTSMETHODTYPE = 14504
    UA_NS0ID_ADDPUBLISHEDEVENTSMETHODTYPE_INPUTARGUMENTS = 14505
    UA_NS0ID_ADDPUBLISHEDEVENTSMETHODTYPE_OUTPUTARGUMENTS = 14506
    UA_NS0ID_REMOVEPUBLISHEDDATASETMETHODTYPE = 14507
    UA_NS0ID_REMOVEPUBLISHEDDATASETMETHODTYPE_INPUTARGUMENTS = 14508
    UA_NS0ID_PUBLISHEDDATASETTYPE = 14509
    UA_NS0ID_PUBLISHEDDATASETTYPE_CONFIGURATIONVERSION = 14519
    UA_NS0ID_DATASETMETADATATYPE = 14523
    UA_NS0ID_FIELDMETADATA = 14524
    UA_NS0ID_DATATYPEDESCRIPTION = 14525
    UA_NS0ID_STRUCTURETYPE_ENUMSTRINGS = 14528
    UA_NS0ID_KEYVALUEPAIR = 14533
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE = 14534
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_CONFIGURATIONVERSION = 14544
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_PUBLISHEDDATA = 14548
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_ADDVARIABLES = 14555
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_ADDVARIABLES_INPUTARGUMENTS = 14556
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_ADDVARIABLES_OUTPUTARGUMENTS = 14557
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_REMOVEVARIABLES = 14558
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_REMOVEVARIABLES_INPUTARGUMENTS = 14559
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_REMOVEVARIABLES_OUTPUTARGUMENTS = 14560
    UA_NS0ID_PUBLISHEDDATAITEMSADDVARIABLESMETHODTYPE = 14564
    UA_NS0ID_PUBLISHEDDATAITEMSADDVARIABLESMETHODTYPE_INPUTARGUMENTS = 14565
    UA_NS0ID_PUBLISHEDDATAITEMSADDVARIABLESMETHODTYPE_OUTPUTARGUMENTS = 14566
    UA_NS0ID_PUBLISHEDDATAITEMSREMOVEVARIABLESMETHODTYPE = 14567
    UA_NS0ID_PUBLISHEDDATAITEMSREMOVEVARIABLESMETHODTYPE_INPUTARGUMENTS = 14568
    UA_NS0ID_PUBLISHEDDATAITEMSREMOVEVARIABLESMETHODTYPE_OUTPUTARGUMENTS = 14569
    UA_NS0ID_PUBLISHEDEVENTSTYPE = 14572
    UA_NS0ID_PUBLISHEDEVENTSTYPE_CONFIGURATIONVERSION = 14582
    UA_NS0ID_PUBLISHEDEVENTSTYPE_PUBSUBEVENTNOTIFIER = 14586
    UA_NS0ID_PUBLISHEDEVENTSTYPE_SELECTEDFIELDS = 14587
    UA_NS0ID_PUBLISHEDEVENTSTYPE_FILTER = 14588
    UA_NS0ID_CONFIGURATIONVERSIONDATATYPE = 14593
    UA_NS0ID_PUBSUBCONNECTIONTYPE_PUBLISHERID = 14595
    UA_NS0ID_PUBSUBCONNECTIONTYPE_STATUS = 14600
    UA_NS0ID_PUBSUBCONNECTIONTYPE_STATUS_STATE = 14601
    UA_NS0ID_PUBSUBCONNECTIONTYPE_STATUS_ENABLE = 14602
    UA_NS0ID_PUBSUBCONNECTIONTYPE_STATUS_DISABLE = 14603
    UA_NS0ID_PUBSUBCONNECTIONTYPEREMOVEGROUPMETHODTYPE = 14604
    UA_NS0ID_PUBSUBCONNECTIONTYPEREMOVEGROUPMETHODTYPE_INPUTARGUMENTS = 14605
    UA_NS0ID_PUBSUBGROUPTYPEREMOVEWRITERMETHODTYPE = 14623
    UA_NS0ID_PUBSUBGROUPTYPEREMOVEWRITERMETHODTYPE_INPUTARGUMENTS = 14624
    UA_NS0ID_PUBSUBGROUPTYPEREMOVEREADERMETHODTYPE = 14625
    UA_NS0ID_PUBSUBGROUPTYPEREMOVEREADERMETHODTYPE_INPUTARGUMENTS = 14626
    UA_NS0ID_PUBSUBSTATUSTYPE = 14643
    UA_NS0ID_PUBSUBSTATUSTYPE_STATE = 14644
    UA_NS0ID_PUBSUBSTATUSTYPE_ENABLE = 14645
    UA_NS0ID_PUBSUBSTATUSTYPE_DISABLE = 14646
    UA_NS0ID_PUBSUBSTATE = 14647
    UA_NS0ID_PUBSUBSTATE_ENUMSTRINGS = 14648
    UA_NS0ID_FIELDTARGETDATATYPE = 14744
    UA_NS0ID_DATASETMETADATATYPE_ENCODING_DEFAULTXML = 14794
    UA_NS0ID_FIELDMETADATA_ENCODING_DEFAULTXML = 14795
    UA_NS0ID_DATATYPEDESCRIPTION_ENCODING_DEFAULTXML = 14796
    UA_NS0ID_DATATYPEDEFINITION_ENCODING_DEFAULTXML = 14797
    UA_NS0ID_STRUCTUREDEFINITION_ENCODING_DEFAULTXML = 14798
    UA_NS0ID_ENUMDEFINITION_ENCODING_DEFAULTXML = 14799
    UA_NS0ID_STRUCTUREFIELD_ENCODING_DEFAULTXML = 14800
    UA_NS0ID_ENUMFIELD_ENCODING_DEFAULTXML = 14801
    UA_NS0ID_KEYVALUEPAIR_ENCODING_DEFAULTXML = 14802
    UA_NS0ID_CONFIGURATIONVERSIONDATATYPE_ENCODING_DEFAULTXML = 14803
    UA_NS0ID_FIELDTARGETDATATYPE_ENCODING_DEFAULTXML = 14804
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETMETADATATYPE = 14805
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETMETADATATYPE_DATATYPEVERSION = 14806
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETMETADATATYPE_DICTIONARYFRAGMENT = 14807
    UA_NS0ID_OPCUA_XMLSCHEMA_FIELDMETADATA = 14808
    UA_NS0ID_OPCUA_XMLSCHEMA_FIELDMETADATA_DATATYPEVERSION = 14809
    UA_NS0ID_OPCUA_XMLSCHEMA_FIELDMETADATA_DICTIONARYFRAGMENT = 14810
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPEDESCRIPTION = 14811
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPEDESCRIPTION_DATATYPEVERSION = 14812
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPEDESCRIPTION_DICTIONARYFRAGMENT = 14813
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMFIELD = 14826
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMFIELD_DATATYPEVERSION = 14827
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMFIELD_DICTIONARYFRAGMENT = 14828
    UA_NS0ID_OPCUA_XMLSCHEMA_KEYVALUEPAIR = 14829
    UA_NS0ID_OPCUA_XMLSCHEMA_KEYVALUEPAIR_DATATYPEVERSION = 14830
    UA_NS0ID_OPCUA_XMLSCHEMA_KEYVALUEPAIR_DICTIONARYFRAGMENT = 14831
    UA_NS0ID_OPCUA_XMLSCHEMA_CONFIGURATIONVERSIONDATATYPE = 14832
    UA_NS0ID_OPCUA_XMLSCHEMA_CONFIGURATIONVERSIONDATATYPE_DATATYPEVERSION = 14833
    UA_NS0ID_OPCUA_XMLSCHEMA_CONFIGURATIONVERSIONDATATYPE_DICTIONARYFRAGMENT = 14834
    UA_NS0ID_OPCUA_XMLSCHEMA_FIELDTARGETDATATYPE = 14835
    UA_NS0ID_OPCUA_XMLSCHEMA_FIELDTARGETDATATYPE_DATATYPEVERSION = 14836
    UA_NS0ID_OPCUA_XMLSCHEMA_FIELDTARGETDATATYPE_DICTIONARYFRAGMENT = 14837
    UA_NS0ID_FIELDMETADATA_ENCODING_DEFAULTBINARY = 14839
    UA_NS0ID_STRUCTUREFIELD_ENCODING_DEFAULTBINARY = 14844
    UA_NS0ID_ENUMFIELD_ENCODING_DEFAULTBINARY = 14845
    UA_NS0ID_KEYVALUEPAIR_ENCODING_DEFAULTBINARY = 14846
    UA_NS0ID_CONFIGURATIONVERSIONDATATYPE_ENCODING_DEFAULTBINARY = 14847
    UA_NS0ID_FIELDTARGETDATATYPE_ENCODING_DEFAULTBINARY = 14848
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETMETADATATYPE = 14849
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETMETADATATYPE_DATATYPEVERSION = 14850
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETMETADATATYPE_DICTIONARYFRAGMENT = 14851
    UA_NS0ID_OPCUA_BINARYSCHEMA_FIELDMETADATA = 14852
    UA_NS0ID_OPCUA_BINARYSCHEMA_FIELDMETADATA_DATATYPEVERSION = 14853
    UA_NS0ID_OPCUA_BINARYSCHEMA_FIELDMETADATA_DICTIONARYFRAGMENT = 14854
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPEDESCRIPTION = 14855
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPEDESCRIPTION_DATATYPEVERSION = 14856
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPEDESCRIPTION_DICTIONARYFRAGMENT = 14857
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMFIELD = 14870
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMFIELD_DATATYPEVERSION = 14871
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMFIELD_DICTIONARYFRAGMENT = 14872
    UA_NS0ID_OPCUA_BINARYSCHEMA_KEYVALUEPAIR = 14873
    UA_NS0ID_OPCUA_BINARYSCHEMA_KEYVALUEPAIR_DATATYPEVERSION = 14874
    UA_NS0ID_OPCUA_BINARYSCHEMA_KEYVALUEPAIR_DICTIONARYFRAGMENT = 14875
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONFIGURATIONVERSIONDATATYPE = 14876
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONFIGURATIONVERSIONDATATYPE_DATATYPEVERSION = 14877
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONFIGURATIONVERSIONDATATYPE_DICTIONARYFRAGMENT = 14878
    UA_NS0ID_OPCUA_BINARYSCHEMA_FIELDTARGETDATATYPE_DATATYPEVERSION = 14880
    UA_NS0ID_OPCUA_BINARYSCHEMA_FIELDTARGETDATATYPE_DICTIONARYFRAGMENT = 14881
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_EXPIRATIONLIMIT = 14900
    UA_NS0ID_DATASETTOWRITER = 14936
    UA_NS0ID_DATATYPEDICTIONARYTYPE_DEPRECATED = 15001
    UA_NS0ID_MAXCHARACTERS = 15002
    UA_NS0ID_SERVERTYPE_URISVERSION = 15003
    UA_NS0ID_SERVER_URISVERSION = 15004
    UA_NS0ID_SIMPLETYPEDESCRIPTION = 15005
    UA_NS0ID_UABINARYFILEDATATYPE = 15006
    UA_NS0ID_BROKERCONNECTIONTRANSPORTDATATYPE = 15007
    UA_NS0ID_BROKERTRANSPORTQUALITYOFSERVICE = 15008
    UA_NS0ID_BROKERTRANSPORTQUALITYOFSERVICE_ENUMSTRINGS = 15009
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPNAME_PLACEHOLDER_KEYLIFETIME = 15010
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPNAME_PLACEHOLDER_SECURITYPOLICYURI = 15011
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPNAME_PLACEHOLDER_MAXFUTUREKEYCOUNT = 15012
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE = 15013
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_EVENTID = 15014
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_EVENTTYPE = 15015
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_SOURCENODE = 15016
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_SOURCENAME = 15017
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_TIME = 15018
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_RECEIVETIME = 15019
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_LOCALTIME = 15020
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_MESSAGE = 15021
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_SEVERITY = 15022
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_ACTIONTIMESTAMP = 15023
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_STATUS = 15024
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_SERVERID = 15025
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_CLIENTAUDITENTRYID = 15026
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_CLIENTUSERID = 15027
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_METHODID = 15028
    UA_NS0ID_AUDITCONDITIONRESETEVENTTYPE_INPUTARGUMENTS = 15029
    UA_NS0ID_PERMISSIONTYPE_OPTIONSETVALUES = 15030
    UA_NS0ID_ACCESSLEVELTYPE = 15031
    UA_NS0ID_ACCESSLEVELTYPE_OPTIONSETVALUES = 15032
    UA_NS0ID_EVENTNOTIFIERTYPE = 15033
    UA_NS0ID_EVENTNOTIFIERTYPE_OPTIONSETVALUES = 15034
    UA_NS0ID_ACCESSRESTRICTIONTYPE_OPTIONSETVALUES = 15035
    UA_NS0ID_ATTRIBUTEWRITEMASK_OPTIONSETVALUES = 15036
    UA_NS0ID_OPCUA_BINARYSCHEMA_DEPRECATED = 15037
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_LASTMETHODINPUTVALUES = 15038
    UA_NS0ID_OPCUA_XMLSCHEMA_DEPRECATED = 15039
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_PROGRAMDIAGNOSTIC_LASTMETHODOUTPUTVALUES = 15040
    UA_NS0ID_KEYVALUEPAIR_ENCODING_DEFAULTJSON = 15041
    UA_NS0ID_IDENTITYMAPPINGRULETYPE_ENCODING_DEFAULTJSON = 15042
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPNAME_PLACEHOLDER_MAXPASTKEYCOUNT = 15043
    UA_NS0ID_TRUSTLISTDATATYPE_ENCODING_DEFAULTJSON = 15044
    UA_NS0ID_DECIMALDATATYPE_ENCODING_DEFAULTJSON = 15045
    UA_NS0ID_SECURITYGROUPTYPE_KEYLIFETIME = 15046
    UA_NS0ID_SECURITYGROUPTYPE_SECURITYPOLICYURI = 15047
    UA_NS0ID_SECURITYGROUPTYPE_MAXFUTUREKEYCOUNT = 15048
    UA_NS0ID_CONFIGURATIONVERSIONDATATYPE_ENCODING_DEFAULTJSON = 15049
    UA_NS0ID_DATASETMETADATATYPE_ENCODING_DEFAULTJSON = 15050
    UA_NS0ID_FIELDMETADATA_ENCODING_DEFAULTJSON = 15051
    UA_NS0ID_PUBLISHEDEVENTSTYPE_MODIFYFIELDSELECTION = 15052
    UA_NS0ID_PUBLISHEDEVENTSTYPE_MODIFYFIELDSELECTION_INPUTARGUMENTS = 15053
    UA_NS0ID_PUBLISHEDEVENTSTYPEMODIFYFIELDSELECTIONMETHODTYPE = 15054
    UA_NS0ID_PUBLISHEDEVENTSTYPEMODIFYFIELDSELECTIONMETHODTYPE_INPUTARGUMENTS = 15055
    UA_NS0ID_SECURITYGROUPTYPE_MAXPASTKEYCOUNT = 15056
    UA_NS0ID_DATATYPEDESCRIPTION_ENCODING_DEFAULTJSON = 15057
    UA_NS0ID_STRUCTUREDESCRIPTION_ENCODING_DEFAULTJSON = 15058
    UA_NS0ID_ENUMDESCRIPTION_ENCODING_DEFAULTJSON = 15059
    UA_NS0ID_PUBLISHEDVARIABLEDATATYPE_ENCODING_DEFAULTJSON = 15060
    UA_NS0ID_FIELDTARGETDATATYPE_ENCODING_DEFAULTJSON = 15061
    UA_NS0ID_ROLEPERMISSIONTYPE_ENCODING_DEFAULTJSON = 15062
    UA_NS0ID_DATATYPEDEFINITION_ENCODING_DEFAULTJSON = 15063
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTTYPE = 15064
    UA_NS0ID_STRUCTUREFIELD_ENCODING_DEFAULTJSON = 15065
    UA_NS0ID_STRUCTUREDEFINITION_ENCODING_DEFAULTJSON = 15066
    UA_NS0ID_ENUMDEFINITION_ENCODING_DEFAULTJSON = 15067
    UA_NS0ID_NODE_ENCODING_DEFAULTJSON = 15068
    UA_NS0ID_INSTANCENODE_ENCODING_DEFAULTJSON = 15069
    UA_NS0ID_TYPENODE_ENCODING_DEFAULTJSON = 15070
    UA_NS0ID_OBJECTNODE_ENCODING_DEFAULTJSON = 15071
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTTYPE_DISCOVERYADDRESS = 15072
    UA_NS0ID_OBJECTTYPENODE_ENCODING_DEFAULTJSON = 15073
    UA_NS0ID_VARIABLENODE_ENCODING_DEFAULTJSON = 15074
    UA_NS0ID_VARIABLETYPENODE_ENCODING_DEFAULTJSON = 15075
    UA_NS0ID_REFERENCETYPENODE_ENCODING_DEFAULTJSON = 15076
    UA_NS0ID_METHODNODE_ENCODING_DEFAULTJSON = 15077
    UA_NS0ID_VIEWNODE_ENCODING_DEFAULTJSON = 15078
    UA_NS0ID_DATATYPENODE_ENCODING_DEFAULTJSON = 15079
    UA_NS0ID_REFERENCENODE_ENCODING_DEFAULTJSON = 15080
    UA_NS0ID_ARGUMENT_ENCODING_DEFAULTJSON = 15081
    UA_NS0ID_ENUMVALUETYPE_ENCODING_DEFAULTJSON = 15082
    UA_NS0ID_ENUMFIELD_ENCODING_DEFAULTJSON = 15083
    UA_NS0ID_OPTIONSET_ENCODING_DEFAULTJSON = 15084
    UA_NS0ID_UNION_ENCODING_DEFAULTJSON = 15085
    UA_NS0ID_TIMEZONEDATATYPE_ENCODING_DEFAULTJSON = 15086
    UA_NS0ID_APPLICATIONDESCRIPTION_ENCODING_DEFAULTJSON = 15087
    UA_NS0ID_REQUESTHEADER_ENCODING_DEFAULTJSON = 15088
    UA_NS0ID_RESPONSEHEADER_ENCODING_DEFAULTJSON = 15089
    UA_NS0ID_SERVICEFAULT_ENCODING_DEFAULTJSON = 15090
    UA_NS0ID_SESSIONLESSINVOKEREQUESTTYPE_ENCODING_DEFAULTJSON = 15091
    UA_NS0ID_SESSIONLESSINVOKERESPONSETYPE_ENCODING_DEFAULTJSON = 15092
    UA_NS0ID_FINDSERVERSREQUEST_ENCODING_DEFAULTJSON = 15093
    UA_NS0ID_FINDSERVERSRESPONSE_ENCODING_DEFAULTJSON = 15094
    UA_NS0ID_SERVERONNETWORK_ENCODING_DEFAULTJSON = 15095
    UA_NS0ID_FINDSERVERSONNETWORKREQUEST_ENCODING_DEFAULTJSON = 15096
    UA_NS0ID_FINDSERVERSONNETWORKRESPONSE_ENCODING_DEFAULTJSON = 15097
    UA_NS0ID_USERTOKENPOLICY_ENCODING_DEFAULTJSON = 15098
    UA_NS0ID_ENDPOINTDESCRIPTION_ENCODING_DEFAULTJSON = 15099
    UA_NS0ID_GETENDPOINTSREQUEST_ENCODING_DEFAULTJSON = 15100
    UA_NS0ID_GETENDPOINTSRESPONSE_ENCODING_DEFAULTJSON = 15101
    UA_NS0ID_REGISTEREDSERVER_ENCODING_DEFAULTJSON = 15102
    UA_NS0ID_REGISTERSERVERREQUEST_ENCODING_DEFAULTJSON = 15103
    UA_NS0ID_REGISTERSERVERRESPONSE_ENCODING_DEFAULTJSON = 15104
    UA_NS0ID_DISCOVERYCONFIGURATION_ENCODING_DEFAULTJSON = 15105
    UA_NS0ID_MDNSDISCOVERYCONFIGURATION_ENCODING_DEFAULTJSON = 15106
    UA_NS0ID_REGISTERSERVER2REQUEST_ENCODING_DEFAULTJSON = 15107
    UA_NS0ID_SUBSCRIBEDDATASETTYPE = 15108
    UA_NS0ID_CHOICESTATETYPE = 15109
    UA_NS0ID_CHOICESTATETYPE_STATENUMBER = 15110
    UA_NS0ID_TARGETVARIABLESTYPE = 15111
    UA_NS0ID_HASGUARD = 15112
    UA_NS0ID_GUARDVARIABLETYPE = 15113
    UA_NS0ID_TARGETVARIABLESTYPE_TARGETVARIABLES = 15114
    UA_NS0ID_TARGETVARIABLESTYPE_ADDTARGETVARIABLES = 15115
    UA_NS0ID_TARGETVARIABLESTYPE_ADDTARGETVARIABLES_INPUTARGUMENTS = 15116
    UA_NS0ID_TARGETVARIABLESTYPE_ADDTARGETVARIABLES_OUTPUTARGUMENTS = 15117
    UA_NS0ID_TARGETVARIABLESTYPE_REMOVETARGETVARIABLES = 15118
    UA_NS0ID_TARGETVARIABLESTYPE_REMOVETARGETVARIABLES_INPUTARGUMENTS = 15119
    UA_NS0ID_TARGETVARIABLESTYPE_REMOVETARGETVARIABLES_OUTPUTARGUMENTS = 15120
    UA_NS0ID_TARGETVARIABLESTYPEADDTARGETVARIABLESMETHODTYPE = 15121
    UA_NS0ID_TARGETVARIABLESTYPEADDTARGETVARIABLESMETHODTYPE_INPUTARGUMENTS = 15122
    UA_NS0ID_TARGETVARIABLESTYPEADDTARGETVARIABLESMETHODTYPE_OUTPUTARGUMENTS = 15123
    UA_NS0ID_TARGETVARIABLESTYPEREMOVETARGETVARIABLESMETHODTYPE = 15124
    UA_NS0ID_TARGETVARIABLESTYPEREMOVETARGETVARIABLESMETHODTYPE_INPUTARGUMENTS = 15125
    UA_NS0ID_TARGETVARIABLESTYPEREMOVETARGETVARIABLESMETHODTYPE_OUTPUTARGUMENTS = 15126
    UA_NS0ID_SUBSCRIBEDDATASETMIRRORTYPE = 15127
    UA_NS0ID_EXPRESSIONGUARDVARIABLETYPE = 15128
    UA_NS0ID_EXPRESSIONGUARDVARIABLETYPE_EXPRESSION = 15129
    UA_NS0ID_REGISTERSERVER2RESPONSE_ENCODING_DEFAULTJSON = 15130
    UA_NS0ID_CHANNELSECURITYTOKEN_ENCODING_DEFAULTJSON = 15131
    UA_NS0ID_OPENSECURECHANNELREQUEST_ENCODING_DEFAULTJSON = 15132
    UA_NS0ID_OPENSECURECHANNELRESPONSE_ENCODING_DEFAULTJSON = 15133
    UA_NS0ID_CLOSESECURECHANNELREQUEST_ENCODING_DEFAULTJSON = 15134
    UA_NS0ID_CLOSESECURECHANNELRESPONSE_ENCODING_DEFAULTJSON = 15135
    UA_NS0ID_SIGNEDSOFTWARECERTIFICATE_ENCODING_DEFAULTJSON = 15136
    UA_NS0ID_SIGNATUREDATA_ENCODING_DEFAULTJSON = 15137
    UA_NS0ID_CREATESESSIONREQUEST_ENCODING_DEFAULTJSON = 15138
    UA_NS0ID_CREATESESSIONRESPONSE_ENCODING_DEFAULTJSON = 15139
    UA_NS0ID_USERIDENTITYTOKEN_ENCODING_DEFAULTJSON = 15140
    UA_NS0ID_ANONYMOUSIDENTITYTOKEN_ENCODING_DEFAULTJSON = 15141
    UA_NS0ID_USERNAMEIDENTITYTOKEN_ENCODING_DEFAULTJSON = 15142
    UA_NS0ID_X509IDENTITYTOKEN_ENCODING_DEFAULTJSON = 15143
    UA_NS0ID_ISSUEDIDENTITYTOKEN_ENCODING_DEFAULTJSON = 15144
    UA_NS0ID_ACTIVATESESSIONREQUEST_ENCODING_DEFAULTJSON = 15145
    UA_NS0ID_ACTIVATESESSIONRESPONSE_ENCODING_DEFAULTJSON = 15146
    UA_NS0ID_CLOSESESSIONREQUEST_ENCODING_DEFAULTJSON = 15147
    UA_NS0ID_CLOSESESSIONRESPONSE_ENCODING_DEFAULTJSON = 15148
    UA_NS0ID_CANCELREQUEST_ENCODING_DEFAULTJSON = 15149
    UA_NS0ID_CANCELRESPONSE_ENCODING_DEFAULTJSON = 15150
    UA_NS0ID_NODEATTRIBUTES_ENCODING_DEFAULTJSON = 15151
    UA_NS0ID_OBJECTATTRIBUTES_ENCODING_DEFAULTJSON = 15152
    UA_NS0ID_VARIABLEATTRIBUTES_ENCODING_DEFAULTJSON = 15153
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTTYPE_DISCOVERYADDRESS_NETWORKINTERFACE = 15154
    UA_NS0ID_BROKERCONNECTIONTRANSPORTTYPE = 15155
    UA_NS0ID_BROKERCONNECTIONTRANSPORTTYPE_RESOURCEURI = 15156
    UA_NS0ID_METHODATTRIBUTES_ENCODING_DEFAULTJSON = 15157
    UA_NS0ID_OBJECTTYPEATTRIBUTES_ENCODING_DEFAULTJSON = 15158
    UA_NS0ID_VARIABLETYPEATTRIBUTES_ENCODING_DEFAULTJSON = 15159
    UA_NS0ID_REFERENCETYPEATTRIBUTES_ENCODING_DEFAULTJSON = 15160
    UA_NS0ID_DATATYPEATTRIBUTES_ENCODING_DEFAULTJSON = 15161
    UA_NS0ID_VIEWATTRIBUTES_ENCODING_DEFAULTJSON = 15162
    UA_NS0ID_GENERICATTRIBUTEVALUE_ENCODING_DEFAULTJSON = 15163
    UA_NS0ID_GENERICATTRIBUTES_ENCODING_DEFAULTJSON = 15164
    UA_NS0ID_ADDNODESITEM_ENCODING_DEFAULTJSON = 15165
    UA_NS0ID_ADDNODESRESULT_ENCODING_DEFAULTJSON = 15166
    UA_NS0ID_ADDNODESREQUEST_ENCODING_DEFAULTJSON = 15167
    UA_NS0ID_ADDNODESRESPONSE_ENCODING_DEFAULTJSON = 15168
    UA_NS0ID_ADDREFERENCESITEM_ENCODING_DEFAULTJSON = 15169
    UA_NS0ID_ADDREFERENCESREQUEST_ENCODING_DEFAULTJSON = 15170
    UA_NS0ID_ADDREFERENCESRESPONSE_ENCODING_DEFAULTJSON = 15171
    UA_NS0ID_DELETENODESITEM_ENCODING_DEFAULTJSON = 15172
    UA_NS0ID_DELETENODESREQUEST_ENCODING_DEFAULTJSON = 15173
    UA_NS0ID_DELETENODESRESPONSE_ENCODING_DEFAULTJSON = 15174
    UA_NS0ID_DELETEREFERENCESITEM_ENCODING_DEFAULTJSON = 15175
    UA_NS0ID_DELETEREFERENCESREQUEST_ENCODING_DEFAULTJSON = 15176
    UA_NS0ID_DELETEREFERENCESRESPONSE_ENCODING_DEFAULTJSON = 15177
    UA_NS0ID_BROKERCONNECTIONTRANSPORTTYPE_AUTHENTICATIONPROFILEURI = 15178
    UA_NS0ID_VIEWDESCRIPTION_ENCODING_DEFAULTJSON = 15179
    UA_NS0ID_BROWSEDESCRIPTION_ENCODING_DEFAULTJSON = 15180
    UA_NS0ID_USERCREDENTIALCERTIFICATETYPE = 15181
    UA_NS0ID_REFERENCEDESCRIPTION_ENCODING_DEFAULTJSON = 15182
    UA_NS0ID_BROWSERESULT_ENCODING_DEFAULTJSON = 15183
    UA_NS0ID_BROWSEREQUEST_ENCODING_DEFAULTJSON = 15184
    UA_NS0ID_BROWSERESPONSE_ENCODING_DEFAULTJSON = 15185
    UA_NS0ID_BROWSENEXTREQUEST_ENCODING_DEFAULTJSON = 15186
    UA_NS0ID_BROWSENEXTRESPONSE_ENCODING_DEFAULTJSON = 15187
    UA_NS0ID_RELATIVEPATHELEMENT_ENCODING_DEFAULTJSON = 15188
    UA_NS0ID_RELATIVEPATH_ENCODING_DEFAULTJSON = 15189
    UA_NS0ID_BROWSEPATH_ENCODING_DEFAULTJSON = 15190
    UA_NS0ID_BROWSEPATHTARGET_ENCODING_DEFAULTJSON = 15191
    UA_NS0ID_BROWSEPATHRESULT_ENCODING_DEFAULTJSON = 15192
    UA_NS0ID_TRANSLATEBROWSEPATHSTONODEIDSREQUEST_ENCODING_DEFAULTJSON = 15193
    UA_NS0ID_TRANSLATEBROWSEPATHSTONODEIDSRESPONSE_ENCODING_DEFAULTJSON = 15194
    UA_NS0ID_REGISTERNODESREQUEST_ENCODING_DEFAULTJSON = 15195
    UA_NS0ID_REGISTERNODESRESPONSE_ENCODING_DEFAULTJSON = 15196
    UA_NS0ID_UNREGISTERNODESREQUEST_ENCODING_DEFAULTJSON = 15197
    UA_NS0ID_UNREGISTERNODESRESPONSE_ENCODING_DEFAULTJSON = 15198
    UA_NS0ID_ENDPOINTCONFIGURATION_ENCODING_DEFAULTJSON = 15199
    UA_NS0ID_QUERYDATADESCRIPTION_ENCODING_DEFAULTJSON = 15200
    UA_NS0ID_NODETYPEDESCRIPTION_ENCODING_DEFAULTJSON = 15201
    UA_NS0ID_QUERYDATASET_ENCODING_DEFAULTJSON = 15202
    UA_NS0ID_NODEREFERENCE_ENCODING_DEFAULTJSON = 15203
    UA_NS0ID_CONTENTFILTERELEMENT_ENCODING_DEFAULTJSON = 15204
    UA_NS0ID_CONTENTFILTER_ENCODING_DEFAULTJSON = 15205
    UA_NS0ID_FILTEROPERAND_ENCODING_DEFAULTJSON = 15206
    UA_NS0ID_ELEMENTOPERAND_ENCODING_DEFAULTJSON = 15207
    UA_NS0ID_LITERALOPERAND_ENCODING_DEFAULTJSON = 15208
    UA_NS0ID_ATTRIBUTEOPERAND_ENCODING_DEFAULTJSON = 15209
    UA_NS0ID_SIMPLEATTRIBUTEOPERAND_ENCODING_DEFAULTJSON = 15210
    UA_NS0ID_CONTENTFILTERELEMENTRESULT_ENCODING_DEFAULTJSON = 15211
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_GETSECURITYKEYS = 15212
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_GETSECURITYKEYS_INPUTARGUMENTS = 15213
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_GETSECURITYKEYS_OUTPUTARGUMENTS = 15214
    UA_NS0ID_PUBLISHSUBSCRIBE_GETSECURITYKEYS = 15215
    UA_NS0ID_PUBLISHSUBSCRIBE_GETSECURITYKEYS_INPUTARGUMENTS = 15216
    UA_NS0ID_PUBLISHSUBSCRIBE_GETSECURITYKEYS_OUTPUTARGUMENTS = 15217
    UA_NS0ID_GETSECURITYKEYSMETHODTYPE = 15218
    UA_NS0ID_GETSECURITYKEYSMETHODTYPE_INPUTARGUMENTS = 15219
    UA_NS0ID_GETSECURITYKEYSMETHODTYPE_OUTPUTARGUMENTS = 15220
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER_DATASETMETADATA = 15221
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER = 15222
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS = 15223
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_STATE = 15224
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_ENABLE = 15225
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_DISABLE = 15226
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_TRANSPORTSETTINGS = 15227
    UA_NS0ID_CONTENTFILTERRESULT_ENCODING_DEFAULTJSON = 15228
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETMETADATA = 15229
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER = 15230
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS = 15231
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_STATE = 15232
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_ENABLE = 15233
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_DISABLE = 15234
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_TRANSPORTSETTINGS = 15235
    UA_NS0ID_PARSINGRESULT_ENCODING_DEFAULTJSON = 15236
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETMETADATA = 15237
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER = 15238
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS = 15239
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_STATE = 15240
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_ENABLE = 15241
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_DISABLE = 15242
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_TRANSPORTSETTINGS = 15243
    UA_NS0ID_QUERYFIRSTREQUEST_ENCODING_DEFAULTJSON = 15244
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETMETADATA = 15245
    UA_NS0ID_BROKERWRITERGROUPTRANSPORTTYPE_RESOURCEURI = 15246
    UA_NS0ID_BROKERWRITERGROUPTRANSPORTTYPE_AUTHENTICATIONPROFILEURI = 15247
    UA_NS0ID_CREATECREDENTIALMETHODTYPE = 15248
    UA_NS0ID_BROKERWRITERGROUPTRANSPORTTYPE_REQUESTEDDELIVERYGUARANTEE = 15249
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTTYPE_RESOURCEURI = 15250
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTTYPE_AUTHENTICATIONPROFILEURI = 15251
    UA_NS0ID_QUERYFIRSTRESPONSE_ENCODING_DEFAULTJSON = 15252
    UA_NS0ID_CREATECREDENTIALMETHODTYPE_INPUTARGUMENTS = 15253
    UA_NS0ID_QUERYNEXTREQUEST_ENCODING_DEFAULTJSON = 15254
    UA_NS0ID_QUERYNEXTRESPONSE_ENCODING_DEFAULTJSON = 15255
    UA_NS0ID_READVALUEID_ENCODING_DEFAULTJSON = 15256
    UA_NS0ID_READREQUEST_ENCODING_DEFAULTJSON = 15257
    UA_NS0ID_READRESPONSE_ENCODING_DEFAULTJSON = 15258
    UA_NS0ID_HISTORYREADVALUEID_ENCODING_DEFAULTJSON = 15259
    UA_NS0ID_HISTORYREADRESULT_ENCODING_DEFAULTJSON = 15260
    UA_NS0ID_HISTORYREADDETAILS_ENCODING_DEFAULTJSON = 15261
    UA_NS0ID_READEVENTDETAILS_ENCODING_DEFAULTJSON = 15262
    UA_NS0ID_READRAWMODIFIEDDETAILS_ENCODING_DEFAULTJSON = 15263
    UA_NS0ID_READPROCESSEDDETAILS_ENCODING_DEFAULTJSON = 15264
    UA_NS0ID_PUBSUBGROUPTYPE_STATUS = 15265
    UA_NS0ID_PUBSUBGROUPTYPE_STATUS_STATE = 15266
    UA_NS0ID_PUBSUBGROUPTYPE_STATUS_ENABLE = 15267
    UA_NS0ID_PUBSUBGROUPTYPE_STATUS_DISABLE = 15268
    UA_NS0ID_READATTIMEDETAILS_ENCODING_DEFAULTJSON = 15269
    UA_NS0ID_HISTORYDATA_ENCODING_DEFAULTJSON = 15270
    UA_NS0ID_MODIFICATIONINFO_ENCODING_DEFAULTJSON = 15271
    UA_NS0ID_HISTORYMODIFIEDDATA_ENCODING_DEFAULTJSON = 15272
    UA_NS0ID_HISTORYEVENT_ENCODING_DEFAULTJSON = 15273
    UA_NS0ID_HISTORYREADREQUEST_ENCODING_DEFAULTJSON = 15274
    UA_NS0ID_HISTORYREADRESPONSE_ENCODING_DEFAULTJSON = 15275
    UA_NS0ID_WRITEVALUE_ENCODING_DEFAULTJSON = 15276
    UA_NS0ID_WRITEREQUEST_ENCODING_DEFAULTJSON = 15277
    UA_NS0ID_WRITERESPONSE_ENCODING_DEFAULTJSON = 15278
    UA_NS0ID_HISTORYUPDATEDETAILS_ENCODING_DEFAULTJSON = 15279
    UA_NS0ID_UPDATEDATADETAILS_ENCODING_DEFAULTJSON = 15280
    UA_NS0ID_UPDATESTRUCTUREDATADETAILS_ENCODING_DEFAULTJSON = 15281
    UA_NS0ID_UPDATEEVENTDETAILS_ENCODING_DEFAULTJSON = 15282
    UA_NS0ID_DELETERAWMODIFIEDDETAILS_ENCODING_DEFAULTJSON = 15283
    UA_NS0ID_DELETEATTIMEDETAILS_ENCODING_DEFAULTJSON = 15284
    UA_NS0ID_DELETEEVENTDETAILS_ENCODING_DEFAULTJSON = 15285
    UA_NS0ID_HISTORYUPDATERESULT_ENCODING_DEFAULTJSON = 15286
    UA_NS0ID_HISTORYUPDATEREQUEST_ENCODING_DEFAULTJSON = 15287
    UA_NS0ID_HISTORYUPDATERESPONSE_ENCODING_DEFAULTJSON = 15288
    UA_NS0ID_CALLMETHODREQUEST_ENCODING_DEFAULTJSON = 15289
    UA_NS0ID_CALLMETHODRESULT_ENCODING_DEFAULTJSON = 15290
    UA_NS0ID_CALLREQUEST_ENCODING_DEFAULTJSON = 15291
    UA_NS0ID_CALLRESPONSE_ENCODING_DEFAULTJSON = 15292
    UA_NS0ID_MONITORINGFILTER_ENCODING_DEFAULTJSON = 15293
    UA_NS0ID_DATACHANGEFILTER_ENCODING_DEFAULTJSON = 15294
    UA_NS0ID_EVENTFILTER_ENCODING_DEFAULTJSON = 15295
    UA_NS0ID_HASDATASETWRITER = 15296
    UA_NS0ID_HASDATASETREADER = 15297
    UA_NS0ID_DATASETWRITERTYPE = 15298
    UA_NS0ID_DATASETWRITERTYPE_STATUS = 15299
    UA_NS0ID_DATASETWRITERTYPE_STATUS_STATE = 15300
    UA_NS0ID_DATASETWRITERTYPE_STATUS_ENABLE = 15301
    UA_NS0ID_DATASETWRITERTYPE_STATUS_DISABLE = 15302
    UA_NS0ID_DATASETWRITERTYPE_TRANSPORTSETTINGS = 15303
    UA_NS0ID_AGGREGATECONFIGURATION_ENCODING_DEFAULTJSON = 15304
    UA_NS0ID_DATASETWRITERTRANSPORTTYPE = 15305
    UA_NS0ID_DATASETREADERTYPE = 15306
    UA_NS0ID_DATASETREADERTYPE_STATUS = 15307
    UA_NS0ID_DATASETREADERTYPE_STATUS_STATE = 15308
    UA_NS0ID_DATASETREADERTYPE_STATUS_ENABLE = 15309
    UA_NS0ID_DATASETREADERTYPE_STATUS_DISABLE = 15310
    UA_NS0ID_DATASETREADERTYPE_TRANSPORTSETTINGS = 15311
    UA_NS0ID_AGGREGATEFILTER_ENCODING_DEFAULTJSON = 15312
    UA_NS0ID_MONITORINGFILTERRESULT_ENCODING_DEFAULTJSON = 15313
    UA_NS0ID_EVENTFILTERRESULT_ENCODING_DEFAULTJSON = 15314
    UA_NS0ID_AGGREGATEFILTERRESULT_ENCODING_DEFAULTJSON = 15315
    UA_NS0ID_DATASETREADERTYPE_SUBSCRIBEDDATASET = 15316
    UA_NS0ID_ELSEGUARDVARIABLETYPE = 15317
    UA_NS0ID_BASEANALOGTYPE = 15318
    UA_NS0ID_DATASETREADERTRANSPORTTYPE = 15319
    UA_NS0ID_MONITORINGPARAMETERS_ENCODING_DEFAULTJSON = 15320
    UA_NS0ID_MONITOREDITEMCREATEREQUEST_ENCODING_DEFAULTJSON = 15321
    UA_NS0ID_MONITOREDITEMCREATERESULT_ENCODING_DEFAULTJSON = 15322
    UA_NS0ID_CREATEMONITOREDITEMSREQUEST_ENCODING_DEFAULTJSON = 15323
    UA_NS0ID_CREATEMONITOREDITEMSRESPONSE_ENCODING_DEFAULTJSON = 15324
    UA_NS0ID_MONITOREDITEMMODIFYREQUEST_ENCODING_DEFAULTJSON = 15325
    UA_NS0ID_MONITOREDITEMMODIFYRESULT_ENCODING_DEFAULTJSON = 15326
    UA_NS0ID_MODIFYMONITOREDITEMSREQUEST_ENCODING_DEFAULTJSON = 15327
    UA_NS0ID_MODIFYMONITOREDITEMSRESPONSE_ENCODING_DEFAULTJSON = 15328
    UA_NS0ID_SETMONITORINGMODEREQUEST_ENCODING_DEFAULTJSON = 15329
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTTYPE_REQUESTEDDELIVERYGUARANTEE = 15330
    UA_NS0ID_SETMONITORINGMODERESPONSE_ENCODING_DEFAULTJSON = 15331
    UA_NS0ID_SETTRIGGERINGREQUEST_ENCODING_DEFAULTJSON = 15332
    UA_NS0ID_SETTRIGGERINGRESPONSE_ENCODING_DEFAULTJSON = 15333
    UA_NS0ID_BROKERDATASETREADERTRANSPORTTYPE_RESOURCEURI = 15334
    UA_NS0ID_DELETEMONITOREDITEMSREQUEST_ENCODING_DEFAULTJSON = 15335
    UA_NS0ID_DELETEMONITOREDITEMSRESPONSE_ENCODING_DEFAULTJSON = 15336
    UA_NS0ID_CREATESUBSCRIPTIONREQUEST_ENCODING_DEFAULTJSON = 15337
    UA_NS0ID_CREATESUBSCRIPTIONRESPONSE_ENCODING_DEFAULTJSON = 15338
    UA_NS0ID_MODIFYSUBSCRIPTIONREQUEST_ENCODING_DEFAULTJSON = 15339
    UA_NS0ID_MODIFYSUBSCRIPTIONRESPONSE_ENCODING_DEFAULTJSON = 15340
    UA_NS0ID_SETPUBLISHINGMODEREQUEST_ENCODING_DEFAULTJSON = 15341
    UA_NS0ID_SETPUBLISHINGMODERESPONSE_ENCODING_DEFAULTJSON = 15342
    UA_NS0ID_NOTIFICATIONMESSAGE_ENCODING_DEFAULTJSON = 15343
    UA_NS0ID_NOTIFICATIONDATA_ENCODING_DEFAULTJSON = 15344
    UA_NS0ID_DATACHANGENOTIFICATION_ENCODING_DEFAULTJSON = 15345
    UA_NS0ID_MONITOREDITEMNOTIFICATION_ENCODING_DEFAULTJSON = 15346
    UA_NS0ID_EVENTNOTIFICATIONLIST_ENCODING_DEFAULTJSON = 15347
    UA_NS0ID_EVENTFIELDLIST_ENCODING_DEFAULTJSON = 15348
    UA_NS0ID_HISTORYEVENTFIELDLIST_ENCODING_DEFAULTJSON = 15349
    UA_NS0ID_STATUSCHANGENOTIFICATION_ENCODING_DEFAULTJSON = 15350
    UA_NS0ID_SUBSCRIPTIONACKNOWLEDGEMENT_ENCODING_DEFAULTJSON = 15351
    UA_NS0ID_PUBLISHREQUEST_ENCODING_DEFAULTJSON = 15352
    UA_NS0ID_PUBLISHRESPONSE_ENCODING_DEFAULTJSON = 15353
    UA_NS0ID_REPUBLISHREQUEST_ENCODING_DEFAULTJSON = 15354
    UA_NS0ID_REPUBLISHRESPONSE_ENCODING_DEFAULTJSON = 15355
    UA_NS0ID_TRANSFERRESULT_ENCODING_DEFAULTJSON = 15356
    UA_NS0ID_TRANSFERSUBSCRIPTIONSREQUEST_ENCODING_DEFAULTJSON = 15357
    UA_NS0ID_TRANSFERSUBSCRIPTIONSRESPONSE_ENCODING_DEFAULTJSON = 15358
    UA_NS0ID_DELETESUBSCRIPTIONSREQUEST_ENCODING_DEFAULTJSON = 15359
    UA_NS0ID_DELETESUBSCRIPTIONSRESPONSE_ENCODING_DEFAULTJSON = 15360
    UA_NS0ID_BUILDINFO_ENCODING_DEFAULTJSON = 15361
    UA_NS0ID_REDUNDANTSERVERDATATYPE_ENCODING_DEFAULTJSON = 15362
    UA_NS0ID_ENDPOINTURLLISTDATATYPE_ENCODING_DEFAULTJSON = 15363
    UA_NS0ID_NETWORKGROUPDATATYPE_ENCODING_DEFAULTJSON = 15364
    UA_NS0ID_SAMPLINGINTERVALDIAGNOSTICSDATATYPE_ENCODING_DEFAULTJSON = 15365
    UA_NS0ID_SERVERDIAGNOSTICSSUMMARYDATATYPE_ENCODING_DEFAULTJSON = 15366
    UA_NS0ID_SERVERSTATUSDATATYPE_ENCODING_DEFAULTJSON = 15367
    UA_NS0ID_SESSIONDIAGNOSTICSDATATYPE_ENCODING_DEFAULTJSON = 15368
    UA_NS0ID_SESSIONSECURITYDIAGNOSTICSDATATYPE_ENCODING_DEFAULTJSON = 15369
    UA_NS0ID_SERVICECOUNTERDATATYPE_ENCODING_DEFAULTJSON = 15370
    UA_NS0ID_STATUSRESULT_ENCODING_DEFAULTJSON = 15371
    UA_NS0ID_SUBSCRIPTIONDIAGNOSTICSDATATYPE_ENCODING_DEFAULTJSON = 15372
    UA_NS0ID_MODELCHANGESTRUCTUREDATATYPE_ENCODING_DEFAULTJSON = 15373
    UA_NS0ID_SEMANTICCHANGESTRUCTUREDATATYPE_ENCODING_DEFAULTJSON = 15374
    UA_NS0ID_RANGE_ENCODING_DEFAULTJSON = 15375
    UA_NS0ID_EUINFORMATION_ENCODING_DEFAULTJSON = 15376
    UA_NS0ID_COMPLEXNUMBERTYPE_ENCODING_DEFAULTJSON = 15377
    UA_NS0ID_DOUBLECOMPLEXNUMBERTYPE_ENCODING_DEFAULTJSON = 15378
    UA_NS0ID_AXISINFORMATION_ENCODING_DEFAULTJSON = 15379
    UA_NS0ID_XVTYPE_ENCODING_DEFAULTJSON = 15380
    UA_NS0ID_PROGRAMDIAGNOSTICDATATYPE_ENCODING_DEFAULTJSON = 15381
    UA_NS0ID_ANNOTATION_ENCODING_DEFAULTJSON = 15382
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE = 15383
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_CREATESESSIONID = 15384
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_CREATECLIENTNAME = 15385
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_INVOCATIONCREATIONTIME = 15386
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_LASTTRANSITIONTIME = 15387
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_LASTMETHODCALL = 15388
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_LASTMETHODSESSIONID = 15389
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_LASTMETHODINPUTARGUMENTS = 15390
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_LASTMETHODOUTPUTARGUMENTS = 15391
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_LASTMETHODINPUTVALUES = 15392
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_LASTMETHODOUTPUTVALUES = 15393
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_LASTMETHODCALLTIME = 15394
    UA_NS0ID_PROGRAMDIAGNOSTIC2TYPE_LASTMETHODRETURNSTATUS = 15395
    UA_NS0ID_PROGRAMDIAGNOSTIC2DATATYPE = 15396
    UA_NS0ID_PROGRAMDIAGNOSTIC2DATATYPE_ENCODING_DEFAULTBINARY = 15397
    UA_NS0ID_OPCUA_BINARYSCHEMA_PROGRAMDIAGNOSTIC2DATATYPE = 15398
    UA_NS0ID_OPCUA_BINARYSCHEMA_PROGRAMDIAGNOSTIC2DATATYPE_DATATYPEVERSION = 15399
    UA_NS0ID_OPCUA_BINARYSCHEMA_PROGRAMDIAGNOSTIC2DATATYPE_DICTIONARYFRAGMENT = 15400
    UA_NS0ID_PROGRAMDIAGNOSTIC2DATATYPE_ENCODING_DEFAULTXML = 15401
    UA_NS0ID_OPCUA_XMLSCHEMA_PROGRAMDIAGNOSTIC2DATATYPE = 15402
    UA_NS0ID_OPCUA_XMLSCHEMA_PROGRAMDIAGNOSTIC2DATATYPE_DATATYPEVERSION = 15403
    UA_NS0ID_OPCUA_XMLSCHEMA_PROGRAMDIAGNOSTIC2DATATYPE_DICTIONARYFRAGMENT = 15404
    UA_NS0ID_PROGRAMDIAGNOSTIC2DATATYPE_ENCODING_DEFAULTJSON = 15405
    UA_NS0ID_ACCESSLEVELEXTYPE = 15406
    UA_NS0ID_ACCESSLEVELEXTYPE_OPTIONSETVALUES = 15407
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_APPLICATIONSEXCLUDE = 15408
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_ENDPOINTSEXCLUDE = 15409
    UA_NS0ID_ROLETYPE_APPLICATIONSEXCLUDE = 15410
    UA_NS0ID_ROLETYPE_ENDPOINTSEXCLUDE = 15411
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_APPLICATIONSEXCLUDE = 15412
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_ENDPOINTSEXCLUDE = 15413
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_APPLICATIONSEXCLUDE = 15414
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_ENDPOINTSEXCLUDE = 15415
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_APPLICATIONSEXCLUDE = 15416
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_ENDPOINTSEXCLUDE = 15417
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_APPLICATIONSEXCLUDE = 15418
    UA_NS0ID_BROKERDATASETREADERTRANSPORTTYPE_AUTHENTICATIONPROFILEURI = 15419
    UA_NS0ID_BROKERDATASETREADERTRANSPORTTYPE_REQUESTEDDELIVERYGUARANTEE = 15420
    UA_NS0ID_SIMPLETYPEDESCRIPTION_ENCODING_DEFAULTBINARY = 15421
    UA_NS0ID_UABINARYFILEDATATYPE_ENCODING_DEFAULTBINARY = 15422
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_ENDPOINTSEXCLUDE = 15423
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_APPLICATIONSEXCLUDE = 15424
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_ENDPOINTSEXCLUDE = 15425
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_APPLICATIONSEXCLUDE = 15426
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_ENDPOINTSEXCLUDE = 15427
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_APPLICATIONSEXCLUDE = 15428
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_ENDPOINTSEXCLUDE = 15429
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_APPLICATIONSEXCLUDE = 15430
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_GETSECURITYGROUP = 15431
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_GETSECURITYGROUP_INPUTARGUMENTS = 15432
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_GETSECURITYGROUP_OUTPUTARGUMENTS = 15433
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_SECURITYGROUPS = 15434
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_SECURITYGROUPS_ADDSECURITYGROUP = 15435
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_SECURITYGROUPS_ADDSECURITYGROUP_INPUTARGUMENTS = 15436
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_SECURITYGROUPS_ADDSECURITYGROUP_OUTPUTARGUMENTS = 15437
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_SECURITYGROUPS_REMOVESECURITYGROUP = 15438
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_SECURITYGROUPS_REMOVESECURITYGROUP_INPUTARGUMENTS = 15439
    UA_NS0ID_PUBLISHSUBSCRIBE_GETSECURITYGROUP = 15440
    UA_NS0ID_PUBLISHSUBSCRIBE_GETSECURITYGROUP_INPUTARGUMENTS = 15441
    UA_NS0ID_PUBLISHSUBSCRIBE_GETSECURITYGROUP_OUTPUTARGUMENTS = 15442
    UA_NS0ID_PUBLISHSUBSCRIBE_SECURITYGROUPS = 15443
    UA_NS0ID_PUBLISHSUBSCRIBE_SECURITYGROUPS_ADDSECURITYGROUP = 15444
    UA_NS0ID_PUBLISHSUBSCRIBE_SECURITYGROUPS_ADDSECURITYGROUP_INPUTARGUMENTS = 15445
    UA_NS0ID_PUBLISHSUBSCRIBE_SECURITYGROUPS_ADDSECURITYGROUP_OUTPUTARGUMENTS = 15446
    UA_NS0ID_PUBLISHSUBSCRIBE_SECURITYGROUPS_REMOVESECURITYGROUP = 15447
    UA_NS0ID_PUBLISHSUBSCRIBE_SECURITYGROUPS_REMOVESECURITYGROUP_INPUTARGUMENTS = 15448
    UA_NS0ID_GETSECURITYGROUPMETHODTYPE = 15449
    UA_NS0ID_GETSECURITYGROUPMETHODTYPE_INPUTARGUMENTS = 15450
    UA_NS0ID_GETSECURITYGROUPMETHODTYPE_OUTPUTARGUMENTS = 15451
    UA_NS0ID_SECURITYGROUPFOLDERTYPE = 15452
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPFOLDERNAME_PLACEHOLDER = 15453
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPFOLDERNAME_PLACEHOLDER_ADDSECURITYGROUP = 15454
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPFOLDERNAME_PLACEHOLDER_ADDSECURITYGROUP_INPUTARGUMENTS = 15455
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPFOLDERNAME_PLACEHOLDER_ADDSECURITYGROUP_OUTPUTARGUMENTS = 15456
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPFOLDERNAME_PLACEHOLDER_REMOVESECURITYGROUP = 15457
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPFOLDERNAME_PLACEHOLDER_REMOVESECURITYGROUP_INPUTARGUMENTS = 15458
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPNAME_PLACEHOLDER = 15459
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_SECURITYGROUPNAME_PLACEHOLDER_SECURITYGROUPID = 15460
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_ADDSECURITYGROUP = 15461
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_ADDSECURITYGROUP_INPUTARGUMENTS = 15462
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_ADDSECURITYGROUP_OUTPUTARGUMENTS = 15463
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_REMOVESECURITYGROUP = 15464
    UA_NS0ID_SECURITYGROUPFOLDERTYPE_REMOVESECURITYGROUP_INPUTARGUMENTS = 15465
    UA_NS0ID_ADDSECURITYGROUPMETHODTYPE = 15466
    UA_NS0ID_ADDSECURITYGROUPMETHODTYPE_INPUTARGUMENTS = 15467
    UA_NS0ID_ADDSECURITYGROUPMETHODTYPE_OUTPUTARGUMENTS = 15468
    UA_NS0ID_REMOVESECURITYGROUPMETHODTYPE = 15469
    UA_NS0ID_REMOVESECURITYGROUPMETHODTYPE_INPUTARGUMENTS = 15470
    UA_NS0ID_SECURITYGROUPTYPE = 15471
    UA_NS0ID_SECURITYGROUPTYPE_SECURITYGROUPID = 15472
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER_EXTENSIONFIELDS = 15473
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER_EXTENSIONFIELDS_ADDEXTENSIONFIELD = 15474
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER_EXTENSIONFIELDS_ADDEXTENSIONFIELD_INPUTARGUMENTS = 15475
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER_EXTENSIONFIELDS_ADDEXTENSIONFIELD_OUTPUTARGUMENTS = 15476
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER_EXTENSIONFIELDS_REMOVEEXTENSIONFIELD = 15477
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER_EXTENSIONFIELDS_REMOVEEXTENSIONFIELD_INPUTARGUMENTS = 15478
    UA_NS0ID_BROKERCONNECTIONTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 15479
    UA_NS0ID_WRITERGROUPDATATYPE = 15480
    UA_NS0ID_PUBLISHEDDATASETTYPE_EXTENSIONFIELDS = 15481
    UA_NS0ID_PUBLISHEDDATASETTYPE_EXTENSIONFIELDS_ADDEXTENSIONFIELD = 15482
    UA_NS0ID_PUBLISHEDDATASETTYPE_EXTENSIONFIELDS_ADDEXTENSIONFIELD_INPUTARGUMENTS = 15483
    UA_NS0ID_PUBLISHEDDATASETTYPE_EXTENSIONFIELDS_ADDEXTENSIONFIELD_OUTPUTARGUMENTS = 15484
    UA_NS0ID_PUBLISHEDDATASETTYPE_EXTENSIONFIELDS_REMOVEEXTENSIONFIELD = 15485
    UA_NS0ID_PUBLISHEDDATASETTYPE_EXTENSIONFIELDS_REMOVEEXTENSIONFIELD_INPUTARGUMENTS = 15486
    UA_NS0ID_STRUCTUREDESCRIPTION = 15487
    UA_NS0ID_ENUMDESCRIPTION = 15488
    UA_NS0ID_EXTENSIONFIELDSTYPE = 15489
    UA_NS0ID_EXTENSIONFIELDSTYPE_EXTENSIONFIELDNAME_PLACEHOLDER = 15490
    UA_NS0ID_EXTENSIONFIELDSTYPE_ADDEXTENSIONFIELD = 15491
    UA_NS0ID_EXTENSIONFIELDSTYPE_ADDEXTENSIONFIELD_INPUTARGUMENTS = 15492
    UA_NS0ID_EXTENSIONFIELDSTYPE_ADDEXTENSIONFIELD_OUTPUTARGUMENTS = 15493
    UA_NS0ID_EXTENSIONFIELDSTYPE_REMOVEEXTENSIONFIELD = 15494
    UA_NS0ID_EXTENSIONFIELDSTYPE_REMOVEEXTENSIONFIELD_INPUTARGUMENTS = 15495
    UA_NS0ID_ADDEXTENSIONFIELDMETHODTYPE = 15496
    UA_NS0ID_ADDEXTENSIONFIELDMETHODTYPE_INPUTARGUMENTS = 15497
    UA_NS0ID_ADDEXTENSIONFIELDMETHODTYPE_OUTPUTARGUMENTS = 15498
    UA_NS0ID_REMOVEEXTENSIONFIELDMETHODTYPE = 15499
    UA_NS0ID_REMOVEEXTENSIONFIELDMETHODTYPE_INPUTARGUMENTS = 15500
    UA_NS0ID_OPCUA_BINARYSCHEMA_SIMPLETYPEDESCRIPTION = 15501
    UA_NS0ID_NETWORKADDRESSDATATYPE = 15502
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_EXTENSIONFIELDS = 15503
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_EXTENSIONFIELDS_ADDEXTENSIONFIELD = 15504
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_EXTENSIONFIELDS_ADDEXTENSIONFIELD_INPUTARGUMENTS = 15505
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_EXTENSIONFIELDS_ADDEXTENSIONFIELD_OUTPUTARGUMENTS = 15506
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_EXTENSIONFIELDS_REMOVEEXTENSIONFIELD = 15507
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_EXTENSIONFIELDS_REMOVEEXTENSIONFIELD_INPUTARGUMENTS = 15508
    UA_NS0ID_OPCUA_BINARYSCHEMA_SIMPLETYPEDESCRIPTION_DATATYPEVERSION = 15509
    UA_NS0ID_NETWORKADDRESSURLDATATYPE = 15510
    UA_NS0ID_PUBLISHEDEVENTSTYPE_EXTENSIONFIELDS = 15511
    UA_NS0ID_PUBLISHEDEVENTSTYPE_EXTENSIONFIELDS_ADDEXTENSIONFIELD = 15512
    UA_NS0ID_PUBLISHEDEVENTSTYPE_EXTENSIONFIELDS_ADDEXTENSIONFIELD_INPUTARGUMENTS = 15513
    UA_NS0ID_PUBLISHEDEVENTSTYPE_EXTENSIONFIELDS_ADDEXTENSIONFIELD_OUTPUTARGUMENTS = 15514
    UA_NS0ID_PUBLISHEDEVENTSTYPE_EXTENSIONFIELDS_REMOVEEXTENSIONFIELD = 15515
    UA_NS0ID_PUBLISHEDEVENTSTYPE_EXTENSIONFIELDS_REMOVEEXTENSIONFIELD_INPUTARGUMENTS = 15516
    UA_NS0ID_PUBLISHEDEVENTSTYPE_MODIFYFIELDSELECTION_OUTPUTARGUMENTS = 15517
    UA_NS0ID_PUBLISHEDEVENTSTYPEMODIFYFIELDSELECTIONMETHODTYPE_OUTPUTARGUMENTS = 15518
    UA_NS0ID_OPCUA_BINARYSCHEMA_SIMPLETYPEDESCRIPTION_DICTIONARYFRAGMENT = 15519
    UA_NS0ID_READERGROUPDATATYPE = 15520
    UA_NS0ID_OPCUA_BINARYSCHEMA_UABINARYFILEDATATYPE = 15521
    UA_NS0ID_OPCUA_BINARYSCHEMA_UABINARYFILEDATATYPE_DATATYPEVERSION = 15522
    UA_NS0ID_OPCUA_BINARYSCHEMA_UABINARYFILEDATATYPE_DICTIONARYFRAGMENT = 15523
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERCONNECTIONTRANSPORTDATATYPE = 15524
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERCONNECTIONTRANSPORTDATATYPE_DATATYPEVERSION = 15525
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERCONNECTIONTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15526
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_ENDPOINTSEXCLUDE = 15527
    UA_NS0ID_ENDPOINTTYPE = 15528
    UA_NS0ID_SIMPLETYPEDESCRIPTION_ENCODING_DEFAULTXML = 15529
    UA_NS0ID_PUBSUBCONFIGURATIONDATATYPE = 15530
    UA_NS0ID_UABINARYFILEDATATYPE_ENCODING_DEFAULTXML = 15531
    UA_NS0ID_DATAGRAMWRITERGROUPTRANSPORTDATATYPE = 15532
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDRESS_NETWORKINTERFACE = 15533
    UA_NS0ID_DATATYPESCHEMAHEADER = 15534
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE = 15535
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_EVENTID = 15536
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_EVENTTYPE = 15537
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_SOURCENODE = 15538
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_SOURCENAME = 15539
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_TIME = 15540
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_RECEIVETIME = 15541
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_LOCALTIME = 15542
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_MESSAGE = 15543
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_SEVERITY = 15544
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_CONNECTIONID = 15545
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_GROUPID = 15546
    UA_NS0ID_PUBSUBSTATUSEVENTTYPE_STATE = 15547
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE = 15548
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_EVENTID = 15549
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_EVENTTYPE = 15550
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_SOURCENODE = 15551
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_SOURCENAME = 15552
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_TIME = 15553
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_RECEIVETIME = 15554
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_LOCALTIME = 15555
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_MESSAGE = 15556
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_SEVERITY = 15557
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_CONNECTIONID = 15558
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_GROUPID = 15559
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_STATE = 15560
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_ACTUAL = 15561
    UA_NS0ID_PUBSUBTRANSPORTLIMITSEXCEEDEVENTTYPE_MAXIMUM = 15562
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE = 15563
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_EVENTID = 15564
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_EVENTTYPE = 15565
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_SOURCENODE = 15566
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_SOURCENAME = 15567
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_TIME = 15568
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_RECEIVETIME = 15569
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_LOCALTIME = 15570
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_MESSAGE = 15571
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_SEVERITY = 15572
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_CONNECTIONID = 15573
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_GROUPID = 15574
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_STATE = 15575
    UA_NS0ID_PUBSUBCOMMUNICATIONFAILUREEVENTTYPE_ERROR = 15576
    UA_NS0ID_DATASETFIELDFLAGS_OPTIONSETVALUES = 15577
    UA_NS0ID_PUBLISHEDDATASETDATATYPE = 15578
    UA_NS0ID_BROKERCONNECTIONTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 15579
    UA_NS0ID_PUBLISHEDDATASETSOURCEDATATYPE = 15580
    UA_NS0ID_PUBLISHEDDATAITEMSDATATYPE = 15581
    UA_NS0ID_PUBLISHEDEVENTSDATATYPE = 15582
    UA_NS0ID_DATASETFIELDCONTENTMASK = 15583
    UA_NS0ID_DATASETFIELDCONTENTMASK_OPTIONSETVALUES = 15584
    UA_NS0ID_OPCUA_XMLSCHEMA_SIMPLETYPEDESCRIPTION = 15585
    UA_NS0ID_OPCUA_XMLSCHEMA_SIMPLETYPEDESCRIPTION_DATATYPEVERSION = 15586
    UA_NS0ID_OPCUA_XMLSCHEMA_SIMPLETYPEDESCRIPTION_DICTIONARYFRAGMENT = 15587
    UA_NS0ID_OPCUA_XMLSCHEMA_UABINARYFILEDATATYPE = 15588
    UA_NS0ID_STRUCTUREDESCRIPTION_ENCODING_DEFAULTXML = 15589
    UA_NS0ID_ENUMDESCRIPTION_ENCODING_DEFAULTXML = 15590
    UA_NS0ID_OPCUA_XMLSCHEMA_STRUCTUREDESCRIPTION = 15591
    UA_NS0ID_OPCUA_XMLSCHEMA_STRUCTUREDESCRIPTION_DATATYPEVERSION = 15592
    UA_NS0ID_OPCUA_XMLSCHEMA_STRUCTUREDESCRIPTION_DICTIONARYFRAGMENT = 15593
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMDESCRIPTION = 15594
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMDESCRIPTION_DATATYPEVERSION = 15595
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMDESCRIPTION_DICTIONARYFRAGMENT = 15596
    UA_NS0ID_DATASETWRITERDATATYPE = 15597
    UA_NS0ID_DATASETWRITERTRANSPORTDATATYPE = 15598
    UA_NS0ID_OPCUA_BINARYSCHEMA_STRUCTUREDESCRIPTION = 15599
    UA_NS0ID_OPCUA_BINARYSCHEMA_STRUCTUREDESCRIPTION_DATATYPEVERSION = 15600
    UA_NS0ID_OPCUA_BINARYSCHEMA_STRUCTUREDESCRIPTION_DICTIONARYFRAGMENT = 15601
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMDESCRIPTION = 15602
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMDESCRIPTION_DATATYPEVERSION = 15603
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMDESCRIPTION_DICTIONARYFRAGMENT = 15604
    UA_NS0ID_DATASETWRITERMESSAGEDATATYPE = 15605
    UA_NS0ID_SERVER_SERVERCAPABILITIES_ROLESET = 15606
    UA_NS0ID_ROLESETTYPE = 15607
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER = 15608
    UA_NS0ID_PUBSUBGROUPDATATYPE = 15609
    UA_NS0ID_OPCUA_XMLSCHEMA_UABINARYFILEDATATYPE_DATATYPEVERSION = 15610
    UA_NS0ID_WRITERGROUPTRANSPORTDATATYPE = 15611
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_ADDIDENTITY = 15612
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_ADDIDENTITY_INPUTARGUMENTS = 15613
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_REMOVEIDENTITY = 15614
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_REMOVEIDENTITY_INPUTARGUMENTS = 15615
    UA_NS0ID_WRITERGROUPMESSAGEDATATYPE = 15616
    UA_NS0ID_PUBSUBCONNECTIONDATATYPE = 15617
    UA_NS0ID_CONNECTIONTRANSPORTDATATYPE = 15618
    UA_NS0ID_OPCUA_XMLSCHEMA_UABINARYFILEDATATYPE_DICTIONARYFRAGMENT = 15619
    UA_NS0ID_ROLETYPE = 15620
    UA_NS0ID_READERGROUPTRANSPORTDATATYPE = 15621
    UA_NS0ID_READERGROUPMESSAGEDATATYPE = 15622
    UA_NS0ID_DATASETREADERDATATYPE = 15623
    UA_NS0ID_ROLETYPE_ADDIDENTITY = 15624
    UA_NS0ID_ROLETYPE_ADDIDENTITY_INPUTARGUMENTS = 15625
    UA_NS0ID_ROLETYPE_REMOVEIDENTITY = 15626
    UA_NS0ID_ROLETYPE_REMOVEIDENTITY_INPUTARGUMENTS = 15627
    UA_NS0ID_DATASETREADERTRANSPORTDATATYPE = 15628
    UA_NS0ID_DATASETREADERMESSAGEDATATYPE = 15629
    UA_NS0ID_SUBSCRIBEDDATASETDATATYPE = 15630
    UA_NS0ID_TARGETVARIABLESDATATYPE = 15631
    UA_NS0ID_IDENTITYCRITERIATYPE = 15632
    UA_NS0ID_IDENTITYCRITERIATYPE_ENUMVALUES = 15633
    UA_NS0ID_IDENTITYMAPPINGRULETYPE = 15634
    UA_NS0ID_SUBSCRIBEDDATASETMIRRORDATATYPE = 15635
    UA_NS0ID_ADDIDENTITYMETHODTYPE = 15636
    UA_NS0ID_ADDIDENTITYMETHODTYPE_INPUTARGUMENTS = 15637
    UA_NS0ID_REMOVEIDENTITYMETHODTYPE = 15638
    UA_NS0ID_REMOVEIDENTITYMETHODTYPE_INPUTARGUMENTS = 15639
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERCONNECTIONTRANSPORTDATATYPE = 15640
    UA_NS0ID_DATASETORDERINGTYPE_ENUMSTRINGS = 15641
    UA_NS0ID_UADPNETWORKMESSAGECONTENTMASK = 15642
    UA_NS0ID_UADPNETWORKMESSAGECONTENTMASK_OPTIONSETVALUES = 15643
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS = 15644
    UA_NS0ID_UADPWRITERGROUPMESSAGEDATATYPE = 15645
    UA_NS0ID_UADPDATASETMESSAGECONTENTMASK = 15646
    UA_NS0ID_UADPDATASETMESSAGECONTENTMASK_OPTIONSETVALUES = 15647
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_ADDIDENTITY = 15648
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_ADDIDENTITY_INPUTARGUMENTS = 15649
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_REMOVEIDENTITY = 15650
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_REMOVEIDENTITY_INPUTARGUMENTS = 15651
    UA_NS0ID_UADPDATASETWRITERMESSAGEDATATYPE = 15652
    UA_NS0ID_UADPDATASETREADERMESSAGEDATATYPE = 15653
    UA_NS0ID_JSONNETWORKMESSAGECONTENTMASK = 15654
    UA_NS0ID_JSONNETWORKMESSAGECONTENTMASK_OPTIONSETVALUES = 15655
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER = 15656
    UA_NS0ID_JSONWRITERGROUPMESSAGEDATATYPE = 15657
    UA_NS0ID_JSONDATASETMESSAGECONTENTMASK = 15658
    UA_NS0ID_JSONDATASETMESSAGECONTENTMASK_OPTIONSETVALUES = 15659
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_ADDIDENTITY = 15660
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_ADDIDENTITY_INPUTARGUMENTS = 15661
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_REMOVEIDENTITY = 15662
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_REMOVEIDENTITY_INPUTARGUMENTS = 15663
    UA_NS0ID_JSONDATASETWRITERMESSAGEDATATYPE = 15664
    UA_NS0ID_JSONDATASETREADERMESSAGEDATATYPE = 15665
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERCONNECTIONTRANSPORTDATATYPE_DATATYPEVERSION = 15666
    UA_NS0ID_BROKERWRITERGROUPTRANSPORTDATATYPE = 15667
    UA_NS0ID_WELLKNOWNROLE_OBSERVER = 15668
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTDATATYPE = 15669
    UA_NS0ID_BROKERDATASETREADERTRANSPORTDATATYPE = 15670
    UA_NS0ID_ENDPOINTTYPE_ENCODING_DEFAULTBINARY = 15671
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_ADDIDENTITY = 15672
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_ADDIDENTITY_INPUTARGUMENTS = 15673
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_REMOVEIDENTITY = 15674
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_REMOVEIDENTITY_INPUTARGUMENTS = 15675
    UA_NS0ID_DATATYPESCHEMAHEADER_ENCODING_DEFAULTBINARY = 15676
    UA_NS0ID_PUBLISHEDDATASETDATATYPE_ENCODING_DEFAULTBINARY = 15677
    UA_NS0ID_PUBLISHEDDATASETSOURCEDATATYPE_ENCODING_DEFAULTBINARY = 15678
    UA_NS0ID_PUBLISHEDDATAITEMSDATATYPE_ENCODING_DEFAULTBINARY = 15679
    UA_NS0ID_WELLKNOWNROLE_OPERATOR = 15680
    UA_NS0ID_PUBLISHEDEVENTSDATATYPE_ENCODING_DEFAULTBINARY = 15681
    UA_NS0ID_DATASETWRITERDATATYPE_ENCODING_DEFAULTBINARY = 15682
    UA_NS0ID_DATASETWRITERTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 15683
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_ADDIDENTITY = 15684
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_ADDIDENTITY_INPUTARGUMENTS = 15685
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_REMOVEIDENTITY = 15686
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_REMOVEIDENTITY_INPUTARGUMENTS = 15687
    UA_NS0ID_DATASETWRITERMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15688
    UA_NS0ID_PUBSUBGROUPDATATYPE_ENCODING_DEFAULTBINARY = 15689
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERCONNECTIONTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15690
    UA_NS0ID_WRITERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 15691
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR = 15692
    UA_NS0ID_WRITERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15693
    UA_NS0ID_PUBSUBCONNECTIONDATATYPE_ENCODING_DEFAULTBINARY = 15694
    UA_NS0ID_CONNECTIONTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 15695
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_ADDIDENTITY = 15696
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_ADDIDENTITY_INPUTARGUMENTS = 15697
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_REMOVEIDENTITY = 15698
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_REMOVEIDENTITY_INPUTARGUMENTS = 15699
    UA_NS0ID_SIMPLETYPEDESCRIPTION_ENCODING_DEFAULTJSON = 15700
    UA_NS0ID_READERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 15701
    UA_NS0ID_READERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15702
    UA_NS0ID_DATASETREADERDATATYPE_ENCODING_DEFAULTBINARY = 15703
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN = 15704
    UA_NS0ID_DATASETREADERTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 15705
    UA_NS0ID_DATASETREADERMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15706
    UA_NS0ID_SUBSCRIBEDDATASETDATATYPE_ENCODING_DEFAULTBINARY = 15707
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_ADDIDENTITY = 15708
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_ADDIDENTITY_INPUTARGUMENTS = 15709
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_REMOVEIDENTITY = 15710
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_REMOVEIDENTITY_INPUTARGUMENTS = 15711
    UA_NS0ID_TARGETVARIABLESDATATYPE_ENCODING_DEFAULTBINARY = 15712
    UA_NS0ID_SUBSCRIBEDDATASETMIRRORDATATYPE_ENCODING_DEFAULTBINARY = 15713
    UA_NS0ID_UABINARYFILEDATATYPE_ENCODING_DEFAULTJSON = 15714
    UA_NS0ID_UADPWRITERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15715
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN = 15716
    UA_NS0ID_UADPDATASETWRITERMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15717
    UA_NS0ID_UADPDATASETREADERMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15718
    UA_NS0ID_JSONWRITERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15719
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_ADDIDENTITY = 15720
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_ADDIDENTITY_INPUTARGUMENTS = 15721
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_REMOVEIDENTITY = 15722
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_REMOVEIDENTITY_INPUTARGUMENTS = 15723
    UA_NS0ID_JSONDATASETWRITERMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15724
    UA_NS0ID_JSONDATASETREADERMESSAGEDATATYPE_ENCODING_DEFAULTBINARY = 15725
    UA_NS0ID_BROKERCONNECTIONTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 15726
    UA_NS0ID_BROKERWRITERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 15727
    UA_NS0ID_IDENTITYMAPPINGRULETYPE_ENCODING_DEFAULTXML = 15728
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 15729
    UA_NS0ID_OPCUA_XMLSCHEMA_IDENTITYMAPPINGRULETYPE = 15730
    UA_NS0ID_OPCUA_XMLSCHEMA_IDENTITYMAPPINGRULETYPE_DATATYPEVERSION = 15731
    UA_NS0ID_OPCUA_XMLSCHEMA_IDENTITYMAPPINGRULETYPE_DICTIONARYFRAGMENT = 15732
    UA_NS0ID_BROKERDATASETREADERTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 15733
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTTYPE = 15734
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTTYPE_DATATYPEVERSION = 15735
    UA_NS0ID_IDENTITYMAPPINGRULETYPE_ENCODING_DEFAULTBINARY = 15736
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENDPOINTTYPE_DICTIONARYFRAGMENT = 15737
    UA_NS0ID_OPCUA_BINARYSCHEMA_IDENTITYMAPPINGRULETYPE = 15738
    UA_NS0ID_OPCUA_BINARYSCHEMA_IDENTITYMAPPINGRULETYPE_DATATYPEVERSION = 15739
    UA_NS0ID_OPCUA_BINARYSCHEMA_IDENTITYMAPPINGRULETYPE_DICTIONARYFRAGMENT = 15740
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPESCHEMAHEADER = 15741
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPESCHEMAHEADER_DATATYPEVERSION = 15742
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPESCHEMAHEADER_DICTIONARYFRAGMENT = 15743
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE = 15744
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_CLIENTPROCESSINGTIMEOUT = 15745
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_GENERATEFILEFORREAD = 15746
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_GENERATEFILEFORREAD_INPUTARGUMENTS = 15747
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_GENERATEFILEFORREAD_OUTPUTARGUMENTS = 15748
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_GENERATEFILEFORWRITE = 15749
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_GENERATEFILEFORWRITE_OUTPUTARGUMENTS = 15750
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_CLOSEANDCOMMIT = 15751
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_CLOSEANDCOMMIT_INPUTARGUMENTS = 15752
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_CLOSEANDCOMMIT_OUTPUTARGUMENTS = 15753
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER = 15754
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_CURRENTSTATE = 15755
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_CURRENTSTATE_ID = 15756
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_CURRENTSTATE_NAME = 15757
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_CURRENTSTATE_NUMBER = 15758
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 15759
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_LASTTRANSITION = 15760
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_LASTTRANSITION_ID = 15761
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_LASTTRANSITION_NAME = 15762
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_LASTTRANSITION_NUMBER = 15763
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_LASTTRANSITION_TRANSITIONTIME = 15764
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 15765
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDDATASETDATATYPE = 15766
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDDATASETDATATYPE_DATATYPEVERSION = 15767
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDDATASETDATATYPE_DICTIONARYFRAGMENT = 15768
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDDATASETSOURCEDATATYPE = 15769
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDDATASETSOURCEDATATYPE_DATATYPEVERSION = 15770
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDDATASETSOURCEDATATYPE_DICTIONARYFRAGMENT = 15771
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDDATAITEMSDATATYPE = 15772
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDDATAITEMSDATATYPE_DATATYPEVERSION = 15773
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDDATAITEMSDATATYPE_DICTIONARYFRAGMENT = 15774
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDEVENTSDATATYPE = 15775
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDEVENTSDATATYPE_DATATYPEVERSION = 15776
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBLISHEDEVENTSDATATYPE_DICTIONARYFRAGMENT = 15777
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETWRITERDATATYPE = 15778
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETWRITERDATATYPE_DATATYPEVERSION = 15779
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETWRITERDATATYPE_DICTIONARYFRAGMENT = 15780
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETWRITERTRANSPORTDATATYPE = 15781
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETWRITERTRANSPORTDATATYPE_DATATYPEVERSION = 15782
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETWRITERTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15783
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETWRITERMESSAGEDATATYPE = 15784
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETWRITERMESSAGEDATATYPE_DATATYPEVERSION = 15785
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETWRITERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15786
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBSUBGROUPDATATYPE = 15787
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBSUBGROUPDATATYPE_DATATYPEVERSION = 15788
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBSUBGROUPDATATYPE_DICTIONARYFRAGMENT = 15789
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER = 15790
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_PUBLISHERID = 15791
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTPROFILEURI = 15792
    UA_NS0ID_OPCUA_BINARYSCHEMA_WRITERGROUPTRANSPORTDATATYPE = 15793
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_RESET = 15794
    UA_NS0ID_GENERATEFILEFORREADMETHODTYPE = 15795
    UA_NS0ID_GENERATEFILEFORREADMETHODTYPE_INPUTARGUMENTS = 15796
    UA_NS0ID_GENERATEFILEFORREADMETHODTYPE_OUTPUTARGUMENTS = 15797
    UA_NS0ID_GENERATEFILEFORWRITEMETHODTYPE = 15798
    UA_NS0ID_GENERATEFILEFORWRITEMETHODTYPE_OUTPUTARGUMENTS = 15799
    UA_NS0ID_CLOSEANDCOMMITMETHODTYPE = 15800
    UA_NS0ID_CLOSEANDCOMMITMETHODTYPE_INPUTARGUMENTS = 15801
    UA_NS0ID_CLOSEANDCOMMITMETHODTYPE_OUTPUTARGUMENTS = 15802
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE = 15803
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_CURRENTSTATE = 15804
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_CURRENTSTATE_ID = 15805
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_CURRENTSTATE_NAME = 15806
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_CURRENTSTATE_NUMBER = 15807
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 15808
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_LASTTRANSITION = 15809
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_LASTTRANSITION_ID = 15810
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_LASTTRANSITION_NAME = 15811
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_LASTTRANSITION_NUMBER = 15812
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_LASTTRANSITION_TRANSITIONTIME = 15813
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 15814
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_IDLE = 15815
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_IDLE_STATENUMBER = 15816
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READPREPARE = 15817
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READPREPARE_STATENUMBER = 15818
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READTRANSFER = 15819
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READTRANSFER_STATENUMBER = 15820
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_APPLYWRITE = 15821
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_APPLYWRITE_STATENUMBER = 15822
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_ERROR = 15823
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_ERROR_STATENUMBER = 15824
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_IDLETOREADPREPARE = 15825
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_IDLETOREADPREPARE_TRANSITIONNUMBER = 15826
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READPREPARETOREADTRANSFER = 15827
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READPREPARETOREADTRANSFER_TRANSITIONNUMBER = 15828
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READTRANSFERTOIDLE = 15829
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READTRANSFERTOIDLE_TRANSITIONNUMBER = 15830
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_IDLETOAPPLYWRITE = 15831
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_IDLETOAPPLYWRITE_TRANSITIONNUMBER = 15832
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_APPLYWRITETOIDLE = 15833
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_APPLYWRITETOIDLE_TRANSITIONNUMBER = 15834
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READPREPARETOERROR = 15835
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READPREPARETOERROR_TRANSITIONNUMBER = 15836
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READTRANSFERTOERROR = 15837
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_READTRANSFERTOERROR_TRANSITIONNUMBER = 15838
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_APPLYWRITETOERROR = 15839
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_APPLYWRITETOERROR_TRANSITIONNUMBER = 15840
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_ERRORTOIDLE = 15841
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_ERRORTOIDLE_TRANSITIONNUMBER = 15842
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_RESET = 15843
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_STATUS = 15844
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_STATUS_STATE = 15845
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_STATUS_ENABLE = 15846
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_STATUS_DISABLE = 15847
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTPROFILEURI_SELECTIONS = 15848
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTPROFILEURI_SELECTIONDESCRIPTIONS = 15849
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTPROFILEURI_RESTRICTTOLIST = 15850
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDRESS = 15851
    UA_NS0ID_OPCUA_BINARYSCHEMA_WRITERGROUPTRANSPORTDATATYPE_DATATYPEVERSION = 15852
    UA_NS0ID_OPCUA_BINARYSCHEMA_WRITERGROUPTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15853
    UA_NS0ID_OPCUA_BINARYSCHEMA_WRITERGROUPMESSAGEDATATYPE = 15854
    UA_NS0ID_OPCUA_BINARYSCHEMA_WRITERGROUPMESSAGEDATATYPE_DATATYPEVERSION = 15855
    UA_NS0ID_OPCUA_BINARYSCHEMA_WRITERGROUPMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15856
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBSUBCONNECTIONDATATYPE = 15857
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBSUBCONNECTIONDATATYPE_DATATYPEVERSION = 15858
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBSUBCONNECTIONDATATYPE_DICTIONARYFRAGMENT = 15859
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONNECTIONTRANSPORTDATATYPE = 15860
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONNECTIONTRANSPORTDATATYPE_DATATYPEVERSION = 15861
    UA_NS0ID_OPCUA_BINARYSCHEMA_CONNECTIONTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15862
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDRESS_NETWORKINTERFACE = 15863
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTSETTINGS = 15864
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_STATUS = 15865
    UA_NS0ID_OPCUA_BINARYSCHEMA_READERGROUPTRANSPORTDATATYPE = 15866
    UA_NS0ID_OPCUA_BINARYSCHEMA_READERGROUPTRANSPORTDATATYPE_DATATYPEVERSION = 15867
    UA_NS0ID_OPCUA_BINARYSCHEMA_READERGROUPTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15868
    UA_NS0ID_OPCUA_BINARYSCHEMA_READERGROUPMESSAGEDATATYPE = 15869
    UA_NS0ID_OPCUA_BINARYSCHEMA_READERGROUPMESSAGEDATATYPE_DATATYPEVERSION = 15870
    UA_NS0ID_OPCUA_BINARYSCHEMA_READERGROUPMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15871
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETREADERDATATYPE = 15872
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETREADERDATATYPE_DATATYPEVERSION = 15873
    UA_NS0ID_OVERRIDEVALUEHANDLING = 15874
    UA_NS0ID_OVERRIDEVALUEHANDLING_ENUMSTRINGS = 15875
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETREADERDATATYPE_DICTIONARYFRAGMENT = 15876
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETREADERTRANSPORTDATATYPE = 15877
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETREADERTRANSPORTDATATYPE_DATATYPEVERSION = 15878
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETREADERTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15879
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETREADERMESSAGEDATATYPE = 15880
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETREADERMESSAGEDATATYPE_DATATYPEVERSION = 15881
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATASETREADERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15882
    UA_NS0ID_OPCUA_BINARYSCHEMA_SUBSCRIBEDDATASETDATATYPE = 15883
    UA_NS0ID_OPCUA_BINARYSCHEMA_SUBSCRIBEDDATASETDATATYPE_DATATYPEVERSION = 15884
    UA_NS0ID_OPCUA_BINARYSCHEMA_SUBSCRIBEDDATASETDATATYPE_DICTIONARYFRAGMENT = 15885
    UA_NS0ID_OPCUA_BINARYSCHEMA_TARGETVARIABLESDATATYPE = 15886
    UA_NS0ID_OPCUA_BINARYSCHEMA_TARGETVARIABLESDATATYPE_DATATYPEVERSION = 15887
    UA_NS0ID_OPCUA_BINARYSCHEMA_TARGETVARIABLESDATATYPE_DICTIONARYFRAGMENT = 15888
    UA_NS0ID_OPCUA_BINARYSCHEMA_SUBSCRIBEDDATASETMIRRORDATATYPE = 15889
    UA_NS0ID_OPCUA_BINARYSCHEMA_SUBSCRIBEDDATASETMIRRORDATATYPE_DATATYPEVERSION = 15890
    UA_NS0ID_OPCUA_BINARYSCHEMA_SUBSCRIBEDDATASETMIRRORDATATYPE_DICTIONARYFRAGMENT = 15891
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_STATUS_STATE = 15892
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_STATUS_ENABLE = 15893
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_STATUS_DISABLE = 15894
    UA_NS0ID_OPCUA_BINARYSCHEMA_UADPWRITERGROUPMESSAGEDATATYPE = 15895
    UA_NS0ID_OPCUA_BINARYSCHEMA_UADPWRITERGROUPMESSAGEDATATYPE_DATATYPEVERSION = 15896
    UA_NS0ID_OPCUA_BINARYSCHEMA_UADPWRITERGROUPMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15897
    UA_NS0ID_OPCUA_BINARYSCHEMA_UADPDATASETWRITERMESSAGEDATATYPE = 15898
    UA_NS0ID_OPCUA_BINARYSCHEMA_UADPDATASETWRITERMESSAGEDATATYPE_DATATYPEVERSION = 15899
    UA_NS0ID_OPCUA_BINARYSCHEMA_UADPDATASETWRITERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15900
    UA_NS0ID_SESSIONLESSINVOKEREQUESTTYPE = 15901
    UA_NS0ID_SESSIONLESSINVOKEREQUESTTYPE_ENCODING_DEFAULTXML = 15902
    UA_NS0ID_SESSIONLESSINVOKEREQUESTTYPE_ENCODING_DEFAULTBINARY = 15903
    UA_NS0ID_DATASETFIELDFLAGS = 15904
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTSETTINGS = 15905
    UA_NS0ID_PUBSUBKEYSERVICETYPE = 15906
    UA_NS0ID_PUBSUBKEYSERVICETYPE_GETSECURITYKEYS = 15907
    UA_NS0ID_PUBSUBKEYSERVICETYPE_GETSECURITYKEYS_INPUTARGUMENTS = 15908
    UA_NS0ID_PUBSUBKEYSERVICETYPE_GETSECURITYKEYS_OUTPUTARGUMENTS = 15909
    UA_NS0ID_PUBSUBKEYSERVICETYPE_GETSECURITYGROUP = 15910
    UA_NS0ID_PUBSUBKEYSERVICETYPE_GETSECURITYGROUP_INPUTARGUMENTS = 15911
    UA_NS0ID_PUBSUBKEYSERVICETYPE_GETSECURITYGROUP_OUTPUTARGUMENTS = 15912
    UA_NS0ID_PUBSUBKEYSERVICETYPE_SECURITYGROUPS = 15913
    UA_NS0ID_PUBSUBKEYSERVICETYPE_SECURITYGROUPS_ADDSECURITYGROUP = 15914
    UA_NS0ID_PUBSUBKEYSERVICETYPE_SECURITYGROUPS_ADDSECURITYGROUP_INPUTARGUMENTS = 15915
    UA_NS0ID_PUBSUBKEYSERVICETYPE_SECURITYGROUPS_ADDSECURITYGROUP_OUTPUTARGUMENTS = 15916
    UA_NS0ID_PUBSUBKEYSERVICETYPE_SECURITYGROUPS_REMOVESECURITYGROUP = 15917
    UA_NS0ID_PUBSUBKEYSERVICETYPE_SECURITYGROUPS_REMOVESECURITYGROUP_INPUTARGUMENTS = 15918
    UA_NS0ID_OPCUA_BINARYSCHEMA_UADPDATASETREADERMESSAGEDATATYPE = 15919
    UA_NS0ID_OPCUA_BINARYSCHEMA_UADPDATASETREADERMESSAGEDATATYPE_DATATYPEVERSION = 15920
    UA_NS0ID_OPCUA_BINARYSCHEMA_UADPDATASETREADERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15921
    UA_NS0ID_OPCUA_BINARYSCHEMA_JSONWRITERGROUPMESSAGEDATATYPE = 15922
    UA_NS0ID_OPCUA_BINARYSCHEMA_JSONWRITERGROUPMESSAGEDATATYPE_DATATYPEVERSION = 15923
    UA_NS0ID_OPCUA_BINARYSCHEMA_JSONWRITERGROUPMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15924
    UA_NS0ID_OPCUA_BINARYSCHEMA_JSONDATASETWRITERMESSAGEDATATYPE = 15925
    UA_NS0ID_PUBSUBGROUPTYPE_SECURITYMODE = 15926
    UA_NS0ID_PUBSUBGROUPTYPE_SECURITYGROUPID = 15927
    UA_NS0ID_PUBSUBGROUPTYPE_SECURITYKEYSERVICES = 15928
    UA_NS0ID_OPCUA_BINARYSCHEMA_JSONDATASETWRITERMESSAGEDATATYPE_DATATYPEVERSION = 15929
    UA_NS0ID_OPCUA_BINARYSCHEMA_JSONDATASETWRITERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15930
    UA_NS0ID_OPCUA_BINARYSCHEMA_JSONDATASETREADERMESSAGEDATATYPE = 15931
    UA_NS0ID_DATASETREADERTYPE_SECURITYMODE = 15932
    UA_NS0ID_DATASETREADERTYPE_SECURITYGROUPID = 15933
    UA_NS0ID_DATASETREADERTYPE_SECURITYKEYSERVICES = 15934
    UA_NS0ID_OPCUA_BINARYSCHEMA_JSONDATASETREADERMESSAGEDATATYPE_DATATYPEVERSION = 15935
    UA_NS0ID_OPCUA_BINARYSCHEMA_JSONDATASETREADERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 15936
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS = 15937
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_DIAGNOSTICSLEVEL = 15938
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION = 15939
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERWRITERGROUPTRANSPORTDATATYPE = 15940
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERWRITERGROUPTRANSPORTDATATYPE_DATATYPEVERSION = 15941
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERWRITERGROUPTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15942
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERDATASETWRITERTRANSPORTDATATYPE = 15943
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERDATASETWRITERTRANSPORTDATATYPE_DATATYPEVERSION = 15944
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERDATASETWRITERTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15945
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERDATASETREADERTRANSPORTDATATYPE = 15946
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERDATASETREADERTRANSPORTDATATYPE_DATATYPEVERSION = 15947
    UA_NS0ID_OPCUA_BINARYSCHEMA_BROKERDATASETREADERTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 15948
    UA_NS0ID_ENDPOINTTYPE_ENCODING_DEFAULTXML = 15949
    UA_NS0ID_DATATYPESCHEMAHEADER_ENCODING_DEFAULTXML = 15950
    UA_NS0ID_PUBLISHEDDATASETDATATYPE_ENCODING_DEFAULTXML = 15951
    UA_NS0ID_PUBLISHEDDATASETSOURCEDATATYPE_ENCODING_DEFAULTXML = 15952
    UA_NS0ID_PUBLISHEDDATAITEMSDATATYPE_ENCODING_DEFAULTXML = 15953
    UA_NS0ID_PUBLISHEDEVENTSDATATYPE_ENCODING_DEFAULTXML = 15954
    UA_NS0ID_DATASETWRITERDATATYPE_ENCODING_DEFAULTXML = 15955
    UA_NS0ID_DATASETWRITERTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 15956
    UA_NS0ID_OPCUANAMESPACEMETADATA = 15957
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEURI = 15958
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEVERSION = 15959
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEPUBLICATIONDATE = 15960
    UA_NS0ID_OPCUANAMESPACEMETADATA_ISNAMESPACESUBSET = 15961
    UA_NS0ID_OPCUANAMESPACEMETADATA_STATICNODEIDTYPES = 15962
    UA_NS0ID_OPCUANAMESPACEMETADATA_STATICNUMERICNODEIDRANGE = 15963
    UA_NS0ID_OPCUANAMESPACEMETADATA_STATICSTRINGNODEIDPATTERN = 15964
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE = 15965
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_SIZE = 15966
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_WRITABLE = 15967
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_USERWRITABLE = 15968
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_OPENCOUNT = 15969
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_MIMETYPE = 15970
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_OPEN = 15971
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_OPEN_INPUTARGUMENTS = 15972
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_OPEN_OUTPUTARGUMENTS = 15973
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_CLOSE = 15974
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_CLOSE_INPUTARGUMENTS = 15975
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_READ = 15976
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_READ_INPUTARGUMENTS = 15977
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_READ_OUTPUTARGUMENTS = 15978
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_WRITE = 15979
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_WRITE_INPUTARGUMENTS = 15980
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_GETPOSITION = 15981
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_GETPOSITION_INPUTARGUMENTS = 15982
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_GETPOSITION_OUTPUTARGUMENTS = 15983
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_SETPOSITION = 15984
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_SETPOSITION_INPUTARGUMENTS = 15985
    UA_NS0ID_OPCUANAMESPACEMETADATA_NAMESPACEFILE_EXPORTNAMESPACE = 15986
    UA_NS0ID_DATASETWRITERMESSAGEDATATYPE_ENCODING_DEFAULTXML = 15987
    UA_NS0ID_PUBSUBGROUPDATATYPE_ENCODING_DEFAULTXML = 15988
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 15989
    UA_NS0ID_WRITERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 15990
    UA_NS0ID_WRITERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTXML = 15991
    UA_NS0ID_PUBSUBCONNECTIONDATATYPE_ENCODING_DEFAULTXML = 15992
    UA_NS0ID_CONNECTIONTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 15993
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 15994
    UA_NS0ID_READERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 15995
    UA_NS0ID_READERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTXML = 15996
    UA_NS0ID_ROLESETTYPE_ADDROLE = 15997
    UA_NS0ID_ROLESETTYPE_ADDROLE_INPUTARGUMENTS = 15998
    UA_NS0ID_ROLESETTYPE_ADDROLE_OUTPUTARGUMENTS = 15999
    UA_NS0ID_ROLESETTYPE_REMOVEROLE = 16000
    UA_NS0ID_ROLESETTYPE_REMOVEROLE_INPUTARGUMENTS = 16001
    UA_NS0ID_ADDROLEMETHODTYPE = 16002
    UA_NS0ID_ADDROLEMETHODTYPE_INPUTARGUMENTS = 16003
    UA_NS0ID_ADDROLEMETHODTYPE_OUTPUTARGUMENTS = 16004
    UA_NS0ID_REMOVEROLEMETHODTYPE = 16005
    UA_NS0ID_REMOVEROLEMETHODTYPE_INPUTARGUMENTS = 16006
    UA_NS0ID_DATASETREADERDATATYPE_ENCODING_DEFAULTXML = 16007
    UA_NS0ID_DATASETREADERTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 16008
    UA_NS0ID_DATASETREADERMESSAGEDATATYPE_ENCODING_DEFAULTXML = 16009
    UA_NS0ID_SUBSCRIBEDDATASETDATATYPE_ENCODING_DEFAULTXML = 16010
    UA_NS0ID_TARGETVARIABLESDATATYPE_ENCODING_DEFAULTXML = 16011
    UA_NS0ID_SUBSCRIBEDDATASETMIRRORDATATYPE_ENCODING_DEFAULTXML = 16012
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 16013
    UA_NS0ID_UADPWRITERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTXML = 16014
    UA_NS0ID_UADPDATASETWRITERMESSAGEDATATYPE_ENCODING_DEFAULTXML = 16015
    UA_NS0ID_UADPDATASETREADERMESSAGEDATATYPE_ENCODING_DEFAULTXML = 16016
    UA_NS0ID_JSONWRITERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTXML = 16017
    UA_NS0ID_JSONDATASETWRITERMESSAGEDATATYPE_ENCODING_DEFAULTXML = 16018
    UA_NS0ID_JSONDATASETREADERMESSAGEDATATYPE_ENCODING_DEFAULTXML = 16019
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 16020
    UA_NS0ID_BROKERWRITERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 16021
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 16022
    UA_NS0ID_BROKERDATASETREADERTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 16023
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTTYPE = 16024
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTTYPE_DATATYPEVERSION = 16025
    UA_NS0ID_OPCUA_XMLSCHEMA_ENDPOINTTYPE_DICTIONARYFRAGMENT = 16026
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPESCHEMAHEADER = 16027
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPESCHEMAHEADER_DATATYPEVERSION = 16028
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPESCHEMAHEADER_DICTIONARYFRAGMENT = 16029
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDDATASETDATATYPE = 16030
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDDATASETDATATYPE_DATATYPEVERSION = 16031
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDDATASETDATATYPE_DICTIONARYFRAGMENT = 16032
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDDATASETSOURCEDATATYPE = 16033
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDDATASETSOURCEDATATYPE_DATATYPEVERSION = 16034
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDDATASETSOURCEDATATYPE_DICTIONARYFRAGMENT = 16035
    UA_NS0ID_WELLKNOWNROLE_ENGINEER = 16036
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDDATAITEMSDATATYPE = 16037
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDDATAITEMSDATATYPE_DATATYPEVERSION = 16038
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDDATAITEMSDATATYPE_DICTIONARYFRAGMENT = 16039
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDEVENTSDATATYPE = 16040
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_ADDIDENTITY = 16041
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_ADDIDENTITY_INPUTARGUMENTS = 16042
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_REMOVEIDENTITY = 16043
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_REMOVEIDENTITY_INPUTARGUMENTS = 16044
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDEVENTSDATATYPE_DATATYPEVERSION = 16045
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBLISHEDEVENTSDATATYPE_DICTIONARYFRAGMENT = 16046
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETWRITERDATATYPE = 16047
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETWRITERDATATYPE_DATATYPEVERSION = 16048
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETWRITERDATATYPE_DICTIONARYFRAGMENT = 16049
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETWRITERTRANSPORTDATATYPE = 16050
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETWRITERTRANSPORTDATATYPE_DATATYPEVERSION = 16051
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETWRITERTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 16052
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETWRITERMESSAGEDATATYPE = 16053
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETWRITERMESSAGEDATATYPE_DATATYPEVERSION = 16054
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETWRITERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16055
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBSUBGROUPDATATYPE = 16056
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBSUBGROUPDATATYPE_DATATYPEVERSION = 16057
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBSUBGROUPDATATYPE_DICTIONARYFRAGMENT = 16058
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR = 16059
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_ACTIVE = 16060
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 16061
    UA_NS0ID_OPCUA_XMLSCHEMA_WRITERGROUPTRANSPORTDATATYPE = 16062
    UA_NS0ID_OPCUA_XMLSCHEMA_WRITERGROUPTRANSPORTDATATYPE_DATATYPEVERSION = 16063
    UA_NS0ID_OPCUA_XMLSCHEMA_WRITERGROUPTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 16064
    UA_NS0ID_OPCUA_XMLSCHEMA_WRITERGROUPMESSAGEDATATYPE = 16065
    UA_NS0ID_OPCUA_XMLSCHEMA_WRITERGROUPMESSAGEDATATYPE_DATATYPEVERSION = 16066
    UA_NS0ID_OPCUA_XMLSCHEMA_WRITERGROUPMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16067
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBSUBCONNECTIONDATATYPE = 16068
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBSUBCONNECTIONDATATYPE_DATATYPEVERSION = 16069
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBSUBCONNECTIONDATATYPE_DICTIONARYFRAGMENT = 16070
    UA_NS0ID_OPCUA_XMLSCHEMA_CONNECTIONTRANSPORTDATATYPE = 16071
    UA_NS0ID_OPCUA_XMLSCHEMA_CONNECTIONTRANSPORTDATATYPE_DATATYPEVERSION = 16072
    UA_NS0ID_OPCUA_XMLSCHEMA_CONNECTIONTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 16073
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 16074
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 16075
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_RESET = 16076
    UA_NS0ID_OPCUA_XMLSCHEMA_READERGROUPTRANSPORTDATATYPE = 16077
    UA_NS0ID_OPCUA_XMLSCHEMA_READERGROUPTRANSPORTDATATYPE_DATATYPEVERSION = 16078
    UA_NS0ID_OPCUA_XMLSCHEMA_READERGROUPTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 16079
    UA_NS0ID_OPCUA_XMLSCHEMA_READERGROUPMESSAGEDATATYPE = 16080
    UA_NS0ID_OPCUA_XMLSCHEMA_READERGROUPMESSAGEDATATYPE_DATATYPEVERSION = 16081
    UA_NS0ID_OPCUA_XMLSCHEMA_READERGROUPMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16082
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETREADERDATATYPE = 16083
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETREADERDATATYPE_DATATYPEVERSION = 16084
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETREADERDATATYPE_DICTIONARYFRAGMENT = 16085
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETREADERTRANSPORTDATATYPE = 16086
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETREADERTRANSPORTDATATYPE_DATATYPEVERSION = 16087
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETREADERTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 16088
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETREADERMESSAGEDATATYPE = 16089
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETREADERMESSAGEDATATYPE_DATATYPEVERSION = 16090
    UA_NS0ID_OPCUA_XMLSCHEMA_DATASETREADERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16091
    UA_NS0ID_OPCUA_XMLSCHEMA_SUBSCRIBEDDATASETDATATYPE = 16092
    UA_NS0ID_OPCUA_XMLSCHEMA_SUBSCRIBEDDATASETDATATYPE_DATATYPEVERSION = 16093
    UA_NS0ID_OPCUA_XMLSCHEMA_SUBSCRIBEDDATASETDATATYPE_DICTIONARYFRAGMENT = 16094
    UA_NS0ID_OPCUA_XMLSCHEMA_TARGETVARIABLESDATATYPE = 16095
    UA_NS0ID_OPCUA_XMLSCHEMA_TARGETVARIABLESDATATYPE_DATATYPEVERSION = 16096
    UA_NS0ID_OPCUA_XMLSCHEMA_TARGETVARIABLESDATATYPE_DICTIONARYFRAGMENT = 16097
    UA_NS0ID_OPCUA_XMLSCHEMA_SUBSCRIBEDDATASETMIRRORDATATYPE = 16098
    UA_NS0ID_OPCUA_XMLSCHEMA_SUBSCRIBEDDATASETMIRRORDATATYPE_DATATYPEVERSION = 16099
    UA_NS0ID_OPCUA_XMLSCHEMA_SUBSCRIBEDDATASETMIRRORDATATYPE_DICTIONARYFRAGMENT = 16100
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_SUBERROR = 16101
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS = 16102
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR = 16103
    UA_NS0ID_OPCUA_XMLSCHEMA_UADPWRITERGROUPMESSAGEDATATYPE = 16104
    UA_NS0ID_OPCUA_XMLSCHEMA_UADPWRITERGROUPMESSAGEDATATYPE_DATATYPEVERSION = 16105
    UA_NS0ID_OPCUA_XMLSCHEMA_UADPWRITERGROUPMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16106
    UA_NS0ID_OPCUA_XMLSCHEMA_UADPDATASETWRITERMESSAGEDATATYPE = 16107
    UA_NS0ID_OPCUA_XMLSCHEMA_UADPDATASETWRITERMESSAGEDATATYPE_DATATYPEVERSION = 16108
    UA_NS0ID_OPCUA_XMLSCHEMA_UADPDATASETWRITERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16109
    UA_NS0ID_OPCUA_XMLSCHEMA_UADPDATASETREADERMESSAGEDATATYPE = 16110
    UA_NS0ID_OPCUA_XMLSCHEMA_UADPDATASETREADERMESSAGEDATATYPE_DATATYPEVERSION = 16111
    UA_NS0ID_OPCUA_XMLSCHEMA_UADPDATASETREADERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16112
    UA_NS0ID_OPCUA_XMLSCHEMA_JSONWRITERGROUPMESSAGEDATATYPE = 16113
    UA_NS0ID_OPCUA_XMLSCHEMA_JSONWRITERGROUPMESSAGEDATATYPE_DATATYPEVERSION = 16114
    UA_NS0ID_OPCUA_XMLSCHEMA_JSONWRITERGROUPMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16115
    UA_NS0ID_OPCUA_XMLSCHEMA_JSONDATASETWRITERMESSAGEDATATYPE = 16116
    UA_NS0ID_OPCUA_XMLSCHEMA_JSONDATASETWRITERMESSAGEDATATYPE_DATATYPEVERSION = 16117
    UA_NS0ID_OPCUA_XMLSCHEMA_JSONDATASETWRITERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16118
    UA_NS0ID_OPCUA_XMLSCHEMA_JSONDATASETREADERMESSAGEDATATYPE = 16119
    UA_NS0ID_OPCUA_XMLSCHEMA_JSONDATASETREADERMESSAGEDATATYPE_DATATYPEVERSION = 16120
    UA_NS0ID_OPCUA_XMLSCHEMA_JSONDATASETREADERMESSAGEDATATYPE_DICTIONARYFRAGMENT = 16121
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 16122
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 16123
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 16124
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERWRITERGROUPTRANSPORTDATATYPE = 16125
    UA_NS0ID_ROLEPERMISSIONTYPE_ENCODING_DEFAULTXML = 16126
    UA_NS0ID_OPCUA_XMLSCHEMA_ROLEPERMISSIONTYPE = 16127
    UA_NS0ID_OPCUA_XMLSCHEMA_ROLEPERMISSIONTYPE_DATATYPEVERSION = 16128
    UA_NS0ID_OPCUA_XMLSCHEMA_ROLEPERMISSIONTYPE_DICTIONARYFRAGMENT = 16129
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERWRITERGROUPTRANSPORTDATATYPE_DATATYPEVERSION = 16130
    UA_NS0ID_OPCUA_BINARYSCHEMA_ROLEPERMISSIONTYPE = 16131
    UA_NS0ID_OPCUA_BINARYSCHEMA_ROLEPERMISSIONTYPE_DATATYPEVERSION = 16132
    UA_NS0ID_OPCUA_BINARYSCHEMA_ROLEPERMISSIONTYPE_DICTIONARYFRAGMENT = 16133
    UA_NS0ID_OPCUANAMESPACEMETADATA_DEFAULTROLEPERMISSIONS = 16134
    UA_NS0ID_OPCUANAMESPACEMETADATA_DEFAULTUSERROLEPERMISSIONS = 16135
    UA_NS0ID_OPCUANAMESPACEMETADATA_DEFAULTACCESSRESTRICTIONS = 16136
    UA_NS0ID_NAMESPACEMETADATATYPE_DEFAULTROLEPERMISSIONS = 16137
    UA_NS0ID_NAMESPACEMETADATATYPE_DEFAULTUSERROLEPERMISSIONS = 16138
    UA_NS0ID_NAMESPACEMETADATATYPE_DEFAULTACCESSRESTRICTIONS = 16139
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_DEFAULTROLEPERMISSIONS = 16140
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_DEFAULTUSERROLEPERMISSIONS = 16141
    UA_NS0ID_NAMESPACESTYPE_NAMESPACEIDENTIFIER_PLACEHOLDER_DEFAULTACCESSRESTRICTIONS = 16142
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERWRITERGROUPTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 16143
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERDATASETWRITERTRANSPORTDATATYPE = 16144
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERDATASETWRITERTRANSPORTDATATYPE_DATATYPEVERSION = 16145
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERDATASETWRITERTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 16146
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERDATASETREADERTRANSPORTDATATYPE = 16147
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERDATASETREADERTRANSPORTDATATYPE_DATATYPEVERSION = 16148
    UA_NS0ID_OPCUA_XMLSCHEMA_BROKERDATASETREADERTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 16149
    UA_NS0ID_ENDPOINTTYPE_ENCODING_DEFAULTJSON = 16150
    UA_NS0ID_DATATYPESCHEMAHEADER_ENCODING_DEFAULTJSON = 16151
    UA_NS0ID_PUBLISHEDDATASETDATATYPE_ENCODING_DEFAULTJSON = 16152
    UA_NS0ID_PUBLISHEDDATASETSOURCEDATATYPE_ENCODING_DEFAULTJSON = 16153
    UA_NS0ID_PUBLISHEDDATAITEMSDATATYPE_ENCODING_DEFAULTJSON = 16154
    UA_NS0ID_PUBLISHEDEVENTSDATATYPE_ENCODING_DEFAULTJSON = 16155
    UA_NS0ID_DATASETWRITERDATATYPE_ENCODING_DEFAULTJSON = 16156
    UA_NS0ID_DATASETWRITERTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 16157
    UA_NS0ID_DATASETWRITERMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16158
    UA_NS0ID_PUBSUBGROUPDATATYPE_ENCODING_DEFAULTJSON = 16159
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 16160
    UA_NS0ID_WRITERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 16161
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_IDENTITIES = 16162
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_APPLICATIONS = 16163
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_ENDPOINTS = 16164
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_ADDAPPLICATION = 16165
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_ADDAPPLICATION_INPUTARGUMENTS = 16166
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_REMOVEAPPLICATION = 16167
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_REMOVEAPPLICATION_INPUTARGUMENTS = 16168
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_ADDENDPOINT = 16169
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_ADDENDPOINT_INPUTARGUMENTS = 16170
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_REMOVEENDPOINT = 16171
    UA_NS0ID_ROLESETTYPE_ROLENAME_PLACEHOLDER_REMOVEENDPOINT_INPUTARGUMENTS = 16172
    UA_NS0ID_ROLETYPE_IDENTITIES = 16173
    UA_NS0ID_ROLETYPE_APPLICATIONS = 16174
    UA_NS0ID_ROLETYPE_ENDPOINTS = 16175
    UA_NS0ID_ROLETYPE_ADDAPPLICATION = 16176
    UA_NS0ID_ROLETYPE_ADDAPPLICATION_INPUTARGUMENTS = 16177
    UA_NS0ID_ROLETYPE_REMOVEAPPLICATION = 16178
    UA_NS0ID_ROLETYPE_REMOVEAPPLICATION_INPUTARGUMENTS = 16179
    UA_NS0ID_ROLETYPE_ADDENDPOINT = 16180
    UA_NS0ID_ROLETYPE_ADDENDPOINT_INPUTARGUMENTS = 16181
    UA_NS0ID_ROLETYPE_REMOVEENDPOINT = 16182
    UA_NS0ID_ROLETYPE_REMOVEENDPOINT_INPUTARGUMENTS = 16183
    UA_NS0ID_ADDAPPLICATIONMETHODTYPE = 16184
    UA_NS0ID_ADDAPPLICATIONMETHODTYPE_INPUTARGUMENTS = 16185
    UA_NS0ID_REMOVEAPPLICATIONMETHODTYPE = 16186
    UA_NS0ID_REMOVEAPPLICATIONMETHODTYPE_INPUTARGUMENTS = 16187
    UA_NS0ID_ADDENDPOINTMETHODTYPE = 16188
    UA_NS0ID_ADDENDPOINTMETHODTYPE_INPUTARGUMENTS = 16189
    UA_NS0ID_REMOVEENDPOINTMETHODTYPE = 16190
    UA_NS0ID_REMOVEENDPOINTMETHODTYPE_INPUTARGUMENTS = 16191
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_IDENTITIES = 16192
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_APPLICATIONS = 16193
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_ENDPOINTS = 16194
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_ADDAPPLICATION = 16195
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_ADDAPPLICATION_INPUTARGUMENTS = 16196
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_REMOVEAPPLICATION = 16197
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_REMOVEAPPLICATION_INPUTARGUMENTS = 16198
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_ADDENDPOINT = 16199
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_ADDENDPOINT_INPUTARGUMENTS = 16200
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_REMOVEENDPOINT = 16201
    UA_NS0ID_WELLKNOWNROLE_ANONYMOUS_REMOVEENDPOINT_INPUTARGUMENTS = 16202
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_IDENTITIES = 16203
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_APPLICATIONS = 16204
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_ENDPOINTS = 16205
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_ADDAPPLICATION = 16206
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_ADDAPPLICATION_INPUTARGUMENTS = 16207
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_REMOVEAPPLICATION = 16208
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_REMOVEAPPLICATION_INPUTARGUMENTS = 16209
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_ADDENDPOINT = 16210
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_ADDENDPOINT_INPUTARGUMENTS = 16211
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_REMOVEENDPOINT = 16212
    UA_NS0ID_WELLKNOWNROLE_AUTHENTICATEDUSER_REMOVEENDPOINT_INPUTARGUMENTS = 16213
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_IDENTITIES = 16214
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_APPLICATIONS = 16215
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_ENDPOINTS = 16216
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_ADDAPPLICATION = 16217
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_ADDAPPLICATION_INPUTARGUMENTS = 16218
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_REMOVEAPPLICATION = 16219
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_REMOVEAPPLICATION_INPUTARGUMENTS = 16220
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_ADDENDPOINT = 16221
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_ADDENDPOINT_INPUTARGUMENTS = 16222
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_REMOVEENDPOINT = 16223
    UA_NS0ID_WELLKNOWNROLE_OBSERVER_REMOVEENDPOINT_INPUTARGUMENTS = 16224
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_IDENTITIES = 16225
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_APPLICATIONS = 16226
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_ENDPOINTS = 16227
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_ADDAPPLICATION = 16228
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_ADDAPPLICATION_INPUTARGUMENTS = 16229
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_REMOVEAPPLICATION = 16230
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_REMOVEAPPLICATION_INPUTARGUMENTS = 16231
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_ADDENDPOINT = 16232
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_ADDENDPOINT_INPUTARGUMENTS = 16233
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_REMOVEENDPOINT = 16234
    UA_NS0ID_WELLKNOWNROLE_OPERATOR_REMOVEENDPOINT_INPUTARGUMENTS = 16235
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_IDENTITIES = 16236
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_APPLICATIONS = 16237
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_ENDPOINTS = 16238
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_ADDAPPLICATION = 16239
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_ADDAPPLICATION_INPUTARGUMENTS = 16240
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_REMOVEAPPLICATION = 16241
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_REMOVEAPPLICATION_INPUTARGUMENTS = 16242
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_ADDENDPOINT = 16243
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_ADDENDPOINT_INPUTARGUMENTS = 16244
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_REMOVEENDPOINT = 16245
    UA_NS0ID_WELLKNOWNROLE_ENGINEER_REMOVEENDPOINT_INPUTARGUMENTS = 16246
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_IDENTITIES = 16247
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_APPLICATIONS = 16248
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_ENDPOINTS = 16249
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_ADDAPPLICATION = 16250
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_ADDAPPLICATION_INPUTARGUMENTS = 16251
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_REMOVEAPPLICATION = 16252
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_REMOVEAPPLICATION_INPUTARGUMENTS = 16253
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_ADDENDPOINT = 16254
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_ADDENDPOINT_INPUTARGUMENTS = 16255
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_REMOVEENDPOINT = 16256
    UA_NS0ID_WELLKNOWNROLE_SUPERVISOR_REMOVEENDPOINT_INPUTARGUMENTS = 16257
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_IDENTITIES = 16258
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_APPLICATIONS = 16259
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_ENDPOINTS = 16260
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_ADDAPPLICATION = 16261
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_ADDAPPLICATION_INPUTARGUMENTS = 16262
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_REMOVEAPPLICATION = 16263
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_REMOVEAPPLICATION_INPUTARGUMENTS = 16264
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_ADDENDPOINT = 16265
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_ADDENDPOINT_INPUTARGUMENTS = 16266
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_REMOVEENDPOINT = 16267
    UA_NS0ID_WELLKNOWNROLE_SECURITYADMIN_REMOVEENDPOINT_INPUTARGUMENTS = 16268
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_IDENTITIES = 16269
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_APPLICATIONS = 16270
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_ENDPOINTS = 16271
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_ADDAPPLICATION = 16272
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_ADDAPPLICATION_INPUTARGUMENTS = 16273
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_REMOVEAPPLICATION = 16274
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_REMOVEAPPLICATION_INPUTARGUMENTS = 16275
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_ADDENDPOINT = 16276
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_ADDENDPOINT_INPUTARGUMENTS = 16277
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_REMOVEENDPOINT = 16278
    UA_NS0ID_WELLKNOWNROLE_CONFIGUREADMIN_REMOVEENDPOINT_INPUTARGUMENTS = 16279
    UA_NS0ID_WRITERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16280
    UA_NS0ID_PUBSUBCONNECTIONDATATYPE_ENCODING_DEFAULTJSON = 16281
    UA_NS0ID_CONNECTIONTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 16282
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 16283
    UA_NS0ID_READERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 16284
    UA_NS0ID_READERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16285
    UA_NS0ID_DATASETREADERDATATYPE_ENCODING_DEFAULTJSON = 16286
    UA_NS0ID_DATASETREADERTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 16287
    UA_NS0ID_DATASETREADERMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16288
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_ROLESET = 16289
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_ROLESET_ADDROLE = 16290
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_ROLESET_ADDROLE_INPUTARGUMENTS = 16291
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_ROLESET_ADDROLE_OUTPUTARGUMENTS = 16292
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_ROLESET_REMOVEROLE = 16293
    UA_NS0ID_SERVERTYPE_SERVERCAPABILITIES_ROLESET_REMOVEROLE_INPUTARGUMENTS = 16294
    UA_NS0ID_SERVERCAPABILITIESTYPE_ROLESET = 16295
    UA_NS0ID_SERVERCAPABILITIESTYPE_ROLESET_ADDROLE = 16296
    UA_NS0ID_SERVERCAPABILITIESTYPE_ROLESET_ADDROLE_INPUTARGUMENTS = 16297
    UA_NS0ID_SERVERCAPABILITIESTYPE_ROLESET_ADDROLE_OUTPUTARGUMENTS = 16298
    UA_NS0ID_SERVERCAPABILITIESTYPE_ROLESET_REMOVEROLE = 16299
    UA_NS0ID_SERVERCAPABILITIESTYPE_ROLESET_REMOVEROLE_INPUTARGUMENTS = 16300
    UA_NS0ID_SERVER_SERVERCAPABILITIES_ROLESET_ADDROLE = 16301
    UA_NS0ID_SERVER_SERVERCAPABILITIES_ROLESET_ADDROLE_INPUTARGUMENTS = 16302
    UA_NS0ID_SERVER_SERVERCAPABILITIES_ROLESET_ADDROLE_OUTPUTARGUMENTS = 16303
    UA_NS0ID_SERVER_SERVERCAPABILITIES_ROLESET_REMOVEROLE = 16304
    UA_NS0ID_SERVER_SERVERCAPABILITIES_ROLESET_REMOVEROLE_INPUTARGUMENTS = 16305
    UA_NS0ID_AUDIODATATYPE = 16307
    UA_NS0ID_SUBSCRIBEDDATASETDATATYPE_ENCODING_DEFAULTJSON = 16308
    UA_NS0ID_SELECTIONLISTTYPE = 16309
    UA_NS0ID_TARGETVARIABLESDATATYPE_ENCODING_DEFAULTJSON = 16310
    UA_NS0ID_SUBSCRIBEDDATASETMIRRORDATATYPE_ENCODING_DEFAULTJSON = 16311
    UA_NS0ID_SELECTIONLISTTYPE_RESTRICTTOLIST = 16312
    UA_NS0ID_ADDITIONALPARAMETERSTYPE = 16313
    UA_NS0ID_FILESYSTEM = 16314
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER = 16315
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_CREATEDIRECTORY = 16316
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_CREATEDIRECTORY_INPUTARGUMENTS = 16317
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_CREATEDIRECTORY_OUTPUTARGUMENTS = 16318
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_CREATEFILE = 16319
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_CREATEFILE_INPUTARGUMENTS = 16320
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_CREATEFILE_OUTPUTARGUMENTS = 16321
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 16322
    UA_NS0ID_UADPWRITERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16323
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_MOVEORCOPY = 16324
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_MOVEORCOPY_INPUTARGUMENTS = 16325
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_MOVEORCOPY_OUTPUTARGUMENTS = 16326
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER = 16327
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_SIZE = 16328
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_WRITABLE = 16329
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_USERWRITABLE = 16330
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_OPENCOUNT = 16331
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_MIMETYPE = 16332
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_OPEN = 16333
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_OPEN_INPUTARGUMENTS = 16334
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_OPEN_OUTPUTARGUMENTS = 16335
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_CLOSE = 16336
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_CLOSE_INPUTARGUMENTS = 16337
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_READ = 16338
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_READ_INPUTARGUMENTS = 16339
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_READ_OUTPUTARGUMENTS = 16340
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_WRITE = 16341
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_WRITE_INPUTARGUMENTS = 16342
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_GETPOSITION = 16343
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_GETPOSITION_INPUTARGUMENTS = 16344
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_GETPOSITION_OUTPUTARGUMENTS = 16345
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_SETPOSITION = 16346
    UA_NS0ID_FILESYSTEM_FILENAME_PLACEHOLDER_SETPOSITION_INPUTARGUMENTS = 16347
    UA_NS0ID_FILESYSTEM_CREATEDIRECTORY = 16348
    UA_NS0ID_FILESYSTEM_CREATEDIRECTORY_INPUTARGUMENTS = 16349
    UA_NS0ID_FILESYSTEM_CREATEDIRECTORY_OUTPUTARGUMENTS = 16350
    UA_NS0ID_FILESYSTEM_CREATEFILE = 16351
    UA_NS0ID_FILESYSTEM_CREATEFILE_INPUTARGUMENTS = 16352
    UA_NS0ID_FILESYSTEM_CREATEFILE_OUTPUTARGUMENTS = 16353
    UA_NS0ID_FILESYSTEM_DELETEFILESYSTEMOBJECT = 16354
    UA_NS0ID_FILESYSTEM_DELETEFILESYSTEMOBJECT_INPUTARGUMENTS = 16355
    UA_NS0ID_FILESYSTEM_MOVEORCOPY = 16356
    UA_NS0ID_FILESYSTEM_MOVEORCOPY_INPUTARGUMENTS = 16357
    UA_NS0ID_FILESYSTEM_MOVEORCOPY_OUTPUTARGUMENTS = 16358
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_GENERATEFILEFORWRITE_INPUTARGUMENTS = 16359
    UA_NS0ID_GENERATEFILEFORWRITEMETHODTYPE_INPUTARGUMENTS = 16360
    UA_NS0ID_HASALARMSUPPRESSIONGROUP = 16361
    UA_NS0ID_ALARMGROUPMEMBER = 16362
    UA_NS0ID_CONDITIONTYPE_CONDITIONSUBCLASSID = 16363
    UA_NS0ID_CONDITIONTYPE_CONDITIONSUBCLASSNAME = 16364
    UA_NS0ID_DIALOGCONDITIONTYPE_CONDITIONSUBCLASSID = 16365
    UA_NS0ID_DIALOGCONDITIONTYPE_CONDITIONSUBCLASSNAME = 16366
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONDITIONSUBCLASSID = 16367
    UA_NS0ID_ACKNOWLEDGEABLECONDITIONTYPE_CONDITIONSUBCLASSNAME = 16368
    UA_NS0ID_ALARMCONDITIONTYPE_CONDITIONSUBCLASSID = 16369
    UA_NS0ID_ALARMCONDITIONTYPE_CONDITIONSUBCLASSNAME = 16370
    UA_NS0ID_ALARMCONDITIONTYPE_OUTOFSERVICESTATE = 16371
    UA_NS0ID_ALARMCONDITIONTYPE_OUTOFSERVICESTATE_ID = 16372
    UA_NS0ID_ALARMCONDITIONTYPE_OUTOFSERVICESTATE_NAME = 16373
    UA_NS0ID_ALARMCONDITIONTYPE_OUTOFSERVICESTATE_NUMBER = 16374
    UA_NS0ID_ALARMCONDITIONTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16375
    UA_NS0ID_ALARMCONDITIONTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16376
    UA_NS0ID_ALARMCONDITIONTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16377
    UA_NS0ID_ALARMCONDITIONTYPE_OUTOFSERVICESTATE_TRUESTATE = 16378
    UA_NS0ID_ALARMCONDITIONTYPE_OUTOFSERVICESTATE_FALSESTATE = 16379
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCESTATE = 16380
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCESTATE_ID = 16381
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCESTATE_NAME = 16382
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCESTATE_NUMBER = 16383
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16384
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCESTATE_TRANSITIONTIME = 16385
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16386
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCESTATE_TRUESTATE = 16387
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCESTATE_FALSESTATE = 16388
    UA_NS0ID_ALARMCONDITIONTYPE_AUDIBLEENABLED = 16389
    UA_NS0ID_ALARMCONDITIONTYPE_AUDIBLESOUND = 16390
    UA_NS0ID_UADPDATASETWRITERMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16391
    UA_NS0ID_UADPDATASETREADERMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16392
    UA_NS0ID_JSONWRITERGROUPMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16393
    UA_NS0ID_JSONDATASETWRITERMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16394
    UA_NS0ID_ALARMCONDITIONTYPE_ONDELAY = 16395
    UA_NS0ID_ALARMCONDITIONTYPE_OFFDELAY = 16396
    UA_NS0ID_ALARMCONDITIONTYPE_FIRSTINGROUPFLAG = 16397
    UA_NS0ID_ALARMCONDITIONTYPE_FIRSTINGROUP = 16398
    UA_NS0ID_ALARMCONDITIONTYPE_ALARMGROUP_PLACEHOLDER = 16399
    UA_NS0ID_ALARMCONDITIONTYPE_REALARMTIME = 16400
    UA_NS0ID_ALARMCONDITIONTYPE_REALARMREPEATCOUNT = 16401
    UA_NS0ID_ALARMCONDITIONTYPE_SILENCE = 16402
    UA_NS0ID_ALARMCONDITIONTYPE_SUPPRESS = 16403
    UA_NS0ID_JSONDATASETREADERMESSAGEDATATYPE_ENCODING_DEFAULTJSON = 16404
    UA_NS0ID_ALARMGROUPTYPE = 16405
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER = 16406
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_EVENTID = 16407
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_EVENTTYPE = 16408
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SOURCENODE = 16409
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SOURCENAME = 16410
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_TIME = 16411
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_RECEIVETIME = 16412
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LOCALTIME = 16413
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_MESSAGE = 16414
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SEVERITY = 16415
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONDITIONCLASSID = 16416
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONDITIONCLASSNAME = 16417
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONDITIONSUBCLASSID = 16418
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONDITIONSUBCLASSNAME = 16419
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONDITIONNAME = 16420
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_BRANCHID = 16421
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_RETAIN = 16422
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLEDSTATE = 16423
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLEDSTATE_ID = 16424
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLEDSTATE_NAME = 16425
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLEDSTATE_NUMBER = 16426
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 16427
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLEDSTATE_TRANSITIONTIME = 16428
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 16429
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLEDSTATE_TRUESTATE = 16430
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLEDSTATE_FALSESTATE = 16431
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_QUALITY = 16432
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_QUALITY_SOURCETIMESTAMP = 16433
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LASTSEVERITY = 16434
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LASTSEVERITY_SOURCETIMESTAMP = 16435
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_COMMENT = 16436
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_COMMENT_SOURCETIMESTAMP = 16437
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CLIENTUSERID = 16438
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_DISABLE = 16439
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ENABLE = 16440
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ADDCOMMENT = 16441
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ADDCOMMENT_INPUTARGUMENTS = 16442
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKEDSTATE = 16443
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKEDSTATE_ID = 16444
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKEDSTATE_NAME = 16445
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKEDSTATE_NUMBER = 16446
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 16447
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKEDSTATE_TRANSITIONTIME = 16448
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 16449
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKEDSTATE_TRUESTATE = 16450
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKEDSTATE_FALSESTATE = 16451
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRMEDSTATE = 16452
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRMEDSTATE_ID = 16453
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRMEDSTATE_NAME = 16454
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRMEDSTATE_NUMBER = 16455
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 16456
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRMEDSTATE_TRANSITIONTIME = 16457
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 16458
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRMEDSTATE_TRUESTATE = 16459
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRMEDSTATE_FALSESTATE = 16460
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKNOWLEDGE = 16461
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACKNOWLEDGE_INPUTARGUMENTS = 16462
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRM = 16463
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_CONFIRM_INPUTARGUMENTS = 16464
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACTIVESTATE = 16465
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACTIVESTATE_ID = 16466
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACTIVESTATE_NAME = 16467
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACTIVESTATE_NUMBER = 16468
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 16469
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACTIVESTATE_TRANSITIONTIME = 16470
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 16471
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACTIVESTATE_TRUESTATE = 16472
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ACTIVESTATE_FALSESTATE = 16473
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_INPUTNODE = 16474
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDSTATE = 16475
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDSTATE_ID = 16476
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDSTATE_NAME = 16477
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDSTATE_NUMBER = 16478
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 16479
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDSTATE_TRANSITIONTIME = 16480
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 16481
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDSTATE_TRUESTATE = 16482
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDSTATE_FALSESTATE = 16483
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OUTOFSERVICESTATE = 16484
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OUTOFSERVICESTATE_ID = 16485
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OUTOFSERVICESTATE_NAME = 16486
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OUTOFSERVICESTATE_NUMBER = 16487
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16488
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OUTOFSERVICESTATE_TRANSITIONTIME = 16489
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16490
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OUTOFSERVICESTATE_TRUESTATE = 16491
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OUTOFSERVICESTATE_FALSESTATE = 16492
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCESTATE = 16493
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCESTATE_ID = 16494
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCESTATE_NAME = 16495
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCESTATE_NUMBER = 16496
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16497
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCESTATE_TRANSITIONTIME = 16498
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16499
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCESTATE_TRUESTATE = 16500
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCESTATE_FALSESTATE = 16501
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE = 16502
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_CURRENTSTATE = 16503
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_CURRENTSTATE_ID = 16504
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_CURRENTSTATE_NAME = 16505
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_CURRENTSTATE_NUMBER = 16506
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 16507
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_LASTTRANSITION = 16508
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_LASTTRANSITION_ID = 16509
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_LASTTRANSITION_NAME = 16510
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_LASTTRANSITION_NUMBER = 16511
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 16512
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 16513
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_UNSHELVETIME = 16514
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_UNSHELVE = 16515
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_ONESHOTSHELVE = 16516
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_TIMEDSHELVE = 16517
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 16518
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESSEDORSHELVED = 16519
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_MAXTIMESHELVED = 16520
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_AUDIBLEENABLED = 16521
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_AUDIBLESOUND = 16522
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 16523
    UA_NS0ID_BROKERWRITERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 16524
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 16525
    UA_NS0ID_BROKERDATASETREADERTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 16526
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_ONDELAY = 16527
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_OFFDELAY = 16528
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_FIRSTINGROUPFLAG = 16529
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_FIRSTINGROUP = 16530
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_REALARMTIME = 16531
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_REALARMREPEATCOUNT = 16532
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SILENCE = 16533
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SUPPRESS = 16534
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDWRITERGROUP = 16535
    UA_NS0ID_LIMITALARMTYPE_CONDITIONSUBCLASSID = 16536
    UA_NS0ID_LIMITALARMTYPE_CONDITIONSUBCLASSNAME = 16537
    UA_NS0ID_LIMITALARMTYPE_OUTOFSERVICESTATE = 16538
    UA_NS0ID_LIMITALARMTYPE_OUTOFSERVICESTATE_ID = 16539
    UA_NS0ID_LIMITALARMTYPE_OUTOFSERVICESTATE_NAME = 16540
    UA_NS0ID_LIMITALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16541
    UA_NS0ID_LIMITALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16542
    UA_NS0ID_LIMITALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16543
    UA_NS0ID_LIMITALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16544
    UA_NS0ID_LIMITALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16545
    UA_NS0ID_LIMITALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16546
    UA_NS0ID_LIMITALARMTYPE_SILENCESTATE = 16547
    UA_NS0ID_LIMITALARMTYPE_SILENCESTATE_ID = 16548
    UA_NS0ID_LIMITALARMTYPE_SILENCESTATE_NAME = 16549
    UA_NS0ID_LIMITALARMTYPE_SILENCESTATE_NUMBER = 16550
    UA_NS0ID_LIMITALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16551
    UA_NS0ID_LIMITALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16552
    UA_NS0ID_LIMITALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16553
    UA_NS0ID_LIMITALARMTYPE_SILENCESTATE_TRUESTATE = 16554
    UA_NS0ID_LIMITALARMTYPE_SILENCESTATE_FALSESTATE = 16555
    UA_NS0ID_LIMITALARMTYPE_AUDIBLEENABLED = 16556
    UA_NS0ID_LIMITALARMTYPE_AUDIBLESOUND = 16557
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDWRITERGROUP_INPUTARGUMENTS = 16558
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDWRITERGROUP_OUTPUTARGUMENTS = 16559
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDREADERGROUP = 16560
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDREADERGROUP_INPUTARGUMENTS = 16561
    UA_NS0ID_LIMITALARMTYPE_ONDELAY = 16562
    UA_NS0ID_LIMITALARMTYPE_OFFDELAY = 16563
    UA_NS0ID_LIMITALARMTYPE_FIRSTINGROUPFLAG = 16564
    UA_NS0ID_LIMITALARMTYPE_FIRSTINGROUP = 16565
    UA_NS0ID_LIMITALARMTYPE_ALARMGROUP_PLACEHOLDER = 16566
    UA_NS0ID_LIMITALARMTYPE_REALARMTIME = 16567
    UA_NS0ID_LIMITALARMTYPE_REALARMREPEATCOUNT = 16568
    UA_NS0ID_LIMITALARMTYPE_SILENCE = 16569
    UA_NS0ID_LIMITALARMTYPE_SUPPRESS = 16570
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDREADERGROUP_OUTPUTARGUMENTS = 16571
    UA_NS0ID_LIMITALARMTYPE_BASEHIGHHIGHLIMIT = 16572
    UA_NS0ID_LIMITALARMTYPE_BASEHIGHLIMIT = 16573
    UA_NS0ID_LIMITALARMTYPE_BASELOWLIMIT = 16574
    UA_NS0ID_LIMITALARMTYPE_BASELOWLOWLIMIT = 16575
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONDITIONSUBCLASSID = 16576
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_CONDITIONSUBCLASSNAME = 16577
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE = 16578
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_ID = 16579
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_NAME = 16580
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16581
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16582
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16583
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16584
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16585
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16586
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCESTATE = 16587
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCESTATE_ID = 16588
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCESTATE_NAME = 16589
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCESTATE_NUMBER = 16590
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16591
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16592
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16593
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCESTATE_TRUESTATE = 16594
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCESTATE_FALSESTATE = 16595
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_AUDIBLEENABLED = 16596
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_AUDIBLESOUND = 16597
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_ADDCONNECTION = 16598
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_ADDCONNECTION_INPUTARGUMENTS = 16599
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_ADDCONNECTION_OUTPUTARGUMENTS = 16600
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMSTEMPLATE = 16601
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ONDELAY = 16602
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_OFFDELAY = 16603
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_FIRSTINGROUPFLAG = 16604
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_FIRSTINGROUP = 16605
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_ALARMGROUP_PLACEHOLDER = 16606
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_REALARMTIME = 16607
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_REALARMREPEATCOUNT = 16608
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SILENCE = 16609
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SUPPRESS = 16610
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMSTEMPLATE_INPUTARGUMENTS = 16611
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_BASEHIGHHIGHLIMIT = 16612
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_BASEHIGHLIMIT = 16613
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_BASELOWLIMIT = 16614
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_BASELOWLOWLIMIT = 16615
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONDITIONSUBCLASSID = 16616
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_CONDITIONSUBCLASSNAME = 16617
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE = 16618
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_ID = 16619
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_NAME = 16620
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16621
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16622
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16623
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16624
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16625
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16626
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCESTATE = 16627
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCESTATE_ID = 16628
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCESTATE_NAME = 16629
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCESTATE_NUMBER = 16630
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16631
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16632
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16633
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCESTATE_TRUESTATE = 16634
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCESTATE_FALSESTATE = 16635
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_AUDIBLEENABLED = 16636
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_AUDIBLESOUND = 16637
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMSTEMPLATE_OUTPUTARGUMENTS = 16638
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTSTEMPLATE = 16639
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTSTEMPLATE_INPUTARGUMENTS = 16640
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTSTEMPLATE_OUTPUTARGUMENTS = 16641
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ONDELAY = 16642
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_OFFDELAY = 16643
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_FIRSTINGROUPFLAG = 16644
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_FIRSTINGROUP = 16645
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_ALARMGROUP_PLACEHOLDER = 16646
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_REALARMTIME = 16647
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_REALARMREPEATCOUNT = 16648
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SILENCE = 16649
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SUPPRESS = 16650
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDDATASETFOLDER = 16651
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_BASEHIGHHIGHLIMIT = 16652
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_BASEHIGHLIMIT = 16653
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_BASELOWLIMIT = 16654
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_BASELOWLOWLIMIT = 16655
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONDITIONSUBCLASSID = 16656
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_CONDITIONSUBCLASSNAME = 16657
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE = 16658
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_ID = 16659
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_NAME = 16660
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16661
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16662
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16663
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16664
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16665
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16666
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCESTATE = 16667
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCESTATE_ID = 16668
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCESTATE_NAME = 16669
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCESTATE_NUMBER = 16670
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16671
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16672
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16673
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCESTATE_TRUESTATE = 16674
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCESTATE_FALSESTATE = 16675
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_AUDIBLEENABLED = 16676
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_AUDIBLESOUND = 16677
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDDATASETFOLDER_INPUTARGUMENTS = 16678
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_ADDDATASETFOLDER_OUTPUTARGUMENTS = 16679
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_REMOVEDATASETFOLDER = 16680
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_PUBLISHEDDATASETS_REMOVEDATASETFOLDER_INPUTARGUMENTS = 16681
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ONDELAY = 16682
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_OFFDELAY = 16683
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_FIRSTINGROUPFLAG = 16684
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_FIRSTINGROUP = 16685
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_ALARMGROUP_PLACEHOLDER = 16686
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_REALARMTIME = 16687
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_REALARMREPEATCOUNT = 16688
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SILENCE = 16689
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SUPPRESS = 16690
    UA_NS0ID_ADDCONNECTIONMETHODTYPE = 16691
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_BASEHIGHHIGHLIMIT = 16692
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_BASEHIGHLIMIT = 16693
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_BASELOWLIMIT = 16694
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_BASELOWLOWLIMIT = 16695
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONDITIONSUBCLASSID = 16696
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_CONDITIONSUBCLASSNAME = 16697
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE = 16698
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_ID = 16699
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_NAME = 16700
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16701
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16702
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16703
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16704
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16705
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16706
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCESTATE = 16707
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCESTATE_ID = 16708
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCESTATE_NAME = 16709
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCESTATE_NUMBER = 16710
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16711
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16712
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16713
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCESTATE_TRUESTATE = 16714
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCESTATE_FALSESTATE = 16715
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_AUDIBLEENABLED = 16716
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_AUDIBLESOUND = 16717
    UA_NS0ID_ADDCONNECTIONMETHODTYPE_INPUTARGUMENTS = 16718
    UA_NS0ID_ADDCONNECTIONMETHODTYPE_OUTPUTARGUMENTS = 16719
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETWRITERID = 16720
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETFIELDCONTENTMASK = 16721
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ONDELAY = 16722
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_OFFDELAY = 16723
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_FIRSTINGROUPFLAG = 16724
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_FIRSTINGROUP = 16725
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_ALARMGROUP_PLACEHOLDER = 16726
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_REALARMTIME = 16727
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_REALARMREPEATCOUNT = 16728
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SILENCE = 16729
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SUPPRESS = 16730
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_KEYFRAMECOUNT = 16731
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_BASEHIGHHIGHLIMIT = 16732
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_BASEHIGHLIMIT = 16733
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_BASELOWLIMIT = 16734
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_BASELOWLOWLIMIT = 16735
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONDITIONSUBCLASSID = 16736
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_CONDITIONSUBCLASSNAME = 16737
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE = 16738
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_ID = 16739
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_NAME = 16740
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16741
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16742
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16743
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16744
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16745
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16746
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE = 16747
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_ID = 16748
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_NAME = 16749
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_NUMBER = 16750
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16751
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16752
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16753
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_TRUESTATE = 16754
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_FALSESTATE = 16755
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_AUDIBLEENABLED = 16756
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_AUDIBLESOUND = 16757
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_MESSAGESETTINGS = 16758
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETCLASSID = 16759
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETWRITERID = 16760
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETFIELDCONTENTMASK = 16761
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ONDELAY = 16762
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_OFFDELAY = 16763
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_FIRSTINGROUPFLAG = 16764
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_FIRSTINGROUP = 16765
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_ALARMGROUP_PLACEHOLDER = 16766
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_REALARMTIME = 16767
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_REALARMREPEATCOUNT = 16768
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SILENCE = 16769
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SUPPRESS = 16770
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_KEYFRAMECOUNT = 16771
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_BASEHIGHHIGHLIMIT = 16772
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_BASEHIGHLIMIT = 16773
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_BASELOWLIMIT = 16774
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_BASELOWLOWLIMIT = 16775
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_BASESETPOINTNODE = 16776
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONDITIONSUBCLASSID = 16777
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_CONDITIONSUBCLASSNAME = 16778
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE = 16779
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_ID = 16780
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_NAME = 16781
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16782
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16783
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16784
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16785
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16786
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16787
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE = 16788
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_ID = 16789
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_NAME = 16790
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_NUMBER = 16791
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16792
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16793
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16794
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_TRUESTATE = 16795
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCESTATE_FALSESTATE = 16796
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_AUDIBLEENABLED = 16797
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_AUDIBLESOUND = 16798
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_MESSAGESETTINGS = 16799
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETCLASSID = 16800
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETWRITERID = 16801
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETFIELDCONTENTMASK = 16802
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ONDELAY = 16803
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_OFFDELAY = 16804
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_FIRSTINGROUPFLAG = 16805
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_FIRSTINGROUP = 16806
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_ALARMGROUP_PLACEHOLDER = 16807
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_REALARMTIME = 16808
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_REALARMREPEATCOUNT = 16809
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SILENCE = 16810
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SUPPRESS = 16811
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_KEYFRAMECOUNT = 16812
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_BASEHIGHHIGHLIMIT = 16813
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_BASEHIGHLIMIT = 16814
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_BASELOWLIMIT = 16815
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_BASELOWLOWLIMIT = 16816
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_BASESETPOINTNODE = 16817
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONSUBCLASSID = 16818
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONSUBCLASSNAME = 16819
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE = 16820
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_ID = 16821
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_NAME = 16822
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16823
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16824
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16825
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16826
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16827
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16828
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE = 16829
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_ID = 16830
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_NAME = 16831
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_NUMBER = 16832
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16833
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16834
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16835
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_TRUESTATE = 16836
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_FALSESTATE = 16837
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLEENABLED = 16838
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLESOUND = 16839
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_MESSAGESETTINGS = 16840
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETCLASSID = 16841
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDDATAITEMSTEMPLATE = 16842
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDDATAITEMSTEMPLATE_INPUTARGUMENTS = 16843
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ONDELAY = 16844
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_OFFDELAY = 16845
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_FIRSTINGROUPFLAG = 16846
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_FIRSTINGROUP = 16847
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ALARMGROUP_PLACEHOLDER = 16848
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_REALARMTIME = 16849
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_REALARMREPEATCOUNT = 16850
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SILENCE = 16851
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESS = 16852
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDDATAITEMSTEMPLATE_OUTPUTARGUMENTS = 16853
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_BASEHIGHHIGHLIMIT = 16854
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_BASEHIGHLIMIT = 16855
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_BASELOWLIMIT = 16856
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_BASELOWLOWLIMIT = 16857
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_ENGINEERINGUNITS = 16858
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONSUBCLASSID = 16859
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_CONDITIONSUBCLASSNAME = 16860
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE = 16861
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_ID = 16862
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_NAME = 16863
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16864
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16865
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16866
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16867
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16868
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16869
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE = 16870
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_ID = 16871
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_NAME = 16872
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_NUMBER = 16873
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16874
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16875
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16876
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_TRUESTATE = 16877
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCESTATE_FALSESTATE = 16878
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLEENABLED = 16879
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLESOUND = 16880
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDEVENTSTEMPLATE = 16881
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDEVENTSTEMPLATE_INPUTARGUMENTS = 16882
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDPUBLISHEDEVENTSTEMPLATE_OUTPUTARGUMENTS = 16883
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDDATASETFOLDER = 16884
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ONDELAY = 16885
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_OFFDELAY = 16886
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_FIRSTINGROUPFLAG = 16887
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_FIRSTINGROUP = 16888
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ALARMGROUP_PLACEHOLDER = 16889
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_REALARMTIME = 16890
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_REALARMREPEATCOUNT = 16891
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SILENCE = 16892
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SUPPRESS = 16893
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDDATASETFOLDER_INPUTARGUMENTS = 16894
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_BASEHIGHHIGHLIMIT = 16895
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_BASEHIGHLIMIT = 16896
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_BASELOWLIMIT = 16897
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_BASELOWLOWLIMIT = 16898
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_ENGINEERINGUNITS = 16899
    UA_NS0ID_DISCRETEALARMTYPE_CONDITIONSUBCLASSID = 16900
    UA_NS0ID_DISCRETEALARMTYPE_CONDITIONSUBCLASSNAME = 16901
    UA_NS0ID_DISCRETEALARMTYPE_OUTOFSERVICESTATE = 16902
    UA_NS0ID_DISCRETEALARMTYPE_OUTOFSERVICESTATE_ID = 16903
    UA_NS0ID_DISCRETEALARMTYPE_OUTOFSERVICESTATE_NAME = 16904
    UA_NS0ID_DISCRETEALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16905
    UA_NS0ID_DISCRETEALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16906
    UA_NS0ID_DISCRETEALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16907
    UA_NS0ID_DISCRETEALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16908
    UA_NS0ID_DISCRETEALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16909
    UA_NS0ID_DISCRETEALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16910
    UA_NS0ID_DISCRETEALARMTYPE_SILENCESTATE = 16911
    UA_NS0ID_DISCRETEALARMTYPE_SILENCESTATE_ID = 16912
    UA_NS0ID_DISCRETEALARMTYPE_SILENCESTATE_NAME = 16913
    UA_NS0ID_DISCRETEALARMTYPE_SILENCESTATE_NUMBER = 16914
    UA_NS0ID_DISCRETEALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16915
    UA_NS0ID_DISCRETEALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16916
    UA_NS0ID_DISCRETEALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16917
    UA_NS0ID_DISCRETEALARMTYPE_SILENCESTATE_TRUESTATE = 16918
    UA_NS0ID_DISCRETEALARMTYPE_SILENCESTATE_FALSESTATE = 16919
    UA_NS0ID_DISCRETEALARMTYPE_AUDIBLEENABLED = 16920
    UA_NS0ID_DISCRETEALARMTYPE_AUDIBLESOUND = 16921
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_ADDDATASETFOLDER_OUTPUTARGUMENTS = 16922
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_REMOVEDATASETFOLDER = 16923
    UA_NS0ID_DATASETFOLDERTYPE_DATASETFOLDERNAME_PLACEHOLDER_REMOVEDATASETFOLDER_INPUTARGUMENTS = 16924
    UA_NS0ID_DATASETFOLDERTYPE_PUBLISHEDDATASETNAME_PLACEHOLDER_DATASETCLASSID = 16925
    UA_NS0ID_DISCRETEALARMTYPE_ONDELAY = 16926
    UA_NS0ID_DISCRETEALARMTYPE_OFFDELAY = 16927
    UA_NS0ID_DISCRETEALARMTYPE_FIRSTINGROUPFLAG = 16928
    UA_NS0ID_DISCRETEALARMTYPE_FIRSTINGROUP = 16929
    UA_NS0ID_DISCRETEALARMTYPE_ALARMGROUP_PLACEHOLDER = 16930
    UA_NS0ID_DISCRETEALARMTYPE_REALARMTIME = 16931
    UA_NS0ID_DISCRETEALARMTYPE_REALARMREPEATCOUNT = 16932
    UA_NS0ID_DISCRETEALARMTYPE_SILENCE = 16933
    UA_NS0ID_DISCRETEALARMTYPE_SUPPRESS = 16934
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDDATAITEMSTEMPLATE = 16935
    UA_NS0ID_OFFNORMALALARMTYPE_CONDITIONSUBCLASSID = 16936
    UA_NS0ID_OFFNORMALALARMTYPE_CONDITIONSUBCLASSNAME = 16937
    UA_NS0ID_OFFNORMALALARMTYPE_OUTOFSERVICESTATE = 16938
    UA_NS0ID_OFFNORMALALARMTYPE_OUTOFSERVICESTATE_ID = 16939
    UA_NS0ID_OFFNORMALALARMTYPE_OUTOFSERVICESTATE_NAME = 16940
    UA_NS0ID_OFFNORMALALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16941
    UA_NS0ID_OFFNORMALALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16942
    UA_NS0ID_OFFNORMALALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16943
    UA_NS0ID_OFFNORMALALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16944
    UA_NS0ID_OFFNORMALALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16945
    UA_NS0ID_OFFNORMALALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16946
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCESTATE = 16947
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCESTATE_ID = 16948
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCESTATE_NAME = 16949
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCESTATE_NUMBER = 16950
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16951
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16952
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16953
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCESTATE_TRUESTATE = 16954
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCESTATE_FALSESTATE = 16955
    UA_NS0ID_OFFNORMALALARMTYPE_AUDIBLEENABLED = 16956
    UA_NS0ID_OFFNORMALALARMTYPE_AUDIBLESOUND = 16957
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDDATAITEMSTEMPLATE_INPUTARGUMENTS = 16958
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDDATAITEMSTEMPLATE_OUTPUTARGUMENTS = 16959
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDEVENTSTEMPLATE = 16960
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDEVENTSTEMPLATE_INPUTARGUMENTS = 16961
    UA_NS0ID_OFFNORMALALARMTYPE_ONDELAY = 16962
    UA_NS0ID_OFFNORMALALARMTYPE_OFFDELAY = 16963
    UA_NS0ID_OFFNORMALALARMTYPE_FIRSTINGROUPFLAG = 16964
    UA_NS0ID_OFFNORMALALARMTYPE_FIRSTINGROUP = 16965
    UA_NS0ID_OFFNORMALALARMTYPE_ALARMGROUP_PLACEHOLDER = 16966
    UA_NS0ID_OFFNORMALALARMTYPE_REALARMTIME = 16967
    UA_NS0ID_OFFNORMALALARMTYPE_REALARMREPEATCOUNT = 16968
    UA_NS0ID_OFFNORMALALARMTYPE_SILENCE = 16969
    UA_NS0ID_OFFNORMALALARMTYPE_SUPPRESS = 16970
    UA_NS0ID_DATASETFOLDERTYPE_ADDPUBLISHEDEVENTSTEMPLATE_OUTPUTARGUMENTS = 16971
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONDITIONSUBCLASSID = 16972
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_CONDITIONSUBCLASSNAME = 16973
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OUTOFSERVICESTATE = 16974
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OUTOFSERVICESTATE_ID = 16975
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OUTOFSERVICESTATE_NAME = 16976
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OUTOFSERVICESTATE_NUMBER = 16977
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 16978
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 16979
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 16980
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 16981
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 16982
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCESTATE = 16983
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCESTATE_ID = 16984
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCESTATE_NAME = 16985
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCESTATE_NUMBER = 16986
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 16987
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCESTATE_TRANSITIONTIME = 16988
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 16989
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCESTATE_TRUESTATE = 16990
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCESTATE_FALSESTATE = 16991
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_AUDIBLEENABLED = 16992
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_AUDIBLESOUND = 16993
    UA_NS0ID_DATASETFOLDERTYPE_ADDDATASETFOLDER = 16994
    UA_NS0ID_DATASETFOLDERTYPE_ADDDATASETFOLDER_INPUTARGUMENTS = 16995
    UA_NS0ID_DATASETFOLDERTYPE_ADDDATASETFOLDER_OUTPUTARGUMENTS = 16996
    UA_NS0ID_DATASETFOLDERTYPE_REMOVEDATASETFOLDER = 16997
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ONDELAY = 16998
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_OFFDELAY = 16999
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_FIRSTINGROUPFLAG = 17000
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_FIRSTINGROUP = 17001
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_ALARMGROUP_PLACEHOLDER = 17002
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_REALARMTIME = 17003
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_REALARMREPEATCOUNT = 17004
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SILENCE = 17005
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SUPPRESS = 17006
    UA_NS0ID_DATASETFOLDERTYPE_REMOVEDATASETFOLDER_INPUTARGUMENTS = 17007
    UA_NS0ID_TRIPALARMTYPE_CONDITIONSUBCLASSID = 17008
    UA_NS0ID_TRIPALARMTYPE_CONDITIONSUBCLASSNAME = 17009
    UA_NS0ID_TRIPALARMTYPE_OUTOFSERVICESTATE = 17010
    UA_NS0ID_TRIPALARMTYPE_OUTOFSERVICESTATE_ID = 17011
    UA_NS0ID_TRIPALARMTYPE_OUTOFSERVICESTATE_NAME = 17012
    UA_NS0ID_TRIPALARMTYPE_OUTOFSERVICESTATE_NUMBER = 17013
    UA_NS0ID_TRIPALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 17014
    UA_NS0ID_TRIPALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 17015
    UA_NS0ID_TRIPALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 17016
    UA_NS0ID_TRIPALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 17017
    UA_NS0ID_TRIPALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 17018
    UA_NS0ID_TRIPALARMTYPE_SILENCESTATE = 17019
    UA_NS0ID_TRIPALARMTYPE_SILENCESTATE_ID = 17020
    UA_NS0ID_TRIPALARMTYPE_SILENCESTATE_NAME = 17021
    UA_NS0ID_TRIPALARMTYPE_SILENCESTATE_NUMBER = 17022
    UA_NS0ID_TRIPALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 17023
    UA_NS0ID_TRIPALARMTYPE_SILENCESTATE_TRANSITIONTIME = 17024
    UA_NS0ID_TRIPALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 17025
    UA_NS0ID_TRIPALARMTYPE_SILENCESTATE_TRUESTATE = 17026
    UA_NS0ID_TRIPALARMTYPE_SILENCESTATE_FALSESTATE = 17027
    UA_NS0ID_TRIPALARMTYPE_AUDIBLEENABLED = 17028
    UA_NS0ID_TRIPALARMTYPE_AUDIBLESOUND = 17029
    UA_NS0ID_ADDPUBLISHEDDATAITEMSTEMPLATEMETHODTYPE = 17030
    UA_NS0ID_ADDPUBLISHEDDATAITEMSTEMPLATEMETHODTYPE_INPUTARGUMENTS = 17031
    UA_NS0ID_ADDPUBLISHEDDATAITEMSTEMPLATEMETHODTYPE_OUTPUTARGUMENTS = 17032
    UA_NS0ID_ADDPUBLISHEDEVENTSTEMPLATEMETHODTYPE = 17033
    UA_NS0ID_TRIPALARMTYPE_ONDELAY = 17034
    UA_NS0ID_TRIPALARMTYPE_OFFDELAY = 17035
    UA_NS0ID_TRIPALARMTYPE_FIRSTINGROUPFLAG = 17036
    UA_NS0ID_TRIPALARMTYPE_FIRSTINGROUP = 17037
    UA_NS0ID_TRIPALARMTYPE_ALARMGROUP_PLACEHOLDER = 17038
    UA_NS0ID_TRIPALARMTYPE_REALARMTIME = 17039
    UA_NS0ID_TRIPALARMTYPE_REALARMREPEATCOUNT = 17040
    UA_NS0ID_TRIPALARMTYPE_SILENCE = 17041
    UA_NS0ID_TRIPALARMTYPE_SUPPRESS = 17042
    UA_NS0ID_ADDPUBLISHEDEVENTSTEMPLATEMETHODTYPE_INPUTARGUMENTS = 17043
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONDITIONSUBCLASSID = 17044
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_CONDITIONSUBCLASSNAME = 17045
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OUTOFSERVICESTATE = 17046
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OUTOFSERVICESTATE_ID = 17047
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OUTOFSERVICESTATE_NAME = 17048
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OUTOFSERVICESTATE_NUMBER = 17049
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 17050
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 17051
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 17052
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 17053
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 17054
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCESTATE = 17055
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCESTATE_ID = 17056
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCESTATE_NAME = 17057
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCESTATE_NUMBER = 17058
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 17059
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCESTATE_TRANSITIONTIME = 17060
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 17061
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCESTATE_TRUESTATE = 17062
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCESTATE_FALSESTATE = 17063
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_AUDIBLEENABLED = 17064
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_AUDIBLESOUND = 17065
    UA_NS0ID_ADDPUBLISHEDEVENTSTEMPLATEMETHODTYPE_OUTPUTARGUMENTS = 17066
    UA_NS0ID_ADDDATASETFOLDERMETHODTYPE = 17067
    UA_NS0ID_ADDDATASETFOLDERMETHODTYPE_INPUTARGUMENTS = 17068
    UA_NS0ID_ADDDATASETFOLDERMETHODTYPE_OUTPUTARGUMENTS = 17069
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ONDELAY = 17070
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_OFFDELAY = 17071
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_FIRSTINGROUPFLAG = 17072
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_FIRSTINGROUP = 17073
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_ALARMGROUP_PLACEHOLDER = 17074
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_REALARMTIME = 17075
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_REALARMREPEATCOUNT = 17076
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SILENCE = 17077
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SUPPRESS = 17078
    UA_NS0ID_REMOVEDATASETFOLDERMETHODTYPE = 17079
    UA_NS0ID_DISCREPANCYALARMTYPE = 17080
    UA_NS0ID_DISCREPANCYALARMTYPE_EVENTID = 17081
    UA_NS0ID_DISCREPANCYALARMTYPE_EVENTTYPE = 17082
    UA_NS0ID_DISCREPANCYALARMTYPE_SOURCENODE = 17083
    UA_NS0ID_DISCREPANCYALARMTYPE_SOURCENAME = 17084
    UA_NS0ID_DISCREPANCYALARMTYPE_TIME = 17085
    UA_NS0ID_DISCREPANCYALARMTYPE_RECEIVETIME = 17086
    UA_NS0ID_DISCREPANCYALARMTYPE_LOCALTIME = 17087
    UA_NS0ID_DISCREPANCYALARMTYPE_MESSAGE = 17088
    UA_NS0ID_DISCREPANCYALARMTYPE_SEVERITY = 17089
    UA_NS0ID_DISCREPANCYALARMTYPE_CONDITIONCLASSID = 17090
    UA_NS0ID_DISCREPANCYALARMTYPE_CONDITIONCLASSNAME = 17091
    UA_NS0ID_DISCREPANCYALARMTYPE_CONDITIONSUBCLASSID = 17092
    UA_NS0ID_DISCREPANCYALARMTYPE_CONDITIONSUBCLASSNAME = 17093
    UA_NS0ID_DISCREPANCYALARMTYPE_CONDITIONNAME = 17094
    UA_NS0ID_DISCREPANCYALARMTYPE_BRANCHID = 17095
    UA_NS0ID_DISCREPANCYALARMTYPE_RETAIN = 17096
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLEDSTATE = 17097
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLEDSTATE_ID = 17098
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLEDSTATE_NAME = 17099
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLEDSTATE_NUMBER = 17100
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 17101
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 17102
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 17103
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLEDSTATE_TRUESTATE = 17104
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLEDSTATE_FALSESTATE = 17105
    UA_NS0ID_DISCREPANCYALARMTYPE_QUALITY = 17106
    UA_NS0ID_DISCREPANCYALARMTYPE_QUALITY_SOURCETIMESTAMP = 17107
    UA_NS0ID_DISCREPANCYALARMTYPE_LASTSEVERITY = 17108
    UA_NS0ID_DISCREPANCYALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 17109
    UA_NS0ID_DISCREPANCYALARMTYPE_COMMENT = 17110
    UA_NS0ID_DISCREPANCYALARMTYPE_COMMENT_SOURCETIMESTAMP = 17111
    UA_NS0ID_DISCREPANCYALARMTYPE_CLIENTUSERID = 17112
    UA_NS0ID_DISCREPANCYALARMTYPE_DISABLE = 17113
    UA_NS0ID_DISCREPANCYALARMTYPE_ENABLE = 17114
    UA_NS0ID_DISCREPANCYALARMTYPE_ADDCOMMENT = 17115
    UA_NS0ID_DISCREPANCYALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 17116
    UA_NS0ID_DISCREPANCYALARMTYPE_CONDITIONREFRESH = 17117
    UA_NS0ID_DISCREPANCYALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 17118
    UA_NS0ID_DISCREPANCYALARMTYPE_CONDITIONREFRESH2 = 17119
    UA_NS0ID_DISCREPANCYALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 17120
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKEDSTATE = 17121
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKEDSTATE_ID = 17122
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKEDSTATE_NAME = 17123
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKEDSTATE_NUMBER = 17124
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 17125
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 17126
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 17127
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKEDSTATE_TRUESTATE = 17128
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKEDSTATE_FALSESTATE = 17129
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRMEDSTATE = 17130
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRMEDSTATE_ID = 17131
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRMEDSTATE_NAME = 17132
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRMEDSTATE_NUMBER = 17133
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 17134
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 17135
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 17136
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 17137
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 17138
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKNOWLEDGE = 17139
    UA_NS0ID_DISCREPANCYALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 17140
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRM = 17141
    UA_NS0ID_DISCREPANCYALARMTYPE_CONFIRM_INPUTARGUMENTS = 17142
    UA_NS0ID_DISCREPANCYALARMTYPE_ACTIVESTATE = 17143
    UA_NS0ID_DISCREPANCYALARMTYPE_ACTIVESTATE_ID = 17144
    UA_NS0ID_DISCREPANCYALARMTYPE_ACTIVESTATE_NAME = 17145
    UA_NS0ID_DISCREPANCYALARMTYPE_ACTIVESTATE_NUMBER = 17146
    UA_NS0ID_DISCREPANCYALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 17147
    UA_NS0ID_DISCREPANCYALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 17148
    UA_NS0ID_DISCREPANCYALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 17149
    UA_NS0ID_DISCREPANCYALARMTYPE_ACTIVESTATE_TRUESTATE = 17150
    UA_NS0ID_DISCREPANCYALARMTYPE_ACTIVESTATE_FALSESTATE = 17151
    UA_NS0ID_DISCREPANCYALARMTYPE_INPUTNODE = 17152
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDSTATE = 17153
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDSTATE_ID = 17154
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDSTATE_NAME = 17155
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDSTATE_NUMBER = 17156
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 17157
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 17158
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 17159
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 17160
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 17161
    UA_NS0ID_DISCREPANCYALARMTYPE_OUTOFSERVICESTATE = 17162
    UA_NS0ID_DISCREPANCYALARMTYPE_OUTOFSERVICESTATE_ID = 17163
    UA_NS0ID_DISCREPANCYALARMTYPE_OUTOFSERVICESTATE_NAME = 17164
    UA_NS0ID_DISCREPANCYALARMTYPE_OUTOFSERVICESTATE_NUMBER = 17165
    UA_NS0ID_DISCREPANCYALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 17166
    UA_NS0ID_DISCREPANCYALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 17167
    UA_NS0ID_DISCREPANCYALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 17168
    UA_NS0ID_DISCREPANCYALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 17169
    UA_NS0ID_DISCREPANCYALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 17170
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCESTATE = 17171
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCESTATE_ID = 17172
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCESTATE_NAME = 17173
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCESTATE_NUMBER = 17174
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 17175
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCESTATE_TRANSITIONTIME = 17176
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 17177
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCESTATE_TRUESTATE = 17178
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCESTATE_FALSESTATE = 17179
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE = 17180
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 17181
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 17182
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 17183
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 17184
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 17185
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 17186
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 17187
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 17188
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 17189
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 17190
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 17191
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 17192
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_UNSHELVE = 17193
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 17194
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 17195
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 17196
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESSEDORSHELVED = 17197
    UA_NS0ID_DISCREPANCYALARMTYPE_MAXTIMESHELVED = 17198
    UA_NS0ID_DISCREPANCYALARMTYPE_AUDIBLEENABLED = 17199
    UA_NS0ID_DISCREPANCYALARMTYPE_AUDIBLESOUND = 17200
    UA_NS0ID_REMOVEDATASETFOLDERMETHODTYPE_INPUTARGUMENTS = 17201
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDRESS_NETWORKINTERFACE = 17202
    UA_NS0ID_PUBSUBCONNECTIONTYPE_TRANSPORTSETTINGS = 17203
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_MAXNETWORKMESSAGESIZE = 17204
    UA_NS0ID_DISCREPANCYALARMTYPE_ONDELAY = 17205
    UA_NS0ID_DISCREPANCYALARMTYPE_OFFDELAY = 17206
    UA_NS0ID_DISCREPANCYALARMTYPE_FIRSTINGROUPFLAG = 17207
    UA_NS0ID_DISCREPANCYALARMTYPE_FIRSTINGROUP = 17208
    UA_NS0ID_DISCREPANCYALARMTYPE_ALARMGROUP_PLACEHOLDER = 17209
    UA_NS0ID_DISCREPANCYALARMTYPE_REALARMTIME = 17210
    UA_NS0ID_DISCREPANCYALARMTYPE_REALARMREPEATCOUNT = 17211
    UA_NS0ID_DISCREPANCYALARMTYPE_SILENCE = 17212
    UA_NS0ID_DISCREPANCYALARMTYPE_SUPPRESS = 17213
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_WRITERGROUPID = 17214
    UA_NS0ID_DISCREPANCYALARMTYPE_TARGETVALUENODE = 17215
    UA_NS0ID_DISCREPANCYALARMTYPE_EXPECTEDTIME = 17216
    UA_NS0ID_DISCREPANCYALARMTYPE_TOLERANCE = 17217
    UA_NS0ID_SAFETYCONDITIONCLASSTYPE = 17218
    UA_NS0ID_HIGHLYMANAGEDALARMCONDITIONCLASSTYPE = 17219
    UA_NS0ID_TRAININGCONDITIONCLASSTYPE = 17220
    UA_NS0ID_TESTINGCONDITIONSUBCLASSTYPE = 17221
    UA_NS0ID_AUDITCONDITIONCOMMENTEVENTTYPE_CONDITIONEVENTID = 17222
    UA_NS0ID_AUDITCONDITIONACKNOWLEDGEEVENTTYPE_CONDITIONEVENTID = 17223
    UA_NS0ID_AUDITCONDITIONCONFIRMEVENTTYPE_CONDITIONEVENTID = 17224
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE = 17225
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_EVENTID = 17226
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_EVENTTYPE = 17227
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_SOURCENODE = 17228
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_SOURCENAME = 17229
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_TIME = 17230
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_RECEIVETIME = 17231
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_LOCALTIME = 17232
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_MESSAGE = 17233
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_SEVERITY = 17234
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_ACTIONTIMESTAMP = 17235
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_STATUS = 17236
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_SERVERID = 17237
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_CLIENTAUDITENTRYID = 17238
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_CLIENTUSERID = 17239
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_METHODID = 17240
    UA_NS0ID_AUDITCONDITIONSUPPRESSIONEVENTTYPE_INPUTARGUMENTS = 17241
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE = 17242
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_EVENTID = 17243
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_EVENTTYPE = 17244
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_SOURCENODE = 17245
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_SOURCENAME = 17246
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_TIME = 17247
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_RECEIVETIME = 17248
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_LOCALTIME = 17249
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_MESSAGE = 17250
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_SEVERITY = 17251
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_ACTIONTIMESTAMP = 17252
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_STATUS = 17253
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_SERVERID = 17254
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_CLIENTAUDITENTRYID = 17255
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_CLIENTUSERID = 17256
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_METHODID = 17257
    UA_NS0ID_AUDITCONDITIONSILENCEEVENTTYPE_INPUTARGUMENTS = 17258
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE = 17259
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_EVENTID = 17260
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_EVENTTYPE = 17261
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_SOURCENODE = 17262
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_SOURCENAME = 17263
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_TIME = 17264
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_RECEIVETIME = 17265
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_LOCALTIME = 17266
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_MESSAGE = 17267
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_SEVERITY = 17268
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_ACTIONTIMESTAMP = 17269
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_STATUS = 17270
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_SERVERID = 17271
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_CLIENTAUDITENTRYID = 17272
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_CLIENTUSERID = 17273
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_METHODID = 17274
    UA_NS0ID_AUDITCONDITIONOUTOFSERVICEEVENTTYPE_INPUTARGUMENTS = 17275
    UA_NS0ID_HASEFFECTDISABLE = 17276
    UA_NS0ID_ALARMRATEVARIABLETYPE = 17277
    UA_NS0ID_ALARMRATEVARIABLETYPE_RATE = 17278
    UA_NS0ID_ALARMMETRICSTYPE = 17279
    UA_NS0ID_ALARMMETRICSTYPE_ALARMCOUNT = 17280
    UA_NS0ID_ALARMMETRICSTYPE_MAXIMUMACTIVESTATE = 17281
    UA_NS0ID_ALARMMETRICSTYPE_MAXIMUMUNACK = 17282
    UA_NS0ID_ALARMMETRICSTYPE_MAXIMUMREALARMCOUNT = 17283
    UA_NS0ID_ALARMMETRICSTYPE_CURRENTALARMRATE = 17284
    UA_NS0ID_ALARMMETRICSTYPE_CURRENTALARMRATE_RATE = 17285
    UA_NS0ID_ALARMMETRICSTYPE_MAXIMUMALARMRATE = 17286
    UA_NS0ID_ALARMMETRICSTYPE_MAXIMUMALARMRATE_RATE = 17287
    UA_NS0ID_ALARMMETRICSTYPE_AVERAGEALARMRATE = 17288
    UA_NS0ID_ALARMMETRICSTYPE_AVERAGEALARMRATE_RATE = 17289
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_TRANSPORTSETTINGS = 17290
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_MESSAGESETTINGS = 17291
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTPROFILEURI = 17292
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_ADDDATASETWRITER = 17293
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_ADDDATASETWRITER_INPUTARGUMENTS = 17294
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTPROFILEURI_RESTRICTTOLIST = 17295
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_SETSECURITYKEYS = 17296
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_SETSECURITYKEYS_INPUTARGUMENTS = 17297
    UA_NS0ID_SETSECURITYKEYSMETHODTYPE = 17298
    UA_NS0ID_SETSECURITYKEYSMETHODTYPE_INPUTARGUMENTS = 17299
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 17300
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_ADDDATASETWRITER_OUTPUTARGUMENTS = 17301
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_MAXNETWORKMESSAGESIZE = 17302
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 17303
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 17304
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 17305
    UA_NS0ID_PUBSUBCONNECTIONTYPE_TRANSPORTPROFILEURI = 17306
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_TRANSPORTSETTINGS = 17307
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_MESSAGESETTINGS = 17308
    UA_NS0ID_PUBSUBCONNECTIONTYPE_TRANSPORTPROFILEURI_RESTRICTTOLIST = 17309
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER = 17310
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_SECURITYMODE = 17311
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_SECURITYGROUPID = 17312
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_SECURITYKEYSERVICES = 17313
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_STATUS = 17314
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_STATUS_STATE = 17315
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_STATUS_ENABLE = 17316
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_STATUS_DISABLE = 17317
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_PUBLISHINGINTERVAL = 17318
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_KEEPALIVETIME = 17319
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 17320
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_PRIORITY = 17321
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_LOCALEIDS = 17322
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_REMOVEDATASETWRITER = 17323
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_REMOVEDATASETWRITER_INPUTARGUMENTS = 17324
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER = 17325
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_SECURITYMODE = 17326
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_SECURITYGROUPID = 17327
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_SECURITYKEYSERVICES = 17328
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_STATUS = 17329
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_STATUS_STATE = 17330
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_STATUS_ENABLE = 17331
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_STATUS_DISABLE = 17332
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_REMOVEDATASETREADER = 17333
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_REMOVEDATASETREADER_INPUTARGUMENTS = 17334
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 17335
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 17336
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 17337
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 17338
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 17339
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 17340
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 17341
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 17342
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 17343
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 17344
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 17345
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 17346
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 17347
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 17348
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 17349
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 17350
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 17351
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES = 17352
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_RESOLVEDADDRESS = 17353
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_RESOLVEDADDRESS_DIAGNOSTICSLEVEL = 17354
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_ADDDATASETREADER = 17355
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDWRITERGROUP = 17356
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDWRITERGROUP_INPUTARGUMENTS = 17357
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDWRITERGROUP_OUTPUTARGUMENTS = 17358
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDREADERGROUP = 17359
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDREADERGROUP_INPUTARGUMENTS = 17360
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDREADERGROUP_OUTPUTARGUMENTS = 17361
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_REMOVEGROUP = 17362
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_REMOVEGROUP_INPUTARGUMENTS = 17363
    UA_NS0ID_PUBLISHSUBSCRIBE_SETSECURITYKEYS = 17364
    UA_NS0ID_PUBLISHSUBSCRIBE_SETSECURITYKEYS_INPUTARGUMENTS = 17365
    UA_NS0ID_PUBLISHSUBSCRIBE_ADDCONNECTION = 17366
    UA_NS0ID_PUBLISHSUBSCRIBE_ADDCONNECTION_INPUTARGUMENTS = 17367
    UA_NS0ID_PUBLISHSUBSCRIBE_ADDCONNECTION_OUTPUTARGUMENTS = 17368
    UA_NS0ID_PUBLISHSUBSCRIBE_REMOVECONNECTION = 17369
    UA_NS0ID_PUBLISHSUBSCRIBE_REMOVECONNECTION_INPUTARGUMENTS = 17370
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS = 17371
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMS = 17372
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMS_INPUTARGUMENTS = 17373
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMS_OUTPUTARGUMENTS = 17374
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTS = 17375
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTS_INPUTARGUMENTS = 17376
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTS_OUTPUTARGUMENTS = 17377
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMSTEMPLATE = 17378
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMSTEMPLATE_INPUTARGUMENTS = 17379
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDDATAITEMSTEMPLATE_OUTPUTARGUMENTS = 17380
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTSTEMPLATE = 17381
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTSTEMPLATE_INPUTARGUMENTS = 17382
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDPUBLISHEDEVENTSTEMPLATE_OUTPUTARGUMENTS = 17383
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_REMOVEPUBLISHEDDATASET = 17384
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_REMOVEPUBLISHEDDATASET_INPUTARGUMENTS = 17385
    UA_NS0ID_DATASETREADERTYPE_CREATETARGETVARIABLES = 17386
    UA_NS0ID_DATASETREADERTYPE_CREATETARGETVARIABLES_INPUTARGUMENTS = 17387
    UA_NS0ID_DATASETREADERTYPE_CREATETARGETVARIABLES_OUTPUTARGUMENTS = 17388
    UA_NS0ID_DATASETREADERTYPE_CREATEDATASETMIRROR = 17389
    UA_NS0ID_DATASETREADERTYPE_CREATEDATASETMIRROR_INPUTARGUMENTS = 17390
    UA_NS0ID_DATASETREADERTYPE_CREATEDATASETMIRROR_OUTPUTARGUMENTS = 17391
    UA_NS0ID_DATASETREADERTYPECREATETARGETVARIABLESMETHODTYPE = 17392
    UA_NS0ID_DATASETREADERTYPECREATETARGETVARIABLESMETHODTYPE_INPUTARGUMENTS = 17393
    UA_NS0ID_DATASETREADERTYPECREATETARGETVARIABLESMETHODTYPE_OUTPUTARGUMENTS = 17394
    UA_NS0ID_DATASETREADERTYPECREATEDATASETMIRRORMETHODTYPE = 17395
    UA_NS0ID_DATASETREADERTYPECREATEDATASETMIRRORMETHODTYPE_INPUTARGUMENTS = 17396
    UA_NS0ID_DATASETREADERTYPECREATEDATASETMIRRORMETHODTYPE_OUTPUTARGUMENTS = 17397
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDDATASETFOLDER = 17398
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_ADDDATASETREADER_INPUTARGUMENTS = 17399
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_ADDDATASETREADER_OUTPUTARGUMENTS = 17400
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDDATASETFOLDER_INPUTARGUMENTS = 17401
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_ADDDATASETFOLDER_OUTPUTARGUMENTS = 17402
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_REMOVEDATASETFOLDER = 17403
    UA_NS0ID_PUBLISHSUBSCRIBE_PUBLISHEDDATASETS_REMOVEDATASETFOLDER_INPUTARGUMENTS = 17404
    UA_NS0ID_PUBLISHSUBSCRIBE_STATUS = 17405
    UA_NS0ID_PUBLISHSUBSCRIBE_STATUS_STATE = 17406
    UA_NS0ID_PUBLISHSUBSCRIBE_STATUS_ENABLE = 17407
    UA_NS0ID_PUBLISHSUBSCRIBE_STATUS_DISABLE = 17408
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS = 17409
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_DIAGNOSTICSLEVEL = 17410
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALINFORMATION = 17411
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 17412
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 17413
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 17414
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 17415
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALERROR = 17416
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALERROR_ACTIVE = 17417
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 17418
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 17419
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 17420
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_RESET = 17421
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_SUBERROR = 17422
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS = 17423
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEERROR = 17424
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 17425
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 17426
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDWRITERGROUP = 17427
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDWRITERGROUP_INPUTARGUMENTS = 17428
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 17429
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 17430
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 17431
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 17432
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 17433
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 17434
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 17435
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 17436
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 17437
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 17438
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 17439
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 17440
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 17441
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 17442
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 17443
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 17444
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 17445
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 17446
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 17447
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 17448
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 17449
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 17450
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 17451
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 17452
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 17453
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 17454
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 17455
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDWRITERGROUP_OUTPUTARGUMENTS = 17456
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_LIVEVALUES = 17457
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETWRITERS = 17458
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETWRITERS_DIAGNOSTICSLEVEL = 17459
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETREADERS = 17460
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETREADERS_DIAGNOSTICSLEVEL = 17461
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETWRITERS = 17462
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETWRITERS_DIAGNOSTICSLEVEL = 17463
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETREADERS = 17464
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDREADERGROUP = 17465
    UA_NS0ID_PUBLISHSUBSCRIBE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETREADERS_DIAGNOSTICSLEVEL = 17466
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTDATATYPE = 17467
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 17468
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATAGRAMCONNECTIONTRANSPORTDATATYPE = 17469
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATAGRAMCONNECTIONTRANSPORTDATATYPE_DATATYPEVERSION = 17470
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATAGRAMCONNECTIONTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 17471
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 17472
    UA_NS0ID_OPCUA_XMLSCHEMA_DATAGRAMCONNECTIONTRANSPORTDATATYPE = 17473
    UA_NS0ID_OPCUA_XMLSCHEMA_DATAGRAMCONNECTIONTRANSPORTDATATYPE_DATATYPEVERSION = 17474
    UA_NS0ID_OPCUA_XMLSCHEMA_DATAGRAMCONNECTIONTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 17475
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 17476
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE_DATASETOFFSET = 17477
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_CONNECTIONPROPERTIES = 17478
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_SUPPORTEDTRANSPORTPROFILES = 17479
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_CONNECTIONPROPERTIES = 17480
    UA_NS0ID_PUBLISHSUBSCRIBE_SUPPORTEDTRANSPORTPROFILES = 17481
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETWRITERPROPERTIES = 17482
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETWRITERPROPERTIES = 17483
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETWRITERPROPERTIES = 17484
    UA_NS0ID_PUBSUBCONNECTIONTYPE_CONNECTIONPROPERTIES = 17485
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_GROUPPROPERTIES = 17486
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_GROUPPROPERTIES = 17487
    UA_NS0ID_PUBSUBGROUPTYPE_GROUPPROPERTIES = 17488
    UA_NS0ID_WRITERGROUPTYPE_GROUPPROPERTIES = 17489
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETWRITERPROPERTIES = 17490
    UA_NS0ID_READERGROUPTYPE_GROUPPROPERTIES = 17491
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DATASETREADERPROPERTIES = 17492
    UA_NS0ID_DATASETWRITERTYPE_DATASETWRITERPROPERTIES = 17493
    UA_NS0ID_DATASETREADERTYPE_DATASETREADERPROPERTIES = 17494
    UA_NS0ID_CREATECREDENTIALMETHODTYPE_OUTPUTARGUMENTS = 17495
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE = 17496
    UA_NS0ID_ANALOGUNITTYPE = 17497
    UA_NS0ID_ANALOGUNITTYPE_DEFINITION = 17498
    UA_NS0ID_ANALOGUNITTYPE_VALUEPRECISION = 17499
    UA_NS0ID_ANALOGUNITTYPE_INSTRUMENTRANGE = 17500
    UA_NS0ID_ANALOGUNITTYPE_EURANGE = 17501
    UA_NS0ID_ANALOGUNITTYPE_ENGINEERINGUNITS = 17502
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDRESS_NETWORKINTERFACE_SELECTIONS = 17503
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDRESS_NETWORKINTERFACE_SELECTIONDESCRIPTIONS = 17504
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_ADDRESS_NETWORKINTERFACE_RESTRICTTOLIST = 17505
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDRESS_NETWORKINTERFACE_SELECTIONS = 17506
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDREADERGROUP_INPUTARGUMENTS = 17507
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDREADERGROUP_OUTPUTARGUMENTS = 17508
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDRESS_NETWORKINTERFACE_SELECTIONDESCRIPTIONS = 17509
    UA_NS0ID_PUBLISHSUBSCRIBE_CONNECTIONNAME_PLACEHOLDER_ADDRESS_NETWORKINTERFACE_RESTRICTTOLIST = 17510
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER = 17511
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_RESOURCEURI = 17512
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_PROFILEURI = 17513
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_ENDPOINTURLS = 17514
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_SERVICESTATUS = 17515
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_GETENCRYPTINGKEY = 17516
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_GETENCRYPTINGKEY_INPUTARGUMENTS = 17517
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_GETENCRYPTINGKEY_OUTPUTARGUMENTS = 17518
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_UPDATECREDENTIAL = 17519
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_UPDATECREDENTIAL_INPUTARGUMENTS = 17520
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_DELETECREDENTIAL = 17521
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_CREATECREDENTIAL = 17522
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_CREATECREDENTIAL_INPUTARGUMENTS = 17523
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONFOLDERTYPE_CREATECREDENTIAL_OUTPUTARGUMENTS = 17524
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_GETENCRYPTINGKEY = 17525
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_GETENCRYPTINGKEY_INPUTARGUMENTS = 17526
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_GETENCRYPTINGKEY_OUTPUTARGUMENTS = 17527
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_CREATECREDENTIAL = 17528
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_CREATECREDENTIAL_INPUTARGUMENTS = 17529
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_CREATECREDENTIAL_OUTPUTARGUMENTS = 17530
    UA_NS0ID_GETENCRYPTINGKEYMETHODTYPE = 17531
    UA_NS0ID_GETENCRYPTINGKEYMETHODTYPE_INPUTARGUMENTS = 17532
    UA_NS0ID_GETENCRYPTINGKEYMETHODTYPE_OUTPUTARGUMENTS = 17533
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_GETENCRYPTINGKEY = 17534
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_GETENCRYPTINGKEY_INPUTARGUMENTS = 17535
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_GETENCRYPTINGKEY_OUTPUTARGUMENTS = 17536
    UA_NS0ID_ADDITIONALPARAMETERSTYPE_ENCODING_DEFAULTBINARY = 17537
    UA_NS0ID_OPCUA_BINARYSCHEMA_ADDITIONALPARAMETERSTYPE = 17538
    UA_NS0ID_OPCUA_BINARYSCHEMA_ADDITIONALPARAMETERSTYPE_DATATYPEVERSION = 17539
    UA_NS0ID_OPCUA_BINARYSCHEMA_ADDITIONALPARAMETERSTYPE_DICTIONARYFRAGMENT = 17540
    UA_NS0ID_ADDITIONALPARAMETERSTYPE_ENCODING_DEFAULTXML = 17541
    UA_NS0ID_OPCUA_XMLSCHEMA_ADDITIONALPARAMETERSTYPE = 17542
    UA_NS0ID_OPCUA_XMLSCHEMA_ADDITIONALPARAMETERSTYPE_DATATYPEVERSION = 17543
    UA_NS0ID_OPCUA_XMLSCHEMA_ADDITIONALPARAMETERSTYPE_DICTIONARYFRAGMENT = 17544
    UA_NS0ID_RSAENCRYPTEDSECRET = 17545
    UA_NS0ID_ECCENCRYPTEDSECRET = 17546
    UA_NS0ID_ADDITIONALPARAMETERSTYPE_ENCODING_DEFAULTJSON = 17547
    UA_NS0ID_EPHEMERALKEYTYPE = 17548
    UA_NS0ID_EPHEMERALKEYTYPE_ENCODING_DEFAULTBINARY = 17549
    UA_NS0ID_OPCUA_BINARYSCHEMA_EPHEMERALKEYTYPE = 17550
    UA_NS0ID_OPCUA_BINARYSCHEMA_EPHEMERALKEYTYPE_DATATYPEVERSION = 17551
    UA_NS0ID_OPCUA_BINARYSCHEMA_EPHEMERALKEYTYPE_DICTIONARYFRAGMENT = 17552
    UA_NS0ID_EPHEMERALKEYTYPE_ENCODING_DEFAULTXML = 17553
    UA_NS0ID_OPCUA_XMLSCHEMA_EPHEMERALKEYTYPE = 17554
    UA_NS0ID_OPCUA_XMLSCHEMA_EPHEMERALKEYTYPE_DATATYPEVERSION = 17555
    UA_NS0ID_OPCUA_XMLSCHEMA_EPHEMERALKEYTYPE_DICTIONARYFRAGMENT = 17556
    UA_NS0ID_EPHEMERALKEYTYPE_ENCODING_DEFAULTJSON = 17557
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_HEADERLAYOUTURI = 17558
    UA_NS0ID_WRITERGROUPTYPE_HEADERLAYOUTURI = 17559
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_KEYFRAMECOUNT = 17560
    UA_NS0ID_PUBSUBCONNECTIONTYPEADDWRITERGROUPMETHODTYPE = 17561
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_HEADERLAYOUTURI = 17562
    UA_NS0ID_DATASETREADERTYPE_KEYFRAMECOUNT = 17563
    UA_NS0ID_DATASETREADERTYPE_HEADERLAYOUTURI = 17564
    UA_NS0ID_BASEANALOGTYPE_DEFINITION = 17565
    UA_NS0ID_BASEANALOGTYPE_VALUEPRECISION = 17566
    UA_NS0ID_BASEANALOGTYPE_INSTRUMENTRANGE = 17567
    UA_NS0ID_BASEANALOGTYPE_EURANGE = 17568
    UA_NS0ID_BASEANALOGTYPE_ENGINEERINGUNITS = 17569
    UA_NS0ID_ANALOGUNITRANGETYPE = 17570
    UA_NS0ID_ANALOGUNITRANGETYPE_DEFINITION = 17571
    UA_NS0ID_ANALOGUNITRANGETYPE_VALUEPRECISION = 17572
    UA_NS0ID_ANALOGUNITRANGETYPE_INSTRUMENTRANGE = 17573
    UA_NS0ID_ANALOGUNITRANGETYPE_EURANGE = 17574
    UA_NS0ID_ANALOGUNITRANGETYPE_ENGINEERINGUNITS = 17575
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDRESS_NETWORKINTERFACE_SELECTIONS = 17576
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDRESS_NETWORKINTERFACE_SELECTIONDESCRIPTIONS = 17577
    UA_NS0ID_PUBSUBCONNECTIONTYPE_ADDRESS_NETWORKINTERFACE_RESTRICTTOLIST = 17578
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTTYPE_DISCOVERYADDRESS_NETWORKINTERFACE_SELECTIONS = 17579
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTTYPE_DISCOVERYADDRESS_NETWORKINTERFACE_SELECTIONDESCRIPTIONS = 17580
    UA_NS0ID_DATAGRAMCONNECTIONTRANSPORTTYPE_DISCOVERYADDRESS_NETWORKINTERFACE_RESTRICTTOLIST = 17581
    UA_NS0ID_NETWORKADDRESSTYPE_NETWORKINTERFACE_SELECTIONS = 17582
    UA_NS0ID_NETWORKADDRESSTYPE_NETWORKINTERFACE_SELECTIONDESCRIPTIONS = 17583
    UA_NS0ID_NETWORKADDRESSTYPE_NETWORKINTERFACE_RESTRICTTOLIST = 17584
    UA_NS0ID_NETWORKADDRESSURLTYPE_NETWORKINTERFACE_SELECTIONS = 17585
    UA_NS0ID_NETWORKADDRESSURLTYPE_NETWORKINTERFACE_SELECTIONDESCRIPTIONS = 17586
    UA_NS0ID_NETWORKADDRESSURLTYPE_NETWORKINTERFACE_RESTRICTTOLIST = 17587
    UA_NS0ID_INDEX = 17588
    UA_NS0ID_DICTIONARYENTRYTYPE = 17589
    UA_NS0ID_DICTIONARYENTRYTYPE_DICTIONARYENTRYNAME_PLACEHOLDER = 17590
    UA_NS0ID_DICTIONARYFOLDERTYPE = 17591
    UA_NS0ID_DICTIONARYFOLDERTYPE_DICTIONARYFOLDERNAME_PLACEHOLDER = 17592
    UA_NS0ID_DICTIONARYFOLDERTYPE_DICTIONARYENTRYNAME_PLACEHOLDER = 17593
    UA_NS0ID_DICTIONARIES = 17594
    UA_NS0ID_DICTIONARIES_DICTIONARYFOLDERNAME_PLACEHOLDER = 17595
    UA_NS0ID_DICTIONARIES_DICTIONARYENTRYNAME_PLACEHOLDER = 17596
    UA_NS0ID_HASDICTIONARYENTRY = 17597
    UA_NS0ID_IRDIDICTIONARYENTRYTYPE = 17598
    UA_NS0ID_IRDIDICTIONARYENTRYTYPE_DICTIONARYENTRYNAME_PLACEHOLDER = 17599
    UA_NS0ID_URIDICTIONARYENTRYTYPE = 17600
    UA_NS0ID_URIDICTIONARYENTRYTYPE_DICTIONARYENTRYNAME_PLACEHOLDER = 17601
    UA_NS0ID_BASEINTERFACETYPE = 17602
    UA_NS0ID_HASINTERFACE = 17603
    UA_NS0ID_HASADDIN = 17604
    UA_NS0ID_DEFAULTINSTANCEBROWSENAME = 17605
    UA_NS0ID_GENERICATTRIBUTEVALUE = 17606
    UA_NS0ID_GENERICATTRIBUTES = 17607
    UA_NS0ID_GENERICATTRIBUTEVALUE_ENCODING_DEFAULTXML = 17608
    UA_NS0ID_GENERICATTRIBUTES_ENCODING_DEFAULTXML = 17609
    UA_NS0ID_GENERICATTRIBUTEVALUE_ENCODING_DEFAULTBINARY = 17610
    UA_NS0ID_GENERICATTRIBUTES_ENCODING_DEFAULTBINARY = 17611
    UA_NS0ID_SERVERTYPE_LOCALTIME = 17612
    UA_NS0ID_PUBSUBCONNECTIONTYPEADDWRITERGROUPMETHODTYPE_INPUTARGUMENTS = 17613
    UA_NS0ID_PUBSUBCONNECTIONTYPEADDWRITERGROUPMETHODTYPE_OUTPUTARGUMENTS = 17614
    UA_NS0ID_AUDITSECURITYEVENTTYPE_STATUSCODEID = 17615
    UA_NS0ID_AUDITCHANNELEVENTTYPE_STATUSCODEID = 17616
    UA_NS0ID_AUDITOPENSECURECHANNELEVENTTYPE_STATUSCODEID = 17617
    UA_NS0ID_AUDITSESSIONEVENTTYPE_STATUSCODEID = 17618
    UA_NS0ID_AUDITCREATESESSIONEVENTTYPE_STATUSCODEID = 17619
    UA_NS0ID_AUDITURLMISMATCHEVENTTYPE_STATUSCODEID = 17620
    UA_NS0ID_AUDITACTIVATESESSIONEVENTTYPE_STATUSCODEID = 17621
    UA_NS0ID_AUDITCANCELEVENTTYPE_STATUSCODEID = 17622
    UA_NS0ID_AUDITCERTIFICATEEVENTTYPE_STATUSCODEID = 17623
    UA_NS0ID_AUDITCERTIFICATEDATAMISMATCHEVENTTYPE_STATUSCODEID = 17624
    UA_NS0ID_AUDITCERTIFICATEEXPIREDEVENTTYPE_STATUSCODEID = 17625
    UA_NS0ID_AUDITCERTIFICATEINVALIDEVENTTYPE_STATUSCODEID = 17626
    UA_NS0ID_AUDITCERTIFICATEUNTRUSTEDEVENTTYPE_STATUSCODEID = 17627
    UA_NS0ID_AUDITCERTIFICATEREVOKEDEVENTTYPE_STATUSCODEID = 17628
    UA_NS0ID_AUDITCERTIFICATEMISMATCHEVENTTYPE_STATUSCODEID = 17629
    UA_NS0ID_PUBSUBCONNECTIONADDREADERGROUPGROUPMETHODTYPE = 17630
    UA_NS0ID_PUBSUBCONNECTIONADDREADERGROUPGROUPMETHODTYPE_INPUTARGUMENTS = 17631
    UA_NS0ID_SELECTIONLISTTYPE_SELECTIONS = 17632
    UA_NS0ID_SELECTIONLISTTYPE_SELECTIONDESCRIPTIONS = 17633
    UA_NS0ID_SERVER_LOCALTIME = 17634
    UA_NS0ID_FINITESTATEMACHINETYPE_AVAILABLESTATES = 17635
    UA_NS0ID_FINITESTATEMACHINETYPE_AVAILABLETRANSITIONS = 17636
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_AVAILABLESTATES = 17637
    UA_NS0ID_TEMPORARYFILETRANSFERTYPE_TRANSFERSTATE_PLACEHOLDER_AVAILABLETRANSITIONS = 17638
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_AVAILABLESTATES = 17639
    UA_NS0ID_FILETRANSFERSTATEMACHINETYPE_AVAILABLETRANSITIONS = 17640
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE = 17641
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_EVENTID = 17642
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_EVENTTYPE = 17643
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_SOURCENODE = 17644
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_SOURCENAME = 17645
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_TIME = 17646
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_RECEIVETIME = 17647
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_LOCALTIME = 17648
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_MESSAGE = 17649
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_SEVERITY = 17650
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_ACTIONTIMESTAMP = 17651
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_STATUS = 17652
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_SERVERID = 17653
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_CLIENTAUDITENTRYID = 17654
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_CLIENTUSERID = 17655
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_METHODID = 17656
    UA_NS0ID_ROLEMAPPINGRULECHANGEDAUDITEVENTTYPE_INPUTARGUMENTS = 17657
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_AVAILABLESTATES = 17658
    UA_NS0ID_ALARMCONDITIONTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17659
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_AVAILABLESTATES = 17660
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_SHELVINGSTATE_AVAILABLETRANSITIONS = 17661
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_AVAILABLESTATES = 17662
    UA_NS0ID_SHELVEDSTATEMACHINETYPE_AVAILABLETRANSITIONS = 17663
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17664
    UA_NS0ID_LIMITALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17665
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_AVAILABLESTATES = 17666
    UA_NS0ID_EXCLUSIVELIMITSTATEMACHINETYPE_AVAILABLETRANSITIONS = 17667
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17668
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17669
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_AVAILABLESTATES = 17670
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LIMITSTATE_AVAILABLETRANSITIONS = 17671
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17672
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17673
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17674
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17675
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17676
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17677
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_AVAILABLESTATES = 17678
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LIMITSTATE_AVAILABLETRANSITIONS = 17679
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17680
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17681
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17682
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17683
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_AVAILABLESTATES = 17684
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LIMITSTATE_AVAILABLETRANSITIONS = 17685
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17686
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17687
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17688
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17689
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_AVAILABLESTATES = 17690
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LIMITSTATE_AVAILABLETRANSITIONS = 17691
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17692
    UA_NS0ID_DISCRETEALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17693
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17694
    UA_NS0ID_OFFNORMALALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17695
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17696
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17697
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17698
    UA_NS0ID_TRIPALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17699
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17700
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17701
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 17702
    UA_NS0ID_DISCREPANCYALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 17703
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_AVAILABLESTATES = 17704
    UA_NS0ID_PROGRAMSTATEMACHINETYPE_AVAILABLETRANSITIONS = 17705
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTPROFILEURI_SELECTIONS = 17706
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_TRANSPORTPROFILEURI_SELECTIONDESCRIPTIONS = 17707
    UA_NS0ID_INTERFACETYPES = 17708
    UA_NS0ID_RATIONALNUMBERTYPE = 17709
    UA_NS0ID_PUBSUBCONNECTIONTYPE_TRANSPORTPROFILEURI_SELECTIONS = 17710
    UA_NS0ID_PUBSUBCONNECTIONTYPE_TRANSPORTPROFILEURI_SELECTIONDESCRIPTIONS = 17711
    UA_NS0ID_RATIONALNUMBERTYPE_NUMERATOR = 17712
    UA_NS0ID_RATIONALNUMBERTYPE_DENOMINATOR = 17713
    UA_NS0ID_VECTORTYPE = 17714
    UA_NS0ID_VECTORTYPE_VECTORUNIT = 17715
    UA_NS0ID_THREEDVECTORTYPE = 17716
    UA_NS0ID_THREEDVECTORTYPE_VECTORUNIT = 17717
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_DELETEFILESYSTEMOBJECT = 17718
    UA_NS0ID_FILEDIRECTORYTYPE_FILEDIRECTORYNAME_PLACEHOLDER_DELETEFILESYSTEMOBJECT_INPUTARGUMENTS = 17719
    UA_NS0ID_PUBSUBCONNECTIONADDREADERGROUPGROUPMETHODTYPE_OUTPUTARGUMENTS = 17720
    UA_NS0ID_CONNECTIONTRANSPORTTYPE = 17721
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_DELETEFILESYSTEMOBJECT = 17722
    UA_NS0ID_FILESYSTEM_FILEDIRECTORYNAME_PLACEHOLDER_DELETEFILESYSTEMOBJECT_INPUTARGUMENTS = 17723
    UA_NS0ID_PUBSUBGROUPTYPE_MAXNETWORKMESSAGESIZE = 17724
    UA_NS0ID_WRITERGROUPTYPE = 17725
    UA_NS0ID_WRITERGROUPTYPE_SECURITYMODE = 17726
    UA_NS0ID_WRITERGROUPTYPE_SECURITYGROUPID = 17727
    UA_NS0ID_WRITERGROUPTYPE_SECURITYKEYSERVICES = 17728
    UA_NS0ID_WRITERGROUPTYPE_MAXNETWORKMESSAGESIZE = 17729
    UA_NS0ID_WRITERGROUPTYPE_STATUS = 17730
    UA_NS0ID_WRITERGROUPTYPE_STATUS_STATE = 17731
    UA_NS0ID_AUTHORIZATIONSERVICES = 17732
    UA_NS0ID_WRITERGROUPTYPE_STATUS_ENABLE = 17734
    UA_NS0ID_WRITERGROUPTYPE_STATUS_DISABLE = 17735
    UA_NS0ID_WRITERGROUPTYPE_WRITERGROUPID = 17736
    UA_NS0ID_WRITERGROUPTYPE_PUBLISHINGINTERVAL = 17737
    UA_NS0ID_WRITERGROUPTYPE_KEEPALIVETIME = 17738
    UA_NS0ID_WRITERGROUPTYPE_PRIORITY = 17739
    UA_NS0ID_WRITERGROUPTYPE_LOCALEIDS = 17740
    UA_NS0ID_WRITERGROUPTYPE_TRANSPORTSETTINGS = 17741
    UA_NS0ID_WRITERGROUPTYPE_MESSAGESETTINGS = 17742
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER = 17743
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETWRITERID = 17744
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DATASETFIELDCONTENTMASK = 17745
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_KEYFRAMECOUNT = 17746
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_TRANSPORTSETTINGS = 17747
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_MESSAGESETTINGS = 17748
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS = 17749
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_STATE = 17750
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_ENABLE = 17751
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_STATUS_DISABLE = 17752
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS = 17753
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_DIAGNOSTICSLEVEL = 17754
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION = 17755
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 17756
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 17757
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 17758
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 17759
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR = 17760
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_ACTIVE = 17761
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 17762
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 17763
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 17764
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_RESET = 17765
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_SUBERROR = 17766
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS = 17767
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR = 17768
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 17769
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 17770
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 17771
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 17772
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 17773
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 17774
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 17775
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 17776
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 17777
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 17778
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 17779
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 17780
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 17781
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 17782
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 17783
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 17784
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 17785
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 17786
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 17787
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 17788
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 17789
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 17790
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 17791
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 17792
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 17793
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 17794
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 17795
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 17796
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 17797
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES = 17798
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES = 17799
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_ACTIVE = 17800
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_CLASSIFICATION = 17801
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_DIAGNOSTICSLEVEL = 17802
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_TIMEFIRSTCHANGE = 17803
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER = 17804
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER_DIAGNOSTICSLEVEL = 17805
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE = 17806
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE_DIAGNOSTICSLEVEL = 17807
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION = 17808
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION_DIAGNOSTICSLEVEL = 17809
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION = 17810
    UA_NS0ID_WRITERGROUPTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION_DIAGNOSTICSLEVEL = 17811
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS = 17812
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_DIAGNOSTICSLEVEL = 17813
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION = 17814
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 17815
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 17816
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 17817
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 17818
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALERROR = 17819
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALERROR_ACTIVE = 17820
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 17821
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 17822
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 17823
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_RESET = 17824
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_SUBERROR = 17825
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS = 17826
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR = 17827
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 17828
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 17829
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 17830
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 17831
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 17832
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 17833
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 17834
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 17835
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 17836
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 17837
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 17838
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 17839
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 17840
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 17841
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 17842
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 17843
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 17844
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 17845
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 17846
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 17847
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 17848
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 17849
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 17850
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 17851
    UA_NS0ID_AUTHORIZATIONSERVICECONFIGURATIONTYPE = 17852
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 17853
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 17854
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 17855
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 17856
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 17857
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_LIVEVALUES = 17858
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES = 17859
    UA_NS0ID_AUTHORIZATIONSERVICECONFIGURATIONTYPE_SERVICECERTIFICATE = 17860
    UA_NS0ID_DECIMALDATATYPE = 17861
    UA_NS0ID_DECIMALDATATYPE_ENCODING_DEFAULTXML = 17862
    UA_NS0ID_DECIMALDATATYPE_ENCODING_DEFAULTBINARY = 17863
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES_ACTIVE = 17864
    UA_NS0ID_ALARMCONDITIONTYPE_AUDIBLESOUND_LISTID = 17865
    UA_NS0ID_ALARMCONDITIONTYPE_AUDIBLESOUND_AGENCYID = 17866
    UA_NS0ID_ALARMCONDITIONTYPE_AUDIBLESOUND_VERSIONID = 17867
    UA_NS0ID_ALARMCONDITIONTYPE_UNSUPPRESS = 17868
    UA_NS0ID_ALARMCONDITIONTYPE_REMOVEFROMSERVICE = 17869
    UA_NS0ID_ALARMCONDITIONTYPE_PLACEINSERVICE = 17870
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES_CLASSIFICATION = 17871
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES_DIAGNOSTICSLEVEL = 17872
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES_TIMEFIRSTCHANGE = 17873
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS = 17874
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_UNSUPPRESS = 17875
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_REMOVEFROMSERVICE = 17876
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_PLACEINSERVICE = 17877
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS_ACTIVE = 17878
    UA_NS0ID_LIMITALARMTYPE_AUDIBLESOUND_LISTID = 17879
    UA_NS0ID_LIMITALARMTYPE_AUDIBLESOUND_AGENCYID = 17880
    UA_NS0ID_LIMITALARMTYPE_AUDIBLESOUND_VERSIONID = 17881
    UA_NS0ID_LIMITALARMTYPE_UNSUPPRESS = 17882
    UA_NS0ID_LIMITALARMTYPE_REMOVEFROMSERVICE = 17883
    UA_NS0ID_LIMITALARMTYPE_PLACEINSERVICE = 17884
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS_CLASSIFICATION = 17885
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_AUDIBLESOUND_LISTID = 17886
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_AUDIBLESOUND_AGENCYID = 17887
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_AUDIBLESOUND_VERSIONID = 17888
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_UNSUPPRESS = 17889
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_REMOVEFROMSERVICE = 17890
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_PLACEINSERVICE = 17891
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS_DIAGNOSTICSLEVEL = 17892
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_AUDIBLESOUND_LISTID = 17893
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_AUDIBLESOUND_AGENCYID = 17894
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_AUDIBLESOUND_VERSIONID = 17895
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_UNSUPPRESS = 17896
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_REMOVEFROMSERVICE = 17897
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_PLACEINSERVICE = 17898
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS_TIMEFIRSTCHANGE = 17899
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS = 17900
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS_ACTIVE = 17901
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS_CLASSIFICATION = 17902
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS_DIAGNOSTICSLEVEL = 17903
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_REMOVEFROMSERVICE = 17904
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_PLACEINSERVICE = 17905
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS_TIMEFIRSTCHANGE = 17906
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_AUDIBLESOUND_LISTID = 17907
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_AUDIBLESOUND_AGENCYID = 17908
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_AUDIBLESOUND_VERSIONID = 17909
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_UNSUPPRESS = 17910
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_REMOVEFROMSERVICE = 17911
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_PLACEINSERVICE = 17912
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETWRITERS = 17913
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_AUDIBLESOUND_LISTID = 17914
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_AUDIBLESOUND_AGENCYID = 17915
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_AUDIBLESOUND_VERSIONID = 17916
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_UNSUPPRESS = 17917
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_REMOVEFROMSERVICE = 17918
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_PLACEINSERVICE = 17919
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETWRITERS_DIAGNOSTICSLEVEL = 17920
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLESOUND_LISTID = 17921
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLESOUND_AGENCYID = 17922
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLESOUND_VERSIONID = 17923
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_UNSUPPRESS = 17924
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_REMOVEFROMSERVICE = 17925
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_PLACEINSERVICE = 17926
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETWRITERS = 17927
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_AUDIBLESOUND_LISTID = 17928
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_AUDIBLESOUND_AGENCYID = 17929
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_AUDIBLESOUND_VERSIONID = 17930
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_UNSUPPRESS = 17931
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_REMOVEFROMSERVICE = 17932
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_PLACEINSERVICE = 17933
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETWRITERS_DIAGNOSTICSLEVEL = 17934
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLESOUND_LISTID = 17935
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLESOUND_AGENCYID = 17936
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_AUDIBLESOUND_VERSIONID = 17937
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_UNSUPPRESS = 17938
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_REMOVEFROMSERVICE = 17939
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_PLACEINSERVICE = 17940
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_SECURITYTOKENID = 17941
    UA_NS0ID_DISCRETEALARMTYPE_AUDIBLESOUND_LISTID = 17942
    UA_NS0ID_DISCRETEALARMTYPE_AUDIBLESOUND_AGENCYID = 17943
    UA_NS0ID_DISCRETEALARMTYPE_AUDIBLESOUND_VERSIONID = 17944
    UA_NS0ID_DISCRETEALARMTYPE_UNSUPPRESS = 17945
    UA_NS0ID_DISCRETEALARMTYPE_REMOVEFROMSERVICE = 17946
    UA_NS0ID_DISCRETEALARMTYPE_PLACEINSERVICE = 17947
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_SECURITYTOKENID_DIAGNOSTICSLEVEL = 17948
    UA_NS0ID_OFFNORMALALARMTYPE_AUDIBLESOUND_LISTID = 17949
    UA_NS0ID_OFFNORMALALARMTYPE_AUDIBLESOUND_AGENCYID = 17950
    UA_NS0ID_OFFNORMALALARMTYPE_AUDIBLESOUND_VERSIONID = 17951
    UA_NS0ID_OFFNORMALALARMTYPE_UNSUPPRESS = 17952
    UA_NS0ID_OFFNORMALALARMTYPE_REMOVEFROMSERVICE = 17953
    UA_NS0ID_OFFNORMALALARMTYPE_PLACEINSERVICE = 17954
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_TIMETONEXTTOKENID = 17955
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_AUDIBLESOUND_LISTID = 17956
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_AUDIBLESOUND_AGENCYID = 17957
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_AUDIBLESOUND_VERSIONID = 17958
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_UNSUPPRESS = 17959
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_REMOVEFROMSERVICE = 17960
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_PLACEINSERVICE = 17961
    UA_NS0ID_WRITERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_TIMETONEXTTOKENID_DIAGNOSTICSLEVEL = 17962
    UA_NS0ID_TRIPALARMTYPE_AUDIBLESOUND_LISTID = 17963
    UA_NS0ID_TRIPALARMTYPE_AUDIBLESOUND_AGENCYID = 17964
    UA_NS0ID_TRIPALARMTYPE_AUDIBLESOUND_VERSIONID = 17965
    UA_NS0ID_TRIPALARMTYPE_UNSUPPRESS = 17966
    UA_NS0ID_TRIPALARMTYPE_REMOVEFROMSERVICE = 17967
    UA_NS0ID_TRIPALARMTYPE_PLACEINSERVICE = 17968
    UA_NS0ID_WRITERGROUPTYPE_ADDDATASETWRITER = 17969
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_AUDIBLESOUND_LISTID = 17970
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_AUDIBLESOUND_AGENCYID = 17971
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_AUDIBLESOUND_VERSIONID = 17972
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_UNSUPPRESS = 17973
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_REMOVEFROMSERVICE = 17974
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_PLACEINSERVICE = 17975
    UA_NS0ID_WRITERGROUPTYPE_ADDDATASETWRITER_INPUTARGUMENTS = 17976
    UA_NS0ID_DISCREPANCYALARMTYPE_AUDIBLESOUND_LISTID = 17977
    UA_NS0ID_DISCREPANCYALARMTYPE_AUDIBLESOUND_AGENCYID = 17978
    UA_NS0ID_DISCREPANCYALARMTYPE_AUDIBLESOUND_VERSIONID = 17979
    UA_NS0ID_DISCREPANCYALARMTYPE_UNSUPPRESS = 17980
    UA_NS0ID_DISCREPANCYALARMTYPE_REMOVEFROMSERVICE = 17981
    UA_NS0ID_DISCREPANCYALARMTYPE_PLACEINSERVICE = 17982
    UA_NS0ID_HASEFFECTENABLE = 17983
    UA_NS0ID_HASEFFECTSUPPRESSED = 17984
    UA_NS0ID_HASEFFECTUNSUPPRESSED = 17985
    UA_NS0ID_AUDIOVARIABLETYPE = 17986
    UA_NS0ID_WRITERGROUPTYPE_ADDDATASETWRITER_OUTPUTARGUMENTS = 17987
    UA_NS0ID_AUDIOVARIABLETYPE_LISTID = 17988
    UA_NS0ID_AUDIOVARIABLETYPE_AGENCYID = 17989
    UA_NS0ID_AUDIOVARIABLETYPE_VERSIONID = 17990
    UA_NS0ID_ALARMMETRICSTYPE_STARTTIME = 17991
    UA_NS0ID_WRITERGROUPTYPE_REMOVEDATASETWRITER = 17992
    UA_NS0ID_WRITERGROUPTYPE_REMOVEDATASETWRITER_INPUTARGUMENTS = 17993
    UA_NS0ID_PUBSUBGROUPTYPEADDWRITERRMETHODTYPE = 17994
    UA_NS0ID_PUBSUBGROUPTYPEADDWRITERRMETHODTYPE_INPUTARGUMENTS = 17995
    UA_NS0ID_PUBSUBGROUPTYPEADDWRITERRMETHODTYPE_OUTPUTARGUMENTS = 17996
    UA_NS0ID_WRITERGROUPTRANSPORTTYPE = 17997
    UA_NS0ID_WRITERGROUPMESSAGETYPE = 17998
    UA_NS0ID_READERGROUPTYPE = 17999
    UA_NS0ID_READERGROUPTYPE_SECURITYMODE = 18000
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE = 18001
    UA_NS0ID_READERGROUPTYPE_SECURITYGROUPID = 18002
    UA_NS0ID_READERGROUPTYPE_SECURITYKEYSERVICES = 18003
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_ENDPOINTURLS = 18004
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_SERVICESTATUS = 18005
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_UPDATECREDENTIAL = 18006
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_UPDATECREDENTIAL_INPUTARGUMENTS = 18007
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_DELETECREDENTIAL = 18008
    UA_NS0ID_KEYCREDENTIALUPDATEMETHODTYPE = 18009
    UA_NS0ID_KEYCREDENTIALUPDATEMETHODTYPE_INPUTARGUMENTS = 18010
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE = 18011
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_EVENTID = 18012
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_EVENTTYPE = 18013
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_SOURCENODE = 18014
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_SOURCENAME = 18015
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_TIME = 18016
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_RECEIVETIME = 18017
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_LOCALTIME = 18018
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_MESSAGE = 18019
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_SEVERITY = 18020
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_ACTIONTIMESTAMP = 18021
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_STATUS = 18022
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_SERVERID = 18023
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_CLIENTAUDITENTRYID = 18024
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_CLIENTUSERID = 18025
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_METHODID = 18026
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_INPUTARGUMENTS = 18027
    UA_NS0ID_KEYCREDENTIALAUDITEVENTTYPE_RESOURCEURI = 18028
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE = 18029
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_EVENTID = 18030
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_EVENTTYPE = 18031
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_SOURCENODE = 18032
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_SOURCENAME = 18033
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_TIME = 18034
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_RECEIVETIME = 18035
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_LOCALTIME = 18036
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_MESSAGE = 18037
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_SEVERITY = 18038
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_ACTIONTIMESTAMP = 18039
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_STATUS = 18040
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_SERVERID = 18041
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_CLIENTAUDITENTRYID = 18042
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_CLIENTUSERID = 18043
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_METHODID = 18044
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_INPUTARGUMENTS = 18045
    UA_NS0ID_KEYCREDENTIALUPDATEDAUDITEVENTTYPE_RESOURCEURI = 18046
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE = 18047
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_EVENTID = 18048
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_EVENTTYPE = 18049
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_SOURCENODE = 18050
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_SOURCENAME = 18051
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_TIME = 18052
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_RECEIVETIME = 18053
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_LOCALTIME = 18054
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_MESSAGE = 18055
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_SEVERITY = 18056
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_ACTIONTIMESTAMP = 18057
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_STATUS = 18058
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_SERVERID = 18059
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_CLIENTAUDITENTRYID = 18060
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_CLIENTUSERID = 18061
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_METHODID = 18062
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_INPUTARGUMENTS = 18063
    UA_NS0ID_KEYCREDENTIALDELETEDAUDITEVENTTYPE_RESOURCEURI = 18064
    UA_NS0ID_READERGROUPTYPE_MAXNETWORKMESSAGESIZE = 18065
    UA_NS0ID_READERGROUPTYPE_STATUS = 18067
    UA_NS0ID_READERGROUPTYPE_STATUS_STATE = 18068
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_RESOURCEURI = 18069
    UA_NS0ID_AUTHORIZATIONSERVICECONFIGURATIONTYPE_SERVICEURI = 18072
    UA_NS0ID_AUTHORIZATIONSERVICECONFIGURATIONTYPE_ISSUERENDPOINTURL = 18073
    UA_NS0ID_READERGROUPTYPE_STATUS_ENABLE = 18074
    UA_NS0ID_READERGROUPTYPE_STATUS_DISABLE = 18075
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER = 18076
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_PUBLISHERID = 18077
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_WRITERGROUPID = 18078
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DATASETWRITERID = 18079
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DATASETMETADATA = 18080
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DATASETFIELDCONTENTMASK = 18081
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_MESSAGERECEIVETIMEOUT = 18082
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_SECURITYMODE = 18083
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_SECURITYGROUPID = 18084
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_SECURITYKEYSERVICES = 18085
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_TRANSPORTSETTINGS = 18086
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_MESSAGESETTINGS = 18087
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_STATUS = 18088
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_STATUS_STATE = 18089
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_STATUS_ENABLE = 18090
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_STATUS_DISABLE = 18091
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS = 18092
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_DIAGNOSTICSLEVEL = 18093
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION = 18094
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 18095
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 18096
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 18097
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 18098
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR = 18099
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_ACTIVE = 18100
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 18101
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 18102
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 18103
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_RESET = 18104
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_SUBERROR = 18105
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS = 18106
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR = 18107
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 18108
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 18109
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 18110
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 18111
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 18112
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 18113
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 18114
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 18115
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 18116
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 18117
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 18118
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 18119
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 18120
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 18121
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 18122
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 18123
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 18124
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 18125
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 18126
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 18127
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 18128
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 18129
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 18130
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 18131
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 18132
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 18133
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 18134
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 18135
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 18136
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES = 18137
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES = 18138
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_ACTIVE = 18139
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_CLASSIFICATION = 18140
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_DIAGNOSTICSLEVEL = 18141
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_TIMEFIRSTCHANGE = 18142
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS = 18143
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_ACTIVE = 18144
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_CLASSIFICATION = 18145
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_DIAGNOSTICSLEVEL = 18146
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_TIMEFIRSTCHANGE = 18147
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER = 18148
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER_DIAGNOSTICSLEVEL = 18149
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE = 18150
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE_DIAGNOSTICSLEVEL = 18151
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION = 18152
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION_DIAGNOSTICSLEVEL = 18153
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION = 18154
    UA_NS0ID_KEYCREDENTIALCONFIGURATION = 18155
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER = 18156
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_RESOURCEURI = 18157
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION_DIAGNOSTICSLEVEL = 18158
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_ENDPOINTURLS = 18159
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_SERVICESTATUS = 18160
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_UPDATECREDENTIAL = 18161
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_UPDATECREDENTIAL_INPUTARGUMENTS = 18162
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_DELETECREDENTIAL = 18163
    UA_NS0ID_KEYCREDENTIALCONFIGURATION_SERVICENAME_PLACEHOLDER_PROFILEURI = 18164
    UA_NS0ID_KEYCREDENTIALCONFIGURATIONTYPE_PROFILEURI = 18165
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPEDEFINITION = 18166
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPEDEFINITION_DATATYPEVERSION = 18167
    UA_NS0ID_OPCUA_XMLSCHEMA_DATATYPEDEFINITION_DICTIONARYFRAGMENT = 18168
    UA_NS0ID_OPCUA_XMLSCHEMA_STRUCTUREFIELD = 18169
    UA_NS0ID_OPCUA_XMLSCHEMA_STRUCTUREFIELD_DATATYPEVERSION = 18170
    UA_NS0ID_OPCUA_XMLSCHEMA_STRUCTUREFIELD_DICTIONARYFRAGMENT = 18171
    UA_NS0ID_OPCUA_XMLSCHEMA_STRUCTUREDEFINITION = 18172
    UA_NS0ID_OPCUA_XMLSCHEMA_STRUCTUREDEFINITION_DATATYPEVERSION = 18173
    UA_NS0ID_OPCUA_XMLSCHEMA_STRUCTUREDEFINITION_DICTIONARYFRAGMENT = 18174
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMDEFINITION = 18175
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMDEFINITION_DATATYPEVERSION = 18176
    UA_NS0ID_OPCUA_XMLSCHEMA_ENUMDEFINITION_DICTIONARYFRAGMENT = 18177
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPEDEFINITION = 18178
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPEDEFINITION_DATATYPEVERSION = 18179
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATATYPEDEFINITION_DICTIONARYFRAGMENT = 18180
    UA_NS0ID_OPCUA_BINARYSCHEMA_STRUCTUREFIELD = 18181
    UA_NS0ID_OPCUA_BINARYSCHEMA_STRUCTUREFIELD_DATATYPEVERSION = 18182
    UA_NS0ID_OPCUA_BINARYSCHEMA_STRUCTUREFIELD_DICTIONARYFRAGMENT = 18183
    UA_NS0ID_OPCUA_BINARYSCHEMA_STRUCTUREDEFINITION = 18184
    UA_NS0ID_OPCUA_BINARYSCHEMA_STRUCTUREDEFINITION_DATATYPEVERSION = 18185
    UA_NS0ID_OPCUA_BINARYSCHEMA_STRUCTUREDEFINITION_DICTIONARYFRAGMENT = 18186
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMDEFINITION = 18187
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMDEFINITION_DATATYPEVERSION = 18188
    UA_NS0ID_OPCUA_BINARYSCHEMA_ENUMDEFINITION_DICTIONARYFRAGMENT = 18189
    UA_NS0ID_ALARMCONDITIONTYPE_LATCHEDSTATE = 18190
    UA_NS0ID_ALARMCONDITIONTYPE_LATCHEDSTATE_ID = 18191
    UA_NS0ID_ALARMCONDITIONTYPE_LATCHEDSTATE_NAME = 18192
    UA_NS0ID_ALARMCONDITIONTYPE_LATCHEDSTATE_NUMBER = 18193
    UA_NS0ID_ALARMCONDITIONTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18194
    UA_NS0ID_ALARMCONDITIONTYPE_LATCHEDSTATE_TRANSITIONTIME = 18195
    UA_NS0ID_ALARMCONDITIONTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18196
    UA_NS0ID_ALARMCONDITIONTYPE_LATCHEDSTATE_TRUESTATE = 18197
    UA_NS0ID_ALARMCONDITIONTYPE_LATCHEDSTATE_FALSESTATE = 18198
    UA_NS0ID_ALARMCONDITIONTYPE_RESET = 18199
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_AUDIBLESOUND_LISTID = 18200
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_AUDIBLESOUND_AGENCYID = 18201
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_AUDIBLESOUND_VERSIONID = 18202
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LATCHEDSTATE = 18203
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LATCHEDSTATE_ID = 18204
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LATCHEDSTATE_NAME = 18205
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LATCHEDSTATE_NUMBER = 18206
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18207
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LATCHEDSTATE_TRANSITIONTIME = 18208
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18209
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LATCHEDSTATE_TRUESTATE = 18210
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_LATCHEDSTATE_FALSESTATE = 18211
    UA_NS0ID_ALARMGROUPTYPE_ALARMCONDITIONINSTANCE_PLACEHOLDER_RESET = 18212
    UA_NS0ID_LIMITALARMTYPE_LATCHEDSTATE = 18213
    UA_NS0ID_LIMITALARMTYPE_LATCHEDSTATE_ID = 18214
    UA_NS0ID_LIMITALARMTYPE_LATCHEDSTATE_NAME = 18215
    UA_NS0ID_LIMITALARMTYPE_LATCHEDSTATE_NUMBER = 18216
    UA_NS0ID_LIMITALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18217
    UA_NS0ID_LIMITALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18218
    UA_NS0ID_LIMITALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18219
    UA_NS0ID_LIMITALARMTYPE_LATCHEDSTATE_TRUESTATE = 18220
    UA_NS0ID_LIMITALARMTYPE_LATCHEDSTATE_FALSESTATE = 18221
    UA_NS0ID_LIMITALARMTYPE_RESET = 18222
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LATCHEDSTATE = 18223
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_ID = 18224
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_NAME = 18225
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_NUMBER = 18226
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18227
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18228
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18229
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_TRUESTATE = 18230
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_FALSESTATE = 18231
    UA_NS0ID_EXCLUSIVELIMITALARMTYPE_RESET = 18232
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LATCHEDSTATE = 18233
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_ID = 18234
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_NAME = 18235
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_NUMBER = 18236
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18237
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18238
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18239
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_TRUESTATE = 18240
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_LATCHEDSTATE_FALSESTATE = 18241
    UA_NS0ID_NONEXCLUSIVELIMITALARMTYPE_RESET = 18242
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_AUDIBLESOUND_LISTID = 18243
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_AUDIBLESOUND_AGENCYID = 18244
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_AUDIBLESOUND_VERSIONID = 18245
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LATCHEDSTATE = 18246
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_ID = 18247
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_NAME = 18248
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_NUMBER = 18249
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18250
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18251
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18252
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_TRUESTATE = 18253
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_FALSESTATE = 18254
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_UNSUPPRESS = 18255
    UA_NS0ID_NONEXCLUSIVELEVELALARMTYPE_RESET = 18256
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LATCHEDSTATE = 18257
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_ID = 18258
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_NAME = 18259
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_NUMBER = 18260
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18261
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18262
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18263
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_TRUESTATE = 18264
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_LATCHEDSTATE_FALSESTATE = 18265
    UA_NS0ID_EXCLUSIVELEVELALARMTYPE_RESET = 18266
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE = 18267
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_ID = 18268
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_NAME = 18269
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_NUMBER = 18270
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18271
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18272
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18273
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_TRUESTATE = 18274
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_FALSESTATE = 18275
    UA_NS0ID_NONEXCLUSIVEDEVIATIONALARMTYPE_RESET = 18276
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE = 18277
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_ID = 18278
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_NAME = 18279
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_NUMBER = 18280
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18281
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18282
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18283
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_TRUESTATE = 18284
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_FALSESTATE = 18285
    UA_NS0ID_NONEXCLUSIVERATEOFCHANGEALARMTYPE_RESET = 18286
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE = 18287
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_ID = 18288
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_NAME = 18289
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_NUMBER = 18290
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18291
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18292
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18293
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_TRUESTATE = 18294
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_LATCHEDSTATE_FALSESTATE = 18295
    UA_NS0ID_EXCLUSIVEDEVIATIONALARMTYPE_RESET = 18296
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE = 18297
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_ID = 18298
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_NAME = 18299
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_NUMBER = 18300
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18301
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18302
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18303
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_TRUESTATE = 18304
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_LATCHEDSTATE_FALSESTATE = 18305
    UA_NS0ID_EXCLUSIVERATEOFCHANGEALARMTYPE_RESET = 18306
    UA_NS0ID_DISCRETEALARMTYPE_LATCHEDSTATE = 18307
    UA_NS0ID_DISCRETEALARMTYPE_LATCHEDSTATE_ID = 18308
    UA_NS0ID_DISCRETEALARMTYPE_LATCHEDSTATE_NAME = 18309
    UA_NS0ID_DISCRETEALARMTYPE_LATCHEDSTATE_NUMBER = 18310
    UA_NS0ID_DISCRETEALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18311
    UA_NS0ID_DISCRETEALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18312
    UA_NS0ID_DISCRETEALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18313
    UA_NS0ID_DISCRETEALARMTYPE_LATCHEDSTATE_TRUESTATE = 18314
    UA_NS0ID_DISCRETEALARMTYPE_LATCHEDSTATE_FALSESTATE = 18315
    UA_NS0ID_DISCRETEALARMTYPE_RESET = 18316
    UA_NS0ID_OFFNORMALALARMTYPE_LATCHEDSTATE = 18317
    UA_NS0ID_OFFNORMALALARMTYPE_LATCHEDSTATE_ID = 18318
    UA_NS0ID_OFFNORMALALARMTYPE_LATCHEDSTATE_NAME = 18319
    UA_NS0ID_OFFNORMALALARMTYPE_LATCHEDSTATE_NUMBER = 18320
    UA_NS0ID_OFFNORMALALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18321
    UA_NS0ID_OFFNORMALALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18322
    UA_NS0ID_OFFNORMALALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18323
    UA_NS0ID_OFFNORMALALARMTYPE_LATCHEDSTATE_TRUESTATE = 18324
    UA_NS0ID_OFFNORMALALARMTYPE_LATCHEDSTATE_FALSESTATE = 18325
    UA_NS0ID_OFFNORMALALARMTYPE_RESET = 18326
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LATCHEDSTATE = 18327
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LATCHEDSTATE_ID = 18328
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LATCHEDSTATE_NAME = 18329
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LATCHEDSTATE_NUMBER = 18330
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18331
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18332
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18333
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LATCHEDSTATE_TRUESTATE = 18334
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_LATCHEDSTATE_FALSESTATE = 18335
    UA_NS0ID_SYSTEMOFFNORMALALARMTYPE_RESET = 18336
    UA_NS0ID_TRIPALARMTYPE_LATCHEDSTATE = 18337
    UA_NS0ID_TRIPALARMTYPE_LATCHEDSTATE_ID = 18338
    UA_NS0ID_TRIPALARMTYPE_LATCHEDSTATE_NAME = 18339
    UA_NS0ID_TRIPALARMTYPE_LATCHEDSTATE_NUMBER = 18340
    UA_NS0ID_TRIPALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18341
    UA_NS0ID_TRIPALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18342
    UA_NS0ID_TRIPALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18343
    UA_NS0ID_TRIPALARMTYPE_LATCHEDSTATE_TRUESTATE = 18344
    UA_NS0ID_TRIPALARMTYPE_LATCHEDSTATE_FALSESTATE = 18345
    UA_NS0ID_TRIPALARMTYPE_RESET = 18346
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE = 18347
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_EVENTID = 18348
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_EVENTTYPE = 18349
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SOURCENODE = 18350
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SOURCENAME = 18351
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_TIME = 18352
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_RECEIVETIME = 18353
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LOCALTIME = 18354
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_MESSAGE = 18355
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SEVERITY = 18356
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONDITIONCLASSID = 18357
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONDITIONCLASSNAME = 18358
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONDITIONSUBCLASSID = 18359
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONDITIONSUBCLASSNAME = 18360
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONDITIONNAME = 18361
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_BRANCHID = 18362
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_RETAIN = 18363
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLEDSTATE = 18364
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLEDSTATE_ID = 18365
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLEDSTATE_NAME = 18366
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLEDSTATE_NUMBER = 18367
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 18368
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 18369
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 18370
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLEDSTATE_TRUESTATE = 18371
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLEDSTATE_FALSESTATE = 18372
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_QUALITY = 18373
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_QUALITY_SOURCETIMESTAMP = 18374
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LASTSEVERITY = 18375
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 18376
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_COMMENT = 18377
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_COMMENT_SOURCETIMESTAMP = 18378
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CLIENTUSERID = 18379
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_DISABLE = 18380
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ENABLE = 18381
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ADDCOMMENT = 18382
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 18383
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONDITIONREFRESH = 18384
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 18385
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONDITIONREFRESH2 = 18386
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 18387
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKEDSTATE = 18388
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKEDSTATE_ID = 18389
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKEDSTATE_NAME = 18390
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKEDSTATE_NUMBER = 18391
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 18392
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 18393
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 18394
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKEDSTATE_TRUESTATE = 18395
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKEDSTATE_FALSESTATE = 18396
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRMEDSTATE = 18397
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_ID = 18398
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_NAME = 18399
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_NUMBER = 18400
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 18401
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 18402
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 18403
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 18404
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 18405
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKNOWLEDGE = 18406
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 18407
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRM = 18408
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_CONFIRM_INPUTARGUMENTS = 18409
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACTIVESTATE = 18410
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACTIVESTATE_ID = 18411
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACTIVESTATE_NAME = 18412
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACTIVESTATE_NUMBER = 18413
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 18414
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 18415
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 18416
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACTIVESTATE_TRUESTATE = 18417
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ACTIVESTATE_FALSESTATE = 18418
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_INPUTNODE = 18419
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE = 18420
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_ID = 18421
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_NAME = 18422
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_NUMBER = 18423
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 18424
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 18425
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 18426
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 18427
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 18428
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE = 18429
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_ID = 18430
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_NAME = 18431
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_NUMBER = 18432
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 18433
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 18434
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 18435
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 18436
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 18437
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE = 18438
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 18439
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 18440
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 18441
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 18442
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 18443
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 18444
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 18445
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 18446
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 18447
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 18448
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 18449
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 18450
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 18451
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 18452
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 18453
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 18454
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_UNSHELVE = 18455
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 18456
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESSEDORSHELVED = 18457
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_MAXTIMESHELVED = 18458
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_AUDIBLEENABLED = 18459
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_AUDIBLESOUND = 18460
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_AUDIBLESOUND_LISTID = 18461
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_AUDIBLESOUND_AGENCYID = 18462
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_AUDIBLESOUND_VERSIONID = 18463
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCESTATE = 18464
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCESTATE_ID = 18465
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCESTATE_NAME = 18466
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCESTATE_NUMBER = 18467
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 18468
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCESTATE_TRANSITIONTIME = 18469
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 18470
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCESTATE_TRUESTATE = 18471
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCESTATE_FALSESTATE = 18472
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ONDELAY = 18473
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_OFFDELAY = 18474
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_FIRSTINGROUPFLAG = 18475
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_FIRSTINGROUP = 18476
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LATCHEDSTATE = 18477
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LATCHEDSTATE_ID = 18478
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LATCHEDSTATE_NAME = 18479
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LATCHEDSTATE_NUMBER = 18480
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18481
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18482
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18483
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LATCHEDSTATE_TRUESTATE = 18484
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_LATCHEDSTATE_FALSESTATE = 18485
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_ALARMGROUP_PLACEHOLDER = 18486
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_REALARMTIME = 18487
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_REALARMREPEATCOUNT = 18488
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SILENCE = 18489
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_SUPPRESS = 18490
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_UNSUPPRESS = 18491
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_REMOVEFROMSERVICE = 18492
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_PLACEINSERVICE = 18493
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_RESET = 18494
    UA_NS0ID_INSTRUMENTDIAGNOSTICALARMTYPE_NORMALSTATE = 18495
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE = 18496
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_EVENTID = 18497
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_EVENTTYPE = 18498
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SOURCENODE = 18499
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SOURCENAME = 18500
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_TIME = 18501
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_RECEIVETIME = 18502
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LOCALTIME = 18503
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_MESSAGE = 18504
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SEVERITY = 18505
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONDITIONCLASSID = 18506
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONDITIONCLASSNAME = 18507
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONDITIONSUBCLASSID = 18508
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONDITIONSUBCLASSNAME = 18509
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONDITIONNAME = 18510
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_BRANCHID = 18511
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_RETAIN = 18512
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLEDSTATE = 18513
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLEDSTATE_ID = 18514
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLEDSTATE_NAME = 18515
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLEDSTATE_NUMBER = 18516
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 18517
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 18518
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 18519
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLEDSTATE_TRUESTATE = 18520
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLEDSTATE_FALSESTATE = 18521
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_QUALITY = 18522
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_QUALITY_SOURCETIMESTAMP = 18523
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LASTSEVERITY = 18524
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 18525
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_COMMENT = 18526
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_COMMENT_SOURCETIMESTAMP = 18527
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CLIENTUSERID = 18528
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_DISABLE = 18529
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ENABLE = 18530
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ADDCOMMENT = 18531
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 18532
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONDITIONREFRESH = 18533
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 18534
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONDITIONREFRESH2 = 18535
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 18536
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKEDSTATE = 18537
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKEDSTATE_ID = 18538
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKEDSTATE_NAME = 18539
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKEDSTATE_NUMBER = 18540
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 18541
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 18542
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 18543
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKEDSTATE_TRUESTATE = 18544
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKEDSTATE_FALSESTATE = 18545
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRMEDSTATE = 18546
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_ID = 18547
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_NAME = 18548
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_NUMBER = 18549
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 18550
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 18551
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 18552
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 18553
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 18554
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKNOWLEDGE = 18555
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 18556
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRM = 18557
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_CONFIRM_INPUTARGUMENTS = 18558
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACTIVESTATE = 18559
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACTIVESTATE_ID = 18560
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACTIVESTATE_NAME = 18561
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACTIVESTATE_NUMBER = 18562
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 18563
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 18564
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 18565
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACTIVESTATE_TRUESTATE = 18566
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ACTIVESTATE_FALSESTATE = 18567
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_INPUTNODE = 18568
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE = 18569
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_ID = 18570
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_NAME = 18571
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_NUMBER = 18572
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 18573
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 18574
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 18575
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 18576
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 18577
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE = 18578
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_ID = 18579
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_NAME = 18580
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_NUMBER = 18581
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 18582
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 18583
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 18584
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 18585
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 18586
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE = 18587
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 18588
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 18589
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 18590
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 18591
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 18592
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 18593
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 18594
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 18595
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 18596
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 18597
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 18598
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 18599
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 18600
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 18601
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 18602
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 18603
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_UNSHELVE = 18604
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 18605
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESSEDORSHELVED = 18606
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_MAXTIMESHELVED = 18607
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_AUDIBLEENABLED = 18608
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_AUDIBLESOUND = 18609
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_AUDIBLESOUND_LISTID = 18610
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_AUDIBLESOUND_AGENCYID = 18611
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_AUDIBLESOUND_VERSIONID = 18612
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCESTATE = 18613
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCESTATE_ID = 18614
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCESTATE_NAME = 18615
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCESTATE_NUMBER = 18616
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 18617
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCESTATE_TRANSITIONTIME = 18618
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 18619
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCESTATE_TRUESTATE = 18620
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCESTATE_FALSESTATE = 18621
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ONDELAY = 18622
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_OFFDELAY = 18623
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_FIRSTINGROUPFLAG = 18624
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_FIRSTINGROUP = 18625
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LATCHEDSTATE = 18626
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LATCHEDSTATE_ID = 18627
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LATCHEDSTATE_NAME = 18628
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LATCHEDSTATE_NUMBER = 18629
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18630
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18631
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18632
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LATCHEDSTATE_TRUESTATE = 18633
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_LATCHEDSTATE_FALSESTATE = 18634
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_ALARMGROUP_PLACEHOLDER = 18635
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_REALARMTIME = 18636
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_REALARMREPEATCOUNT = 18637
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SILENCE = 18638
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_SUPPRESS = 18639
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_UNSUPPRESS = 18640
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_REMOVEFROMSERVICE = 18641
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_PLACEINSERVICE = 18642
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_RESET = 18643
    UA_NS0ID_SYSTEMDIAGNOSTICALARMTYPE_NORMALSTATE = 18644
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LATCHEDSTATE = 18645
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LATCHEDSTATE_ID = 18646
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LATCHEDSTATE_NAME = 18647
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LATCHEDSTATE_NUMBER = 18648
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18649
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18650
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18651
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LATCHEDSTATE_TRUESTATE = 18652
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_LATCHEDSTATE_FALSESTATE = 18653
    UA_NS0ID_CERTIFICATEEXPIRATIONALARMTYPE_RESET = 18654
    UA_NS0ID_DISCREPANCYALARMTYPE_LATCHEDSTATE = 18655
    UA_NS0ID_DISCREPANCYALARMTYPE_LATCHEDSTATE_ID = 18656
    UA_NS0ID_DISCREPANCYALARMTYPE_LATCHEDSTATE_NAME = 18657
    UA_NS0ID_DISCREPANCYALARMTYPE_LATCHEDSTATE_NUMBER = 18658
    UA_NS0ID_DISCREPANCYALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 18659
    UA_NS0ID_DISCREPANCYALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 18660
    UA_NS0ID_DISCREPANCYALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 18661
    UA_NS0ID_DISCREPANCYALARMTYPE_LATCHEDSTATE_TRUESTATE = 18662
    UA_NS0ID_DISCREPANCYALARMTYPE_LATCHEDSTATE_FALSESTATE = 18663
    UA_NS0ID_DISCREPANCYALARMTYPE_RESET = 18664
    UA_NS0ID_STATISTICALCONDITIONCLASSTYPE = 18665
    UA_NS0ID_ALARMMETRICSTYPE_RESET = 18666
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS = 18667
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_DIAGNOSTICSLEVEL = 18668
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION = 18669
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 18670
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 18671
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 18672
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 18673
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR = 18674
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_ACTIVE = 18675
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 18676
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 18677
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 18678
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_RESET = 18679
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_SUBERROR = 18680
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS = 18681
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR = 18682
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 18683
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 18684
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 18685
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 18686
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 18687
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 18688
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 18689
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 18690
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 18691
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 18692
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 18693
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 18694
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 18695
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 18696
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 18697
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 18698
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 18699
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 18700
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 18701
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 18702
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 18703
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 18704
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 18705
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 18706
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 18707
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 18708
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 18709
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 18710
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 18711
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES = 18712
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_RESOLVEDADDRESS = 18713
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_CONNECTIONNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_RESOLVEDADDRESS_DIAGNOSTICSLEVEL = 18714
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS = 18715
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_DIAGNOSTICSLEVEL = 18716
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALINFORMATION = 18717
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 18718
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 18719
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 18720
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 18721
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALERROR = 18722
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALERROR_ACTIVE = 18723
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 18724
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 18725
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 18726
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_RESET = 18727
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_SUBERROR = 18728
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS = 18729
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEERROR = 18730
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 18731
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 18732
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 18733
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 18734
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 18735
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 18736
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 18737
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 18738
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 18739
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 18740
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 18741
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 18742
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 18743
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 18744
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 18745
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 18746
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 18747
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 18748
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 18749
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 18750
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 18751
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 18752
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 18753
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 18754
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 18755
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 18756
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 18757
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 18758
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 18759
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_LIVEVALUES = 18760
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETWRITERS = 18761
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETWRITERS_DIAGNOSTICSLEVEL = 18762
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETREADERS = 18763
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETREADERS_DIAGNOSTICSLEVEL = 18764
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETWRITERS = 18765
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETWRITERS_DIAGNOSTICSLEVEL = 18766
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETREADERS = 18767
    UA_NS0ID_PUBLISHSUBSCRIBETYPE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETREADERS_DIAGNOSTICSLEVEL = 18768
    UA_NS0ID_THREEDVECTORTYPE_X = 18769
    UA_NS0ID_THREEDVECTORTYPE_Y = 18770
    UA_NS0ID_THREEDVECTORTYPE_Z = 18771
    UA_NS0ID_CARTESIANCOORDINATESTYPE = 18772
    UA_NS0ID_CARTESIANCOORDINATESTYPE_LENGTHUNIT = 18773
    UA_NS0ID_THREEDCARTESIANCOORDINATESTYPE = 18774
    UA_NS0ID_THREEDCARTESIANCOORDINATESTYPE_LENGTHUNIT = 18775
    UA_NS0ID_THREEDCARTESIANCOORDINATESTYPE_X = 18776
    UA_NS0ID_THREEDCARTESIANCOORDINATESTYPE_Y = 18777
    UA_NS0ID_THREEDCARTESIANCOORDINATESTYPE_Z = 18778
    UA_NS0ID_ORIENTATIONTYPE = 18779
    UA_NS0ID_ORIENTATIONTYPE_ANGLEUNIT = 18780
    UA_NS0ID_THREEDORIENTATIONTYPE = 18781
    UA_NS0ID_THREEDORIENTATIONTYPE_ANGLEUNIT = 18782
    UA_NS0ID_THREEDORIENTATIONTYPE_A = 18783
    UA_NS0ID_THREEDORIENTATIONTYPE_B = 18784
    UA_NS0ID_THREEDORIENTATIONTYPE_C = 18785
    UA_NS0ID_FRAMETYPE = 18786
    UA_NS0ID_FRAMETYPE_ORIENTATION = 18787
    UA_NS0ID_FRAMETYPE_CONSTANT = 18788
    UA_NS0ID_FRAMETYPE_BASEFRAME = 18789
    UA_NS0ID_FRAMETYPE_FIXEDBASE = 18790
    UA_NS0ID_THREEDFRAMETYPE = 18791
    UA_NS0ID_THREEDFRAMETYPE_ORIENTATION = 18792
    UA_NS0ID_THREEDFRAMETYPE_CONSTANT = 18793
    UA_NS0ID_THREEDFRAMETYPE_BASEFRAME = 18794
    UA_NS0ID_THREEDFRAMETYPE_FIXEDBASE = 18795
    UA_NS0ID_THREEDFRAMETYPE_CARTESIANCOORDINATES = 18796
    UA_NS0ID_THREEDFRAMETYPE_CARTESIANCOORDINATES_LENGTHUNIT = 18797
    UA_NS0ID_THREEDFRAMETYPE_CARTESIANCOORDINATES_X = 18798
    UA_NS0ID_THREEDFRAMETYPE_CARTESIANCOORDINATES_Y = 18799
    UA_NS0ID_THREEDFRAMETYPE_CARTESIANCOORDINATES_Z = 18800
    UA_NS0ID_FRAMETYPE_CARTESIANCOORDINATES = 18801
    UA_NS0ID_FRAMETYPE_CARTESIANCOORDINATES_LENGTHUNIT = 18802
    UA_NS0ID_FRAMETYPE_ORIENTATION_ANGLEUNIT = 18803
    UA_NS0ID_HASWRITERGROUP = 18804
    UA_NS0ID_HASREADERGROUP = 18805
    UA_NS0ID_RATIONALNUMBER = 18806
    UA_NS0ID_VECTOR = 18807
    UA_NS0ID_THREEDVECTOR = 18808
    UA_NS0ID_CARTESIANCOORDINATES = 18809
    UA_NS0ID_THREEDCARTESIANCOORDINATES = 18810
    UA_NS0ID_ORIENTATION = 18811
    UA_NS0ID_THREEDORIENTATION = 18812
    UA_NS0ID_FRAME = 18813
    UA_NS0ID_THREEDFRAME = 18814
    UA_NS0ID_RATIONALNUMBER_ENCODING_DEFAULTBINARY = 18815
    UA_NS0ID_VECTOR_ENCODING_DEFAULTBINARY = 18816
    UA_NS0ID_THREEDVECTOR_ENCODING_DEFAULTBINARY = 18817
    UA_NS0ID_CARTESIANCOORDINATES_ENCODING_DEFAULTBINARY = 18818
    UA_NS0ID_THREEDCARTESIANCOORDINATES_ENCODING_DEFAULTBINARY = 18819
    UA_NS0ID_ORIENTATION_ENCODING_DEFAULTBINARY = 18820
    UA_NS0ID_THREEDORIENTATION_ENCODING_DEFAULTBINARY = 18821
    UA_NS0ID_FRAME_ENCODING_DEFAULTBINARY = 18822
    UA_NS0ID_THREEDFRAME_ENCODING_DEFAULTBINARY = 18823
    UA_NS0ID_OPCUA_BINARYSCHEMA_RATIONALNUMBER = 18824
    UA_NS0ID_OPCUA_BINARYSCHEMA_RATIONALNUMBER_DATATYPEVERSION = 18825
    UA_NS0ID_OPCUA_BINARYSCHEMA_RATIONALNUMBER_DICTIONARYFRAGMENT = 18826
    UA_NS0ID_OPCUA_BINARYSCHEMA_VECTOR = 18827
    UA_NS0ID_OPCUA_BINARYSCHEMA_VECTOR_DATATYPEVERSION = 18828
    UA_NS0ID_OPCUA_BINARYSCHEMA_VECTOR_DICTIONARYFRAGMENT = 18829
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDVECTOR = 18830
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDVECTOR_DATATYPEVERSION = 18831
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDVECTOR_DICTIONARYFRAGMENT = 18832
    UA_NS0ID_OPCUA_BINARYSCHEMA_CARTESIANCOORDINATES = 18833
    UA_NS0ID_OPCUA_BINARYSCHEMA_CARTESIANCOORDINATES_DATATYPEVERSION = 18834
    UA_NS0ID_OPCUA_BINARYSCHEMA_CARTESIANCOORDINATES_DICTIONARYFRAGMENT = 18835
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDCARTESIANCOORDINATES = 18836
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDCARTESIANCOORDINATES_DATATYPEVERSION = 18837
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDCARTESIANCOORDINATES_DICTIONARYFRAGMENT = 18838
    UA_NS0ID_OPCUA_BINARYSCHEMA_ORIENTATION = 18839
    UA_NS0ID_OPCUA_BINARYSCHEMA_ORIENTATION_DATATYPEVERSION = 18840
    UA_NS0ID_OPCUA_BINARYSCHEMA_ORIENTATION_DICTIONARYFRAGMENT = 18841
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDORIENTATION = 18842
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDORIENTATION_DATATYPEVERSION = 18843
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDORIENTATION_DICTIONARYFRAGMENT = 18844
    UA_NS0ID_OPCUA_BINARYSCHEMA_FRAME = 18845
    UA_NS0ID_OPCUA_BINARYSCHEMA_FRAME_DATATYPEVERSION = 18846
    UA_NS0ID_OPCUA_BINARYSCHEMA_FRAME_DICTIONARYFRAGMENT = 18847
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDFRAME = 18848
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDFRAME_DATATYPEVERSION = 18849
    UA_NS0ID_OPCUA_BINARYSCHEMA_THREEDFRAME_DICTIONARYFRAGMENT = 18850
    UA_NS0ID_RATIONALNUMBER_ENCODING_DEFAULTXML = 18851
    UA_NS0ID_VECTOR_ENCODING_DEFAULTXML = 18852
    UA_NS0ID_THREEDVECTOR_ENCODING_DEFAULTXML = 18853
    UA_NS0ID_CARTESIANCOORDINATES_ENCODING_DEFAULTXML = 18854
    UA_NS0ID_THREEDCARTESIANCOORDINATES_ENCODING_DEFAULTXML = 18855
    UA_NS0ID_ORIENTATION_ENCODING_DEFAULTXML = 18856
    UA_NS0ID_THREEDORIENTATION_ENCODING_DEFAULTXML = 18857
    UA_NS0ID_FRAME_ENCODING_DEFAULTXML = 18858
    UA_NS0ID_THREEDFRAME_ENCODING_DEFAULTXML = 18859
    UA_NS0ID_OPCUA_XMLSCHEMA_RATIONALNUMBER = 18860
    UA_NS0ID_OPCUA_XMLSCHEMA_RATIONALNUMBER_DATATYPEVERSION = 18861
    UA_NS0ID_OPCUA_XMLSCHEMA_RATIONALNUMBER_DICTIONARYFRAGMENT = 18862
    UA_NS0ID_OPCUA_XMLSCHEMA_VECTOR = 18863
    UA_NS0ID_OPCUA_XMLSCHEMA_VECTOR_DATATYPEVERSION = 18864
    UA_NS0ID_OPCUA_XMLSCHEMA_VECTOR_DICTIONARYFRAGMENT = 18865
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDVECTOR = 18866
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDVECTOR_DATATYPEVERSION = 18867
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDVECTOR_DICTIONARYFRAGMENT = 18868
    UA_NS0ID_OPCUA_XMLSCHEMA_CARTESIANCOORDINATES = 18869
    UA_NS0ID_OPCUA_XMLSCHEMA_CARTESIANCOORDINATES_DATATYPEVERSION = 18870
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS = 18871
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_DIAGNOSTICSLEVEL = 18872
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION = 18873
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 18874
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 18875
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 18876
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 18877
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR = 18878
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_ACTIVE = 18879
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 18880
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 18881
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 18882
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_RESET = 18883
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_SUBERROR = 18884
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS = 18885
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR = 18886
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 18887
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 18888
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 18889
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 18890
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 18891
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 18892
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 18893
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 18894
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 18895
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 18896
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 18897
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 18898
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 18899
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 18900
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 18901
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 18902
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 18903
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 18904
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 18905
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 18906
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 18907
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 18908
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 18909
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 18910
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 18911
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 18912
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 18913
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 18914
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 18915
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES = 18916
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES = 18917
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_ACTIVE = 18918
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_CLASSIFICATION = 18919
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_DIAGNOSTICSLEVEL = 18920
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_TIMEFIRSTCHANGE = 18921
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER = 18922
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER_DIAGNOSTICSLEVEL = 18923
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE = 18924
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE_DIAGNOSTICSLEVEL = 18925
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION = 18926
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION_DIAGNOSTICSLEVEL = 18927
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION = 18928
    UA_NS0ID_PUBLISHEDDATASETTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION_DIAGNOSTICSLEVEL = 18929
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS = 18930
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_DIAGNOSTICSLEVEL = 18931
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION = 18932
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 18933
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 18934
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 18935
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 18936
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR = 18937
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_ACTIVE = 18938
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 18939
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 18940
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 18941
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_RESET = 18942
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_SUBERROR = 18943
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS = 18944
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR = 18945
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 18946
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 18947
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 18948
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 18949
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 18950
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 18951
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 18952
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 18953
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 18954
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 18955
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 18956
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 18957
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 18958
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 18959
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 18960
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 18961
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 18962
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 18963
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 18964
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 18965
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 18966
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 18967
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 18968
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 18969
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 18970
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 18971
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 18972
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 18973
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 18974
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES = 18975
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES = 18976
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_ACTIVE = 18977
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_CLASSIFICATION = 18978
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_DIAGNOSTICSLEVEL = 18979
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_TIMEFIRSTCHANGE = 18980
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER = 18981
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER_DIAGNOSTICSLEVEL = 18982
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE = 18983
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE_DIAGNOSTICSLEVEL = 18984
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION = 18985
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION_DIAGNOSTICSLEVEL = 18986
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION = 18987
    UA_NS0ID_PUBLISHEDDATAITEMSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION_DIAGNOSTICSLEVEL = 18988
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS = 18989
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_DIAGNOSTICSLEVEL = 18990
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION = 18991
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 18992
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 18993
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 18994
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 18995
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR = 18996
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_ACTIVE = 18997
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 18998
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 18999
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 19000
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_RESET = 19001
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_SUBERROR = 19002
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS = 19003
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR = 19004
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 19005
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 19006
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19007
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19008
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 19009
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19010
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19011
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19012
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19013
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 19014
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19015
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19016
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19017
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19018
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 19019
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19020
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19021
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19022
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19023
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 19024
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19025
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19026
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19027
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19028
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 19029
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19030
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19031
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19032
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19033
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES = 19034
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES = 19035
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_ACTIVE = 19036
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_CLASSIFICATION = 19037
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_DIAGNOSTICSLEVEL = 19038
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_TIMEFIRSTCHANGE = 19039
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER = 19040
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER_DIAGNOSTICSLEVEL = 19041
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE = 19042
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_STATUSCODE_DIAGNOSTICSLEVEL = 19043
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION = 19044
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MAJORVERSION_DIAGNOSTICSLEVEL = 19045
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION = 19046
    UA_NS0ID_PUBLISHEDEVENTSTYPE_DATASETWRITERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_MINORVERSION_DIAGNOSTICSLEVEL = 19047
    UA_NS0ID_OPCUA_XMLSCHEMA_CARTESIANCOORDINATES_DICTIONARYFRAGMENT = 19048
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDCARTESIANCOORDINATES = 19049
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDCARTESIANCOORDINATES_DATATYPEVERSION = 19050
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDCARTESIANCOORDINATES_DICTIONARYFRAGMENT = 19051
    UA_NS0ID_OPCUA_XMLSCHEMA_ORIENTATION = 19052
    UA_NS0ID_OPCUA_XMLSCHEMA_ORIENTATION_DATATYPEVERSION = 19053
    UA_NS0ID_OPCUA_XMLSCHEMA_ORIENTATION_DICTIONARYFRAGMENT = 19054
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDORIENTATION = 19055
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDORIENTATION_DATATYPEVERSION = 19056
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDORIENTATION_DICTIONARYFRAGMENT = 19057
    UA_NS0ID_OPCUA_XMLSCHEMA_FRAME = 19058
    UA_NS0ID_OPCUA_XMLSCHEMA_FRAME_DATATYPEVERSION = 19059
    UA_NS0ID_OPCUA_XMLSCHEMA_FRAME_DICTIONARYFRAGMENT = 19060
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDFRAME = 19061
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDFRAME_DATATYPEVERSION = 19062
    UA_NS0ID_OPCUA_XMLSCHEMA_THREEDFRAME_DICTIONARYFRAGMENT = 19063
    UA_NS0ID_RATIONALNUMBER_ENCODING_DEFAULTJSON = 19064
    UA_NS0ID_VECTOR_ENCODING_DEFAULTJSON = 19065
    UA_NS0ID_THREEDVECTOR_ENCODING_DEFAULTJSON = 19066
    UA_NS0ID_CARTESIANCOORDINATES_ENCODING_DEFAULTJSON = 19067
    UA_NS0ID_THREEDCARTESIANCOORDINATES_ENCODING_DEFAULTJSON = 19068
    UA_NS0ID_ORIENTATION_ENCODING_DEFAULTJSON = 19069
    UA_NS0ID_THREEDORIENTATION_ENCODING_DEFAULTJSON = 19070
    UA_NS0ID_FRAME_ENCODING_DEFAULTJSON = 19071
    UA_NS0ID_THREEDFRAME_ENCODING_DEFAULTJSON = 19072
    UA_NS0ID_THREEDFRAMETYPE_ORIENTATION_ANGLEUNIT = 19073
    UA_NS0ID_THREEDFRAMETYPE_ORIENTATION_A = 19074
    UA_NS0ID_THREEDFRAMETYPE_ORIENTATION_B = 19075
    UA_NS0ID_THREEDFRAMETYPE_ORIENTATION_C = 19076
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETEBASETYPE = 19077
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETEBASETYPE_DEFINITION = 19078
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETEBASETYPE_VALUEPRECISION = 19079
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETEBASETYPE_ENUMVALUES = 19080
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETEBASETYPE_VALUEASTEXT = 19081
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETEBASETYPE_ENUMDICTIONARYENTRIES = 19082
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETEBASETYPE_VALUEASDICTIONARYENTRIES = 19083
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETETYPE = 19084
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETETYPE_DEFINITION = 19085
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETETYPE_VALUEPRECISION = 19086
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETETYPE_ENUMVALUES = 19087
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETETYPE_VALUEASTEXT = 19088
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETETYPE_ENUMDICTIONARYENTRIES = 19089
    UA_NS0ID_MULTISTATEDICTIONARYENTRYDISCRETETYPE_VALUEASDICTIONARYENTRIES = 19090
    UA_NS0ID_HISTORYSERVERCAPABILITIES_SERVERTIMESTAMPSUPPORTED = 19091
    UA_NS0ID_HISTORICALDATACONFIGURATIONTYPE_SERVERTIMESTAMPSUPPORTED = 19092
    UA_NS0ID_HACONFIGURATION_SERVERTIMESTAMPSUPPORTED = 19093
    UA_NS0ID_HISTORYSERVERCAPABILITIESTYPE_SERVERTIMESTAMPSUPPORTED = 19094
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE = 19095
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_EVENTID = 19096
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_EVENTTYPE = 19097
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_SOURCENODE = 19098
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_SOURCENAME = 19099
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_TIME = 19100
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_RECEIVETIME = 19101
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_LOCALTIME = 19102
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_MESSAGE = 19103
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_SEVERITY = 19104
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_ACTIONTIMESTAMP = 19105
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_STATUS = 19106
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS = 19107
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_DIAGNOSTICSLEVEL = 19108
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION = 19109
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 19110
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 19111
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19112
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 19113
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR = 19114
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_ACTIVE = 19115
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 19116
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 19117
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 19118
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_RESET = 19119
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_SUBERROR = 19120
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS = 19121
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR = 19122
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 19123
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 19124
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19125
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19126
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 19127
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19128
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19129
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19130
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19131
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 19132
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19133
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19134
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19135
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19136
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 19137
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19138
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19139
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19140
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19141
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 19142
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19143
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19144
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19145
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19146
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 19147
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19148
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19149
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19150
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19151
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES = 19152
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES = 19153
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES_ACTIVE = 19154
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES_CLASSIFICATION = 19155
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES_DIAGNOSTICSLEVEL = 19156
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_SENTNETWORKMESSAGES_TIMEFIRSTCHANGE = 19157
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS = 19158
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS_ACTIVE = 19159
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS_CLASSIFICATION = 19160
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS_DIAGNOSTICSLEVEL = 19161
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_FAILEDTRANSMISSIONS_TIMEFIRSTCHANGE = 19162
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS = 19163
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS_ACTIVE = 19164
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS_CLASSIFICATION = 19165
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS_DIAGNOSTICSLEVEL = 19166
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_ENCRYPTIONERRORS_TIMEFIRSTCHANGE = 19167
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETWRITERS = 19168
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETWRITERS_DIAGNOSTICSLEVEL = 19169
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETWRITERS = 19170
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETWRITERS_DIAGNOSTICSLEVEL = 19171
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_SECURITYTOKENID = 19172
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_SECURITYTOKENID_DIAGNOSTICSLEVEL = 19173
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_TIMETONEXTTOKENID = 19174
    UA_NS0ID_PUBSUBCONNECTIONTYPE_WRITERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_TIMETONEXTTOKENID_DIAGNOSTICSLEVEL = 19175
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS = 19176
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_DIAGNOSTICSLEVEL = 19177
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION = 19178
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 19179
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 19180
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19181
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 19182
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR = 19183
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_ACTIVE = 19184
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 19185
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 19186
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 19187
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_RESET = 19188
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_SUBERROR = 19189
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS = 19190
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR = 19191
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 19192
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 19193
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19194
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19195
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 19196
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19197
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19198
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19199
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19200
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 19201
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19202
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19203
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19204
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19205
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 19206
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19207
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19208
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19209
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19210
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 19211
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19212
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19213
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19214
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19215
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 19216
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19217
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19218
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19219
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19220
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES = 19221
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES = 19222
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES_ACTIVE = 19223
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES_CLASSIFICATION = 19224
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES_DIAGNOSTICSLEVEL = 19225
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES_TIMEFIRSTCHANGE = 19226
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES = 19227
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_ACTIVE = 19228
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_CLASSIFICATION = 19229
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_DIAGNOSTICSLEVEL = 19230
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_TIMEFIRSTCHANGE = 19231
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS = 19232
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_ACTIVE = 19233
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_CLASSIFICATION = 19234
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_DIAGNOSTICSLEVEL = 19235
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_TIMEFIRSTCHANGE = 19236
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETREADERS = 19237
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETREADERS_DIAGNOSTICSLEVEL = 19238
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETREADERS = 19239
    UA_NS0ID_PUBSUBCONNECTIONTYPE_READERGROUPNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETREADERS_DIAGNOSTICSLEVEL = 19240
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS = 19241
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_DIAGNOSTICSLEVEL = 19242
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALINFORMATION = 19243
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 19244
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 19245
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19246
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 19247
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALERROR = 19248
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALERROR_ACTIVE = 19249
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 19250
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 19251
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 19252
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_RESET = 19253
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_SUBERROR = 19254
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS = 19255
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEERROR = 19256
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 19257
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 19258
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19259
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19260
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 19261
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19262
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19263
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19264
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19265
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 19266
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19267
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19268
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19269
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19270
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 19271
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19272
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19273
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19274
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19275
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 19276
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19277
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19278
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19279
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19280
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 19281
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19282
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19283
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19284
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19285
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_LIVEVALUES = 19286
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_LIVEVALUES_RESOLVEDADDRESS = 19287
    UA_NS0ID_PUBSUBCONNECTIONTYPE_DIAGNOSTICS_LIVEVALUES_RESOLVEDADDRESS_DIAGNOSTICSLEVEL = 19288
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_SERVERID = 19289
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_CLIENTAUDITENTRYID = 19290
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_CLIENTUSERID = 19291
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_PARAMETERDATATYPEID = 19292
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_PERFORMINSERTREPLACE = 19293
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_NEWVALUES = 19294
    UA_NS0ID_AUDITHISTORYANNOTATIONUPDATEEVENTTYPE_OLDVALUES = 19295
    UA_NS0ID_TRUSTLISTTYPE_UPDATEFREQUENCY = 19296
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE = 19297
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_EVENTID = 19298
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_EVENTTYPE = 19299
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SOURCENODE = 19300
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SOURCENAME = 19301
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_TIME = 19302
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_RECEIVETIME = 19303
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LOCALTIME = 19304
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_MESSAGE = 19305
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SEVERITY = 19306
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONDITIONCLASSID = 19307
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONDITIONCLASSNAME = 19308
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONDITIONSUBCLASSID = 19309
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONDITIONSUBCLASSNAME = 19310
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONDITIONNAME = 19311
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_BRANCHID = 19312
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_RETAIN = 19313
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLEDSTATE = 19314
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLEDSTATE_ID = 19315
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLEDSTATE_NAME = 19316
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLEDSTATE_NUMBER = 19317
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLEDSTATE_EFFECTIVEDISPLAYNAME = 19318
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLEDSTATE_TRANSITIONTIME = 19319
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLEDSTATE_EFFECTIVETRANSITIONTIME = 19320
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLEDSTATE_TRUESTATE = 19321
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLEDSTATE_FALSESTATE = 19322
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_QUALITY = 19323
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_QUALITY_SOURCETIMESTAMP = 19324
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LASTSEVERITY = 19325
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LASTSEVERITY_SOURCETIMESTAMP = 19326
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_COMMENT = 19327
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_COMMENT_SOURCETIMESTAMP = 19328
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CLIENTUSERID = 19329
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_DISABLE = 19330
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ENABLE = 19331
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ADDCOMMENT = 19332
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ADDCOMMENT_INPUTARGUMENTS = 19333
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONDITIONREFRESH = 19334
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONDITIONREFRESH_INPUTARGUMENTS = 19335
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONDITIONREFRESH2 = 19336
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONDITIONREFRESH2_INPUTARGUMENTS = 19337
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKEDSTATE = 19338
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKEDSTATE_ID = 19339
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKEDSTATE_NAME = 19340
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKEDSTATE_NUMBER = 19341
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKEDSTATE_EFFECTIVEDISPLAYNAME = 19342
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKEDSTATE_TRANSITIONTIME = 19343
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKEDSTATE_EFFECTIVETRANSITIONTIME = 19344
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKEDSTATE_TRUESTATE = 19345
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKEDSTATE_FALSESTATE = 19346
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRMEDSTATE = 19347
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRMEDSTATE_ID = 19348
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRMEDSTATE_NAME = 19349
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRMEDSTATE_NUMBER = 19350
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRMEDSTATE_EFFECTIVEDISPLAYNAME = 19351
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRMEDSTATE_TRANSITIONTIME = 19352
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRMEDSTATE_EFFECTIVETRANSITIONTIME = 19353
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRMEDSTATE_TRUESTATE = 19354
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRMEDSTATE_FALSESTATE = 19355
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKNOWLEDGE = 19356
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACKNOWLEDGE_INPUTARGUMENTS = 19357
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRM = 19358
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_CONFIRM_INPUTARGUMENTS = 19359
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACTIVESTATE = 19360
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACTIVESTATE_ID = 19361
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACTIVESTATE_NAME = 19362
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACTIVESTATE_NUMBER = 19363
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACTIVESTATE_EFFECTIVEDISPLAYNAME = 19364
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACTIVESTATE_TRANSITIONTIME = 19365
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACTIVESTATE_EFFECTIVETRANSITIONTIME = 19366
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACTIVESTATE_TRUESTATE = 19367
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ACTIVESTATE_FALSESTATE = 19368
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_INPUTNODE = 19369
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDSTATE = 19370
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDSTATE_ID = 19371
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDSTATE_NAME = 19372
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDSTATE_NUMBER = 19373
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDSTATE_EFFECTIVEDISPLAYNAME = 19374
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDSTATE_TRANSITIONTIME = 19375
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDSTATE_EFFECTIVETRANSITIONTIME = 19376
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDSTATE_TRUESTATE = 19377
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDSTATE_FALSESTATE = 19378
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OUTOFSERVICESTATE = 19379
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OUTOFSERVICESTATE_ID = 19380
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OUTOFSERVICESTATE_NAME = 19381
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OUTOFSERVICESTATE_NUMBER = 19382
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OUTOFSERVICESTATE_EFFECTIVEDISPLAYNAME = 19383
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OUTOFSERVICESTATE_TRANSITIONTIME = 19384
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OUTOFSERVICESTATE_EFFECTIVETRANSITIONTIME = 19385
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OUTOFSERVICESTATE_TRUESTATE = 19386
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OUTOFSERVICESTATE_FALSESTATE = 19387
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE = 19388
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_CURRENTSTATE = 19389
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_ID = 19390
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NAME = 19391
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_NUMBER = 19392
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_CURRENTSTATE_EFFECTIVEDISPLAYNAME = 19393
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_LASTTRANSITION = 19394
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_ID = 19395
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NAME = 19396
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_NUMBER = 19397
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_TRANSITIONTIME = 19398
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_LASTTRANSITION_EFFECTIVETRANSITIONTIME = 19399
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_AVAILABLESTATES = 19400
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_AVAILABLETRANSITIONS = 19401
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_UNSHELVETIME = 19402
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_TIMEDSHELVE = 19403
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_TIMEDSHELVE_INPUTARGUMENTS = 19404
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_UNSHELVE = 19405
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SHELVINGSTATE_ONESHOTSHELVE = 19406
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESSEDORSHELVED = 19407
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_MAXTIMESHELVED = 19408
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_AUDIBLEENABLED = 19409
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_AUDIBLESOUND = 19410
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_AUDIBLESOUND_LISTID = 19411
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_AUDIBLESOUND_AGENCYID = 19412
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_AUDIBLESOUND_VERSIONID = 19413
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCESTATE = 19414
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCESTATE_ID = 19415
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCESTATE_NAME = 19416
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCESTATE_NUMBER = 19417
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCESTATE_EFFECTIVEDISPLAYNAME = 19418
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCESTATE_TRANSITIONTIME = 19419
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCESTATE_EFFECTIVETRANSITIONTIME = 19420
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCESTATE_TRUESTATE = 19421
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCESTATE_FALSESTATE = 19422
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ONDELAY = 19423
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_OFFDELAY = 19424
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_FIRSTINGROUPFLAG = 19425
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_FIRSTINGROUP = 19426
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LATCHEDSTATE = 19427
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LATCHEDSTATE_ID = 19428
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LATCHEDSTATE_NAME = 19429
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LATCHEDSTATE_NUMBER = 19430
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LATCHEDSTATE_EFFECTIVEDISPLAYNAME = 19431
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LATCHEDSTATE_TRANSITIONTIME = 19432
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LATCHEDSTATE_EFFECTIVETRANSITIONTIME = 19433
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LATCHEDSTATE_TRUESTATE = 19434
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LATCHEDSTATE_FALSESTATE = 19435
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_ALARMGROUP_PLACEHOLDER = 19436
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_REALARMTIME = 19437
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_REALARMREPEATCOUNT = 19438
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SILENCE = 19439
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_SUPPRESS = 19440
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_UNSUPPRESS = 19441
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_REMOVEFROMSERVICE = 19442
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_PLACEINSERVICE = 19443
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_RESET = 19444
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_NORMALSTATE = 19445
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_TRUSTLISTID = 19446
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_LASTUPDATETIME = 19447
    UA_NS0ID_TRUSTLISTOUTOFDATEALARMTYPE_UPDATEFREQUENCY = 19448
    UA_NS0ID_CERTIFICATEGROUPTYPE_TRUSTLIST_UPDATEFREQUENCY = 19449
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS = 19550
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_DIAGNOSTICSLEVEL = 19551
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALINFORMATION = 19552
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 19553
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 19554
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19555
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 19556
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALERROR = 19557
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALERROR_ACTIVE = 19558
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 19559
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 19560
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 19561
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_RESET = 19562
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_SUBERROR = 19563
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS = 19564
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR = 19565
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 19566
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 19567
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19568
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19569
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 19570
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19571
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19572
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19573
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19574
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 19575
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19576
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19577
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19578
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19579
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 19580
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19581
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19582
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19583
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19584
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 19585
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19586
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19587
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19588
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19589
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 19590
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19591
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19592
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19593
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19594
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_LIVEVALUES = 19595
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES = 19596
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_ACTIVE = 19597
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_CLASSIFICATION = 19598
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_DIAGNOSTICSLEVEL = 19599
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_TIMEFIRSTCHANGE = 19600
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER = 19601
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER_DIAGNOSTICSLEVEL = 19602
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_LIVEVALUES_STATUSCODE = 19603
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_LIVEVALUES_STATUSCODE_DIAGNOSTICSLEVEL = 19604
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_LIVEVALUES_MAJORVERSION = 19605
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_LIVEVALUES_MAJORVERSION_DIAGNOSTICSLEVEL = 19606
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_LIVEVALUES_MINORVERSION = 19607
    UA_NS0ID_DATASETWRITERTYPE_DIAGNOSTICS_LIVEVALUES_MINORVERSION_DIAGNOSTICSLEVEL = 19608
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS = 19609
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_DIAGNOSTICSLEVEL = 19610
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALINFORMATION = 19611
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 19612
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 19613
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19614
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 19615
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALERROR = 19616
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALERROR_ACTIVE = 19617
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 19618
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 19619
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 19620
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_RESET = 19621
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_SUBERROR = 19622
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS = 19623
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR = 19624
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 19625
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 19626
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19627
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19628
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 19629
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19630
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19631
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19632
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19633
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 19634
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19635
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19636
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19637
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19638
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 19639
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19640
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19641
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19642
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19643
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 19644
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19645
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19646
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19647
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19648
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 19649
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19650
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19651
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19652
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19653
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES = 19654
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES = 19655
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_ACTIVE = 19656
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_CLASSIFICATION = 19657
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_DIAGNOSTICSLEVEL = 19658
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_FAILEDDATASETMESSAGES_TIMEFIRSTCHANGE = 19659
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS = 19660
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_ACTIVE = 19661
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_CLASSIFICATION = 19662
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_DIAGNOSTICSLEVEL = 19663
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_TIMEFIRSTCHANGE = 19664
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER = 19665
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_MESSAGESEQUENCENUMBER_DIAGNOSTICSLEVEL = 19666
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_STATUSCODE = 19667
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_STATUSCODE_DIAGNOSTICSLEVEL = 19668
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_MAJORVERSION = 19669
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_MAJORVERSION_DIAGNOSTICSLEVEL = 19670
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_MINORVERSION = 19671
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_MINORVERSION_DIAGNOSTICSLEVEL = 19672
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_SECURITYTOKENID = 19673
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_SECURITYTOKENID_DIAGNOSTICSLEVEL = 19674
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_TIMETONEXTTOKENID = 19675
    UA_NS0ID_DATASETREADERTYPE_DIAGNOSTICS_LIVEVALUES_TIMETONEXTTOKENID_DIAGNOSTICSLEVEL = 19676
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE = 19677
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_DIAGNOSTICSLEVEL = 19678
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALINFORMATION = 19679
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALINFORMATION_ACTIVE = 19680
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALINFORMATION_CLASSIFICATION = 19681
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19682
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALINFORMATION_TIMEFIRSTCHANGE = 19683
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALERROR = 19684
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALERROR_ACTIVE = 19685
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALERROR_CLASSIFICATION = 19686
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALERROR_DIAGNOSTICSLEVEL = 19687
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_TOTALERROR_TIMEFIRSTCHANGE = 19688
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_RESET = 19689
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_SUBERROR = 19690
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS = 19691
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEERROR = 19692
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEERROR_ACTIVE = 19693
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEERROR_CLASSIFICATION = 19694
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19695
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19696
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYMETHOD = 19697
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19698
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19699
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19700
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19701
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYPARENT = 19702
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19703
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19704
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19705
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19706
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALFROMERROR = 19707
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19708
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19709
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19710
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19711
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEPAUSEDBYPARENT = 19712
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19713
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19714
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19715
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19716
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEDISABLEDBYMETHOD = 19717
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19718
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19719
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19720
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19721
    UA_NS0ID_PUBSUBDIAGNOSTICSTYPE_LIVEVALUES = 19722
    UA_NS0ID_DIAGNOSTICSLEVEL = 19723
    UA_NS0ID_DIAGNOSTICSLEVEL_ENUMSTRINGS = 19724
    UA_NS0ID_PUBSUBDIAGNOSTICSCOUNTERTYPE = 19725
    UA_NS0ID_PUBSUBDIAGNOSTICSCOUNTERTYPE_ACTIVE = 19726
    UA_NS0ID_PUBSUBDIAGNOSTICSCOUNTERTYPE_CLASSIFICATION = 19727
    UA_NS0ID_PUBSUBDIAGNOSTICSCOUNTERTYPE_DIAGNOSTICSLEVEL = 19728
    UA_NS0ID_PUBSUBDIAGNOSTICSCOUNTERTYPE_TIMEFIRSTCHANGE = 19729
    UA_NS0ID_PUBSUBDIAGNOSTICSCOUNTERCLASSIFICATION = 19730
    UA_NS0ID_PUBSUBDIAGNOSTICSCOUNTERCLASSIFICATION_ENUMSTRINGS = 19731
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE = 19732
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_DIAGNOSTICSLEVEL = 19733
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALINFORMATION = 19734
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALINFORMATION_ACTIVE = 19735
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALINFORMATION_CLASSIFICATION = 19736
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19737
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALINFORMATION_TIMEFIRSTCHANGE = 19738
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALERROR = 19739
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALERROR_ACTIVE = 19740
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALERROR_CLASSIFICATION = 19741
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALERROR_DIAGNOSTICSLEVEL = 19742
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_TOTALERROR_TIMEFIRSTCHANGE = 19743
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_RESET = 19744
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_SUBERROR = 19745
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS = 19746
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEERROR = 19747
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEERROR_ACTIVE = 19748
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEERROR_CLASSIFICATION = 19749
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19750
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19751
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYMETHOD = 19752
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19753
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19754
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19755
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19756
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYPARENT = 19757
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19758
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19759
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19760
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19761
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALFROMERROR = 19762
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19763
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19764
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19765
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19766
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEPAUSEDBYPARENT = 19767
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19768
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19769
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19770
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19771
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEDISABLEDBYMETHOD = 19772
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19773
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19774
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19775
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19776
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_LIVEVALUES = 19777
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_LIVEVALUES_CONFIGUREDDATASETWRITERS = 19778
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_LIVEVALUES_CONFIGUREDDATASETWRITERS_DIAGNOSTICSLEVEL = 19779
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_LIVEVALUES_CONFIGUREDDATASETREADERS = 19780
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_LIVEVALUES_CONFIGUREDDATASETREADERS_DIAGNOSTICSLEVEL = 19781
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_LIVEVALUES_OPERATIONALDATASETWRITERS = 19782
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_LIVEVALUES_OPERATIONALDATASETWRITERS_DIAGNOSTICSLEVEL = 19783
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_LIVEVALUES_OPERATIONALDATASETREADERS = 19784
    UA_NS0ID_PUBSUBDIAGNOSTICSROOTTYPE_LIVEVALUES_OPERATIONALDATASETREADERS_DIAGNOSTICSLEVEL = 19785
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE = 19786
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_DIAGNOSTICSLEVEL = 19787
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALINFORMATION = 19788
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALINFORMATION_ACTIVE = 19789
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALINFORMATION_CLASSIFICATION = 19790
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19791
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALINFORMATION_TIMEFIRSTCHANGE = 19792
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALERROR = 19793
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALERROR_ACTIVE = 19794
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALERROR_CLASSIFICATION = 19795
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALERROR_DIAGNOSTICSLEVEL = 19796
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_TOTALERROR_TIMEFIRSTCHANGE = 19797
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_RESET = 19798
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_SUBERROR = 19799
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS = 19800
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEERROR = 19801
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEERROR_ACTIVE = 19802
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEERROR_CLASSIFICATION = 19803
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19804
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19805
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYMETHOD = 19806
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19807
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19808
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19809
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19810
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYPARENT = 19811
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19812
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19813
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19814
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19815
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALFROMERROR = 19816
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19817
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19818
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19819
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19820
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEPAUSEDBYPARENT = 19821
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19822
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19823
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19824
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19825
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEDISABLEDBYMETHOD = 19826
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19827
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19828
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19829
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19830
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_LIVEVALUES = 19831
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_LIVEVALUES_RESOLVEDADDRESS = 19832
    UA_NS0ID_PUBSUBDIAGNOSTICSCONNECTIONTYPE_LIVEVALUES_RESOLVEDADDRESS_DIAGNOSTICSLEVEL = 19833
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE = 19834
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_DIAGNOSTICSLEVEL = 19835
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALINFORMATION = 19836
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALINFORMATION_ACTIVE = 19837
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALINFORMATION_CLASSIFICATION = 19838
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19839
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALINFORMATION_TIMEFIRSTCHANGE = 19840
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALERROR = 19841
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALERROR_ACTIVE = 19842
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALERROR_CLASSIFICATION = 19843
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALERROR_DIAGNOSTICSLEVEL = 19844
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_TOTALERROR_TIMEFIRSTCHANGE = 19845
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_RESET = 19846
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_SUBERROR = 19847
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS = 19848
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEERROR = 19849
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEERROR_ACTIVE = 19850
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEERROR_CLASSIFICATION = 19851
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19852
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19853
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD = 19854
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19855
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19856
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19857
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19858
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT = 19859
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19860
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19861
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19862
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19863
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR = 19864
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19865
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19866
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19867
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19868
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT = 19869
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19870
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19871
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19872
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19873
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD = 19874
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19875
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19876
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19877
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19878
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_LIVEVALUES = 19879
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_SENTNETWORKMESSAGES = 19880
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_SENTNETWORKMESSAGES_ACTIVE = 19881
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_SENTNETWORKMESSAGES_CLASSIFICATION = 19882
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_SENTNETWORKMESSAGES_DIAGNOSTICSLEVEL = 19883
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_SENTNETWORKMESSAGES_TIMEFIRSTCHANGE = 19884
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_FAILEDTRANSMISSIONS = 19885
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_FAILEDTRANSMISSIONS_ACTIVE = 19886
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_FAILEDTRANSMISSIONS_CLASSIFICATION = 19887
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_FAILEDTRANSMISSIONS_DIAGNOSTICSLEVEL = 19888
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_FAILEDTRANSMISSIONS_TIMEFIRSTCHANGE = 19889
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_ENCRYPTIONERRORS = 19890
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_ENCRYPTIONERRORS_ACTIVE = 19891
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_ENCRYPTIONERRORS_CLASSIFICATION = 19892
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_ENCRYPTIONERRORS_DIAGNOSTICSLEVEL = 19893
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_COUNTERS_ENCRYPTIONERRORS_TIMEFIRSTCHANGE = 19894
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_LIVEVALUES_CONFIGUREDDATASETWRITERS = 19895
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_LIVEVALUES_CONFIGUREDDATASETWRITERS_DIAGNOSTICSLEVEL = 19896
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_LIVEVALUES_OPERATIONALDATASETWRITERS = 19897
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_LIVEVALUES_OPERATIONALDATASETWRITERS_DIAGNOSTICSLEVEL = 19898
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_LIVEVALUES_SECURITYTOKENID = 19899
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_LIVEVALUES_SECURITYTOKENID_DIAGNOSTICSLEVEL = 19900
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_LIVEVALUES_TIMETONEXTTOKENID = 19901
    UA_NS0ID_PUBSUBDIAGNOSTICSWRITERGROUPTYPE_LIVEVALUES_TIMETONEXTTOKENID_DIAGNOSTICSLEVEL = 19902
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE = 19903
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_DIAGNOSTICSLEVEL = 19904
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALINFORMATION = 19905
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALINFORMATION_ACTIVE = 19906
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALINFORMATION_CLASSIFICATION = 19907
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19908
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALINFORMATION_TIMEFIRSTCHANGE = 19909
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALERROR = 19910
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALERROR_ACTIVE = 19911
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALERROR_CLASSIFICATION = 19912
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALERROR_DIAGNOSTICSLEVEL = 19913
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_TOTALERROR_TIMEFIRSTCHANGE = 19914
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_RESET = 19915
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_SUBERROR = 19916
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS = 19917
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEERROR = 19918
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEERROR_ACTIVE = 19919
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEERROR_CLASSIFICATION = 19920
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19921
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19922
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD = 19923
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19924
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19925
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19926
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19927
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT = 19928
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19929
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19930
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19931
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19932
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR = 19933
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19934
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 19935
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 19936
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 19937
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT = 19938
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 19939
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 19940
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 19941
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 19942
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD = 19943
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 19944
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 19945
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 19946
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 19947
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_LIVEVALUES = 19948
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDNETWORKMESSAGES = 19949
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDNETWORKMESSAGES_ACTIVE = 19950
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDNETWORKMESSAGES_CLASSIFICATION = 19951
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDNETWORKMESSAGES_DIAGNOSTICSLEVEL = 19952
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDNETWORKMESSAGES_TIMEFIRSTCHANGE = 19953
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES = 19954
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_ACTIVE = 19955
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_CLASSIFICATION = 19956
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_DIAGNOSTICSLEVEL = 19957
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_TIMEFIRSTCHANGE = 19958
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_DECRYPTIONERRORS = 19959
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_DECRYPTIONERRORS_ACTIVE = 19960
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_DECRYPTIONERRORS_CLASSIFICATION = 19961
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_DECRYPTIONERRORS_DIAGNOSTICSLEVEL = 19962
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_COUNTERS_DECRYPTIONERRORS_TIMEFIRSTCHANGE = 19963
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_LIVEVALUES_CONFIGUREDDATASETREADERS = 19964
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_LIVEVALUES_CONFIGUREDDATASETREADERS_DIAGNOSTICSLEVEL = 19965
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_LIVEVALUES_OPERATIONALDATASETREADERS = 19966
    UA_NS0ID_PUBSUBDIAGNOSTICSREADERGROUPTYPE_LIVEVALUES_OPERATIONALDATASETREADERS_DIAGNOSTICSLEVEL = 19967
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE = 19968
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_DIAGNOSTICSLEVEL = 19969
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALINFORMATION = 19970
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALINFORMATION_ACTIVE = 19971
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALINFORMATION_CLASSIFICATION = 19972
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALINFORMATION_DIAGNOSTICSLEVEL = 19973
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALINFORMATION_TIMEFIRSTCHANGE = 19974
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALERROR = 19975
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALERROR_ACTIVE = 19976
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALERROR_CLASSIFICATION = 19977
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALERROR_DIAGNOSTICSLEVEL = 19978
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_TOTALERROR_TIMEFIRSTCHANGE = 19979
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_RESET = 19980
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_SUBERROR = 19981
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS = 19982
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEERROR = 19983
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEERROR_ACTIVE = 19984
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEERROR_CLASSIFICATION = 19985
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 19986
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 19987
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD = 19988
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 19989
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 19990
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 19991
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 19992
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYPARENT = 19993
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 19994
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 19995
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 19996
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 19997
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALFROMERROR = 19998
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 19999
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 20000
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 20001
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 20002
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEPAUSEDBYPARENT = 20003
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 20004
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 20005
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 20006
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 20007
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEDISABLEDBYMETHOD = 20008
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 20009
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 20010
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 20011
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 20012
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_LIVEVALUES = 20013
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_FAILEDDATASETMESSAGES = 20014
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_FAILEDDATASETMESSAGES_ACTIVE = 20015
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_FAILEDDATASETMESSAGES_CLASSIFICATION = 20016
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_FAILEDDATASETMESSAGES_DIAGNOSTICSLEVEL = 20017
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_COUNTERS_FAILEDDATASETMESSAGES_TIMEFIRSTCHANGE = 20018
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_LIVEVALUES_MESSAGESEQUENCENUMBER = 20019
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_LIVEVALUES_MESSAGESEQUENCENUMBER_DIAGNOSTICSLEVEL = 20020
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_LIVEVALUES_STATUSCODE = 20021
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_LIVEVALUES_STATUSCODE_DIAGNOSTICSLEVEL = 20022
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_LIVEVALUES_MAJORVERSION = 20023
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_LIVEVALUES_MAJORVERSION_DIAGNOSTICSLEVEL = 20024
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_LIVEVALUES_MINORVERSION = 20025
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETWRITERTYPE_LIVEVALUES_MINORVERSION_DIAGNOSTICSLEVEL = 20026
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE = 20027
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_DIAGNOSTICSLEVEL = 20028
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALINFORMATION = 20029
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALINFORMATION_ACTIVE = 20030
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALINFORMATION_CLASSIFICATION = 20031
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALINFORMATION_DIAGNOSTICSLEVEL = 20032
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALINFORMATION_TIMEFIRSTCHANGE = 20033
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALERROR = 20034
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALERROR_ACTIVE = 20035
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALERROR_CLASSIFICATION = 20036
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALERROR_DIAGNOSTICSLEVEL = 20037
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_TOTALERROR_TIMEFIRSTCHANGE = 20038
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_RESET = 20039
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_SUBERROR = 20040
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS = 20041
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEERROR = 20042
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEERROR_ACTIVE = 20043
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEERROR_CLASSIFICATION = 20044
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 20045
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 20046
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD = 20047
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 20048
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 20049
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 20050
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 20051
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYPARENT = 20052
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 20053
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 20054
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 20055
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 20056
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALFROMERROR = 20057
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 20058
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 20059
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 20060
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 20061
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEPAUSEDBYPARENT = 20062
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 20063
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 20064
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 20065
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 20066
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEDISABLEDBYMETHOD = 20067
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 20068
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 20069
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 20070
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 20071
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES = 20072
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_FAILEDDATASETMESSAGES = 20073
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_FAILEDDATASETMESSAGES_ACTIVE = 20074
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_FAILEDDATASETMESSAGES_CLASSIFICATION = 20075
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_FAILEDDATASETMESSAGES_DIAGNOSTICSLEVEL = 20076
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_FAILEDDATASETMESSAGES_TIMEFIRSTCHANGE = 20077
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_DECRYPTIONERRORS = 20078
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_DECRYPTIONERRORS_ACTIVE = 20079
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_DECRYPTIONERRORS_CLASSIFICATION = 20080
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_DECRYPTIONERRORS_DIAGNOSTICSLEVEL = 20081
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_COUNTERS_DECRYPTIONERRORS_TIMEFIRSTCHANGE = 20082
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_MESSAGESEQUENCENUMBER = 20083
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_MESSAGESEQUENCENUMBER_DIAGNOSTICSLEVEL = 20084
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_STATUSCODE = 20085
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_STATUSCODE_DIAGNOSTICSLEVEL = 20086
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_MAJORVERSION = 20087
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_MAJORVERSION_DIAGNOSTICSLEVEL = 20088
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_MINORVERSION = 20089
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_MINORVERSION_DIAGNOSTICSLEVEL = 20090
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_SECURITYTOKENID = 20091
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_SECURITYTOKENID_DIAGNOSTICSLEVEL = 20092
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_TIMETONEXTTOKENID = 20093
    UA_NS0ID_PUBSUBDIAGNOSTICSDATASETREADERTYPE_LIVEVALUES_TIMETONEXTTOKENID_DIAGNOSTICSLEVEL = 20094
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_TRUSTLIST_UPDATEFREQUENCY = 20290
    UA_NS0ID_DATASETORDERINGTYPE = 20408
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_SECURITYTOKENID = 20409
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_TRUSTLIST_UPDATEFREQUENCY = 20588
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_TRUSTLIST_UPDATEFREQUENCY = 20884
    UA_NS0ID_VERSIONTIME = 20998
    UA_NS0ID_SESSIONLESSINVOKERESPONSETYPE = 20999
    UA_NS0ID_SESSIONLESSINVOKERESPONSETYPE_ENCODING_DEFAULTXML = 21000
    UA_NS0ID_SESSIONLESSINVOKERESPONSETYPE_ENCODING_DEFAULTBINARY = 21001
    UA_NS0ID_OPCUA_BINARYSCHEMA_FIELDTARGETDATATYPE = 21002
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_SECURITYTOKENID_DIAGNOSTICSLEVEL = 21003
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_TIMETONEXTTOKENID = 21004
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_DIAGNOSTICS_LIVEVALUES_TIMETONEXTTOKENID_DIAGNOSTICSLEVEL = 21005
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_SUBSCRIBEDDATASET = 21006
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_CREATETARGETVARIABLES = 21009
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_CREATETARGETVARIABLES_INPUTARGUMENTS = 21010
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_CREATETARGETVARIABLES_OUTPUTARGUMENTS = 21011
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_CREATEDATASETMIRROR = 21012
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_CREATEDATASETMIRROR_INPUTARGUMENTS = 21013
    UA_NS0ID_READERGROUPTYPE_DATASETREADERNAME_PLACEHOLDER_CREATEDATASETMIRROR_OUTPUTARGUMENTS = 21014
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS = 21015
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_DIAGNOSTICSLEVEL = 21016
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION = 21017
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION_ACTIVE = 21018
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION_CLASSIFICATION = 21019
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION_DIAGNOSTICSLEVEL = 21020
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALINFORMATION_TIMEFIRSTCHANGE = 21021
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALERROR = 21022
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALERROR_ACTIVE = 21023
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALERROR_CLASSIFICATION = 21024
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALERROR_DIAGNOSTICSLEVEL = 21025
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_TOTALERROR_TIMEFIRSTCHANGE = 21026
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_RESET = 21027
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_SUBERROR = 21028
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS = 21029
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR = 21030
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_ACTIVE = 21031
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_CLASSIFICATION = 21032
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_DIAGNOSTICSLEVEL = 21033
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEERROR_TIMEFIRSTCHANGE = 21034
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD = 21035
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_ACTIVE = 21036
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_CLASSIFICATION = 21037
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_DIAGNOSTICSLEVEL = 21038
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYMETHOD_TIMEFIRSTCHANGE = 21039
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT = 21040
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_ACTIVE = 21041
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_CLASSIFICATION = 21042
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_DIAGNOSTICSLEVEL = 21043
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALBYPARENT_TIMEFIRSTCHANGE = 21044
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR = 21045
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_ACTIVE = 21046
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_CLASSIFICATION = 21047
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_DIAGNOSTICSLEVEL = 21048
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEOPERATIONALFROMERROR_TIMEFIRSTCHANGE = 21049
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT = 21050
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_ACTIVE = 21051
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_CLASSIFICATION = 21052
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_DIAGNOSTICSLEVEL = 21053
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEPAUSEDBYPARENT_TIMEFIRSTCHANGE = 21054
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD = 21055
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_ACTIVE = 21056
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_CLASSIFICATION = 21057
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_DIAGNOSTICSLEVEL = 21058
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_STATEDISABLEDBYMETHOD_TIMEFIRSTCHANGE = 21059
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_LIVEVALUES = 21060
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES = 21061
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES_ACTIVE = 21062
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES_CLASSIFICATION = 21063
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES_DIAGNOSTICSLEVEL = 21064
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDNETWORKMESSAGES_TIMEFIRSTCHANGE = 21065
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES = 21066
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_ACTIVE = 21067
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_CLASSIFICATION = 21068
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_DIAGNOSTICSLEVEL = 21069
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_RECEIVEDINVALIDNETWORKMESSAGES_TIMEFIRSTCHANGE = 21070
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS = 21071
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_ACTIVE = 21072
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_CLASSIFICATION = 21073
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_DIAGNOSTICSLEVEL = 21074
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_COUNTERS_DECRYPTIONERRORS_TIMEFIRSTCHANGE = 21075
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETREADERS = 21076
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_CONFIGUREDDATASETREADERS_DIAGNOSTICSLEVEL = 21077
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETREADERS = 21078
    UA_NS0ID_READERGROUPTYPE_DIAGNOSTICS_LIVEVALUES_OPERATIONALDATASETREADERS_DIAGNOSTICSLEVEL = 21079
    UA_NS0ID_READERGROUPTYPE_TRANSPORTSETTINGS = 21080
    UA_NS0ID_READERGROUPTYPE_MESSAGESETTINGS = 21081
    UA_NS0ID_READERGROUPTYPE_ADDDATASETREADER = 21082
    UA_NS0ID_READERGROUPTYPE_ADDDATASETREADER_INPUTARGUMENTS = 21083
    UA_NS0ID_READERGROUPTYPE_ADDDATASETREADER_OUTPUTARGUMENTS = 21084
    UA_NS0ID_READERGROUPTYPE_REMOVEDATASETREADER = 21085
    UA_NS0ID_READERGROUPTYPE_REMOVEDATASETREADER_INPUTARGUMENTS = 21086
    UA_NS0ID_PUBSUBGROUPTYPEADDREADERMETHODTYPE = 21087
    UA_NS0ID_PUBSUBGROUPTYPEADDREADERMETHODTYPE_INPUTARGUMENTS = 21088
    UA_NS0ID_PUBSUBGROUPTYPEADDREADERMETHODTYPE_OUTPUTARGUMENTS = 21089
    UA_NS0ID_READERGROUPTRANSPORTTYPE = 21090
    UA_NS0ID_READERGROUPMESSAGETYPE = 21091
    UA_NS0ID_DATASETWRITERTYPE_DATASETWRITERID = 21092
    UA_NS0ID_DATASETWRITERTYPE_DATASETFIELDCONTENTMASK = 21093
    UA_NS0ID_DATASETWRITERTYPE_KEYFRAMECOUNT = 21094
    UA_NS0ID_DATASETWRITERTYPE_MESSAGESETTINGS = 21095
    UA_NS0ID_DATASETWRITERMESSAGETYPE = 21096
    UA_NS0ID_DATASETREADERTYPE_PUBLISHERID = 21097
    UA_NS0ID_DATASETREADERTYPE_WRITERGROUPID = 21098
    UA_NS0ID_DATASETREADERTYPE_DATASETWRITERID = 21099
    UA_NS0ID_DATASETREADERTYPE_DATASETMETADATA = 21100
    UA_NS0ID_DATASETREADERTYPE_DATASETFIELDCONTENTMASK = 21101
    UA_NS0ID_DATASETREADERTYPE_MESSAGERECEIVETIMEOUT = 21102
    UA_NS0ID_DATASETREADERTYPE_MESSAGESETTINGS = 21103
    UA_NS0ID_DATASETREADERMESSAGETYPE = 21104
    UA_NS0ID_UADPWRITERGROUPMESSAGETYPE = 21105
    UA_NS0ID_UADPWRITERGROUPMESSAGETYPE_GROUPVERSION = 21106
    UA_NS0ID_UADPWRITERGROUPMESSAGETYPE_DATASETORDERING = 21107
    UA_NS0ID_UADPWRITERGROUPMESSAGETYPE_NETWORKMESSAGECONTENTMASK = 21108
    UA_NS0ID_UADPWRITERGROUPMESSAGETYPE_SAMPLINGOFFSET = 21109
    UA_NS0ID_UADPWRITERGROUPMESSAGETYPE_PUBLISHINGOFFSET = 21110
    UA_NS0ID_UADPDATASETWRITERMESSAGETYPE = 21111
    UA_NS0ID_UADPDATASETWRITERMESSAGETYPE_DATASETMESSAGECONTENTMASK = 21112
    UA_NS0ID_UADPDATASETWRITERMESSAGETYPE_CONFIGUREDSIZE = 21113
    UA_NS0ID_UADPDATASETWRITERMESSAGETYPE_NETWORKMESSAGENUMBER = 21114
    UA_NS0ID_UADPDATASETWRITERMESSAGETYPE_DATASETOFFSET = 21115
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE = 21116
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE_GROUPVERSION = 21117
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE_NETWORKMESSAGENUMBER = 21119
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE_DATASETCLASSID = 21120
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE_NETWORKMESSAGECONTENTMASK = 21121
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE_DATASETMESSAGECONTENTMASK = 21122
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE_PUBLISHINGINTERVAL = 21123
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE_PROCESSINGOFFSET = 21124
    UA_NS0ID_UADPDATASETREADERMESSAGETYPE_RECEIVEOFFSET = 21125
    UA_NS0ID_JSONWRITERGROUPMESSAGETYPE = 21126
    UA_NS0ID_JSONWRITERGROUPMESSAGETYPE_NETWORKMESSAGECONTENTMASK = 21127
    UA_NS0ID_JSONDATASETWRITERMESSAGETYPE = 21128
    UA_NS0ID_JSONDATASETWRITERMESSAGETYPE_DATASETMESSAGECONTENTMASK = 21129
    UA_NS0ID_JSONDATASETREADERMESSAGETYPE = 21130
    UA_NS0ID_JSONDATASETREADERMESSAGETYPE_NETWORKMESSAGECONTENTMASK = 21131
    UA_NS0ID_JSONDATASETREADERMESSAGETYPE_DATASETMESSAGECONTENTMASK = 21132
    UA_NS0ID_DATAGRAMWRITERGROUPTRANSPORTTYPE = 21133
    UA_NS0ID_DATAGRAMWRITERGROUPTRANSPORTTYPE_MESSAGEREPEATCOUNT = 21134
    UA_NS0ID_DATAGRAMWRITERGROUPTRANSPORTTYPE_MESSAGEREPEATDELAY = 21135
    UA_NS0ID_BROKERWRITERGROUPTRANSPORTTYPE = 21136
    UA_NS0ID_BROKERWRITERGROUPTRANSPORTTYPE_QUEUENAME = 21137
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTTYPE = 21138
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTTYPE_QUEUENAME = 21139
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTTYPE_METADATAQUEUENAME = 21140
    UA_NS0ID_BROKERDATASETWRITERTRANSPORTTYPE_METADATAUPDATETIME = 21141
    UA_NS0ID_BROKERDATASETREADERTRANSPORTTYPE = 21142
    UA_NS0ID_BROKERDATASETREADERTRANSPORTTYPE_QUEUENAME = 21143
    UA_NS0ID_BROKERDATASETREADERTRANSPORTTYPE_METADATAQUEUENAME = 21144
    UA_NS0ID_NETWORKADDRESSTYPE = 21145
    UA_NS0ID_NETWORKADDRESSTYPE_NETWORKINTERFACE = 21146
    UA_NS0ID_NETWORKADDRESSURLTYPE = 21147
    UA_NS0ID_NETWORKADDRESSURLTYPE_NETWORKINTERFACE = 21148
    UA_NS0ID_NETWORKADDRESSURLTYPE_URL = 21149
    UA_NS0ID_WRITERGROUPDATATYPE_ENCODING_DEFAULTBINARY = 21150
    UA_NS0ID_NETWORKADDRESSDATATYPE_ENCODING_DEFAULTBINARY = 21151
    UA_NS0ID_NETWORKADDRESSURLDATATYPE_ENCODING_DEFAULTBINARY = 21152
    UA_NS0ID_READERGROUPDATATYPE_ENCODING_DEFAULTBINARY = 21153
    UA_NS0ID_PUBSUBCONFIGURATIONDATATYPE_ENCODING_DEFAULTBINARY = 21154
    UA_NS0ID_DATAGRAMWRITERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTBINARY = 21155
    UA_NS0ID_OPCUA_BINARYSCHEMA_WRITERGROUPDATATYPE = 21156
    UA_NS0ID_OPCUA_BINARYSCHEMA_WRITERGROUPDATATYPE_DATATYPEVERSION = 21157
    UA_NS0ID_OPCUA_BINARYSCHEMA_WRITERGROUPDATATYPE_DICTIONARYFRAGMENT = 21158
    UA_NS0ID_OPCUA_BINARYSCHEMA_NETWORKADDRESSDATATYPE = 21159
    UA_NS0ID_OPCUA_BINARYSCHEMA_NETWORKADDRESSDATATYPE_DATATYPEVERSION = 21160
    UA_NS0ID_OPCUA_BINARYSCHEMA_NETWORKADDRESSDATATYPE_DICTIONARYFRAGMENT = 21161
    UA_NS0ID_OPCUA_BINARYSCHEMA_NETWORKADDRESSURLDATATYPE = 21162
    UA_NS0ID_OPCUA_BINARYSCHEMA_NETWORKADDRESSURLDATATYPE_DATATYPEVERSION = 21163
    UA_NS0ID_OPCUA_BINARYSCHEMA_NETWORKADDRESSURLDATATYPE_DICTIONARYFRAGMENT = 21164
    UA_NS0ID_OPCUA_BINARYSCHEMA_READERGROUPDATATYPE = 21165
    UA_NS0ID_OPCUA_BINARYSCHEMA_READERGROUPDATATYPE_DATATYPEVERSION = 21166
    UA_NS0ID_OPCUA_BINARYSCHEMA_READERGROUPDATATYPE_DICTIONARYFRAGMENT = 21167
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBSUBCONFIGURATIONDATATYPE = 21168
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBSUBCONFIGURATIONDATATYPE_DATATYPEVERSION = 21169
    UA_NS0ID_OPCUA_BINARYSCHEMA_PUBSUBCONFIGURATIONDATATYPE_DICTIONARYFRAGMENT = 21170
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATAGRAMWRITERGROUPTRANSPORTDATATYPE = 21171
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATAGRAMWRITERGROUPTRANSPORTDATATYPE_DATATYPEVERSION = 21172
    UA_NS0ID_OPCUA_BINARYSCHEMA_DATAGRAMWRITERGROUPTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 21173
    UA_NS0ID_WRITERGROUPDATATYPE_ENCODING_DEFAULTXML = 21174
    UA_NS0ID_NETWORKADDRESSDATATYPE_ENCODING_DEFAULTXML = 21175
    UA_NS0ID_NETWORKADDRESSURLDATATYPE_ENCODING_DEFAULTXML = 21176
    UA_NS0ID_READERGROUPDATATYPE_ENCODING_DEFAULTXML = 21177
    UA_NS0ID_PUBSUBCONFIGURATIONDATATYPE_ENCODING_DEFAULTXML = 21178
    UA_NS0ID_DATAGRAMWRITERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTXML = 21179
    UA_NS0ID_OPCUA_XMLSCHEMA_WRITERGROUPDATATYPE = 21180
    UA_NS0ID_OPCUA_XMLSCHEMA_WRITERGROUPDATATYPE_DATATYPEVERSION = 21181
    UA_NS0ID_OPCUA_XMLSCHEMA_WRITERGROUPDATATYPE_DICTIONARYFRAGMENT = 21182
    UA_NS0ID_OPCUA_XMLSCHEMA_NETWORKADDRESSDATATYPE = 21183
    UA_NS0ID_OPCUA_XMLSCHEMA_NETWORKADDRESSDATATYPE_DATATYPEVERSION = 21184
    UA_NS0ID_OPCUA_XMLSCHEMA_NETWORKADDRESSDATATYPE_DICTIONARYFRAGMENT = 21185
    UA_NS0ID_OPCUA_XMLSCHEMA_NETWORKADDRESSURLDATATYPE = 21186
    UA_NS0ID_OPCUA_XMLSCHEMA_NETWORKADDRESSURLDATATYPE_DATATYPEVERSION = 21187
    UA_NS0ID_OPCUA_XMLSCHEMA_NETWORKADDRESSURLDATATYPE_DICTIONARYFRAGMENT = 21188
    UA_NS0ID_OPCUA_XMLSCHEMA_READERGROUPDATATYPE = 21189
    UA_NS0ID_OPCUA_XMLSCHEMA_READERGROUPDATATYPE_DATATYPEVERSION = 21190
    UA_NS0ID_OPCUA_XMLSCHEMA_READERGROUPDATATYPE_DICTIONARYFRAGMENT = 21191
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBSUBCONFIGURATIONDATATYPE = 21192
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBSUBCONFIGURATIONDATATYPE_DATATYPEVERSION = 21193
    UA_NS0ID_OPCUA_XMLSCHEMA_PUBSUBCONFIGURATIONDATATYPE_DICTIONARYFRAGMENT = 21194
    UA_NS0ID_OPCUA_XMLSCHEMA_DATAGRAMWRITERGROUPTRANSPORTDATATYPE = 21195
    UA_NS0ID_OPCUA_XMLSCHEMA_DATAGRAMWRITERGROUPTRANSPORTDATATYPE_DATATYPEVERSION = 21196
    UA_NS0ID_OPCUA_XMLSCHEMA_DATAGRAMWRITERGROUPTRANSPORTDATATYPE_DICTIONARYFRAGMENT = 21197
    UA_NS0ID_WRITERGROUPDATATYPE_ENCODING_DEFAULTJSON = 21198
    UA_NS0ID_NETWORKADDRESSDATATYPE_ENCODING_DEFAULTJSON = 21199
    UA_NS0ID_NETWORKADDRESSURLDATATYPE_ENCODING_DEFAULTJSON = 21200
    UA_NS0ID_READERGROUPDATATYPE_ENCODING_DEFAULTJSON = 21201
    UA_NS0ID_PUBSUBCONFIGURATIONDATATYPE_ENCODING_DEFAULTJSON = 21202
    UA_NS0ID_DATAGRAMWRITERGROUPTRANSPORTDATATYPE_ENCODING_DEFAULTJSON = 21203
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_TRUSTLIST_UPDATEFREQUENCY = 21383
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_UPDATEFREQUENCY = 21679
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_UPDATEFREQUENCY = 21975
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_UPDATEFREQUENCY = 22271
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_TRUSTLIST_UPDATEFREQUENCY = 22567
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_TRUSTLIST_UPDATEFREQUENCY = 22863
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_TRUSTLIST_UPDATEFREQUENCY = 23159
    UA_NS0ID_ALIASNAMETYPE = 23455
    UA_NS0ID_ALIASNAMECATEGORYTYPE = 23456
    UA_NS0ID_ALIASNAMECATEGORYTYPE_ALIAS_PLACEHOLDER = 23457
    UA_NS0ID_ALIASNAMECATEGORYTYPE_SUBALIASNAMECATEGORIES_PLACEHOLDER = 23458
    UA_NS0ID_ALIASNAMECATEGORYTYPE_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS = 23459
    UA_NS0ID_ALIASNAMECATEGORYTYPE_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS_INPUTARGUMENTS = 23460
    UA_NS0ID_ALIASNAMECATEGORYTYPE_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS_OUTPUTARGUMENTS = 23461
    UA_NS0ID_ALIASNAMECATEGORYTYPE_FINDALIAS = 23462
    UA_NS0ID_ALIASNAMECATEGORYTYPE_FINDALIAS_INPUTARGUMENTS = 23463
    UA_NS0ID_ALIASNAMECATEGORYTYPE_FINDALIAS_OUTPUTARGUMENTS = 23464
    UA_NS0ID_FINDALIASMETHODTYPE = 23465
    UA_NS0ID_FINDALIASMETHODTYPE_INPUTARGUMENTS = 23466
    UA_NS0ID_FINDALIASMETHODTYPE_OUTPUTARGUMENTS = 23467
    UA_NS0ID_ALIASNAMEDATATYPE = 23468
    UA_NS0ID_ALIASFOR = 23469
    UA_NS0ID_ALIASES = 23470
    UA_NS0ID_ALIASES_ALIAS_PLACEHOLDER = 23471
    UA_NS0ID_ALIASES_SUBALIASNAMECATEGORIES_PLACEHOLDER = 23472
    UA_NS0ID_ALIASES_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS = 23473
    UA_NS0ID_ALIASES_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS_INPUTARGUMENTS = 23474
    UA_NS0ID_ALIASES_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS_OUTPUTARGUMENTS = 23475
    UA_NS0ID_ALIASES_FINDALIAS = 23476
    UA_NS0ID_ALIASES_FINDALIAS_INPUTARGUMENTS = 23477
    UA_NS0ID_ALIASES_FINDALIAS_OUTPUTARGUMENTS = 23478
    UA_NS0ID_TAGVARIABLES = 23479
    UA_NS0ID_TAGVARIABLES_ALIAS_PLACEHOLDER = 23480
    UA_NS0ID_TAGVARIABLES_SUBALIASNAMECATEGORIES_PLACEHOLDER = 23481
    UA_NS0ID_TAGVARIABLES_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS = 23482
    UA_NS0ID_TAGVARIABLES_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS_INPUTARGUMENTS = 23483
    UA_NS0ID_TAGVARIABLES_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS_OUTPUTARGUMENTS = 23484
    UA_NS0ID_TAGVARIABLES_FINDALIAS = 23485
    UA_NS0ID_TAGVARIABLES_FINDALIAS_INPUTARGUMENTS = 23486
    UA_NS0ID_TAGVARIABLES_FINDALIAS_OUTPUTARGUMENTS = 23487
    UA_NS0ID_TOPICS = 23488
    UA_NS0ID_TOPICS_ALIAS_PLACEHOLDER = 23489
    UA_NS0ID_TOPICS_SUBALIASNAMECATEGORIES_PLACEHOLDER = 23490
    UA_NS0ID_TOPICS_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS = 23491
    UA_NS0ID_TOPICS_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS_INPUTARGUMENTS = 23492
    UA_NS0ID_TOPICS_SUBALIASNAMECATEGORIES_PLACEHOLDER_FINDALIAS_OUTPUTARGUMENTS = 23493
    UA_NS0ID_TOPICS_FINDALIAS = 23494
    UA_NS0ID_TOPICS_FINDALIAS_INPUTARGUMENTS = 23495
    UA_NS0ID_TOPICS_FINDALIAS_OUTPUTARGUMENTS = 23496
    UA_NS0ID_READANNOTATIONDATADETAILS = 23497
    UA_NS0ID_CURRENCYUNITTYPE = 23498
    UA_NS0ID_ALIASNAMEDATATYPE_ENCODING_DEFAULTBINARY = 23499
    UA_NS0ID_READANNOTATIONDATADETAILS_ENCODING_DEFAULTBINARY = 23500
    UA_NS0ID_CURRENCYUNIT = 23501
    UA_NS0ID_OPCUA_BINARYSCHEMA_ALIASNAMEDATATYPE = 23502
    UA_NS0ID_OPCUA_BINARYSCHEMA_ALIASNAMEDATATYPE_DATATYPEVERSION = 23503
    UA_NS0ID_OPCUA_BINARYSCHEMA_ALIASNAMEDATATYPE_DICTIONARYFRAGMENT = 23504
    UA_NS0ID_ALIASNAMEDATATYPE_ENCODING_DEFAULTXML = 23505
    UA_NS0ID_READANNOTATIONDATADETAILS_ENCODING_DEFAULTXML = 23506
    UA_NS0ID_CURRENCYUNITTYPE_ENCODING_DEFAULTBINARY = 23507
    UA_NS0ID_OPCUA_XMLSCHEMA_ALIASNAMEDATATYPE = 23508
    UA_NS0ID_OPCUA_XMLSCHEMA_ALIASNAMEDATATYPE_DATATYPEVERSION = 23509
    UA_NS0ID_OPCUA_XMLSCHEMA_ALIASNAMEDATATYPE_DICTIONARYFRAGMENT = 23510
    UA_NS0ID_ALIASNAMEDATATYPE_ENCODING_DEFAULTJSON = 23511
    UA_NS0ID_READANNOTATIONDATADETAILS_ENCODING_DEFAULTJSON = 23512
    UA_NS0ID_IORDEREDOBJECTTYPE = 23513
    UA_NS0ID_OPCUA_BINARYSCHEMA_CURRENCYUNITTYPE = 23514
    UA_NS0ID_OPCUA_BINARYSCHEMA_CURRENCYUNITTYPE_DATATYPEVERSION = 23515
    UA_NS0ID_OPCUA_BINARYSCHEMA_CURRENCYUNITTYPE_DICTIONARYFRAGMENT = 23516
    UA_NS0ID_IORDEREDOBJECTTYPE_NUMBERINLIST = 23517
    UA_NS0ID_ORDEREDLISTTYPE = 23518
    UA_NS0ID_ORDEREDLISTTYPE_ORDEREDOBJECT_PLACEHOLDER = 23519
    UA_NS0ID_CURRENCYUNITTYPE_ENCODING_DEFAULTXML = 23520
    UA_NS0ID_ORDEREDLISTTYPE_ORDEREDOBJECT_PLACEHOLDER_NUMBERINLIST = 23521
    UA_NS0ID_OPCUA_XMLSCHEMA_CURRENCYUNITTYPE = 23522
    UA_NS0ID_OPCUA_XMLSCHEMA_CURRENCYUNITTYPE_DATATYPEVERSION = 23523
    UA_NS0ID_OPCUA_XMLSCHEMA_CURRENCYUNITTYPE_DICTIONARYFRAGMENT = 23524
    UA_NS0ID_ORDEREDLISTTYPE_NODEVERSION = 23525
    UA_NS0ID_CERTIFICATEGROUPTYPE_GETREJECTEDLIST = 23526
    UA_NS0ID_CERTIFICATEGROUPTYPE_GETREJECTEDLIST_OUTPUTARGUMENTS = 23527
    UA_NS0ID_CURRENCYUNITTYPE_ENCODING_DEFAULTJSON = 23528
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_GETREJECTEDLIST = 23529
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTAPPLICATIONGROUP_GETREJECTEDLIST_OUTPUTARGUMENTS = 23530
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_GETREJECTEDLIST = 23531
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTHTTPSGROUP_GETREJECTEDLIST_OUTPUTARGUMENTS = 23532
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_GETREJECTEDLIST = 23533
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_DEFAULTUSERTOKENGROUP_GETREJECTEDLIST_OUTPUTARGUMENTS = 23534
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_GETREJECTEDLIST = 23535
    UA_NS0ID_CERTIFICATEGROUPFOLDERTYPE_ADDITIONALGROUP_PLACEHOLDER_GETREJECTEDLIST_OUTPUTARGUMENTS = 23536
    UA_NS0ID_ECCAPPLICATIONCERTIFICATETYPE = 23537
    UA_NS0ID_ECCNISTP256APPLICATIONCERTIFICATETYPE = 23538
    UA_NS0ID_ECCNISTP384APPLICATIONCERTIFICATETYPE = 23539
    UA_NS0ID_ECCBRAINPOOLP256R1APPLICATIONCERTIFICATETYPE = 23540
    UA_NS0ID_ECCBRAINPOOLP384R1APPLICATIONCERTIFICATETYPE = 23541
    UA_NS0ID_ECCCURVE25519APPLICATIONCERTIFICATETYPE = 23542
    UA_NS0ID_ECCCURVE448APPLICATIONCERTIFICATETYPE = 23543
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_GETREJECTEDLIST = 23544
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_GETREJECTEDLIST_OUTPUTARGUMENTS = 23545
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_GETREJECTEDLIST = 23546
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_GETREJECTEDLIST_OUTPUTARGUMENTS = 23547
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_GETREJECTEDLIST = 23548
    UA_NS0ID_SERVERCONFIGURATIONTYPE_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_GETREJECTEDLIST_OUTPUTARGUMENTS = 23549
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_GETREJECTEDLIST = 23550
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTAPPLICATIONGROUP_GETREJECTEDLIST_OUTPUTARGUMENTS = 23551
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_GETREJECTEDLIST = 23552
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTHTTPSGROUP_GETREJECTEDLIST_OUTPUTARGUMENTS = 23553
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_GETREJECTEDLIST = 23554
    UA_NS0ID_SERVERCONFIGURATION_CERTIFICATEGROUPS_DEFAULTUSERTOKENGROUP_GETREJECTEDLIST_OUTPUTARGUMENTS = 23555
    UA_NS0ID_AUTHORIZATIONSERVICESCONFIGURATIONFOLDERTYPE = 23556
    UA_NS0ID_AUTHORIZATIONSERVICESCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER = 23557
    UA_NS0ID_AUTHORIZATIONSERVICESCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_SERVICEURI = 23558
    UA_NS0ID_AUTHORIZATIONSERVICESCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_SERVICECERTIFICATE = 23559
    UA_NS0ID_AUTHORIZATIONSERVICESCONFIGURATIONFOLDERTYPE_SERVICENAME_PLACEHOLDER_ISSUERENDPOINTURL = 23560

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

            val = ffi.new("UA_NodeId*", val)

        super().__init__(val=val, is_pointer=is_pointer)
        self._namespace_index = UaUInt16(val=val.namespaceIndex, is_pointer=False)
        self._identifier_type = UaNodeIdType(val=val.identifierType, is_pointer=False)

        # TODO: refactor
        if self._identifier_type._val == 0:
            self._identifier = UaUInt32(val=val.identifier.numeric)
        elif self._identifier_type._val == 1:
            self._identifier = UaUInt32(val=val.identifier.numeric)
        elif self._identifier_type._val == 2:
            self._identifier = UaUInt32(val=val.identifier.numeric)
        elif self._identifier_type._val == 3:
            self._identifier = UaString(val=val.identifier.string)
        elif self._identifier_type._val == 4:
            self._identifier = UaGuid(val=val.identifier.guid)
        elif self._identifier_type._val == 5:
            self._identifier = UaByteString(val=val.identifier.byteString)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NodeId")
        else:
            self._value[0] = _val(val)
        self._namespace_index._value[0] = _val(val.namespaceIndex)
        self._identifier_type._value[0] = _val(val.identifierType)
        cases = {
            0: val.identifier.numeric,
            1: val.identifier.numeric,
            2: val.identifier.numeric,
            3: val.identifier.string,
            4: val.identifier.guid,
            5: val.identifier.byteString
        }
        self._identifier._value[0] = cases[self._identifier_type._value]

    @property
    def namespace_index(self):
        return self._namespace_index

    # @namespace_index.setter
    # def namespace_index(self, val):
    #     self._namespace_index = val
    #     self._value.namespaceIndex = val._val

    @property
    def identifier_type(self):
        return self._identifier_type

    # @identifier_type.setter
    # def identifier_type(self, val):
    #     self._identifier_type = val
    #     self._value.identifierType = val._val

    @property
    def identifier(self):
        return self._identifier

    # @identifier.setter
    # def identifier(self, val):
    #     self._identifier = val
    #     self._value.identifier = val._val

    def __str__(self, n=0):
        return ("(UaNodeId) :\n" +
                "\t" * (n + 1) + "namespace_index" + self._namespace_index.__str__(n + 1) +
                "\t" * (n + 1) + "identifier_type" + self._identifier_type.__str__(n + 1) +
                "\t" * (n + 1) + "identifier" + self._identifier.__str__(n + 1) + "\n")

    def __eq__(self, other):
        return lib.UA_NodeId_equal(self._ptr, other._ptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_null(self):
        return lib.UA_NodeId_isNull(self._ptr)


# +++++++++++++++++++ UaExpandedNodeId +++++++++++++++++++++++
class UaExpandedNodeId(UaType):
    NULL = lib.UA_EXPANDEDNODEID_NULL

    # TODO: refactor
    # TODO: Memory management
    def __init__(self, ns_index=None, ident=None, is_pointer=False, val=ffi.new("UA_ExpandedNodeId*")):
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

            val = ffi.new("UA_ExpandedNodeId*", val)

        super().__init__(val=val, is_pointer=is_pointer)

        self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
        self._namespace_uri = UaString(val=val.namespaceUri, is_pointer=False)
        self._server_index = UaUInt32(val=val.serverIndex, is_pointer=False)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._node_id._value[0] = _val(val.nodeId)
        self._namespace_uri._value[0] = _val(val.namespaceUri)
        self._server_index._value[0] = _val(val.serverIndex)

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
        self._value.nodeId = val._val

    @namespace_uri.setter
    def namespace_uri(self, val):
        self._namespace_uri = val
        self._value.namespaceUri = val._val

    @server_index.setter
    def server_index(self, val):
        self._server_index = val
        self._value.serverIndex = val._val

    def __str__(self, n=0):
        return ("(UaExpandedNodeId) :\n" +
                "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1) +
                "\t" * (n + 1) + "namespace_uri" + self._namespace_uri.__str__(n + 1) +
                "\t" * (n + 1) + "server_index" + self._server_index.__str__(n + 1) + "\n")

    def is_local(self):
        return lib.UA_ExpandedNodeId_isLocal(self._ptr)

    def __eq__(self, other):
        return lib.UA_ExpandedNodeId_equal(self._ptr, other._ptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return lib.UA_ExpandedNodeId_order(self._ptr, other._ptr) == 1

    def __lt__(self, other):
        return lib.UA_ExpandedNodeId_order(self._ptr, other._ptr) == -1

    def __ge__(self, other):
        return lib.UA_ExpandedNodeId_order(self._ptr, other._ptr) in [1, 0]

    def __le__(self, other):
        return lib.UA_ExpandedNodeId_order(self._ptr, other._ptr) in [-1, 0]

    def __hash__(self):
        return lib.UA_ExpandedNodeId_hash(self._ptr)


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

            val = ffi.new("UA_QualifiedName*", val)

        super().__init__(val=val, is_pointer=is_pointer)

        self._namespace_index = UaUInt16(val=val.namespaceIndex, is_pointer=False)
        self._name = UaString(val=val.name, is_pointer=False)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._namespace_index._value[0] = _val(val.namespaceIndex)
        self._name._value[0] = _val(val.name)

    @property
    def namespace_index(self):
        return self._namespace_index

    @property
    def name(self):
        return self._name

    @namespace_index.setter
    def namespace_index(self, val):
        self._namespace_index = val
        self._value.namespaceIndex = val._val

    @name.setter
    def name(self, val):
        self._name = val
        self._value.name = val._val

    def __str__(self, n=0):
        return ("(UaQualifiedName) :\n" +
                "\t" * (n + 1) + "namespace_index" + self._namespace_index.__str__(n + 1) +
                "\t" * (n + 1) + "name" + self._name.__str__(n + 1) + "\n")

    def is_null(self):
        return lib.UA_QualifiedName_isNull(self._ptr)

    def __hash__(self):
        return lib.UA_QualifiedName_hash(self._ptr)

    def __eq__(self, other):
        return lib.UA_QualifiedName_equal(self._ptr, other.__value)


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

            val = ffi.new("UA_LocalizedText*", val)

        super().__init__(val=val, is_pointer=is_pointer)

        self._locale = UaString(val=val.locale, is_pointer=False)
        self._text = UaString(val=val.text, is_pointer=False)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._locale._value[0] = _val(val.locale)
        self._text._value[0] = _val(val.text)

    @property
    def locale(self):
        return self._locale

    @property
    def text(self):
        return self._text

    @locale.setter
    def locale(self, val):
        self._locale = val
        self._value.locale = val._val

    @text.setter
    def text(self, val):
        self._text = val
        self._value.text = val._val

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

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._min._value[0] = _val(val.min)
        self._max._value[0] = _val(val.max)

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @min.setter
    def min(self, val):
        self._min = val
        self._value.min = val._val

    @max.setter
    def max(self, val):
        self._max = val
        self._value.max = val._val

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

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._dimensions_size._value[0] = _val(val.dimensionsSize)
        self._dimensions._value = val.dimensions

    @property
    def dimensions_size(self):
        return self._dimensions_size

    @property
    def dimensions(self):
        return self._dimensions

    # @dimensions_size.setter
    # def dimensions_size(self, val):
    #     self._dimensions_size = val
    #     self._value.dimensionsSize = val._val
    #
    # @dimensions.setter
    # def dimensions(self, val):
    #     self._dimensions = val
    #     self._value.dimensions = val._ptr

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

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._type._value = val.type
        self._storage_type._value[0] = _val(val.storageType)
        self._array_length._value[0] = _val(val.arrayLength)
        self._data._value = val.data
        self._array_dimensions_size._value[0] = _val(val.arrayDimensionsSize)
        self._array_dimensions._value = val.arrayDimensions

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

    # @type.setter
    # def type(self, val):
    #     self._type = val
    #     self._value.type = val._ptr
    #
    # @storage_type.setter
    # def storage_type(self, val):
    #     self._storage_type = val
    #     self._value.storageType = val._val
    #
    # @array_length.setter
    # def array_length(self, val):
    #     self._array_length = val
    #     self._value.arrayLength = val._val
    #
    # @data.setter
    # def data(self, val):
    #     self._data = val
    #     self._value.data = val._ptr
    #
    # @array_dimensions_size.setter
    # def array_dimensions_size(self, val):
    #     self._array_dimensions_size = val
    #     self._value.arrayDimensionsSize = val._val
    #
    # @array_dimensions.setter
    # def array_dimensions(self, val):
    #     self._array_dimensions = val
    #     self._value.arrayDimensions = val._ptr

    def __str__(self, n=0):
        return ("(UaVariant) :\n" +
                "\t" * (n + 1) + "type" + self._type.__str__(n + 1) +
                "\t" * (n + 1) + "storage_type" + self._storage_type.__str__(n + 1) +
                "\t" * (n + 1) + "array_length" + self._array_length.__str__(n + 1) +
                "\t" * (n + 1) + "data" + self._data.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions_size" + self._array_dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions" + self._array_dimensions.__str__(n + 1) + "\n")

    def is_empty(self):
        lib.UA_Variant_isEmpty(self._ptr)

    def is_scalar(self):
        lib.UA_Variant_isScalar(self._ptr)

    def has_scalar_type(self, data_type):
        lib.UA_Variant_hasScalarType(self._ptr, data_type._ptr)

    def has_array_type(self, data_type):
        lib.UA_Variant_hasArrayType(self._ptr, data_type._ptr)

    # TODO: memory management
    def _set_attributes(self):
        self._type._value = self._value.type
        self._storage_type._value = self._value.storageType
        self._array_length._value = self._value.arrayLength
        self._data._value = self._ptr.data
        self._array_dimensions_size._value = self._value.arrayDimensionsSize
        self._array_dimensions._value = self._value.arrayDimensions

    def set_scalar(self, data, data_type):
        # TODO: might cause memory problems!
        lib.UA_Variant_setScalarCopy(self._ptr, ffi.new_handle(data), data_type._ptr)
        self._set_attributes()

    def set_array(self, array, size, data_type):
        if size is int:
            size = SizeT(size)
        if size is not SizeT:
            raise AttributeError(f"size={size} has to be int or SizeT")
        # TODO: might cause memory problems!
        status_code = lib.UA_Variant_setArrayCopy(self._ptr, ffi.new_handle(array), size._val, data_type._ptr)
        status_code = UaStatusCode(status_code)
        if not status_code.is_bad():
            self._set_attributes()
        else:
            raise Exception(f"An Error occured - {str(status_code)}")

    def copy_range_to(self, variant, num_range: UaNumericRange):
        # TODO: might cause memory problems!
        status_code = lib.UA_Variant_copyRange(self._ptr, variant._ptr, num_range._val)
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
        # TODO: might cause memory problems
        status_code = lib.UA_Variant_setRangeCopy(self._ptr, ffi.new_handle(array), size, num_range._val)
        status_code = UaStatusCode(status_code)
        if not status_code.is_bad():
            self._set_attributes()
        else:
            raise AttributeError(f"An Error occured - {str(status_code)}")


# +++++++++++++++++++ UaDataValue +++++++++++++++++++++++
class UaDataValue(UaType):
    def __init__(self, val=ffi.new("UA_DataValue*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._variant = UaVariant(val=val.value, is_pointer=False)
        self._source_timestamp = UaDateTime(val=val.sourceTimestamp, is_pointer=False)
        self._server_timestamp = UaDateTime(val=val.serverTimestamp, is_pointer=False)
        self._source_picoseconds = UaUInt16(val=val.sourcePicoseconds, is_pointer=False)
        self._server_picoseconds = UaUInt16(val=val.serverPicoseconds, is_pointer=False)
        self._status = UaStatusCode(val=val.status, is_pointer=False)
        self._has_variant = UaBoolean(val=val.hasValue, is_pointer=False)
        self._has_status = UaBoolean(val=val.hasStatus, is_pointer=False)
        self._has_source_timestamp = UaBoolean(val=val.hasSourceTimestamp, is_pointer=False)
        self._has_server_timestamp = UaBoolean(val=val.hasServerTimestamp, is_pointer=False)
        self._has_source_picoseconds = UaBoolean(val=val.hasSourcePicoseconds, is_pointer=False)
        self._has_server_picoseconds = UaBoolean(val=val.hasServerPicoseconds, is_pointer=False)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._variant._value[0] = _val(val.value)
        self._source_timestamp._value[0] = _val(val.sourceTimestamp)
        self._server_timestamp._value[0] = _val(val.serverTimestamp)
        self._source_picoseconds._value[0] = _val(val.sourcePicoseconds)
        self._server_picoseconds._value[0] = _val(val.serverPicoseconds)
        self._status._value[0] = _val(val.status)
        self._has_variant._value[0] = _val(val.hasValue)
        self._has_status._value[0] = _val(val.hasStatus)
        self._has_source_timestamp._value[0] = _val(val.hasSourceTimestamp)
        self._has_server_timestamp._value[0] = _val(val.hasServerTimestamp)
        self._has_source_picoseconds._value[0] = _val(val.hasSourcePicoseconds)
        self._has_server_picoseconds._value[0] = _val(val.hasServerPicoseconds)

    @property
    def variant(self):
        return self._variant

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
    def has_variant(self):
        return self._has_variant

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

    # @variant.setter
    # def variant(self, val):
    #     self._variant = val
    #     self._value.value = val._val
    #
    # @source_timestamp.setter
    # def source_timestamp(self, val):
    #     self._source_timestamp = val
    #     self._value.sourceTimestamp = val._val
    #
    # @server_timestamp.setter
    # def server_timestamp(self, val):
    #     self._server_timestamp = val
    #     self._value.serverTimestamp = val._val
    #
    # @source_picoseconds.setter
    # def source_picoseconds(self, val):
    #     self._source_picoseconds = val
    #     self._value.sourcePicoseconds = val._val
    #
    # @server_picoseconds.setter
    # def server_picoseconds(self, val):
    #     self._server_picoseconds = val
    #     self._value.serverPicoseconds = val._val
    #
    # @status.setter
    # def status(self, val):
    #     self._status = val
    #     self._value.status = val._val
    #
    # @has_variant.setter
    # def has_variant(self, val):
    #     self._has_variant = val
    #     self._value.hasValue = val._val
    #
    # @has_status.setter
    # def has_status(self, val):
    #     self._has_status = val
    #     self._value.hasStatus = val._val
    #
    # @has_source_timestamp.setter
    # def has_source_timestamp(self, val):
    #     self._has_source_timestamp = val
    #     self._value.hasSourceTimestamp = val._val
    #
    # @has_server_timestamp.setter
    # def has_server_timestamp(self, val):
    #     self._has_server_timestamp = val
    #     self._value.hasServerTimestamp = val._val
    #
    # @has_source_picoseconds.setter
    # def has_source_picoseconds(self, val):
    #     self._has_source_picoseconds = val
    #     self._value.hasSourcePicoseconds = val._val
    #
    # @has_server_picoseconds.setter
    # def has_server_picoseconds(self, val):
    #     self._has_server_picoseconds = val
    #     self._value.hasServerPicoseconds = val._val

    def __str__(self, n=0):
        return ("(UaDataValue) :\n" +
                "\t" * (n + 1) + "variant" + self._variant.__str__(n + 1) +
                "\t" * (n + 1) + "source_timestamp" + self._source_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "server_timestamp" + self._server_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "source_picoseconds" + self._source_picoseconds.__str__(n + 1) +
                "\t" * (n + 1) + "server_picoseconds" + self._server_picoseconds.__str__(n + 1) +
                "\t" * (n + 1) + "status" + self._status.__str__(n + 1) +
                "\t" * (n + 1) + "has_variant" + self._has_variant.__str__(n + 1) +
                "\t" * (n + 1) + "has_status" + self._has_status.__str__(n + 1) +
                "\t" * (n + 1) + "has_source_timestamp" + self._has_source_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "has_server_timestamp" + self._has_server_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "has_source_picoseconds" + self._has_source_picoseconds.__str__(n + 1) +
                "\t" * (n + 1) + "has_server_picoseconds" + self._has_server_picoseconds.__str__(n + 1) + "\n")


class UaExtensionObject(UaType):
    def __init__(self, val=ffi.new("UA_ExtensionObject*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        self._encoding = UaExtensionObjectEncoding(val=val.encoding)
        if self._encoding._val in [0, 1, 2]:
            self._type = UaNodeId(val=val.content.encoded.typeId)
            self._data = UaByteString(val=val.content.encoded.body)
        elif self._encoding._val in [3, 4]:
            self._type = UaDataType(val=val.content.decoded.type, is_pointer=True)
            self._data = Void(val.content.encoded.body)
        else:
            raise ValueError(f"Encoding does not exist.")

    # TODO: might cause trouble since at _value[0] might not be enough memory for an other encoding type
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._encoding._value[0] = _val(val.encoding)
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

    # @type.setter
    # def type(self, val):
    #     if self._encoding._val in [0, 1, 2] and type(val) not in UaNodeId:
    #         raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaNodeId")
    #     if self._encoding._val in [3, 4] and type(val) not in UaDataType:
    #         raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaDataType")
    #     self._type = val
    #     self._value.type = val._val if self._encoding._val < 3 else val._ptr

    @property
    def data(self):
        return self._data

    # @data.setter
    # def data(self, val):
    #     if self._encoding._val in [0, 1, 2] and type(val) is not UaByteString:
    #         raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaNodeId")
    #     if self._encoding._val in [3, 4] and type(val) is not Void:
    #         val = Void(val)
    #
    #     self._data = val
    #     self._value.data = val._val if self._encoding._value < 3 else val._ptr

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

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
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

    # @has_symbolic_id.setter
    # def has_symbolic_id(self, val):
    #     self._has_symbolic_id = val
    #     self._value.hasSymbolicId = val._val
    #
    # @has_namespace_uri.setter
    # def has_namespace_uri(self, val):
    #     self._has_namespace_uri = val
    #     self._value.hasNamespaceUri = val._val
    #
    # @has_localized_text.setter
    # def has_localized_text(self, val):
    #     self._has_localized_text = val
    #     self._value.hasLocalizedText = val._val
    #
    # @has_locale.setter
    # def has_locale(self, val):
    #     self._has_locale = val
    #     self._value.hasLocale = val._val
    #
    # @has_additional_info.setter
    # def has_additional_info(self, val):
    #     self._has_additional_info = val
    #     self._value.hasAdditionalInfo = val._val
    #
    # @has_inner_status_code.setter
    # def has_inner_status_code(self, val):
    #     self._has_inner_status_code = val
    #     self._value.hasInnerStatusCode = val._val
    #
    # @has_inner_diagnostic_info.setter
    # def has_inner_diagnostic_info(self, val):
    #     self._has_inner_diagnostic_info = val
    #     self._value.hasInnerDiagnosticInfo = val._val
    #
    # @symbolic_id.setter
    # def symbolic_id(self, val):
    #     self._symbolic_id = val
    #     self._value.symbolicId = val._val
    #
    # @namespace_uri.setter
    # def namespace_uri(self, val):
    #     self._namespace_uri = val
    #     self._value.namespaceUri = val._val
    #
    # @localized_text.setter
    # def localized_text(self, val):
    #     self._localized_text = val
    #     self._value.localizedText = val._val
    #
    # @locale.setter
    # def locale(self, val):
    #     self._locale = val
    #     self._value.locale = val._val
    #
    # @additional_info.setter
    # def additional_info(self, val):
    #     self._additional_info = val
    #     self._value.additionalInfo = val._val
    #
    # @inner_status_code.setter
    # def inner_status_code(self, val):
    #     self._inner_status_code = val
    #     self._value.innerStatusCode = val._val
    #
    # @inner_diagnostic_info.setter
    # def inner_diagnostic_info(self, val):
    #     self._inner_diagnostic_info = val
    #     self._value.innerDiagnosticInfo = val._ptr

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

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._member_type_index._value[0] = _val(val.memberTypeIndex)
        self._padding._value[0] = _val(val.padding)
        self._namespace_zero._value[0] = _val(val.namespaceZero)
        self._is_array._value[0] = _val(val.isArray)
        self._is_optional._value[0] = _val(val.isOptional)
        self._member_name._value = val.memberName

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

    # @member_type_index.setter
    # def member_type_index(self, val):
    #     self._member_type_index = val
    #     self._value.memberTypeIndex = val._val
    #
    # @padding.setter
    # def padding(self, val):
    #     self._padding = val
    #     self._value.padding = val._val
    #
    # @namespace_zero.setter
    # def namespace_zero(self, val):
    #     self._namespace_zero = val
    #     self._value.namespaceZero = val._val
    #
    # @is_array.setter
    # def is_array(self, val):
    #     self._is_array = val
    #     self._value.isArray = val._val
    #
    # @is_optional.setter
    # def is_optional(self, val):
    #     self._is_optional = val
    #     self._value.isOptional = val._val
    #
    # @member_name.setter
    # def member_name(self, val):
    #     self._member_name = val
    #     self._value.memberName = val._ptr

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

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
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

    # @type_id.setter
    # def type_id(self, val):
    #     self._type_id = val
    #     self._value.typeId = val._val
    #
    # @binary_encoding_id.setter
    # def binary_encoding_id(self, val):
    #     self._binary_encoding_id = val
    #     self._value.binaryEncodingId = val._val
    #
    # @mem_size.setter
    # def mem_size(self, val):
    #     self._mem_size = val
    #     self._value.memSize = val._val
    #
    # @type_index.setter
    # def type_index(self, val):
    #     self._type_index = val
    #     self._value.typeIndex = val._val
    #
    # @type_kind.setter
    # def type_kind(self, val):
    #     self._type_kind = val
    #     self._value.typeKind = val._val
    #
    # @pointer_free.setter
    # def pointer_free(self, val):
    #     self._pointer_free = val
    #     self._value.pointerFree = val._val
    #
    # @overlayable.setter
    # def overlayable(self, val):
    #     self._overlayable = val
    #     self._value.overlayable = val._val
    #
    # @members_size.setter
    # def members_size(self, val):
    #     self._members_size = val
    #     self._value.membersSize = val._val
    #
    # @members.setter
    # def members(self, val):
    #     self._members = val
    #     self._value.members = val._ptr
    #
    # @type_name.setter
    # def type_name(self, val):
    #     self._type_name = val
    #     self._value.typeName = val._ptr

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
        return lib.UA_DataType_isNumeric(self._ptr)

    @staticmethod
    def find_by_node_id(type_id: UaNodeId):
        return UaDataType(val=ffi.new("UA_DataType*", lib.UA_findDataType(type_id._ptr)), is_pointer=True)

    # TODO: generic type handling!!!
    # ----> init, copy, new, array_new, array_copy should be methods of a class, which represent members of an in an
    # attribute provided UaDataType
    # returns void ptr
    def new_instance(self):
        return lib.UA_new(self._ptr)


# +++++++++++++++++++ UaDataTypeArray +++++++++++++++++++++++
class UaDataTypeArray(UaType):
    def __init__(self, val=ffi.new("UA_DataTypeArray*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        self._next = UaDataTypeArray(val=val.next, is_pointer=True)
        self._types_size = SizeT(val=val.typesSize, is_pointer=False)
        self._types = UaDataType(val=val.types, is_pointer=True)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "")
        else:
            self._value[0] = _val(val)
        self._next._value = val.next
        self._types_size._value[0] = _val(val.typesSize)
        self._types._value = val.types

    @property
    def next(self):
        return self._next

    @property
    def types_size(self):
        return self._types_size

    @property
    def types(self):
        return self._types

    # @next.setter
    # def next(self, val):
    #     self._next = val
    #     self._value.next = val._ptr
    #
    # @types_size.setter
    # def types_size(self, val):
    #     self._types_size = val
    #     self._value.typesSize = val._val
    #
    # @types.setter
    # def types(self, val):
    #     self._types = val
    #     self._value.types = val._ptr

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