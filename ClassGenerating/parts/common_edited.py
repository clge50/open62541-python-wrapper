
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
                "\t"*(n+1) + "current_channel_count" + self._current_channel_count.__str__(n+1) +
                "\t"*(n+1) + "cumulated_channel_count" + self._cumulated_channel_count.__str__(n+1) +
                "\t"*(n+1) + "rejected_channel_count" + self._rejected_channel_count.__str__(n+1) +
                "\t"*(n+1) + "channel_timeout_count" + self._channel_timeout_count.__str__(n+1) +
                "\t"*(n+1) + "channel_abort_count" + self._channel_abort_count.__str__(n+1) +
                "\t"*(n+1) + "channel_purge_count" + self._channel_purge_count.__str__(n+1) + "\n")


