# TODO: How to handle arrays?
# TODO: insert content of basetypes.py in this file

class UaType:
    def __init__(self, val, is_pointer=False):
        self._value = val
        self._is_pointer = is_pointer

    @property
    def value(self):
        if self._is_pointer:
            return self._value
        else:
            return self._value[0]

    def _ref(self):
        return self._value

    def _deref(self):
        return self._value[0]

    def __str__(self):
        return str(self._value)


# +++++++++++++++++++ SizeT +++++++++++++++++++++++
class SizeT(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("SizeT*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("SizeT*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range") from e

    def __str__(self):
        return "SizeT: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "SizeT: " + str(self._p_value)


# +++++++++++++++++++ Char +++++++++++++++++++++++
class Char(UaType):
    def __init__(self, p_val: bytes = bytes(), is_pointer=True, val=None):
        if p_val is None:
            p_val = []
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
    def p_value(self, val:bytes):
        self._p_value = val
        self._value = ffi.new("char[]", self._p_value)

    def __str__(self):
        return "Char*: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "Char*: " + str(self._p_value)


# -----------------------------------------------------------------
# ----------------------------- common.h --------------------------
# -----------------------------------------------------------------

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
            super().__init__(ffi.new("UA_AttributeId*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaAttributeId: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_RuleHandling*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaRuleHandling: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_Order*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaOrder: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_SecureChannelState*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaSecureChannelState: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_SessionState*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaSessionState: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


# +++++++++++++++++++ UaNetworkStatistics +++++++++++++++++++++++
class UaNetworkStatistics(UaType):
    def __init__(self, val=ffi.new("UA_NetworkStatistics*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._current_connection_count = SizeT(val=val.currentConnectionCount, is_pointer=is_pointer)
        self._cumulated_connection_count = SizeT(val=val.cumulatedConnectionCount, is_pointer=is_pointer)
        self._rejected_connection_count = SizeT(val=val.rejectedConnectionCount, is_pointer=is_pointer)
        self._connection_timeout_count = SizeT(val=val.connectionTimeoutCount, is_pointer=is_pointer)
        self._connection_abort_count = SizeT(val=val.connectionAbortCount, is_pointer=is_pointer)

    @property
    def current_connection_count(self):
        return self._current_connection_count

    @current_connection_count.setter
    def current_connection_count(self, val):
        self._current_connection_count = val
        self._value.currentConnectionCount = val.value

    @property
    def cumulated_connection_count(self):
        return self._cumulated_connection_count

    @cumulated_connection_count.setter
    def cumulated_connection_count(self, val):
        self._cumulated_connection_count = val
        self._value.cumulatedConnectionCount = val.value

    @property
    def rejected_connection_count(self):
        return self._rejected_connection_count

    @rejected_connection_count.setter
    def rejected_connection_count(self, val):
        self._rejected_connection_count = val
        self._value.rejectedConnectionCount = val.value

    @property
    def connection_timeout_count(self):
        return self._connection_timeout_count

    @connection_timeout_count.setter
    def connection_timeout_count(self, val):
        self._connection_timeout_count = val
        self._value.connectionTimeoutCount = val.value

    @property
    def connection_abort_count(self):
        return self._connection_abort_count

    @connection_abort_count.setter
    def connection_abort_count(self, val):
        self._connection_abort_count = val
        self._value.connectionAbortCount = val.value

    def __str__(self):
        return ("UaNetworkStatistics:\n" +
                self._current_connection_count.str_helper(1) +
                self._cumulated_connection_count.str_helper(1) +
                self._rejected_connection_count.str_helper(1) +
                self._connection_timeout_count.str_helper(1) +
                self._connection_abort_count.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaNetworkStatistics:\n" +
                self._current_connection_count.str_helper(n + 1) +
                self._cumulated_connection_count.str_helper(n + 1) +
                self._rejected_connection_count.str_helper(n + 1) +
                self._connection_timeout_count.str_helper(n + 1) +
                self._connection_abort_count.str_helper(n + 1))


# +++++++++++++++++++ UaSecureChannelStatistics +++++++++++++++++++++++
class UaSecureChannelStatistics(UaType):
    def __init__(self, val=ffi.new("UA_SecureChannelStatistics*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._current_channel_count = SizeT(val=val.currentChannelCount, is_pointer=is_pointer)
        self._cumulated_channel_count = SizeT(val=val.cumulatedChannelCount, is_pointer=is_pointer)
        self._rejected_channel_count = SizeT(val=val.rejectedChannelCount, is_pointer=is_pointer)
        self._channel_timeout_count = SizeT(val=val.channelTimeoutCount, is_pointer=is_pointer)
        self._channel_abort_count = SizeT(val=val.channelAbortCount, is_pointer=is_pointer)
        self._channel_purge_count = SizeT(val=val.channelPurgeCount, is_pointer=is_pointer)

    @property
    def current_channel_count(self):
        return self._current_channel_count

    @current_channel_count.setter
    def current_channel_count(self, val):
        self._current_channel_count = val
        self._value.currentChannelCount = val.value

    @property
    def cumulated_channel_count(self):
        return self._cumulated_channel_count

    @cumulated_channel_count.setter
    def cumulated_channel_count(self, val):
        self._cumulated_channel_count = val
        self._value.cumulatedChannelCount = val.value

    @property
    def rejected_channel_count(self):
        return self._rejected_channel_count

    @rejected_channel_count.setter
    def rejected_channel_count(self, val):
        self._rejected_channel_count = val
        self._value.rejectedChannelCount = val.value

    @property
    def channel_timeout_count(self):
        return self._channel_timeout_count

    @channel_timeout_count.setter
    def channel_timeout_count(self, val):
        self._channel_timeout_count = val
        self._value.channelTimeoutCount = val.value

    @property
    def channel_abort_count(self):
        return self._channel_abort_count

    @channel_abort_count.setter
    def channel_abort_count(self, val):
        self._channel_abort_count = val
        self._value.channelAbortCount = val.value

    @property
    def channel_purge_count(self):
        return self._channel_purge_count

    @channel_purge_count.setter
    def channel_purge_count(self, val):
        self._channel_purge_count = val
        self._value.channelPurgeCount = val.value

    def __str__(self):
        return ("UaSecureChannelStatistics:\n" +
                self._current_channel_count.str_helper(1) +
                self._cumulated_channel_count.str_helper(1) +
                self._rejected_channel_count.str_helper(1) +
                self._channel_timeout_count.str_helper(1) +
                self._channel_abort_count.str_helper(1) +
                self._channel_purge_count.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaSecureChannelStatistics:\n" +
                self._current_channel_count.str_helper(n + 1) +
                self._cumulated_channel_count.str_helper(n + 1) +
                self._rejected_channel_count.str_helper(n + 1) +
                self._channel_timeout_count.str_helper(n + 1) +
                self._channel_abort_count.str_helper(n + 1) +
                self._channel_purge_count.str_helper(n + 1))


# +++++++++++++++++++ UaSessionStatistics +++++++++++++++++++++++
class UaSessionStatistics(UaType):
    def __init__(self, val=ffi.new("UA_SessionStatistics*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._current_session_count = SizeT(val=val.currentSessionCount, is_pointer=is_pointer)
        self._cumulated_session_count = SizeT(val=val.cumulatedSessionCount, is_pointer=is_pointer)
        self._security_rejected_session_count = SizeT(val=val.securityRejectedSessionCount, is_pointer=is_pointer)
        self._rejected_session_count = SizeT(val=val.rejectedSessionCount, is_pointer=is_pointer)
        self._session_timeout_count = SizeT(val=val.sessionTimeoutCount, is_pointer=is_pointer)
        self._session_abort_count = SizeT(val=val.sessionAbortCount, is_pointer=is_pointer)

    @property
    def current_session_count(self):
        return self._current_session_count

    @current_session_count.setter
    def current_session_count(self, val):
        self._current_session_count = val
        self._value.currentSessionCount = val.value

    @property
    def cumulated_session_count(self):
        return self._cumulated_session_count

    @cumulated_session_count.setter
    def cumulated_session_count(self, val):
        self._cumulated_session_count = val
        self._value.cumulatedSessionCount = val.value

    @property
    def security_rejected_session_count(self):
        return self._security_rejected_session_count

    @security_rejected_session_count.setter
    def security_rejected_session_count(self, val):
        self._security_rejected_session_count = val
        self._value.securityRejectedSessionCount = val.value

    @property
    def rejected_session_count(self):
        return self._rejected_session_count

    @rejected_session_count.setter
    def rejected_session_count(self, val):
        self._rejected_session_count = val
        self._value.rejectedSessionCount = val.value

    @property
    def session_timeout_count(self):
        return self._session_timeout_count

    @session_timeout_count.setter
    def session_timeout_count(self, val):
        self._session_timeout_count = val
        self._value.sessionTimeoutCount = val.value

    @property
    def session_abort_count(self):
        return self._session_abort_count

    @session_abort_count.setter
    def session_abort_count(self, val):
        self._session_abort_count = val
        self._value.sessionAbortCount = val.value

    def __str__(self):
        return ("UaSessionStatistics:\n" +
                self._current_session_count.str_helper(1) +
                self._cumulated_session_count.str_helper(1) +
                self._security_rejected_session_count.str_helper(1) +
                self._rejected_session_count.str_helper(1) +
                self._session_timeout_count.str_helper(1) +
                self._session_abort_count.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaSessionStatistics:\n" +
                self._current_session_count.str_helper(n + 1) +
                self._cumulated_session_count.str_helper(n + 1) +
                self._security_rejected_session_count.str_helper(n + 1) +
                self._rejected_session_count.str_helper(n + 1) +
                self._session_timeout_count.str_helper(n + 1) +
                self._session_abort_count.str_helper(n + 1))


# -----------------------------------------------------------------
# ----------------------------- types.h --------------------------
# -----------------------------------------------------------------

# +++++++++++++++++++ UaBoolean +++++++++++++++++++++++
class UaBoolean(UaType):
    def __init__(self, p_val=False, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_Boolean*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        self._p_value = val
        self._value = ffi.new("UA_Boolean*", val)

    def __str__(self):
        return "UaBoolean: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaBoolean: " + str(self._p_value)


# +++++++++++++++++++ UaSByte +++++++++++++++++++++++
class UaSByte(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is not None:
            super().__init__(val, is_pointer)
            self._p_value = val[0]
        else:
            super().__init__(ffi.new("UA_SByte*", p_val), is_pointer)
            self._p_value = None

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_SByte*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range -128 .. 127") from e

    def __str__(self):
        return "UaSByte: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaSByte: " + str(self._p_value)


# +++++++++++++++++++ UaByte +++++++++++++++++++++++
class UaByte(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_Byte*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_Byte*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range 0 .. 255") from e

    def __str__(self):
        return "UaByte: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaByte: " + str(self._p_value)


# +++++++++++++++++++ UaInt16 +++++++++++++++++++++++
class UaInt16(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_Int16*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val,is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_Int16*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range -32,768 .. 32,767") from e

    def __str__(self):
        return "UaInt16: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaInt16: " + str(self._p_value)


# +++++++++++++++++++ UaUInt16 +++++++++++++++++++++++
class UaUInt16(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_UInt16*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_UInt16*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range 0 .. 65,535") from e

    def __str__(self):
        return "UaUInt16: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaUInt16: " + str(self._p_value)

# +++++++++++++++++++ UaInt32 +++++++++++++++++++++++
class UaInt32(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_Int32*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_Int32*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range -2,147,483,648 .. 2,147,483,647") from e

    def __str__(self):
        return "UaInt32: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaInt32: " + str(self._p_value)


# +++++++++++++++++++ UaUInt32 +++++++++++++++++++++++
class UaUInt32(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_UInt32*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_UInt32*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range 0 .. 4,294,967,295") from e

    def __str__(self):
        return "UaUInt32: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaUInt32: " + str(self._p_value)


# +++++++++++++++++++ UaInt64 +++++++++++++++++++++++
class UaInt64(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_Int64*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_Int64*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range -9,223,372,036,854,775,808 .. 9,223,372,036,854,775,807") from e

    def __str__(self):
        return "UaInt64: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaInt64: " + str(self._p_value)


# +++++++++++++++++++ UaUInt64 +++++++++++++++++++++++
class UaUInt64(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_UInt64*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_UInt64*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range 0 .. 18,446,744,073,709,551,615") from e

    def __str__(self):
        return "UaUInt64: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaUInt64: " + str(self._p_value)


# +++++++++++++++++++ UaFloat +++++++++++++++++++++++
class UaFloat(UaType):
    def __init__(self, p_val=0.0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_Float*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_Float*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range -3.4E38 .. 3.4E38") from e

    def __str__(self):
        return "UaFloat: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaFloat: " + str(self._p_value)


# +++++++++++++++++++ UaDouble +++++++++++++++++++++++
class UaDouble(UaType):
    def __init__(self, p_val=0.0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_Double*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_Double*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range -1.7E308 .. 1.7E308") from e

    def __str__(self):
        return "UaDouble: " + str(self._p_value)

    def str_helper(self, n: int):
        return "\t" * n + "UaDouble: " + str(self._p_value)


# +++++++++++++++++++ UaStatusCode +++++++++++++++++++++++
class UaStatusCode(UaType):
    @staticmethod
    def code_is_bad(status_code):
        return lib.UA_StatusCode_isBad(status_code)

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

    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_StatusCode*", p_val), is_pointer)
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
            self._value = ffi.new("UA_StatusCode*", val)
        else:
            raise ValueError(f"{val} is no legal status code")

    def __str__(self):
        return f"UaStatusCode: {UaStatusCode.val_to_string[self._p_value]} ({self._p_value})"

    def str_helper(self, n: int):
        return "\t" * n + self.__str__()

    def is_bad(self):
        return lib.UA_StatusCode_isBad(self.value)


# +++++++++++++++++++ UaDateTime +++++++++++++++++++++++
class UaDateTime(UaType):
    def __init__(self, p_val=0, is_pointer=False, val=None):
        if val is None:
            super().__init__(ffi.new("UA_DateTime*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        try:
            self._p_value = val
            self._value = ffi.new("UA_DateTime*", val)
        except OverflowError as e:
            raise OverflowError(f"{val} is not in range -4,294,967,295 .. 4,294,967,295") from e

    def __str__(self):
        return f"UA_DateTime: {self._p_value}"

    def str_helper(self, n: int):
        return "\t" * n + self.__str__()

    @staticmethod
    def now():
        return UaDateTime(lib.UA_DateTime_now())


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
    UA_EXTENSIONOBJECT_ENCODED_NOBODY = 0
    UA_EXTENSIONOBJECT_ENCODED_BYTESTRING = 1
    UA_EXTENSIONOBJECT_ENCODED_XML = 2
    UA_EXTENSIONOBJECT_DECODED = 3
    UA_EXTENSIONOBJECT_DECODED_NODELETE = 4

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
        return "\t" * n + str(self)


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

    # byte array of length 8
    @data4.setter
    def data4(self, val):
        self._data4 = val
        self._value.data4 = val.value

    def __eq__(self, other):
        return lib.UA_Guid_equal(self._value, other._value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        d1 = '{0:0{1}X}'.format(self._data1.value, 8)
        d2 = '{0:0{1}X}'.format(self._data2.value, 4)
        d3 = '{0:0{1}X}'.format(self._data3.value, 4)
        d4 = ""
        for i in range(2):
            d4 += '{0:0{1}X}'.format(self._data4.value[i], 2)
        d5 = ""
        for i in range(2, 8):
            d5 += '{0:0{1}X}'.format(self._data4.value[i], 2)

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
        self._identifier = cases[self._identifier_type]

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

    def __init__(self, ns_index=None, ident=None, val=ffi.new("UA_ExpandedNodeId*"), is_pointer=False):
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
        return ("\t" * n + "UaExpandedNodeId:\n" +
                self._node_id.str_helper(n + 1) +
                self._namespace_uri.str_helper(n + 1) +
                self._server_index.str_helper(n + 1))

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
    def __init__(self, ns_index=None, string=None, val=ffi.new("UA_QualifiedName*"), is_pointer=False):
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
        return ("\t" * n + "UaQualifiedName:\n" +
                self._namespace_index.str_helper(n + 1) +
                self._name.str_helper(n + 1))

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
        return ("\t" * n + "UaLocalizedText:\n" +
                self._locale.str_helper(n + 1) +
                self._text.str_helper(n + 1))


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
        return ("\t" * n + "UaNumericRangeDimension:\n" +
                self._min.str_helper(n + 1) +
                self._max.str_helper(n + 1))


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
        return self._dimension

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
        return self._type

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
                self._type.str_helper(1) +
                self._storage_type.str_helper(1) +
                self._array_length.str_helper(1) +
                self._data.str_helper(1) +
                self._array_dimensions_size.str_helper(1) +
                self._array_dimensions.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaVariant:\n" +
                self._type.str_helper(n + 1) +
                self._storage_type.str_helper(n + 1) +
                self._array_length.str_helper(n + 1) +
                self._data.str_helper(n + 1) +
                self._array_dimensions_size.str_helper(n + 1) +
                self._array_dimensions.str_helper(n + 1))

    def is_empty(self):
        lib.UA_Variant_isEmpty(self._value)

    def is_scalar(self):
        lib.UA_Variant_isScalar(self._value)

    def has_scalar_type(self, data_type):
        lib.UA_Variant_hasScalarType(self._value, data_type._ref())

    def has_array_type(self, data_type):
        lib.UA_Variant_hasArrayType(self._value, data_type._ref())

    def _set_attributes(self):
        self._type = self._value.type
        self._storage_type = self._value.storageType
        self._array_length = self._value.arrayLength
        self._data = self._value.data
        self._array_dimensions_size = self._value.arrayDimensionsSize
        self._array_dimensions = self._value.arrayDimensions

    def set_scalar(self, data, data_type):
        lib.UA_Variant_setScalarCopy(self.value, ffi.new_handle(data), data_type._ref())
        self._set_attributes()

    def set_array(self, array, size, data_type):
        if size is int:
            size = SizeT(size)
        if size is not SizeT:
            raise AttributeError(f"size={size} has to be int or SizeT")
        status_code = lib.UA_Variant_setArrayCopy(self._value, ffi.new_handle(array), size._deref(), data_type._ref())
        status_code = UaStatusCode(status_code)
        if not status_code.is_bad():
            self._set_attributes()
        else:
            raise Exception(f"An Error occured - {str(status_code)}")

    def copy_range_to(self, variant, num_range: UaNumericRange):
        status_code = lib.UA_Variant_copyRange(self._value, variant._ref(), num_range._deref())
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
        status_code = lib.UA_Variant_setRangeCopy(self._value, ffi.new_handle(array), size, num_range._deref())
        status_code = UaStatusCode(status_code)
        if not status_code.is_bad():
            self._set_attributes()
        else:
            raise AttributeError(f"An Error occured - {str(status_code)}")


# +++++++++++++++++++ UaExtensionObject +++++++++++++++++++++++
class UaExtensionObject(UaType):
    def __init__(self, val=ffi.new("UA_ExtensionObject*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._encoding = UaExtensionObjectEncoding(val=val.encoding)
        if self._encoding in [0, 1, 2]:
            self._type = UaNodeId(val=val.content.encoded.typeId)
            self._data = UaByteString(val=val.content.encoded.body)
        elif self._encoding in [3, 4]:
            self._type = UaDataType(val=val.content.decoded.type, is_pointer=True)
            # data not void *
            self._data = ffi.from_handle(val.content.encoded.body)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        if self._encoding in [0, 1, 2] and val not in UaNodeId:
            raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaNodeId")
        if self._encoding in [3, 4] and val not in UaDataType:
            raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaDataType")
        self._type = val
        self._value.type = val.value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        if self._encoding in [0, 1, 2] and val not in UaByteString:
            raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaNodeId")
        if self._encoding in [3, 4] and val is not type(ffi.new_handle()):
            self._data = val
            val = ffi.new_handle(val)

        self._value.data = val

    def __str__(self):
        return ("UaExtensionObject:\n" +
                self._type.str_helper(1) +
                self._data.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaExtensionObject:\n" +
                self._type.str_helper(n + 1) +
                self._data.str_helper(n + 1))


# +++++++++++++++++++ UaDataValue +++++++++++++++++++++++
class UaDataValue(UaType):
    def __init__(self, val=ffi.new("UA_DataValue*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._variant = UaVariant(val=val.value)
        self._source_timestamp = UaDateTime(val=val.sourceTimestamp)
        self._server_timestamp = UaDateTime(val=val.serverTimestamp)
        self._source_picoseconds = UaUInt16(val=val.sourcePicoseconds)
        self._server_picoseconds = UaUInt16(val=val.serverPicoseconds)
        self._status = UaStatusCode(val=val.status)
        self._has_value = UaBoolean(val=val.hasValue)
        self._has_status = UaBoolean(val=val.hasStatus)
        self._has_source_timestamp = UaBoolean(val=val.hasSourceTimestamp)
        self._has_server_timestamp = UaBoolean(val=val.hasServerTimestamp)
        self._has_source_picoseconds = UaBoolean(val=val.hasSourcePicoseconds)
        self._has_server_picoseconds = UaBoolean(val=val.hasServerPicoseconds)

    @property
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, val):
        self._variant = val
        self._value.value = val.value

    @property
    def source_timestamp(self):
        return self._source_timestamp

    @source_timestamp.setter
    def source_timestamp(self, val):
        self._source_timestamp = val
        self._value.sourceTimestamp = val.value

    @property
    def server_timestamp(self):
        return self._server_timestamp

    @server_timestamp.setter
    def server_timestamp(self, val):
        self._server_timestamp = val
        self._value.serverTimestamp = val.value

    @property
    def source_picoseconds(self):
        return self._source_picoseconds

    @source_picoseconds.setter
    def source_picoseconds(self, val):
        self._source_picoseconds = val
        self._value.sourcePicoseconds = val.value

    @property
    def server_picoseconds(self):
        return self._server_picoseconds

    @server_picoseconds.setter
    def server_picoseconds(self, val):
        self._server_picoseconds = val
        self._value.serverPicoseconds = val.value

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
        self._value.hasValue = val.value

    @property
    def has_status(self):
        return self._has_status

    @has_status.setter
    def has_status(self, val):
        self._has_status = val
        self._value.hasStatus = val.value

    @property
    def has_source_timestamp(self):
        return self._has_source_timestamp

    @has_source_timestamp.setter
    def has_source_timestamp(self, val):
        self._has_source_timestamp = val
        self._value.hasSourceTimestamp = val.value

    @property
    def has_server_timestamp(self):
        return self._has_server_timestamp

    @has_server_timestamp.setter
    def has_server_timestamp(self, val):
        self._has_server_timestamp = val
        self._value.hasServerTimestamp = val.value

    @property
    def has_source_picoseconds(self):
        return self._has_source_timestamp

    @has_source_picoseconds.setter
    def has_source_picoseconds(self, val):
        self._has_source_picoseconds = val
        self._value.hasSourcePicoseconds = val.value

    @property
    def has_server_picoseconds(self):
        return self._has_server_picoseconds

    @has_server_picoseconds.setter
    def has_server_picoseconds(self, val):
        self._has_server_picoseconds = val
        self._value.hasServerPicoseconds = val.value

    def __str__(self):
        return ("UaDataValue:\n" +
                self._variant.str_helper(1) +
                self._source_timestamp.str_helper(1) +
                self._server_timestamp.str_helper(1) +
                self._source_picoseconds.str_helper(1) +
                self._server_picoseconds.str_helper(1) +
                self._status.str_helper(1) +
                self._has_value.str_helper(1) +
                self._has_status.str_helper(1) +
                self._has_source_timestamp.str_helper(1) +
                self._has_server_timestamp.str_helper(1) +
                self._has_source_picoseconds.str_helper(1) +
                self._has_server_picoseconds.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaDataValue:\n" +
                self._variant.str_helper(n + 1) +
                self._source_timestamp.str_helper(n + 1) +
                self._server_timestamp.str_helper(n + 1) +
                self._source_picoseconds.str_helper(n + 1) +
                self._server_picoseconds.str_helper(n + 1) +
                self._status.str_helper(n + 1) +
                self._has_value.str_helper(n + 1) +
                self._has_status.str_helper(n + 1) +
                self._has_source_timestamp.str_helper(n + 1) +
                self._has_server_timestamp.str_helper(n + 1) +
                self._has_source_picoseconds.str_helper(n + 1) +
                self._has_server_picoseconds.str_helper(n + 1))


# +++++++++++++++++++ UaDiagnosticInfo +++++++++++++++++++++++
class UaDiagnosticInfo(UaType):
    def __init__(self, val=ffi.new("UA_DiagnosticInfo*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._has_symbolic_id = UaBoolean(val=val.hasSymbolicId)
        self._has_namespace_uri = UaBoolean(val=val.hasNamespaceUri)
        self._has_localized_text = UaBoolean(val=val.hasLocalizedText)
        self._has_locale = UaBoolean(val=val.hasLocale)
        self._has_additional_info = UaBoolean(val=val.hasAdditionalInfo)
        self._has_inner_status_code = UaBoolean(val=val.hasInnerStatusCode)
        self._has_inner_diagnostic_info = UaBoolean(val=val.hasInnerDiagnosticInfo)
        self._symbolic_id = UaInt32(val=val.symbolicId)
        self._namespace_uri = UaInt32(val=val.namespaceUri)
        self._localized_text = UaInt32(val=val.localizedText)
        self._locale = UaInt32(val=val.locale)
        self._additional_info = UaString(val=val.additionalInfo)
        self._inner_status_code = UaStatusCode(val=val.innerStatusCode)
        self._inner_diagnostic_info = UaDiagnosticInfo(val=val.innerDiagnosticInfo, is_pointer=True)

    @property
    def has_symbolic_id(self):
        return self._has_symbolic_id

    @has_symbolic_id.setter
    def has_symbolic_id(self, val):
        self._has_symbolic_id = val
        self._value.hasSymbolicId = val.value

    @property
    def has_namespace_uri(self):
        return self._has_namespace_uri

    @has_namespace_uri.setter
    def has_namespace_uri(self, val):
        self._has_namespace_uri = val
        self._value.hasNamespaceUri = val.value

    @property
    def has_localized_text(self):
        return self._has_localized_text

    @has_localized_text.setter
    def has_localized_text(self, val):
        self._has_localized_text = val
        self._value.hasLocalizedText = val.value

    @property
    def has_locale(self):
        return self._has_locale

    @has_locale.setter
    def has_locale(self, val):
        self._has_locale = val
        self._value.hasLocale = val.value

    @property
    def has_additional_info(self):
        return self._has_additional_info

    @has_additional_info.setter
    def has_additional_info(self, val):
        self._has_additional_info = val
        self._value.hasAdditionalInfo = val.value

    @property
    def has_inner_status_code(self):
        return self._has_inner_status_code

    @has_inner_status_code.setter
    def has_inner_status_code(self, val):
        self._has_inner_status_code = val
        self._value.hasInnerStatusCode = val.value

    @property
    def has_inner_diagnostic_info(self):
        return self._has_inner_diagnostic_info

    @has_inner_diagnostic_info.setter
    def has_inner_diagnostic_info(self, val):
        self._has_inner_diagnostic_info = val
        self._value.hasInnerDiagnosticInfo = val.value

    @property
    def symbolic_id(self):
        return self._symbolic_id

    @symbolic_id.setter
    def symbolic_id(self, val):
        self._symbolic_id = val
        self._value.symbolicId = val.value

    @property
    def namespace_uri(self):
        return self._namespace_uri

    @namespace_uri.setter
    def namespace_uri(self, val):
        self._namespace_uri = val
        self._value.namespaceUri = val.value

    @property
    def localized_text(self):
        return self._localized_text

    @localized_text.setter
    def localized_text(self, val):
        self._localized_text = val
        self._value.localizedText = val.value

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, val):
        self._locale = val
        self._value.locale = val.value

    @property
    def additional_info(self):
        return self._additional_info

    @additional_info.setter
    def additional_info(self, val):
        self._additional_info = val
        self._value.additionalInfo = val.value

    @property
    def inner_status_code(self):
        return self._inner_status_code

    @inner_status_code.setter
    def inner_status_code(self, val):
        self._inner_status_code = val
        self._value.innerStatusCode = val.value

    @property
    def inner_diagnostic_info(self):
        return self._inner_diagnostic_info

    @inner_diagnostic_info.setter
    def inner_diagnostic_info(self, val):
        self._inner_diagnostic_info = val
        self._value.innerDiagnosticInfo = val.value

    def __str__(self):
        return ("UaDiagnosticInfo:\n" +
                self._has_symbolic_id.str_helper(1) +
                self._has_namespace_uri.str_helper(1) +
                self._has_localized_text.str_helper(1) +
                self._has_locale.str_helper(1) +
                self._has_additional_info.str_helper(1) +
                self._has_inner_status_code.str_helper(1) +
                self._has_inner_diagnostic_info.str_helper(1) +
                self._symbolic_id.str_helper(1) +
                self._namespace_uri.str_helper(1) +
                self._localized_text.str_helper(1) +
                self._locale.str_helper(1) +
                self._additional_info.str_helper(1) +
                self._inner_status_code.str_helper(1) +
                self._inner_diagnostic_info.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaDiagnosticInfo:\n" +
                self._has_symbolic_id.str_helper(n + 1) +
                self._has_namespace_uri.str_helper(n + 1) +
                self._has_localized_text.str_helper(n + 1) +
                self._has_locale.str_helper(n + 1) +
                self._has_additional_info.str_helper(n + 1) +
                self._has_inner_status_code.str_helper(n + 1) +
                self._has_inner_diagnostic_info.str_helper(n + 1) +
                self._symbolic_id.str_helper(n + 1) +
                self._namespace_uri.str_helper(n + 1) +
                self._localized_text.str_helper(n + 1) +
                self._locale.str_helper(n + 1) +
                self._additional_info.str_helper(n + 1) +
                self._inner_status_code.str_helper(n + 1) +
                self._inner_diagnostic_info.str_helper(n + 1))


# +++++++++++++++++++ UaDataTypeMember +++++++++++++++++++++++
class UaDataTypeMember(UaType):
    def __init__(self, val=ffi.new("UA_DataTypeMember*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._member_type_index = UaUInt16(val=val.memberTypeIndex)
        self._padding = UaByte(val=val.padding)
        self._namespace_zero = UaBoolean(val=val.namespaceZero)
        self._is_array = UaBoolean(val=val.isArray)
        self._is_optional = UaBoolean(val=val.isOptional)
        self._member_name = Char(val=val.memberName)

    @property
    def member_type_index(self):
        return self._member_type_index

    @member_type_index.setter
    def member_type_index(self, val):
        self._member_type_index = val
        self._value.memberTypeIndex = val.value

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, val):
        self._padding = val
        self._value.padding = val.value

    @property
    def namespace_zero(self):
        return self._namespace_zero

    @namespace_zero.setter
    def namespace_zero(self, val):
        self._namespace_zero = val
        self._value.namespaceZero = val.value

    @property
    def is_array(self):
        return self._is_array

    @is_array.setter
    def is_array(self, val):
        self._is_array = val
        self._value.isArray = val.value

    @property
    def is_optional(self):
        return self._is_optional

    @is_optional.setter
    def is_optional(self, val):
        self._is_optional = val
        self._value.isOptional = val.value

    @property
    def member_name(self):
        return self._member_name

    @member_name.setter
    def member_name(self, val):
        self._member_name = val
        self._value.memberName = val.value

    def __str__(self):
        return ("UaDataTypeMember:\n" +
                self._member_type_index.str_helper(1) +
                self._padding.str_helper(1) +
                self._namespace_zero.str_helper(1) +
                self._is_array.str_helper(1) +
                self._is_optional.str_helper(1) +
                self._member_name.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaDataTypeMember:\n" +
                self._member_type_index.str_helper(n + 1) +
                self._padding.str_helper(n + 1) +
                self._namespace_zero.str_helper(n + 1) +
                self._is_array.str_helper(n + 1) +
                self._is_optional.str_helper(n + 1) +
                self._member_name.str_helper(n + 1))


# +++++++++++++++++++ UaDataType +++++++++++++++++++++++
class UaDataType(UaType):
    def __init__(self, val=ffi.new("UA_DataType*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._type_id = UaNodeId(val=val.typeId)
        self._binary_encoding_id = UaNodeId(val=val.binaryEncodingId)
        self._mem_size = UaUInt16(val=val.memSize)
        self._type_index = UaUInt16(val=val.typeIndex)
        self._type_kind = UaUInt32(val=val.typeKind)
        self._pointer_free = UaUInt32(val=val.pointerFree)
        self._overlayable = UaUInt32(val=val.overlayable)
        self._members_size = UaUInt32(val=val.membersSize)
        self._members = UaDataTypeMember(val=val.members, is_pointer=True)
        self._type_name = Char(val=val.typeName, is_pointer=True)

    @property
    def type_id(self):
        return self._type_id

    @type_id.setter
    def type_id(self, val):
        self._type_id = val
        self._value.typeId = val.value

    @property
    def binary_encoding_id(self):
        return self._binary_encoding_id

    @binary_encoding_id.setter
    def binary_encoding_id(self, val):
        self._binary_encoding_id = val
        self._value.binaryEncodingId = val.value

    @property
    def mem_size(self):
        return self._mem_size

    @mem_size.setter
    def mem_size(self, val):
        self._mem_size = val
        self._value.memSize = val.value

    @property
    def type_index(self):
        return self._type_index

    @type_index.setter
    def type_index(self, val):
        self._type_index = val
        self._value.typeIndex = val.value

    @property
    def type_kind(self):
        return self._type_kind

    @type_kind.setter
    def type_kind(self, val):
        self._type_kind = val
        self._value.typeKind = val.value

    @property
    def pointer_free(self):
        return self._pointer_free

    @pointer_free.setter
    def pointer_free(self, val):
        self._pointer_free = val
        self._value.pointerFree = val.value

    @property
    def overlayable(self):
        return self._overlayable

    @overlayable.setter
    def overlayable(self, val):
        self._overlayable = val
        self._value.overlayable = val.value

    @property
    def members_size(self):
        return self._members_size

    @members_size.setter
    def members_size(self, val):
        self._members_size = val
        self._value.membersSize = val.value

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, val):
        self._members = val
        self._value.members = val.value

    @property
    def type_name(self):
        return self._type_name

    @type_name.setter
    def type_name(self, val):
        self._type_name = val
        self._value.typeName = val.value

    def __str__(self):
        return ("UaDataType:\n" +
                self._type_id.str_helper(1) +
                self._binary_encoding_id.str_helper(1) +
                self._mem_size.str_helper(1) +
                self._type_index.str_helper(1) +
                self._type_kind.str_helper(1) +
                self._pointer_free.str_helper(1) +
                self._overlayable.str_helper(1) +
                self._members_size.str_helper(1) +
                self._members.str_helper(1) +
                self._type_name.str_helper(1))

    def str_helper(self, n: int):
        return ("\t" * n + "UaDataType:\n" +
                self._type_id.str_helper(n + 1) +
                self._binary_encoding_id.str_helper(n + 1) +
                self._mem_size.str_helper(n + 1) +
                self._type_index.str_helper(n + 1) +
                self._type_kind.str_helper(n + 1) +
                self._pointer_free.str_helper(n + 1) +
                self._overlayable.str_helper(n + 1) +
                self._members_size.str_helper(n + 1) +
                self._members.str_helper(n + 1) +
                self._type_name.str_helper(n + 1))

    def is_numeric(self):
        return lib.UA_DataType_isNumeric(self._value)

    @staticmethod
    def find_by_node_id(type_id: UaNodeId):
        return UaDataType(val=lib.UA_findDataType(type_id._ref()), is_pointer=True)

    # TODO: generic type handling!!!
    # ----> init, copy, new, array_new, array_copy should be methods of a class, which represent members of an in an
    # attribute provided UaDataType
    # returns void ptr
    def new_instance(self):
        return lib.UA_new(self._value)


# +++++++++++++++++++ UaDataTypeArray +++++++++++++++++++++++
class UaDataTypeArray(UaType):
    def __init__(self, val=ffi.new("UA_DataTypeArray*"), is_pointer=False):
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
        return self._types

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
                self._next.str_helper(n + 1) +
                self._types_size.str_helper(n + 1) +
                self._types.str_helper(n + 1))


class Randomize:
    @staticmethod
    def random_uint_32():
        return lib.UA_UInt32_random()

    @staticmethod
    def ua_random_seed(seed: int):
        lib.UA_random_seed(ffi.cast("UA_UInt64*", seed))



