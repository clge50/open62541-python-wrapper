# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_consts_types_raw import _UA_TYPES
from ua_types_base import *
from ua_types_parent import _ptr, _val


# +++++++++++++++++++ UaMessageSecurityMode +++++++++++++++++++++++
class UaMessageSecurityMode(UaType):
    _UA_TYPE = _UA_TYPES._MESSAGESECURITYMODE

    val_to_string = dict([
        (0, "UA_MESSAGESECURITYMODE_INVALID"),
        (1, "UA_MESSAGESECURITYMODE_NONE"),
        (2, "UA_MESSAGESECURITYMODE_SIGN"),
        (3, "UA_MESSAGESECURITYMODE_SIGNANDENCRYPT"),
        (2147483647, "__UA_MESSAGESECURITYMODE_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_MessageSecurityMode*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_MessageSecurityMode*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_MessageSecurityMode", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_MessageSecurityMode")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def INVALID():
        return UaMessageSecurityMode(0)

    @staticmethod
    def NONE():
        return UaMessageSecurityMode(1)

    @staticmethod
    def SIGN():
        return UaMessageSecurityMode(2)

    @staticmethod
    def SIGNANDENCRYPT():
        return UaMessageSecurityMode(3)

    @staticmethod
    def UA_MESSAGESECURITYMODE_FORCE32BIT():
        return UaMessageSecurityMode(2147483647)

    def __str__(self, n=0):
        return f"(UaMessageSecurityMode): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaStructureType +++++++++++++++++++++++
class UaStructureType(UaType):
    _UA_TYPE = _UA_TYPES._STRUCTURETYPE

    val_to_string = dict([
        (0, "UA_STRUCTURETYPE_STRUCTURE"),
        (1, "UA_STRUCTURETYPE_STRUCTUREWITHOPTIONALFIELDS"),
        (2, "UA_STRUCTURETYPE_UNION"),
        (2147483647, "__UA_STRUCTURETYPE_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_StructureType*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_StructureType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_StructureType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_StructureType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def STRUCTURE():
        return UaStructureType(0)

    @staticmethod
    def STRUCTUREWITHOPTIONALFIELDS():
        return UaStructureType(1)

    @staticmethod
    def UNION():
        return UaStructureType(2)

    @staticmethod
    def UA_STRUCTURETYPE_FORCE32BIT():
        return UaStructureType(2147483647)

    def __str__(self, n=0):
        return f"(UaStructureType): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaMonitoringMode +++++++++++++++++++++++
class UaMonitoringMode(UaType):
    _UA_TYPE = _UA_TYPES._MONITORINGMODE

    val_to_string = dict([
        (0, "UA_MONITORINGMODE_DISABLED"),
        (1, "UA_MONITORINGMODE_SAMPLING"),
        (2, "UA_MONITORINGMODE_REPORTING"),
        (2147483647, "__UA_MONITORINGMODE_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_MonitoringMode*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_MonitoringMode*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_MonitoringMode", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_MonitoringMode")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def DISABLED():
        return UaMonitoringMode(0)

    @staticmethod
    def SAMPLING():
        return UaMonitoringMode(1)

    @staticmethod
    def REPORTING():
        return UaMonitoringMode(2)

    @staticmethod
    def UA_MONITORINGMODE_FORCE32BIT():
        return UaMonitoringMode(2147483647)

    def __str__(self, n=0):
        return f"(UaMonitoringMode): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaBrowseResultMask +++++++++++++++++++++++
class UaBrowseResultMask(UaType):
    _UA_TYPE = _UA_TYPES._BROWSERESULTMASK

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

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_BrowseResultMask*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_BrowseResultMask*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_BrowseResultMask", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_BrowseResultMask")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def NONE():
        return UaBrowseResultMask(0)

    @staticmethod
    def REFERENCETYPEID():
        return UaBrowseResultMask(1)

    @staticmethod
    def ISFORWARD():
        return UaBrowseResultMask(2)

    @staticmethod
    def NODECLASS():
        return UaBrowseResultMask(4)

    @staticmethod
    def BROWSENAME():
        return UaBrowseResultMask(8)

    @staticmethod
    def DISPLAYNAME():
        return UaBrowseResultMask(16)

    @staticmethod
    def TYPEDEFINITION():
        return UaBrowseResultMask(32)

    @staticmethod
    def ALL():
        return UaBrowseResultMask(63)

    @staticmethod
    def REFERENCETYPEINFO():
        return UaBrowseResultMask(3)

    @staticmethod
    def TARGETINFO():
        return UaBrowseResultMask(60)

    @staticmethod
    def UA_BROWSERESULTMASK_FORCE32BIT():
        return UaBrowseResultMask(2147483647)

    def __str__(self, n=0):
        return f"(UaBrowseResultMask): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaAxisScaleEnumeration +++++++++++++++++++++++
class UaAxisScaleEnumeration(UaType):
    _UA_TYPE = _UA_TYPES._AXISSCALEENUMERATION

    val_to_string = dict([
        (0, "UA_AXISSCALEENUMERATION_LINEAR"),
        (1, "UA_AXISSCALEENUMERATION_LOG"),
        (2, "UA_AXISSCALEENUMERATION_LN"),
        (2147483647, "__UA_AXISSCALEENUMERATION_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_AxisScaleEnumeration*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_AxisScaleEnumeration*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_AxisScaleEnumeration", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_AxisScaleEnumeration")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def LINEAR():
        return UaAxisScaleEnumeration(0)

    @staticmethod
    def LOG():
        return UaAxisScaleEnumeration(1)

    @staticmethod
    def LN():
        return UaAxisScaleEnumeration(2)

    @staticmethod
    def UA_AXISSCALEENUMERATION_FORCE32BIT():
        return UaAxisScaleEnumeration(2147483647)

    def __str__(self, n=0):
        return f"(UaAxisScaleEnumeration): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaBrowseDirection +++++++++++++++++++++++
class UaBrowseDirection(UaType):
    _UA_TYPE = _UA_TYPES._BROWSEDIRECTION

    val_to_string = dict([
        (0, "UA_BROWSEDIRECTION_FORWARD"),
        (1, "UA_BROWSEDIRECTION_INVERSE"),
        (2, "UA_BROWSEDIRECTION_BOTH"),
        (3, "UA_BROWSEDIRECTION_INVALID"),
        (2147483647, "__UA_BROWSEDIRECTION_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_BrowseDirection*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_BrowseDirection*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_BrowseDirection", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_BrowseDirection")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def FORWARD():
        return UaBrowseDirection(0)

    @staticmethod
    def INVERSE():
        return UaBrowseDirection(1)

    @staticmethod
    def BOTH():
        return UaBrowseDirection(2)

    @staticmethod
    def INVALID():
        return UaBrowseDirection(3)

    @staticmethod
    def UA_BROWSEDIRECTION_FORCE32BIT():
        return UaBrowseDirection(2147483647)

    def __str__(self, n=0):
        return f"(UaBrowseDirection): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaTimestampsToReturn +++++++++++++++++++++++
class UaTimestampsToReturn(UaType):
    _UA_TYPE = _UA_TYPES._TIMESTAMPSTORETURN

    val_to_string = dict([
        (0, "UA_TIMESTAMPSTORETURN_SOURCE"),
        (1, "UA_TIMESTAMPSTORETURN_SERVER"),
        (2, "UA_TIMESTAMPSTORETURN_BOTH"),
        (3, "UA_TIMESTAMPSTORETURN_NEITHER"),
        (4, "UA_TIMESTAMPSTORETURN_INVALID"),
        (2147483647, "__UA_TIMESTAMPSTORETURN_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_TimestampsToReturn*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_TimestampsToReturn*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_TimestampsToReturn", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_TimestampsToReturn")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def SOURCE():
        return UaTimestampsToReturn(0)

    @staticmethod
    def SERVER():
        return UaTimestampsToReturn(1)

    @staticmethod
    def BOTH():
        return UaTimestampsToReturn(2)

    @staticmethod
    def NEITHER():
        return UaTimestampsToReturn(3)

    @staticmethod
    def INVALID():
        return UaTimestampsToReturn(4)

    @staticmethod
    def UA_TIMESTAMPSTORETURN_FORCE32BIT():
        return UaTimestampsToReturn(2147483647)

    def __str__(self, n=0):
        return f"(UaTimestampsToReturn): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaNodeClass +++++++++++++++++++++++
class UaNodeClass(UaType):
    _UA_TYPE = _UA_TYPES._NODECLASS

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

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_NodeClass*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_NodeClass*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_NodeClass", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_NodeClass")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def UNSPECIFIED():
        return UaNodeClass(0)

    @staticmethod
    def OBJECT():
        return UaNodeClass(1)

    @staticmethod
    def VARIABLE():
        return UaNodeClass(2)

    @staticmethod
    def METHOD():
        return UaNodeClass(4)

    @staticmethod
    def OBJECTTYPE():
        return UaNodeClass(8)

    @staticmethod
    def VARIABLETYPE():
        return UaNodeClass(16)

    @staticmethod
    def REFERENCETYPE():
        return UaNodeClass(32)

    @staticmethod
    def DATATYPE():
        return UaNodeClass(64)

    @staticmethod
    def VIEW():
        return UaNodeClass(128)

    @staticmethod
    def UA_NODECLASS_FORCE32BIT():
        return UaNodeClass(2147483647)

    def __str__(self, n=0):
        return f"(UaNodeClass): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaSecurityTokenRequestType +++++++++++++++++++++++
class UaSecurityTokenRequestType(UaType):
    _UA_TYPE = _UA_TYPES._SECURITYTOKENREQUESTTYPE

    val_to_string = dict([
        (0, "UA_SECURITYTOKENREQUESTTYPE_ISSUE"),
        (1, "UA_SECURITYTOKENREQUESTTYPE_RENEW"),
        (2147483647, "__UA_SECURITYTOKENREQUESTTYPE_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_SecurityTokenRequestType*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_SecurityTokenRequestType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_SecurityTokenRequestType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_SecurityTokenRequestType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def ISSUE():
        return UaSecurityTokenRequestType(0)

    @staticmethod
    def RENEW():
        return UaSecurityTokenRequestType(1)

    @staticmethod
    def UA_SECURITYTOKENREQUESTTYPE_FORCE32BIT():
        return UaSecurityTokenRequestType(2147483647)

    def __str__(self, n=0):
        return f"(UaSecurityTokenRequestType): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaApplicationType +++++++++++++++++++++++
class UaApplicationType(UaType):
    _UA_TYPE = _UA_TYPES._APPLICATIONTYPE

    val_to_string = dict([
        (0, "UA_APPLICATIONTYPE_SERVER"),
        (1, "UA_APPLICATIONTYPE_CLIENT"),
        (2, "UA_APPLICATIONTYPE_CLIENTANDSERVER"),
        (3, "UA_APPLICATIONTYPE_DISCOVERYSERVER"),
        (2147483647, "__UA_APPLICATIONTYPE_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_ApplicationType*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_ApplicationType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_ApplicationType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_ApplicationType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def SERVER():
        return UaApplicationType(0)

    @staticmethod
    def CLIENT():
        return UaApplicationType(1)

    @staticmethod
    def CLIENTANDSERVER():
        return UaApplicationType(2)

    @staticmethod
    def DISCOVERYSERVER():
        return UaApplicationType(3)

    @staticmethod
    def UA_APPLICATIONTYPE_FORCE32BIT():
        return UaApplicationType(2147483647)

    def __str__(self, n=0):
        return f"(UaApplicationType): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaDeadbandType +++++++++++++++++++++++
class UaDeadbandType(UaType):
    _UA_TYPE = _UA_TYPES._DEADBANDTYPE

    val_to_string = dict([
        (0, "UA_DEADBANDTYPE_NONE"),
        (1, "UA_DEADBANDTYPE_ABSOLUTE"),
        (2, "UA_DEADBANDTYPE_PERCENT"),
        (2147483647, "__UA_DEADBANDTYPE_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_DeadbandType*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_DeadbandType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_DeadbandType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_DeadbandType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def NONE():
        return UaDeadbandType(0)

    @staticmethod
    def ABSOLUTE():
        return UaDeadbandType(1)

    @staticmethod
    def PERCENT():
        return UaDeadbandType(2)

    @staticmethod
    def UA_DEADBANDTYPE_FORCE32BIT():
        return UaDeadbandType(2147483647)

    def __str__(self, n=0):
        return f"(UaDeadbandType): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaDataChangeTrigger +++++++++++++++++++++++
class UaDataChangeTrigger(UaType):
    _UA_TYPE = _UA_TYPES._DATACHANGETRIGGER

    val_to_string = dict([
        (0, "UA_DATACHANGETRIGGER_STATUS"),
        (1, "UA_DATACHANGETRIGGER_STATUSVALUE"),
        (2, "UA_DATACHANGETRIGGER_STATUSVALUETIMESTAMP"),
        (2147483647, "__UA_DATACHANGETRIGGER_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_DataChangeTrigger*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_DataChangeTrigger*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_DataChangeTrigger", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_DataChangeTrigger")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def STATUS():
        return UaDataChangeTrigger(0)

    @staticmethod
    def STATUSVALUE():
        return UaDataChangeTrigger(1)

    @staticmethod
    def STATUSVALUETIMESTAMP():
        return UaDataChangeTrigger(2)

    @staticmethod
    def UA_DATACHANGETRIGGER_FORCE32BIT():
        return UaDataChangeTrigger(2147483647)

    def __str__(self, n=0):
        return f"(UaDataChangeTrigger): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaUserTokenType +++++++++++++++++++++++
class UaUserTokenType(UaType):
    _UA_TYPE = _UA_TYPES._USERTOKENTYPE

    val_to_string = dict([
        (0, "UA_USERTOKENTYPE_ANONYMOUS"),
        (1, "UA_USERTOKENTYPE_USERNAME"),
        (2, "UA_USERTOKENTYPE_CERTIFICATE"),
        (3, "UA_USERTOKENTYPE_ISSUEDTOKEN"),
        (2147483647, "__UA_USERTOKENTYPE_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_UserTokenType*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_UserTokenType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_UserTokenType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_UserTokenType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def ANONYMOUS():
        return UaUserTokenType(0)

    @staticmethod
    def USERNAME():
        return UaUserTokenType(1)

    @staticmethod
    def CERTIFICATE():
        return UaUserTokenType(2)

    @staticmethod
    def ISSUEDTOKEN():
        return UaUserTokenType(3)

    @staticmethod
    def UA_USERTOKENTYPE_FORCE32BIT():
        return UaUserTokenType(2147483647)

    def __str__(self, n=0):
        return f"(UaUserTokenType): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaNodeAttributesMask +++++++++++++++++++++++
class UaNodeAttributesMask(UaType):
    _UA_TYPE = _UA_TYPES._NODEATTRIBUTESMASK

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

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_NodeAttributesMask*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_NodeAttributesMask*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_NodeAttributesMask", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_NodeAttributesMask")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def NONE():
        return UaNodeAttributesMask(0)

    @staticmethod
    def ACCESSLEVEL():
        return UaNodeAttributesMask(1)

    @staticmethod
    def ARRAYDIMENSIONS():
        return UaNodeAttributesMask(2)

    @staticmethod
    def BROWSENAME():
        return UaNodeAttributesMask(4)

    @staticmethod
    def CONTAINSNOLOOPS():
        return UaNodeAttributesMask(8)

    @staticmethod
    def DATATYPE():
        return UaNodeAttributesMask(16)

    @staticmethod
    def DESCRIPTION():
        return UaNodeAttributesMask(32)

    @staticmethod
    def DISPLAYNAME():
        return UaNodeAttributesMask(64)

    @staticmethod
    def EVENTNOTIFIER():
        return UaNodeAttributesMask(128)

    @staticmethod
    def EXECUTABLE():
        return UaNodeAttributesMask(256)

    @staticmethod
    def HISTORIZING():
        return UaNodeAttributesMask(512)

    @staticmethod
    def INVERSENAME():
        return UaNodeAttributesMask(1024)

    @staticmethod
    def ISABSTRACT():
        return UaNodeAttributesMask(2048)

    @staticmethod
    def MINIMUMSAMPLINGINTERVAL():
        return UaNodeAttributesMask(4096)

    @staticmethod
    def NODECLASS():
        return UaNodeAttributesMask(8192)

    @staticmethod
    def NODEID():
        return UaNodeAttributesMask(16384)

    @staticmethod
    def SYMMETRIC():
        return UaNodeAttributesMask(32768)

    @staticmethod
    def USERACCESSLEVEL():
        return UaNodeAttributesMask(65536)

    @staticmethod
    def USEREXECUTABLE():
        return UaNodeAttributesMask(131072)

    @staticmethod
    def USERWRITEMASK():
        return UaNodeAttributesMask(262144)

    @staticmethod
    def VALUERANK():
        return UaNodeAttributesMask(524288)

    @staticmethod
    def WRITEMASK():
        return UaNodeAttributesMask(1048576)

    @staticmethod
    def VALUE():
        return UaNodeAttributesMask(2097152)

    @staticmethod
    def DATATYPEDEFINITION():
        return UaNodeAttributesMask(4194304)

    @staticmethod
    def ROLEPERMISSIONS():
        return UaNodeAttributesMask(8388608)

    @staticmethod
    def ACCESSRESTRICTIONS():
        return UaNodeAttributesMask(16777216)

    @staticmethod
    def ALL():
        return UaNodeAttributesMask(33554431)

    @staticmethod
    def BASENODE():
        return UaNodeAttributesMask(26501220)

    @staticmethod
    def OBJECT():
        return UaNodeAttributesMask(26501348)

    @staticmethod
    def OBJECTTYPE():
        return UaNodeAttributesMask(26503268)

    @staticmethod
    def VARIABLE():
        return UaNodeAttributesMask(26571383)

    @staticmethod
    def VARIABLETYPE():
        return UaNodeAttributesMask(28600438)

    @staticmethod
    def METHOD():
        return UaNodeAttributesMask(26632548)

    @staticmethod
    def REFERENCETYPE():
        return UaNodeAttributesMask(26537060)

    @staticmethod
    def VIEW():
        return UaNodeAttributesMask(26501356)

    @staticmethod
    def UA_NODEATTRIBUTESMASK_FORCE32BIT():
        return UaNodeAttributesMask(2147483647)

    def __str__(self, n=0):
        return f"(UaNodeAttributesMask): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaServerState +++++++++++++++++++++++
class UaServerState(UaType):
    _UA_TYPE = _UA_TYPES._SERVERSTATE

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

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_ServerState*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_ServerState*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_ServerState", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_ServerState")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def RUNNING():
        return UaServerState(0)

    @staticmethod
    def FAILED():
        return UaServerState(1)

    @staticmethod
    def NOCONFIGURATION():
        return UaServerState(2)

    @staticmethod
    def SUSPENDED():
        return UaServerState(3)

    @staticmethod
    def SHUTDOWN():
        return UaServerState(4)

    @staticmethod
    def TEST():
        return UaServerState(5)

    @staticmethod
    def COMMUNICATIONFAULT():
        return UaServerState(6)

    @staticmethod
    def UNKNOWN():
        return UaServerState(7)

    @staticmethod
    def UA_SERVERSTATE_FORCE32BIT():
        return UaServerState(2147483647)

    def __str__(self, n=0):
        return f"(UaServerState): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaFilterOperator +++++++++++++++++++++++
class UaFilterOperator(UaType):
    _UA_TYPE = _UA_TYPES._FILTEROPERATOR

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

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_FilterOperator*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_FilterOperator*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_FilterOperator", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_FilterOperator")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def EQUALS():
        return UaFilterOperator(0)

    @staticmethod
    def ISNULL():
        return UaFilterOperator(1)

    @staticmethod
    def GREATERTHAN():
        return UaFilterOperator(2)

    @staticmethod
    def LESSTHAN():
        return UaFilterOperator(3)

    @staticmethod
    def GREATERTHANOREQUAL():
        return UaFilterOperator(4)

    @staticmethod
    def LESSTHANOREQUAL():
        return UaFilterOperator(5)

    @staticmethod
    def LIKE():
        return UaFilterOperator(6)

    @staticmethod
    def NOT():
        return UaFilterOperator(7)

    @staticmethod
    def BETWEEN():
        return UaFilterOperator(8)

    @staticmethod
    def INLIST():
        return UaFilterOperator(9)

    @staticmethod
    def AND():
        return UaFilterOperator(10)

    @staticmethod
    def OR():
        return UaFilterOperator(11)

    @staticmethod
    def CAST():
        return UaFilterOperator(12)

    @staticmethod
    def INVIEW():
        return UaFilterOperator(13)

    @staticmethod
    def OFTYPE():
        return UaFilterOperator(14)

    @staticmethod
    def RELATEDTO():
        return UaFilterOperator(15)

    @staticmethod
    def BITWISEAND():
        return UaFilterOperator(16)

    @staticmethod
    def BITWISEOR():
        return UaFilterOperator(17)

    @staticmethod
    def UA_FILTEROPERATOR_FORCE32BIT():
        return UaFilterOperator(2147483647)

    def __str__(self, n=0):
        return f"(UaFilterOperator): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaRedundancySupport +++++++++++++++++++++++
class UaRedundancySupport(UaType):
    _UA_TYPE = _UA_TYPES._REDUNDANCYSUPPORT

    val_to_string = dict([
        (0, "UA_REDUNDANCYSUPPORT_NONE"),
        (1, "UA_REDUNDANCYSUPPORT_COLD"),
        (2, "UA_REDUNDANCYSUPPORT_WARM"),
        (3, "UA_REDUNDANCYSUPPORT_HOT"),
        (4, "UA_REDUNDANCYSUPPORT_TRANSPARENT"),
        (5, "UA_REDUNDANCYSUPPORT_HOTANDMIRRORED"),
        (2147483647, "__UA_REDUNDANCYSUPPORT_FORCE32BIT")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_RedundancySupport*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_RedundancySupport*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_RedundancySupport", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_RedundancySupport")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def NONE():
        return UaRedundancySupport(0)

    @staticmethod
    def COLD():
        return UaRedundancySupport(1)

    @staticmethod
    def WARM():
        return UaRedundancySupport(2)

    @staticmethod
    def HOT():
        return UaRedundancySupport(3)

    @staticmethod
    def TRANSPARENT():
        return UaRedundancySupport(4)

    @staticmethod
    def HOTANDMIRRORED():
        return UaRedundancySupport(5)

    @staticmethod
    def UA_REDUNDANCYSUPPORT_FORCE32BIT():
        return UaRedundancySupport(2147483647)

    def __str__(self, n=0):
        return f"(UaRedundancySupport): {self.val_to_string[self._val]} ({str(self._val)})\n"
