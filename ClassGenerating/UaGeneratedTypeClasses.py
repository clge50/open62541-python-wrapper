from intermediateApi import ffi, lib
# -------------------------------------------------------------
# ------------- Classes from open62541 types.h ----------------
# -------------------------------------------------------------
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




# -------------------------------------------------------------
# --------- Classes from types_generated.h (Enums) ------------
# -------------------------------------------------------------
# These autogenerated classes represent the open62541 enumerated types.
# The attribute val holds a ffi POINTER(!) on a variable with the Type of the corresponding enum.
# So a member of this class represents a variable with type of that enum
# The static attributes are the Python equivalents to the members of the enum.


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
            super().__init__(ffi.new("UA_MessageSecurityMode*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaMessageSecurityMode: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_StructureType*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaStructureType: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_MonitoringMode*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaMonitoringMode: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_BrowseResultMask*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaBrowseResultMask: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_AxisScaleEnumeration*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaAxisScaleEnumeration: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_BrowseDirection*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaBrowseDirection: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_TimestampsToReturn*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaTimestampsToReturn: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_NodeClass*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaNodeClass: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_SecurityTokenRequestType*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaSecurityTokenRequestType: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_ApplicationType*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaApplicationType: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_DeadbandType*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaDeadbandType: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_DataChangeTrigger*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaDataChangeTrigger: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_UserTokenType*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaUserTokenType: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_NodeAttributesMask*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaNodeAttributesMask: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_ServerState*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaServerState: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_FilterOperator*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaFilterOperator: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)


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
            super().__init__(ffi.new("UA_RedundancySupport*", val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaRedundancySupport: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)



# -------------------------------------------------------------
# -------- Classes from types_generated.h (Structs) -----------
# -------------------------------------------------------------
# These autogenerated classes represent the open62541 structured types.
# The attribute val holds a ffi POINTER(!) on a a variable with the Type of the corresponding struct.
# The other attributes are the Python equivalents to the attributes of the c struct.


# +++++++++++++++++++ UaViewAttributes +++++++++++++++++++++++
class UaViewAttributes(UaType):
    def __init__(self, val=ffi.new("UA_ViewAttributes*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._specified_attributes = UaUInt32(val=val.specifiedAttributes)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._write_mask = UaUInt32(val=val.writeMask)
        self._user_write_mask = UaUInt32(val=val.userWriteMask)
        self._contains_no_loops = UaBoolean(val=val.containsNoLoops)
        self._event_notifier = UaByte(val=val.eventNotifier)
    

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def write_mask(self):
        return self._write_mask

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val.value

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val.value

    @property
    def contains_no_loops(self):
        return self._contains_no_loops

    @contains_no_loops.setter
    def contains_no_loops(self, val):
        self._contains_no_loops = val
        self._value.containsNoLoops = val.value

    @property
    def event_notifier(self):
        return self._event_notifier

    @event_notifier.setter
    def event_notifier(self, val):
        self._event_notifier = val
        self._value.eventNotifier = val.value

    def __str__(self):
        return ("UaViewAttributes:\n" + 
                self._specified_attributes.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._write_mask.str_helper(1) +
                self._user_write_mask.str_helper(1) +
                self._contains_no_loops.str_helper(1) +
                self._event_notifier.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaViewAttributes:\n" + 
                self._specified_attributes.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._write_mask.str_helper(n+1) +
                self._user_write_mask.str_helper(n+1) +
                self._contains_no_loops.str_helper(n+1) +
                self._event_notifier.str_helper(n+1))


# +++++++++++++++++++ UaXVType +++++++++++++++++++++++
class UaXVType(UaType):
    def __init__(self, val=ffi.new("UA_XVType*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._x = UaDouble(val=val.x)
        self._value = UaFloat(val=val.value)
    

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val
        self._value.x = val.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val.value

    def __str__(self):
        return ("UaXVType:\n" + 
                self._x.str_helper(1) +
                self._value.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaXVType:\n" + 
                self._x.str_helper(n+1) +
                self._value.str_helper(n+1))


# +++++++++++++++++++ UaElementOperand +++++++++++++++++++++++
class UaElementOperand(UaType):
    def __init__(self, val=ffi.new("UA_ElementOperand*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._index = UaUInt32(val=val.index)
    

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val
        self._value.index = val.value

    def __str__(self):
        return ("UaElementOperand:\n" + 
                self._index.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaElementOperand:\n" + 
                self._index.str_helper(n+1))


# +++++++++++++++++++ UaVariableAttributes +++++++++++++++++++++++
class UaVariableAttributes(UaType):
    def __init__(self, val=ffi.new("UA_VariableAttributes*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._specified_attributes = UaUInt32(val=val.specifiedAttributes)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._write_mask = UaUInt32(val=val.writeMask)
        self._user_write_mask = UaUInt32(val=val.userWriteMask)
        self._value = UaVariant(val=val.value)
        self._data_type = UaNodeId(val=val.dataType)
        self._value_rank = UaInt32(val=val.valueRank)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
        self._access_level = UaByte(val=val.accessLevel)
        self._user_access_level = UaByte(val=val.userAccessLevel)
        self._minimum_sampling_interval = UaDouble(val=val.minimumSamplingInterval)
        self._historizing = UaBoolean(val=val.historizing)
    

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def write_mask(self):
        return self._write_mask

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val.value

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val.value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, val):
        self._data_type = val
        self._value.dataType = val.value

    @property
    def value_rank(self):
        return self._value_rank

    @value_rank.setter
    def value_rank(self, val):
        self._value_rank = val
        self._value.valueRank = val.value

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

    @property
    def access_level(self):
        return self._access_level

    @access_level.setter
    def access_level(self, val):
        self._access_level = val
        self._value.accessLevel = val.value

    @property
    def user_access_level(self):
        return self._user_access_level

    @user_access_level.setter
    def user_access_level(self, val):
        self._user_access_level = val
        self._value.userAccessLevel = val.value

    @property
    def minimum_sampling_interval(self):
        return self._minimum_sampling_interval

    @minimum_sampling_interval.setter
    def minimum_sampling_interval(self, val):
        self._minimum_sampling_interval = val
        self._value.minimumSamplingInterval = val.value

    @property
    def historizing(self):
        return self._historizing

    @historizing.setter
    def historizing(self, val):
        self._historizing = val
        self._value.historizing = val.value

    def __str__(self):
        return ("UaVariableAttributes:\n" + 
                self._specified_attributes.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._write_mask.str_helper(1) +
                self._user_write_mask.str_helper(1) +
                self._value.str_helper(1) +
                self._data_type.str_helper(1) +
                self._value_rank.str_helper(1) +
                self._array_dimensions_size.str_helper(1) +
                self._array_dimensions.str_helper(1) +
                self._access_level.str_helper(1) +
                self._user_access_level.str_helper(1) +
                self._minimum_sampling_interval.str_helper(1) +
                self._historizing.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaVariableAttributes:\n" + 
                self._specified_attributes.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._write_mask.str_helper(n+1) +
                self._user_write_mask.str_helper(n+1) +
                self._value.str_helper(n+1) +
                self._data_type.str_helper(n+1) +
                self._value_rank.str_helper(n+1) +
                self._array_dimensions_size.str_helper(n+1) +
                self._array_dimensions.str_helper(n+1) +
                self._access_level.str_helper(n+1) +
                self._user_access_level.str_helper(n+1) +
                self._minimum_sampling_interval.str_helper(n+1) +
                self._historizing.str_helper(n+1))


# +++++++++++++++++++ UaEnumValueType +++++++++++++++++++++++
class UaEnumValueType(UaType):
    def __init__(self, val=ffi.new("UA_EnumValueType*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._value = UaInt64(val=val.value)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
    

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    def __str__(self):
        return ("UaEnumValueType:\n" + 
                self._value.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaEnumValueType:\n" + 
                self._value.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1))


# +++++++++++++++++++ UaEventFieldList +++++++++++++++++++++++
class UaEventFieldList(UaType):
    def __init__(self, val=ffi.new("UA_EventFieldList*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._client_handle = UaUInt32(val=val.clientHandle)
        self._event_fields_size = SizeT(val=val.eventFieldsSize)
        self._event_fields = UaVariant(val=val.eventFields, is_pointer=True)
    

    @property
    def client_handle(self):
        return self._client_handle

    @client_handle.setter
    def client_handle(self, val):
        self._client_handle = val
        self._value.clientHandle = val.value

    @property
    def event_fields_size(self):
        return self._event_fields_size

    @event_fields_size.setter
    def event_fields_size(self, val):
        self._event_fields_size = val
        self._value.eventFieldsSize = val.value

    @property
    def event_fields(self):
        return self._event_fields

    @event_fields.setter
    def event_fields(self, val):
        self._event_fields = val
        self._value.eventFields = val.value

    def __str__(self):
        return ("UaEventFieldList:\n" + 
                self._client_handle.str_helper(1) +
                self._event_fields_size.str_helper(1) +
                self._event_fields.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaEventFieldList:\n" + 
                self._client_handle.str_helper(n+1) +
                self._event_fields_size.str_helper(n+1) +
                self._event_fields.str_helper(n+1))


# +++++++++++++++++++ UaMonitoredItemCreateResult +++++++++++++++++++++++
class UaMonitoredItemCreateResult(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemCreateResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._status_code = UaStatusCode(val=val.statusCode)
        self._monitored_item_id = UaUInt32(val=val.monitoredItemId)
        self._revised_sampling_interval = UaDouble(val=val.revisedSamplingInterval)
        self._revised_queue_size = UaUInt32(val=val.revisedQueueSize)
        self._filter_result = UaExtensionObject(val=val.filterResult)
    

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val.value

    @property
    def monitored_item_id(self):
        return self._monitored_item_id

    @monitored_item_id.setter
    def monitored_item_id(self, val):
        self._monitored_item_id = val
        self._value.monitoredItemId = val.value

    @property
    def revised_sampling_interval(self):
        return self._revised_sampling_interval

    @revised_sampling_interval.setter
    def revised_sampling_interval(self, val):
        self._revised_sampling_interval = val
        self._value.revisedSamplingInterval = val.value

    @property
    def revised_queue_size(self):
        return self._revised_queue_size

    @revised_queue_size.setter
    def revised_queue_size(self, val):
        self._revised_queue_size = val
        self._value.revisedQueueSize = val.value

    @property
    def filter_result(self):
        return self._filter_result

    @filter_result.setter
    def filter_result(self, val):
        self._filter_result = val
        self._value.filterResult = val.value

    def __str__(self):
        return ("UaMonitoredItemCreateResult:\n" + 
                self._status_code.str_helper(1) +
                self._monitored_item_id.str_helper(1) +
                self._revised_sampling_interval.str_helper(1) +
                self._revised_queue_size.str_helper(1) +
                self._filter_result.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaMonitoredItemCreateResult:\n" + 
                self._status_code.str_helper(n+1) +
                self._monitored_item_id.str_helper(n+1) +
                self._revised_sampling_interval.str_helper(n+1) +
                self._revised_queue_size.str_helper(n+1) +
                self._filter_result.str_helper(n+1))


# +++++++++++++++++++ UaEUInformation +++++++++++++++++++++++
class UaEUInformation(UaType):
    def __init__(self, val=ffi.new("UA_EUInformation*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._namespace_uri = UaString(val=val.namespaceUri)
        self._unit_id = UaInt32(val=val.unitId)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
    

    @property
    def namespace_uri(self):
        return self._namespace_uri

    @namespace_uri.setter
    def namespace_uri(self, val):
        self._namespace_uri = val
        self._value.namespaceUri = val.value

    @property
    def unit_id(self):
        return self._unit_id

    @unit_id.setter
    def unit_id(self, val):
        self._unit_id = val
        self._value.unitId = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    def __str__(self):
        return ("UaEUInformation:\n" + 
                self._namespace_uri.str_helper(1) +
                self._unit_id.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaEUInformation:\n" + 
                self._namespace_uri.str_helper(n+1) +
                self._unit_id.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1))


# +++++++++++++++++++ UaServerDiagnosticsSummaryDataType +++++++++++++++++++++++
class UaServerDiagnosticsSummaryDataType(UaType):
    def __init__(self, val=ffi.new("UA_ServerDiagnosticsSummaryDataType*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._server_view_count = UaUInt32(val=val.serverViewCount)
        self._current_session_count = UaUInt32(val=val.currentSessionCount)
        self._cumulated_session_count = UaUInt32(val=val.cumulatedSessionCount)
        self._security_rejected_session_count = UaUInt32(val=val.securityRejectedSessionCount)
        self._rejected_session_count = UaUInt32(val=val.rejectedSessionCount)
        self._session_timeout_count = UaUInt32(val=val.sessionTimeoutCount)
        self._session_abort_count = UaUInt32(val=val.sessionAbortCount)
        self._current_subscription_count = UaUInt32(val=val.currentSubscriptionCount)
        self._cumulated_subscription_count = UaUInt32(val=val.cumulatedSubscriptionCount)
        self._publishing_interval_count = UaUInt32(val=val.publishingIntervalCount)
        self._security_rejected_requests_count = UaUInt32(val=val.securityRejectedRequestsCount)
        self._rejected_requests_count = UaUInt32(val=val.rejectedRequestsCount)
    

    @property
    def server_view_count(self):
        return self._server_view_count

    @server_view_count.setter
    def server_view_count(self, val):
        self._server_view_count = val
        self._value.serverViewCount = val.value

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

    @property
    def current_subscription_count(self):
        return self._current_subscription_count

    @current_subscription_count.setter
    def current_subscription_count(self, val):
        self._current_subscription_count = val
        self._value.currentSubscriptionCount = val.value

    @property
    def cumulated_subscription_count(self):
        return self._cumulated_subscription_count

    @cumulated_subscription_count.setter
    def cumulated_subscription_count(self, val):
        self._cumulated_subscription_count = val
        self._value.cumulatedSubscriptionCount = val.value

    @property
    def publishing_interval_count(self):
        return self._publishing_interval_count

    @publishing_interval_count.setter
    def publishing_interval_count(self, val):
        self._publishing_interval_count = val
        self._value.publishingIntervalCount = val.value

    @property
    def security_rejected_requests_count(self):
        return self._security_rejected_requests_count

    @security_rejected_requests_count.setter
    def security_rejected_requests_count(self, val):
        self._security_rejected_requests_count = val
        self._value.securityRejectedRequestsCount = val.value

    @property
    def rejected_requests_count(self):
        return self._rejected_requests_count

    @rejected_requests_count.setter
    def rejected_requests_count(self, val):
        self._rejected_requests_count = val
        self._value.rejectedRequestsCount = val.value

    def __str__(self):
        return ("UaServerDiagnosticsSummaryDataType:\n" + 
                self._server_view_count.str_helper(1) +
                self._current_session_count.str_helper(1) +
                self._cumulated_session_count.str_helper(1) +
                self._security_rejected_session_count.str_helper(1) +
                self._rejected_session_count.str_helper(1) +
                self._session_timeout_count.str_helper(1) +
                self._session_abort_count.str_helper(1) +
                self._current_subscription_count.str_helper(1) +
                self._cumulated_subscription_count.str_helper(1) +
                self._publishing_interval_count.str_helper(1) +
                self._security_rejected_requests_count.str_helper(1) +
                self._rejected_requests_count.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaServerDiagnosticsSummaryDataType:\n" + 
                self._server_view_count.str_helper(n+1) +
                self._current_session_count.str_helper(n+1) +
                self._cumulated_session_count.str_helper(n+1) +
                self._security_rejected_session_count.str_helper(n+1) +
                self._rejected_session_count.str_helper(n+1) +
                self._session_timeout_count.str_helper(n+1) +
                self._session_abort_count.str_helper(n+1) +
                self._current_subscription_count.str_helper(n+1) +
                self._cumulated_subscription_count.str_helper(n+1) +
                self._publishing_interval_count.str_helper(n+1) +
                self._security_rejected_requests_count.str_helper(n+1) +
                self._rejected_requests_count.str_helper(n+1))


# +++++++++++++++++++ UaContentFilterElementResult +++++++++++++++++++++++
class UaContentFilterElementResult(UaType):
    def __init__(self, val=ffi.new("UA_ContentFilterElementResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._status_code = UaStatusCode(val=val.statusCode)
        self._operand_status_codes_size = SizeT(val=val.operandStatusCodesSize)
        self._operand_status_codes = UaStatusCode(val=val.operandStatusCodes, is_pointer=True)
        self._operand_diagnostic_infos_size = SizeT(val=val.operandDiagnosticInfosSize)
        self._operand_diagnostic_infos = UaDiagnosticInfo(val=val.operandDiagnosticInfos, is_pointer=True)
    

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val.value

    @property
    def operand_status_codes_size(self):
        return self._operand_status_codes_size

    @operand_status_codes_size.setter
    def operand_status_codes_size(self, val):
        self._operand_status_codes_size = val
        self._value.operandStatusCodesSize = val.value

    @property
    def operand_status_codes(self):
        return self._operand_status_codes

    @operand_status_codes.setter
    def operand_status_codes(self, val):
        self._operand_status_codes = val
        self._value.operandStatusCodes = val.value

    @property
    def operand_diagnostic_infos_size(self):
        return self._operand_diagnostic_infos_size

    @operand_diagnostic_infos_size.setter
    def operand_diagnostic_infos_size(self, val):
        self._operand_diagnostic_infos_size = val
        self._value.operandDiagnosticInfosSize = val.value

    @property
    def operand_diagnostic_infos(self):
        return self._operand_diagnostic_infos

    @operand_diagnostic_infos.setter
    def operand_diagnostic_infos(self, val):
        self._operand_diagnostic_infos = val
        self._value.operandDiagnosticInfos = val.value

    def __str__(self):
        return ("UaContentFilterElementResult:\n" + 
                self._status_code.str_helper(1) +
                self._operand_status_codes_size.str_helper(1) +
                self._operand_status_codes.str_helper(1) +
                self._operand_diagnostic_infos_size.str_helper(1) +
                self._operand_diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaContentFilterElementResult:\n" + 
                self._status_code.str_helper(n+1) +
                self._operand_status_codes_size.str_helper(n+1) +
                self._operand_status_codes.str_helper(n+1) +
                self._operand_diagnostic_infos_size.str_helper(n+1) +
                self._operand_diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaLiteralOperand +++++++++++++++++++++++
class UaLiteralOperand(UaType):
    def __init__(self, val=ffi.new("UA_LiteralOperand*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._value = UaVariant(val=val.value)
    

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val.value

    def __str__(self):
        return ("UaLiteralOperand:\n" + 
                self._value.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaLiteralOperand:\n" + 
                self._value.str_helper(n+1))


# +++++++++++++++++++ UaUserIdentityToken +++++++++++++++++++++++
class UaUserIdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_UserIdentityToken*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._policy_id = UaString(val=val.policyId)
    

    @property
    def policy_id(self):
        return self._policy_id

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val.value

    def __str__(self):
        return ("UaUserIdentityToken:\n" + 
                self._policy_id.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaUserIdentityToken:\n" + 
                self._policy_id.str_helper(n+1))


# +++++++++++++++++++ UaX509IdentityToken +++++++++++++++++++++++
class UaX509IdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_X509IdentityToken*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._policy_id = UaString(val=val.policyId)
        self._certificate_data = UaByteString(val=val.certificateData)
    

    @property
    def policy_id(self):
        return self._policy_id

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val.value

    @property
    def certificate_data(self):
        return self._certificate_data

    @certificate_data.setter
    def certificate_data(self, val):
        self._certificate_data = val
        self._value.certificateData = val.value

    def __str__(self):
        return ("UaX509IdentityToken:\n" + 
                self._policy_id.str_helper(1) +
                self._certificate_data.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaX509IdentityToken:\n" + 
                self._policy_id.str_helper(n+1) +
                self._certificate_data.str_helper(n+1))


# +++++++++++++++++++ UaMonitoredItemNotification +++++++++++++++++++++++
class UaMonitoredItemNotification(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemNotification*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._client_handle = UaUInt32(val=val.clientHandle)
        self._value = UaDataValue(val=val.value)
    

    @property
    def client_handle(self):
        return self._client_handle

    @client_handle.setter
    def client_handle(self, val):
        self._client_handle = val
        self._value.clientHandle = val.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val.value

    def __str__(self):
        return ("UaMonitoredItemNotification:\n" + 
                self._client_handle.str_helper(1) +
                self._value.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaMonitoredItemNotification:\n" + 
                self._client_handle.str_helper(n+1) +
                self._value.str_helper(n+1))


# +++++++++++++++++++ UaResponseHeader +++++++++++++++++++++++
class UaResponseHeader(UaType):
    def __init__(self, val=ffi.new("UA_ResponseHeader*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._timestamp = UaDateTime(val=val.timestamp)
        self._request_handle = UaUInt32(val=val.requestHandle)
        self._service_result = UaStatusCode(val=val.serviceResult)
        self._service_diagnostics = UaDiagnosticInfo(val=val.serviceDiagnostics)
        self._string_table_size = SizeT(val=val.stringTableSize)
        self._string_table = UaString(val=val.stringTable, is_pointer=True)
        self._additional_header = UaExtensionObject(val=val.additionalHeader)
    

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, val):
        self._timestamp = val
        self._value.timestamp = val.value

    @property
    def request_handle(self):
        return self._request_handle

    @request_handle.setter
    def request_handle(self, val):
        self._request_handle = val
        self._value.requestHandle = val.value

    @property
    def service_result(self):
        return self._service_result

    @service_result.setter
    def service_result(self, val):
        self._service_result = val
        self._value.serviceResult = val.value

    @property
    def service_diagnostics(self):
        return self._service_diagnostics

    @service_diagnostics.setter
    def service_diagnostics(self, val):
        self._service_diagnostics = val
        self._value.serviceDiagnostics = val.value

    @property
    def string_table_size(self):
        return self._string_table_size

    @string_table_size.setter
    def string_table_size(self, val):
        self._string_table_size = val
        self._value.stringTableSize = val.value

    @property
    def string_table(self):
        return self._string_table

    @string_table.setter
    def string_table(self, val):
        self._string_table = val
        self._value.stringTable = val.value

    @property
    def additional_header(self):
        return self._additional_header

    @additional_header.setter
    def additional_header(self, val):
        self._additional_header = val
        self._value.additionalHeader = val.value

    def __str__(self):
        return ("UaResponseHeader:\n" + 
                self._timestamp.str_helper(1) +
                self._request_handle.str_helper(1) +
                self._service_result.str_helper(1) +
                self._service_diagnostics.str_helper(1) +
                self._string_table_size.str_helper(1) +
                self._string_table.str_helper(1) +
                self._additional_header.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaResponseHeader:\n" + 
                self._timestamp.str_helper(n+1) +
                self._request_handle.str_helper(n+1) +
                self._service_result.str_helper(n+1) +
                self._service_diagnostics.str_helper(n+1) +
                self._string_table_size.str_helper(n+1) +
                self._string_table.str_helper(n+1) +
                self._additional_header.str_helper(n+1))


# +++++++++++++++++++ UaSignatureData +++++++++++++++++++++++
class UaSignatureData(UaType):
    def __init__(self, val=ffi.new("UA_SignatureData*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._algorithm = UaString(val=val.algorithm)
        self._signature = UaByteString(val=val.signature)
    

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, val):
        self._algorithm = val
        self._value.algorithm = val.value

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, val):
        self._signature = val
        self._value.signature = val.value

    def __str__(self):
        return ("UaSignatureData:\n" + 
                self._algorithm.str_helper(1) +
                self._signature.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSignatureData:\n" + 
                self._algorithm.str_helper(n+1) +
                self._signature.str_helper(n+1))


# +++++++++++++++++++ UaModifySubscriptionResponse +++++++++++++++++++++++
class UaModifySubscriptionResponse(UaType):
    def __init__(self, val=ffi.new("UA_ModifySubscriptionResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._revised_publishing_interval = UaDouble(val=val.revisedPublishingInterval)
        self._revised_lifetime_count = UaUInt32(val=val.revisedLifetimeCount)
        self._revised_max_keep_alive_count = UaUInt32(val=val.revisedMaxKeepAliveCount)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def revised_publishing_interval(self):
        return self._revised_publishing_interval

    @revised_publishing_interval.setter
    def revised_publishing_interval(self, val):
        self._revised_publishing_interval = val
        self._value.revisedPublishingInterval = val.value

    @property
    def revised_lifetime_count(self):
        return self._revised_lifetime_count

    @revised_lifetime_count.setter
    def revised_lifetime_count(self, val):
        self._revised_lifetime_count = val
        self._value.revisedLifetimeCount = val.value

    @property
    def revised_max_keep_alive_count(self):
        return self._revised_max_keep_alive_count

    @revised_max_keep_alive_count.setter
    def revised_max_keep_alive_count(self, val):
        self._revised_max_keep_alive_count = val
        self._value.revisedMaxKeepAliveCount = val.value

    def __str__(self):
        return ("UaModifySubscriptionResponse:\n" + 
                self._response_header.str_helper(1) +
                self._revised_publishing_interval.str_helper(1) +
                self._revised_lifetime_count.str_helper(1) +
                self._revised_max_keep_alive_count.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaModifySubscriptionResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._revised_publishing_interval.str_helper(n+1) +
                self._revised_lifetime_count.str_helper(n+1) +
                self._revised_max_keep_alive_count.str_helper(n+1))


# +++++++++++++++++++ UaNodeAttributes +++++++++++++++++++++++
class UaNodeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_NodeAttributes*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._specified_attributes = UaUInt32(val=val.specifiedAttributes)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._write_mask = UaUInt32(val=val.writeMask)
        self._user_write_mask = UaUInt32(val=val.userWriteMask)
    

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def write_mask(self):
        return self._write_mask

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val.value

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val.value

    def __str__(self):
        return ("UaNodeAttributes:\n" + 
                self._specified_attributes.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._write_mask.str_helper(1) +
                self._user_write_mask.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaNodeAttributes:\n" + 
                self._specified_attributes.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._write_mask.str_helper(n+1) +
                self._user_write_mask.str_helper(n+1))


# +++++++++++++++++++ UaActivateSessionResponse +++++++++++++++++++++++
class UaActivateSessionResponse(UaType):
    def __init__(self, val=ffi.new("UA_ActivateSessionResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._server_nonce = UaByteString(val=val.serverNonce)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def server_nonce(self):
        return self._server_nonce

    @server_nonce.setter
    def server_nonce(self, val):
        self._server_nonce = val
        self._value.serverNonce = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaActivateSessionResponse:\n" + 
                self._response_header.str_helper(1) +
                self._server_nonce.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaActivateSessionResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._server_nonce.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaEnumField +++++++++++++++++++++++
class UaEnumField(UaType):
    def __init__(self, val=ffi.new("UA_EnumField*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._value = UaInt64(val=val.value)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._name = UaString(val=val.name)
    

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val
        self._value.name = val.value

    def __str__(self):
        return ("UaEnumField:\n" + 
                self._value.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._name.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaEnumField:\n" + 
                self._value.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._name.str_helper(n+1))


# +++++++++++++++++++ UaVariableTypeAttributes +++++++++++++++++++++++
class UaVariableTypeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_VariableTypeAttributes*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._specified_attributes = UaUInt32(val=val.specifiedAttributes)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._write_mask = UaUInt32(val=val.writeMask)
        self._user_write_mask = UaUInt32(val=val.userWriteMask)
        self._value = UaVariant(val=val.value)
        self._data_type = UaNodeId(val=val.dataType)
        self._value_rank = UaInt32(val=val.valueRank)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
        self._is_abstract = UaBoolean(val=val.isAbstract)
    

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def write_mask(self):
        return self._write_mask

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val.value

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val.value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, val):
        self._data_type = val
        self._value.dataType = val.value

    @property
    def value_rank(self):
        return self._value_rank

    @value_rank.setter
    def value_rank(self, val):
        self._value_rank = val
        self._value.valueRank = val.value

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

    @property
    def is_abstract(self):
        return self._is_abstract

    @is_abstract.setter
    def is_abstract(self, val):
        self._is_abstract = val
        self._value.isAbstract = val.value

    def __str__(self):
        return ("UaVariableTypeAttributes:\n" + 
                self._specified_attributes.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._write_mask.str_helper(1) +
                self._user_write_mask.str_helper(1) +
                self._value.str_helper(1) +
                self._data_type.str_helper(1) +
                self._value_rank.str_helper(1) +
                self._array_dimensions_size.str_helper(1) +
                self._array_dimensions.str_helper(1) +
                self._is_abstract.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaVariableTypeAttributes:\n" + 
                self._specified_attributes.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._write_mask.str_helper(n+1) +
                self._user_write_mask.str_helper(n+1) +
                self._value.str_helper(n+1) +
                self._data_type.str_helper(n+1) +
                self._value_rank.str_helper(n+1) +
                self._array_dimensions_size.str_helper(n+1) +
                self._array_dimensions.str_helper(n+1) +
                self._is_abstract.str_helper(n+1))


# +++++++++++++++++++ UaCallMethodResult +++++++++++++++++++++++
class UaCallMethodResult(UaType):
    def __init__(self, val=ffi.new("UA_CallMethodResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._status_code = UaStatusCode(val=val.statusCode)
        self._input_argument_results_size = SizeT(val=val.inputArgumentResultsSize)
        self._input_argument_results = UaStatusCode(val=val.inputArgumentResults, is_pointer=True)
        self._input_argument_diagnostic_infos_size = SizeT(val=val.inputArgumentDiagnosticInfosSize)
        self._input_argument_diagnostic_infos = UaDiagnosticInfo(val=val.inputArgumentDiagnosticInfos, is_pointer=True)
        self._output_arguments_size = SizeT(val=val.outputArgumentsSize)
        self._output_arguments = UaVariant(val=val.outputArguments, is_pointer=True)
    

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val.value

    @property
    def input_argument_results_size(self):
        return self._input_argument_results_size

    @input_argument_results_size.setter
    def input_argument_results_size(self, val):
        self._input_argument_results_size = val
        self._value.inputArgumentResultsSize = val.value

    @property
    def input_argument_results(self):
        return self._input_argument_results

    @input_argument_results.setter
    def input_argument_results(self, val):
        self._input_argument_results = val
        self._value.inputArgumentResults = val.value

    @property
    def input_argument_diagnostic_infos_size(self):
        return self._input_argument_diagnostic_infos_size

    @input_argument_diagnostic_infos_size.setter
    def input_argument_diagnostic_infos_size(self, val):
        self._input_argument_diagnostic_infos_size = val
        self._value.inputArgumentDiagnosticInfosSize = val.value

    @property
    def input_argument_diagnostic_infos(self):
        return self._input_argument_diagnostic_infos

    @input_argument_diagnostic_infos.setter
    def input_argument_diagnostic_infos(self, val):
        self._input_argument_diagnostic_infos = val
        self._value.inputArgumentDiagnosticInfos = val.value

    @property
    def output_arguments_size(self):
        return self._output_arguments_size

    @output_arguments_size.setter
    def output_arguments_size(self, val):
        self._output_arguments_size = val
        self._value.outputArgumentsSize = val.value

    @property
    def output_arguments(self):
        return self._output_arguments

    @output_arguments.setter
    def output_arguments(self, val):
        self._output_arguments = val
        self._value.outputArguments = val.value

    def __str__(self):
        return ("UaCallMethodResult:\n" + 
                self._status_code.str_helper(1) +
                self._input_argument_results_size.str_helper(1) +
                self._input_argument_results.str_helper(1) +
                self._input_argument_diagnostic_infos_size.str_helper(1) +
                self._input_argument_diagnostic_infos.str_helper(1) +
                self._output_arguments_size.str_helper(1) +
                self._output_arguments.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCallMethodResult:\n" + 
                self._status_code.str_helper(n+1) +
                self._input_argument_results_size.str_helper(n+1) +
                self._input_argument_results.str_helper(n+1) +
                self._input_argument_diagnostic_infos_size.str_helper(n+1) +
                self._input_argument_diagnostic_infos.str_helper(n+1) +
                self._output_arguments_size.str_helper(n+1) +
                self._output_arguments.str_helper(n+1))


# +++++++++++++++++++ UaSetMonitoringModeResponse +++++++++++++++++++++++
class UaSetMonitoringModeResponse(UaType):
    def __init__(self, val=ffi.new("UA_SetMonitoringModeResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaSetMonitoringModeResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSetMonitoringModeResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaRequestHeader +++++++++++++++++++++++
class UaRequestHeader(UaType):
    def __init__(self, val=ffi.new("UA_RequestHeader*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._authentication_token = UaNodeId(val=val.authenticationToken)
        self._timestamp = UaDateTime(val=val.timestamp)
        self._request_handle = UaUInt32(val=val.requestHandle)
        self._return_diagnostics = UaUInt32(val=val.returnDiagnostics)
        self._audit_entry_id = UaString(val=val.auditEntryId)
        self._timeout_hint = UaUInt32(val=val.timeoutHint)
        self._additional_header = UaExtensionObject(val=val.additionalHeader)
    

    @property
    def authentication_token(self):
        return self._authentication_token

    @authentication_token.setter
    def authentication_token(self, val):
        self._authentication_token = val
        self._value.authenticationToken = val.value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, val):
        self._timestamp = val
        self._value.timestamp = val.value

    @property
    def request_handle(self):
        return self._request_handle

    @request_handle.setter
    def request_handle(self, val):
        self._request_handle = val
        self._value.requestHandle = val.value

    @property
    def return_diagnostics(self):
        return self._return_diagnostics

    @return_diagnostics.setter
    def return_diagnostics(self, val):
        self._return_diagnostics = val
        self._value.returnDiagnostics = val.value

    @property
    def audit_entry_id(self):
        return self._audit_entry_id

    @audit_entry_id.setter
    def audit_entry_id(self, val):
        self._audit_entry_id = val
        self._value.auditEntryId = val.value

    @property
    def timeout_hint(self):
        return self._timeout_hint

    @timeout_hint.setter
    def timeout_hint(self, val):
        self._timeout_hint = val
        self._value.timeoutHint = val.value

    @property
    def additional_header(self):
        return self._additional_header

    @additional_header.setter
    def additional_header(self, val):
        self._additional_header = val
        self._value.additionalHeader = val.value

    def __str__(self):
        return ("UaRequestHeader:\n" + 
                self._authentication_token.str_helper(1) +
                self._timestamp.str_helper(1) +
                self._request_handle.str_helper(1) +
                self._return_diagnostics.str_helper(1) +
                self._audit_entry_id.str_helper(1) +
                self._timeout_hint.str_helper(1) +
                self._additional_header.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaRequestHeader:\n" + 
                self._authentication_token.str_helper(n+1) +
                self._timestamp.str_helper(n+1) +
                self._request_handle.str_helper(n+1) +
                self._return_diagnostics.str_helper(n+1) +
                self._audit_entry_id.str_helper(n+1) +
                self._timeout_hint.str_helper(n+1) +
                self._additional_header.str_helper(n+1))


# +++++++++++++++++++ UaMonitoredItemModifyResult +++++++++++++++++++++++
class UaMonitoredItemModifyResult(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemModifyResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._status_code = UaStatusCode(val=val.statusCode)
        self._revised_sampling_interval = UaDouble(val=val.revisedSamplingInterval)
        self._revised_queue_size = UaUInt32(val=val.revisedQueueSize)
        self._filter_result = UaExtensionObject(val=val.filterResult)
    

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val.value

    @property
    def revised_sampling_interval(self):
        return self._revised_sampling_interval

    @revised_sampling_interval.setter
    def revised_sampling_interval(self, val):
        self._revised_sampling_interval = val
        self._value.revisedSamplingInterval = val.value

    @property
    def revised_queue_size(self):
        return self._revised_queue_size

    @revised_queue_size.setter
    def revised_queue_size(self, val):
        self._revised_queue_size = val
        self._value.revisedQueueSize = val.value

    @property
    def filter_result(self):
        return self._filter_result

    @filter_result.setter
    def filter_result(self, val):
        self._filter_result = val
        self._value.filterResult = val.value

    def __str__(self):
        return ("UaMonitoredItemModifyResult:\n" + 
                self._status_code.str_helper(1) +
                self._revised_sampling_interval.str_helper(1) +
                self._revised_queue_size.str_helper(1) +
                self._filter_result.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaMonitoredItemModifyResult:\n" + 
                self._status_code.str_helper(n+1) +
                self._revised_sampling_interval.str_helper(n+1) +
                self._revised_queue_size.str_helper(n+1) +
                self._filter_result.str_helper(n+1))


# +++++++++++++++++++ UaCloseSecureChannelRequest +++++++++++++++++++++++
class UaCloseSecureChannelRequest(UaType):
    def __init__(self, val=ffi.new("UA_CloseSecureChannelRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    def __str__(self):
        return ("UaCloseSecureChannelRequest:\n" + 
                self._request_header.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCloseSecureChannelRequest:\n" + 
                self._request_header.str_helper(n+1))


# +++++++++++++++++++ UaNotificationMessage +++++++++++++++++++++++
class UaNotificationMessage(UaType):
    def __init__(self, val=ffi.new("UA_NotificationMessage*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._sequence_number = UaUInt32(val=val.sequenceNumber)
        self._publish_time = UaDateTime(val=val.publishTime)
        self._notification_data_size = SizeT(val=val.notificationDataSize)
        self._notification_data = UaExtensionObject(val=val.notificationData, is_pointer=True)
    

    @property
    def sequence_number(self):
        return self._sequence_number

    @sequence_number.setter
    def sequence_number(self, val):
        self._sequence_number = val
        self._value.sequenceNumber = val.value

    @property
    def publish_time(self):
        return self._publish_time

    @publish_time.setter
    def publish_time(self, val):
        self._publish_time = val
        self._value.publishTime = val.value

    @property
    def notification_data_size(self):
        return self._notification_data_size

    @notification_data_size.setter
    def notification_data_size(self, val):
        self._notification_data_size = val
        self._value.notificationDataSize = val.value

    @property
    def notification_data(self):
        return self._notification_data

    @notification_data.setter
    def notification_data(self, val):
        self._notification_data = val
        self._value.notificationData = val.value

    def __str__(self):
        return ("UaNotificationMessage:\n" + 
                self._sequence_number.str_helper(1) +
                self._publish_time.str_helper(1) +
                self._notification_data_size.str_helper(1) +
                self._notification_data.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaNotificationMessage:\n" + 
                self._sequence_number.str_helper(n+1) +
                self._publish_time.str_helper(n+1) +
                self._notification_data_size.str_helper(n+1) +
                self._notification_data.str_helper(n+1))


# +++++++++++++++++++ UaCreateSubscriptionResponse +++++++++++++++++++++++
class UaCreateSubscriptionResponse(UaType):
    def __init__(self, val=ffi.new("UA_CreateSubscriptionResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._revised_publishing_interval = UaDouble(val=val.revisedPublishingInterval)
        self._revised_lifetime_count = UaUInt32(val=val.revisedLifetimeCount)
        self._revised_max_keep_alive_count = UaUInt32(val=val.revisedMaxKeepAliveCount)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def revised_publishing_interval(self):
        return self._revised_publishing_interval

    @revised_publishing_interval.setter
    def revised_publishing_interval(self, val):
        self._revised_publishing_interval = val
        self._value.revisedPublishingInterval = val.value

    @property
    def revised_lifetime_count(self):
        return self._revised_lifetime_count

    @revised_lifetime_count.setter
    def revised_lifetime_count(self, val):
        self._revised_lifetime_count = val
        self._value.revisedLifetimeCount = val.value

    @property
    def revised_max_keep_alive_count(self):
        return self._revised_max_keep_alive_count

    @revised_max_keep_alive_count.setter
    def revised_max_keep_alive_count(self, val):
        self._revised_max_keep_alive_count = val
        self._value.revisedMaxKeepAliveCount = val.value

    def __str__(self):
        return ("UaCreateSubscriptionResponse:\n" + 
                self._response_header.str_helper(1) +
                self._subscription_id.str_helper(1) +
                self._revised_publishing_interval.str_helper(1) +
                self._revised_lifetime_count.str_helper(1) +
                self._revised_max_keep_alive_count.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCreateSubscriptionResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._subscription_id.str_helper(n+1) +
                self._revised_publishing_interval.str_helper(n+1) +
                self._revised_lifetime_count.str_helper(n+1) +
                self._revised_max_keep_alive_count.str_helper(n+1))


# +++++++++++++++++++ UaEnumDefinition +++++++++++++++++++++++
class UaEnumDefinition(UaType):
    def __init__(self, val=ffi.new("UA_EnumDefinition*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._fields_size = SizeT(val=val.fieldsSize)
        self._fields = UaEnumField(val=val.fields, is_pointer=True)
    

    @property
    def fields_size(self):
        return self._fields_size

    @fields_size.setter
    def fields_size(self, val):
        self._fields_size = val
        self._value.fieldsSize = val.value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, val):
        self._fields = val
        self._value.fields = val.value

    def __str__(self):
        return ("UaEnumDefinition:\n" + 
                self._fields_size.str_helper(1) +
                self._fields.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaEnumDefinition:\n" + 
                self._fields_size.str_helper(n+1) +
                self._fields.str_helper(n+1))


# +++++++++++++++++++ UaCallMethodRequest +++++++++++++++++++++++
class UaCallMethodRequest(UaType):
    def __init__(self, val=ffi.new("UA_CallMethodRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._object_id = UaNodeId(val=val.objectId)
        self._method_id = UaNodeId(val=val.methodId)
        self._input_arguments_size = SizeT(val=val.inputArgumentsSize)
        self._input_arguments = UaVariant(val=val.inputArguments, is_pointer=True)
    

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, val):
        self._object_id = val
        self._value.objectId = val.value

    @property
    def method_id(self):
        return self._method_id

    @method_id.setter
    def method_id(self, val):
        self._method_id = val
        self._value.methodId = val.value

    @property
    def input_arguments_size(self):
        return self._input_arguments_size

    @input_arguments_size.setter
    def input_arguments_size(self, val):
        self._input_arguments_size = val
        self._value.inputArgumentsSize = val.value

    @property
    def input_arguments(self):
        return self._input_arguments

    @input_arguments.setter
    def input_arguments(self, val):
        self._input_arguments = val
        self._value.inputArguments = val.value

    def __str__(self):
        return ("UaCallMethodRequest:\n" + 
                self._object_id.str_helper(1) +
                self._method_id.str_helper(1) +
                self._input_arguments_size.str_helper(1) +
                self._input_arguments.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCallMethodRequest:\n" + 
                self._object_id.str_helper(n+1) +
                self._method_id.str_helper(n+1) +
                self._input_arguments_size.str_helper(n+1) +
                self._input_arguments.str_helper(n+1))


# +++++++++++++++++++ UaReadResponse +++++++++++++++++++++++
class UaReadResponse(UaType):
    def __init__(self, val=ffi.new("UA_ReadResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaDataValue(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaReadResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaReadResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaObjectTypeAttributes +++++++++++++++++++++++
class UaObjectTypeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_ObjectTypeAttributes*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._specified_attributes = UaUInt32(val=val.specifiedAttributes)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._write_mask = UaUInt32(val=val.writeMask)
        self._user_write_mask = UaUInt32(val=val.userWriteMask)
        self._is_abstract = UaBoolean(val=val.isAbstract)
    

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def write_mask(self):
        return self._write_mask

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val.value

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val.value

    @property
    def is_abstract(self):
        return self._is_abstract

    @is_abstract.setter
    def is_abstract(self, val):
        self._is_abstract = val
        self._value.isAbstract = val.value

    def __str__(self):
        return ("UaObjectTypeAttributes:\n" + 
                self._specified_attributes.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._write_mask.str_helper(1) +
                self._user_write_mask.str_helper(1) +
                self._is_abstract.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaObjectTypeAttributes:\n" + 
                self._specified_attributes.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._write_mask.str_helper(n+1) +
                self._user_write_mask.str_helper(n+1) +
                self._is_abstract.str_helper(n+1))


# +++++++++++++++++++ UaCloseSessionResponse +++++++++++++++++++++++
class UaCloseSessionResponse(UaType):
    def __init__(self, val=ffi.new("UA_CloseSessionResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    def __str__(self):
        return ("UaCloseSessionResponse:\n" + 
                self._response_header.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCloseSessionResponse:\n" + 
                self._response_header.str_helper(n+1))


# +++++++++++++++++++ UaSetPublishingModeRequest +++++++++++++++++++++++
class UaSetPublishingModeRequest(UaType):
    def __init__(self, val=ffi.new("UA_SetPublishingModeRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._publishing_enabled = UaBoolean(val=val.publishingEnabled)
        self._subscription_ids_size = SizeT(val=val.subscriptionIdsSize)
        self._subscription_ids = UaUInt32(val=val.subscriptionIds, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def publishing_enabled(self):
        return self._publishing_enabled

    @publishing_enabled.setter
    def publishing_enabled(self, val):
        self._publishing_enabled = val
        self._value.publishingEnabled = val.value

    @property
    def subscription_ids_size(self):
        return self._subscription_ids_size

    @subscription_ids_size.setter
    def subscription_ids_size(self, val):
        self._subscription_ids_size = val
        self._value.subscriptionIdsSize = val.value

    @property
    def subscription_ids(self):
        return self._subscription_ids

    @subscription_ids.setter
    def subscription_ids(self, val):
        self._subscription_ids = val
        self._value.subscriptionIds = val.value

    def __str__(self):
        return ("UaSetPublishingModeRequest:\n" + 
                self._request_header.str_helper(1) +
                self._publishing_enabled.str_helper(1) +
                self._subscription_ids_size.str_helper(1) +
                self._subscription_ids.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSetPublishingModeRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._publishing_enabled.str_helper(n+1) +
                self._subscription_ids_size.str_helper(n+1) +
                self._subscription_ids.str_helper(n+1))


# +++++++++++++++++++ UaIssuedIdentityToken +++++++++++++++++++++++
class UaIssuedIdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_IssuedIdentityToken*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._policy_id = UaString(val=val.policyId)
        self._token_data = UaByteString(val=val.tokenData)
        self._encryption_algorithm = UaString(val=val.encryptionAlgorithm)
    

    @property
    def policy_id(self):
        return self._policy_id

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val.value

    @property
    def token_data(self):
        return self._token_data

    @token_data.setter
    def token_data(self, val):
        self._token_data = val
        self._value.tokenData = val.value

    @property
    def encryption_algorithm(self):
        return self._encryption_algorithm

    @encryption_algorithm.setter
    def encryption_algorithm(self, val):
        self._encryption_algorithm = val
        self._value.encryptionAlgorithm = val.value

    def __str__(self):
        return ("UaIssuedIdentityToken:\n" + 
                self._policy_id.str_helper(1) +
                self._token_data.str_helper(1) +
                self._encryption_algorithm.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaIssuedIdentityToken:\n" + 
                self._policy_id.str_helper(n+1) +
                self._token_data.str_helper(n+1) +
                self._encryption_algorithm.str_helper(n+1))


# +++++++++++++++++++ UaDeleteMonitoredItemsResponse +++++++++++++++++++++++
class UaDeleteMonitoredItemsResponse(UaType):
    def __init__(self, val=ffi.new("UA_DeleteMonitoredItemsResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaDeleteMonitoredItemsResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteMonitoredItemsResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaBrowseNextRequest +++++++++++++++++++++++
class UaBrowseNextRequest(UaType):
    def __init__(self, val=ffi.new("UA_BrowseNextRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._release_continuation_points = UaBoolean(val=val.releaseContinuationPoints)
        self._continuation_points_size = SizeT(val=val.continuationPointsSize)
        self._continuation_points = UaByteString(val=val.continuationPoints, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def release_continuation_points(self):
        return self._release_continuation_points

    @release_continuation_points.setter
    def release_continuation_points(self, val):
        self._release_continuation_points = val
        self._value.releaseContinuationPoints = val.value

    @property
    def continuation_points_size(self):
        return self._continuation_points_size

    @continuation_points_size.setter
    def continuation_points_size(self, val):
        self._continuation_points_size = val
        self._value.continuationPointsSize = val.value

    @property
    def continuation_points(self):
        return self._continuation_points

    @continuation_points.setter
    def continuation_points(self, val):
        self._continuation_points = val
        self._value.continuationPoints = val.value

    def __str__(self):
        return ("UaBrowseNextRequest:\n" + 
                self._request_header.str_helper(1) +
                self._release_continuation_points.str_helper(1) +
                self._continuation_points_size.str_helper(1) +
                self._continuation_points.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBrowseNextRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._release_continuation_points.str_helper(n+1) +
                self._continuation_points_size.str_helper(n+1) +
                self._continuation_points.str_helper(n+1))


# +++++++++++++++++++ UaModifySubscriptionRequest +++++++++++++++++++++++
class UaModifySubscriptionRequest(UaType):
    def __init__(self, val=ffi.new("UA_ModifySubscriptionRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._requested_publishing_interval = UaDouble(val=val.requestedPublishingInterval)
        self._requested_lifetime_count = UaUInt32(val=val.requestedLifetimeCount)
        self._requested_max_keep_alive_count = UaUInt32(val=val.requestedMaxKeepAliveCount)
        self._max_notifications_per_publish = UaUInt32(val=val.maxNotificationsPerPublish)
        self._priority = UaByte(val=val.priority)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def requested_publishing_interval(self):
        return self._requested_publishing_interval

    @requested_publishing_interval.setter
    def requested_publishing_interval(self, val):
        self._requested_publishing_interval = val
        self._value.requestedPublishingInterval = val.value

    @property
    def requested_lifetime_count(self):
        return self._requested_lifetime_count

    @requested_lifetime_count.setter
    def requested_lifetime_count(self, val):
        self._requested_lifetime_count = val
        self._value.requestedLifetimeCount = val.value

    @property
    def requested_max_keep_alive_count(self):
        return self._requested_max_keep_alive_count

    @requested_max_keep_alive_count.setter
    def requested_max_keep_alive_count(self, val):
        self._requested_max_keep_alive_count = val
        self._value.requestedMaxKeepAliveCount = val.value

    @property
    def max_notifications_per_publish(self):
        return self._max_notifications_per_publish

    @max_notifications_per_publish.setter
    def max_notifications_per_publish(self, val):
        self._max_notifications_per_publish = val
        self._value.maxNotificationsPerPublish = val.value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, val):
        self._priority = val
        self._value.priority = val.value

    def __str__(self):
        return ("UaModifySubscriptionRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_id.str_helper(1) +
                self._requested_publishing_interval.str_helper(1) +
                self._requested_lifetime_count.str_helper(1) +
                self._requested_max_keep_alive_count.str_helper(1) +
                self._max_notifications_per_publish.str_helper(1) +
                self._priority.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaModifySubscriptionRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_id.str_helper(n+1) +
                self._requested_publishing_interval.str_helper(n+1) +
                self._requested_lifetime_count.str_helper(n+1) +
                self._requested_max_keep_alive_count.str_helper(n+1) +
                self._max_notifications_per_publish.str_helper(n+1) +
                self._priority.str_helper(n+1))


# +++++++++++++++++++ UaBrowseDescription +++++++++++++++++++++++
class UaBrowseDescription(UaType):
    def __init__(self, val=ffi.new("UA_BrowseDescription*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._node_id = UaNodeId(val=val.nodeId)
        self._browse_direction = UaBrowseDirection(val=val.browseDirection)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId)
        self._include_subtypes = UaBoolean(val=val.includeSubtypes)
        self._node_class_mask = UaUInt32(val=val.nodeClassMask)
        self._result_mask = UaUInt32(val=val.resultMask)
    

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val.value

    @property
    def browse_direction(self):
        return self._browse_direction

    @browse_direction.setter
    def browse_direction(self, val):
        self._browse_direction = val
        self._value.browseDirection = val.value

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val.value

    @property
    def include_subtypes(self):
        return self._include_subtypes

    @include_subtypes.setter
    def include_subtypes(self, val):
        self._include_subtypes = val
        self._value.includeSubtypes = val.value

    @property
    def node_class_mask(self):
        return self._node_class_mask

    @node_class_mask.setter
    def node_class_mask(self, val):
        self._node_class_mask = val
        self._value.nodeClassMask = val.value

    @property
    def result_mask(self):
        return self._result_mask

    @result_mask.setter
    def result_mask(self, val):
        self._result_mask = val
        self._value.resultMask = val.value

    def __str__(self):
        return ("UaBrowseDescription:\n" + 
                self._node_id.str_helper(1) +
                self._browse_direction.str_helper(1) +
                self._reference_type_id.str_helper(1) +
                self._include_subtypes.str_helper(1) +
                self._node_class_mask.str_helper(1) +
                self._result_mask.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBrowseDescription:\n" + 
                self._node_id.str_helper(n+1) +
                self._browse_direction.str_helper(n+1) +
                self._reference_type_id.str_helper(n+1) +
                self._include_subtypes.str_helper(n+1) +
                self._node_class_mask.str_helper(n+1) +
                self._result_mask.str_helper(n+1))


# +++++++++++++++++++ UaSignedSoftwareCertificate +++++++++++++++++++++++
class UaSignedSoftwareCertificate(UaType):
    def __init__(self, val=ffi.new("UA_SignedSoftwareCertificate*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._certificate_data = UaByteString(val=val.certificateData)
        self._signature = UaByteString(val=val.signature)
    

    @property
    def certificate_data(self):
        return self._certificate_data

    @certificate_data.setter
    def certificate_data(self, val):
        self._certificate_data = val
        self._value.certificateData = val.value

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, val):
        self._signature = val
        self._value.signature = val.value

    def __str__(self):
        return ("UaSignedSoftwareCertificate:\n" + 
                self._certificate_data.str_helper(1) +
                self._signature.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSignedSoftwareCertificate:\n" + 
                self._certificate_data.str_helper(n+1) +
                self._signature.str_helper(n+1))


# +++++++++++++++++++ UaBrowsePathTarget +++++++++++++++++++++++
class UaBrowsePathTarget(UaType):
    def __init__(self, val=ffi.new("UA_BrowsePathTarget*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._target_id = UaExpandedNodeId(val=val.targetId)
        self._remaining_path_index = UaUInt32(val=val.remainingPathIndex)
    

    @property
    def target_id(self):
        return self._target_id

    @target_id.setter
    def target_id(self, val):
        self._target_id = val
        self._value.targetId = val.value

    @property
    def remaining_path_index(self):
        return self._remaining_path_index

    @remaining_path_index.setter
    def remaining_path_index(self, val):
        self._remaining_path_index = val
        self._value.remainingPathIndex = val.value

    def __str__(self):
        return ("UaBrowsePathTarget:\n" + 
                self._target_id.str_helper(1) +
                self._remaining_path_index.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBrowsePathTarget:\n" + 
                self._target_id.str_helper(n+1) +
                self._remaining_path_index.str_helper(n+1))


# +++++++++++++++++++ UaWriteResponse +++++++++++++++++++++++
class UaWriteResponse(UaType):
    def __init__(self, val=ffi.new("UA_WriteResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaWriteResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaWriteResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaAddNodesResult +++++++++++++++++++++++
class UaAddNodesResult(UaType):
    def __init__(self, val=ffi.new("UA_AddNodesResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._status_code = UaStatusCode(val=val.statusCode)
        self._added_node_id = UaNodeId(val=val.addedNodeId)
    

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val.value

    @property
    def added_node_id(self):
        return self._added_node_id

    @added_node_id.setter
    def added_node_id(self, val):
        self._added_node_id = val
        self._value.addedNodeId = val.value

    def __str__(self):
        return ("UaAddNodesResult:\n" + 
                self._status_code.str_helper(1) +
                self._added_node_id.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAddNodesResult:\n" + 
                self._status_code.str_helper(n+1) +
                self._added_node_id.str_helper(n+1))


# +++++++++++++++++++ UaAddReferencesItem +++++++++++++++++++++++
class UaAddReferencesItem(UaType):
    def __init__(self, val=ffi.new("UA_AddReferencesItem*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._source_node_id = UaNodeId(val=val.sourceNodeId)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId)
        self._is_forward = UaBoolean(val=val.isForward)
        self._target_server_uri = UaString(val=val.targetServerUri)
        self._target_node_id = UaExpandedNodeId(val=val.targetNodeId)
        self._target_node_class = UaNodeClass(val=val.targetNodeClass)
    

    @property
    def source_node_id(self):
        return self._source_node_id

    @source_node_id.setter
    def source_node_id(self, val):
        self._source_node_id = val
        self._value.sourceNodeId = val.value

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val.value

    @property
    def is_forward(self):
        return self._is_forward

    @is_forward.setter
    def is_forward(self, val):
        self._is_forward = val
        self._value.isForward = val.value

    @property
    def target_server_uri(self):
        return self._target_server_uri

    @target_server_uri.setter
    def target_server_uri(self, val):
        self._target_server_uri = val
        self._value.targetServerUri = val.value

    @property
    def target_node_id(self):
        return self._target_node_id

    @target_node_id.setter
    def target_node_id(self, val):
        self._target_node_id = val
        self._value.targetNodeId = val.value

    @property
    def target_node_class(self):
        return self._target_node_class

    @target_node_class.setter
    def target_node_class(self, val):
        self._target_node_class = val
        self._value.targetNodeClass = val.value

    def __str__(self):
        return ("UaAddReferencesItem:\n" + 
                self._source_node_id.str_helper(1) +
                self._reference_type_id.str_helper(1) +
                self._is_forward.str_helper(1) +
                self._target_server_uri.str_helper(1) +
                self._target_node_id.str_helper(1) +
                self._target_node_class.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAddReferencesItem:\n" + 
                self._source_node_id.str_helper(n+1) +
                self._reference_type_id.str_helper(n+1) +
                self._is_forward.str_helper(n+1) +
                self._target_server_uri.str_helper(n+1) +
                self._target_node_id.str_helper(n+1) +
                self._target_node_class.str_helper(n+1))


# +++++++++++++++++++ UaDeleteReferencesResponse +++++++++++++++++++++++
class UaDeleteReferencesResponse(UaType):
    def __init__(self, val=ffi.new("UA_DeleteReferencesResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaDeleteReferencesResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteReferencesResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaRelativePathElement +++++++++++++++++++++++
class UaRelativePathElement(UaType):
    def __init__(self, val=ffi.new("UA_RelativePathElement*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId)
        self._is_inverse = UaBoolean(val=val.isInverse)
        self._include_subtypes = UaBoolean(val=val.includeSubtypes)
        self._target_name = UaQualifiedName(val=val.targetName)
    

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val.value

    @property
    def is_inverse(self):
        return self._is_inverse

    @is_inverse.setter
    def is_inverse(self, val):
        self._is_inverse = val
        self._value.isInverse = val.value

    @property
    def include_subtypes(self):
        return self._include_subtypes

    @include_subtypes.setter
    def include_subtypes(self, val):
        self._include_subtypes = val
        self._value.includeSubtypes = val.value

    @property
    def target_name(self):
        return self._target_name

    @target_name.setter
    def target_name(self, val):
        self._target_name = val
        self._value.targetName = val.value

    def __str__(self):
        return ("UaRelativePathElement:\n" + 
                self._reference_type_id.str_helper(1) +
                self._is_inverse.str_helper(1) +
                self._include_subtypes.str_helper(1) +
                self._target_name.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaRelativePathElement:\n" + 
                self._reference_type_id.str_helper(n+1) +
                self._is_inverse.str_helper(n+1) +
                self._include_subtypes.str_helper(n+1) +
                self._target_name.str_helper(n+1))


# +++++++++++++++++++ UaSubscriptionAcknowledgement +++++++++++++++++++++++
class UaSubscriptionAcknowledgement(UaType):
    def __init__(self, val=ffi.new("UA_SubscriptionAcknowledgement*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._sequence_number = UaUInt32(val=val.sequenceNumber)
    

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def sequence_number(self):
        return self._sequence_number

    @sequence_number.setter
    def sequence_number(self, val):
        self._sequence_number = val
        self._value.sequenceNumber = val.value

    def __str__(self):
        return ("UaSubscriptionAcknowledgement:\n" + 
                self._subscription_id.str_helper(1) +
                self._sequence_number.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSubscriptionAcknowledgement:\n" + 
                self._subscription_id.str_helper(n+1) +
                self._sequence_number.str_helper(n+1))


# +++++++++++++++++++ UaTransferResult +++++++++++++++++++++++
class UaTransferResult(UaType):
    def __init__(self, val=ffi.new("UA_TransferResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._status_code = UaStatusCode(val=val.statusCode)
        self._available_sequence_numbers_size = SizeT(val=val.availableSequenceNumbersSize)
        self._available_sequence_numbers = UaUInt32(val=val.availableSequenceNumbers, is_pointer=True)
    

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val.value

    @property
    def available_sequence_numbers_size(self):
        return self._available_sequence_numbers_size

    @available_sequence_numbers_size.setter
    def available_sequence_numbers_size(self, val):
        self._available_sequence_numbers_size = val
        self._value.availableSequenceNumbersSize = val.value

    @property
    def available_sequence_numbers(self):
        return self._available_sequence_numbers

    @available_sequence_numbers.setter
    def available_sequence_numbers(self, val):
        self._available_sequence_numbers = val
        self._value.availableSequenceNumbers = val.value

    def __str__(self):
        return ("UaTransferResult:\n" + 
                self._status_code.str_helper(1) +
                self._available_sequence_numbers_size.str_helper(1) +
                self._available_sequence_numbers.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaTransferResult:\n" + 
                self._status_code.str_helper(n+1) +
                self._available_sequence_numbers_size.str_helper(n+1) +
                self._available_sequence_numbers.str_helper(n+1))


# +++++++++++++++++++ UaCreateMonitoredItemsResponse +++++++++++++++++++++++
class UaCreateMonitoredItemsResponse(UaType):
    def __init__(self, val=ffi.new("UA_CreateMonitoredItemsResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaMonitoredItemCreateResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaCreateMonitoredItemsResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCreateMonitoredItemsResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaDeleteReferencesItem +++++++++++++++++++++++
class UaDeleteReferencesItem(UaType):
    def __init__(self, val=ffi.new("UA_DeleteReferencesItem*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._source_node_id = UaNodeId(val=val.sourceNodeId)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId)
        self._is_forward = UaBoolean(val=val.isForward)
        self._target_node_id = UaExpandedNodeId(val=val.targetNodeId)
        self._delete_bidirectional = UaBoolean(val=val.deleteBidirectional)
    

    @property
    def source_node_id(self):
        return self._source_node_id

    @source_node_id.setter
    def source_node_id(self, val):
        self._source_node_id = val
        self._value.sourceNodeId = val.value

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val.value

    @property
    def is_forward(self):
        return self._is_forward

    @is_forward.setter
    def is_forward(self, val):
        self._is_forward = val
        self._value.isForward = val.value

    @property
    def target_node_id(self):
        return self._target_node_id

    @target_node_id.setter
    def target_node_id(self, val):
        self._target_node_id = val
        self._value.targetNodeId = val.value

    @property
    def delete_bidirectional(self):
        return self._delete_bidirectional

    @delete_bidirectional.setter
    def delete_bidirectional(self, val):
        self._delete_bidirectional = val
        self._value.deleteBidirectional = val.value

    def __str__(self):
        return ("UaDeleteReferencesItem:\n" + 
                self._source_node_id.str_helper(1) +
                self._reference_type_id.str_helper(1) +
                self._is_forward.str_helper(1) +
                self._target_node_id.str_helper(1) +
                self._delete_bidirectional.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteReferencesItem:\n" + 
                self._source_node_id.str_helper(n+1) +
                self._reference_type_id.str_helper(n+1) +
                self._is_forward.str_helper(n+1) +
                self._target_node_id.str_helper(n+1) +
                self._delete_bidirectional.str_helper(n+1))


# +++++++++++++++++++ UaWriteValue +++++++++++++++++++++++
class UaWriteValue(UaType):
    def __init__(self, val=ffi.new("UA_WriteValue*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._node_id = UaNodeId(val=val.nodeId)
        self._attribute_id = UaUInt32(val=val.attributeId)
        self._index_range = UaString(val=val.indexRange)
        self._value = UaDataValue(val=val.value)
    

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val.value

    @property
    def attribute_id(self):
        return self._attribute_id

    @attribute_id.setter
    def attribute_id(self, val):
        self._attribute_id = val
        self._value.attributeId = val.value

    @property
    def index_range(self):
        return self._index_range

    @index_range.setter
    def index_range(self, val):
        self._index_range = val
        self._value.indexRange = val.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._value.value = val.value

    def __str__(self):
        return ("UaWriteValue:\n" + 
                self._node_id.str_helper(1) +
                self._attribute_id.str_helper(1) +
                self._index_range.str_helper(1) +
                self._value.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaWriteValue:\n" + 
                self._node_id.str_helper(n+1) +
                self._attribute_id.str_helper(n+1) +
                self._index_range.str_helper(n+1) +
                self._value.str_helper(n+1))


# +++++++++++++++++++ UaDataTypeAttributes +++++++++++++++++++++++
class UaDataTypeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_DataTypeAttributes*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._specified_attributes = UaUInt32(val=val.specifiedAttributes)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._write_mask = UaUInt32(val=val.writeMask)
        self._user_write_mask = UaUInt32(val=val.userWriteMask)
        self._is_abstract = UaBoolean(val=val.isAbstract)
    

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def write_mask(self):
        return self._write_mask

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val.value

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val.value

    @property
    def is_abstract(self):
        return self._is_abstract

    @is_abstract.setter
    def is_abstract(self, val):
        self._is_abstract = val
        self._value.isAbstract = val.value

    def __str__(self):
        return ("UaDataTypeAttributes:\n" + 
                self._specified_attributes.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._write_mask.str_helper(1) +
                self._user_write_mask.str_helper(1) +
                self._is_abstract.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDataTypeAttributes:\n" + 
                self._specified_attributes.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._write_mask.str_helper(n+1) +
                self._user_write_mask.str_helper(n+1) +
                self._is_abstract.str_helper(n+1))


# +++++++++++++++++++ UaTransferSubscriptionsResponse +++++++++++++++++++++++
class UaTransferSubscriptionsResponse(UaType):
    def __init__(self, val=ffi.new("UA_TransferSubscriptionsResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaTransferResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaTransferSubscriptionsResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaTransferSubscriptionsResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaAddReferencesResponse +++++++++++++++++++++++
class UaAddReferencesResponse(UaType):
    def __init__(self, val=ffi.new("UA_AddReferencesResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaAddReferencesResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAddReferencesResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaBuildInfo +++++++++++++++++++++++
class UaBuildInfo(UaType):
    def __init__(self, val=ffi.new("UA_BuildInfo*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._product_uri = UaString(val=val.productUri)
        self._manufacturer_name = UaString(val=val.manufacturerName)
        self._product_name = UaString(val=val.productName)
        self._software_version = UaString(val=val.softwareVersion)
        self._build_number = UaString(val=val.buildNumber)
        self._build_date = UaDateTime(val=val.buildDate)
    

    @property
    def product_uri(self):
        return self._product_uri

    @product_uri.setter
    def product_uri(self, val):
        self._product_uri = val
        self._value.productUri = val.value

    @property
    def manufacturer_name(self):
        return self._manufacturer_name

    @manufacturer_name.setter
    def manufacturer_name(self, val):
        self._manufacturer_name = val
        self._value.manufacturerName = val.value

    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, val):
        self._product_name = val
        self._value.productName = val.value

    @property
    def software_version(self):
        return self._software_version

    @software_version.setter
    def software_version(self, val):
        self._software_version = val
        self._value.softwareVersion = val.value

    @property
    def build_number(self):
        return self._build_number

    @build_number.setter
    def build_number(self, val):
        self._build_number = val
        self._value.buildNumber = val.value

    @property
    def build_date(self):
        return self._build_date

    @build_date.setter
    def build_date(self, val):
        self._build_date = val
        self._value.buildDate = val.value

    def __str__(self):
        return ("UaBuildInfo:\n" + 
                self._product_uri.str_helper(1) +
                self._manufacturer_name.str_helper(1) +
                self._product_name.str_helper(1) +
                self._software_version.str_helper(1) +
                self._build_number.str_helper(1) +
                self._build_date.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBuildInfo:\n" + 
                self._product_uri.str_helper(n+1) +
                self._manufacturer_name.str_helper(n+1) +
                self._product_name.str_helper(n+1) +
                self._software_version.str_helper(n+1) +
                self._build_number.str_helper(n+1) +
                self._build_date.str_helper(n+1))


# +++++++++++++++++++ UaMonitoringParameters +++++++++++++++++++++++
class UaMonitoringParameters(UaType):
    def __init__(self, val=ffi.new("UA_MonitoringParameters*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._client_handle = UaUInt32(val=val.clientHandle)
        self._sampling_interval = UaDouble(val=val.samplingInterval)
        self._filter = UaExtensionObject(val=val.filter)
        self._queue_size = UaUInt32(val=val.queueSize)
        self._discard_oldest = UaBoolean(val=val.discardOldest)
    

    @property
    def client_handle(self):
        return self._client_handle

    @client_handle.setter
    def client_handle(self, val):
        self._client_handle = val
        self._value.clientHandle = val.value

    @property
    def sampling_interval(self):
        return self._sampling_interval

    @sampling_interval.setter
    def sampling_interval(self, val):
        self._sampling_interval = val
        self._value.samplingInterval = val.value

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, val):
        self._filter = val
        self._value.filter = val.value

    @property
    def queue_size(self):
        return self._queue_size

    @queue_size.setter
    def queue_size(self, val):
        self._queue_size = val
        self._value.queueSize = val.value

    @property
    def discard_oldest(self):
        return self._discard_oldest

    @discard_oldest.setter
    def discard_oldest(self, val):
        self._discard_oldest = val
        self._value.discardOldest = val.value

    def __str__(self):
        return ("UaMonitoringParameters:\n" + 
                self._client_handle.str_helper(1) +
                self._sampling_interval.str_helper(1) +
                self._filter.str_helper(1) +
                self._queue_size.str_helper(1) +
                self._discard_oldest.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaMonitoringParameters:\n" + 
                self._client_handle.str_helper(n+1) +
                self._sampling_interval.str_helper(n+1) +
                self._filter.str_helper(n+1) +
                self._queue_size.str_helper(n+1) +
                self._discard_oldest.str_helper(n+1))


# +++++++++++++++++++ UaDoubleComplexNumberType +++++++++++++++++++++++
class UaDoubleComplexNumberType(UaType):
    def __init__(self, val=ffi.new("UA_DoubleComplexNumberType*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._real = UaDouble(val=val.real)
        self._imaginary = UaDouble(val=val.imaginary)
    

    @property
    def real(self):
        return self._real

    @real.setter
    def real(self, val):
        self._real = val
        self._value.real = val.value

    @property
    def imaginary(self):
        return self._imaginary

    @imaginary.setter
    def imaginary(self, val):
        self._imaginary = val
        self._value.imaginary = val.value

    def __str__(self):
        return ("UaDoubleComplexNumberType:\n" + 
                self._real.str_helper(1) +
                self._imaginary.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDoubleComplexNumberType:\n" + 
                self._real.str_helper(n+1) +
                self._imaginary.str_helper(n+1))


# +++++++++++++++++++ UaDeleteNodesItem +++++++++++++++++++++++
class UaDeleteNodesItem(UaType):
    def __init__(self, val=ffi.new("UA_DeleteNodesItem*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._node_id = UaNodeId(val=val.nodeId)
        self._delete_target_references = UaBoolean(val=val.deleteTargetReferences)
    

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val.value

    @property
    def delete_target_references(self):
        return self._delete_target_references

    @delete_target_references.setter
    def delete_target_references(self, val):
        self._delete_target_references = val
        self._value.deleteTargetReferences = val.value

    def __str__(self):
        return ("UaDeleteNodesItem:\n" + 
                self._node_id.str_helper(1) +
                self._delete_target_references.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteNodesItem:\n" + 
                self._node_id.str_helper(n+1) +
                self._delete_target_references.str_helper(n+1))


# +++++++++++++++++++ UaReadValueId +++++++++++++++++++++++
class UaReadValueId(UaType):
    def __init__(self, val=ffi.new("UA_ReadValueId*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._node_id = UaNodeId(val=val.nodeId)
        self._attribute_id = UaUInt32(val=val.attributeId)
        self._index_range = UaString(val=val.indexRange)
        self._data_encoding = UaQualifiedName(val=val.dataEncoding)
    

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val.value

    @property
    def attribute_id(self):
        return self._attribute_id

    @attribute_id.setter
    def attribute_id(self, val):
        self._attribute_id = val
        self._value.attributeId = val.value

    @property
    def index_range(self):
        return self._index_range

    @index_range.setter
    def index_range(self, val):
        self._index_range = val
        self._value.indexRange = val.value

    @property
    def data_encoding(self):
        return self._data_encoding

    @data_encoding.setter
    def data_encoding(self, val):
        self._data_encoding = val
        self._value.dataEncoding = val.value

    def __str__(self):
        return ("UaReadValueId:\n" + 
                self._node_id.str_helper(1) +
                self._attribute_id.str_helper(1) +
                self._index_range.str_helper(1) +
                self._data_encoding.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaReadValueId:\n" + 
                self._node_id.str_helper(n+1) +
                self._attribute_id.str_helper(n+1) +
                self._index_range.str_helper(n+1) +
                self._data_encoding.str_helper(n+1))


# +++++++++++++++++++ UaCallRequest +++++++++++++++++++++++
class UaCallRequest(UaType):
    def __init__(self, val=ffi.new("UA_CallRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._methods_to_call_size = SizeT(val=val.methodsToCallSize)
        self._methods_to_call = UaCallMethodRequest(val=val.methodsToCall, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def methods_to_call_size(self):
        return self._methods_to_call_size

    @methods_to_call_size.setter
    def methods_to_call_size(self, val):
        self._methods_to_call_size = val
        self._value.methodsToCallSize = val.value

    @property
    def methods_to_call(self):
        return self._methods_to_call

    @methods_to_call.setter
    def methods_to_call(self, val):
        self._methods_to_call = val
        self._value.methodsToCall = val.value

    def __str__(self):
        return ("UaCallRequest:\n" + 
                self._request_header.str_helper(1) +
                self._methods_to_call_size.str_helper(1) +
                self._methods_to_call.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCallRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._methods_to_call_size.str_helper(n+1) +
                self._methods_to_call.str_helper(n+1))


# +++++++++++++++++++ UaRelativePath +++++++++++++++++++++++
class UaRelativePath(UaType):
    def __init__(self, val=ffi.new("UA_RelativePath*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._elements_size = SizeT(val=val.elementsSize)
        self._elements = UaRelativePathElement(val=val.elements, is_pointer=True)
    

    @property
    def elements_size(self):
        return self._elements_size

    @elements_size.setter
    def elements_size(self, val):
        self._elements_size = val
        self._value.elementsSize = val.value

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, val):
        self._elements = val
        self._value.elements = val.value

    def __str__(self):
        return ("UaRelativePath:\n" + 
                self._elements_size.str_helper(1) +
                self._elements.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaRelativePath:\n" + 
                self._elements_size.str_helper(n+1) +
                self._elements.str_helper(n+1))


# +++++++++++++++++++ UaDeleteNodesRequest +++++++++++++++++++++++
class UaDeleteNodesRequest(UaType):
    def __init__(self, val=ffi.new("UA_DeleteNodesRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._nodes_to_delete_size = SizeT(val=val.nodesToDeleteSize)
        self._nodes_to_delete = UaDeleteNodesItem(val=val.nodesToDelete, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def nodes_to_delete_size(self):
        return self._nodes_to_delete_size

    @nodes_to_delete_size.setter
    def nodes_to_delete_size(self, val):
        self._nodes_to_delete_size = val
        self._value.nodesToDeleteSize = val.value

    @property
    def nodes_to_delete(self):
        return self._nodes_to_delete

    @nodes_to_delete.setter
    def nodes_to_delete(self, val):
        self._nodes_to_delete = val
        self._value.nodesToDelete = val.value

    def __str__(self):
        return ("UaDeleteNodesRequest:\n" + 
                self._request_header.str_helper(1) +
                self._nodes_to_delete_size.str_helper(1) +
                self._nodes_to_delete.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteNodesRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._nodes_to_delete_size.str_helper(n+1) +
                self._nodes_to_delete.str_helper(n+1))


# +++++++++++++++++++ UaMonitoredItemModifyRequest +++++++++++++++++++++++
class UaMonitoredItemModifyRequest(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemModifyRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._monitored_item_id = UaUInt32(val=val.monitoredItemId)
        self._requested_parameters = UaMonitoringParameters(val=val.requestedParameters)
    

    @property
    def monitored_item_id(self):
        return self._monitored_item_id

    @monitored_item_id.setter
    def monitored_item_id(self, val):
        self._monitored_item_id = val
        self._value.monitoredItemId = val.value

    @property
    def requested_parameters(self):
        return self._requested_parameters

    @requested_parameters.setter
    def requested_parameters(self, val):
        self._requested_parameters = val
        self._value.requestedParameters = val.value

    def __str__(self):
        return ("UaMonitoredItemModifyRequest:\n" + 
                self._monitored_item_id.str_helper(1) +
                self._requested_parameters.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaMonitoredItemModifyRequest:\n" + 
                self._monitored_item_id.str_helper(n+1) +
                self._requested_parameters.str_helper(n+1))


# +++++++++++++++++++ UaAggregateConfiguration +++++++++++++++++++++++
class UaAggregateConfiguration(UaType):
    def __init__(self, val=ffi.new("UA_AggregateConfiguration*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._use_server_capabilities_defaults = UaBoolean(val=val.useServerCapabilitiesDefaults)
        self._treat_uncertain_as_bad = UaBoolean(val=val.treatUncertainAsBad)
        self._percent_data_bad = UaByte(val=val.percentDataBad)
        self._percent_data_good = UaByte(val=val.percentDataGood)
        self._use_sloped_extrapolation = UaBoolean(val=val.useSlopedExtrapolation)
    

    @property
    def use_server_capabilities_defaults(self):
        return self._use_server_capabilities_defaults

    @use_server_capabilities_defaults.setter
    def use_server_capabilities_defaults(self, val):
        self._use_server_capabilities_defaults = val
        self._value.useServerCapabilitiesDefaults = val.value

    @property
    def treat_uncertain_as_bad(self):
        return self._treat_uncertain_as_bad

    @treat_uncertain_as_bad.setter
    def treat_uncertain_as_bad(self, val):
        self._treat_uncertain_as_bad = val
        self._value.treatUncertainAsBad = val.value

    @property
    def percent_data_bad(self):
        return self._percent_data_bad

    @percent_data_bad.setter
    def percent_data_bad(self, val):
        self._percent_data_bad = val
        self._value.percentDataBad = val.value

    @property
    def percent_data_good(self):
        return self._percent_data_good

    @percent_data_good.setter
    def percent_data_good(self, val):
        self._percent_data_good = val
        self._value.percentDataGood = val.value

    @property
    def use_sloped_extrapolation(self):
        return self._use_sloped_extrapolation

    @use_sloped_extrapolation.setter
    def use_sloped_extrapolation(self, val):
        self._use_sloped_extrapolation = val
        self._value.useSlopedExtrapolation = val.value

    def __str__(self):
        return ("UaAggregateConfiguration:\n" + 
                self._use_server_capabilities_defaults.str_helper(1) +
                self._treat_uncertain_as_bad.str_helper(1) +
                self._percent_data_bad.str_helper(1) +
                self._percent_data_good.str_helper(1) +
                self._use_sloped_extrapolation.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAggregateConfiguration:\n" + 
                self._use_server_capabilities_defaults.str_helper(n+1) +
                self._treat_uncertain_as_bad.str_helper(n+1) +
                self._percent_data_bad.str_helper(n+1) +
                self._percent_data_good.str_helper(n+1) +
                self._use_sloped_extrapolation.str_helper(n+1))


# +++++++++++++++++++ UaUnregisterNodesResponse +++++++++++++++++++++++
class UaUnregisterNodesResponse(UaType):
    def __init__(self, val=ffi.new("UA_UnregisterNodesResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    def __str__(self):
        return ("UaUnregisterNodesResponse:\n" + 
                self._response_header.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaUnregisterNodesResponse:\n" + 
                self._response_header.str_helper(n+1))


# +++++++++++++++++++ UaContentFilterResult +++++++++++++++++++++++
class UaContentFilterResult(UaType):
    def __init__(self, val=ffi.new("UA_ContentFilterResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._element_results_size = SizeT(val=val.elementResultsSize)
        self._element_results = UaContentFilterElementResult(val=val.elementResults, is_pointer=True)
        self._element_diagnostic_infos_size = SizeT(val=val.elementDiagnosticInfosSize)
        self._element_diagnostic_infos = UaDiagnosticInfo(val=val.elementDiagnosticInfos, is_pointer=True)
    

    @property
    def element_results_size(self):
        return self._element_results_size

    @element_results_size.setter
    def element_results_size(self, val):
        self._element_results_size = val
        self._value.elementResultsSize = val.value

    @property
    def element_results(self):
        return self._element_results

    @element_results.setter
    def element_results(self, val):
        self._element_results = val
        self._value.elementResults = val.value

    @property
    def element_diagnostic_infos_size(self):
        return self._element_diagnostic_infos_size

    @element_diagnostic_infos_size.setter
    def element_diagnostic_infos_size(self, val):
        self._element_diagnostic_infos_size = val
        self._value.elementDiagnosticInfosSize = val.value

    @property
    def element_diagnostic_infos(self):
        return self._element_diagnostic_infos

    @element_diagnostic_infos.setter
    def element_diagnostic_infos(self, val):
        self._element_diagnostic_infos = val
        self._value.elementDiagnosticInfos = val.value

    def __str__(self):
        return ("UaContentFilterResult:\n" + 
                self._element_results_size.str_helper(1) +
                self._element_results.str_helper(1) +
                self._element_diagnostic_infos_size.str_helper(1) +
                self._element_diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaContentFilterResult:\n" + 
                self._element_results_size.str_helper(n+1) +
                self._element_results.str_helper(n+1) +
                self._element_diagnostic_infos_size.str_helper(n+1) +
                self._element_diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaUserTokenPolicy +++++++++++++++++++++++
class UaUserTokenPolicy(UaType):
    def __init__(self, val=ffi.new("UA_UserTokenPolicy*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._policy_id = UaString(val=val.policyId)
        self._token_type = UaUserTokenType(val=val.tokenType)
        self._issued_token_type = UaString(val=val.issuedTokenType)
        self._issuer_endpoint_url = UaString(val=val.issuerEndpointUrl)
        self._security_policy_uri = UaString(val=val.securityPolicyUri)
    

    @property
    def policy_id(self):
        return self._policy_id

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val.value

    @property
    def token_type(self):
        return self._token_type

    @token_type.setter
    def token_type(self, val):
        self._token_type = val
        self._value.tokenType = val.value

    @property
    def issued_token_type(self):
        return self._issued_token_type

    @issued_token_type.setter
    def issued_token_type(self, val):
        self._issued_token_type = val
        self._value.issuedTokenType = val.value

    @property
    def issuer_endpoint_url(self):
        return self._issuer_endpoint_url

    @issuer_endpoint_url.setter
    def issuer_endpoint_url(self, val):
        self._issuer_endpoint_url = val
        self._value.issuerEndpointUrl = val.value

    @property
    def security_policy_uri(self):
        return self._security_policy_uri

    @security_policy_uri.setter
    def security_policy_uri(self, val):
        self._security_policy_uri = val
        self._value.securityPolicyUri = val.value

    def __str__(self):
        return ("UaUserTokenPolicy:\n" + 
                self._policy_id.str_helper(1) +
                self._token_type.str_helper(1) +
                self._issued_token_type.str_helper(1) +
                self._issuer_endpoint_url.str_helper(1) +
                self._security_policy_uri.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaUserTokenPolicy:\n" + 
                self._policy_id.str_helper(n+1) +
                self._token_type.str_helper(n+1) +
                self._issued_token_type.str_helper(n+1) +
                self._issuer_endpoint_url.str_helper(n+1) +
                self._security_policy_uri.str_helper(n+1))


# +++++++++++++++++++ UaDeleteMonitoredItemsRequest +++++++++++++++++++++++
class UaDeleteMonitoredItemsRequest(UaType):
    def __init__(self, val=ffi.new("UA_DeleteMonitoredItemsRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._monitored_item_ids_size = SizeT(val=val.monitoredItemIdsSize)
        self._monitored_item_ids = UaUInt32(val=val.monitoredItemIds, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def monitored_item_ids_size(self):
        return self._monitored_item_ids_size

    @monitored_item_ids_size.setter
    def monitored_item_ids_size(self, val):
        self._monitored_item_ids_size = val
        self._value.monitoredItemIdsSize = val.value

    @property
    def monitored_item_ids(self):
        return self._monitored_item_ids

    @monitored_item_ids.setter
    def monitored_item_ids(self, val):
        self._monitored_item_ids = val
        self._value.monitoredItemIds = val.value

    def __str__(self):
        return ("UaDeleteMonitoredItemsRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_id.str_helper(1) +
                self._monitored_item_ids_size.str_helper(1) +
                self._monitored_item_ids.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteMonitoredItemsRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_id.str_helper(n+1) +
                self._monitored_item_ids_size.str_helper(n+1) +
                self._monitored_item_ids.str_helper(n+1))


# +++++++++++++++++++ UaSetMonitoringModeRequest +++++++++++++++++++++++
class UaSetMonitoringModeRequest(UaType):
    def __init__(self, val=ffi.new("UA_SetMonitoringModeRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._monitoring_mode = UaMonitoringMode(val=val.monitoringMode)
        self._monitored_item_ids_size = SizeT(val=val.monitoredItemIdsSize)
        self._monitored_item_ids = UaUInt32(val=val.monitoredItemIds, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def monitoring_mode(self):
        return self._monitoring_mode

    @monitoring_mode.setter
    def monitoring_mode(self, val):
        self._monitoring_mode = val
        self._value.monitoringMode = val.value

    @property
    def monitored_item_ids_size(self):
        return self._monitored_item_ids_size

    @monitored_item_ids_size.setter
    def monitored_item_ids_size(self, val):
        self._monitored_item_ids_size = val
        self._value.monitoredItemIdsSize = val.value

    @property
    def monitored_item_ids(self):
        return self._monitored_item_ids

    @monitored_item_ids.setter
    def monitored_item_ids(self, val):
        self._monitored_item_ids = val
        self._value.monitoredItemIds = val.value

    def __str__(self):
        return ("UaSetMonitoringModeRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_id.str_helper(1) +
                self._monitoring_mode.str_helper(1) +
                self._monitored_item_ids_size.str_helper(1) +
                self._monitored_item_ids.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSetMonitoringModeRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_id.str_helper(n+1) +
                self._monitoring_mode.str_helper(n+1) +
                self._monitored_item_ids_size.str_helper(n+1) +
                self._monitored_item_ids.str_helper(n+1))


# +++++++++++++++++++ UaReferenceTypeAttributes +++++++++++++++++++++++
class UaReferenceTypeAttributes(UaType):
    def __init__(self, val=ffi.new("UA_ReferenceTypeAttributes*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._specified_attributes = UaUInt32(val=val.specifiedAttributes)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._write_mask = UaUInt32(val=val.writeMask)
        self._user_write_mask = UaUInt32(val=val.userWriteMask)
        self._is_abstract = UaBoolean(val=val.isAbstract)
        self._symmetric = UaBoolean(val=val.symmetric)
        self._inverse_name = UaLocalizedText(val=val.inverseName)
    

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def write_mask(self):
        return self._write_mask

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val.value

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val.value

    @property
    def is_abstract(self):
        return self._is_abstract

    @is_abstract.setter
    def is_abstract(self, val):
        self._is_abstract = val
        self._value.isAbstract = val.value

    @property
    def symmetric(self):
        return self._symmetric

    @symmetric.setter
    def symmetric(self, val):
        self._symmetric = val
        self._value.symmetric = val.value

    @property
    def inverse_name(self):
        return self._inverse_name

    @inverse_name.setter
    def inverse_name(self, val):
        self._inverse_name = val
        self._value.inverseName = val.value

    def __str__(self):
        return ("UaReferenceTypeAttributes:\n" + 
                self._specified_attributes.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._write_mask.str_helper(1) +
                self._user_write_mask.str_helper(1) +
                self._is_abstract.str_helper(1) +
                self._symmetric.str_helper(1) +
                self._inverse_name.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaReferenceTypeAttributes:\n" + 
                self._specified_attributes.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._write_mask.str_helper(n+1) +
                self._user_write_mask.str_helper(n+1) +
                self._is_abstract.str_helper(n+1) +
                self._symmetric.str_helper(n+1) +
                self._inverse_name.str_helper(n+1))


# +++++++++++++++++++ UaGetEndpointsRequest +++++++++++++++++++++++
class UaGetEndpointsRequest(UaType):
    def __init__(self, val=ffi.new("UA_GetEndpointsRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._endpoint_url = UaString(val=val.endpointUrl)
        self._locale_ids_size = SizeT(val=val.localeIdsSize)
        self._locale_ids = UaString(val=val.localeIds, is_pointer=True)
        self._profile_uris_size = SizeT(val=val.profileUrisSize)
        self._profile_uris = UaString(val=val.profileUris, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, val):
        self._endpoint_url = val
        self._value.endpointUrl = val.value

    @property
    def locale_ids_size(self):
        return self._locale_ids_size

    @locale_ids_size.setter
    def locale_ids_size(self, val):
        self._locale_ids_size = val
        self._value.localeIdsSize = val.value

    @property
    def locale_ids(self):
        return self._locale_ids

    @locale_ids.setter
    def locale_ids(self, val):
        self._locale_ids = val
        self._value.localeIds = val.value

    @property
    def profile_uris_size(self):
        return self._profile_uris_size

    @profile_uris_size.setter
    def profile_uris_size(self, val):
        self._profile_uris_size = val
        self._value.profileUrisSize = val.value

    @property
    def profile_uris(self):
        return self._profile_uris

    @profile_uris.setter
    def profile_uris(self, val):
        self._profile_uris = val
        self._value.profileUris = val.value

    def __str__(self):
        return ("UaGetEndpointsRequest:\n" + 
                self._request_header.str_helper(1) +
                self._endpoint_url.str_helper(1) +
                self._locale_ids_size.str_helper(1) +
                self._locale_ids.str_helper(1) +
                self._profile_uris_size.str_helper(1) +
                self._profile_uris.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaGetEndpointsRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._endpoint_url.str_helper(n+1) +
                self._locale_ids_size.str_helper(n+1) +
                self._locale_ids.str_helper(n+1) +
                self._profile_uris_size.str_helper(n+1) +
                self._profile_uris.str_helper(n+1))


# +++++++++++++++++++ UaCloseSecureChannelResponse +++++++++++++++++++++++
class UaCloseSecureChannelResponse(UaType):
    def __init__(self, val=ffi.new("UA_CloseSecureChannelResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    def __str__(self):
        return ("UaCloseSecureChannelResponse:\n" + 
                self._response_header.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCloseSecureChannelResponse:\n" + 
                self._response_header.str_helper(n+1))


# +++++++++++++++++++ UaViewDescription +++++++++++++++++++++++
class UaViewDescription(UaType):
    def __init__(self, val=ffi.new("UA_ViewDescription*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._view_id = UaNodeId(val=val.viewId)
        self._timestamp = UaDateTime(val=val.timestamp)
        self._view_version = UaUInt32(val=val.viewVersion)
    

    @property
    def view_id(self):
        return self._view_id

    @view_id.setter
    def view_id(self, val):
        self._view_id = val
        self._value.viewId = val.value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, val):
        self._timestamp = val
        self._value.timestamp = val.value

    @property
    def view_version(self):
        return self._view_version

    @view_version.setter
    def view_version(self, val):
        self._view_version = val
        self._value.viewVersion = val.value

    def __str__(self):
        return ("UaViewDescription:\n" + 
                self._view_id.str_helper(1) +
                self._timestamp.str_helper(1) +
                self._view_version.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaViewDescription:\n" + 
                self._view_id.str_helper(n+1) +
                self._timestamp.str_helper(n+1) +
                self._view_version.str_helper(n+1))


# +++++++++++++++++++ UaSetPublishingModeResponse +++++++++++++++++++++++
class UaSetPublishingModeResponse(UaType):
    def __init__(self, val=ffi.new("UA_SetPublishingModeResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaSetPublishingModeResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSetPublishingModeResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaStatusChangeNotification +++++++++++++++++++++++
class UaStatusChangeNotification(UaType):
    def __init__(self, val=ffi.new("UA_StatusChangeNotification*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._status = UaStatusCode(val=val.status)
        self._diagnostic_info = UaDiagnosticInfo(val=val.diagnosticInfo)
    

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val
        self._value.status = val.value

    @property
    def diagnostic_info(self):
        return self._diagnostic_info

    @diagnostic_info.setter
    def diagnostic_info(self, val):
        self._diagnostic_info = val
        self._value.diagnosticInfo = val.value

    def __str__(self):
        return ("UaStatusChangeNotification:\n" + 
                self._status.str_helper(1) +
                self._diagnostic_info.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaStatusChangeNotification:\n" + 
                self._status.str_helper(n+1) +
                self._diagnostic_info.str_helper(n+1))


# +++++++++++++++++++ UaStructureField +++++++++++++++++++++++
class UaStructureField(UaType):
    def __init__(self, val=ffi.new("UA_StructureField*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._name = UaString(val=val.name)
        self._description = UaLocalizedText(val=val.description)
        self._data_type = UaNodeId(val=val.dataType)
        self._value_rank = UaInt32(val=val.valueRank)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
        self._max_string_length = UaUInt32(val=val.maxStringLength)
        self._is_optional = UaBoolean(val=val.isOptional)
    

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val
        self._value.name = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, val):
        self._data_type = val
        self._value.dataType = val.value

    @property
    def value_rank(self):
        return self._value_rank

    @value_rank.setter
    def value_rank(self, val):
        self._value_rank = val
        self._value.valueRank = val.value

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

    @property
    def max_string_length(self):
        return self._max_string_length

    @max_string_length.setter
    def max_string_length(self, val):
        self._max_string_length = val
        self._value.maxStringLength = val.value

    @property
    def is_optional(self):
        return self._is_optional

    @is_optional.setter
    def is_optional(self, val):
        self._is_optional = val
        self._value.isOptional = val.value

    def __str__(self):
        return ("UaStructureField:\n" + 
                self._name.str_helper(1) +
                self._description.str_helper(1) +
                self._data_type.str_helper(1) +
                self._value_rank.str_helper(1) +
                self._array_dimensions_size.str_helper(1) +
                self._array_dimensions.str_helper(1) +
                self._max_string_length.str_helper(1) +
                self._is_optional.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaStructureField:\n" + 
                self._name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._data_type.str_helper(n+1) +
                self._value_rank.str_helper(n+1) +
                self._array_dimensions_size.str_helper(n+1) +
                self._array_dimensions.str_helper(n+1) +
                self._max_string_length.str_helper(n+1) +
                self._is_optional.str_helper(n+1))


# +++++++++++++++++++ UaEventFilterResult +++++++++++++++++++++++
class UaEventFilterResult(UaType):
    def __init__(self, val=ffi.new("UA_EventFilterResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._select_clause_results_size = SizeT(val=val.selectClauseResultsSize)
        self._select_clause_results = UaStatusCode(val=val.selectClauseResults, is_pointer=True)
        self._select_clause_diagnostic_infos_size = SizeT(val=val.selectClauseDiagnosticInfosSize)
        self._select_clause_diagnostic_infos = UaDiagnosticInfo(val=val.selectClauseDiagnosticInfos, is_pointer=True)
        self._where_clause_result = UaContentFilterResult(val=val.whereClauseResult)
    

    @property
    def select_clause_results_size(self):
        return self._select_clause_results_size

    @select_clause_results_size.setter
    def select_clause_results_size(self, val):
        self._select_clause_results_size = val
        self._value.selectClauseResultsSize = val.value

    @property
    def select_clause_results(self):
        return self._select_clause_results

    @select_clause_results.setter
    def select_clause_results(self, val):
        self._select_clause_results = val
        self._value.selectClauseResults = val.value

    @property
    def select_clause_diagnostic_infos_size(self):
        return self._select_clause_diagnostic_infos_size

    @select_clause_diagnostic_infos_size.setter
    def select_clause_diagnostic_infos_size(self, val):
        self._select_clause_diagnostic_infos_size = val
        self._value.selectClauseDiagnosticInfosSize = val.value

    @property
    def select_clause_diagnostic_infos(self):
        return self._select_clause_diagnostic_infos

    @select_clause_diagnostic_infos.setter
    def select_clause_diagnostic_infos(self, val):
        self._select_clause_diagnostic_infos = val
        self._value.selectClauseDiagnosticInfos = val.value

    @property
    def where_clause_result(self):
        return self._where_clause_result

    @where_clause_result.setter
    def where_clause_result(self, val):
        self._where_clause_result = val
        self._value.whereClauseResult = val.value

    def __str__(self):
        return ("UaEventFilterResult:\n" + 
                self._select_clause_results_size.str_helper(1) +
                self._select_clause_results.str_helper(1) +
                self._select_clause_diagnostic_infos_size.str_helper(1) +
                self._select_clause_diagnostic_infos.str_helper(1) +
                self._where_clause_result.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaEventFilterResult:\n" + 
                self._select_clause_results_size.str_helper(n+1) +
                self._select_clause_results.str_helper(n+1) +
                self._select_clause_diagnostic_infos_size.str_helper(n+1) +
                self._select_clause_diagnostic_infos.str_helper(n+1) +
                self._where_clause_result.str_helper(n+1))


# +++++++++++++++++++ UaMonitoredItemCreateRequest +++++++++++++++++++++++
class UaMonitoredItemCreateRequest(UaType):
    def __init__(self, val=ffi.new("UA_MonitoredItemCreateRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._item_to_monitor = UaReadValueId(val=val.itemToMonitor)
        self._monitoring_mode = UaMonitoringMode(val=val.monitoringMode)
        self._requested_parameters = UaMonitoringParameters(val=val.requestedParameters)
    

    @property
    def item_to_monitor(self):
        return self._item_to_monitor

    @item_to_monitor.setter
    def item_to_monitor(self, val):
        self._item_to_monitor = val
        self._value.itemToMonitor = val.value

    @property
    def monitoring_mode(self):
        return self._monitoring_mode

    @monitoring_mode.setter
    def monitoring_mode(self, val):
        self._monitoring_mode = val
        self._value.monitoringMode = val.value

    @property
    def requested_parameters(self):
        return self._requested_parameters

    @requested_parameters.setter
    def requested_parameters(self, val):
        self._requested_parameters = val
        self._value.requestedParameters = val.value

    def __str__(self):
        return ("UaMonitoredItemCreateRequest:\n" + 
                self._item_to_monitor.str_helper(1) +
                self._monitoring_mode.str_helper(1) +
                self._requested_parameters.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaMonitoredItemCreateRequest:\n" + 
                self._item_to_monitor.str_helper(n+1) +
                self._monitoring_mode.str_helper(n+1) +
                self._requested_parameters.str_helper(n+1))


# +++++++++++++++++++ UaComplexNumberType +++++++++++++++++++++++
class UaComplexNumberType(UaType):
    def __init__(self, val=ffi.new("UA_ComplexNumberType*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._real = UaFloat(val=val.real)
        self._imaginary = UaFloat(val=val.imaginary)
    

    @property
    def real(self):
        return self._real

    @real.setter
    def real(self, val):
        self._real = val
        self._value.real = val.value

    @property
    def imaginary(self):
        return self._imaginary

    @imaginary.setter
    def imaginary(self, val):
        self._imaginary = val
        self._value.imaginary = val.value

    def __str__(self):
        return ("UaComplexNumberType:\n" + 
                self._real.str_helper(1) +
                self._imaginary.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaComplexNumberType:\n" + 
                self._real.str_helper(n+1) +
                self._imaginary.str_helper(n+1))


# +++++++++++++++++++ UaRange +++++++++++++++++++++++
class UaRange(UaType):
    def __init__(self, val=ffi.new("UA_Range*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._low = UaDouble(val=val.low)
        self._high = UaDouble(val=val.high)
    

    @property
    def low(self):
        return self._low

    @low.setter
    def low(self, val):
        self._low = val
        self._value.low = val.value

    @property
    def high(self):
        return self._high

    @high.setter
    def high(self, val):
        self._high = val
        self._value.high = val.value

    def __str__(self):
        return ("UaRange:\n" + 
                self._low.str_helper(1) +
                self._high.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaRange:\n" + 
                self._low.str_helper(n+1) +
                self._high.str_helper(n+1))


# +++++++++++++++++++ UaDataChangeNotification +++++++++++++++++++++++
class UaDataChangeNotification(UaType):
    def __init__(self, val=ffi.new("UA_DataChangeNotification*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._monitored_items_size = SizeT(val=val.monitoredItemsSize)
        self._monitored_items = UaMonitoredItemNotification(val=val.monitoredItems, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def monitored_items_size(self):
        return self._monitored_items_size

    @monitored_items_size.setter
    def monitored_items_size(self, val):
        self._monitored_items_size = val
        self._value.monitoredItemsSize = val.value

    @property
    def monitored_items(self):
        return self._monitored_items

    @monitored_items.setter
    def monitored_items(self, val):
        self._monitored_items = val
        self._value.monitoredItems = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaDataChangeNotification:\n" + 
                self._monitored_items_size.str_helper(1) +
                self._monitored_items.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDataChangeNotification:\n" + 
                self._monitored_items_size.str_helper(n+1) +
                self._monitored_items.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaArgument +++++++++++++++++++++++
class UaArgument(UaType):
    def __init__(self, val=ffi.new("UA_Argument*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._name = UaString(val=val.name)
        self._data_type = UaNodeId(val=val.dataType)
        self._value_rank = UaInt32(val=val.valueRank)
        self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize)
        self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
        self._description = UaLocalizedText(val=val.description)
    

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val
        self._value.name = val.value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, val):
        self._data_type = val
        self._value.dataType = val.value

    @property
    def value_rank(self):
        return self._value_rank

    @value_rank.setter
    def value_rank(self, val):
        self._value_rank = val
        self._value.valueRank = val.value

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

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    def __str__(self):
        return ("UaArgument:\n" + 
                self._name.str_helper(1) +
                self._data_type.str_helper(1) +
                self._value_rank.str_helper(1) +
                self._array_dimensions_size.str_helper(1) +
                self._array_dimensions.str_helper(1) +
                self._description.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaArgument:\n" + 
                self._name.str_helper(n+1) +
                self._data_type.str_helper(n+1) +
                self._value_rank.str_helper(n+1) +
                self._array_dimensions_size.str_helper(n+1) +
                self._array_dimensions.str_helper(n+1) +
                self._description.str_helper(n+1))


# +++++++++++++++++++ UaTransferSubscriptionsRequest +++++++++++++++++++++++
class UaTransferSubscriptionsRequest(UaType):
    def __init__(self, val=ffi.new("UA_TransferSubscriptionsRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_ids_size = SizeT(val=val.subscriptionIdsSize)
        self._subscription_ids = UaUInt32(val=val.subscriptionIds, is_pointer=True)
        self._send_initial_values = UaBoolean(val=val.sendInitialValues)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_ids_size(self):
        return self._subscription_ids_size

    @subscription_ids_size.setter
    def subscription_ids_size(self, val):
        self._subscription_ids_size = val
        self._value.subscriptionIdsSize = val.value

    @property
    def subscription_ids(self):
        return self._subscription_ids

    @subscription_ids.setter
    def subscription_ids(self, val):
        self._subscription_ids = val
        self._value.subscriptionIds = val.value

    @property
    def send_initial_values(self):
        return self._send_initial_values

    @send_initial_values.setter
    def send_initial_values(self, val):
        self._send_initial_values = val
        self._value.sendInitialValues = val.value

    def __str__(self):
        return ("UaTransferSubscriptionsRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_ids_size.str_helper(1) +
                self._subscription_ids.str_helper(1) +
                self._send_initial_values.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaTransferSubscriptionsRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_ids_size.str_helper(n+1) +
                self._subscription_ids.str_helper(n+1) +
                self._send_initial_values.str_helper(n+1))


# +++++++++++++++++++ UaChannelSecurityToken +++++++++++++++++++++++
class UaChannelSecurityToken(UaType):
    def __init__(self, val=ffi.new("UA_ChannelSecurityToken*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._channel_id = UaUInt32(val=val.channelId)
        self._token_id = UaUInt32(val=val.tokenId)
        self._created_at = UaDateTime(val=val.createdAt)
        self._revised_lifetime = UaUInt32(val=val.revisedLifetime)
    

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, val):
        self._channel_id = val
        self._value.channelId = val.value

    @property
    def token_id(self):
        return self._token_id

    @token_id.setter
    def token_id(self, val):
        self._token_id = val
        self._value.tokenId = val.value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, val):
        self._created_at = val
        self._value.createdAt = val.value

    @property
    def revised_lifetime(self):
        return self._revised_lifetime

    @revised_lifetime.setter
    def revised_lifetime(self, val):
        self._revised_lifetime = val
        self._value.revisedLifetime = val.value

    def __str__(self):
        return ("UaChannelSecurityToken:\n" + 
                self._channel_id.str_helper(1) +
                self._token_id.str_helper(1) +
                self._created_at.str_helper(1) +
                self._revised_lifetime.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaChannelSecurityToken:\n" + 
                self._channel_id.str_helper(n+1) +
                self._token_id.str_helper(n+1) +
                self._created_at.str_helper(n+1) +
                self._revised_lifetime.str_helper(n+1))


# +++++++++++++++++++ UaEventNotificationList +++++++++++++++++++++++
class UaEventNotificationList(UaType):
    def __init__(self, val=ffi.new("UA_EventNotificationList*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._events_size = SizeT(val=val.eventsSize)
        self._events = UaEventFieldList(val=val.events, is_pointer=True)
    

    @property
    def events_size(self):
        return self._events_size

    @events_size.setter
    def events_size(self, val):
        self._events_size = val
        self._value.eventsSize = val.value

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, val):
        self._events = val
        self._value.events = val.value

    def __str__(self):
        return ("UaEventNotificationList:\n" + 
                self._events_size.str_helper(1) +
                self._events.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaEventNotificationList:\n" + 
                self._events_size.str_helper(n+1) +
                self._events.str_helper(n+1))


# +++++++++++++++++++ UaAnonymousIdentityToken +++++++++++++++++++++++
class UaAnonymousIdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_AnonymousIdentityToken*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._policy_id = UaString(val=val.policyId)
    

    @property
    def policy_id(self):
        return self._policy_id

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val.value

    def __str__(self):
        return ("UaAnonymousIdentityToken:\n" + 
                self._policy_id.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAnonymousIdentityToken:\n" + 
                self._policy_id.str_helper(n+1))


# +++++++++++++++++++ UaAggregateFilter +++++++++++++++++++++++
class UaAggregateFilter(UaType):
    def __init__(self, val=ffi.new("UA_AggregateFilter*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._start_time = UaDateTime(val=val.startTime)
        self._aggregate_type = UaNodeId(val=val.aggregateType)
        self._processing_interval = UaDouble(val=val.processingInterval)
        self._aggregate_configuration = UaAggregateConfiguration(val=val.aggregateConfiguration)
    

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, val):
        self._start_time = val
        self._value.startTime = val.value

    @property
    def aggregate_type(self):
        return self._aggregate_type

    @aggregate_type.setter
    def aggregate_type(self, val):
        self._aggregate_type = val
        self._value.aggregateType = val.value

    @property
    def processing_interval(self):
        return self._processing_interval

    @processing_interval.setter
    def processing_interval(self, val):
        self._processing_interval = val
        self._value.processingInterval = val.value

    @property
    def aggregate_configuration(self):
        return self._aggregate_configuration

    @aggregate_configuration.setter
    def aggregate_configuration(self, val):
        self._aggregate_configuration = val
        self._value.aggregateConfiguration = val.value

    def __str__(self):
        return ("UaAggregateFilter:\n" + 
                self._start_time.str_helper(1) +
                self._aggregate_type.str_helper(1) +
                self._processing_interval.str_helper(1) +
                self._aggregate_configuration.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAggregateFilter:\n" + 
                self._start_time.str_helper(n+1) +
                self._aggregate_type.str_helper(n+1) +
                self._processing_interval.str_helper(n+1) +
                self._aggregate_configuration.str_helper(n+1))


# +++++++++++++++++++ UaRepublishResponse +++++++++++++++++++++++
class UaRepublishResponse(UaType):
    def __init__(self, val=ffi.new("UA_RepublishResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._notification_message = UaNotificationMessage(val=val.notificationMessage)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def notification_message(self):
        return self._notification_message

    @notification_message.setter
    def notification_message(self, val):
        self._notification_message = val
        self._value.notificationMessage = val.value

    def __str__(self):
        return ("UaRepublishResponse:\n" + 
                self._response_header.str_helper(1) +
                self._notification_message.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaRepublishResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._notification_message.str_helper(n+1))


# +++++++++++++++++++ UaDeleteSubscriptionsResponse +++++++++++++++++++++++
class UaDeleteSubscriptionsResponse(UaType):
    def __init__(self, val=ffi.new("UA_DeleteSubscriptionsResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaDeleteSubscriptionsResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteSubscriptionsResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaRegisterNodesRequest +++++++++++++++++++++++
class UaRegisterNodesRequest(UaType):
    def __init__(self, val=ffi.new("UA_RegisterNodesRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._nodes_to_register_size = SizeT(val=val.nodesToRegisterSize)
        self._nodes_to_register = UaNodeId(val=val.nodesToRegister, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def nodes_to_register_size(self):
        return self._nodes_to_register_size

    @nodes_to_register_size.setter
    def nodes_to_register_size(self, val):
        self._nodes_to_register_size = val
        self._value.nodesToRegisterSize = val.value

    @property
    def nodes_to_register(self):
        return self._nodes_to_register

    @nodes_to_register.setter
    def nodes_to_register(self, val):
        self._nodes_to_register = val
        self._value.nodesToRegister = val.value

    def __str__(self):
        return ("UaRegisterNodesRequest:\n" + 
                self._request_header.str_helper(1) +
                self._nodes_to_register_size.str_helper(1) +
                self._nodes_to_register.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaRegisterNodesRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._nodes_to_register_size.str_helper(n+1) +
                self._nodes_to_register.str_helper(n+1))


# +++++++++++++++++++ UaStructureDefinition +++++++++++++++++++++++
class UaStructureDefinition(UaType):
    def __init__(self, val=ffi.new("UA_StructureDefinition*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._default_encoding_id = UaNodeId(val=val.defaultEncodingId)
        self._base_data_type = UaNodeId(val=val.baseDataType)
        self._structure_type = UaStructureType(val=val.structureType)
        self._fields_size = SizeT(val=val.fieldsSize)
        self._fields = UaStructureField(val=val.fields, is_pointer=True)
    

    @property
    def default_encoding_id(self):
        return self._default_encoding_id

    @default_encoding_id.setter
    def default_encoding_id(self, val):
        self._default_encoding_id = val
        self._value.defaultEncodingId = val.value

    @property
    def base_data_type(self):
        return self._base_data_type

    @base_data_type.setter
    def base_data_type(self, val):
        self._base_data_type = val
        self._value.baseDataType = val.value

    @property
    def structure_type(self):
        return self._structure_type

    @structure_type.setter
    def structure_type(self, val):
        self._structure_type = val
        self._value.structureType = val.value

    @property
    def fields_size(self):
        return self._fields_size

    @fields_size.setter
    def fields_size(self, val):
        self._fields_size = val
        self._value.fieldsSize = val.value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, val):
        self._fields = val
        self._value.fields = val.value

    def __str__(self):
        return ("UaStructureDefinition:\n" + 
                self._default_encoding_id.str_helper(1) +
                self._base_data_type.str_helper(1) +
                self._structure_type.str_helper(1) +
                self._fields_size.str_helper(1) +
                self._fields.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaStructureDefinition:\n" + 
                self._default_encoding_id.str_helper(n+1) +
                self._base_data_type.str_helper(n+1) +
                self._structure_type.str_helper(n+1) +
                self._fields_size.str_helper(n+1) +
                self._fields.str_helper(n+1))


# +++++++++++++++++++ UaMethodAttributes +++++++++++++++++++++++
class UaMethodAttributes(UaType):
    def __init__(self, val=ffi.new("UA_MethodAttributes*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._specified_attributes = UaUInt32(val=val.specifiedAttributes)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._write_mask = UaUInt32(val=val.writeMask)
        self._user_write_mask = UaUInt32(val=val.userWriteMask)
        self._executable = UaBoolean(val=val.executable)
        self._user_executable = UaBoolean(val=val.userExecutable)
    

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def write_mask(self):
        return self._write_mask

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val.value

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val.value

    @property
    def executable(self):
        return self._executable

    @executable.setter
    def executable(self, val):
        self._executable = val
        self._value.executable = val.value

    @property
    def user_executable(self):
        return self._user_executable

    @user_executable.setter
    def user_executable(self, val):
        self._user_executable = val
        self._value.userExecutable = val.value

    def __str__(self):
        return ("UaMethodAttributes:\n" + 
                self._specified_attributes.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._write_mask.str_helper(1) +
                self._user_write_mask.str_helper(1) +
                self._executable.str_helper(1) +
                self._user_executable.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaMethodAttributes:\n" + 
                self._specified_attributes.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._write_mask.str_helper(n+1) +
                self._user_write_mask.str_helper(n+1) +
                self._executable.str_helper(n+1) +
                self._user_executable.str_helper(n+1))


# +++++++++++++++++++ UaUserNameIdentityToken +++++++++++++++++++++++
class UaUserNameIdentityToken(UaType):
    def __init__(self, val=ffi.new("UA_UserNameIdentityToken*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._policy_id = UaString(val=val.policyId)
        self._user_name = UaString(val=val.userName)
        self._password = UaByteString(val=val.password)
        self._encryption_algorithm = UaString(val=val.encryptionAlgorithm)
    

    @property
    def policy_id(self):
        return self._policy_id

    @policy_id.setter
    def policy_id(self, val):
        self._policy_id = val
        self._value.policyId = val.value

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, val):
        self._user_name = val
        self._value.userName = val.value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, val):
        self._password = val
        self._value.password = val.value

    @property
    def encryption_algorithm(self):
        return self._encryption_algorithm

    @encryption_algorithm.setter
    def encryption_algorithm(self, val):
        self._encryption_algorithm = val
        self._value.encryptionAlgorithm = val.value

    def __str__(self):
        return ("UaUserNameIdentityToken:\n" + 
                self._policy_id.str_helper(1) +
                self._user_name.str_helper(1) +
                self._password.str_helper(1) +
                self._encryption_algorithm.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaUserNameIdentityToken:\n" + 
                self._policy_id.str_helper(n+1) +
                self._user_name.str_helper(n+1) +
                self._password.str_helper(n+1) +
                self._encryption_algorithm.str_helper(n+1))


# +++++++++++++++++++ UaUnregisterNodesRequest +++++++++++++++++++++++
class UaUnregisterNodesRequest(UaType):
    def __init__(self, val=ffi.new("UA_UnregisterNodesRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._nodes_to_unregister_size = SizeT(val=val.nodesToUnregisterSize)
        self._nodes_to_unregister = UaNodeId(val=val.nodesToUnregister, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def nodes_to_unregister_size(self):
        return self._nodes_to_unregister_size

    @nodes_to_unregister_size.setter
    def nodes_to_unregister_size(self, val):
        self._nodes_to_unregister_size = val
        self._value.nodesToUnregisterSize = val.value

    @property
    def nodes_to_unregister(self):
        return self._nodes_to_unregister

    @nodes_to_unregister.setter
    def nodes_to_unregister(self, val):
        self._nodes_to_unregister = val
        self._value.nodesToUnregister = val.value

    def __str__(self):
        return ("UaUnregisterNodesRequest:\n" + 
                self._request_header.str_helper(1) +
                self._nodes_to_unregister_size.str_helper(1) +
                self._nodes_to_unregister.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaUnregisterNodesRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._nodes_to_unregister_size.str_helper(n+1) +
                self._nodes_to_unregister.str_helper(n+1))


# +++++++++++++++++++ UaOpenSecureChannelResponse +++++++++++++++++++++++
class UaOpenSecureChannelResponse(UaType):
    def __init__(self, val=ffi.new("UA_OpenSecureChannelResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._server_protocol_version = UaUInt32(val=val.serverProtocolVersion)
        self._security_token = UaChannelSecurityToken(val=val.securityToken)
        self._server_nonce = UaByteString(val=val.serverNonce)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def server_protocol_version(self):
        return self._server_protocol_version

    @server_protocol_version.setter
    def server_protocol_version(self, val):
        self._server_protocol_version = val
        self._value.serverProtocolVersion = val.value

    @property
    def security_token(self):
        return self._security_token

    @security_token.setter
    def security_token(self, val):
        self._security_token = val
        self._value.securityToken = val.value

    @property
    def server_nonce(self):
        return self._server_nonce

    @server_nonce.setter
    def server_nonce(self, val):
        self._server_nonce = val
        self._value.serverNonce = val.value

    def __str__(self):
        return ("UaOpenSecureChannelResponse:\n" + 
                self._response_header.str_helper(1) +
                self._server_protocol_version.str_helper(1) +
                self._security_token.str_helper(1) +
                self._server_nonce.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaOpenSecureChannelResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._server_protocol_version.str_helper(n+1) +
                self._security_token.str_helper(n+1) +
                self._server_nonce.str_helper(n+1))


# +++++++++++++++++++ UaSetTriggeringResponse +++++++++++++++++++++++
class UaSetTriggeringResponse(UaType):
    def __init__(self, val=ffi.new("UA_SetTriggeringResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._add_results_size = SizeT(val=val.addResultsSize)
        self._add_results = UaStatusCode(val=val.addResults, is_pointer=True)
        self._add_diagnostic_infos_size = SizeT(val=val.addDiagnosticInfosSize)
        self._add_diagnostic_infos = UaDiagnosticInfo(val=val.addDiagnosticInfos, is_pointer=True)
        self._remove_results_size = SizeT(val=val.removeResultsSize)
        self._remove_results = UaStatusCode(val=val.removeResults, is_pointer=True)
        self._remove_diagnostic_infos_size = SizeT(val=val.removeDiagnosticInfosSize)
        self._remove_diagnostic_infos = UaDiagnosticInfo(val=val.removeDiagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def add_results_size(self):
        return self._add_results_size

    @add_results_size.setter
    def add_results_size(self, val):
        self._add_results_size = val
        self._value.addResultsSize = val.value

    @property
    def add_results(self):
        return self._add_results

    @add_results.setter
    def add_results(self, val):
        self._add_results = val
        self._value.addResults = val.value

    @property
    def add_diagnostic_infos_size(self):
        return self._add_diagnostic_infos_size

    @add_diagnostic_infos_size.setter
    def add_diagnostic_infos_size(self, val):
        self._add_diagnostic_infos_size = val
        self._value.addDiagnosticInfosSize = val.value

    @property
    def add_diagnostic_infos(self):
        return self._add_diagnostic_infos

    @add_diagnostic_infos.setter
    def add_diagnostic_infos(self, val):
        self._add_diagnostic_infos = val
        self._value.addDiagnosticInfos = val.value

    @property
    def remove_results_size(self):
        return self._remove_results_size

    @remove_results_size.setter
    def remove_results_size(self, val):
        self._remove_results_size = val
        self._value.removeResultsSize = val.value

    @property
    def remove_results(self):
        return self._remove_results

    @remove_results.setter
    def remove_results(self, val):
        self._remove_results = val
        self._value.removeResults = val.value

    @property
    def remove_diagnostic_infos_size(self):
        return self._remove_diagnostic_infos_size

    @remove_diagnostic_infos_size.setter
    def remove_diagnostic_infos_size(self, val):
        self._remove_diagnostic_infos_size = val
        self._value.removeDiagnosticInfosSize = val.value

    @property
    def remove_diagnostic_infos(self):
        return self._remove_diagnostic_infos

    @remove_diagnostic_infos.setter
    def remove_diagnostic_infos(self, val):
        self._remove_diagnostic_infos = val
        self._value.removeDiagnosticInfos = val.value

    def __str__(self):
        return ("UaSetTriggeringResponse:\n" + 
                self._response_header.str_helper(1) +
                self._add_results_size.str_helper(1) +
                self._add_results.str_helper(1) +
                self._add_diagnostic_infos_size.str_helper(1) +
                self._add_diagnostic_infos.str_helper(1) +
                self._remove_results_size.str_helper(1) +
                self._remove_results.str_helper(1) +
                self._remove_diagnostic_infos_size.str_helper(1) +
                self._remove_diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSetTriggeringResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._add_results_size.str_helper(n+1) +
                self._add_results.str_helper(n+1) +
                self._add_diagnostic_infos_size.str_helper(n+1) +
                self._add_diagnostic_infos.str_helper(n+1) +
                self._remove_results_size.str_helper(n+1) +
                self._remove_results.str_helper(n+1) +
                self._remove_diagnostic_infos_size.str_helper(n+1) +
                self._remove_diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaSimpleAttributeOperand +++++++++++++++++++++++
class UaSimpleAttributeOperand(UaType):
    def __init__(self, val=ffi.new("UA_SimpleAttributeOperand*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._type_definition_id = UaNodeId(val=val.typeDefinitionId)
        self._browse_path_size = SizeT(val=val.browsePathSize)
        self._browse_path = UaQualifiedName(val=val.browsePath, is_pointer=True)
        self._attribute_id = UaUInt32(val=val.attributeId)
        self._index_range = UaString(val=val.indexRange)
    

    @property
    def type_definition_id(self):
        return self._type_definition_id

    @type_definition_id.setter
    def type_definition_id(self, val):
        self._type_definition_id = val
        self._value.typeDefinitionId = val.value

    @property
    def browse_path_size(self):
        return self._browse_path_size

    @browse_path_size.setter
    def browse_path_size(self, val):
        self._browse_path_size = val
        self._value.browsePathSize = val.value

    @property
    def browse_path(self):
        return self._browse_path

    @browse_path.setter
    def browse_path(self, val):
        self._browse_path = val
        self._value.browsePath = val.value

    @property
    def attribute_id(self):
        return self._attribute_id

    @attribute_id.setter
    def attribute_id(self, val):
        self._attribute_id = val
        self._value.attributeId = val.value

    @property
    def index_range(self):
        return self._index_range

    @index_range.setter
    def index_range(self, val):
        self._index_range = val
        self._value.indexRange = val.value

    def __str__(self):
        return ("UaSimpleAttributeOperand:\n" + 
                self._type_definition_id.str_helper(1) +
                self._browse_path_size.str_helper(1) +
                self._browse_path.str_helper(1) +
                self._attribute_id.str_helper(1) +
                self._index_range.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSimpleAttributeOperand:\n" + 
                self._type_definition_id.str_helper(n+1) +
                self._browse_path_size.str_helper(n+1) +
                self._browse_path.str_helper(n+1) +
                self._attribute_id.str_helper(n+1) +
                self._index_range.str_helper(n+1))


# +++++++++++++++++++ UaRepublishRequest +++++++++++++++++++++++
class UaRepublishRequest(UaType):
    def __init__(self, val=ffi.new("UA_RepublishRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._retransmit_sequence_number = UaUInt32(val=val.retransmitSequenceNumber)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def retransmit_sequence_number(self):
        return self._retransmit_sequence_number

    @retransmit_sequence_number.setter
    def retransmit_sequence_number(self, val):
        self._retransmit_sequence_number = val
        self._value.retransmitSequenceNumber = val.value

    def __str__(self):
        return ("UaRepublishRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_id.str_helper(1) +
                self._retransmit_sequence_number.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaRepublishRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_id.str_helper(n+1) +
                self._retransmit_sequence_number.str_helper(n+1))


# +++++++++++++++++++ UaRegisterNodesResponse +++++++++++++++++++++++
class UaRegisterNodesResponse(UaType):
    def __init__(self, val=ffi.new("UA_RegisterNodesResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._registered_node_ids_size = SizeT(val=val.registeredNodeIdsSize)
        self._registered_node_ids = UaNodeId(val=val.registeredNodeIds, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def registered_node_ids_size(self):
        return self._registered_node_ids_size

    @registered_node_ids_size.setter
    def registered_node_ids_size(self, val):
        self._registered_node_ids_size = val
        self._value.registeredNodeIdsSize = val.value

    @property
    def registered_node_ids(self):
        return self._registered_node_ids

    @registered_node_ids.setter
    def registered_node_ids(self, val):
        self._registered_node_ids = val
        self._value.registeredNodeIds = val.value

    def __str__(self):
        return ("UaRegisterNodesResponse:\n" + 
                self._response_header.str_helper(1) +
                self._registered_node_ids_size.str_helper(1) +
                self._registered_node_ids.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaRegisterNodesResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._registered_node_ids_size.str_helper(n+1) +
                self._registered_node_ids.str_helper(n+1))


# +++++++++++++++++++ UaModifyMonitoredItemsResponse +++++++++++++++++++++++
class UaModifyMonitoredItemsResponse(UaType):
    def __init__(self, val=ffi.new("UA_ModifyMonitoredItemsResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaMonitoredItemModifyResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaModifyMonitoredItemsResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaModifyMonitoredItemsResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaDeleteSubscriptionsRequest +++++++++++++++++++++++
class UaDeleteSubscriptionsRequest(UaType):
    def __init__(self, val=ffi.new("UA_DeleteSubscriptionsRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_ids_size = SizeT(val=val.subscriptionIdsSize)
        self._subscription_ids = UaUInt32(val=val.subscriptionIds, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_ids_size(self):
        return self._subscription_ids_size

    @subscription_ids_size.setter
    def subscription_ids_size(self, val):
        self._subscription_ids_size = val
        self._value.subscriptionIdsSize = val.value

    @property
    def subscription_ids(self):
        return self._subscription_ids

    @subscription_ids.setter
    def subscription_ids(self, val):
        self._subscription_ids = val
        self._value.subscriptionIds = val.value

    def __str__(self):
        return ("UaDeleteSubscriptionsRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_ids_size.str_helper(1) +
                self._subscription_ids.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteSubscriptionsRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_ids_size.str_helper(n+1) +
                self._subscription_ids.str_helper(n+1))


# +++++++++++++++++++ UaBrowsePath +++++++++++++++++++++++
class UaBrowsePath(UaType):
    def __init__(self, val=ffi.new("UA_BrowsePath*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._starting_node = UaNodeId(val=val.startingNode)
        self._relative_path = UaRelativePath(val=val.relativePath)
    

    @property
    def starting_node(self):
        return self._starting_node

    @starting_node.setter
    def starting_node(self, val):
        self._starting_node = val
        self._value.startingNode = val.value

    @property
    def relative_path(self):
        return self._relative_path

    @relative_path.setter
    def relative_path(self, val):
        self._relative_path = val
        self._value.relativePath = val.value

    def __str__(self):
        return ("UaBrowsePath:\n" + 
                self._starting_node.str_helper(1) +
                self._relative_path.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBrowsePath:\n" + 
                self._starting_node.str_helper(n+1) +
                self._relative_path.str_helper(n+1))


# +++++++++++++++++++ UaObjectAttributes +++++++++++++++++++++++
class UaObjectAttributes(UaType):
    def __init__(self, val=ffi.new("UA_ObjectAttributes*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._specified_attributes = UaUInt32(val=val.specifiedAttributes)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._description = UaLocalizedText(val=val.description)
        self._write_mask = UaUInt32(val=val.writeMask)
        self._user_write_mask = UaUInt32(val=val.userWriteMask)
        self._event_notifier = UaByte(val=val.eventNotifier)
    

    @property
    def specified_attributes(self):
        return self._specified_attributes

    @specified_attributes.setter
    def specified_attributes(self, val):
        self._specified_attributes = val
        self._value.specifiedAttributes = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val
        self._value.description = val.value

    @property
    def write_mask(self):
        return self._write_mask

    @write_mask.setter
    def write_mask(self, val):
        self._write_mask = val
        self._value.writeMask = val.value

    @property
    def user_write_mask(self):
        return self._user_write_mask

    @user_write_mask.setter
    def user_write_mask(self, val):
        self._user_write_mask = val
        self._value.userWriteMask = val.value

    @property
    def event_notifier(self):
        return self._event_notifier

    @event_notifier.setter
    def event_notifier(self, val):
        self._event_notifier = val
        self._value.eventNotifier = val.value

    def __str__(self):
        return ("UaObjectAttributes:\n" + 
                self._specified_attributes.str_helper(1) +
                self._display_name.str_helper(1) +
                self._description.str_helper(1) +
                self._write_mask.str_helper(1) +
                self._user_write_mask.str_helper(1) +
                self._event_notifier.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaObjectAttributes:\n" + 
                self._specified_attributes.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._description.str_helper(n+1) +
                self._write_mask.str_helper(n+1) +
                self._user_write_mask.str_helper(n+1) +
                self._event_notifier.str_helper(n+1))


# +++++++++++++++++++ UaPublishRequest +++++++++++++++++++++++
class UaPublishRequest(UaType):
    def __init__(self, val=ffi.new("UA_PublishRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_acknowledgements_size = SizeT(val=val.subscriptionAcknowledgementsSize)
        self._subscription_acknowledgements = UaSubscriptionAcknowledgement(val=val.subscriptionAcknowledgements, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_acknowledgements_size(self):
        return self._subscription_acknowledgements_size

    @subscription_acknowledgements_size.setter
    def subscription_acknowledgements_size(self, val):
        self._subscription_acknowledgements_size = val
        self._value.subscriptionAcknowledgementsSize = val.value

    @property
    def subscription_acknowledgements(self):
        return self._subscription_acknowledgements

    @subscription_acknowledgements.setter
    def subscription_acknowledgements(self, val):
        self._subscription_acknowledgements = val
        self._value.subscriptionAcknowledgements = val.value

    def __str__(self):
        return ("UaPublishRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_acknowledgements_size.str_helper(1) +
                self._subscription_acknowledgements.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaPublishRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_acknowledgements_size.str_helper(n+1) +
                self._subscription_acknowledgements.str_helper(n+1))


# +++++++++++++++++++ UaFindServersRequest +++++++++++++++++++++++
class UaFindServersRequest(UaType):
    def __init__(self, val=ffi.new("UA_FindServersRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._endpoint_url = UaString(val=val.endpointUrl)
        self._locale_ids_size = SizeT(val=val.localeIdsSize)
        self._locale_ids = UaString(val=val.localeIds, is_pointer=True)
        self._server_uris_size = SizeT(val=val.serverUrisSize)
        self._server_uris = UaString(val=val.serverUris, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, val):
        self._endpoint_url = val
        self._value.endpointUrl = val.value

    @property
    def locale_ids_size(self):
        return self._locale_ids_size

    @locale_ids_size.setter
    def locale_ids_size(self, val):
        self._locale_ids_size = val
        self._value.localeIdsSize = val.value

    @property
    def locale_ids(self):
        return self._locale_ids

    @locale_ids.setter
    def locale_ids(self, val):
        self._locale_ids = val
        self._value.localeIds = val.value

    @property
    def server_uris_size(self):
        return self._server_uris_size

    @server_uris_size.setter
    def server_uris_size(self, val):
        self._server_uris_size = val
        self._value.serverUrisSize = val.value

    @property
    def server_uris(self):
        return self._server_uris

    @server_uris.setter
    def server_uris(self, val):
        self._server_uris = val
        self._value.serverUris = val.value

    def __str__(self):
        return ("UaFindServersRequest:\n" + 
                self._request_header.str_helper(1) +
                self._endpoint_url.str_helper(1) +
                self._locale_ids_size.str_helper(1) +
                self._locale_ids.str_helper(1) +
                self._server_uris_size.str_helper(1) +
                self._server_uris.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaFindServersRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._endpoint_url.str_helper(n+1) +
                self._locale_ids_size.str_helper(n+1) +
                self._locale_ids.str_helper(n+1) +
                self._server_uris_size.str_helper(n+1) +
                self._server_uris.str_helper(n+1))


# +++++++++++++++++++ UaReferenceDescription +++++++++++++++++++++++
class UaReferenceDescription(UaType):
    def __init__(self, val=ffi.new("UA_ReferenceDescription*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId)
        self._is_forward = UaBoolean(val=val.isForward)
        self._node_id = UaExpandedNodeId(val=val.nodeId)
        self._browse_name = UaQualifiedName(val=val.browseName)
        self._display_name = UaLocalizedText(val=val.displayName)
        self._node_class = UaNodeClass(val=val.nodeClass)
        self._type_definition = UaExpandedNodeId(val=val.typeDefinition)
    

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val.value

    @property
    def is_forward(self):
        return self._is_forward

    @is_forward.setter
    def is_forward(self, val):
        self._is_forward = val
        self._value.isForward = val.value

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val.value

    @property
    def browse_name(self):
        return self._browse_name

    @browse_name.setter
    def browse_name(self, val):
        self._browse_name = val
        self._value.browseName = val.value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val
        self._value.displayName = val.value

    @property
    def node_class(self):
        return self._node_class

    @node_class.setter
    def node_class(self, val):
        self._node_class = val
        self._value.nodeClass = val.value

    @property
    def type_definition(self):
        return self._type_definition

    @type_definition.setter
    def type_definition(self, val):
        self._type_definition = val
        self._value.typeDefinition = val.value

    def __str__(self):
        return ("UaReferenceDescription:\n" + 
                self._reference_type_id.str_helper(1) +
                self._is_forward.str_helper(1) +
                self._node_id.str_helper(1) +
                self._browse_name.str_helper(1) +
                self._display_name.str_helper(1) +
                self._node_class.str_helper(1) +
                self._type_definition.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaReferenceDescription:\n" + 
                self._reference_type_id.str_helper(n+1) +
                self._is_forward.str_helper(n+1) +
                self._node_id.str_helper(n+1) +
                self._browse_name.str_helper(n+1) +
                self._display_name.str_helper(n+1) +
                self._node_class.str_helper(n+1) +
                self._type_definition.str_helper(n+1))


# +++++++++++++++++++ UaCreateSubscriptionRequest +++++++++++++++++++++++
class UaCreateSubscriptionRequest(UaType):
    def __init__(self, val=ffi.new("UA_CreateSubscriptionRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._requested_publishing_interval = UaDouble(val=val.requestedPublishingInterval)
        self._requested_lifetime_count = UaUInt32(val=val.requestedLifetimeCount)
        self._requested_max_keep_alive_count = UaUInt32(val=val.requestedMaxKeepAliveCount)
        self._max_notifications_per_publish = UaUInt32(val=val.maxNotificationsPerPublish)
        self._publishing_enabled = UaBoolean(val=val.publishingEnabled)
        self._priority = UaByte(val=val.priority)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def requested_publishing_interval(self):
        return self._requested_publishing_interval

    @requested_publishing_interval.setter
    def requested_publishing_interval(self, val):
        self._requested_publishing_interval = val
        self._value.requestedPublishingInterval = val.value

    @property
    def requested_lifetime_count(self):
        return self._requested_lifetime_count

    @requested_lifetime_count.setter
    def requested_lifetime_count(self, val):
        self._requested_lifetime_count = val
        self._value.requestedLifetimeCount = val.value

    @property
    def requested_max_keep_alive_count(self):
        return self._requested_max_keep_alive_count

    @requested_max_keep_alive_count.setter
    def requested_max_keep_alive_count(self, val):
        self._requested_max_keep_alive_count = val
        self._value.requestedMaxKeepAliveCount = val.value

    @property
    def max_notifications_per_publish(self):
        return self._max_notifications_per_publish

    @max_notifications_per_publish.setter
    def max_notifications_per_publish(self, val):
        self._max_notifications_per_publish = val
        self._value.maxNotificationsPerPublish = val.value

    @property
    def publishing_enabled(self):
        return self._publishing_enabled

    @publishing_enabled.setter
    def publishing_enabled(self, val):
        self._publishing_enabled = val
        self._value.publishingEnabled = val.value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, val):
        self._priority = val
        self._value.priority = val.value

    def __str__(self):
        return ("UaCreateSubscriptionRequest:\n" + 
                self._request_header.str_helper(1) +
                self._requested_publishing_interval.str_helper(1) +
                self._requested_lifetime_count.str_helper(1) +
                self._requested_max_keep_alive_count.str_helper(1) +
                self._max_notifications_per_publish.str_helper(1) +
                self._publishing_enabled.str_helper(1) +
                self._priority.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCreateSubscriptionRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._requested_publishing_interval.str_helper(n+1) +
                self._requested_lifetime_count.str_helper(n+1) +
                self._requested_max_keep_alive_count.str_helper(n+1) +
                self._max_notifications_per_publish.str_helper(n+1) +
                self._publishing_enabled.str_helper(n+1) +
                self._priority.str_helper(n+1))


# +++++++++++++++++++ UaCallResponse +++++++++++++++++++++++
class UaCallResponse(UaType):
    def __init__(self, val=ffi.new("UA_CallResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaCallMethodResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaCallResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCallResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaDeleteNodesResponse +++++++++++++++++++++++
class UaDeleteNodesResponse(UaType):
    def __init__(self, val=ffi.new("UA_DeleteNodesResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaDeleteNodesResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteNodesResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaModifyMonitoredItemsRequest +++++++++++++++++++++++
class UaModifyMonitoredItemsRequest(UaType):
    def __init__(self, val=ffi.new("UA_ModifyMonitoredItemsRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._timestamps_to_return = UaTimestampsToReturn(val=val.timestampsToReturn)
        self._items_to_modify_size = SizeT(val=val.itemsToModifySize)
        self._items_to_modify = UaMonitoredItemModifyRequest(val=val.itemsToModify, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def timestamps_to_return(self):
        return self._timestamps_to_return

    @timestamps_to_return.setter
    def timestamps_to_return(self, val):
        self._timestamps_to_return = val
        self._value.timestampsToReturn = val.value

    @property
    def items_to_modify_size(self):
        return self._items_to_modify_size

    @items_to_modify_size.setter
    def items_to_modify_size(self, val):
        self._items_to_modify_size = val
        self._value.itemsToModifySize = val.value

    @property
    def items_to_modify(self):
        return self._items_to_modify

    @items_to_modify.setter
    def items_to_modify(self, val):
        self._items_to_modify = val
        self._value.itemsToModify = val.value

    def __str__(self):
        return ("UaModifyMonitoredItemsRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_id.str_helper(1) +
                self._timestamps_to_return.str_helper(1) +
                self._items_to_modify_size.str_helper(1) +
                self._items_to_modify.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaModifyMonitoredItemsRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_id.str_helper(n+1) +
                self._timestamps_to_return.str_helper(n+1) +
                self._items_to_modify_size.str_helper(n+1) +
                self._items_to_modify.str_helper(n+1))


# +++++++++++++++++++ UaServiceFault +++++++++++++++++++++++
class UaServiceFault(UaType):
    def __init__(self, val=ffi.new("UA_ServiceFault*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    def __str__(self):
        return ("UaServiceFault:\n" + 
                self._response_header.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaServiceFault:\n" + 
                self._response_header.str_helper(n+1))


# +++++++++++++++++++ UaPublishResponse +++++++++++++++++++++++
class UaPublishResponse(UaType):
    def __init__(self, val=ffi.new("UA_PublishResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._available_sequence_numbers_size = SizeT(val=val.availableSequenceNumbersSize)
        self._available_sequence_numbers = UaUInt32(val=val.availableSequenceNumbers, is_pointer=True)
        self._more_notifications = UaBoolean(val=val.moreNotifications)
        self._notification_message = UaNotificationMessage(val=val.notificationMessage)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaStatusCode(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def available_sequence_numbers_size(self):
        return self._available_sequence_numbers_size

    @available_sequence_numbers_size.setter
    def available_sequence_numbers_size(self, val):
        self._available_sequence_numbers_size = val
        self._value.availableSequenceNumbersSize = val.value

    @property
    def available_sequence_numbers(self):
        return self._available_sequence_numbers

    @available_sequence_numbers.setter
    def available_sequence_numbers(self, val):
        self._available_sequence_numbers = val
        self._value.availableSequenceNumbers = val.value

    @property
    def more_notifications(self):
        return self._more_notifications

    @more_notifications.setter
    def more_notifications(self, val):
        self._more_notifications = val
        self._value.moreNotifications = val.value

    @property
    def notification_message(self):
        return self._notification_message

    @notification_message.setter
    def notification_message(self, val):
        self._notification_message = val
        self._value.notificationMessage = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaPublishResponse:\n" + 
                self._response_header.str_helper(1) +
                self._subscription_id.str_helper(1) +
                self._available_sequence_numbers_size.str_helper(1) +
                self._available_sequence_numbers.str_helper(1) +
                self._more_notifications.str_helper(1) +
                self._notification_message.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaPublishResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._subscription_id.str_helper(n+1) +
                self._available_sequence_numbers_size.str_helper(n+1) +
                self._available_sequence_numbers.str_helper(n+1) +
                self._more_notifications.str_helper(n+1) +
                self._notification_message.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaCreateMonitoredItemsRequest +++++++++++++++++++++++
class UaCreateMonitoredItemsRequest(UaType):
    def __init__(self, val=ffi.new("UA_CreateMonitoredItemsRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._timestamps_to_return = UaTimestampsToReturn(val=val.timestampsToReturn)
        self._items_to_create_size = SizeT(val=val.itemsToCreateSize)
        self._items_to_create = UaMonitoredItemCreateRequest(val=val.itemsToCreate, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def timestamps_to_return(self):
        return self._timestamps_to_return

    @timestamps_to_return.setter
    def timestamps_to_return(self, val):
        self._timestamps_to_return = val
        self._value.timestampsToReturn = val.value

    @property
    def items_to_create_size(self):
        return self._items_to_create_size

    @items_to_create_size.setter
    def items_to_create_size(self, val):
        self._items_to_create_size = val
        self._value.itemsToCreateSize = val.value

    @property
    def items_to_create(self):
        return self._items_to_create

    @items_to_create.setter
    def items_to_create(self, val):
        self._items_to_create = val
        self._value.itemsToCreate = val.value

    def __str__(self):
        return ("UaCreateMonitoredItemsRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_id.str_helper(1) +
                self._timestamps_to_return.str_helper(1) +
                self._items_to_create_size.str_helper(1) +
                self._items_to_create.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCreateMonitoredItemsRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_id.str_helper(n+1) +
                self._timestamps_to_return.str_helper(n+1) +
                self._items_to_create_size.str_helper(n+1) +
                self._items_to_create.str_helper(n+1))


# +++++++++++++++++++ UaOpenSecureChannelRequest +++++++++++++++++++++++
class UaOpenSecureChannelRequest(UaType):
    def __init__(self, val=ffi.new("UA_OpenSecureChannelRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._client_protocol_version = UaUInt32(val=val.clientProtocolVersion)
        self._request_type = UaSecurityTokenRequestType(val=val.requestType)
        self._security_mode = UaMessageSecurityMode(val=val.securityMode)
        self._client_nonce = UaByteString(val=val.clientNonce)
        self._requested_lifetime = UaUInt32(val=val.requestedLifetime)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def client_protocol_version(self):
        return self._client_protocol_version

    @client_protocol_version.setter
    def client_protocol_version(self, val):
        self._client_protocol_version = val
        self._value.clientProtocolVersion = val.value

    @property
    def request_type(self):
        return self._request_type

    @request_type.setter
    def request_type(self, val):
        self._request_type = val
        self._value.requestType = val.value

    @property
    def security_mode(self):
        return self._security_mode

    @security_mode.setter
    def security_mode(self, val):
        self._security_mode = val
        self._value.securityMode = val.value

    @property
    def client_nonce(self):
        return self._client_nonce

    @client_nonce.setter
    def client_nonce(self, val):
        self._client_nonce = val
        self._value.clientNonce = val.value

    @property
    def requested_lifetime(self):
        return self._requested_lifetime

    @requested_lifetime.setter
    def requested_lifetime(self, val):
        self._requested_lifetime = val
        self._value.requestedLifetime = val.value

    def __str__(self):
        return ("UaOpenSecureChannelRequest:\n" + 
                self._request_header.str_helper(1) +
                self._client_protocol_version.str_helper(1) +
                self._request_type.str_helper(1) +
                self._security_mode.str_helper(1) +
                self._client_nonce.str_helper(1) +
                self._requested_lifetime.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaOpenSecureChannelRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._client_protocol_version.str_helper(n+1) +
                self._request_type.str_helper(n+1) +
                self._security_mode.str_helper(n+1) +
                self._client_nonce.str_helper(n+1) +
                self._requested_lifetime.str_helper(n+1))


# +++++++++++++++++++ UaCloseSessionRequest +++++++++++++++++++++++
class UaCloseSessionRequest(UaType):
    def __init__(self, val=ffi.new("UA_CloseSessionRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._delete_subscriptions = UaBoolean(val=val.deleteSubscriptions)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def delete_subscriptions(self):
        return self._delete_subscriptions

    @delete_subscriptions.setter
    def delete_subscriptions(self, val):
        self._delete_subscriptions = val
        self._value.deleteSubscriptions = val.value

    def __str__(self):
        return ("UaCloseSessionRequest:\n" + 
                self._request_header.str_helper(1) +
                self._delete_subscriptions.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCloseSessionRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._delete_subscriptions.str_helper(n+1))


# +++++++++++++++++++ UaSetTriggeringRequest +++++++++++++++++++++++
class UaSetTriggeringRequest(UaType):
    def __init__(self, val=ffi.new("UA_SetTriggeringRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._subscription_id = UaUInt32(val=val.subscriptionId)
        self._triggering_item_id = UaUInt32(val=val.triggeringItemId)
        self._links_to_add_size = SizeT(val=val.linksToAddSize)
        self._links_to_add = UaUInt32(val=val.linksToAdd, is_pointer=True)
        self._links_to_remove_size = SizeT(val=val.linksToRemoveSize)
        self._links_to_remove = UaUInt32(val=val.linksToRemove, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def subscription_id(self):
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, val):
        self._subscription_id = val
        self._value.subscriptionId = val.value

    @property
    def triggering_item_id(self):
        return self._triggering_item_id

    @triggering_item_id.setter
    def triggering_item_id(self, val):
        self._triggering_item_id = val
        self._value.triggeringItemId = val.value

    @property
    def links_to_add_size(self):
        return self._links_to_add_size

    @links_to_add_size.setter
    def links_to_add_size(self, val):
        self._links_to_add_size = val
        self._value.linksToAddSize = val.value

    @property
    def links_to_add(self):
        return self._links_to_add

    @links_to_add.setter
    def links_to_add(self, val):
        self._links_to_add = val
        self._value.linksToAdd = val.value

    @property
    def links_to_remove_size(self):
        return self._links_to_remove_size

    @links_to_remove_size.setter
    def links_to_remove_size(self, val):
        self._links_to_remove_size = val
        self._value.linksToRemoveSize = val.value

    @property
    def links_to_remove(self):
        return self._links_to_remove

    @links_to_remove.setter
    def links_to_remove(self, val):
        self._links_to_remove = val
        self._value.linksToRemove = val.value

    def __str__(self):
        return ("UaSetTriggeringRequest:\n" + 
                self._request_header.str_helper(1) +
                self._subscription_id.str_helper(1) +
                self._triggering_item_id.str_helper(1) +
                self._links_to_add_size.str_helper(1) +
                self._links_to_add.str_helper(1) +
                self._links_to_remove_size.str_helper(1) +
                self._links_to_remove.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaSetTriggeringRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._subscription_id.str_helper(n+1) +
                self._triggering_item_id.str_helper(n+1) +
                self._links_to_add_size.str_helper(n+1) +
                self._links_to_add.str_helper(n+1) +
                self._links_to_remove_size.str_helper(n+1) +
                self._links_to_remove.str_helper(n+1))


# +++++++++++++++++++ UaBrowseResult +++++++++++++++++++++++
class UaBrowseResult(UaType):
    def __init__(self, val=ffi.new("UA_BrowseResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._status_code = UaStatusCode(val=val.statusCode)
        self._continuation_point = UaByteString(val=val.continuationPoint)
        self._references_size = SizeT(val=val.referencesSize)
        self._references = UaReferenceDescription(val=val.references, is_pointer=True)
    

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val.value

    @property
    def continuation_point(self):
        return self._continuation_point

    @continuation_point.setter
    def continuation_point(self, val):
        self._continuation_point = val
        self._value.continuationPoint = val.value

    @property
    def references_size(self):
        return self._references_size

    @references_size.setter
    def references_size(self, val):
        self._references_size = val
        self._value.referencesSize = val.value

    @property
    def references(self):
        return self._references

    @references.setter
    def references(self, val):
        self._references = val
        self._value.references = val.value

    def __str__(self):
        return ("UaBrowseResult:\n" + 
                self._status_code.str_helper(1) +
                self._continuation_point.str_helper(1) +
                self._references_size.str_helper(1) +
                self._references.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBrowseResult:\n" + 
                self._status_code.str_helper(n+1) +
                self._continuation_point.str_helper(n+1) +
                self._references_size.str_helper(n+1) +
                self._references.str_helper(n+1))


# +++++++++++++++++++ UaAddReferencesRequest +++++++++++++++++++++++
class UaAddReferencesRequest(UaType):
    def __init__(self, val=ffi.new("UA_AddReferencesRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._references_to_add_size = SizeT(val=val.referencesToAddSize)
        self._references_to_add = UaAddReferencesItem(val=val.referencesToAdd, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def references_to_add_size(self):
        return self._references_to_add_size

    @references_to_add_size.setter
    def references_to_add_size(self, val):
        self._references_to_add_size = val
        self._value.referencesToAddSize = val.value

    @property
    def references_to_add(self):
        return self._references_to_add

    @references_to_add.setter
    def references_to_add(self, val):
        self._references_to_add = val
        self._value.referencesToAdd = val.value

    def __str__(self):
        return ("UaAddReferencesRequest:\n" + 
                self._request_header.str_helper(1) +
                self._references_to_add_size.str_helper(1) +
                self._references_to_add.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAddReferencesRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._references_to_add_size.str_helper(n+1) +
                self._references_to_add.str_helper(n+1))


# +++++++++++++++++++ UaAddNodesItem +++++++++++++++++++++++
class UaAddNodesItem(UaType):
    def __init__(self, val=ffi.new("UA_AddNodesItem*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._parent_node_id = UaExpandedNodeId(val=val.parentNodeId)
        self._reference_type_id = UaNodeId(val=val.referenceTypeId)
        self._requested_new_node_id = UaExpandedNodeId(val=val.requestedNewNodeId)
        self._browse_name = UaQualifiedName(val=val.browseName)
        self._node_class = UaNodeClass(val=val.nodeClass)
        self._node_attributes = UaExtensionObject(val=val.nodeAttributes)
        self._type_definition = UaExpandedNodeId(val=val.typeDefinition)
    

    @property
    def parent_node_id(self):
        return self._parent_node_id

    @parent_node_id.setter
    def parent_node_id(self, val):
        self._parent_node_id = val
        self._value.parentNodeId = val.value

    @property
    def reference_type_id(self):
        return self._reference_type_id

    @reference_type_id.setter
    def reference_type_id(self, val):
        self._reference_type_id = val
        self._value.referenceTypeId = val.value

    @property
    def requested_new_node_id(self):
        return self._requested_new_node_id

    @requested_new_node_id.setter
    def requested_new_node_id(self, val):
        self._requested_new_node_id = val
        self._value.requestedNewNodeId = val.value

    @property
    def browse_name(self):
        return self._browse_name

    @browse_name.setter
    def browse_name(self, val):
        self._browse_name = val
        self._value.browseName = val.value

    @property
    def node_class(self):
        return self._node_class

    @node_class.setter
    def node_class(self, val):
        self._node_class = val
        self._value.nodeClass = val.value

    @property
    def node_attributes(self):
        return self._node_attributes

    @node_attributes.setter
    def node_attributes(self, val):
        self._node_attributes = val
        self._value.nodeAttributes = val.value

    @property
    def type_definition(self):
        return self._type_definition

    @type_definition.setter
    def type_definition(self, val):
        self._type_definition = val
        self._value.typeDefinition = val.value

    def __str__(self):
        return ("UaAddNodesItem:\n" + 
                self._parent_node_id.str_helper(1) +
                self._reference_type_id.str_helper(1) +
                self._requested_new_node_id.str_helper(1) +
                self._browse_name.str_helper(1) +
                self._node_class.str_helper(1) +
                self._node_attributes.str_helper(1) +
                self._type_definition.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAddNodesItem:\n" + 
                self._parent_node_id.str_helper(n+1) +
                self._reference_type_id.str_helper(n+1) +
                self._requested_new_node_id.str_helper(n+1) +
                self._browse_name.str_helper(n+1) +
                self._node_class.str_helper(n+1) +
                self._node_attributes.str_helper(n+1) +
                self._type_definition.str_helper(n+1))


# +++++++++++++++++++ UaServerStatusDataType +++++++++++++++++++++++
class UaServerStatusDataType(UaType):
    def __init__(self, val=ffi.new("UA_ServerStatusDataType*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._start_time = UaDateTime(val=val.startTime)
        self._current_time = UaDateTime(val=val.currentTime)
        self._state = UaServerState(val=val.state)
        self._build_info = UaBuildInfo(val=val.buildInfo)
        self._seconds_till_shutdown = UaUInt32(val=val.secondsTillShutdown)
        self._shutdown_reason = UaLocalizedText(val=val.shutdownReason)
    

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, val):
        self._start_time = val
        self._value.startTime = val.value

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, val):
        self._current_time = val
        self._value.currentTime = val.value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val
        self._value.state = val.value

    @property
    def build_info(self):
        return self._build_info

    @build_info.setter
    def build_info(self, val):
        self._build_info = val
        self._value.buildInfo = val.value

    @property
    def seconds_till_shutdown(self):
        return self._seconds_till_shutdown

    @seconds_till_shutdown.setter
    def seconds_till_shutdown(self, val):
        self._seconds_till_shutdown = val
        self._value.secondsTillShutdown = val.value

    @property
    def shutdown_reason(self):
        return self._shutdown_reason

    @shutdown_reason.setter
    def shutdown_reason(self, val):
        self._shutdown_reason = val
        self._value.shutdownReason = val.value

    def __str__(self):
        return ("UaServerStatusDataType:\n" + 
                self._start_time.str_helper(1) +
                self._current_time.str_helper(1) +
                self._state.str_helper(1) +
                self._build_info.str_helper(1) +
                self._seconds_till_shutdown.str_helper(1) +
                self._shutdown_reason.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaServerStatusDataType:\n" + 
                self._start_time.str_helper(n+1) +
                self._current_time.str_helper(n+1) +
                self._state.str_helper(n+1) +
                self._build_info.str_helper(n+1) +
                self._seconds_till_shutdown.str_helper(n+1) +
                self._shutdown_reason.str_helper(n+1))


# +++++++++++++++++++ UaBrowseNextResponse +++++++++++++++++++++++
class UaBrowseNextResponse(UaType):
    def __init__(self, val=ffi.new("UA_BrowseNextResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaBrowseResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaBrowseNextResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBrowseNextResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaAxisInformation +++++++++++++++++++++++
class UaAxisInformation(UaType):
    def __init__(self, val=ffi.new("UA_AxisInformation*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._engineering_units = UaEUInformation(val=val.engineeringUnits)
        self._e_u_range = UaRange(val=val.eURange)
        self._title = UaLocalizedText(val=val.title)
        self._axis_scale_type = UaAxisScaleEnumeration(val=val.axisScaleType)
        self._axis_steps_size = SizeT(val=val.axisStepsSize)
        self._axis_steps = UaDouble(val=val.axisSteps, is_pointer=True)
    

    @property
    def engineering_units(self):
        return self._engineering_units

    @engineering_units.setter
    def engineering_units(self, val):
        self._engineering_units = val
        self._value.engineeringUnits = val.value

    @property
    def e_u_range(self):
        return self._e_u_range

    @e_u_range.setter
    def e_u_range(self, val):
        self._e_u_range = val
        self._value.eURange = val.value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self._value.title = val.value

    @property
    def axis_scale_type(self):
        return self._axis_scale_type

    @axis_scale_type.setter
    def axis_scale_type(self, val):
        self._axis_scale_type = val
        self._value.axisScaleType = val.value

    @property
    def axis_steps_size(self):
        return self._axis_steps_size

    @axis_steps_size.setter
    def axis_steps_size(self, val):
        self._axis_steps_size = val
        self._value.axisStepsSize = val.value

    @property
    def axis_steps(self):
        return self._axis_steps

    @axis_steps.setter
    def axis_steps(self, val):
        self._axis_steps = val
        self._value.axisSteps = val.value

    def __str__(self):
        return ("UaAxisInformation:\n" + 
                self._engineering_units.str_helper(1) +
                self._e_u_range.str_helper(1) +
                self._title.str_helper(1) +
                self._axis_scale_type.str_helper(1) +
                self._axis_steps_size.str_helper(1) +
                self._axis_steps.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAxisInformation:\n" + 
                self._engineering_units.str_helper(n+1) +
                self._e_u_range.str_helper(n+1) +
                self._title.str_helper(n+1) +
                self._axis_scale_type.str_helper(n+1) +
                self._axis_steps_size.str_helper(n+1) +
                self._axis_steps.str_helper(n+1))


# +++++++++++++++++++ UaApplicationDescription +++++++++++++++++++++++
class UaApplicationDescription(UaType):
    def __init__(self, val=ffi.new("UA_ApplicationDescription*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._application_uri = UaString(val=val.applicationUri)
        self._product_uri = UaString(val=val.productUri)
        self._application_name = UaLocalizedText(val=val.applicationName)
        self._application_type = UaApplicationType(val=val.applicationType)
        self._gateway_server_uri = UaString(val=val.gatewayServerUri)
        self._discovery_profile_uri = UaString(val=val.discoveryProfileUri)
        self._discovery_urls_size = SizeT(val=val.discoveryUrlsSize)
        self._discovery_urls = UaString(val=val.discoveryUrls, is_pointer=True)
    

    @property
    def application_uri(self):
        return self._application_uri

    @application_uri.setter
    def application_uri(self, val):
        self._application_uri = val
        self._value.applicationUri = val.value

    @property
    def product_uri(self):
        return self._product_uri

    @product_uri.setter
    def product_uri(self, val):
        self._product_uri = val
        self._value.productUri = val.value

    @property
    def application_name(self):
        return self._application_name

    @application_name.setter
    def application_name(self, val):
        self._application_name = val
        self._value.applicationName = val.value

    @property
    def application_type(self):
        return self._application_type

    @application_type.setter
    def application_type(self, val):
        self._application_type = val
        self._value.applicationType = val.value

    @property
    def gateway_server_uri(self):
        return self._gateway_server_uri

    @gateway_server_uri.setter
    def gateway_server_uri(self, val):
        self._gateway_server_uri = val
        self._value.gatewayServerUri = val.value

    @property
    def discovery_profile_uri(self):
        return self._discovery_profile_uri

    @discovery_profile_uri.setter
    def discovery_profile_uri(self, val):
        self._discovery_profile_uri = val
        self._value.discoveryProfileUri = val.value

    @property
    def discovery_urls_size(self):
        return self._discovery_urls_size

    @discovery_urls_size.setter
    def discovery_urls_size(self, val):
        self._discovery_urls_size = val
        self._value.discoveryUrlsSize = val.value

    @property
    def discovery_urls(self):
        return self._discovery_urls

    @discovery_urls.setter
    def discovery_urls(self, val):
        self._discovery_urls = val
        self._value.discoveryUrls = val.value

    def __str__(self):
        return ("UaApplicationDescription:\n" + 
                self._application_uri.str_helper(1) +
                self._product_uri.str_helper(1) +
                self._application_name.str_helper(1) +
                self._application_type.str_helper(1) +
                self._gateway_server_uri.str_helper(1) +
                self._discovery_profile_uri.str_helper(1) +
                self._discovery_urls_size.str_helper(1) +
                self._discovery_urls.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaApplicationDescription:\n" + 
                self._application_uri.str_helper(n+1) +
                self._product_uri.str_helper(n+1) +
                self._application_name.str_helper(n+1) +
                self._application_type.str_helper(n+1) +
                self._gateway_server_uri.str_helper(n+1) +
                self._discovery_profile_uri.str_helper(n+1) +
                self._discovery_urls_size.str_helper(n+1) +
                self._discovery_urls.str_helper(n+1))


# +++++++++++++++++++ UaReadRequest +++++++++++++++++++++++
class UaReadRequest(UaType):
    def __init__(self, val=ffi.new("UA_ReadRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._max_age = UaDouble(val=val.maxAge)
        self._timestamps_to_return = UaTimestampsToReturn(val=val.timestampsToReturn)
        self._nodes_to_read_size = SizeT(val=val.nodesToReadSize)
        self._nodes_to_read = UaReadValueId(val=val.nodesToRead, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def max_age(self):
        return self._max_age

    @max_age.setter
    def max_age(self, val):
        self._max_age = val
        self._value.maxAge = val.value

    @property
    def timestamps_to_return(self):
        return self._timestamps_to_return

    @timestamps_to_return.setter
    def timestamps_to_return(self, val):
        self._timestamps_to_return = val
        self._value.timestampsToReturn = val.value

    @property
    def nodes_to_read_size(self):
        return self._nodes_to_read_size

    @nodes_to_read_size.setter
    def nodes_to_read_size(self, val):
        self._nodes_to_read_size = val
        self._value.nodesToReadSize = val.value

    @property
    def nodes_to_read(self):
        return self._nodes_to_read

    @nodes_to_read.setter
    def nodes_to_read(self, val):
        self._nodes_to_read = val
        self._value.nodesToRead = val.value

    def __str__(self):
        return ("UaReadRequest:\n" + 
                self._request_header.str_helper(1) +
                self._max_age.str_helper(1) +
                self._timestamps_to_return.str_helper(1) +
                self._nodes_to_read_size.str_helper(1) +
                self._nodes_to_read.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaReadRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._max_age.str_helper(n+1) +
                self._timestamps_to_return.str_helper(n+1) +
                self._nodes_to_read_size.str_helper(n+1) +
                self._nodes_to_read.str_helper(n+1))


# +++++++++++++++++++ UaActivateSessionRequest +++++++++++++++++++++++
class UaActivateSessionRequest(UaType):
    def __init__(self, val=ffi.new("UA_ActivateSessionRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._client_signature = UaSignatureData(val=val.clientSignature)
        self._client_software_certificates_size = SizeT(val=val.clientSoftwareCertificatesSize)
        self._client_software_certificates = UaSignedSoftwareCertificate(val=val.clientSoftwareCertificates, is_pointer=True)
        self._locale_ids_size = SizeT(val=val.localeIdsSize)
        self._locale_ids = UaString(val=val.localeIds, is_pointer=True)
        self._user_identity_token = UaExtensionObject(val=val.userIdentityToken)
        self._user_token_signature = UaSignatureData(val=val.userTokenSignature)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def client_signature(self):
        return self._client_signature

    @client_signature.setter
    def client_signature(self, val):
        self._client_signature = val
        self._value.clientSignature = val.value

    @property
    def client_software_certificates_size(self):
        return self._client_software_certificates_size

    @client_software_certificates_size.setter
    def client_software_certificates_size(self, val):
        self._client_software_certificates_size = val
        self._value.clientSoftwareCertificatesSize = val.value

    @property
    def client_software_certificates(self):
        return self._client_software_certificates

    @client_software_certificates.setter
    def client_software_certificates(self, val):
        self._client_software_certificates = val
        self._value.clientSoftwareCertificates = val.value

    @property
    def locale_ids_size(self):
        return self._locale_ids_size

    @locale_ids_size.setter
    def locale_ids_size(self, val):
        self._locale_ids_size = val
        self._value.localeIdsSize = val.value

    @property
    def locale_ids(self):
        return self._locale_ids

    @locale_ids.setter
    def locale_ids(self, val):
        self._locale_ids = val
        self._value.localeIds = val.value

    @property
    def user_identity_token(self):
        return self._user_identity_token

    @user_identity_token.setter
    def user_identity_token(self, val):
        self._user_identity_token = val
        self._value.userIdentityToken = val.value

    @property
    def user_token_signature(self):
        return self._user_token_signature

    @user_token_signature.setter
    def user_token_signature(self, val):
        self._user_token_signature = val
        self._value.userTokenSignature = val.value

    def __str__(self):
        return ("UaActivateSessionRequest:\n" + 
                self._request_header.str_helper(1) +
                self._client_signature.str_helper(1) +
                self._client_software_certificates_size.str_helper(1) +
                self._client_software_certificates.str_helper(1) +
                self._locale_ids_size.str_helper(1) +
                self._locale_ids.str_helper(1) +
                self._user_identity_token.str_helper(1) +
                self._user_token_signature.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaActivateSessionRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._client_signature.str_helper(n+1) +
                self._client_software_certificates_size.str_helper(n+1) +
                self._client_software_certificates.str_helper(n+1) +
                self._locale_ids_size.str_helper(n+1) +
                self._locale_ids.str_helper(n+1) +
                self._user_identity_token.str_helper(n+1) +
                self._user_token_signature.str_helper(n+1))


# +++++++++++++++++++ UaBrowsePathResult +++++++++++++++++++++++
class UaBrowsePathResult(UaType):
    def __init__(self, val=ffi.new("UA_BrowsePathResult*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._status_code = UaStatusCode(val=val.statusCode)
        self._targets_size = SizeT(val=val.targetsSize)
        self._targets = UaBrowsePathTarget(val=val.targets, is_pointer=True)
    

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        self._status_code = val
        self._value.statusCode = val.value

    @property
    def targets_size(self):
        return self._targets_size

    @targets_size.setter
    def targets_size(self, val):
        self._targets_size = val
        self._value.targetsSize = val.value

    @property
    def targets(self):
        return self._targets

    @targets.setter
    def targets(self, val):
        self._targets = val
        self._value.targets = val.value

    def __str__(self):
        return ("UaBrowsePathResult:\n" + 
                self._status_code.str_helper(1) +
                self._targets_size.str_helper(1) +
                self._targets.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBrowsePathResult:\n" + 
                self._status_code.str_helper(n+1) +
                self._targets_size.str_helper(n+1) +
                self._targets.str_helper(n+1))


# +++++++++++++++++++ UaAddNodesRequest +++++++++++++++++++++++
class UaAddNodesRequest(UaType):
    def __init__(self, val=ffi.new("UA_AddNodesRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._nodes_to_add_size = SizeT(val=val.nodesToAddSize)
        self._nodes_to_add = UaAddNodesItem(val=val.nodesToAdd, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def nodes_to_add_size(self):
        return self._nodes_to_add_size

    @nodes_to_add_size.setter
    def nodes_to_add_size(self, val):
        self._nodes_to_add_size = val
        self._value.nodesToAddSize = val.value

    @property
    def nodes_to_add(self):
        return self._nodes_to_add

    @nodes_to_add.setter
    def nodes_to_add(self, val):
        self._nodes_to_add = val
        self._value.nodesToAdd = val.value

    def __str__(self):
        return ("UaAddNodesRequest:\n" + 
                self._request_header.str_helper(1) +
                self._nodes_to_add_size.str_helper(1) +
                self._nodes_to_add.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAddNodesRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._nodes_to_add_size.str_helper(n+1) +
                self._nodes_to_add.str_helper(n+1))


# +++++++++++++++++++ UaBrowseRequest +++++++++++++++++++++++
class UaBrowseRequest(UaType):
    def __init__(self, val=ffi.new("UA_BrowseRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._view = UaViewDescription(val=val.view)
        self._requested_max_references_per_node = UaUInt32(val=val.requestedMaxReferencesPerNode)
        self._nodes_to_browse_size = SizeT(val=val.nodesToBrowseSize)
        self._nodes_to_browse = UaBrowseDescription(val=val.nodesToBrowse, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, val):
        self._view = val
        self._value.view = val.value

    @property
    def requested_max_references_per_node(self):
        return self._requested_max_references_per_node

    @requested_max_references_per_node.setter
    def requested_max_references_per_node(self, val):
        self._requested_max_references_per_node = val
        self._value.requestedMaxReferencesPerNode = val.value

    @property
    def nodes_to_browse_size(self):
        return self._nodes_to_browse_size

    @nodes_to_browse_size.setter
    def nodes_to_browse_size(self, val):
        self._nodes_to_browse_size = val
        self._value.nodesToBrowseSize = val.value

    @property
    def nodes_to_browse(self):
        return self._nodes_to_browse

    @nodes_to_browse.setter
    def nodes_to_browse(self, val):
        self._nodes_to_browse = val
        self._value.nodesToBrowse = val.value

    def __str__(self):
        return ("UaBrowseRequest:\n" + 
                self._request_header.str_helper(1) +
                self._view.str_helper(1) +
                self._requested_max_references_per_node.str_helper(1) +
                self._nodes_to_browse_size.str_helper(1) +
                self._nodes_to_browse.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBrowseRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._view.str_helper(n+1) +
                self._requested_max_references_per_node.str_helper(n+1) +
                self._nodes_to_browse_size.str_helper(n+1) +
                self._nodes_to_browse.str_helper(n+1))


# +++++++++++++++++++ UaWriteRequest +++++++++++++++++++++++
class UaWriteRequest(UaType):
    def __init__(self, val=ffi.new("UA_WriteRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._nodes_to_write_size = SizeT(val=val.nodesToWriteSize)
        self._nodes_to_write = UaWriteValue(val=val.nodesToWrite, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def nodes_to_write_size(self):
        return self._nodes_to_write_size

    @nodes_to_write_size.setter
    def nodes_to_write_size(self, val):
        self._nodes_to_write_size = val
        self._value.nodesToWriteSize = val.value

    @property
    def nodes_to_write(self):
        return self._nodes_to_write

    @nodes_to_write.setter
    def nodes_to_write(self, val):
        self._nodes_to_write = val
        self._value.nodesToWrite = val.value

    def __str__(self):
        return ("UaWriteRequest:\n" + 
                self._request_header.str_helper(1) +
                self._nodes_to_write_size.str_helper(1) +
                self._nodes_to_write.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaWriteRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._nodes_to_write_size.str_helper(n+1) +
                self._nodes_to_write.str_helper(n+1))


# +++++++++++++++++++ UaAddNodesResponse +++++++++++++++++++++++
class UaAddNodesResponse(UaType):
    def __init__(self, val=ffi.new("UA_AddNodesResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaAddNodesResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaAddNodesResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAddNodesResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaAttributeOperand +++++++++++++++++++++++
class UaAttributeOperand(UaType):
    def __init__(self, val=ffi.new("UA_AttributeOperand*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._node_id = UaNodeId(val=val.nodeId)
        self._alias = UaString(val=val.alias)
        self._browse_path = UaRelativePath(val=val.browsePath)
        self._attribute_id = UaUInt32(val=val.attributeId)
        self._index_range = UaString(val=val.indexRange)
    

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, val):
        self._node_id = val
        self._value.nodeId = val.value

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, val):
        self._alias = val
        self._value.alias = val.value

    @property
    def browse_path(self):
        return self._browse_path

    @browse_path.setter
    def browse_path(self, val):
        self._browse_path = val
        self._value.browsePath = val.value

    @property
    def attribute_id(self):
        return self._attribute_id

    @attribute_id.setter
    def attribute_id(self, val):
        self._attribute_id = val
        self._value.attributeId = val.value

    @property
    def index_range(self):
        return self._index_range

    @index_range.setter
    def index_range(self, val):
        self._index_range = val
        self._value.indexRange = val.value

    def __str__(self):
        return ("UaAttributeOperand:\n" + 
                self._node_id.str_helper(1) +
                self._alias.str_helper(1) +
                self._browse_path.str_helper(1) +
                self._attribute_id.str_helper(1) +
                self._index_range.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaAttributeOperand:\n" + 
                self._node_id.str_helper(n+1) +
                self._alias.str_helper(n+1) +
                self._browse_path.str_helper(n+1) +
                self._attribute_id.str_helper(n+1) +
                self._index_range.str_helper(n+1))


# +++++++++++++++++++ UaDataChangeFilter +++++++++++++++++++++++
class UaDataChangeFilter(UaType):
    def __init__(self, val=ffi.new("UA_DataChangeFilter*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._trigger = UaDataChangeTrigger(val=val.trigger)
        self._deadband_type = UaUInt32(val=val.deadbandType)
        self._deadband_value = UaDouble(val=val.deadbandValue)
    

    @property
    def trigger(self):
        return self._trigger

    @trigger.setter
    def trigger(self, val):
        self._trigger = val
        self._value.trigger = val.value

    @property
    def deadband_type(self):
        return self._deadband_type

    @deadband_type.setter
    def deadband_type(self, val):
        self._deadband_type = val
        self._value.deadbandType = val.value

    @property
    def deadband_value(self):
        return self._deadband_value

    @deadband_value.setter
    def deadband_value(self, val):
        self._deadband_value = val
        self._value.deadbandValue = val.value

    def __str__(self):
        return ("UaDataChangeFilter:\n" + 
                self._trigger.str_helper(1) +
                self._deadband_type.str_helper(1) +
                self._deadband_value.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDataChangeFilter:\n" + 
                self._trigger.str_helper(n+1) +
                self._deadband_type.str_helper(n+1) +
                self._deadband_value.str_helper(n+1))


# +++++++++++++++++++ UaEndpointDescription +++++++++++++++++++++++
class UaEndpointDescription(UaType):
    def __init__(self, val=ffi.new("UA_EndpointDescription*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._endpoint_url = UaString(val=val.endpointUrl)
        self._server = UaApplicationDescription(val=val.server)
        self._server_certificate = UaByteString(val=val.serverCertificate)
        self._security_mode = UaMessageSecurityMode(val=val.securityMode)
        self._security_policy_uri = UaString(val=val.securityPolicyUri)
        self._user_identity_tokens_size = SizeT(val=val.userIdentityTokensSize)
        self._user_identity_tokens = UaUserTokenPolicy(val=val.userIdentityTokens, is_pointer=True)
        self._transport_profile_uri = UaString(val=val.transportProfileUri)
        self._security_level = UaByte(val=val.securityLevel)
    

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, val):
        self._endpoint_url = val
        self._value.endpointUrl = val.value

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, val):
        self._server = val
        self._value.server = val.value

    @property
    def server_certificate(self):
        return self._server_certificate

    @server_certificate.setter
    def server_certificate(self, val):
        self._server_certificate = val
        self._value.serverCertificate = val.value

    @property
    def security_mode(self):
        return self._security_mode

    @security_mode.setter
    def security_mode(self, val):
        self._security_mode = val
        self._value.securityMode = val.value

    @property
    def security_policy_uri(self):
        return self._security_policy_uri

    @security_policy_uri.setter
    def security_policy_uri(self, val):
        self._security_policy_uri = val
        self._value.securityPolicyUri = val.value

    @property
    def user_identity_tokens_size(self):
        return self._user_identity_tokens_size

    @user_identity_tokens_size.setter
    def user_identity_tokens_size(self, val):
        self._user_identity_tokens_size = val
        self._value.userIdentityTokensSize = val.value

    @property
    def user_identity_tokens(self):
        return self._user_identity_tokens

    @user_identity_tokens.setter
    def user_identity_tokens(self, val):
        self._user_identity_tokens = val
        self._value.userIdentityTokens = val.value

    @property
    def transport_profile_uri(self):
        return self._transport_profile_uri

    @transport_profile_uri.setter
    def transport_profile_uri(self, val):
        self._transport_profile_uri = val
        self._value.transportProfileUri = val.value

    @property
    def security_level(self):
        return self._security_level

    @security_level.setter
    def security_level(self, val):
        self._security_level = val
        self._value.securityLevel = val.value

    def __str__(self):
        return ("UaEndpointDescription:\n" + 
                self._endpoint_url.str_helper(1) +
                self._server.str_helper(1) +
                self._server_certificate.str_helper(1) +
                self._security_mode.str_helper(1) +
                self._security_policy_uri.str_helper(1) +
                self._user_identity_tokens_size.str_helper(1) +
                self._user_identity_tokens.str_helper(1) +
                self._transport_profile_uri.str_helper(1) +
                self._security_level.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaEndpointDescription:\n" + 
                self._endpoint_url.str_helper(n+1) +
                self._server.str_helper(n+1) +
                self._server_certificate.str_helper(n+1) +
                self._security_mode.str_helper(n+1) +
                self._security_policy_uri.str_helper(n+1) +
                self._user_identity_tokens_size.str_helper(n+1) +
                self._user_identity_tokens.str_helper(n+1) +
                self._transport_profile_uri.str_helper(n+1) +
                self._security_level.str_helper(n+1))


# +++++++++++++++++++ UaDeleteReferencesRequest +++++++++++++++++++++++
class UaDeleteReferencesRequest(UaType):
    def __init__(self, val=ffi.new("UA_DeleteReferencesRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._references_to_delete_size = SizeT(val=val.referencesToDeleteSize)
        self._references_to_delete = UaDeleteReferencesItem(val=val.referencesToDelete, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def references_to_delete_size(self):
        return self._references_to_delete_size

    @references_to_delete_size.setter
    def references_to_delete_size(self, val):
        self._references_to_delete_size = val
        self._value.referencesToDeleteSize = val.value

    @property
    def references_to_delete(self):
        return self._references_to_delete

    @references_to_delete.setter
    def references_to_delete(self, val):
        self._references_to_delete = val
        self._value.referencesToDelete = val.value

    def __str__(self):
        return ("UaDeleteReferencesRequest:\n" + 
                self._request_header.str_helper(1) +
                self._references_to_delete_size.str_helper(1) +
                self._references_to_delete.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaDeleteReferencesRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._references_to_delete_size.str_helper(n+1) +
                self._references_to_delete.str_helper(n+1))


# +++++++++++++++++++ UaTranslateBrowsePathsToNodeIdsRequest +++++++++++++++++++++++
class UaTranslateBrowsePathsToNodeIdsRequest(UaType):
    def __init__(self, val=ffi.new("UA_TranslateBrowsePathsToNodeIdsRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._browse_paths_size = SizeT(val=val.browsePathsSize)
        self._browse_paths = UaBrowsePath(val=val.browsePaths, is_pointer=True)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def browse_paths_size(self):
        return self._browse_paths_size

    @browse_paths_size.setter
    def browse_paths_size(self, val):
        self._browse_paths_size = val
        self._value.browsePathsSize = val.value

    @property
    def browse_paths(self):
        return self._browse_paths

    @browse_paths.setter
    def browse_paths(self, val):
        self._browse_paths = val
        self._value.browsePaths = val.value

    def __str__(self):
        return ("UaTranslateBrowsePathsToNodeIdsRequest:\n" + 
                self._request_header.str_helper(1) +
                self._browse_paths_size.str_helper(1) +
                self._browse_paths.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaTranslateBrowsePathsToNodeIdsRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._browse_paths_size.str_helper(n+1) +
                self._browse_paths.str_helper(n+1))


# +++++++++++++++++++ UaFindServersResponse +++++++++++++++++++++++
class UaFindServersResponse(UaType):
    def __init__(self, val=ffi.new("UA_FindServersResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._servers_size = SizeT(val=val.serversSize)
        self._servers = UaApplicationDescription(val=val.servers, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def servers_size(self):
        return self._servers_size

    @servers_size.setter
    def servers_size(self, val):
        self._servers_size = val
        self._value.serversSize = val.value

    @property
    def servers(self):
        return self._servers

    @servers.setter
    def servers(self, val):
        self._servers = val
        self._value.servers = val.value

    def __str__(self):
        return ("UaFindServersResponse:\n" + 
                self._response_header.str_helper(1) +
                self._servers_size.str_helper(1) +
                self._servers.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaFindServersResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._servers_size.str_helper(n+1) +
                self._servers.str_helper(n+1))


# +++++++++++++++++++ UaCreateSessionRequest +++++++++++++++++++++++
class UaCreateSessionRequest(UaType):
    def __init__(self, val=ffi.new("UA_CreateSessionRequest*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._request_header = UaRequestHeader(val=val.requestHeader)
        self._client_description = UaApplicationDescription(val=val.clientDescription)
        self._server_uri = UaString(val=val.serverUri)
        self._endpoint_url = UaString(val=val.endpointUrl)
        self._session_name = UaString(val=val.sessionName)
        self._client_nonce = UaByteString(val=val.clientNonce)
        self._client_certificate = UaByteString(val=val.clientCertificate)
        self._requested_session_timeout = UaDouble(val=val.requestedSessionTimeout)
        self._max_response_message_size = UaUInt32(val=val.maxResponseMessageSize)
    

    @property
    def request_header(self):
        return self._request_header

    @request_header.setter
    def request_header(self, val):
        self._request_header = val
        self._value.requestHeader = val.value

    @property
    def client_description(self):
        return self._client_description

    @client_description.setter
    def client_description(self, val):
        self._client_description = val
        self._value.clientDescription = val.value

    @property
    def server_uri(self):
        return self._server_uri

    @server_uri.setter
    def server_uri(self, val):
        self._server_uri = val
        self._value.serverUri = val.value

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, val):
        self._endpoint_url = val
        self._value.endpointUrl = val.value

    @property
    def session_name(self):
        return self._session_name

    @session_name.setter
    def session_name(self, val):
        self._session_name = val
        self._value.sessionName = val.value

    @property
    def client_nonce(self):
        return self._client_nonce

    @client_nonce.setter
    def client_nonce(self, val):
        self._client_nonce = val
        self._value.clientNonce = val.value

    @property
    def client_certificate(self):
        return self._client_certificate

    @client_certificate.setter
    def client_certificate(self, val):
        self._client_certificate = val
        self._value.clientCertificate = val.value

    @property
    def requested_session_timeout(self):
        return self._requested_session_timeout

    @requested_session_timeout.setter
    def requested_session_timeout(self, val):
        self._requested_session_timeout = val
        self._value.requestedSessionTimeout = val.value

    @property
    def max_response_message_size(self):
        return self._max_response_message_size

    @max_response_message_size.setter
    def max_response_message_size(self, val):
        self._max_response_message_size = val
        self._value.maxResponseMessageSize = val.value

    def __str__(self):
        return ("UaCreateSessionRequest:\n" + 
                self._request_header.str_helper(1) +
                self._client_description.str_helper(1) +
                self._server_uri.str_helper(1) +
                self._endpoint_url.str_helper(1) +
                self._session_name.str_helper(1) +
                self._client_nonce.str_helper(1) +
                self._client_certificate.str_helper(1) +
                self._requested_session_timeout.str_helper(1) +
                self._max_response_message_size.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCreateSessionRequest:\n" + 
                self._request_header.str_helper(n+1) +
                self._client_description.str_helper(n+1) +
                self._server_uri.str_helper(n+1) +
                self._endpoint_url.str_helper(n+1) +
                self._session_name.str_helper(n+1) +
                self._client_nonce.str_helper(n+1) +
                self._client_certificate.str_helper(n+1) +
                self._requested_session_timeout.str_helper(n+1) +
                self._max_response_message_size.str_helper(n+1))


# +++++++++++++++++++ UaContentFilterElement +++++++++++++++++++++++
class UaContentFilterElement(UaType):
    def __init__(self, val=ffi.new("UA_ContentFilterElement*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._filter_operator = UaFilterOperator(val=val.filterOperator)
        self._filter_operands_size = SizeT(val=val.filterOperandsSize)
        self._filter_operands = UaExtensionObject(val=val.filterOperands, is_pointer=True)
    

    @property
    def filter_operator(self):
        return self._filter_operator

    @filter_operator.setter
    def filter_operator(self, val):
        self._filter_operator = val
        self._value.filterOperator = val.value

    @property
    def filter_operands_size(self):
        return self._filter_operands_size

    @filter_operands_size.setter
    def filter_operands_size(self, val):
        self._filter_operands_size = val
        self._value.filterOperandsSize = val.value

    @property
    def filter_operands(self):
        return self._filter_operands

    @filter_operands.setter
    def filter_operands(self, val):
        self._filter_operands = val
        self._value.filterOperands = val.value

    def __str__(self):
        return ("UaContentFilterElement:\n" + 
                self._filter_operator.str_helper(1) +
                self._filter_operands_size.str_helper(1) +
                self._filter_operands.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaContentFilterElement:\n" + 
                self._filter_operator.str_helper(n+1) +
                self._filter_operands_size.str_helper(n+1) +
                self._filter_operands.str_helper(n+1))


# +++++++++++++++++++ UaTranslateBrowsePathsToNodeIdsResponse +++++++++++++++++++++++
class UaTranslateBrowsePathsToNodeIdsResponse(UaType):
    def __init__(self, val=ffi.new("UA_TranslateBrowsePathsToNodeIdsResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaBrowsePathResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaTranslateBrowsePathsToNodeIdsResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaTranslateBrowsePathsToNodeIdsResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaBrowseResponse +++++++++++++++++++++++
class UaBrowseResponse(UaType):
    def __init__(self, val=ffi.new("UA_BrowseResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._results_size = SizeT(val=val.resultsSize)
        self._results = UaBrowseResult(val=val.results, is_pointer=True)
        self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize)
        self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def results_size(self):
        return self._results_size

    @results_size.setter
    def results_size(self, val):
        self._results_size = val
        self._value.resultsSize = val.value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, val):
        self._results = val
        self._value.results = val.value

    @property
    def diagnostic_infos_size(self):
        return self._diagnostic_infos_size

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val.value

    @property
    def diagnostic_infos(self):
        return self._diagnostic_infos

    @diagnostic_infos.setter
    def diagnostic_infos(self, val):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val.value

    def __str__(self):
        return ("UaBrowseResponse:\n" + 
                self._response_header.str_helper(1) +
                self._results_size.str_helper(1) +
                self._results.str_helper(1) +
                self._diagnostic_infos_size.str_helper(1) +
                self._diagnostic_infos.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaBrowseResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._results_size.str_helper(n+1) +
                self._results.str_helper(n+1) +
                self._diagnostic_infos_size.str_helper(n+1) +
                self._diagnostic_infos.str_helper(n+1))


# +++++++++++++++++++ UaCreateSessionResponse +++++++++++++++++++++++
class UaCreateSessionResponse(UaType):
    def __init__(self, val=ffi.new("UA_CreateSessionResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._session_id = UaNodeId(val=val.sessionId)
        self._authentication_token = UaNodeId(val=val.authenticationToken)
        self._revised_session_timeout = UaDouble(val=val.revisedSessionTimeout)
        self._server_nonce = UaByteString(val=val.serverNonce)
        self._server_certificate = UaByteString(val=val.serverCertificate)
        self._server_endpoints_size = SizeT(val=val.serverEndpointsSize)
        self._server_endpoints = UaEndpointDescription(val=val.serverEndpoints, is_pointer=True)
        self._server_software_certificates_size = SizeT(val=val.serverSoftwareCertificatesSize)
        self._server_software_certificates = UaSignedSoftwareCertificate(val=val.serverSoftwareCertificates, is_pointer=True)
        self._server_signature = UaSignatureData(val=val.serverSignature)
        self._max_request_message_size = UaUInt32(val=val.maxRequestMessageSize)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, val):
        self._session_id = val
        self._value.sessionId = val.value

    @property
    def authentication_token(self):
        return self._authentication_token

    @authentication_token.setter
    def authentication_token(self, val):
        self._authentication_token = val
        self._value.authenticationToken = val.value

    @property
    def revised_session_timeout(self):
        return self._revised_session_timeout

    @revised_session_timeout.setter
    def revised_session_timeout(self, val):
        self._revised_session_timeout = val
        self._value.revisedSessionTimeout = val.value

    @property
    def server_nonce(self):
        return self._server_nonce

    @server_nonce.setter
    def server_nonce(self, val):
        self._server_nonce = val
        self._value.serverNonce = val.value

    @property
    def server_certificate(self):
        return self._server_certificate

    @server_certificate.setter
    def server_certificate(self, val):
        self._server_certificate = val
        self._value.serverCertificate = val.value

    @property
    def server_endpoints_size(self):
        return self._server_endpoints_size

    @server_endpoints_size.setter
    def server_endpoints_size(self, val):
        self._server_endpoints_size = val
        self._value.serverEndpointsSize = val.value

    @property
    def server_endpoints(self):
        return self._server_endpoints

    @server_endpoints.setter
    def server_endpoints(self, val):
        self._server_endpoints = val
        self._value.serverEndpoints = val.value

    @property
    def server_software_certificates_size(self):
        return self._server_software_certificates_size

    @server_software_certificates_size.setter
    def server_software_certificates_size(self, val):
        self._server_software_certificates_size = val
        self._value.serverSoftwareCertificatesSize = val.value

    @property
    def server_software_certificates(self):
        return self._server_software_certificates

    @server_software_certificates.setter
    def server_software_certificates(self, val):
        self._server_software_certificates = val
        self._value.serverSoftwareCertificates = val.value

    @property
    def server_signature(self):
        return self._server_signature

    @server_signature.setter
    def server_signature(self, val):
        self._server_signature = val
        self._value.serverSignature = val.value

    @property
    def max_request_message_size(self):
        return self._max_request_message_size

    @max_request_message_size.setter
    def max_request_message_size(self, val):
        self._max_request_message_size = val
        self._value.maxRequestMessageSize = val.value

    def __str__(self):
        return ("UaCreateSessionResponse:\n" + 
                self._response_header.str_helper(1) +
                self._session_id.str_helper(1) +
                self._authentication_token.str_helper(1) +
                self._revised_session_timeout.str_helper(1) +
                self._server_nonce.str_helper(1) +
                self._server_certificate.str_helper(1) +
                self._server_endpoints_size.str_helper(1) +
                self._server_endpoints.str_helper(1) +
                self._server_software_certificates_size.str_helper(1) +
                self._server_software_certificates.str_helper(1) +
                self._server_signature.str_helper(1) +
                self._max_request_message_size.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaCreateSessionResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._session_id.str_helper(n+1) +
                self._authentication_token.str_helper(n+1) +
                self._revised_session_timeout.str_helper(n+1) +
                self._server_nonce.str_helper(n+1) +
                self._server_certificate.str_helper(n+1) +
                self._server_endpoints_size.str_helper(n+1) +
                self._server_endpoints.str_helper(n+1) +
                self._server_software_certificates_size.str_helper(n+1) +
                self._server_software_certificates.str_helper(n+1) +
                self._server_signature.str_helper(n+1) +
                self._max_request_message_size.str_helper(n+1))


# +++++++++++++++++++ UaContentFilter +++++++++++++++++++++++
class UaContentFilter(UaType):
    def __init__(self, val=ffi.new("UA_ContentFilter*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._elements_size = SizeT(val=val.elementsSize)
        self._elements = UaContentFilterElement(val=val.elements, is_pointer=True)
    

    @property
    def elements_size(self):
        return self._elements_size

    @elements_size.setter
    def elements_size(self, val):
        self._elements_size = val
        self._value.elementsSize = val.value

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, val):
        self._elements = val
        self._value.elements = val.value

    def __str__(self):
        return ("UaContentFilter:\n" + 
                self._elements_size.str_helper(1) +
                self._elements.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaContentFilter:\n" + 
                self._elements_size.str_helper(n+1) +
                self._elements.str_helper(n+1))


# +++++++++++++++++++ UaGetEndpointsResponse +++++++++++++++++++++++
class UaGetEndpointsResponse(UaType):
    def __init__(self, val=ffi.new("UA_GetEndpointsResponse*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._response_header = UaResponseHeader(val=val.responseHeader)
        self._endpoints_size = SizeT(val=val.endpointsSize)
        self._endpoints = UaEndpointDescription(val=val.endpoints, is_pointer=True)
    

    @property
    def response_header(self):
        return self._response_header

    @response_header.setter
    def response_header(self, val):
        self._response_header = val
        self._value.responseHeader = val.value

    @property
    def endpoints_size(self):
        return self._endpoints_size

    @endpoints_size.setter
    def endpoints_size(self, val):
        self._endpoints_size = val
        self._value.endpointsSize = val.value

    @property
    def endpoints(self):
        return self._endpoints

    @endpoints.setter
    def endpoints(self, val):
        self._endpoints = val
        self._value.endpoints = val.value

    def __str__(self):
        return ("UaGetEndpointsResponse:\n" + 
                self._response_header.str_helper(1) +
                self._endpoints_size.str_helper(1) +
                self._endpoints.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaGetEndpointsResponse:\n" + 
                self._response_header.str_helper(n+1) +
                self._endpoints_size.str_helper(n+1) +
                self._endpoints.str_helper(n+1))


# +++++++++++++++++++ UaEventFilter +++++++++++++++++++++++
class UaEventFilter(UaType):
    def __init__(self, val=ffi.new("UA_EventFilter*"), is_pointer=False):
        super().__init__(val, is_pointer)
        self._select_clauses_size = SizeT(val=val.selectClausesSize)
        self._select_clauses = UaSimpleAttributeOperand(val=val.selectClauses, is_pointer=True)
        self._where_clause = UaContentFilter(val=val.whereClause)
    

    @property
    def select_clauses_size(self):
        return self._select_clauses_size

    @select_clauses_size.setter
    def select_clauses_size(self, val):
        self._select_clauses_size = val
        self._value.selectClausesSize = val.value

    @property
    def select_clauses(self):
        return self._select_clauses

    @select_clauses.setter
    def select_clauses(self, val):
        self._select_clauses = val
        self._value.selectClauses = val.value

    @property
    def where_clause(self):
        return self._where_clause

    @where_clause.setter
    def where_clause(self, val):
        self._where_clause = val
        self._value.whereClause = val.value

    def __str__(self):
        return ("UaEventFilter:\n" + 
                self._select_clauses_size.str_helper(1) +
                self._select_clauses.str_helper(1) +
                self._where_clause.str_helper(1))
    
    def str_helper(self, n: int):
        return ("\t"*n + "UaEventFilter:\n" + 
                self._select_clauses_size.str_helper(n+1) +
                self._select_clauses.str_helper(n+1) +
                self._where_clause.str_helper(n+1))
