# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from typing import Union

from intermediateApi import ffi, lib
from c_types import *
from ua_types_parent import _ptr, _val, _is_null, _is_ptr


# -------------------------------------------------------------
# --------------------------- Enums ---------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaAttributeId +++++++++++++++++++++++
class UaAttributeId(UaType):
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

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_AttributeId*", val._ptr)
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

    @staticmethod
    def NODEID():
        return UaAttributeId(1)

    @staticmethod
    def NODECLASS():
        return UaAttributeId(2)

    @staticmethod
    def BROWSENAME():
        return UaAttributeId(3)

    @staticmethod
    def DISPLAYNAME():
        return UaAttributeId(4)

    @staticmethod
    def DESCRIPTION():
        return UaAttributeId(5)

    @staticmethod
    def WRITEMASK():
        return UaAttributeId(6)

    @staticmethod
    def USERWRITEMASK():
        return UaAttributeId(7)

    @staticmethod
    def ISABSTRACT():
        return UaAttributeId(8)

    @staticmethod
    def SYMMETRIC():
        return UaAttributeId(9)

    @staticmethod
    def INVERSENAME():
        return UaAttributeId(10)

    @staticmethod
    def CONTAINSNOLOOPS():
        return UaAttributeId(11)

    @staticmethod
    def EVENTNOTIFIER():
        return UaAttributeId(12)

    @staticmethod
    def VALUE():
        return UaAttributeId(13)

    @staticmethod
    def DATATYPE():
        return UaAttributeId(14)

    @staticmethod
    def VALUERANK():
        return UaAttributeId(15)

    @staticmethod
    def ARRAYDIMENSIONS():
        return UaAttributeId(16)

    @staticmethod
    def ACCESSLEVEL():
        return UaAttributeId(17)

    @staticmethod
    def USERACCESSLEVEL():
        return UaAttributeId(18)

    @staticmethod
    def MINIMUMSAMPLINGINTERVAL():
        return UaAttributeId(19)

    @staticmethod
    def HISTORIZING():
        return UaAttributeId(20)

    @staticmethod
    def EXECUTABLE():
        return UaAttributeId(21)

    @staticmethod
    def USEREXECUTABLE():
        return UaAttributeId(22)

    @staticmethod
    def DATATYPEDEFINITION():
        return UaAttributeId(23)

    @staticmethod
    def ROLEPERMISSIONS():
        return UaAttributeId(24)

    @staticmethod
    def USERROLEPERMISSIONS():
        return UaAttributeId(25)

    @staticmethod
    def ACCESSRESTRICTIONS():
        return UaAttributeId(26)

    @staticmethod
    def ACCESSLEVELEX():
        return UaAttributeId(27)

    def __str__(self, n=0):
        return f"(UaAttributeId): {self.val_to_string[self._val]} ({str(self._val)})" + ("" if n is None else "\n")


