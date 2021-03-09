# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_base_types import *
from ua_types_parent import _ptr, _val


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

    def __str__(self, n=0):
        return f"(UaMessageSecurityMode): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaStructureType): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaMonitoringMode): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaBrowseResultMask): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaAxisScaleEnumeration): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaBrowseDirection): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaTimestampsToReturn): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaNodeClass): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaSecurityTokenRequestType +++++++++++++++++++++++
class UaSecurityTokenRequestType(UaType):
    UA_SECURITYTOKENREQUESTTYPE_ISSUE = 0
    UA_SECURITYTOKENREQUESTTYPE_RENEW = 1
    __UA_SECURITYTOKENREQUESTTYPE_FORCE32BIT = 2147483647

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

    def __str__(self, n=0):
        return f"(UaSecurityTokenRequestType): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaApplicationType): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaDeadbandType): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaDataChangeTrigger): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaUserTokenType): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaNodeAttributesMask): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaServerState): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaFilterOperator): {self.val_to_string[self._val]} ({str(self._val)})\n"


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

    def __str__(self, n=0):
        return f"(UaRedundancySupport): {self.val_to_string[self._val]} ({str(self._val)})\n"