# +++++++++++++++++++ UaRuleHandling +++++++++++++++++++++++
class UaRuleHandling(UaType):
    val_to_string = dict([
        (0, "UA_RULEHANDLING_DEFAULT"),
        (1, "UA_RULEHANDLING_ABORT"),
        (2, "UA_RULEHANDLING_WARN"),
        (3, "UA_RULEHANDLING_ACCEPT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_RuleHandling*", val._ptr)
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

    @staticmethod
    def DEFAULT():
        return UaRuleHandling(0)

    @staticmethod
    def ABORT():
        return UaRuleHandling(1)

    @staticmethod
    def WARN():
        return UaRuleHandling(2)

    @staticmethod
    def ACCEPT():
        return UaRuleHandling(3)

    def __str__(self, n=0):
        return f"(UaRuleHandling): {self.val_to_string[self._val]} ({str(self._val)})" + ("" if n is None else "\n")


# +++++++++++++++++++ UaOrder +++++++++++++++++++++++
class UaOrder(UaType):
    val_to_string = dict([
        (-1, "UA_ORDER_LESS"),
        (0, "UA_ORDER_EQ"),
        (1, "UA_ORDER_MORE")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Order*", val._ptr)
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

    @staticmethod
    def LESS():
        return UaOrder(-1)

    @staticmethod
    def EQ():
        return UaOrder(0)

    @staticmethod
    def MORE():
        return UaOrder(1)

    def __str__(self, n=0):
        return f"(UaOrder): {self.val_to_string[self._val]} ({str(self._val)})" + ("" if n is None else "\n")


# +++++++++++++++++++ UaSecureChannelState +++++++++++++++++++++++
class UaSecureChannelState(UaType):
    val_to_string = dict([
        (0, "UA_SECURECHANNELSTATE_CLOSED"),
        (1, "UA_SECURECHANNELSTATE_HEL_SENT"),
        (2, "UA_SECURECHANNELSTATE_HEL_RECEIVED"),
        (3, "UA_SECURECHANNELSTATE_ACK_SENT"),
        (4, "UA_SECURECHANNELSTATE_ACK_RECEIVED"),
        (5, "UA_SECURECHANNELSTATE_OPN_SENT"),
        (6, "UA_SECURECHANNELSTATE_OPEN"),
        (7, "UA_SECURECHANNELSTATE_CLOSING")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_SecureChannelState*", val._ptr)
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

    @staticmethod
    def CLOSED():
        return UaSecureChannelState(0)

    @staticmethod
    def HEL_SENT():
        return UaSecureChannelState(1)

    @staticmethod
    def HEL_RECEIVED():
        return UaSecureChannelState(2)

    @staticmethod
    def ACK_SENT():
        return UaSecureChannelState(3)

    @staticmethod
    def ACK_RECEIVED():
        return UaSecureChannelState(4)

    @staticmethod
    def OPN_SENT():
        return UaSecureChannelState(5)

    @staticmethod
    def OPEN():
        return UaSecureChannelState(6)

    @staticmethod
    def CLOSING():
        return UaSecureChannelState(7)

    def __str__(self, n=0):
        return f"(UaSecureChannelState): {self.val_to_string[self._val]} ({str(self._val)})" + ("" if n is None else "\n")


# +++++++++++++++++++ UaSessionState +++++++++++++++++++++++
class UaSessionState(UaType):
    val_to_string = dict([
        (0, "UA_SESSIONSTATE_CLOSED"),
        (1, "UA_SESSIONSTATE_CREATE_REQUESTED"),
        (2, "UA_SESSIONSTATE_CREATED"),
        (3, "UA_SESSIONSTATE_ACTIVATE_REQUESTED"),
        (4, "UA_SESSIONSTATE_ACTIVATED"),
        (5, "UA_SESSIONSTATE_CLOSING")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_SessionState*", val._ptr)
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

    @staticmethod
    def CLOSED():
        return UaSessionState(0)

    @staticmethod
    def CREATE_REQUESTED():
        return UaSessionState(1)

    @staticmethod
    def CREATED():
        return UaSessionState(2)

    @staticmethod
    def ACTIVATE_REQUESTED():
        return UaSessionState(3)

    @staticmethod
    def ACTIVATED():
        return UaSessionState(4)

    @staticmethod
    def CLOSING():
        return UaSessionState(5)

    def __str__(self, n=0):
        return f"(UaSessionState): {self.val_to_string[self._val]} ({str(self._val)})" + ("" if n is None else "\n")


# -------------------------------------------------------------
# -------------------------- Structs --------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaNetworkStatistics +++++++++++++++++++++++
class UaNetworkStatistics(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NetworkStatistics*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_NetworkStatistics*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._current_connection_count = SizeT(val=val.currentConnectionCount, is_pointer=False)
            self._cumulated_connection_count = SizeT(val=val.cumulatedConnectionCount, is_pointer=False)
            self._rejected_connection_count = SizeT(val=val.rejectedConnectionCount, is_pointer=False)
            self._connection_timeout_count = SizeT(val=val.connectionTimeoutCount, is_pointer=False)
            self._connection_abort_count = SizeT(val=val.connectionAbortCount, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NetworkStatistics")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._current_connection_count._value[0] = _val(val.currentConnectionCount)
            self._cumulated_connection_count._value[0] = _val(val.cumulatedConnectionCount)
            self._rejected_connection_count._value[0] = _val(val.rejectedConnectionCount)
            self._connection_timeout_count._value[0] = _val(val.connectionTimeoutCount)
            self._connection_abort_count._value[0] = _val(val.connectionAbortCount)

    @property
    def current_connection_count(self):
        if self._null:
            return None
        else:
            return self._current_connection_count

    @property
    def cumulated_connection_count(self):
        if self._null:
            return None
        else:
            return self._cumulated_connection_count

    @property
    def rejected_connection_count(self):
        if self._null:
            return None
        else:
            return self._rejected_connection_count

    @property
    def connection_timeout_count(self):
        if self._null:
            return None
        else:
            return self._connection_timeout_count

    @property
    def connection_abort_count(self):
        if self._null:
            return None
        else:
            return self._connection_abort_count

    @current_connection_count.setter
    def current_connection_count(self, val: SizeT):
        self._current_connection_count = val
        self._value.currentConnectionCount = val._val

    @cumulated_connection_count.setter
    def cumulated_connection_count(self, val: SizeT):
        self._cumulated_connection_count = val
        self._value.cumulatedConnectionCount = val._val

    @rejected_connection_count.setter
    def rejected_connection_count(self, val: SizeT):
        self._rejected_connection_count = val
        self._value.rejectedConnectionCount = val._val

    @connection_timeout_count.setter
    def connection_timeout_count(self, val: SizeT):
        self._connection_timeout_count = val
        self._value.connectionTimeoutCount = val._val

    @connection_abort_count.setter
    def connection_abort_count(self, val: SizeT):
        self._connection_abort_count = val
        self._value.connectionAbortCount = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaNetworkStatistics): NULL" + ("" if n is None else "\n")

        return ("(UaNetworkStatistics) :\n"
                + "\t" * (1 if n is None else n+1) + "current_connection_count " + self._current_connection_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "cumulated_connection_count " + self._cumulated_connection_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "rejected_connection_count " + self._rejected_connection_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "connection_timeout_count " + self._connection_timeout_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "connection_abort_count " + self._connection_abort_count.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSecureChannelStatistics +++++++++++++++++++++++
class UaSecureChannelStatistics(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SecureChannelStatistics*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SecureChannelStatistics*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._current_channel_count = SizeT(val=val.currentChannelCount, is_pointer=False)
            self._cumulated_channel_count = SizeT(val=val.cumulatedChannelCount, is_pointer=False)
            self._rejected_channel_count = SizeT(val=val.rejectedChannelCount, is_pointer=False)
            self._channel_timeout_count = SizeT(val=val.channelTimeoutCount, is_pointer=False)
            self._channel_abort_count = SizeT(val=val.channelAbortCount, is_pointer=False)
            self._channel_purge_count = SizeT(val=val.channelPurgeCount, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SecureChannelStatistics")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._current_channel_count._value[0] = _val(val.currentChannelCount)
            self._cumulated_channel_count._value[0] = _val(val.cumulatedChannelCount)
            self._rejected_channel_count._value[0] = _val(val.rejectedChannelCount)
            self._channel_timeout_count._value[0] = _val(val.channelTimeoutCount)
            self._channel_abort_count._value[0] = _val(val.channelAbortCount)
            self._channel_purge_count._value[0] = _val(val.channelPurgeCount)

    @property
    def current_channel_count(self):
        if self._null:
            return None
        else:
            return self._current_channel_count

    @property
    def cumulated_channel_count(self):
        if self._null:
            return None
        else:
            return self._cumulated_channel_count

    @property
    def rejected_channel_count(self):
        if self._null:
            return None
        else:
            return self._rejected_channel_count

    @property
    def channel_timeout_count(self):
        if self._null:
            return None
        else:
            return self._channel_timeout_count

    @property
    def channel_abort_count(self):
        if self._null:
            return None
        else:
            return self._channel_abort_count

    @property
    def channel_purge_count(self):
        if self._null:
            return None
        else:
            return self._channel_purge_count

    @current_channel_count.setter
    def current_channel_count(self, val: SizeT):
        self._current_channel_count = val
        self._value.currentChannelCount = val._val

    @cumulated_channel_count.setter
    def cumulated_channel_count(self, val: SizeT):
        self._cumulated_channel_count = val
        self._value.cumulatedChannelCount = val._val

    @rejected_channel_count.setter
    def rejected_channel_count(self, val: SizeT):
        self._rejected_channel_count = val
        self._value.rejectedChannelCount = val._val

    @channel_timeout_count.setter
    def channel_timeout_count(self, val: SizeT):
        self._channel_timeout_count = val
        self._value.channelTimeoutCount = val._val

    @channel_abort_count.setter
    def channel_abort_count(self, val: SizeT):
        self._channel_abort_count = val
        self._value.channelAbortCount = val._val

    @channel_purge_count.setter
    def channel_purge_count(self, val: SizeT):
        self._channel_purge_count = val
        self._value.channelPurgeCount = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaSecureChannelStatistics): NULL" + ("" if n is None else "\n")

        return ("(UaSecureChannelStatistics) :\n"
                + "\t" * (1 if n is None else n+1) + "current_channel_count " + self._current_channel_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "cumulated_channel_count " + self._cumulated_channel_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "rejected_channel_count " + self._rejected_channel_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "channel_timeout_count " + self._channel_timeout_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "channel_abort_count " + self._channel_abort_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "channel_purge_count " + self._channel_purge_count.__str__(1 if n is None else n+1))
