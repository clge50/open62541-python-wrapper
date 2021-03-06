# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_consts_types_raw import _UA_TYPES
from ua_types_generated_enums import *
from ua_types_parent import _ptr, _val, _is_null


# +++++++++++++++++++ UaViewAttributes +++++++++++++++++++++++
class UaViewAttributes(UaType):
    _UA_TYPE = _UA_TYPES._VIEWATTRIBUTES

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ViewAttributes*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ViewAttributes*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
            self._contains_no_loops = UaBoolean(val=val.containsNoLoops, is_pointer=False)
            self._event_notifier = UaByte(val=val.eventNotifier, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ViewAttributes")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._specified_attributes._value[0] = _val(val.specifiedAttributes)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._user_write_mask._value[0] = _val(val.userWriteMask)
            self._contains_no_loops._value[0] = _val(val.containsNoLoops)
            self._event_notifier._value[0] = _val(val.eventNotifier)

    @property
    def specified_attributes(self):
        if self._null:
            return None
        else:
            return self._specified_attributes

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def user_write_mask(self):
        if self._null:
            return None
        else:
            return self._user_write_mask

    @property
    def contains_no_loops(self):
        if self._null:
            return None
        else:
            return self._contains_no_loops

    @property
    def event_notifier(self):
        if self._null:
            return None
        else:
            return self._event_notifier

    @specified_attributes.setter
    def specified_attributes(self, val: UaUInt32):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @user_write_mask.setter
    def user_write_mask(self, val: UaUInt32):
        self._user_write_mask = val
        self._value.userWriteMask = val._val

    @contains_no_loops.setter
    def contains_no_loops(self, val: UaBoolean):
        self._contains_no_loops = val
        self._value.containsNoLoops = val._val

    @event_notifier.setter
    def event_notifier(self, val: UaByte):
        self._event_notifier = val
        self._value.eventNotifier = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaViewAttributes): NULL" + ("" if n is None else "\n")

        return ("(UaViewAttributes) :\n"
                + "\t" * (1 if n is None else n+1) + "specified_attributes " + self._specified_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_write_mask " + self._user_write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "contains_no_loops " + self._contains_no_loops.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "event_notifier " + self._event_notifier.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaXVType +++++++++++++++++++++++
class UaXVType(UaType):
    _UA_TYPE = _UA_TYPES._XVTYPE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_XVType*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_XVType*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._x = UaDouble(val=val.x, is_pointer=False)
            self._data_value = UaFloat(val=val.value, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_XVType")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._x._value[0] = _val(val.x)
            self._data_value._value[0] = _val(val.value)

    @property
    def x(self):
        if self._null:
            return None
        else:
            return self._x

    @property
    def data_value(self):
        if self._null:
            return None
        else:
            return self._data_value

    @x.setter
    def x(self, val: UaDouble):
        self._x = val
        self._value.x = val._val

    @data_value.setter
    def data_value(self, val: UaFloat):
        self._data_value = val
        self._value.value = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaXVType): NULL" + ("" if n is None else "\n")

        return ("(UaXVType) :\n"
                + "\t" * (1 if n is None else n+1) + "x " + self._x.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_value " + self._data_value.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaElementOperand +++++++++++++++++++++++
class UaElementOperand(UaType):
    _UA_TYPE = _UA_TYPES._ELEMENTOPERAND

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ElementOperand*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ElementOperand*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._index = UaUInt32(val=val.index, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ElementOperand")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._index._value[0] = _val(val.index)

    @property
    def index(self):
        if self._null:
            return None
        else:
            return self._index

    @index.setter
    def index(self, val: UaUInt32):
        self._index = val
        self._value.index = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaElementOperand): NULL" + ("" if n is None else "\n")

        return ("(UaElementOperand) :\n"
                + "\t" * (1 if n is None else n+1) + "index " + self._index.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaVariableAttributes +++++++++++++++++++++++
class UaVariableAttributes(UaType):
    _UA_TYPE = _UA_TYPES._VARIABLEATTRIBUTES

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_VariableAttributes*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_VariableAttributes*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
            self._data_value = UaVariant(val=val.value, is_pointer=False)
            self._data_type = UaNodeId(val=val.dataType, is_pointer=False)
            self._value_rank = UaInt32(val=val.valueRank, is_pointer=False)
            self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
            self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
            self._access_level = UaByte(val=val.accessLevel, is_pointer=False)
            self._user_access_level = UaByte(val=val.userAccessLevel, is_pointer=False)
            self._minimum_sampling_interval = UaDouble(val=val.minimumSamplingInterval, is_pointer=False)
            self._historizing = UaBoolean(val=val.historizing, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_VariableAttributes")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._specified_attributes._value[0] = _val(val.specifiedAttributes)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._user_write_mask._value[0] = _val(val.userWriteMask)
            self._data_value._value[0] = _val(val.value)
            self._data_type._value[0] = _val(val.dataType)
            self._value_rank._value[0] = _val(val.valueRank)
            self._array_dimensions_size._value[0] = _val(val.arrayDimensionsSize)
            self._array_dimensions._value = val.arrayDimensions
            self._access_level._value[0] = _val(val.accessLevel)
            self._user_access_level._value[0] = _val(val.userAccessLevel)
            self._minimum_sampling_interval._value[0] = _val(val.minimumSamplingInterval)
            self._historizing._value[0] = _val(val.historizing)

    @property
    def specified_attributes(self):
        if self._null:
            return None
        else:
            return self._specified_attributes

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def user_write_mask(self):
        if self._null:
            return None
        else:
            return self._user_write_mask

    @property
    def data_value(self):
        if self._null:
            return None
        else:
            return self._data_value

    @property
    def data_type(self):
        if self._null:
            return None
        else:
            return self._data_type

    @property
    def value_rank(self):
        if self._null:
            return None
        else:
            return self._value_rank

    @property
    def array_dimensions_size(self):
        if self._null:
            return None
        else:
            return self._array_dimensions_size

    @property
    def array_dimensions(self):
        if self._null:
            return None
        else:
            return self._array_dimensions

    @property
    def access_level(self):
        if self._null:
            return None
        else:
            return self._access_level

    @property
    def user_access_level(self):
        if self._null:
            return None
        else:
            return self._user_access_level

    @property
    def minimum_sampling_interval(self):
        if self._null:
            return None
        else:
            return self._minimum_sampling_interval

    @property
    def historizing(self):
        if self._null:
            return None
        else:
            return self._historizing

    @specified_attributes.setter
    def specified_attributes(self, val: UaUInt32):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @user_write_mask.setter
    def user_write_mask(self, val: UaUInt32):
        self._user_write_mask = val
        self._value.userWriteMask = val._val

    @data_value.setter
    def data_value(self, val: UaVariant):
        self._data_value = val
        self._value.value = val._val

    @data_type.setter
    def data_type(self, val: UaNodeId):
        self._data_type = val
        self._value.dataType = val._val

    @value_rank.setter
    def value_rank(self, val: UaInt32):
        self._value_rank = val
        self._value.valueRank = val._val

    @array_dimensions_size.setter
    def array_dimensions_size(self, val: SizeT):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._val

    @array_dimensions.setter
    def array_dimensions(self, val: UaUInt32):
        self._array_dimensions = val
        self._value.arrayDimensions = val._ptr

    @access_level.setter
    def access_level(self, val: UaByte):
        self._access_level = val
        self._value.accessLevel = val._val

    @user_access_level.setter
    def user_access_level(self, val: UaByte):
        self._user_access_level = val
        self._value.userAccessLevel = val._val

    @minimum_sampling_interval.setter
    def minimum_sampling_interval(self, val: UaDouble):
        self._minimum_sampling_interval = val
        self._value.minimumSamplingInterval = val._val

    @historizing.setter
    def historizing(self, val: UaBoolean):
        self._historizing = val
        self._value.historizing = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaVariableAttributes): NULL" + ("" if n is None else "\n")

        return ("(UaVariableAttributes) :\n"
                + "\t" * (1 if n is None else n+1) + "specified_attributes " + self._specified_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_write_mask " + self._user_write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_value " + self._data_value.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_type " + self._data_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "value_rank " + self._value_rank.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "array_dimensions_size " + self._array_dimensions_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "array_dimensions " + self._array_dimensions.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "access_level " + self._access_level.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_access_level " + self._user_access_level.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "minimum_sampling_interval " + self._minimum_sampling_interval.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "historizing " + self._historizing.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaEnumValueType +++++++++++++++++++++++
class UaEnumValueType(UaType):
    _UA_TYPE = _UA_TYPES._ENUMVALUETYPE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_EnumValueType*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_EnumValueType*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._data_value = UaInt64(val=val.value, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_EnumValueType")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._data_value._value[0] = _val(val.value)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)

    @property
    def data_value(self):
        if self._null:
            return None
        else:
            return self._data_value

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @data_value.setter
    def data_value(self, val: UaInt64):
        self._data_value = val
        self._value.value = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaEnumValueType): NULL" + ("" if n is None else "\n")

        return ("(UaEnumValueType) :\n"
                + "\t" * (1 if n is None else n+1) + "data_value " + self._data_value.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaEventFieldList +++++++++++++++++++++++
class UaEventFieldList(UaType):
    _UA_TYPE = _UA_TYPES._EVENTFIELDLIST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_EventFieldList*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_EventFieldList*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._client_handle = UaUInt32(val=val.clientHandle, is_pointer=False)
            self._event_fields_size = SizeT(val=val.eventFieldsSize, is_pointer=False)
            self._event_fields = UaVariant(val=val.eventFields, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_EventFieldList")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._client_handle._value[0] = _val(val.clientHandle)
            self._event_fields_size._value[0] = _val(val.eventFieldsSize)
            self._event_fields._value = val.eventFields

    @property
    def client_handle(self):
        if self._null:
            return None
        else:
            return self._client_handle

    @property
    def event_fields_size(self):
        if self._null:
            return None
        else:
            return self._event_fields_size

    @property
    def event_fields(self):
        if self._null:
            return None
        else:
            return self._event_fields

    @client_handle.setter
    def client_handle(self, val: UaUInt32):
        self._client_handle = val
        self._value.clientHandle = val._val

    @event_fields_size.setter
    def event_fields_size(self, val: SizeT):
        self._event_fields_size = val
        self._value.eventFieldsSize = val._val

    @event_fields.setter
    def event_fields(self, val: UaVariant):
        self._event_fields = val
        self._value.eventFields = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaEventFieldList): NULL" + ("" if n is None else "\n")

        return ("(UaEventFieldList) :\n"
                + "\t" * (1 if n is None else n+1) + "client_handle " + self._client_handle.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "event_fields_size " + self._event_fields_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "event_fields " + self._event_fields.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaMonitoredItemCreateResult +++++++++++++++++++++++
class UaMonitoredItemCreateResult(UaType):
    _UA_TYPE = _UA_TYPES._MONITOREDITEMCREATERESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_MonitoredItemCreateResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_MonitoredItemCreateResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
            self._monitored_item_id = UaUInt32(val=val.monitoredItemId, is_pointer=False)
            self._revised_sampling_interval = UaDouble(val=val.revisedSamplingInterval, is_pointer=False)
            self._revised_queue_size = UaUInt32(val=val.revisedQueueSize, is_pointer=False)
            self._filter_result = UaExtensionObject(val=val.filterResult, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_MonitoredItemCreateResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._status_code._value[0] = _val(val.statusCode)
            self._monitored_item_id._value[0] = _val(val.monitoredItemId)
            self._revised_sampling_interval._value[0] = _val(val.revisedSamplingInterval)
            self._revised_queue_size._value[0] = _val(val.revisedQueueSize)
            self._filter_result._value[0] = _val(val.filterResult)

    @property
    def status_code(self):
        if self._null:
            return None
        else:
            return self._status_code

    @property
    def monitored_item_id(self):
        if self._null:
            return None
        else:
            return self._monitored_item_id

    @property
    def revised_sampling_interval(self):
        if self._null:
            return None
        else:
            return self._revised_sampling_interval

    @property
    def revised_queue_size(self):
        if self._null:
            return None
        else:
            return self._revised_queue_size

    @property
    def filter_result(self):
        if self._null:
            return None
        else:
            return self._filter_result

    @status_code.setter
    def status_code(self, val: UaStatusCode):
        self._status_code = val
        self._value.statusCode = val._val

    @monitored_item_id.setter
    def monitored_item_id(self, val: UaUInt32):
        self._monitored_item_id = val
        self._value.monitoredItemId = val._val

    @revised_sampling_interval.setter
    def revised_sampling_interval(self, val: UaDouble):
        self._revised_sampling_interval = val
        self._value.revisedSamplingInterval = val._val

    @revised_queue_size.setter
    def revised_queue_size(self, val: UaUInt32):
        self._revised_queue_size = val
        self._value.revisedQueueSize = val._val

    @filter_result.setter
    def filter_result(self, val: UaExtensionObject):
        self._filter_result = val
        self._value.filterResult = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaMonitoredItemCreateResult): NULL" + ("" if n is None else "\n")

        return ("(UaMonitoredItemCreateResult) :\n"
                + "\t" * (1 if n is None else n+1) + "status_code " + self._status_code.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "monitored_item_id " + self._monitored_item_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_sampling_interval " + self._revised_sampling_interval.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_queue_size " + self._revised_queue_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "filter_result " + self._filter_result.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaEUInformation +++++++++++++++++++++++
class UaEUInformation(UaType):
    _UA_TYPE = _UA_TYPES._EUINFORMATION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_EUInformation*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_EUInformation*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._namespace_uri = UaString(val=val.namespaceUri, is_pointer=False)
            self._unit_id = UaInt32(val=val.unitId, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_EUInformation")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._namespace_uri._value[0] = _val(val.namespaceUri)
            self._unit_id._value[0] = _val(val.unitId)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)

    @property
    def namespace_uri(self):
        if self._null:
            return None
        else:
            return self._namespace_uri

    @property
    def unit_id(self):
        if self._null:
            return None
        else:
            return self._unit_id

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @namespace_uri.setter
    def namespace_uri(self, val: UaString):
        self._namespace_uri = val
        self._value.namespaceUri = val._val

    @unit_id.setter
    def unit_id(self, val: UaInt32):
        self._unit_id = val
        self._value.unitId = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaEUInformation): NULL" + ("" if n is None else "\n")

        return ("(UaEUInformation) :\n"
                + "\t" * (1 if n is None else n+1) + "namespace_uri " + self._namespace_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "unit_id " + self._unit_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaServerDiagnosticsSummaryDataType +++++++++++++++++++++++
class UaServerDiagnosticsSummaryDataType(UaType):
    _UA_TYPE = _UA_TYPES._SERVERDIAGNOSTICSSUMMARYDATATYPE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ServerDiagnosticsSummaryDataType*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ServerDiagnosticsSummaryDataType*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
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

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ServerDiagnosticsSummaryDataType")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._server_view_count._value[0] = _val(val.serverViewCount)
            self._current_session_count._value[0] = _val(val.currentSessionCount)
            self._cumulated_session_count._value[0] = _val(val.cumulatedSessionCount)
            self._security_rejected_session_count._value[0] = _val(val.securityRejectedSessionCount)
            self._rejected_session_count._value[0] = _val(val.rejectedSessionCount)
            self._session_timeout_count._value[0] = _val(val.sessionTimeoutCount)
            self._session_abort_count._value[0] = _val(val.sessionAbortCount)
            self._current_subscription_count._value[0] = _val(val.currentSubscriptionCount)
            self._cumulated_subscription_count._value[0] = _val(val.cumulatedSubscriptionCount)
            self._publishing_interval_count._value[0] = _val(val.publishingIntervalCount)
            self._security_rejected_requests_count._value[0] = _val(val.securityRejectedRequestsCount)
            self._rejected_requests_count._value[0] = _val(val.rejectedRequestsCount)

    @property
    def server_view_count(self):
        if self._null:
            return None
        else:
            return self._server_view_count

    @property
    def current_session_count(self):
        if self._null:
            return None
        else:
            return self._current_session_count

    @property
    def cumulated_session_count(self):
        if self._null:
            return None
        else:
            return self._cumulated_session_count

    @property
    def security_rejected_session_count(self):
        if self._null:
            return None
        else:
            return self._security_rejected_session_count

    @property
    def rejected_session_count(self):
        if self._null:
            return None
        else:
            return self._rejected_session_count

    @property
    def session_timeout_count(self):
        if self._null:
            return None
        else:
            return self._session_timeout_count

    @property
    def session_abort_count(self):
        if self._null:
            return None
        else:
            return self._session_abort_count

    @property
    def current_subscription_count(self):
        if self._null:
            return None
        else:
            return self._current_subscription_count

    @property
    def cumulated_subscription_count(self):
        if self._null:
            return None
        else:
            return self._cumulated_subscription_count

    @property
    def publishing_interval_count(self):
        if self._null:
            return None
        else:
            return self._publishing_interval_count

    @property
    def security_rejected_requests_count(self):
        if self._null:
            return None
        else:
            return self._security_rejected_requests_count

    @property
    def rejected_requests_count(self):
        if self._null:
            return None
        else:
            return self._rejected_requests_count

    @server_view_count.setter
    def server_view_count(self, val: UaUInt32):
        self._server_view_count = val
        self._value.serverViewCount = val._val

    @current_session_count.setter
    def current_session_count(self, val: UaUInt32):
        self._current_session_count = val
        self._value.currentSessionCount = val._val

    @cumulated_session_count.setter
    def cumulated_session_count(self, val: UaUInt32):
        self._cumulated_session_count = val
        self._value.cumulatedSessionCount = val._val

    @security_rejected_session_count.setter
    def security_rejected_session_count(self, val: UaUInt32):
        self._security_rejected_session_count = val
        self._value.securityRejectedSessionCount = val._val

    @rejected_session_count.setter
    def rejected_session_count(self, val: UaUInt32):
        self._rejected_session_count = val
        self._value.rejectedSessionCount = val._val

    @session_timeout_count.setter
    def session_timeout_count(self, val: UaUInt32):
        self._session_timeout_count = val
        self._value.sessionTimeoutCount = val._val

    @session_abort_count.setter
    def session_abort_count(self, val: UaUInt32):
        self._session_abort_count = val
        self._value.sessionAbortCount = val._val

    @current_subscription_count.setter
    def current_subscription_count(self, val: UaUInt32):
        self._current_subscription_count = val
        self._value.currentSubscriptionCount = val._val

    @cumulated_subscription_count.setter
    def cumulated_subscription_count(self, val: UaUInt32):
        self._cumulated_subscription_count = val
        self._value.cumulatedSubscriptionCount = val._val

    @publishing_interval_count.setter
    def publishing_interval_count(self, val: UaUInt32):
        self._publishing_interval_count = val
        self._value.publishingIntervalCount = val._val

    @security_rejected_requests_count.setter
    def security_rejected_requests_count(self, val: UaUInt32):
        self._security_rejected_requests_count = val
        self._value.securityRejectedRequestsCount = val._val

    @rejected_requests_count.setter
    def rejected_requests_count(self, val: UaUInt32):
        self._rejected_requests_count = val
        self._value.rejectedRequestsCount = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaServerDiagnosticsSummaryDataType): NULL" + ("" if n is None else "\n")

        return ("(UaServerDiagnosticsSummaryDataType) :\n"
                + "\t" * (1 if n is None else n+1) + "server_view_count " + self._server_view_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "current_session_count " + self._current_session_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "cumulated_session_count " + self._cumulated_session_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_rejected_session_count " + self._security_rejected_session_count.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "rejected_session_count " + self._rejected_session_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "session_timeout_count " + self._session_timeout_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "session_abort_count " + self._session_abort_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "current_subscription_count " + self._current_subscription_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "cumulated_subscription_count " + self._cumulated_subscription_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "publishing_interval_count " + self._publishing_interval_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_rejected_requests_count " + self._security_rejected_requests_count.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "rejected_requests_count " + self._rejected_requests_count.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaContentFilterElementResult +++++++++++++++++++++++
class UaContentFilterElementResult(UaType):
    _UA_TYPE = _UA_TYPES._CONTENTFILTERELEMENTRESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ContentFilterElementResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ContentFilterElementResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
            self._operand_status_codes_size = SizeT(val=val.operandStatusCodesSize, is_pointer=False)
            self._operand_status_codes = UaStatusCode(val=val.operandStatusCodes, is_pointer=True)
            self._operand_diagnostic_infos_size = SizeT(val=val.operandDiagnosticInfosSize, is_pointer=False)
            self._operand_diagnostic_infos = UaDiagnosticInfo(val=val.operandDiagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ContentFilterElementResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._status_code._value[0] = _val(val.statusCode)
            self._operand_status_codes_size._value[0] = _val(val.operandStatusCodesSize)
            self._operand_status_codes._value = val.operandStatusCodes
            self._operand_diagnostic_infos_size._value[0] = _val(val.operandDiagnosticInfosSize)
            self._operand_diagnostic_infos._value = val.operandDiagnosticInfos

    @property
    def status_code(self):
        if self._null:
            return None
        else:
            return self._status_code

    @property
    def operand_status_codes_size(self):
        if self._null:
            return None
        else:
            return self._operand_status_codes_size

    @property
    def operand_status_codes(self):
        if self._null:
            return None
        else:
            return self._operand_status_codes

    @property
    def operand_diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._operand_diagnostic_infos_size

    @property
    def operand_diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._operand_diagnostic_infos

    @status_code.setter
    def status_code(self, val: UaStatusCode):
        self._status_code = val
        self._value.statusCode = val._val

    @operand_status_codes_size.setter
    def operand_status_codes_size(self, val: SizeT):
        self._operand_status_codes_size = val
        self._value.operandStatusCodesSize = val._val

    @operand_status_codes.setter
    def operand_status_codes(self, val: UaStatusCode):
        self._operand_status_codes = val
        self._value.operandStatusCodes = val._ptr

    @operand_diagnostic_infos_size.setter
    def operand_diagnostic_infos_size(self, val: SizeT):
        self._operand_diagnostic_infos_size = val
        self._value.operandDiagnosticInfosSize = val._val

    @operand_diagnostic_infos.setter
    def operand_diagnostic_infos(self, val: UaDiagnosticInfo):
        self._operand_diagnostic_infos = val
        self._value.operandDiagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaContentFilterElementResult): NULL" + ("" if n is None else "\n")

        return ("(UaContentFilterElementResult) :\n"
                + "\t" * (1 if n is None else n+1) + "status_code " + self._status_code.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "operand_status_codes_size " + self._operand_status_codes_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "operand_status_codes " + self._operand_status_codes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "operand_diagnostic_infos_size " + self._operand_diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "operand_diagnostic_infos " + self._operand_diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaLiteralOperand +++++++++++++++++++++++
class UaLiteralOperand(UaType):
    _UA_TYPE = _UA_TYPES._LITERALOPERAND

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_LiteralOperand*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_LiteralOperand*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._data_value = UaVariant(val=val.value, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_LiteralOperand")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._data_value._value[0] = _val(val.value)

    @property
    def data_value(self):
        if self._null:
            return None
        else:
            return self._data_value

    @data_value.setter
    def data_value(self, val: UaVariant):
        self._data_value = val
        self._value.value = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaLiteralOperand): NULL" + ("" if n is None else "\n")

        return ("(UaLiteralOperand) :\n"
                + "\t" * (1 if n is None else n+1) + "data_value " + self._data_value.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaUserIdentityToken +++++++++++++++++++++++
class UaUserIdentityToken(UaType):
    _UA_TYPE = _UA_TYPES._USERIDENTITYTOKEN

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_UserIdentityToken*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_UserIdentityToken*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._policy_id = UaString(val=val.policyId, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UserIdentityToken")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._policy_id._value[0] = _val(val.policyId)

    @property
    def policy_id(self):
        if self._null:
            return None
        else:
            return self._policy_id

    @policy_id.setter
    def policy_id(self, val: UaString):
        self._policy_id = val
        self._value.policyId = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaUserIdentityToken): NULL" + ("" if n is None else "\n")

        return ("(UaUserIdentityToken) :\n"
                + "\t" * (1 if n is None else n+1) + "policy_id " + self._policy_id.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaX509IdentityToken +++++++++++++++++++++++
class UaX509IdentityToken(UaType):
    _UA_TYPE = _UA_TYPES._X509IDENTITYTOKEN

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_X509IdentityToken*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_X509IdentityToken*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._policy_id = UaString(val=val.policyId, is_pointer=False)
            self._certificate_data = UaByteString(val=val.certificateData, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_X509IdentityToken")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._policy_id._value[0] = _val(val.policyId)
            self._certificate_data._value[0] = _val(val.certificateData)

    @property
    def policy_id(self):
        if self._null:
            return None
        else:
            return self._policy_id

    @property
    def certificate_data(self):
        if self._null:
            return None
        else:
            return self._certificate_data

    @policy_id.setter
    def policy_id(self, val: UaString):
        self._policy_id = val
        self._value.policyId = val._val

    @certificate_data.setter
    def certificate_data(self, val: UaByteString):
        self._certificate_data = val
        self._value.certificateData = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaX509IdentityToken): NULL" + ("" if n is None else "\n")

        return ("(UaX509IdentityToken) :\n"
                + "\t" * (1 if n is None else n+1) + "policy_id " + self._policy_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "certificate_data " + self._certificate_data.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaMonitoredItemNotification +++++++++++++++++++++++
class UaMonitoredItemNotification(UaType):
    _UA_TYPE = _UA_TYPES._MONITOREDITEMNOTIFICATION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_MonitoredItemNotification*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_MonitoredItemNotification*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._client_handle = UaUInt32(val=val.clientHandle, is_pointer=False)
            self._data_value = UaDataValue(val=val.value, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_MonitoredItemNotification")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._client_handle._value[0] = _val(val.clientHandle)
            self._data_value._value[0] = _val(val.value)

    @property
    def client_handle(self):
        if self._null:
            return None
        else:
            return self._client_handle

    @property
    def data_value(self):
        if self._null:
            return None
        else:
            return self._data_value

    @client_handle.setter
    def client_handle(self, val: UaUInt32):
        self._client_handle = val
        self._value.clientHandle = val._val

    @data_value.setter
    def data_value(self, val: UaDataValue):
        self._data_value = val
        self._value.value = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaMonitoredItemNotification): NULL" + ("" if n is None else "\n")

        return ("(UaMonitoredItemNotification) :\n"
                + "\t" * (1 if n is None else n+1) + "client_handle " + self._client_handle.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_value " + self._data_value.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaResponseHeader +++++++++++++++++++++++
class UaResponseHeader(UaType):
    _UA_TYPE = _UA_TYPES._RESPONSEHEADER

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ResponseHeader*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ResponseHeader*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._timestamp = UaDateTime(val=val.timestamp, is_pointer=False)
            self._request_handle = UaUInt32(val=val.requestHandle, is_pointer=False)
            self._service_result = UaStatusCode(val=val.serviceResult, is_pointer=False)
            self._service_diagnostics = UaDiagnosticInfo(val=val.serviceDiagnostics, is_pointer=False)
            self._string_table_size = SizeT(val=val.stringTableSize, is_pointer=False)
            self._string_table = UaString(val=val.stringTable, is_pointer=True)
            self._additional_header = UaExtensionObject(val=val.additionalHeader, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ResponseHeader")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._timestamp._value[0] = _val(val.timestamp)
            self._request_handle._value[0] = _val(val.requestHandle)
            self._service_result._value[0] = _val(val.serviceResult)
            self._service_diagnostics._value[0] = _val(val.serviceDiagnostics)
            self._string_table_size._value[0] = _val(val.stringTableSize)
            self._string_table._value = val.stringTable
            self._additional_header._value[0] = _val(val.additionalHeader)

    @property
    def timestamp(self):
        if self._null:
            return None
        else:
            return self._timestamp

    @property
    def request_handle(self):
        if self._null:
            return None
        else:
            return self._request_handle

    @property
    def service_result(self):
        if self._null:
            return None
        else:
            return self._service_result

    @property
    def service_diagnostics(self):
        if self._null:
            return None
        else:
            return self._service_diagnostics

    @property
    def string_table_size(self):
        if self._null:
            return None
        else:
            return self._string_table_size

    @property
    def string_table(self):
        if self._null:
            return None
        else:
            return self._string_table

    @property
    def additional_header(self):
        if self._null:
            return None
        else:
            return self._additional_header

    @timestamp.setter
    def timestamp(self, val: UaDateTime):
        self._timestamp = val
        self._value.timestamp = val._val

    @request_handle.setter
    def request_handle(self, val: UaUInt32):
        self._request_handle = val
        self._value.requestHandle = val._val

    @service_result.setter
    def service_result(self, val: UaStatusCode):
        self._service_result = val
        self._value.serviceResult = val._val

    @service_diagnostics.setter
    def service_diagnostics(self, val: UaDiagnosticInfo):
        self._service_diagnostics = val
        self._value.serviceDiagnostics = val._val

    @string_table_size.setter
    def string_table_size(self, val: SizeT):
        self._string_table_size = val
        self._value.stringTableSize = val._val

    @string_table.setter
    def string_table(self, val: UaString):
        self._string_table = val
        self._value.stringTable = val._ptr

    @additional_header.setter
    def additional_header(self, val: UaExtensionObject):
        self._additional_header = val
        self._value.additionalHeader = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaResponseHeader): NULL" + ("" if n is None else "\n")

        return ("(UaResponseHeader) :\n"
                + "\t" * (1 if n is None else n+1) + "timestamp " + self._timestamp.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "request_handle " + self._request_handle.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "service_result " + self._service_result.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "service_diagnostics " + self._service_diagnostics.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "string_table_size " + self._string_table_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "string_table " + self._string_table.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "additional_header " + self._additional_header.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSignatureData +++++++++++++++++++++++
class UaSignatureData(UaType):
    _UA_TYPE = _UA_TYPES._SIGNATUREDATA

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SignatureData*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SignatureData*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._algorithm = UaString(val=val.algorithm, is_pointer=False)
            self._signature = UaByteString(val=val.signature, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SignatureData")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._algorithm._value[0] = _val(val.algorithm)
            self._signature._value[0] = _val(val.signature)

    @property
    def algorithm(self):
        if self._null:
            return None
        else:
            return self._algorithm

    @property
    def signature(self):
        if self._null:
            return None
        else:
            return self._signature

    @algorithm.setter
    def algorithm(self, val: UaString):
        self._algorithm = val
        self._value.algorithm = val._val

    @signature.setter
    def signature(self, val: UaByteString):
        self._signature = val
        self._value.signature = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaSignatureData): NULL" + ("" if n is None else "\n")

        return ("(UaSignatureData) :\n"
                + "\t" * (1 if n is None else n+1) + "algorithm " + self._algorithm.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "signature " + self._signature.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaModifySubscriptionResponse +++++++++++++++++++++++
class UaModifySubscriptionResponse(UaType):
    _UA_TYPE = _UA_TYPES._MODIFYSUBSCRIPTIONRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ModifySubscriptionResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ModifySubscriptionResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._revised_publishing_interval = UaDouble(val=val.revisedPublishingInterval, is_pointer=False)
            self._revised_lifetime_count = UaUInt32(val=val.revisedLifetimeCount, is_pointer=False)
            self._revised_max_keep_alive_count = UaUInt32(val=val.revisedMaxKeepAliveCount, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ModifySubscriptionResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._revised_publishing_interval._value[0] = _val(val.revisedPublishingInterval)
            self._revised_lifetime_count._value[0] = _val(val.revisedLifetimeCount)
            self._revised_max_keep_alive_count._value[0] = _val(val.revisedMaxKeepAliveCount)

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def revised_publishing_interval(self):
        if self._null:
            return None
        else:
            return self._revised_publishing_interval

    @property
    def revised_lifetime_count(self):
        if self._null:
            return None
        else:
            return self._revised_lifetime_count

    @property
    def revised_max_keep_alive_count(self):
        if self._null:
            return None
        else:
            return self._revised_max_keep_alive_count

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @revised_publishing_interval.setter
    def revised_publishing_interval(self, val: UaDouble):
        self._revised_publishing_interval = val
        self._value.revisedPublishingInterval = val._val

    @revised_lifetime_count.setter
    def revised_lifetime_count(self, val: UaUInt32):
        self._revised_lifetime_count = val
        self._value.revisedLifetimeCount = val._val

    @revised_max_keep_alive_count.setter
    def revised_max_keep_alive_count(self, val: UaUInt32):
        self._revised_max_keep_alive_count = val
        self._value.revisedMaxKeepAliveCount = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaModifySubscriptionResponse): NULL" + ("" if n is None else "\n")

        return ("(UaModifySubscriptionResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_publishing_interval " + self._revised_publishing_interval.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_lifetime_count " + self._revised_lifetime_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_max_keep_alive_count " + self._revised_max_keep_alive_count.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaNodeAttributes +++++++++++++++++++++++
class UaNodeAttributes(UaType):
    _UA_TYPE = _UA_TYPES._NODEATTRIBUTES

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NodeAttributes*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_NodeAttributes*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NodeAttributes")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._specified_attributes._value[0] = _val(val.specifiedAttributes)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._user_write_mask._value[0] = _val(val.userWriteMask)

    @property
    def specified_attributes(self):
        if self._null:
            return None
        else:
            return self._specified_attributes

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def user_write_mask(self):
        if self._null:
            return None
        else:
            return self._user_write_mask

    @specified_attributes.setter
    def specified_attributes(self, val: UaUInt32):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @user_write_mask.setter
    def user_write_mask(self, val: UaUInt32):
        self._user_write_mask = val
        self._value.userWriteMask = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaNodeAttributes): NULL" + ("" if n is None else "\n")

        return ("(UaNodeAttributes) :\n"
                + "\t" * (1 if n is None else n+1) + "specified_attributes " + self._specified_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_write_mask " + self._user_write_mask.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaActivateSessionResponse +++++++++++++++++++++++
class UaActivateSessionResponse(UaType):
    _UA_TYPE = _UA_TYPES._ACTIVATESESSIONRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ActivateSessionResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ActivateSessionResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._server_nonce = UaByteString(val=val.serverNonce, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaStatusCode(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ActivateSessionResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._server_nonce._value[0] = _val(val.serverNonce)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def server_nonce(self):
        if self._null:
            return None
        else:
            return self._server_nonce

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @server_nonce.setter
    def server_nonce(self, val: UaByteString):
        self._server_nonce = val
        self._value.serverNonce = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaActivateSessionResponse): NULL" + ("" if n is None else "\n")

        return ("(UaActivateSessionResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_nonce " + self._server_nonce.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaEnumField +++++++++++++++++++++++
class UaEnumField(UaType):
    _UA_TYPE = _UA_TYPES._ENUMFIELD

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_EnumField*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_EnumField*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._data_value = UaInt64(val=val.value, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._name = UaString(val=val.name, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_EnumField")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._data_value._value[0] = _val(val.value)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._name._value[0] = _val(val.name)

    @property
    def data_value(self):
        if self._null:
            return None
        else:
            return self._data_value

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def name(self):
        if self._null:
            return None
        else:
            return self._name

    @data_value.setter
    def data_value(self, val: UaInt64):
        self._data_value = val
        self._value.value = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @name.setter
    def name(self, val: UaString):
        self._name = val
        self._value.name = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaEnumField): NULL" + ("" if n is None else "\n")

        return ("(UaEnumField) :\n"
                + "\t" * (1 if n is None else n+1) + "data_value " + self._data_value.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "name " + self._name.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaVariableTypeAttributes +++++++++++++++++++++++
class UaVariableTypeAttributes(UaType):
    _UA_TYPE = _UA_TYPES._VARIABLETYPEATTRIBUTES

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_VariableTypeAttributes*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_VariableTypeAttributes*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
            self._data_value = UaVariant(val=val.value, is_pointer=False)
            self._data_type = UaNodeId(val=val.dataType, is_pointer=False)
            self._value_rank = UaInt32(val=val.valueRank, is_pointer=False)
            self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
            self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
            self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_VariableTypeAttributes")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._specified_attributes._value[0] = _val(val.specifiedAttributes)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._user_write_mask._value[0] = _val(val.userWriteMask)
            self._data_value._value[0] = _val(val.value)
            self._data_type._value[0] = _val(val.dataType)
            self._value_rank._value[0] = _val(val.valueRank)
            self._array_dimensions_size._value[0] = _val(val.arrayDimensionsSize)
            self._array_dimensions._value = val.arrayDimensions
            self._is_abstract._value[0] = _val(val.isAbstract)

    @property
    def specified_attributes(self):
        if self._null:
            return None
        else:
            return self._specified_attributes

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def user_write_mask(self):
        if self._null:
            return None
        else:
            return self._user_write_mask

    @property
    def data_value(self):
        if self._null:
            return None
        else:
            return self._data_value

    @property
    def data_type(self):
        if self._null:
            return None
        else:
            return self._data_type

    @property
    def value_rank(self):
        if self._null:
            return None
        else:
            return self._value_rank

    @property
    def array_dimensions_size(self):
        if self._null:
            return None
        else:
            return self._array_dimensions_size

    @property
    def array_dimensions(self):
        if self._null:
            return None
        else:
            return self._array_dimensions

    @property
    def is_abstract(self):
        if self._null:
            return None
        else:
            return self._is_abstract

    @specified_attributes.setter
    def specified_attributes(self, val: UaUInt32):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @user_write_mask.setter
    def user_write_mask(self, val: UaUInt32):
        self._user_write_mask = val
        self._value.userWriteMask = val._val

    @data_value.setter
    def data_value(self, val: UaVariant):
        self._data_value = val
        self._value.value = val._val

    @data_type.setter
    def data_type(self, val: UaNodeId):
        self._data_type = val
        self._value.dataType = val._val

    @value_rank.setter
    def value_rank(self, val: UaInt32):
        self._value_rank = val
        self._value.valueRank = val._val

    @array_dimensions_size.setter
    def array_dimensions_size(self, val: SizeT):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._val

    @array_dimensions.setter
    def array_dimensions(self, val: UaUInt32):
        self._array_dimensions = val
        self._value.arrayDimensions = val._ptr

    @is_abstract.setter
    def is_abstract(self, val: UaBoolean):
        self._is_abstract = val
        self._value.isAbstract = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaVariableTypeAttributes): NULL" + ("" if n is None else "\n")

        return ("(UaVariableTypeAttributes) :\n"
                + "\t" * (1 if n is None else n+1) + "specified_attributes " + self._specified_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_write_mask " + self._user_write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_value " + self._data_value.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_type " + self._data_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "value_rank " + self._value_rank.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "array_dimensions_size " + self._array_dimensions_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "array_dimensions " + self._array_dimensions.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_abstract " + self._is_abstract.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCallMethodResult +++++++++++++++++++++++
class UaCallMethodResult(UaType):
    _UA_TYPE = _UA_TYPES._CALLMETHODRESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CallMethodResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CallMethodResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
            self._input_argument_results_size = SizeT(val=val.inputArgumentResultsSize, is_pointer=False)
            self._input_argument_results = UaStatusCode(val=val.inputArgumentResults, is_pointer=True)
            self._input_argument_diagnostic_infos_size = SizeT(val=val.inputArgumentDiagnosticInfosSize,
                                                               is_pointer=False)
            self._input_argument_diagnostic_infos = UaDiagnosticInfo(val=val.inputArgumentDiagnosticInfos,
                                                                     is_pointer=True)
            self._output_arguments_size = SizeT(val=val.outputArgumentsSize, is_pointer=False)
            self._output_arguments = UaVariant(val=val.outputArguments, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CallMethodResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._status_code._value[0] = _val(val.statusCode)
            self._input_argument_results_size._value[0] = _val(val.inputArgumentResultsSize)
            self._input_argument_results._value = val.inputArgumentResults
            self._input_argument_diagnostic_infos_size._value[0] = _val(val.inputArgumentDiagnosticInfosSize)
            self._input_argument_diagnostic_infos._value = val.inputArgumentDiagnosticInfos
            self._output_arguments_size._value[0] = _val(val.outputArgumentsSize)
            self._output_arguments._value = val.outputArguments

    @property
    def status_code(self):
        if self._null:
            return None
        else:
            return self._status_code

    @property
    def input_argument_results_size(self):
        if self._null:
            return None
        else:
            return self._input_argument_results_size

    @property
    def input_argument_results(self):
        if self._null:
            return None
        else:
            return self._input_argument_results

    @property
    def input_argument_diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._input_argument_diagnostic_infos_size

    @property
    def input_argument_diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._input_argument_diagnostic_infos

    @property
    def output_arguments_size(self):
        if self._null:
            return None
        else:
            return self._output_arguments_size

    @property
    def output_arguments(self):
        if self._null:
            return None
        else:
            return self._output_arguments

    @status_code.setter
    def status_code(self, val: UaStatusCode):
        self._status_code = val
        self._value.statusCode = val._val

    @input_argument_results_size.setter
    def input_argument_results_size(self, val: SizeT):
        self._input_argument_results_size = val
        self._value.inputArgumentResultsSize = val._val

    @input_argument_results.setter
    def input_argument_results(self, val: UaStatusCode):
        self._input_argument_results = val
        self._value.inputArgumentResults = val._ptr

    @input_argument_diagnostic_infos_size.setter
    def input_argument_diagnostic_infos_size(self, val: SizeT):
        self._input_argument_diagnostic_infos_size = val
        self._value.inputArgumentDiagnosticInfosSize = val._val

    @input_argument_diagnostic_infos.setter
    def input_argument_diagnostic_infos(self, val: UaDiagnosticInfo):
        self._input_argument_diagnostic_infos = val
        self._value.inputArgumentDiagnosticInfos = val._ptr

    @output_arguments_size.setter
    def output_arguments_size(self, val: SizeT):
        self._output_arguments_size = val
        self._value.outputArgumentsSize = val._val

    @output_arguments.setter
    def output_arguments(self, val: UaVariant):
        self._output_arguments = val
        self._value.outputArguments = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaCallMethodResult): NULL" + ("" if n is None else "\n")

        return ("(UaCallMethodResult) :\n"
                + "\t" * (1 if n is None else n+1) + "status_code " + self._status_code.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "input_argument_results_size " + self._input_argument_results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "input_argument_results " + self._input_argument_results.__str__(1 if n is None else n+1)
                + "\t" * (
                            n + 1) + "input_argument_diagnostic_infos_size " + self._input_argument_diagnostic_infos_size.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "input_argument_diagnostic_infos " + self._input_argument_diagnostic_infos.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "output_arguments_size " + self._output_arguments_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "output_arguments " + self._output_arguments.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSetMonitoringModeResponse +++++++++++++++++++++++
class UaSetMonitoringModeResponse(UaType):
    _UA_TYPE = _UA_TYPES._SETMONITORINGMODERESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SetMonitoringModeResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SetMonitoringModeResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaStatusCode(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SetMonitoringModeResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaSetMonitoringModeResponse): NULL" + ("" if n is None else "\n")

        return ("(UaSetMonitoringModeResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaRequestHeader +++++++++++++++++++++++
class UaRequestHeader(UaType):
    _UA_TYPE = _UA_TYPES._REQUESTHEADER

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_RequestHeader*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_RequestHeader*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._authentication_token = UaNodeId(val=val.authenticationToken, is_pointer=False)
            self._timestamp = UaDateTime(val=val.timestamp, is_pointer=False)
            self._request_handle = UaUInt32(val=val.requestHandle, is_pointer=False)
            self._return_diagnostics = UaUInt32(val=val.returnDiagnostics, is_pointer=False)
            self._audit_entry_id = UaString(val=val.auditEntryId, is_pointer=False)
            self._timeout_hint = UaUInt32(val=val.timeoutHint, is_pointer=False)
            self._additional_header = UaExtensionObject(val=val.additionalHeader, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_RequestHeader")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._authentication_token._value[0] = _val(val.authenticationToken)
            self._timestamp._value[0] = _val(val.timestamp)
            self._request_handle._value[0] = _val(val.requestHandle)
            self._return_diagnostics._value[0] = _val(val.returnDiagnostics)
            self._audit_entry_id._value[0] = _val(val.auditEntryId)
            self._timeout_hint._value[0] = _val(val.timeoutHint)
            self._additional_header._value[0] = _val(val.additionalHeader)

    @property
    def authentication_token(self):
        if self._null:
            return None
        else:
            return self._authentication_token

    @property
    def timestamp(self):
        if self._null:
            return None
        else:
            return self._timestamp

    @property
    def request_handle(self):
        if self._null:
            return None
        else:
            return self._request_handle

    @property
    def return_diagnostics(self):
        if self._null:
            return None
        else:
            return self._return_diagnostics

    @property
    def audit_entry_id(self):
        if self._null:
            return None
        else:
            return self._audit_entry_id

    @property
    def timeout_hint(self):
        if self._null:
            return None
        else:
            return self._timeout_hint

    @property
    def additional_header(self):
        if self._null:
            return None
        else:
            return self._additional_header

    @authentication_token.setter
    def authentication_token(self, val: UaNodeId):
        self._authentication_token = val
        self._value.authenticationToken = val._val

    @timestamp.setter
    def timestamp(self, val: UaDateTime):
        self._timestamp = val
        self._value.timestamp = val._val

    @request_handle.setter
    def request_handle(self, val: UaUInt32):
        self._request_handle = val
        self._value.requestHandle = val._val

    @return_diagnostics.setter
    def return_diagnostics(self, val: UaUInt32):
        self._return_diagnostics = val
        self._value.returnDiagnostics = val._val

    @audit_entry_id.setter
    def audit_entry_id(self, val: UaString):
        self._audit_entry_id = val
        self._value.auditEntryId = val._val

    @timeout_hint.setter
    def timeout_hint(self, val: UaUInt32):
        self._timeout_hint = val
        self._value.timeoutHint = val._val

    @additional_header.setter
    def additional_header(self, val: UaExtensionObject):
        self._additional_header = val
        self._value.additionalHeader = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaRequestHeader): NULL" + ("" if n is None else "\n")

        return ("(UaRequestHeader) :\n"
                + "\t" * (1 if n is None else n+1) + "authentication_token " + self._authentication_token.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "timestamp " + self._timestamp.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "request_handle " + self._request_handle.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "return_diagnostics " + self._return_diagnostics.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "audit_entry_id " + self._audit_entry_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "timeout_hint " + self._timeout_hint.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "additional_header " + self._additional_header.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaMonitoredItemModifyResult +++++++++++++++++++++++
class UaMonitoredItemModifyResult(UaType):
    _UA_TYPE = _UA_TYPES._MONITOREDITEMMODIFYRESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_MonitoredItemModifyResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_MonitoredItemModifyResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
            self._revised_sampling_interval = UaDouble(val=val.revisedSamplingInterval, is_pointer=False)
            self._revised_queue_size = UaUInt32(val=val.revisedQueueSize, is_pointer=False)
            self._filter_result = UaExtensionObject(val=val.filterResult, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_MonitoredItemModifyResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._status_code._value[0] = _val(val.statusCode)
            self._revised_sampling_interval._value[0] = _val(val.revisedSamplingInterval)
            self._revised_queue_size._value[0] = _val(val.revisedQueueSize)
            self._filter_result._value[0] = _val(val.filterResult)

    @property
    def status_code(self):
        if self._null:
            return None
        else:
            return self._status_code

    @property
    def revised_sampling_interval(self):
        if self._null:
            return None
        else:
            return self._revised_sampling_interval

    @property
    def revised_queue_size(self):
        if self._null:
            return None
        else:
            return self._revised_queue_size

    @property
    def filter_result(self):
        if self._null:
            return None
        else:
            return self._filter_result

    @status_code.setter
    def status_code(self, val: UaStatusCode):
        self._status_code = val
        self._value.statusCode = val._val

    @revised_sampling_interval.setter
    def revised_sampling_interval(self, val: UaDouble):
        self._revised_sampling_interval = val
        self._value.revisedSamplingInterval = val._val

    @revised_queue_size.setter
    def revised_queue_size(self, val: UaUInt32):
        self._revised_queue_size = val
        self._value.revisedQueueSize = val._val

    @filter_result.setter
    def filter_result(self, val: UaExtensionObject):
        self._filter_result = val
        self._value.filterResult = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaMonitoredItemModifyResult): NULL" + ("" if n is None else "\n")

        return ("(UaMonitoredItemModifyResult) :\n"
                + "\t" * (1 if n is None else n+1) + "status_code " + self._status_code.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_sampling_interval " + self._revised_sampling_interval.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_queue_size " + self._revised_queue_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "filter_result " + self._filter_result.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCloseSecureChannelRequest +++++++++++++++++++++++
class UaCloseSecureChannelRequest(UaType):
    _UA_TYPE = _UA_TYPES._CLOSESECURECHANNELREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CloseSecureChannelRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CloseSecureChannelRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CloseSecureChannelRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaCloseSecureChannelRequest): NULL" + ("" if n is None else "\n")

        return ("(UaCloseSecureChannelRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaNotificationMessage +++++++++++++++++++++++
class UaNotificationMessage(UaType):
    _UA_TYPE = _UA_TYPES._NOTIFICATIONMESSAGE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NotificationMessage*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_NotificationMessage*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._sequence_number = UaUInt32(val=val.sequenceNumber, is_pointer=False)
            self._publish_time = UaDateTime(val=val.publishTime, is_pointer=False)
            self._notification_data_size = SizeT(val=val.notificationDataSize, is_pointer=False)
            self._notification_data = UaExtensionObject(val=val.notificationData, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NotificationMessage")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._sequence_number._value[0] = _val(val.sequenceNumber)
            self._publish_time._value[0] = _val(val.publishTime)
            self._notification_data_size._value[0] = _val(val.notificationDataSize)
            self._notification_data._value = val.notificationData

    @property
    def sequence_number(self):
        if self._null:
            return None
        else:
            return self._sequence_number

    @property
    def publish_time(self):
        if self._null:
            return None
        else:
            return self._publish_time

    @property
    def notification_data_size(self):
        if self._null:
            return None
        else:
            return self._notification_data_size

    @property
    def notification_data(self):
        if self._null:
            return None
        else:
            return self._notification_data

    @sequence_number.setter
    def sequence_number(self, val: UaUInt32):
        self._sequence_number = val
        self._value.sequenceNumber = val._val

    @publish_time.setter
    def publish_time(self, val: UaDateTime):
        self._publish_time = val
        self._value.publishTime = val._val

    @notification_data_size.setter
    def notification_data_size(self, val: SizeT):
        self._notification_data_size = val
        self._value.notificationDataSize = val._val

    @notification_data.setter
    def notification_data(self, val: UaExtensionObject):
        self._notification_data = val
        self._value.notificationData = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaNotificationMessage): NULL" + ("" if n is None else "\n")

        return ("(UaNotificationMessage) :\n"
                + "\t" * (1 if n is None else n+1) + "sequence_number " + self._sequence_number.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "publish_time " + self._publish_time.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "notification_data_size " + self._notification_data_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "notification_data " + self._notification_data.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCreateSubscriptionResponse +++++++++++++++++++++++
class UaCreateSubscriptionResponse(UaType):
    _UA_TYPE = _UA_TYPES._CREATESUBSCRIPTIONRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CreateSubscriptionResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CreateSubscriptionResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
            self._revised_publishing_interval = UaDouble(val=val.revisedPublishingInterval, is_pointer=False)
            self._revised_lifetime_count = UaUInt32(val=val.revisedLifetimeCount, is_pointer=False)
            self._revised_max_keep_alive_count = UaUInt32(val=val.revisedMaxKeepAliveCount, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CreateSubscriptionResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._revised_publishing_interval._value[0] = _val(val.revisedPublishingInterval)
            self._revised_lifetime_count._value[0] = _val(val.revisedLifetimeCount)
            self._revised_max_keep_alive_count._value[0] = _val(val.revisedMaxKeepAliveCount)

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def revised_publishing_interval(self):
        if self._null:
            return None
        else:
            return self._revised_publishing_interval

    @property
    def revised_lifetime_count(self):
        if self._null:
            return None
        else:
            return self._revised_lifetime_count

    @property
    def revised_max_keep_alive_count(self):
        if self._null:
            return None
        else:
            return self._revised_max_keep_alive_count

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @revised_publishing_interval.setter
    def revised_publishing_interval(self, val: UaDouble):
        self._revised_publishing_interval = val
        self._value.revisedPublishingInterval = val._val

    @revised_lifetime_count.setter
    def revised_lifetime_count(self, val: UaUInt32):
        self._revised_lifetime_count = val
        self._value.revisedLifetimeCount = val._val

    @revised_max_keep_alive_count.setter
    def revised_max_keep_alive_count(self, val: UaUInt32):
        self._revised_max_keep_alive_count = val
        self._value.revisedMaxKeepAliveCount = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaCreateSubscriptionResponse): NULL" + ("" if n is None else "\n")

        return ("(UaCreateSubscriptionResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_publishing_interval " + self._revised_publishing_interval.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_lifetime_count " + self._revised_lifetime_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_max_keep_alive_count " + self._revised_max_keep_alive_count.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaEnumDefinition +++++++++++++++++++++++
class UaEnumDefinition(UaType):
    _UA_TYPE = _UA_TYPES._ENUMDEFINITION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_EnumDefinition*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_EnumDefinition*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._fields_size = SizeT(val=val.fieldsSize, is_pointer=False)
            self._fields = UaEnumField(val=val.fields, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_EnumDefinition")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._fields_size._value[0] = _val(val.fieldsSize)
            self._fields._value = val.fields

    @property
    def fields_size(self):
        if self._null:
            return None
        else:
            return self._fields_size

    @property
    def fields(self):
        if self._null:
            return None
        else:
            return self._fields

    @fields_size.setter
    def fields_size(self, val: SizeT):
        self._fields_size = val
        self._value.fieldsSize = val._val

    @fields.setter
    def fields(self, val: UaEnumField):
        self._fields = val
        self._value.fields = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaEnumDefinition): NULL" + ("" if n is None else "\n")

        return ("(UaEnumDefinition) :\n"
                + "\t" * (1 if n is None else n+1) + "fields_size " + self._fields_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "fields " + self._fields.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCallMethodRequest +++++++++++++++++++++++
class UaCallMethodRequest(UaType):
    _UA_TYPE = _UA_TYPES._CALLMETHODREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CallMethodRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CallMethodRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._object_id = UaNodeId(val=val.objectId, is_pointer=False)
            self._method_id = UaNodeId(val=val.methodId, is_pointer=False)
            self._input_arguments_size = SizeT(val=val.inputArgumentsSize, is_pointer=False)
            self._input_arguments = UaVariant(val=val.inputArguments, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CallMethodRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._object_id._value[0] = _val(val.objectId)
            self._method_id._value[0] = _val(val.methodId)
            self._input_arguments_size._value[0] = _val(val.inputArgumentsSize)
            self._input_arguments._value = val.inputArguments

    @property
    def object_id(self):
        if self._null:
            return None
        else:
            return self._object_id

    @property
    def method_id(self):
        if self._null:
            return None
        else:
            return self._method_id

    @property
    def input_arguments_size(self):
        if self._null:
            return None
        else:
            return self._input_arguments_size

    @property
    def input_arguments(self):
        if self._null:
            return None
        else:
            return self._input_arguments

    @object_id.setter
    def object_id(self, val: UaNodeId):
        self._object_id = val
        self._value.objectId = val._val

    @method_id.setter
    def method_id(self, val: UaNodeId):
        self._method_id = val
        self._value.methodId = val._val

    @input_arguments_size.setter
    def input_arguments_size(self, val: SizeT):
        self._input_arguments_size = val
        self._value.inputArgumentsSize = val._val

    @input_arguments.setter
    def input_arguments(self, val: UaVariant):
        self._input_arguments = val
        self._value.inputArguments = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaCallMethodRequest): NULL" + ("" if n is None else "\n")

        return ("(UaCallMethodRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "object_id " + self._object_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "method_id " + self._method_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "input_arguments_size " + self._input_arguments_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "input_arguments " + self._input_arguments.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaReadResponse +++++++++++++++++++++++
class UaReadResponse(UaType):
    _UA_TYPE = _UA_TYPES._READRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ReadResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ReadResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaDataValue(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ReadResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaDataValue):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaReadResponse): NULL" + ("" if n is None else "\n")

        return ("(UaReadResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaObjectTypeAttributes +++++++++++++++++++++++
class UaObjectTypeAttributes(UaType):
    _UA_TYPE = _UA_TYPES._OBJECTTYPEATTRIBUTES

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ObjectTypeAttributes*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ObjectTypeAttributes*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
            self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ObjectTypeAttributes")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._specified_attributes._value[0] = _val(val.specifiedAttributes)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._user_write_mask._value[0] = _val(val.userWriteMask)
            self._is_abstract._value[0] = _val(val.isAbstract)

    @property
    def specified_attributes(self):
        if self._null:
            return None
        else:
            return self._specified_attributes

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def user_write_mask(self):
        if self._null:
            return None
        else:
            return self._user_write_mask

    @property
    def is_abstract(self):
        if self._null:
            return None
        else:
            return self._is_abstract

    @specified_attributes.setter
    def specified_attributes(self, val: UaUInt32):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @user_write_mask.setter
    def user_write_mask(self, val: UaUInt32):
        self._user_write_mask = val
        self._value.userWriteMask = val._val

    @is_abstract.setter
    def is_abstract(self, val: UaBoolean):
        self._is_abstract = val
        self._value.isAbstract = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaObjectTypeAttributes): NULL" + ("" if n is None else "\n")

        return ("(UaObjectTypeAttributes) :\n"
                + "\t" * (1 if n is None else n+1) + "specified_attributes " + self._specified_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_write_mask " + self._user_write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_abstract " + self._is_abstract.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCloseSessionResponse +++++++++++++++++++++++
class UaCloseSessionResponse(UaType):
    _UA_TYPE = _UA_TYPES._CLOSESESSIONRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CloseSessionResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CloseSessionResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CloseSessionResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaCloseSessionResponse): NULL" + ("" if n is None else "\n")

        return ("(UaCloseSessionResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSetPublishingModeRequest +++++++++++++++++++++++
class UaSetPublishingModeRequest(UaType):
    _UA_TYPE = _UA_TYPES._SETPUBLISHINGMODEREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SetPublishingModeRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SetPublishingModeRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._publishing_enabled = UaBoolean(val=val.publishingEnabled, is_pointer=False)
            self._subscription_ids_size = SizeT(val=val.subscriptionIdsSize, is_pointer=False)
            self._subscription_ids = UaUInt32(val=val.subscriptionIds, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SetPublishingModeRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._publishing_enabled._value[0] = _val(val.publishingEnabled)
            self._subscription_ids_size._value[0] = _val(val.subscriptionIdsSize)
            self._subscription_ids._value = val.subscriptionIds

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def publishing_enabled(self):
        if self._null:
            return None
        else:
            return self._publishing_enabled

    @property
    def subscription_ids_size(self):
        if self._null:
            return None
        else:
            return self._subscription_ids_size

    @property
    def subscription_ids(self):
        if self._null:
            return None
        else:
            return self._subscription_ids

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @publishing_enabled.setter
    def publishing_enabled(self, val: UaBoolean):
        self._publishing_enabled = val
        self._value.publishingEnabled = val._val

    @subscription_ids_size.setter
    def subscription_ids_size(self, val: SizeT):
        self._subscription_ids_size = val
        self._value.subscriptionIdsSize = val._val

    @subscription_ids.setter
    def subscription_ids(self, val: UaUInt32):
        self._subscription_ids = val
        self._value.subscriptionIds = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaSetPublishingModeRequest): NULL" + ("" if n is None else "\n")

        return ("(UaSetPublishingModeRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "publishing_enabled " + self._publishing_enabled.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_ids_size " + self._subscription_ids_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_ids " + self._subscription_ids.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaIssuedIdentityToken +++++++++++++++++++++++
class UaIssuedIdentityToken(UaType):
    _UA_TYPE = _UA_TYPES._ISSUEDIDENTITYTOKEN

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_IssuedIdentityToken*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_IssuedIdentityToken*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._policy_id = UaString(val=val.policyId, is_pointer=False)
            self._token_data = UaByteString(val=val.tokenData, is_pointer=False)
            self._encryption_algorithm = UaString(val=val.encryptionAlgorithm, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_IssuedIdentityToken")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._policy_id._value[0] = _val(val.policyId)
            self._token_data._value[0] = _val(val.tokenData)
            self._encryption_algorithm._value[0] = _val(val.encryptionAlgorithm)

    @property
    def policy_id(self):
        if self._null:
            return None
        else:
            return self._policy_id

    @property
    def token_data(self):
        if self._null:
            return None
        else:
            return self._token_data

    @property
    def encryption_algorithm(self):
        if self._null:
            return None
        else:
            return self._encryption_algorithm

    @policy_id.setter
    def policy_id(self, val: UaString):
        self._policy_id = val
        self._value.policyId = val._val

    @token_data.setter
    def token_data(self, val: UaByteString):
        self._token_data = val
        self._value.tokenData = val._val

    @encryption_algorithm.setter
    def encryption_algorithm(self, val: UaString):
        self._encryption_algorithm = val
        self._value.encryptionAlgorithm = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaIssuedIdentityToken): NULL" + ("" if n is None else "\n")

        return ("(UaIssuedIdentityToken) :\n"
                + "\t" * (1 if n is None else n+1) + "policy_id " + self._policy_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "token_data " + self._token_data.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "encryption_algorithm " + self._encryption_algorithm.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteMonitoredItemsResponse +++++++++++++++++++++++
class UaDeleteMonitoredItemsResponse(UaType):
    _UA_TYPE = _UA_TYPES._DELETEMONITOREDITEMSRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteMonitoredItemsResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteMonitoredItemsResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaStatusCode(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteMonitoredItemsResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteMonitoredItemsResponse): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteMonitoredItemsResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBrowseNextRequest +++++++++++++++++++++++
class UaBrowseNextRequest(UaType):
    _UA_TYPE = _UA_TYPES._BROWSENEXTREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BrowseNextRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BrowseNextRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._release_continuation_points = UaBoolean(val=val.releaseContinuationPoints, is_pointer=False)
            self._continuation_points_size = SizeT(val=val.continuationPointsSize, is_pointer=False)
            self._continuation_points = UaByteString(val=val.continuationPoints, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BrowseNextRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._release_continuation_points._value[0] = _val(val.releaseContinuationPoints)
            self._continuation_points_size._value[0] = _val(val.continuationPointsSize)
            self._continuation_points._value = val.continuationPoints

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def release_continuation_points(self):
        if self._null:
            return None
        else:
            return self._release_continuation_points

    @property
    def continuation_points_size(self):
        if self._null:
            return None
        else:
            return self._continuation_points_size

    @property
    def continuation_points(self):
        if self._null:
            return None
        else:
            return self._continuation_points

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @release_continuation_points.setter
    def release_continuation_points(self, val: UaBoolean):
        self._release_continuation_points = val
        self._value.releaseContinuationPoints = val._val

    @continuation_points_size.setter
    def continuation_points_size(self, val: SizeT):
        self._continuation_points_size = val
        self._value.continuationPointsSize = val._val

    @continuation_points.setter
    def continuation_points(self, val: UaByteString):
        self._continuation_points = val
        self._value.continuationPoints = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaBrowseNextRequest): NULL" + ("" if n is None else "\n")

        return ("(UaBrowseNextRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "release_continuation_points " + self._release_continuation_points.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "continuation_points_size " + self._continuation_points_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "continuation_points " + self._continuation_points.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaModifySubscriptionRequest +++++++++++++++++++++++
class UaModifySubscriptionRequest(UaType):
    _UA_TYPE = _UA_TYPES._MODIFYSUBSCRIPTIONREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ModifySubscriptionRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ModifySubscriptionRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
            self._requested_publishing_interval = UaDouble(val=val.requestedPublishingInterval, is_pointer=False)
            self._requested_lifetime_count = UaUInt32(val=val.requestedLifetimeCount, is_pointer=False)
            self._requested_max_keep_alive_count = UaUInt32(val=val.requestedMaxKeepAliveCount, is_pointer=False)
            self._max_notifications_per_publish = UaUInt32(val=val.maxNotificationsPerPublish, is_pointer=False)
            self._priority = UaByte(val=val.priority, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ModifySubscriptionRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._requested_publishing_interval._value[0] = _val(val.requestedPublishingInterval)
            self._requested_lifetime_count._value[0] = _val(val.requestedLifetimeCount)
            self._requested_max_keep_alive_count._value[0] = _val(val.requestedMaxKeepAliveCount)
            self._max_notifications_per_publish._value[0] = _val(val.maxNotificationsPerPublish)
            self._priority._value[0] = _val(val.priority)

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def requested_publishing_interval(self):
        if self._null:
            return None
        else:
            return self._requested_publishing_interval

    @property
    def requested_lifetime_count(self):
        if self._null:
            return None
        else:
            return self._requested_lifetime_count

    @property
    def requested_max_keep_alive_count(self):
        if self._null:
            return None
        else:
            return self._requested_max_keep_alive_count

    @property
    def max_notifications_per_publish(self):
        if self._null:
            return None
        else:
            return self._max_notifications_per_publish

    @property
    def priority(self):
        if self._null:
            return None
        else:
            return self._priority

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @requested_publishing_interval.setter
    def requested_publishing_interval(self, val: UaDouble):
        self._requested_publishing_interval = val
        self._value.requestedPublishingInterval = val._val

    @requested_lifetime_count.setter
    def requested_lifetime_count(self, val: UaUInt32):
        self._requested_lifetime_count = val
        self._value.requestedLifetimeCount = val._val

    @requested_max_keep_alive_count.setter
    def requested_max_keep_alive_count(self, val: UaUInt32):
        self._requested_max_keep_alive_count = val
        self._value.requestedMaxKeepAliveCount = val._val

    @max_notifications_per_publish.setter
    def max_notifications_per_publish(self, val: UaUInt32):
        self._max_notifications_per_publish = val
        self._value.maxNotificationsPerPublish = val._val

    @priority.setter
    def priority(self, val: UaByte):
        self._priority = val
        self._value.priority = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaModifySubscriptionRequest): NULL" + ("" if n is None else "\n")

        return ("(UaModifySubscriptionRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_publishing_interval " + self._requested_publishing_interval.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_lifetime_count " + self._requested_lifetime_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_max_keep_alive_count " + self._requested_max_keep_alive_count.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "max_notifications_per_publish " + self._max_notifications_per_publish.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "priority " + self._priority.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBrowseDescription +++++++++++++++++++++++
class UaBrowseDescription(UaType):
    _UA_TYPE = _UA_TYPES._BROWSEDESCRIPTION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BrowseDescription*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BrowseDescription*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
            self._browse_direction = UaBrowseDirection(val=val.browseDirection, is_pointer=False)
            self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
            self._include_subtypes = UaBoolean(val=val.includeSubtypes, is_pointer=False)
            self._node_class_mask = UaUInt32(val=val.nodeClassMask, is_pointer=False)
            self._result_mask = UaUInt32(val=val.resultMask, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BrowseDescription")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._node_id._value[0] = _val(val.nodeId)
            self._browse_direction._value[0] = _val(val.browseDirection)
            self._reference_type_id._value[0] = _val(val.referenceTypeId)
            self._include_subtypes._value[0] = _val(val.includeSubtypes)
            self._node_class_mask._value[0] = _val(val.nodeClassMask)
            self._result_mask._value[0] = _val(val.resultMask)

    @property
    def node_id(self):
        if self._null:
            return None
        else:
            return self._node_id

    @property
    def browse_direction(self):
        if self._null:
            return None
        else:
            return self._browse_direction

    @property
    def reference_type_id(self):
        if self._null:
            return None
        else:
            return self._reference_type_id

    @property
    def include_subtypes(self):
        if self._null:
            return None
        else:
            return self._include_subtypes

    @property
    def node_class_mask(self):
        if self._null:
            return None
        else:
            return self._node_class_mask

    @property
    def result_mask(self):
        if self._null:
            return None
        else:
            return self._result_mask

    @node_id.setter
    def node_id(self, val: UaNodeId):
        self._node_id = val
        self._value.nodeId = val._val

    @browse_direction.setter
    def browse_direction(self, val: UaBrowseDirection):
        self._browse_direction = val
        self._value.browseDirection = val._val

    @reference_type_id.setter
    def reference_type_id(self, val: UaNodeId):
        self._reference_type_id = val
        self._value.referenceTypeId = val._val

    @include_subtypes.setter
    def include_subtypes(self, val: UaBoolean):
        self._include_subtypes = val
        self._value.includeSubtypes = val._val

    @node_class_mask.setter
    def node_class_mask(self, val: UaUInt32):
        self._node_class_mask = val
        self._value.nodeClassMask = val._val

    @result_mask.setter
    def result_mask(self, val: UaUInt32):
        self._result_mask = val
        self._value.resultMask = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaBrowseDescription): NULL" + ("" if n is None else "\n")

        return ("(UaBrowseDescription) :\n"
                + "\t" * (1 if n is None else n+1) + "node_id " + self._node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "browse_direction " + self._browse_direction.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "reference_type_id " + self._reference_type_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "include_subtypes " + self._include_subtypes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "node_class_mask " + self._node_class_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "result_mask " + self._result_mask.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSignedSoftwareCertificate +++++++++++++++++++++++
class UaSignedSoftwareCertificate(UaType):
    _UA_TYPE = _UA_TYPES._SIGNEDSOFTWARECERTIFICATE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SignedSoftwareCertificate*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SignedSoftwareCertificate*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._certificate_data = UaByteString(val=val.certificateData, is_pointer=False)
            self._signature = UaByteString(val=val.signature, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SignedSoftwareCertificate")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._certificate_data._value[0] = _val(val.certificateData)
            self._signature._value[0] = _val(val.signature)

    @property
    def certificate_data(self):
        if self._null:
            return None
        else:
            return self._certificate_data

    @property
    def signature(self):
        if self._null:
            return None
        else:
            return self._signature

    @certificate_data.setter
    def certificate_data(self, val: UaByteString):
        self._certificate_data = val
        self._value.certificateData = val._val

    @signature.setter
    def signature(self, val: UaByteString):
        self._signature = val
        self._value.signature = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaSignedSoftwareCertificate): NULL" + ("" if n is None else "\n")

        return ("(UaSignedSoftwareCertificate) :\n"
                + "\t" * (1 if n is None else n+1) + "certificate_data " + self._certificate_data.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "signature " + self._signature.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBrowsePathTarget +++++++++++++++++++++++
class UaBrowsePathTarget(UaType):
    _UA_TYPE = _UA_TYPES._BROWSEPATHTARGET

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BrowsePathTarget*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BrowsePathTarget*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._target_id = UaExpandedNodeId(val=val.targetId, is_pointer=False)
            self._remaining_path_index = UaUInt32(val=val.remainingPathIndex, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BrowsePathTarget")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._target_id._value[0] = _val(val.targetId)
            self._remaining_path_index._value[0] = _val(val.remainingPathIndex)

    @property
    def target_id(self):
        if self._null:
            return None
        else:
            return self._target_id

    @property
    def remaining_path_index(self):
        if self._null:
            return None
        else:
            return self._remaining_path_index

    @target_id.setter
    def target_id(self, val: UaExpandedNodeId):
        self._target_id = val
        self._value.targetId = val._val

    @remaining_path_index.setter
    def remaining_path_index(self, val: UaUInt32):
        self._remaining_path_index = val
        self._value.remainingPathIndex = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaBrowsePathTarget): NULL" + ("" if n is None else "\n")

        return ("(UaBrowsePathTarget) :\n"
                + "\t" * (1 if n is None else n+1) + "target_id " + self._target_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "remaining_path_index " + self._remaining_path_index.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaWriteResponse +++++++++++++++++++++++
class UaWriteResponse(UaType):
    _UA_TYPE = _UA_TYPES._WRITERESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_WriteResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_WriteResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaStatusCode(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_WriteResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaWriteResponse): NULL" + ("" if n is None else "\n")

        return ("(UaWriteResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAddNodesResult +++++++++++++++++++++++
class UaAddNodesResult(UaType):
    _UA_TYPE = _UA_TYPES._ADDNODESRESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AddNodesResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AddNodesResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
            self._added_node_id = UaNodeId(val=val.addedNodeId, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AddNodesResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._status_code._value[0] = _val(val.statusCode)
            self._added_node_id._value[0] = _val(val.addedNodeId)

    @property
    def status_code(self):
        if self._null:
            return None
        else:
            return self._status_code

    @property
    def added_node_id(self):
        if self._null:
            return None
        else:
            return self._added_node_id

    @status_code.setter
    def status_code(self, val: UaStatusCode):
        self._status_code = val
        self._value.statusCode = val._val

    @added_node_id.setter
    def added_node_id(self, val: UaNodeId):
        self._added_node_id = val
        self._value.addedNodeId = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaAddNodesResult): NULL" + ("" if n is None else "\n")

        return ("(UaAddNodesResult) :\n"
                + "\t" * (1 if n is None else n+1) + "status_code " + self._status_code.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "added_node_id " + self._added_node_id.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAddReferencesItem +++++++++++++++++++++++
class UaAddReferencesItem(UaType):
    _UA_TYPE = _UA_TYPES._ADDREFERENCESITEM

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AddReferencesItem*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AddReferencesItem*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._source_node_id = UaNodeId(val=val.sourceNodeId, is_pointer=False)
            self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
            self._is_forward = UaBoolean(val=val.isForward, is_pointer=False)
            self._target_server_uri = UaString(val=val.targetServerUri, is_pointer=False)
            self._target_node_id = UaExpandedNodeId(val=val.targetNodeId, is_pointer=False)
            self._target_node_class = UaNodeClass(val=val.targetNodeClass, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AddReferencesItem")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._source_node_id._value[0] = _val(val.sourceNodeId)
            self._reference_type_id._value[0] = _val(val.referenceTypeId)
            self._is_forward._value[0] = _val(val.isForward)
            self._target_server_uri._value[0] = _val(val.targetServerUri)
            self._target_node_id._value[0] = _val(val.targetNodeId)
            self._target_node_class._value[0] = _val(val.targetNodeClass)

    @property
    def source_node_id(self):
        if self._null:
            return None
        else:
            return self._source_node_id

    @property
    def reference_type_id(self):
        if self._null:
            return None
        else:
            return self._reference_type_id

    @property
    def is_forward(self):
        if self._null:
            return None
        else:
            return self._is_forward

    @property
    def target_server_uri(self):
        if self._null:
            return None
        else:
            return self._target_server_uri

    @property
    def target_node_id(self):
        if self._null:
            return None
        else:
            return self._target_node_id

    @property
    def target_node_class(self):
        if self._null:
            return None
        else:
            return self._target_node_class

    @source_node_id.setter
    def source_node_id(self, val: UaNodeId):
        self._source_node_id = val
        self._value.sourceNodeId = val._val

    @reference_type_id.setter
    def reference_type_id(self, val: UaNodeId):
        self._reference_type_id = val
        self._value.referenceTypeId = val._val

    @is_forward.setter
    def is_forward(self, val: UaBoolean):
        self._is_forward = val
        self._value.isForward = val._val

    @target_server_uri.setter
    def target_server_uri(self, val: UaString):
        self._target_server_uri = val
        self._value.targetServerUri = val._val

    @target_node_id.setter
    def target_node_id(self, val: UaExpandedNodeId):
        self._target_node_id = val
        self._value.targetNodeId = val._val

    @target_node_class.setter
    def target_node_class(self, val: UaNodeClass):
        self._target_node_class = val
        self._value.targetNodeClass = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaAddReferencesItem): NULL" + ("" if n is None else "\n")

        return ("(UaAddReferencesItem) :\n"
                + "\t" * (1 if n is None else n+1) + "source_node_id " + self._source_node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "reference_type_id " + self._reference_type_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_forward " + self._is_forward.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "target_server_uri " + self._target_server_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "target_node_id " + self._target_node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "target_node_class " + self._target_node_class.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteReferencesResponse +++++++++++++++++++++++
class UaDeleteReferencesResponse(UaType):
    _UA_TYPE = _UA_TYPES._DELETEREFERENCESRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteReferencesResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteReferencesResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaStatusCode(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteReferencesResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteReferencesResponse): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteReferencesResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaRelativePathElement +++++++++++++++++++++++
class UaRelativePathElement(UaType):
    _UA_TYPE = _UA_TYPES._RELATIVEPATHELEMENT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_RelativePathElement*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_RelativePathElement*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
            self._is_inverse = UaBoolean(val=val.isInverse, is_pointer=False)
            self._include_subtypes = UaBoolean(val=val.includeSubtypes, is_pointer=False)
            self._target_name = UaQualifiedName(val=val.targetName, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_RelativePathElement")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._reference_type_id._value[0] = _val(val.referenceTypeId)
            self._is_inverse._value[0] = _val(val.isInverse)
            self._include_subtypes._value[0] = _val(val.includeSubtypes)
            self._target_name._value[0] = _val(val.targetName)

    @property
    def reference_type_id(self):
        if self._null:
            return None
        else:
            return self._reference_type_id

    @property
    def is_inverse(self):
        if self._null:
            return None
        else:
            return self._is_inverse

    @property
    def include_subtypes(self):
        if self._null:
            return None
        else:
            return self._include_subtypes

    @property
    def target_name(self):
        if self._null:
            return None
        else:
            return self._target_name

    @reference_type_id.setter
    def reference_type_id(self, val: UaNodeId):
        self._reference_type_id = val
        self._value.referenceTypeId = val._val

    @is_inverse.setter
    def is_inverse(self, val: UaBoolean):
        self._is_inverse = val
        self._value.isInverse = val._val

    @include_subtypes.setter
    def include_subtypes(self, val: UaBoolean):
        self._include_subtypes = val
        self._value.includeSubtypes = val._val

    @target_name.setter
    def target_name(self, val: UaQualifiedName):
        self._target_name = val
        self._value.targetName = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaRelativePathElement): NULL" + ("" if n is None else "\n")

        return ("(UaRelativePathElement) :\n"
                + "\t" * (1 if n is None else n+1) + "reference_type_id " + self._reference_type_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_inverse " + self._is_inverse.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "include_subtypes " + self._include_subtypes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "target_name " + self._target_name.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSubscriptionAcknowledgement +++++++++++++++++++++++
class UaSubscriptionAcknowledgement(UaType):
    _UA_TYPE = _UA_TYPES._SUBSCRIPTIONACKNOWLEDGEMENT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SubscriptionAcknowledgement*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SubscriptionAcknowledgement*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
            self._sequence_number = UaUInt32(val=val.sequenceNumber, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SubscriptionAcknowledgement")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._sequence_number._value[0] = _val(val.sequenceNumber)

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def sequence_number(self):
        if self._null:
            return None
        else:
            return self._sequence_number

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @sequence_number.setter
    def sequence_number(self, val: UaUInt32):
        self._sequence_number = val
        self._value.sequenceNumber = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaSubscriptionAcknowledgement): NULL" + ("" if n is None else "\n")

        return ("(UaSubscriptionAcknowledgement) :\n"
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "sequence_number " + self._sequence_number.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaTransferResult +++++++++++++++++++++++
class UaTransferResult(UaType):
    _UA_TYPE = _UA_TYPES._TRANSFERRESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_TransferResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_TransferResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
            self._available_sequence_numbers_size = SizeT(val=val.availableSequenceNumbersSize, is_pointer=False)
            self._available_sequence_numbers = UaUInt32(val=val.availableSequenceNumbers, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_TransferResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._status_code._value[0] = _val(val.statusCode)
            self._available_sequence_numbers_size._value[0] = _val(val.availableSequenceNumbersSize)
            self._available_sequence_numbers._value = val.availableSequenceNumbers

    @property
    def status_code(self):
        if self._null:
            return None
        else:
            return self._status_code

    @property
    def available_sequence_numbers_size(self):
        if self._null:
            return None
        else:
            return self._available_sequence_numbers_size

    @property
    def available_sequence_numbers(self):
        if self._null:
            return None
        else:
            return self._available_sequence_numbers

    @status_code.setter
    def status_code(self, val: UaStatusCode):
        self._status_code = val
        self._value.statusCode = val._val

    @available_sequence_numbers_size.setter
    def available_sequence_numbers_size(self, val: SizeT):
        self._available_sequence_numbers_size = val
        self._value.availableSequenceNumbersSize = val._val

    @available_sequence_numbers.setter
    def available_sequence_numbers(self, val: UaUInt32):
        self._available_sequence_numbers = val
        self._value.availableSequenceNumbers = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaTransferResult): NULL" + ("" if n is None else "\n")

        return ("(UaTransferResult) :\n"
                + "\t" * (1 if n is None else n+1) + "status_code " + self._status_code.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "available_sequence_numbers_size " + self._available_sequence_numbers_size.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "available_sequence_numbers " + self._available_sequence_numbers.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCreateMonitoredItemsResponse +++++++++++++++++++++++
class UaCreateMonitoredItemsResponse(UaType):
    _UA_TYPE = _UA_TYPES._CREATEMONITOREDITEMSRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CreateMonitoredItemsResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CreateMonitoredItemsResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaMonitoredItemCreateResult(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CreateMonitoredItemsResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaMonitoredItemCreateResult):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaCreateMonitoredItemsResponse): NULL" + ("" if n is None else "\n")

        return ("(UaCreateMonitoredItemsResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteReferencesItem +++++++++++++++++++++++
class UaDeleteReferencesItem(UaType):
    _UA_TYPE = _UA_TYPES._DELETEREFERENCESITEM

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteReferencesItem*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteReferencesItem*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._source_node_id = UaNodeId(val=val.sourceNodeId, is_pointer=False)
            self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
            self._is_forward = UaBoolean(val=val.isForward, is_pointer=False)
            self._target_node_id = UaExpandedNodeId(val=val.targetNodeId, is_pointer=False)
            self._delete_bidirectional = UaBoolean(val=val.deleteBidirectional, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteReferencesItem")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._source_node_id._value[0] = _val(val.sourceNodeId)
            self._reference_type_id._value[0] = _val(val.referenceTypeId)
            self._is_forward._value[0] = _val(val.isForward)
            self._target_node_id._value[0] = _val(val.targetNodeId)
            self._delete_bidirectional._value[0] = _val(val.deleteBidirectional)

    @property
    def source_node_id(self):
        if self._null:
            return None
        else:
            return self._source_node_id

    @property
    def reference_type_id(self):
        if self._null:
            return None
        else:
            return self._reference_type_id

    @property
    def is_forward(self):
        if self._null:
            return None
        else:
            return self._is_forward

    @property
    def target_node_id(self):
        if self._null:
            return None
        else:
            return self._target_node_id

    @property
    def delete_bidirectional(self):
        if self._null:
            return None
        else:
            return self._delete_bidirectional

    @source_node_id.setter
    def source_node_id(self, val: UaNodeId):
        self._source_node_id = val
        self._value.sourceNodeId = val._val

    @reference_type_id.setter
    def reference_type_id(self, val: UaNodeId):
        self._reference_type_id = val
        self._value.referenceTypeId = val._val

    @is_forward.setter
    def is_forward(self, val: UaBoolean):
        self._is_forward = val
        self._value.isForward = val._val

    @target_node_id.setter
    def target_node_id(self, val: UaExpandedNodeId):
        self._target_node_id = val
        self._value.targetNodeId = val._val

    @delete_bidirectional.setter
    def delete_bidirectional(self, val: UaBoolean):
        self._delete_bidirectional = val
        self._value.deleteBidirectional = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteReferencesItem): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteReferencesItem) :\n"
                + "\t" * (1 if n is None else n+1) + "source_node_id " + self._source_node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "reference_type_id " + self._reference_type_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_forward " + self._is_forward.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "target_node_id " + self._target_node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "delete_bidirectional " + self._delete_bidirectional.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaWriteValue +++++++++++++++++++++++
class UaWriteValue(UaType):
    _UA_TYPE = _UA_TYPES._WRITEVALUE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_WriteValue*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_WriteValue*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
            self._attribute_id = UaUInt32(val=val.attributeId, is_pointer=False)
            self._index_range = UaString(val=val.indexRange, is_pointer=False)
            self._data_value = UaDataValue(val=val.value, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_WriteValue")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._node_id._value[0] = _val(val.nodeId)
            self._attribute_id._value[0] = _val(val.attributeId)
            self._index_range._value[0] = _val(val.indexRange)
            self._data_value._value[0] = _val(val.value)

    @property
    def node_id(self):
        if self._null:
            return None
        else:
            return self._node_id

    @property
    def attribute_id(self):
        if self._null:
            return None
        else:
            return self._attribute_id

    @property
    def index_range(self):
        if self._null:
            return None
        else:
            return self._index_range

    @property
    def data_value(self):
        if self._null:
            return None
        else:
            return self._data_value

    @node_id.setter
    def node_id(self, val: UaNodeId):
        self._node_id = val
        self._value.nodeId = val._val

    @attribute_id.setter
    def attribute_id(self, val: UaUInt32):
        self._attribute_id = val
        self._value.attributeId = val._val

    @index_range.setter
    def index_range(self, val: UaString):
        self._index_range = val
        self._value.indexRange = val._val

    @data_value.setter
    def data_value(self, val: UaDataValue):
        self._data_value = val
        self._value.value = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaWriteValue): NULL" + ("" if n is None else "\n")

        return ("(UaWriteValue) :\n"
                + "\t" * (1 if n is None else n+1) + "node_id " + self._node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "attribute_id " + self._attribute_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "index_range " + self._index_range.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_value " + self._data_value.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDataTypeAttributes +++++++++++++++++++++++
class UaDataTypeAttributes(UaType):
    _UA_TYPE = _UA_TYPES._DATATYPEATTRIBUTES

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataTypeAttributes*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DataTypeAttributes*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
            self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataTypeAttributes")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._specified_attributes._value[0] = _val(val.specifiedAttributes)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._user_write_mask._value[0] = _val(val.userWriteMask)
            self._is_abstract._value[0] = _val(val.isAbstract)

    @property
    def specified_attributes(self):
        if self._null:
            return None
        else:
            return self._specified_attributes

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def user_write_mask(self):
        if self._null:
            return None
        else:
            return self._user_write_mask

    @property
    def is_abstract(self):
        if self._null:
            return None
        else:
            return self._is_abstract

    @specified_attributes.setter
    def specified_attributes(self, val: UaUInt32):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @user_write_mask.setter
    def user_write_mask(self, val: UaUInt32):
        self._user_write_mask = val
        self._value.userWriteMask = val._val

    @is_abstract.setter
    def is_abstract(self, val: UaBoolean):
        self._is_abstract = val
        self._value.isAbstract = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaDataTypeAttributes): NULL" + ("" if n is None else "\n")

        return ("(UaDataTypeAttributes) :\n"
                + "\t" * (1 if n is None else n+1) + "specified_attributes " + self._specified_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_write_mask " + self._user_write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_abstract " + self._is_abstract.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaTransferSubscriptionsResponse +++++++++++++++++++++++
class UaTransferSubscriptionsResponse(UaType):
    _UA_TYPE = _UA_TYPES._TRANSFERSUBSCRIPTIONSRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_TransferSubscriptionsResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_TransferSubscriptionsResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaTransferResult(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_TransferSubscriptionsResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaTransferResult):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaTransferSubscriptionsResponse): NULL" + ("" if n is None else "\n")

        return ("(UaTransferSubscriptionsResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAddReferencesResponse +++++++++++++++++++++++
class UaAddReferencesResponse(UaType):
    _UA_TYPE = _UA_TYPES._ADDREFERENCESRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AddReferencesResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AddReferencesResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaStatusCode(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AddReferencesResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaAddReferencesResponse): NULL" + ("" if n is None else "\n")

        return ("(UaAddReferencesResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBuildInfo +++++++++++++++++++++++
class UaBuildInfo(UaType):
    _UA_TYPE = _UA_TYPES._BUILDINFO

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BuildInfo*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BuildInfo*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._product_uri = UaString(val=val.productUri, is_pointer=False)
            self._manufacturer_name = UaString(val=val.manufacturerName, is_pointer=False)
            self._product_name = UaString(val=val.productName, is_pointer=False)
            self._software_version = UaString(val=val.softwareVersion, is_pointer=False)
            self._build_number = UaString(val=val.buildNumber, is_pointer=False)
            self._build_date = UaDateTime(val=val.buildDate, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BuildInfo")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._product_uri._value[0] = _val(val.productUri)
            self._manufacturer_name._value[0] = _val(val.manufacturerName)
            self._product_name._value[0] = _val(val.productName)
            self._software_version._value[0] = _val(val.softwareVersion)
            self._build_number._value[0] = _val(val.buildNumber)
            self._build_date._value[0] = _val(val.buildDate)

    @property
    def product_uri(self):
        if self._null:
            return None
        else:
            return self._product_uri

    @property
    def manufacturer_name(self):
        if self._null:
            return None
        else:
            return self._manufacturer_name

    @property
    def product_name(self):
        if self._null:
            return None
        else:
            return self._product_name

    @property
    def software_version(self):
        if self._null:
            return None
        else:
            return self._software_version

    @property
    def build_number(self):
        if self._null:
            return None
        else:
            return self._build_number

    @property
    def build_date(self):
        if self._null:
            return None
        else:
            return self._build_date

    @product_uri.setter
    def product_uri(self, val: UaString):
        self._product_uri = val
        self._value.productUri = val._val

    @manufacturer_name.setter
    def manufacturer_name(self, val: UaString):
        self._manufacturer_name = val
        self._value.manufacturerName = val._val

    @product_name.setter
    def product_name(self, val: UaString):
        self._product_name = val
        self._value.productName = val._val

    @software_version.setter
    def software_version(self, val: UaString):
        self._software_version = val
        self._value.softwareVersion = val._val

    @build_number.setter
    def build_number(self, val: UaString):
        self._build_number = val
        self._value.buildNumber = val._val

    @build_date.setter
    def build_date(self, val: UaDateTime):
        self._build_date = val
        self._value.buildDate = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaBuildInfo): NULL" + ("" if n is None else "\n")

        return ("(UaBuildInfo) :\n"
                + "\t" * (1 if n is None else n+1) + "product_uri " + self._product_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "manufacturer_name " + self._manufacturer_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "product_name " + self._product_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "software_version " + self._software_version.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "build_number " + self._build_number.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "build_date " + self._build_date.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaMonitoringParameters +++++++++++++++++++++++
class UaMonitoringParameters(UaType):
    _UA_TYPE = _UA_TYPES._MONITORINGPARAMETERS

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_MonitoringParameters*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_MonitoringParameters*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._client_handle = UaUInt32(val=val.clientHandle, is_pointer=False)
            self._sampling_interval = UaDouble(val=val.samplingInterval, is_pointer=False)
            self._filter = UaExtensionObject(val=val.filter, is_pointer=False)
            self._queue_size = UaUInt32(val=val.queueSize, is_pointer=False)
            self._discard_oldest = UaBoolean(val=val.discardOldest, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_MonitoringParameters")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._client_handle._value[0] = _val(val.clientHandle)
            self._sampling_interval._value[0] = _val(val.samplingInterval)
            self._filter._value[0] = _val(val.filter)
            self._queue_size._value[0] = _val(val.queueSize)
            self._discard_oldest._value[0] = _val(val.discardOldest)

    @property
    def client_handle(self):
        if self._null:
            return None
        else:
            return self._client_handle

    @property
    def sampling_interval(self):
        if self._null:
            return None
        else:
            return self._sampling_interval

    @property
    def filter(self):
        if self._null:
            return None
        else:
            return self._filter

    @property
    def queue_size(self):
        if self._null:
            return None
        else:
            return self._queue_size

    @property
    def discard_oldest(self):
        if self._null:
            return None
        else:
            return self._discard_oldest

    @client_handle.setter
    def client_handle(self, val: UaUInt32):
        self._client_handle = val
        self._value.clientHandle = val._val

    @sampling_interval.setter
    def sampling_interval(self, val: UaDouble):
        self._sampling_interval = val
        self._value.samplingInterval = val._val

    @filter.setter
    def filter(self, val: UaExtensionObject):
        self._filter = val
        self._value.filter = val._val

    @queue_size.setter
    def queue_size(self, val: UaUInt32):
        self._queue_size = val
        self._value.queueSize = val._val

    @discard_oldest.setter
    def discard_oldest(self, val: UaBoolean):
        self._discard_oldest = val
        self._value.discardOldest = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaMonitoringParameters): NULL" + ("" if n is None else "\n")

        return ("(UaMonitoringParameters) :\n"
                + "\t" * (1 if n is None else n+1) + "client_handle " + self._client_handle.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "sampling_interval " + self._sampling_interval.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "filter " + self._filter.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "queue_size " + self._queue_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "discard_oldest " + self._discard_oldest.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDoubleComplexNumberType +++++++++++++++++++++++
class UaDoubleComplexNumberType(UaType):
    _UA_TYPE = _UA_TYPES._DOUBLECOMPLEXNUMBERTYPE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DoubleComplexNumberType*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DoubleComplexNumberType*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._real = UaDouble(val=val.real, is_pointer=False)
            self._imaginary = UaDouble(val=val.imaginary, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DoubleComplexNumberType")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._real._value[0] = _val(val.real)
            self._imaginary._value[0] = _val(val.imaginary)

    @property
    def real(self):
        if self._null:
            return None
        else:
            return self._real

    @property
    def imaginary(self):
        if self._null:
            return None
        else:
            return self._imaginary

    @real.setter
    def real(self, val: UaDouble):
        self._real = val
        self._value.real = val._val

    @imaginary.setter
    def imaginary(self, val: UaDouble):
        self._imaginary = val
        self._value.imaginary = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaDoubleComplexNumberType): NULL" + ("" if n is None else "\n")

        return ("(UaDoubleComplexNumberType) :\n"
                + "\t" * (1 if n is None else n+1) + "real " + self._real.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "imaginary " + self._imaginary.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteNodesItem +++++++++++++++++++++++
class UaDeleteNodesItem(UaType):
    _UA_TYPE = _UA_TYPES._DELETENODESITEM

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteNodesItem*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteNodesItem*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
            self._delete_target_references = UaBoolean(val=val.deleteTargetReferences, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteNodesItem")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._node_id._value[0] = _val(val.nodeId)
            self._delete_target_references._value[0] = _val(val.deleteTargetReferences)

    @property
    def node_id(self):
        if self._null:
            return None
        else:
            return self._node_id

    @property
    def delete_target_references(self):
        if self._null:
            return None
        else:
            return self._delete_target_references

    @node_id.setter
    def node_id(self, val: UaNodeId):
        self._node_id = val
        self._value.nodeId = val._val

    @delete_target_references.setter
    def delete_target_references(self, val: UaBoolean):
        self._delete_target_references = val
        self._value.deleteTargetReferences = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteNodesItem): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteNodesItem) :\n"
                + "\t" * (1 if n is None else n+1) + "node_id " + self._node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "delete_target_references " + self._delete_target_references.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaReadValueId +++++++++++++++++++++++
class UaReadValueId(UaType):
    _UA_TYPE = _UA_TYPES._READVALUEID

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ReadValueId*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ReadValueId*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
            self._attribute_id = UaUInt32(val=val.attributeId, is_pointer=False)
            self._index_range = UaString(val=val.indexRange, is_pointer=False)
            self._data_encoding = UaQualifiedName(val=val.dataEncoding, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ReadValueId")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._node_id._value[0] = _val(val.nodeId)
            self._attribute_id._value[0] = _val(val.attributeId)
            self._index_range._value[0] = _val(val.indexRange)
            self._data_encoding._value[0] = _val(val.dataEncoding)

    @property
    def node_id(self):
        if self._null:
            return None
        else:
            return self._node_id

    @property
    def attribute_id(self):
        if self._null:
            return None
        else:
            return self._attribute_id

    @property
    def index_range(self):
        if self._null:
            return None
        else:
            return self._index_range

    @property
    def data_encoding(self):
        if self._null:
            return None
        else:
            return self._data_encoding

    @node_id.setter
    def node_id(self, val: UaNodeId):
        self._node_id = val
        self._value.nodeId = val._val

    @attribute_id.setter
    def attribute_id(self, val: UaUInt32):
        self._attribute_id = val
        self._value.attributeId = val._val

    @index_range.setter
    def index_range(self, val: UaString):
        self._index_range = val
        self._value.indexRange = val._val

    @data_encoding.setter
    def data_encoding(self, val: UaQualifiedName):
        self._data_encoding = val
        self._value.dataEncoding = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaReadValueId): NULL" + ("" if n is None else "\n")

        return ("(UaReadValueId) :\n"
                + "\t" * (1 if n is None else n+1) + "node_id " + self._node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "attribute_id " + self._attribute_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "index_range " + self._index_range.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_encoding " + self._data_encoding.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCallRequest +++++++++++++++++++++++
class UaCallRequest(UaType):
    _UA_TYPE = _UA_TYPES._CALLREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CallRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CallRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._methods_to_call_size = SizeT(val=val.methodsToCallSize, is_pointer=False)
            self._methods_to_call = UaCallMethodRequest(val=val.methodsToCall, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CallRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._methods_to_call_size._value[0] = _val(val.methodsToCallSize)
            self._methods_to_call._value = val.methodsToCall

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def methods_to_call_size(self):
        if self._null:
            return None
        else:
            return self._methods_to_call_size

    @property
    def methods_to_call(self):
        if self._null:
            return None
        else:
            return self._methods_to_call

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @methods_to_call_size.setter
    def methods_to_call_size(self, val: SizeT):
        self._methods_to_call_size = val
        self._value.methodsToCallSize = val._val

    @methods_to_call.setter
    def methods_to_call(self, val: UaCallMethodRequest):
        self._methods_to_call = val
        self._value.methodsToCall = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaCallRequest): NULL" + ("" if n is None else "\n")

        return ("(UaCallRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "methods_to_call_size " + self._methods_to_call_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "methods_to_call " + self._methods_to_call.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaRelativePath +++++++++++++++++++++++
class UaRelativePath(UaType):
    _UA_TYPE = _UA_TYPES._RELATIVEPATH

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_RelativePath*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_RelativePath*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._elements_size = SizeT(val=val.elementsSize, is_pointer=False)
            self._elements = UaRelativePathElement(val=val.elements, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_RelativePath")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._elements_size._value[0] = _val(val.elementsSize)
            self._elements._value = val.elements

    @property
    def elements_size(self):
        if self._null:
            return None
        else:
            return self._elements_size

    @property
    def elements(self):
        if self._null:
            return None
        else:
            return self._elements

    @elements_size.setter
    def elements_size(self, val: SizeT):
        self._elements_size = val
        self._value.elementsSize = val._val

    @elements.setter
    def elements(self, val: UaRelativePathElement):
        self._elements = val
        self._value.elements = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaRelativePath): NULL" + ("" if n is None else "\n")

        return ("(UaRelativePath) :\n"
                + "\t" * (1 if n is None else n+1) + "elements_size " + self._elements_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "elements " + self._elements.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteNodesRequest +++++++++++++++++++++++
class UaDeleteNodesRequest(UaType):
    _UA_TYPE = _UA_TYPES._DELETENODESREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteNodesRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteNodesRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._nodes_to_delete_size = SizeT(val=val.nodesToDeleteSize, is_pointer=False)
            self._nodes_to_delete = UaDeleteNodesItem(val=val.nodesToDelete, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteNodesRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._nodes_to_delete_size._value[0] = _val(val.nodesToDeleteSize)
            self._nodes_to_delete._value = val.nodesToDelete

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def nodes_to_delete_size(self):
        if self._null:
            return None
        else:
            return self._nodes_to_delete_size

    @property
    def nodes_to_delete(self):
        if self._null:
            return None
        else:
            return self._nodes_to_delete

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @nodes_to_delete_size.setter
    def nodes_to_delete_size(self, val: SizeT):
        self._nodes_to_delete_size = val
        self._value.nodesToDeleteSize = val._val

    @nodes_to_delete.setter
    def nodes_to_delete(self, val: UaDeleteNodesItem):
        self._nodes_to_delete = val
        self._value.nodesToDelete = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteNodesRequest): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteNodesRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_delete_size " + self._nodes_to_delete_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_delete " + self._nodes_to_delete.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaMonitoredItemModifyRequest +++++++++++++++++++++++
class UaMonitoredItemModifyRequest(UaType):
    _UA_TYPE = _UA_TYPES._MONITOREDITEMMODIFYREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_MonitoredItemModifyRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_MonitoredItemModifyRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._monitored_item_id = UaUInt32(val=val.monitoredItemId, is_pointer=False)
            self._requested_parameters = UaMonitoringParameters(val=val.requestedParameters, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_MonitoredItemModifyRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._monitored_item_id._value[0] = _val(val.monitoredItemId)
            self._requested_parameters._value[0] = _val(val.requestedParameters)

    @property
    def monitored_item_id(self):
        if self._null:
            return None
        else:
            return self._monitored_item_id

    @property
    def requested_parameters(self):
        if self._null:
            return None
        else:
            return self._requested_parameters

    @monitored_item_id.setter
    def monitored_item_id(self, val: UaUInt32):
        self._monitored_item_id = val
        self._value.monitoredItemId = val._val

    @requested_parameters.setter
    def requested_parameters(self, val: UaMonitoringParameters):
        self._requested_parameters = val
        self._value.requestedParameters = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaMonitoredItemModifyRequest): NULL" + ("" if n is None else "\n")

        return ("(UaMonitoredItemModifyRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "monitored_item_id " + self._monitored_item_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_parameters " + self._requested_parameters.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAggregateConfiguration +++++++++++++++++++++++
class UaAggregateConfiguration(UaType):
    _UA_TYPE = _UA_TYPES._AGGREGATECONFIGURATION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AggregateConfiguration*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AggregateConfiguration*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._use_server_capabilities_defaults = UaBoolean(val=val.useServerCapabilitiesDefaults, is_pointer=False)
            self._treat_uncertain_as_bad = UaBoolean(val=val.treatUncertainAsBad, is_pointer=False)
            self._percent_data_bad = UaByte(val=val.percentDataBad, is_pointer=False)
            self._percent_data_good = UaByte(val=val.percentDataGood, is_pointer=False)
            self._use_sloped_extrapolation = UaBoolean(val=val.useSlopedExtrapolation, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AggregateConfiguration")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._use_server_capabilities_defaults._value[0] = _val(val.useServerCapabilitiesDefaults)
            self._treat_uncertain_as_bad._value[0] = _val(val.treatUncertainAsBad)
            self._percent_data_bad._value[0] = _val(val.percentDataBad)
            self._percent_data_good._value[0] = _val(val.percentDataGood)
            self._use_sloped_extrapolation._value[0] = _val(val.useSlopedExtrapolation)

    @property
    def use_server_capabilities_defaults(self):
        if self._null:
            return None
        else:
            return self._use_server_capabilities_defaults

    @property
    def treat_uncertain_as_bad(self):
        if self._null:
            return None
        else:
            return self._treat_uncertain_as_bad

    @property
    def percent_data_bad(self):
        if self._null:
            return None
        else:
            return self._percent_data_bad

    @property
    def percent_data_good(self):
        if self._null:
            return None
        else:
            return self._percent_data_good

    @property
    def use_sloped_extrapolation(self):
        if self._null:
            return None
        else:
            return self._use_sloped_extrapolation

    @use_server_capabilities_defaults.setter
    def use_server_capabilities_defaults(self, val: UaBoolean):
        self._use_server_capabilities_defaults = val
        self._value.useServerCapabilitiesDefaults = val._val

    @treat_uncertain_as_bad.setter
    def treat_uncertain_as_bad(self, val: UaBoolean):
        self._treat_uncertain_as_bad = val
        self._value.treatUncertainAsBad = val._val

    @percent_data_bad.setter
    def percent_data_bad(self, val: UaByte):
        self._percent_data_bad = val
        self._value.percentDataBad = val._val

    @percent_data_good.setter
    def percent_data_good(self, val: UaByte):
        self._percent_data_good = val
        self._value.percentDataGood = val._val

    @use_sloped_extrapolation.setter
    def use_sloped_extrapolation(self, val: UaBoolean):
        self._use_sloped_extrapolation = val
        self._value.useSlopedExtrapolation = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaAggregateConfiguration): NULL" + ("" if n is None else "\n")

        return ("(UaAggregateConfiguration) :\n"
                + "\t" * (1 if n is None else n+1) + "use_server_capabilities_defaults " + self._use_server_capabilities_defaults.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "treat_uncertain_as_bad " + self._treat_uncertain_as_bad.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "percent_data_bad " + self._percent_data_bad.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "percent_data_good " + self._percent_data_good.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "use_sloped_extrapolation " + self._use_sloped_extrapolation.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaUnregisterNodesResponse +++++++++++++++++++++++
class UaUnregisterNodesResponse(UaType):
    _UA_TYPE = _UA_TYPES._UNREGISTERNODESRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_UnregisterNodesResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_UnregisterNodesResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UnregisterNodesResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaUnregisterNodesResponse): NULL" + ("" if n is None else "\n")

        return ("(UaUnregisterNodesResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaContentFilterResult +++++++++++++++++++++++
class UaContentFilterResult(UaType):
    _UA_TYPE = _UA_TYPES._CONTENTFILTERRESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ContentFilterResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ContentFilterResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._element_results_size = SizeT(val=val.elementResultsSize, is_pointer=False)
            self._element_results = UaContentFilterElementResult(val=val.elementResults, is_pointer=True)
            self._element_diagnostic_infos_size = SizeT(val=val.elementDiagnosticInfosSize, is_pointer=False)
            self._element_diagnostic_infos = UaDiagnosticInfo(val=val.elementDiagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ContentFilterResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._element_results_size._value[0] = _val(val.elementResultsSize)
            self._element_results._value = val.elementResults
            self._element_diagnostic_infos_size._value[0] = _val(val.elementDiagnosticInfosSize)
            self._element_diagnostic_infos._value = val.elementDiagnosticInfos

    @property
    def element_results_size(self):
        if self._null:
            return None
        else:
            return self._element_results_size

    @property
    def element_results(self):
        if self._null:
            return None
        else:
            return self._element_results

    @property
    def element_diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._element_diagnostic_infos_size

    @property
    def element_diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._element_diagnostic_infos

    @element_results_size.setter
    def element_results_size(self, val: SizeT):
        self._element_results_size = val
        self._value.elementResultsSize = val._val

    @element_results.setter
    def element_results(self, val: UaContentFilterElementResult):
        self._element_results = val
        self._value.elementResults = val._ptr

    @element_diagnostic_infos_size.setter
    def element_diagnostic_infos_size(self, val: SizeT):
        self._element_diagnostic_infos_size = val
        self._value.elementDiagnosticInfosSize = val._val

    @element_diagnostic_infos.setter
    def element_diagnostic_infos(self, val: UaDiagnosticInfo):
        self._element_diagnostic_infos = val
        self._value.elementDiagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaContentFilterResult): NULL" + ("" if n is None else "\n")

        return ("(UaContentFilterResult) :\n"
                + "\t" * (1 if n is None else n+1) + "element_results_size " + self._element_results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "element_results " + self._element_results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "element_diagnostic_infos_size " + self._element_diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "element_diagnostic_infos " + self._element_diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaUserTokenPolicy +++++++++++++++++++++++
class UaUserTokenPolicy(UaType):
    _UA_TYPE = _UA_TYPES._USERTOKENPOLICY

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_UserTokenPolicy*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_UserTokenPolicy*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._policy_id = UaString(val=val.policyId, is_pointer=False)
            self._token_type = UaUserTokenType(val=val.tokenType, is_pointer=False)
            self._issued_token_type = UaString(val=val.issuedTokenType, is_pointer=False)
            self._issuer_endpoint_url = UaString(val=val.issuerEndpointUrl, is_pointer=False)
            self._security_policy_uri = UaString(val=val.securityPolicyUri, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UserTokenPolicy")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._policy_id._value[0] = _val(val.policyId)
            self._token_type._value[0] = _val(val.tokenType)
            self._issued_token_type._value[0] = _val(val.issuedTokenType)
            self._issuer_endpoint_url._value[0] = _val(val.issuerEndpointUrl)
            self._security_policy_uri._value[0] = _val(val.securityPolicyUri)

    @property
    def policy_id(self):
        if self._null:
            return None
        else:
            return self._policy_id

    @property
    def token_type(self):
        if self._null:
            return None
        else:
            return self._token_type

    @property
    def issued_token_type(self):
        if self._null:
            return None
        else:
            return self._issued_token_type

    @property
    def issuer_endpoint_url(self):
        if self._null:
            return None
        else:
            return self._issuer_endpoint_url

    @property
    def security_policy_uri(self):
        if self._null:
            return None
        else:
            return self._security_policy_uri

    @policy_id.setter
    def policy_id(self, val: UaString):
        self._policy_id = val
        self._value.policyId = val._val

    @token_type.setter
    def token_type(self, val: UaUserTokenType):
        self._token_type = val
        self._value.tokenType = val._val

    @issued_token_type.setter
    def issued_token_type(self, val: UaString):
        self._issued_token_type = val
        self._value.issuedTokenType = val._val

    @issuer_endpoint_url.setter
    def issuer_endpoint_url(self, val: UaString):
        self._issuer_endpoint_url = val
        self._value.issuerEndpointUrl = val._val

    @security_policy_uri.setter
    def security_policy_uri(self, val: UaString):
        self._security_policy_uri = val
        self._value.securityPolicyUri = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaUserTokenPolicy): NULL" + ("" if n is None else "\n")

        return ("(UaUserTokenPolicy) :\n"
                + "\t" * (1 if n is None else n+1) + "policy_id " + self._policy_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "token_type " + self._token_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "issued_token_type " + self._issued_token_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "issuer_endpoint_url " + self._issuer_endpoint_url.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_policy_uri " + self._security_policy_uri.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteMonitoredItemsRequest +++++++++++++++++++++++
class UaDeleteMonitoredItemsRequest(UaType):
    _UA_TYPE = _UA_TYPES._DELETEMONITOREDITEMSREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteMonitoredItemsRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteMonitoredItemsRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
            self._monitored_item_ids_size = SizeT(val=val.monitoredItemIdsSize, is_pointer=False)
            self._monitored_item_ids = UaUInt32(val=val.monitoredItemIds, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteMonitoredItemsRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._monitored_item_ids_size._value[0] = _val(val.monitoredItemIdsSize)
            self._monitored_item_ids._value = val.monitoredItemIds

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def monitored_item_ids_size(self):
        if self._null:
            return None
        else:
            return self._monitored_item_ids_size

    @property
    def monitored_item_ids(self):
        if self._null:
            return None
        else:
            return self._monitored_item_ids

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @monitored_item_ids_size.setter
    def monitored_item_ids_size(self, val: SizeT):
        self._monitored_item_ids_size = val
        self._value.monitoredItemIdsSize = val._val

    @monitored_item_ids.setter
    def monitored_item_ids(self, val: UaUInt32):
        self._monitored_item_ids = val
        self._value.monitoredItemIds = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteMonitoredItemsRequest): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteMonitoredItemsRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "monitored_item_ids_size " + self._monitored_item_ids_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "monitored_item_ids " + self._monitored_item_ids.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSetMonitoringModeRequest +++++++++++++++++++++++
class UaSetMonitoringModeRequest(UaType):
    _UA_TYPE = _UA_TYPES._SETMONITORINGMODEREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SetMonitoringModeRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SetMonitoringModeRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
            self._monitoring_mode = UaMonitoringMode(val=val.monitoringMode, is_pointer=False)
            self._monitored_item_ids_size = SizeT(val=val.monitoredItemIdsSize, is_pointer=False)
            self._monitored_item_ids = UaUInt32(val=val.monitoredItemIds, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SetMonitoringModeRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._monitoring_mode._value[0] = _val(val.monitoringMode)
            self._monitored_item_ids_size._value[0] = _val(val.monitoredItemIdsSize)
            self._monitored_item_ids._value = val.monitoredItemIds

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def monitoring_mode(self):
        if self._null:
            return None
        else:
            return self._monitoring_mode

    @property
    def monitored_item_ids_size(self):
        if self._null:
            return None
        else:
            return self._monitored_item_ids_size

    @property
    def monitored_item_ids(self):
        if self._null:
            return None
        else:
            return self._monitored_item_ids

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @monitoring_mode.setter
    def monitoring_mode(self, val: UaMonitoringMode):
        self._monitoring_mode = val
        self._value.monitoringMode = val._val

    @monitored_item_ids_size.setter
    def monitored_item_ids_size(self, val: SizeT):
        self._monitored_item_ids_size = val
        self._value.monitoredItemIdsSize = val._val

    @monitored_item_ids.setter
    def monitored_item_ids(self, val: UaUInt32):
        self._monitored_item_ids = val
        self._value.monitoredItemIds = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaSetMonitoringModeRequest): NULL" + ("" if n is None else "\n")

        return ("(UaSetMonitoringModeRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "monitoring_mode " + self._monitoring_mode.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "monitored_item_ids_size " + self._monitored_item_ids_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "monitored_item_ids " + self._monitored_item_ids.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaReferenceTypeAttributes +++++++++++++++++++++++
class UaReferenceTypeAttributes(UaType):
    _UA_TYPE = _UA_TYPES._REFERENCETYPEATTRIBUTES

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ReferenceTypeAttributes*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ReferenceTypeAttributes*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
            self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)
            self._symmetric = UaBoolean(val=val.symmetric, is_pointer=False)
            self._inverse_name = UaLocalizedText(val=val.inverseName, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ReferenceTypeAttributes")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._specified_attributes._value[0] = _val(val.specifiedAttributes)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._user_write_mask._value[0] = _val(val.userWriteMask)
            self._is_abstract._value[0] = _val(val.isAbstract)
            self._symmetric._value[0] = _val(val.symmetric)
            self._inverse_name._value[0] = _val(val.inverseName)

    @property
    def specified_attributes(self):
        if self._null:
            return None
        else:
            return self._specified_attributes

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def user_write_mask(self):
        if self._null:
            return None
        else:
            return self._user_write_mask

    @property
    def is_abstract(self):
        if self._null:
            return None
        else:
            return self._is_abstract

    @property
    def symmetric(self):
        if self._null:
            return None
        else:
            return self._symmetric

    @property
    def inverse_name(self):
        if self._null:
            return None
        else:
            return self._inverse_name

    @specified_attributes.setter
    def specified_attributes(self, val: UaUInt32):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @user_write_mask.setter
    def user_write_mask(self, val: UaUInt32):
        self._user_write_mask = val
        self._value.userWriteMask = val._val

    @is_abstract.setter
    def is_abstract(self, val: UaBoolean):
        self._is_abstract = val
        self._value.isAbstract = val._val

    @symmetric.setter
    def symmetric(self, val: UaBoolean):
        self._symmetric = val
        self._value.symmetric = val._val

    @inverse_name.setter
    def inverse_name(self, val: UaLocalizedText):
        self._inverse_name = val
        self._value.inverseName = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaReferenceTypeAttributes): NULL" + ("" if n is None else "\n")

        return ("(UaReferenceTypeAttributes) :\n"
                + "\t" * (1 if n is None else n+1) + "specified_attributes " + self._specified_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_write_mask " + self._user_write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_abstract " + self._is_abstract.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "symmetric " + self._symmetric.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "inverse_name " + self._inverse_name.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaGetEndpointsRequest +++++++++++++++++++++++
class UaGetEndpointsRequest(UaType):
    _UA_TYPE = _UA_TYPES._GETENDPOINTSREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_GetEndpointsRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_GetEndpointsRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._endpoint_url = UaString(val=val.endpointUrl, is_pointer=False)
            self._locale_ids_size = SizeT(val=val.localeIdsSize, is_pointer=False)
            self._locale_ids = UaString(val=val.localeIds, is_pointer=True)
            self._profile_uris_size = SizeT(val=val.profileUrisSize, is_pointer=False)
            self._profile_uris = UaString(val=val.profileUris, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_GetEndpointsRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._endpoint_url._value[0] = _val(val.endpointUrl)
            self._locale_ids_size._value[0] = _val(val.localeIdsSize)
            self._locale_ids._value = val.localeIds
            self._profile_uris_size._value[0] = _val(val.profileUrisSize)
            self._profile_uris._value = val.profileUris

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def endpoint_url(self):
        if self._null:
            return None
        else:
            return self._endpoint_url

    @property
    def locale_ids_size(self):
        if self._null:
            return None
        else:
            return self._locale_ids_size

    @property
    def locale_ids(self):
        if self._null:
            return None
        else:
            return self._locale_ids

    @property
    def profile_uris_size(self):
        if self._null:
            return None
        else:
            return self._profile_uris_size

    @property
    def profile_uris(self):
        if self._null:
            return None
        else:
            return self._profile_uris

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @endpoint_url.setter
    def endpoint_url(self, val: UaString):
        self._endpoint_url = val
        self._value.endpointUrl = val._val

    @locale_ids_size.setter
    def locale_ids_size(self, val: SizeT):
        self._locale_ids_size = val
        self._value.localeIdsSize = val._val

    @locale_ids.setter
    def locale_ids(self, val: UaString):
        self._locale_ids = val
        self._value.localeIds = val._ptr

    @profile_uris_size.setter
    def profile_uris_size(self, val: SizeT):
        self._profile_uris_size = val
        self._value.profileUrisSize = val._val

    @profile_uris.setter
    def profile_uris(self, val: UaString):
        self._profile_uris = val
        self._value.profileUris = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaGetEndpointsRequest): NULL" + ("" if n is None else "\n")

        return ("(UaGetEndpointsRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "endpoint_url " + self._endpoint_url.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "locale_ids_size " + self._locale_ids_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "locale_ids " + self._locale_ids.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "profile_uris_size " + self._profile_uris_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "profile_uris " + self._profile_uris.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCloseSecureChannelResponse +++++++++++++++++++++++
class UaCloseSecureChannelResponse(UaType):
    _UA_TYPE = _UA_TYPES._CLOSESECURECHANNELRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CloseSecureChannelResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CloseSecureChannelResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CloseSecureChannelResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaCloseSecureChannelResponse): NULL" + ("" if n is None else "\n")

        return ("(UaCloseSecureChannelResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaViewDescription +++++++++++++++++++++++
class UaViewDescription(UaType):
    _UA_TYPE = _UA_TYPES._VIEWDESCRIPTION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ViewDescription*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ViewDescription*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._view_id = UaNodeId(val=val.viewId, is_pointer=False)
            self._timestamp = UaDateTime(val=val.timestamp, is_pointer=False)
            self._view_version = UaUInt32(val=val.viewVersion, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ViewDescription")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._view_id._value[0] = _val(val.viewId)
            self._timestamp._value[0] = _val(val.timestamp)
            self._view_version._value[0] = _val(val.viewVersion)

    @property
    def view_id(self):
        if self._null:
            return None
        else:
            return self._view_id

    @property
    def timestamp(self):
        if self._null:
            return None
        else:
            return self._timestamp

    @property
    def view_version(self):
        if self._null:
            return None
        else:
            return self._view_version

    @view_id.setter
    def view_id(self, val: UaNodeId):
        self._view_id = val
        self._value.viewId = val._val

    @timestamp.setter
    def timestamp(self, val: UaDateTime):
        self._timestamp = val
        self._value.timestamp = val._val

    @view_version.setter
    def view_version(self, val: UaUInt32):
        self._view_version = val
        self._value.viewVersion = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaViewDescription): NULL" + ("" if n is None else "\n")

        return ("(UaViewDescription) :\n"
                + "\t" * (1 if n is None else n+1) + "view_id " + self._view_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "timestamp " + self._timestamp.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "view_version " + self._view_version.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSetPublishingModeResponse +++++++++++++++++++++++
class UaSetPublishingModeResponse(UaType):
    _UA_TYPE = _UA_TYPES._SETPUBLISHINGMODERESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SetPublishingModeResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SetPublishingModeResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaStatusCode(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SetPublishingModeResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaSetPublishingModeResponse): NULL" + ("" if n is None else "\n")

        return ("(UaSetPublishingModeResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaStatusChangeNotification +++++++++++++++++++++++
class UaStatusChangeNotification(UaType):
    _UA_TYPE = _UA_TYPES._STATUSCHANGENOTIFICATION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_StatusChangeNotification*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_StatusChangeNotification*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._status = UaStatusCode(val=val.status, is_pointer=False)
            self._diagnostic_info = UaDiagnosticInfo(val=val.diagnosticInfo, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_StatusChangeNotification")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._status._value[0] = _val(val.status)
            self._diagnostic_info._value[0] = _val(val.diagnosticInfo)

    @property
    def status(self):
        if self._null:
            return None
        else:
            return self._status

    @property
    def diagnostic_info(self):
        if self._null:
            return None
        else:
            return self._diagnostic_info

    @status.setter
    def status(self, val: UaStatusCode):
        self._status = val
        self._value.status = val._val

    @diagnostic_info.setter
    def diagnostic_info(self, val: UaDiagnosticInfo):
        self._diagnostic_info = val
        self._value.diagnosticInfo = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaStatusChangeNotification): NULL" + ("" if n is None else "\n")

        return ("(UaStatusChangeNotification) :\n"
                + "\t" * (1 if n is None else n+1) + "status " + self._status.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_info " + self._diagnostic_info.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaStructureField +++++++++++++++++++++++
class UaStructureField(UaType):
    _UA_TYPE = _UA_TYPES._STRUCTUREFIELD

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_StructureField*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_StructureField*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._name = UaString(val=val.name, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._data_type = UaNodeId(val=val.dataType, is_pointer=False)
            self._value_rank = UaInt32(val=val.valueRank, is_pointer=False)
            self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
            self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
            self._max_string_length = UaUInt32(val=val.maxStringLength, is_pointer=False)
            self._is_optional = UaBoolean(val=val.isOptional, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_StructureField")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._name._value[0] = _val(val.name)
            self._description._value[0] = _val(val.description)
            self._data_type._value[0] = _val(val.dataType)
            self._value_rank._value[0] = _val(val.valueRank)
            self._array_dimensions_size._value[0] = _val(val.arrayDimensionsSize)
            self._array_dimensions._value = val.arrayDimensions
            self._max_string_length._value[0] = _val(val.maxStringLength)
            self._is_optional._value[0] = _val(val.isOptional)

    @property
    def name(self):
        if self._null:
            return None
        else:
            return self._name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def data_type(self):
        if self._null:
            return None
        else:
            return self._data_type

    @property
    def value_rank(self):
        if self._null:
            return None
        else:
            return self._value_rank

    @property
    def array_dimensions_size(self):
        if self._null:
            return None
        else:
            return self._array_dimensions_size

    @property
    def array_dimensions(self):
        if self._null:
            return None
        else:
            return self._array_dimensions

    @property
    def max_string_length(self):
        if self._null:
            return None
        else:
            return self._max_string_length

    @property
    def is_optional(self):
        if self._null:
            return None
        else:
            return self._is_optional

    @name.setter
    def name(self, val: UaString):
        self._name = val
        self._value.name = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @data_type.setter
    def data_type(self, val: UaNodeId):
        self._data_type = val
        self._value.dataType = val._val

    @value_rank.setter
    def value_rank(self, val: UaInt32):
        self._value_rank = val
        self._value.valueRank = val._val

    @array_dimensions_size.setter
    def array_dimensions_size(self, val: SizeT):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._val

    @array_dimensions.setter
    def array_dimensions(self, val: UaUInt32):
        self._array_dimensions = val
        self._value.arrayDimensions = val._ptr

    @max_string_length.setter
    def max_string_length(self, val: UaUInt32):
        self._max_string_length = val
        self._value.maxStringLength = val._val

    @is_optional.setter
    def is_optional(self, val: UaBoolean):
        self._is_optional = val
        self._value.isOptional = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaStructureField): NULL" + ("" if n is None else "\n")

        return ("(UaStructureField) :\n"
                + "\t" * (1 if n is None else n+1) + "name " + self._name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_type " + self._data_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "value_rank " + self._value_rank.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "array_dimensions_size " + self._array_dimensions_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "array_dimensions " + self._array_dimensions.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_string_length " + self._max_string_length.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_optional " + self._is_optional.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaEventFilterResult +++++++++++++++++++++++
class UaEventFilterResult(UaType):
    _UA_TYPE = _UA_TYPES._EVENTFILTERRESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_EventFilterResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_EventFilterResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._select_clause_results_size = SizeT(val=val.selectClauseResultsSize, is_pointer=False)
            self._select_clause_results = UaStatusCode(val=val.selectClauseResults, is_pointer=True)
            self._select_clause_diagnostic_infos_size = SizeT(val=val.selectClauseDiagnosticInfosSize, is_pointer=False)
            self._select_clause_diagnostic_infos = UaDiagnosticInfo(val=val.selectClauseDiagnosticInfos,
                                                                    is_pointer=True)
            self._where_clause_result = UaContentFilterResult(val=val.whereClauseResult, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_EventFilterResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._select_clause_results_size._value[0] = _val(val.selectClauseResultsSize)
            self._select_clause_results._value = val.selectClauseResults
            self._select_clause_diagnostic_infos_size._value[0] = _val(val.selectClauseDiagnosticInfosSize)
            self._select_clause_diagnostic_infos._value = val.selectClauseDiagnosticInfos
            self._where_clause_result._value[0] = _val(val.whereClauseResult)

    @property
    def select_clause_results_size(self):
        if self._null:
            return None
        else:
            return self._select_clause_results_size

    @property
    def select_clause_results(self):
        if self._null:
            return None
        else:
            return self._select_clause_results

    @property
    def select_clause_diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._select_clause_diagnostic_infos_size

    @property
    def select_clause_diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._select_clause_diagnostic_infos

    @property
    def where_clause_result(self):
        if self._null:
            return None
        else:
            return self._where_clause_result

    @select_clause_results_size.setter
    def select_clause_results_size(self, val: SizeT):
        self._select_clause_results_size = val
        self._value.selectClauseResultsSize = val._val

    @select_clause_results.setter
    def select_clause_results(self, val: UaStatusCode):
        self._select_clause_results = val
        self._value.selectClauseResults = val._ptr

    @select_clause_diagnostic_infos_size.setter
    def select_clause_diagnostic_infos_size(self, val: SizeT):
        self._select_clause_diagnostic_infos_size = val
        self._value.selectClauseDiagnosticInfosSize = val._val

    @select_clause_diagnostic_infos.setter
    def select_clause_diagnostic_infos(self, val: UaDiagnosticInfo):
        self._select_clause_diagnostic_infos = val
        self._value.selectClauseDiagnosticInfos = val._ptr

    @where_clause_result.setter
    def where_clause_result(self, val: UaContentFilterResult):
        self._where_clause_result = val
        self._value.whereClauseResult = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaEventFilterResult): NULL" + ("" if n is None else "\n")

        return ("(UaEventFilterResult) :\n"
                + "\t" * (1 if n is None else n+1) + "select_clause_results_size " + self._select_clause_results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "select_clause_results " + self._select_clause_results.__str__(1 if n is None else n+1)
                + "\t" * (
                            n + 1) + "select_clause_diagnostic_infos_size " + self._select_clause_diagnostic_infos_size.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "select_clause_diagnostic_infos " + self._select_clause_diagnostic_infos.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "where_clause_result " + self._where_clause_result.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaMonitoredItemCreateRequest +++++++++++++++++++++++
class UaMonitoredItemCreateRequest(UaType):
    _UA_TYPE = _UA_TYPES._MONITOREDITEMCREATEREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_MonitoredItemCreateRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_MonitoredItemCreateRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._item_to_monitor = UaReadValueId(val=val.itemToMonitor, is_pointer=False)
            self._monitoring_mode = UaMonitoringMode(val=val.monitoringMode, is_pointer=False)
            self._requested_parameters = UaMonitoringParameters(val=val.requestedParameters, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_MonitoredItemCreateRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._item_to_monitor._value[0] = _val(val.itemToMonitor)
            self._monitoring_mode._value[0] = _val(val.monitoringMode)
            self._requested_parameters._value[0] = _val(val.requestedParameters)

    @property
    def item_to_monitor(self):
        if self._null:
            return None
        else:
            return self._item_to_monitor

    @property
    def monitoring_mode(self):
        if self._null:
            return None
        else:
            return self._monitoring_mode

    @property
    def requested_parameters(self):
        if self._null:
            return None
        else:
            return self._requested_parameters

    @item_to_monitor.setter
    def item_to_monitor(self, val: UaReadValueId):
        self._item_to_monitor = val
        self._value.itemToMonitor = val._val

    @monitoring_mode.setter
    def monitoring_mode(self, val: UaMonitoringMode):
        self._monitoring_mode = val
        self._value.monitoringMode = val._val

    @requested_parameters.setter
    def requested_parameters(self, val: UaMonitoringParameters):
        self._requested_parameters = val
        self._value.requestedParameters = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaMonitoredItemCreateRequest): NULL" + ("" if n is None else "\n")

        return ("(UaMonitoredItemCreateRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "item_to_monitor " + self._item_to_monitor.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "monitoring_mode " + self._monitoring_mode.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_parameters " + self._requested_parameters.__str__(1 if n is None else n+1))
    @staticmethod
    def default(node_id: UaNodeId):
        return UaMonitoredItemCreateRequest(val=lib.UA_MonitoredItemCreateRequest_default(node_id._val))


# +++++++++++++++++++ UaComplexNumberType +++++++++++++++++++++++
class UaComplexNumberType(UaType):
    _UA_TYPE = _UA_TYPES._COMPLEXNUMBERTYPE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ComplexNumberType*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ComplexNumberType*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._real = UaFloat(val=val.real, is_pointer=False)
            self._imaginary = UaFloat(val=val.imaginary, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ComplexNumberType")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._real._value[0] = _val(val.real)
            self._imaginary._value[0] = _val(val.imaginary)

    @property
    def real(self):
        if self._null:
            return None
        else:
            return self._real

    @property
    def imaginary(self):
        if self._null:
            return None
        else:
            return self._imaginary

    @real.setter
    def real(self, val: UaFloat):
        self._real = val
        self._value.real = val._val

    @imaginary.setter
    def imaginary(self, val: UaFloat):
        self._imaginary = val
        self._value.imaginary = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaComplexNumberType): NULL" + ("" if n is None else "\n")

        return ("(UaComplexNumberType) :\n"
                + "\t" * (1 if n is None else n+1) + "real " + self._real.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "imaginary " + self._imaginary.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaRange +++++++++++++++++++++++
class UaRange(UaType):
    _UA_TYPE = _UA_TYPES._RANGE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_Range*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_Range*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._low = UaDouble(val=val.low, is_pointer=False)
            self._high = UaDouble(val=val.high, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Range")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._low._value[0] = _val(val.low)
            self._high._value[0] = _val(val.high)

    @property
    def low(self):
        if self._null:
            return None
        else:
            return self._low

    @property
    def high(self):
        if self._null:
            return None
        else:
            return self._high

    @low.setter
    def low(self, val: UaDouble):
        self._low = val
        self._value.low = val._val

    @high.setter
    def high(self, val: UaDouble):
        self._high = val
        self._value.high = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaRange): NULL" + ("" if n is None else "\n")

        return ("(UaRange) :\n"
                + "\t" * (1 if n is None else n+1) + "low " + self._low.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "high " + self._high.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDataChangeNotification +++++++++++++++++++++++
class UaDataChangeNotification(UaType):
    _UA_TYPE = _UA_TYPES._DATACHANGENOTIFICATION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataChangeNotification*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DataChangeNotification*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._monitored_items_size = SizeT(val=val.monitoredItemsSize, is_pointer=False)
            self._monitored_items = UaMonitoredItemNotification(val=val.monitoredItems, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataChangeNotification")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._monitored_items_size._value[0] = _val(val.monitoredItemsSize)
            self._monitored_items._value = val.monitoredItems
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def monitored_items_size(self):
        if self._null:
            return None
        else:
            return self._monitored_items_size

    @property
    def monitored_items(self):
        if self._null:
            return None
        else:
            return self._monitored_items

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @monitored_items_size.setter
    def monitored_items_size(self, val: SizeT):
        self._monitored_items_size = val
        self._value.monitoredItemsSize = val._val

    @monitored_items.setter
    def monitored_items(self, val: UaMonitoredItemNotification):
        self._monitored_items = val
        self._value.monitoredItems = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaDataChangeNotification): NULL" + ("" if n is None else "\n")

        return ("(UaDataChangeNotification) :\n"
                + "\t" * (1 if n is None else n+1) + "monitored_items_size " + self._monitored_items_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "monitored_items " + self._monitored_items.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaArgument +++++++++++++++++++++++
class UaArgument(UaType):
    _UA_TYPE = _UA_TYPES._ARGUMENT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_Argument*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_Argument*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._name = UaString(val=val.name, is_pointer=False)
            self._data_type = UaNodeId(val=val.dataType, is_pointer=False)
            self._value_rank = UaInt32(val=val.valueRank, is_pointer=False)
            self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
            self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Argument")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._name._value[0] = _val(val.name)
            self._data_type._value[0] = _val(val.dataType)
            self._value_rank._value[0] = _val(val.valueRank)
            self._array_dimensions_size._value[0] = _val(val.arrayDimensionsSize)
            self._array_dimensions._value = val.arrayDimensions
            self._description._value[0] = _val(val.description)

    @property
    def name(self):
        if self._null:
            return None
        else:
            return self._name

    @property
    def data_type(self):
        if self._null:
            return None
        else:
            return self._data_type

    @property
    def value_rank(self):
        if self._null:
            return None
        else:
            return self._value_rank

    @property
    def array_dimensions_size(self):
        if self._null:
            return None
        else:
            return self._array_dimensions_size

    @property
    def array_dimensions(self):
        if self._null:
            return None
        else:
            return self._array_dimensions

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @name.setter
    def name(self, val: UaString):
        self._name = val
        self._value.name = val._val

    @data_type.setter
    def data_type(self, val: UaNodeId):
        self._data_type = val
        self._value.dataType = val._val

    @value_rank.setter
    def value_rank(self, val: UaInt32):
        self._value_rank = val
        self._value.valueRank = val._val

    @array_dimensions_size.setter
    def array_dimensions_size(self, val: SizeT):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._val

    @array_dimensions.setter
    def array_dimensions(self, val: UaUInt32):
        self._array_dimensions = val
        self._value.arrayDimensions = val._ptr

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaArgument): NULL" + ("" if n is None else "\n")

        return ("(UaArgument) :\n"
                + "\t" * (1 if n is None else n+1) + "name " + self._name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "data_type " + self._data_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "value_rank " + self._value_rank.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "array_dimensions_size " + self._array_dimensions_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "array_dimensions " + self._array_dimensions.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaTransferSubscriptionsRequest +++++++++++++++++++++++
class UaTransferSubscriptionsRequest(UaType):
    _UA_TYPE = _UA_TYPES._TRANSFERSUBSCRIPTIONSREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_TransferSubscriptionsRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_TransferSubscriptionsRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_ids_size = SizeT(val=val.subscriptionIdsSize, is_pointer=False)
            self._subscription_ids = UaUInt32(val=val.subscriptionIds, is_pointer=True)
            self._send_initial_values = UaBoolean(val=val.sendInitialValues, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_TransferSubscriptionsRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_ids_size._value[0] = _val(val.subscriptionIdsSize)
            self._subscription_ids._value = val.subscriptionIds
            self._send_initial_values._value[0] = _val(val.sendInitialValues)

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_ids_size(self):
        if self._null:
            return None
        else:
            return self._subscription_ids_size

    @property
    def subscription_ids(self):
        if self._null:
            return None
        else:
            return self._subscription_ids

    @property
    def send_initial_values(self):
        if self._null:
            return None
        else:
            return self._send_initial_values

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_ids_size.setter
    def subscription_ids_size(self, val: SizeT):
        self._subscription_ids_size = val
        self._value.subscriptionIdsSize = val._val

    @subscription_ids.setter
    def subscription_ids(self, val: UaUInt32):
        self._subscription_ids = val
        self._value.subscriptionIds = val._ptr

    @send_initial_values.setter
    def send_initial_values(self, val: UaBoolean):
        self._send_initial_values = val
        self._value.sendInitialValues = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaTransferSubscriptionsRequest): NULL" + ("" if n is None else "\n")

        return ("(UaTransferSubscriptionsRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_ids_size " + self._subscription_ids_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_ids " + self._subscription_ids.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "send_initial_values " + self._send_initial_values.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaChannelSecurityToken +++++++++++++++++++++++
class UaChannelSecurityToken(UaType):
    _UA_TYPE = _UA_TYPES._CHANNELSECURITYTOKEN

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ChannelSecurityToken*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ChannelSecurityToken*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._channel_id = UaUInt32(val=val.channelId, is_pointer=False)
            self._token_id = UaUInt32(val=val.tokenId, is_pointer=False)
            self._created_at = UaDateTime(val=val.createdAt, is_pointer=False)
            self._revised_lifetime = UaUInt32(val=val.revisedLifetime, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ChannelSecurityToken")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._channel_id._value[0] = _val(val.channelId)
            self._token_id._value[0] = _val(val.tokenId)
            self._created_at._value[0] = _val(val.createdAt)
            self._revised_lifetime._value[0] = _val(val.revisedLifetime)

    @property
    def channel_id(self):
        if self._null:
            return None
        else:
            return self._channel_id

    @property
    def token_id(self):
        if self._null:
            return None
        else:
            return self._token_id

    @property
    def created_at(self):
        if self._null:
            return None
        else:
            return self._created_at

    @property
    def revised_lifetime(self):
        if self._null:
            return None
        else:
            return self._revised_lifetime

    @channel_id.setter
    def channel_id(self, val: UaUInt32):
        self._channel_id = val
        self._value.channelId = val._val

    @token_id.setter
    def token_id(self, val: UaUInt32):
        self._token_id = val
        self._value.tokenId = val._val

    @created_at.setter
    def created_at(self, val: UaDateTime):
        self._created_at = val
        self._value.createdAt = val._val

    @revised_lifetime.setter
    def revised_lifetime(self, val: UaUInt32):
        self._revised_lifetime = val
        self._value.revisedLifetime = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaChannelSecurityToken): NULL" + ("" if n is None else "\n")

        return ("(UaChannelSecurityToken) :\n"
                + "\t" * (1 if n is None else n+1) + "channel_id " + self._channel_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "token_id " + self._token_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "created_at " + self._created_at.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_lifetime " + self._revised_lifetime.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaEventNotificationList +++++++++++++++++++++++
class UaEventNotificationList(UaType):
    _UA_TYPE = _UA_TYPES._EVENTNOTIFICATIONLIST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_EventNotificationList*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_EventNotificationList*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._events_size = SizeT(val=val.eventsSize, is_pointer=False)
            self._events = UaEventFieldList(val=val.events, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_EventNotificationList")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._events_size._value[0] = _val(val.eventsSize)
            self._events._value = val.events

    @property
    def events_size(self):
        if self._null:
            return None
        else:
            return self._events_size

    @property
    def events(self):
        if self._null:
            return None
        else:
            return self._events

    @events_size.setter
    def events_size(self, val: SizeT):
        self._events_size = val
        self._value.eventsSize = val._val

    @events.setter
    def events(self, val: UaEventFieldList):
        self._events = val
        self._value.events = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaEventNotificationList): NULL" + ("" if n is None else "\n")

        return ("(UaEventNotificationList) :\n"
                + "\t" * (1 if n is None else n+1) + "events_size " + self._events_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "events " + self._events.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAnonymousIdentityToken +++++++++++++++++++++++
class UaAnonymousIdentityToken(UaType):
    _UA_TYPE = _UA_TYPES._ANONYMOUSIDENTITYTOKEN

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AnonymousIdentityToken*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AnonymousIdentityToken*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._policy_id = UaString(val=val.policyId, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AnonymousIdentityToken")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._policy_id._value[0] = _val(val.policyId)

    @property
    def policy_id(self):
        if self._null:
            return None
        else:
            return self._policy_id

    @policy_id.setter
    def policy_id(self, val: UaString):
        self._policy_id = val
        self._value.policyId = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaAnonymousIdentityToken): NULL" + ("" if n is None else "\n")

        return ("(UaAnonymousIdentityToken) :\n"
                + "\t" * (1 if n is None else n+1) + "policy_id " + self._policy_id.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAggregateFilter +++++++++++++++++++++++
class UaAggregateFilter(UaType):
    _UA_TYPE = _UA_TYPES._AGGREGATEFILTER

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AggregateFilter*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AggregateFilter*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._start_time = UaDateTime(val=val.startTime, is_pointer=False)
            self._aggregate_type = UaNodeId(val=val.aggregateType, is_pointer=False)
            self._processing_interval = UaDouble(val=val.processingInterval, is_pointer=False)
            self._aggregate_configuration = UaAggregateConfiguration(val=val.aggregateConfiguration, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AggregateFilter")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._start_time._value[0] = _val(val.startTime)
            self._aggregate_type._value[0] = _val(val.aggregateType)
            self._processing_interval._value[0] = _val(val.processingInterval)
            self._aggregate_configuration._value[0] = _val(val.aggregateConfiguration)

    @property
    def start_time(self):
        if self._null:
            return None
        else:
            return self._start_time

    @property
    def aggregate_type(self):
        if self._null:
            return None
        else:
            return self._aggregate_type

    @property
    def processing_interval(self):
        if self._null:
            return None
        else:
            return self._processing_interval

    @property
    def aggregate_configuration(self):
        if self._null:
            return None
        else:
            return self._aggregate_configuration

    @start_time.setter
    def start_time(self, val: UaDateTime):
        self._start_time = val
        self._value.startTime = val._val

    @aggregate_type.setter
    def aggregate_type(self, val: UaNodeId):
        self._aggregate_type = val
        self._value.aggregateType = val._val

    @processing_interval.setter
    def processing_interval(self, val: UaDouble):
        self._processing_interval = val
        self._value.processingInterval = val._val

    @aggregate_configuration.setter
    def aggregate_configuration(self, val: UaAggregateConfiguration):
        self._aggregate_configuration = val
        self._value.aggregateConfiguration = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaAggregateFilter): NULL" + ("" if n is None else "\n")

        return ("(UaAggregateFilter) :\n"
                + "\t" * (1 if n is None else n+1) + "start_time " + self._start_time.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "aggregate_type " + self._aggregate_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "processing_interval " + self._processing_interval.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "aggregate_configuration " + self._aggregate_configuration.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaRepublishResponse +++++++++++++++++++++++
class UaRepublishResponse(UaType):
    _UA_TYPE = _UA_TYPES._REPUBLISHRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_RepublishResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_RepublishResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._notification_message = UaNotificationMessage(val=val.notificationMessage, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_RepublishResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._notification_message._value[0] = _val(val.notificationMessage)

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def notification_message(self):
        if self._null:
            return None
        else:
            return self._notification_message

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @notification_message.setter
    def notification_message(self, val: UaNotificationMessage):
        self._notification_message = val
        self._value.notificationMessage = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaRepublishResponse): NULL" + ("" if n is None else "\n")

        return ("(UaRepublishResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "notification_message " + self._notification_message.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteSubscriptionsResponse +++++++++++++++++++++++
class UaDeleteSubscriptionsResponse(UaType):
    _UA_TYPE = _UA_TYPES._DELETESUBSCRIPTIONSRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteSubscriptionsResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteSubscriptionsResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaStatusCode(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteSubscriptionsResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteSubscriptionsResponse): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteSubscriptionsResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaRegisterNodesRequest +++++++++++++++++++++++
class UaRegisterNodesRequest(UaType):
    _UA_TYPE = _UA_TYPES._REGISTERNODESREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_RegisterNodesRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_RegisterNodesRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._nodes_to_register_size = SizeT(val=val.nodesToRegisterSize, is_pointer=False)
            self._nodes_to_register = UaNodeId(val=val.nodesToRegister, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_RegisterNodesRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._nodes_to_register_size._value[0] = _val(val.nodesToRegisterSize)
            self._nodes_to_register._value = val.nodesToRegister

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def nodes_to_register_size(self):
        if self._null:
            return None
        else:
            return self._nodes_to_register_size

    @property
    def nodes_to_register(self):
        if self._null:
            return None
        else:
            return self._nodes_to_register

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @nodes_to_register_size.setter
    def nodes_to_register_size(self, val: SizeT):
        self._nodes_to_register_size = val
        self._value.nodesToRegisterSize = val._val

    @nodes_to_register.setter
    def nodes_to_register(self, val: UaNodeId):
        self._nodes_to_register = val
        self._value.nodesToRegister = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaRegisterNodesRequest): NULL" + ("" if n is None else "\n")

        return ("(UaRegisterNodesRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_register_size " + self._nodes_to_register_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_register " + self._nodes_to_register.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaStructureDefinition +++++++++++++++++++++++
class UaStructureDefinition(UaType):
    _UA_TYPE = _UA_TYPES._STRUCTUREDEFINITION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_StructureDefinition*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_StructureDefinition*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._default_encoding_id = UaNodeId(val=val.defaultEncodingId, is_pointer=False)
            self._base_data_type = UaNodeId(val=val.baseDataType, is_pointer=False)
            self._structure_type = UaStructureType(val=val.structureType, is_pointer=False)
            self._fields_size = SizeT(val=val.fieldsSize, is_pointer=False)
            self._fields = UaStructureField(val=val.fields, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_StructureDefinition")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._default_encoding_id._value[0] = _val(val.defaultEncodingId)
            self._base_data_type._value[0] = _val(val.baseDataType)
            self._structure_type._value[0] = _val(val.structureType)
            self._fields_size._value[0] = _val(val.fieldsSize)
            self._fields._value = val.fields

    @property
    def default_encoding_id(self):
        if self._null:
            return None
        else:
            return self._default_encoding_id

    @property
    def base_data_type(self):
        if self._null:
            return None
        else:
            return self._base_data_type

    @property
    def structure_type(self):
        if self._null:
            return None
        else:
            return self._structure_type

    @property
    def fields_size(self):
        if self._null:
            return None
        else:
            return self._fields_size

    @property
    def fields(self):
        if self._null:
            return None
        else:
            return self._fields

    @default_encoding_id.setter
    def default_encoding_id(self, val: UaNodeId):
        self._default_encoding_id = val
        self._value.defaultEncodingId = val._val

    @base_data_type.setter
    def base_data_type(self, val: UaNodeId):
        self._base_data_type = val
        self._value.baseDataType = val._val

    @structure_type.setter
    def structure_type(self, val: UaStructureType):
        self._structure_type = val
        self._value.structureType = val._val

    @fields_size.setter
    def fields_size(self, val: SizeT):
        self._fields_size = val
        self._value.fieldsSize = val._val

    @fields.setter
    def fields(self, val: UaStructureField):
        self._fields = val
        self._value.fields = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaStructureDefinition): NULL" + ("" if n is None else "\n")

        return ("(UaStructureDefinition) :\n"
                + "\t" * (1 if n is None else n+1) + "default_encoding_id " + self._default_encoding_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "base_data_type " + self._base_data_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "structure_type " + self._structure_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "fields_size " + self._fields_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "fields " + self._fields.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaMethodAttributes +++++++++++++++++++++++
class UaMethodAttributes(UaType):
    _UA_TYPE = _UA_TYPES._METHODATTRIBUTES

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_MethodAttributes*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_MethodAttributes*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
            self._executable = UaBoolean(val=val.executable, is_pointer=False)
            self._user_executable = UaBoolean(val=val.userExecutable, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_MethodAttributes")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._specified_attributes._value[0] = _val(val.specifiedAttributes)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._user_write_mask._value[0] = _val(val.userWriteMask)
            self._executable._value[0] = _val(val.executable)
            self._user_executable._value[0] = _val(val.userExecutable)

    @property
    def specified_attributes(self):
        if self._null:
            return None
        else:
            return self._specified_attributes

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def user_write_mask(self):
        if self._null:
            return None
        else:
            return self._user_write_mask

    @property
    def executable(self):
        if self._null:
            return None
        else:
            return self._executable

    @property
    def user_executable(self):
        if self._null:
            return None
        else:
            return self._user_executable

    @specified_attributes.setter
    def specified_attributes(self, val: UaUInt32):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @user_write_mask.setter
    def user_write_mask(self, val: UaUInt32):
        self._user_write_mask = val
        self._value.userWriteMask = val._val

    @executable.setter
    def executable(self, val: UaBoolean):
        self._executable = val
        self._value.executable = val._val

    @user_executable.setter
    def user_executable(self, val: UaBoolean):
        self._user_executable = val
        self._value.userExecutable = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaMethodAttributes): NULL" + ("" if n is None else "\n")

        return ("(UaMethodAttributes) :\n"
                + "\t" * (1 if n is None else n+1) + "specified_attributes " + self._specified_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_write_mask " + self._user_write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "executable " + self._executable.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_executable " + self._user_executable.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaUserNameIdentityToken +++++++++++++++++++++++
class UaUserNameIdentityToken(UaType):
    _UA_TYPE = _UA_TYPES._USERNAMEIDENTITYTOKEN

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_UserNameIdentityToken*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_UserNameIdentityToken*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._policy_id = UaString(val=val.policyId, is_pointer=False)
            self._user_name = UaString(val=val.userName, is_pointer=False)
            self._password = UaByteString(val=val.password, is_pointer=False)
            self._encryption_algorithm = UaString(val=val.encryptionAlgorithm, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UserNameIdentityToken")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._policy_id._value[0] = _val(val.policyId)
            self._user_name._value[0] = _val(val.userName)
            self._password._value[0] = _val(val.password)
            self._encryption_algorithm._value[0] = _val(val.encryptionAlgorithm)

    @property
    def policy_id(self):
        if self._null:
            return None
        else:
            return self._policy_id

    @property
    def user_name(self):
        if self._null:
            return None
        else:
            return self._user_name

    @property
    def password(self):
        if self._null:
            return None
        else:
            return self._password

    @property
    def encryption_algorithm(self):
        if self._null:
            return None
        else:
            return self._encryption_algorithm

    @policy_id.setter
    def policy_id(self, val: UaString):
        self._policy_id = val
        self._value.policyId = val._val

    @user_name.setter
    def user_name(self, val: UaString):
        self._user_name = val
        self._value.userName = val._val

    @password.setter
    def password(self, val: UaByteString):
        self._password = val
        self._value.password = val._val

    @encryption_algorithm.setter
    def encryption_algorithm(self, val: UaString):
        self._encryption_algorithm = val
        self._value.encryptionAlgorithm = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaUserNameIdentityToken): NULL" + ("" if n is None else "\n")

        return ("(UaUserNameIdentityToken) :\n"
                + "\t" * (1 if n is None else n+1) + "policy_id " + self._policy_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_name " + self._user_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "password " + self._password.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "encryption_algorithm " + self._encryption_algorithm.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaUnregisterNodesRequest +++++++++++++++++++++++
class UaUnregisterNodesRequest(UaType):
    _UA_TYPE = _UA_TYPES._UNREGISTERNODESREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_UnregisterNodesRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_UnregisterNodesRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._nodes_to_unregister_size = SizeT(val=val.nodesToUnregisterSize, is_pointer=False)
            self._nodes_to_unregister = UaNodeId(val=val.nodesToUnregister, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UnregisterNodesRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._nodes_to_unregister_size._value[0] = _val(val.nodesToUnregisterSize)
            self._nodes_to_unregister._value = val.nodesToUnregister

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def nodes_to_unregister_size(self):
        if self._null:
            return None
        else:
            return self._nodes_to_unregister_size

    @property
    def nodes_to_unregister(self):
        if self._null:
            return None
        else:
            return self._nodes_to_unregister

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @nodes_to_unregister_size.setter
    def nodes_to_unregister_size(self, val: SizeT):
        self._nodes_to_unregister_size = val
        self._value.nodesToUnregisterSize = val._val

    @nodes_to_unregister.setter
    def nodes_to_unregister(self, val: UaNodeId):
        self._nodes_to_unregister = val
        self._value.nodesToUnregister = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaUnregisterNodesRequest): NULL" + ("" if n is None else "\n")

        return ("(UaUnregisterNodesRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_unregister_size " + self._nodes_to_unregister_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_unregister " + self._nodes_to_unregister.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaOpenSecureChannelResponse +++++++++++++++++++++++
class UaOpenSecureChannelResponse(UaType):
    _UA_TYPE = _UA_TYPES._OPENSECURECHANNELRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_OpenSecureChannelResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_OpenSecureChannelResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._server_protocol_version = UaUInt32(val=val.serverProtocolVersion, is_pointer=False)
            self._security_token = UaChannelSecurityToken(val=val.securityToken, is_pointer=False)
            self._server_nonce = UaByteString(val=val.serverNonce, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_OpenSecureChannelResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._server_protocol_version._value[0] = _val(val.serverProtocolVersion)
            self._security_token._value[0] = _val(val.securityToken)
            self._server_nonce._value[0] = _val(val.serverNonce)

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def server_protocol_version(self):
        if self._null:
            return None
        else:
            return self._server_protocol_version

    @property
    def security_token(self):
        if self._null:
            return None
        else:
            return self._security_token

    @property
    def server_nonce(self):
        if self._null:
            return None
        else:
            return self._server_nonce

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @server_protocol_version.setter
    def server_protocol_version(self, val: UaUInt32):
        self._server_protocol_version = val
        self._value.serverProtocolVersion = val._val

    @security_token.setter
    def security_token(self, val: UaChannelSecurityToken):
        self._security_token = val
        self._value.securityToken = val._val

    @server_nonce.setter
    def server_nonce(self, val: UaByteString):
        self._server_nonce = val
        self._value.serverNonce = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaOpenSecureChannelResponse): NULL" + ("" if n is None else "\n")

        return ("(UaOpenSecureChannelResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_protocol_version " + self._server_protocol_version.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_token " + self._security_token.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_nonce " + self._server_nonce.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSetTriggeringResponse +++++++++++++++++++++++
class UaSetTriggeringResponse(UaType):
    _UA_TYPE = _UA_TYPES._SETTRIGGERINGRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SetTriggeringResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SetTriggeringResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._add_results_size = SizeT(val=val.addResultsSize, is_pointer=False)
            self._add_results = UaStatusCode(val=val.addResults, is_pointer=True)
            self._add_diagnostic_infos_size = SizeT(val=val.addDiagnosticInfosSize, is_pointer=False)
            self._add_diagnostic_infos = UaDiagnosticInfo(val=val.addDiagnosticInfos, is_pointer=True)
            self._remove_results_size = SizeT(val=val.removeResultsSize, is_pointer=False)
            self._remove_results = UaStatusCode(val=val.removeResults, is_pointer=True)
            self._remove_diagnostic_infos_size = SizeT(val=val.removeDiagnosticInfosSize, is_pointer=False)
            self._remove_diagnostic_infos = UaDiagnosticInfo(val=val.removeDiagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SetTriggeringResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._add_results_size._value[0] = _val(val.addResultsSize)
            self._add_results._value = val.addResults
            self._add_diagnostic_infos_size._value[0] = _val(val.addDiagnosticInfosSize)
            self._add_diagnostic_infos._value = val.addDiagnosticInfos
            self._remove_results_size._value[0] = _val(val.removeResultsSize)
            self._remove_results._value = val.removeResults
            self._remove_diagnostic_infos_size._value[0] = _val(val.removeDiagnosticInfosSize)
            self._remove_diagnostic_infos._value = val.removeDiagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def add_results_size(self):
        if self._null:
            return None
        else:
            return self._add_results_size

    @property
    def add_results(self):
        if self._null:
            return None
        else:
            return self._add_results

    @property
    def add_diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._add_diagnostic_infos_size

    @property
    def add_diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._add_diagnostic_infos

    @property
    def remove_results_size(self):
        if self._null:
            return None
        else:
            return self._remove_results_size

    @property
    def remove_results(self):
        if self._null:
            return None
        else:
            return self._remove_results

    @property
    def remove_diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._remove_diagnostic_infos_size

    @property
    def remove_diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._remove_diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @add_results_size.setter
    def add_results_size(self, val: SizeT):
        self._add_results_size = val
        self._value.addResultsSize = val._val

    @add_results.setter
    def add_results(self, val: UaStatusCode):
        self._add_results = val
        self._value.addResults = val._ptr

    @add_diagnostic_infos_size.setter
    def add_diagnostic_infos_size(self, val: SizeT):
        self._add_diagnostic_infos_size = val
        self._value.addDiagnosticInfosSize = val._val

    @add_diagnostic_infos.setter
    def add_diagnostic_infos(self, val: UaDiagnosticInfo):
        self._add_diagnostic_infos = val
        self._value.addDiagnosticInfos = val._ptr

    @remove_results_size.setter
    def remove_results_size(self, val: SizeT):
        self._remove_results_size = val
        self._value.removeResultsSize = val._val

    @remove_results.setter
    def remove_results(self, val: UaStatusCode):
        self._remove_results = val
        self._value.removeResults = val._ptr

    @remove_diagnostic_infos_size.setter
    def remove_diagnostic_infos_size(self, val: SizeT):
        self._remove_diagnostic_infos_size = val
        self._value.removeDiagnosticInfosSize = val._val

    @remove_diagnostic_infos.setter
    def remove_diagnostic_infos(self, val: UaDiagnosticInfo):
        self._remove_diagnostic_infos = val
        self._value.removeDiagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaSetTriggeringResponse): NULL" + ("" if n is None else "\n")

        return ("(UaSetTriggeringResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "add_results_size " + self._add_results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "add_results " + self._add_results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "add_diagnostic_infos_size " + self._add_diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "add_diagnostic_infos " + self._add_diagnostic_infos.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "remove_results_size " + self._remove_results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "remove_results " + self._remove_results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "remove_diagnostic_infos_size " + self._remove_diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "remove_diagnostic_infos " + self._remove_diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSimpleAttributeOperand +++++++++++++++++++++++
class UaSimpleAttributeOperand(UaType):
    _UA_TYPE = _UA_TYPES._SIMPLEATTRIBUTEOPERAND

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SimpleAttributeOperand*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SimpleAttributeOperand*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._type_definition_id = UaNodeId(val=val.typeDefinitionId, is_pointer=False)
            self._browse_path_size = SizeT(val=val.browsePathSize, is_pointer=False)
            self._browse_path = UaQualifiedName(val=val.browsePath, is_pointer=True)
            self._attribute_id = UaUInt32(val=val.attributeId, is_pointer=False)
            self._index_range = UaString(val=val.indexRange, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SimpleAttributeOperand")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._type_definition_id._value[0] = _val(val.typeDefinitionId)
            self._browse_path_size._value[0] = _val(val.browsePathSize)
            self._browse_path._value = val.browsePath
            self._attribute_id._value[0] = _val(val.attributeId)
            self._index_range._value[0] = _val(val.indexRange)

    @property
    def type_definition_id(self):
        if self._null:
            return None
        else:
            return self._type_definition_id

    @property
    def browse_path_size(self):
        if self._null:
            return None
        else:
            return self._browse_path_size

    @property
    def browse_path(self):
        if self._null:
            return None
        else:
            return self._browse_path

    @property
    def attribute_id(self):
        if self._null:
            return None
        else:
            return self._attribute_id

    @property
    def index_range(self):
        if self._null:
            return None
        else:
            return self._index_range

    @type_definition_id.setter
    def type_definition_id(self, val: UaNodeId):
        self._type_definition_id = val
        self._value.typeDefinitionId = val._val

    @browse_path_size.setter
    def browse_path_size(self, val: SizeT):
        self._browse_path_size = val
        self._value.browsePathSize = val._val

    @browse_path.setter
    def browse_path(self, val: UaQualifiedName):
        self._browse_path = val
        self._value.browsePath = val._ptr

    @attribute_id.setter
    def attribute_id(self, val: UaUInt32):
        self._attribute_id = val
        self._value.attributeId = val._val

    @index_range.setter
    def index_range(self, val: UaString):
        self._index_range = val
        self._value.indexRange = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaSimpleAttributeOperand): NULL" + ("" if n is None else "\n")

        return ("(UaSimpleAttributeOperand) :\n"
                + "\t" * (1 if n is None else n+1) + "type_definition_id " + self._type_definition_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "browse_path_size " + self._browse_path_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "browse_path " + self._browse_path.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "attribute_id " + self._attribute_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "index_range " + self._index_range.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaRepublishRequest +++++++++++++++++++++++
class UaRepublishRequest(UaType):
    _UA_TYPE = _UA_TYPES._REPUBLISHREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_RepublishRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_RepublishRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
            self._retransmit_sequence_number = UaUInt32(val=val.retransmitSequenceNumber, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_RepublishRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._retransmit_sequence_number._value[0] = _val(val.retransmitSequenceNumber)

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def retransmit_sequence_number(self):
        if self._null:
            return None
        else:
            return self._retransmit_sequence_number

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @retransmit_sequence_number.setter
    def retransmit_sequence_number(self, val: UaUInt32):
        self._retransmit_sequence_number = val
        self._value.retransmitSequenceNumber = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaRepublishRequest): NULL" + ("" if n is None else "\n")

        return ("(UaRepublishRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "retransmit_sequence_number " + self._retransmit_sequence_number.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaRegisterNodesResponse +++++++++++++++++++++++
class UaRegisterNodesResponse(UaType):
    _UA_TYPE = _UA_TYPES._REGISTERNODESRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_RegisterNodesResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_RegisterNodesResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._registered_node_ids_size = SizeT(val=val.registeredNodeIdsSize, is_pointer=False)
            self._registered_node_ids = UaNodeId(val=val.registeredNodeIds, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_RegisterNodesResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._registered_node_ids_size._value[0] = _val(val.registeredNodeIdsSize)
            self._registered_node_ids._value = val.registeredNodeIds

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def registered_node_ids_size(self):
        if self._null:
            return None
        else:
            return self._registered_node_ids_size

    @property
    def registered_node_ids(self):
        if self._null:
            return None
        else:
            return self._registered_node_ids

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @registered_node_ids_size.setter
    def registered_node_ids_size(self, val: SizeT):
        self._registered_node_ids_size = val
        self._value.registeredNodeIdsSize = val._val

    @registered_node_ids.setter
    def registered_node_ids(self, val: UaNodeId):
        self._registered_node_ids = val
        self._value.registeredNodeIds = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaRegisterNodesResponse): NULL" + ("" if n is None else "\n")

        return ("(UaRegisterNodesResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "registered_node_ids_size " + self._registered_node_ids_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "registered_node_ids " + self._registered_node_ids.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaModifyMonitoredItemsResponse +++++++++++++++++++++++
class UaModifyMonitoredItemsResponse(UaType):
    _UA_TYPE = _UA_TYPES._MODIFYMONITOREDITEMSRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ModifyMonitoredItemsResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ModifyMonitoredItemsResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaMonitoredItemModifyResult(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ModifyMonitoredItemsResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaMonitoredItemModifyResult):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaModifyMonitoredItemsResponse): NULL" + ("" if n is None else "\n")

        return ("(UaModifyMonitoredItemsResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteSubscriptionsRequest +++++++++++++++++++++++
class UaDeleteSubscriptionsRequest(UaType):
    _UA_TYPE = _UA_TYPES._DELETESUBSCRIPTIONSREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteSubscriptionsRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteSubscriptionsRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_ids_size = SizeT(val=val.subscriptionIdsSize, is_pointer=False)
            self._subscription_ids = UaUInt32(val=val.subscriptionIds, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteSubscriptionsRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_ids_size._value[0] = _val(val.subscriptionIdsSize)
            self._subscription_ids._value = val.subscriptionIds

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_ids_size(self):
        if self._null:
            return None
        else:
            return self._subscription_ids_size

    @property
    def subscription_ids(self):
        if self._null:
            return None
        else:
            return self._subscription_ids

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_ids_size.setter
    def subscription_ids_size(self, val: SizeT):
        self._subscription_ids_size = val
        self._value.subscriptionIdsSize = val._val

    @subscription_ids.setter
    def subscription_ids(self, val: UaUInt32):
        self._subscription_ids = val
        self._value.subscriptionIds = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteSubscriptionsRequest): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteSubscriptionsRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_ids_size " + self._subscription_ids_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_ids " + self._subscription_ids.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBrowsePath +++++++++++++++++++++++
class UaBrowsePath(UaType):
    _UA_TYPE = _UA_TYPES._BROWSEPATH

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BrowsePath*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BrowsePath*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._starting_node = UaNodeId(val=val.startingNode, is_pointer=False)
            self._relative_path = UaRelativePath(val=val.relativePath, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BrowsePath")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._starting_node._value[0] = _val(val.startingNode)
            self._relative_path._value[0] = _val(val.relativePath)

    @property
    def starting_node(self):
        if self._null:
            return None
        else:
            return self._starting_node

    @property
    def relative_path(self):
        if self._null:
            return None
        else:
            return self._relative_path

    @starting_node.setter
    def starting_node(self, val: UaNodeId):
        self._starting_node = val
        self._value.startingNode = val._val

    @relative_path.setter
    def relative_path(self, val: UaRelativePath):
        self._relative_path = val
        self._value.relativePath = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaBrowsePath): NULL" + ("" if n is None else "\n")

        return ("(UaBrowsePath) :\n"
                + "\t" * (1 if n is None else n+1) + "starting_node " + self._starting_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "relative_path " + self._relative_path.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaObjectAttributes +++++++++++++++++++++++
class UaObjectAttributes(UaType):
    _UA_TYPE = _UA_TYPES._OBJECTATTRIBUTES

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ObjectAttributes*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ObjectAttributes*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._specified_attributes = UaUInt32(val=val.specifiedAttributes, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._user_write_mask = UaUInt32(val=val.userWriteMask, is_pointer=False)
            self._event_notifier = UaByte(val=val.eventNotifier, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ObjectAttributes")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._specified_attributes._value[0] = _val(val.specifiedAttributes)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._user_write_mask._value[0] = _val(val.userWriteMask)
            self._event_notifier._value[0] = _val(val.eventNotifier)

    @property
    def specified_attributes(self):
        if self._null:
            return None
        else:
            return self._specified_attributes

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def user_write_mask(self):
        if self._null:
            return None
        else:
            return self._user_write_mask

    @property
    def event_notifier(self):
        if self._null:
            return None
        else:
            return self._event_notifier

    @specified_attributes.setter
    def specified_attributes(self, val: UaUInt32):
        self._specified_attributes = val
        self._value.specifiedAttributes = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @user_write_mask.setter
    def user_write_mask(self, val: UaUInt32):
        self._user_write_mask = val
        self._value.userWriteMask = val._val

    @event_notifier.setter
    def event_notifier(self, val: UaByte):
        self._event_notifier = val
        self._value.eventNotifier = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaObjectAttributes): NULL" + ("" if n is None else "\n")

        return ("(UaObjectAttributes) :\n"
                + "\t" * (1 if n is None else n+1) + "specified_attributes " + self._specified_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_write_mask " + self._user_write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "event_notifier " + self._event_notifier.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaPublishRequest +++++++++++++++++++++++
class UaPublishRequest(UaType):
    _UA_TYPE = _UA_TYPES._PUBLISHREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_PublishRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_PublishRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_acknowledgements_size = SizeT(val=val.subscriptionAcknowledgementsSize, is_pointer=False)
            self._subscription_acknowledgements = UaSubscriptionAcknowledgement(val=val.subscriptionAcknowledgements,
                                                                                is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_PublishRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_acknowledgements_size._value[0] = _val(val.subscriptionAcknowledgementsSize)
            self._subscription_acknowledgements._value = val.subscriptionAcknowledgements

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_acknowledgements_size(self):
        if self._null:
            return None
        else:
            return self._subscription_acknowledgements_size

    @property
    def subscription_acknowledgements(self):
        if self._null:
            return None
        else:
            return self._subscription_acknowledgements

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_acknowledgements_size.setter
    def subscription_acknowledgements_size(self, val: SizeT):
        self._subscription_acknowledgements_size = val
        self._value.subscriptionAcknowledgementsSize = val._val

    @subscription_acknowledgements.setter
    def subscription_acknowledgements(self, val: UaSubscriptionAcknowledgement):
        self._subscription_acknowledgements = val
        self._value.subscriptionAcknowledgements = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaPublishRequest): NULL" + ("" if n is None else "\n")

        return ("(UaPublishRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (
                            n + 1) + "subscription_acknowledgements_size " + self._subscription_acknowledgements_size.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "subscription_acknowledgements " + self._subscription_acknowledgements.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaFindServersRequest +++++++++++++++++++++++
class UaFindServersRequest(UaType):
    _UA_TYPE = _UA_TYPES._FINDSERVERSREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_FindServersRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_FindServersRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._endpoint_url = UaString(val=val.endpointUrl, is_pointer=False)
            self._locale_ids_size = SizeT(val=val.localeIdsSize, is_pointer=False)
            self._locale_ids = UaString(val=val.localeIds, is_pointer=True)
            self._server_uris_size = SizeT(val=val.serverUrisSize, is_pointer=False)
            self._server_uris = UaString(val=val.serverUris, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_FindServersRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._endpoint_url._value[0] = _val(val.endpointUrl)
            self._locale_ids_size._value[0] = _val(val.localeIdsSize)
            self._locale_ids._value = val.localeIds
            self._server_uris_size._value[0] = _val(val.serverUrisSize)
            self._server_uris._value = val.serverUris

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def endpoint_url(self):
        if self._null:
            return None
        else:
            return self._endpoint_url

    @property
    def locale_ids_size(self):
        if self._null:
            return None
        else:
            return self._locale_ids_size

    @property
    def locale_ids(self):
        if self._null:
            return None
        else:
            return self._locale_ids

    @property
    def server_uris_size(self):
        if self._null:
            return None
        else:
            return self._server_uris_size

    @property
    def server_uris(self):
        if self._null:
            return None
        else:
            return self._server_uris

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @endpoint_url.setter
    def endpoint_url(self, val: UaString):
        self._endpoint_url = val
        self._value.endpointUrl = val._val

    @locale_ids_size.setter
    def locale_ids_size(self, val: SizeT):
        self._locale_ids_size = val
        self._value.localeIdsSize = val._val

    @locale_ids.setter
    def locale_ids(self, val: UaString):
        self._locale_ids = val
        self._value.localeIds = val._ptr

    @server_uris_size.setter
    def server_uris_size(self, val: SizeT):
        self._server_uris_size = val
        self._value.serverUrisSize = val._val

    @server_uris.setter
    def server_uris(self, val: UaString):
        self._server_uris = val
        self._value.serverUris = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaFindServersRequest): NULL" + ("" if n is None else "\n")

        return ("(UaFindServersRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "endpoint_url " + self._endpoint_url.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "locale_ids_size " + self._locale_ids_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "locale_ids " + self._locale_ids.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_uris_size " + self._server_uris_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_uris " + self._server_uris.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaReferenceDescription +++++++++++++++++++++++
class UaReferenceDescription(UaType):
    _UA_TYPE = _UA_TYPES._REFERENCEDESCRIPTION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ReferenceDescription*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ReferenceDescription*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
            self._is_forward = UaBoolean(val=val.isForward, is_pointer=False)
            self._node_id = UaExpandedNodeId(val=val.nodeId, is_pointer=False)
            self._browse_name = UaQualifiedName(val=val.browseName, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._node_class = UaNodeClass(val=val.nodeClass, is_pointer=False)
            self._type_definition = UaExpandedNodeId(val=val.typeDefinition, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ReferenceDescription")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._reference_type_id._value[0] = _val(val.referenceTypeId)
            self._is_forward._value[0] = _val(val.isForward)
            self._node_id._value[0] = _val(val.nodeId)
            self._browse_name._value[0] = _val(val.browseName)
            self._display_name._value[0] = _val(val.displayName)
            self._node_class._value[0] = _val(val.nodeClass)
            self._type_definition._value[0] = _val(val.typeDefinition)

    @property
    def reference_type_id(self):
        if self._null:
            return None
        else:
            return self._reference_type_id

    @property
    def is_forward(self):
        if self._null:
            return None
        else:
            return self._is_forward

    @property
    def node_id(self):
        if self._null:
            return None
        else:
            return self._node_id

    @property
    def browse_name(self):
        if self._null:
            return None
        else:
            return self._browse_name

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def node_class(self):
        if self._null:
            return None
        else:
            return self._node_class

    @property
    def type_definition(self):
        if self._null:
            return None
        else:
            return self._type_definition

    @reference_type_id.setter
    def reference_type_id(self, val: UaNodeId):
        self._reference_type_id = val
        self._value.referenceTypeId = val._val

    @is_forward.setter
    def is_forward(self, val: UaBoolean):
        self._is_forward = val
        self._value.isForward = val._val

    @node_id.setter
    def node_id(self, val: UaExpandedNodeId):
        self._node_id = val
        self._value.nodeId = val._val

    @browse_name.setter
    def browse_name(self, val: UaQualifiedName):
        self._browse_name = val
        self._value.browseName = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @node_class.setter
    def node_class(self, val: UaNodeClass):
        self._node_class = val
        self._value.nodeClass = val._val

    @type_definition.setter
    def type_definition(self, val: UaExpandedNodeId):
        self._type_definition = val
        self._value.typeDefinition = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaReferenceDescription): NULL" + ("" if n is None else "\n")

        return ("(UaReferenceDescription) :\n"
                + "\t" * (1 if n is None else n+1) + "reference_type_id " + self._reference_type_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_forward " + self._is_forward.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "node_id " + self._node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "browse_name " + self._browse_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "node_class " + self._node_class.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "type_definition " + self._type_definition.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCreateSubscriptionRequest +++++++++++++++++++++++
class UaCreateSubscriptionRequest(UaType):
    _UA_TYPE = _UA_TYPES._CREATESUBSCRIPTIONREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CreateSubscriptionRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CreateSubscriptionRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._requested_publishing_interval = UaDouble(val=val.requestedPublishingInterval, is_pointer=False)
            self._requested_lifetime_count = UaUInt32(val=val.requestedLifetimeCount, is_pointer=False)
            self._requested_max_keep_alive_count = UaUInt32(val=val.requestedMaxKeepAliveCount, is_pointer=False)
            self._max_notifications_per_publish = UaUInt32(val=val.maxNotificationsPerPublish, is_pointer=False)
            self._publishing_enabled = UaBoolean(val=val.publishingEnabled, is_pointer=False)
            self._priority = UaByte(val=val.priority, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CreateSubscriptionRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._requested_publishing_interval._value[0] = _val(val.requestedPublishingInterval)
            self._requested_lifetime_count._value[0] = _val(val.requestedLifetimeCount)
            self._requested_max_keep_alive_count._value[0] = _val(val.requestedMaxKeepAliveCount)
            self._max_notifications_per_publish._value[0] = _val(val.maxNotificationsPerPublish)
            self._publishing_enabled._value[0] = _val(val.publishingEnabled)
            self._priority._value[0] = _val(val.priority)

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def requested_publishing_interval(self):
        if self._null:
            return None
        else:
            return self._requested_publishing_interval

    @property
    def requested_lifetime_count(self):
        if self._null:
            return None
        else:
            return self._requested_lifetime_count

    @property
    def requested_max_keep_alive_count(self):
        if self._null:
            return None
        else:
            return self._requested_max_keep_alive_count

    @property
    def max_notifications_per_publish(self):
        if self._null:
            return None
        else:
            return self._max_notifications_per_publish

    @property
    def publishing_enabled(self):
        if self._null:
            return None
        else:
            return self._publishing_enabled

    @property
    def priority(self):
        if self._null:
            return None
        else:
            return self._priority

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @requested_publishing_interval.setter
    def requested_publishing_interval(self, val: UaDouble):
        self._requested_publishing_interval = val
        self._value.requestedPublishingInterval = val._val

    @requested_lifetime_count.setter
    def requested_lifetime_count(self, val: UaUInt32):
        self._requested_lifetime_count = val
        self._value.requestedLifetimeCount = val._val

    @requested_max_keep_alive_count.setter
    def requested_max_keep_alive_count(self, val: UaUInt32):
        self._requested_max_keep_alive_count = val
        self._value.requestedMaxKeepAliveCount = val._val

    @max_notifications_per_publish.setter
    def max_notifications_per_publish(self, val: UaUInt32):
        self._max_notifications_per_publish = val
        self._value.maxNotificationsPerPublish = val._val

    @publishing_enabled.setter
    def publishing_enabled(self, val: UaBoolean):
        self._publishing_enabled = val
        self._value.publishingEnabled = val._val

    @priority.setter
    def priority(self, val: UaByte):
        self._priority = val
        self._value.priority = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaCreateSubscriptionRequest): NULL" + ("" if n is None else "\n")

        return ("(UaCreateSubscriptionRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_publishing_interval " + self._requested_publishing_interval.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_lifetime_count " + self._requested_lifetime_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_max_keep_alive_count " + self._requested_max_keep_alive_count.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "max_notifications_per_publish " + self._max_notifications_per_publish.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "publishing_enabled " + self._publishing_enabled.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "priority " + self._priority.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCallResponse +++++++++++++++++++++++
class UaCallResponse(UaType):
    _UA_TYPE = _UA_TYPES._CALLRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CallResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CallResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaCallMethodResult(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CallResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaCallMethodResult):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaCallResponse): NULL" + ("" if n is None else "\n")

        return ("(UaCallResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteNodesResponse +++++++++++++++++++++++
class UaDeleteNodesResponse(UaType):
    _UA_TYPE = _UA_TYPES._DELETENODESRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteNodesResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteNodesResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaStatusCode(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteNodesResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteNodesResponse): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteNodesResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaModifyMonitoredItemsRequest +++++++++++++++++++++++
class UaModifyMonitoredItemsRequest(UaType):
    _UA_TYPE = _UA_TYPES._MODIFYMONITOREDITEMSREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ModifyMonitoredItemsRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ModifyMonitoredItemsRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
            self._timestamps_to_return = UaTimestampsToReturn(val=val.timestampsToReturn, is_pointer=False)
            self._items_to_modify_size = SizeT(val=val.itemsToModifySize, is_pointer=False)
            self._items_to_modify = UaMonitoredItemModifyRequest(val=val.itemsToModify, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ModifyMonitoredItemsRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._timestamps_to_return._value[0] = _val(val.timestampsToReturn)
            self._items_to_modify_size._value[0] = _val(val.itemsToModifySize)
            self._items_to_modify._value = val.itemsToModify

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def timestamps_to_return(self):
        if self._null:
            return None
        else:
            return self._timestamps_to_return

    @property
    def items_to_modify_size(self):
        if self._null:
            return None
        else:
            return self._items_to_modify_size

    @property
    def items_to_modify(self):
        if self._null:
            return None
        else:
            return self._items_to_modify

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @timestamps_to_return.setter
    def timestamps_to_return(self, val: UaTimestampsToReturn):
        self._timestamps_to_return = val
        self._value.timestampsToReturn = val._val

    @items_to_modify_size.setter
    def items_to_modify_size(self, val: SizeT):
        self._items_to_modify_size = val
        self._value.itemsToModifySize = val._val

    @items_to_modify.setter
    def items_to_modify(self, val: UaMonitoredItemModifyRequest):
        self._items_to_modify = val
        self._value.itemsToModify = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaModifyMonitoredItemsRequest): NULL" + ("" if n is None else "\n")

        return ("(UaModifyMonitoredItemsRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "timestamps_to_return " + self._timestamps_to_return.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "items_to_modify_size " + self._items_to_modify_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "items_to_modify " + self._items_to_modify.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaServiceFault +++++++++++++++++++++++
class UaServiceFault(UaType):
    _UA_TYPE = _UA_TYPES._SERVICEFAULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ServiceFault*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ServiceFault*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ServiceFault")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaServiceFault): NULL" + ("" if n is None else "\n")

        return ("(UaServiceFault) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaPublishResponse +++++++++++++++++++++++
class UaPublishResponse(UaType):
    _UA_TYPE = _UA_TYPES._PUBLISHRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_PublishResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_PublishResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
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

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_PublishResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._available_sequence_numbers_size._value[0] = _val(val.availableSequenceNumbersSize)
            self._available_sequence_numbers._value = val.availableSequenceNumbers
            self._more_notifications._value[0] = _val(val.moreNotifications)
            self._notification_message._value[0] = _val(val.notificationMessage)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def available_sequence_numbers_size(self):
        if self._null:
            return None
        else:
            return self._available_sequence_numbers_size

    @property
    def available_sequence_numbers(self):
        if self._null:
            return None
        else:
            return self._available_sequence_numbers

    @property
    def more_notifications(self):
        if self._null:
            return None
        else:
            return self._more_notifications

    @property
    def notification_message(self):
        if self._null:
            return None
        else:
            return self._notification_message

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @available_sequence_numbers_size.setter
    def available_sequence_numbers_size(self, val: SizeT):
        self._available_sequence_numbers_size = val
        self._value.availableSequenceNumbersSize = val._val

    @available_sequence_numbers.setter
    def available_sequence_numbers(self, val: UaUInt32):
        self._available_sequence_numbers = val
        self._value.availableSequenceNumbers = val._ptr

    @more_notifications.setter
    def more_notifications(self, val: UaBoolean):
        self._more_notifications = val
        self._value.moreNotifications = val._val

    @notification_message.setter
    def notification_message(self, val: UaNotificationMessage):
        self._notification_message = val
        self._value.notificationMessage = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaStatusCode):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaPublishResponse): NULL" + ("" if n is None else "\n")

        return ("(UaPublishResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "available_sequence_numbers_size " + self._available_sequence_numbers_size.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "available_sequence_numbers " + self._available_sequence_numbers.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "more_notifications " + self._more_notifications.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "notification_message " + self._notification_message.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCreateMonitoredItemsRequest +++++++++++++++++++++++
class UaCreateMonitoredItemsRequest(UaType):
    _UA_TYPE = _UA_TYPES._CREATEMONITOREDITEMSREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CreateMonitoredItemsRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CreateMonitoredItemsRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
            self._timestamps_to_return = UaTimestampsToReturn(val=val.timestampsToReturn, is_pointer=False)
            self._items_to_create_size = SizeT(val=val.itemsToCreateSize, is_pointer=False)
            self._items_to_create = UaMonitoredItemCreateRequest(val=val.itemsToCreate, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CreateMonitoredItemsRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._timestamps_to_return._value[0] = _val(val.timestampsToReturn)
            self._items_to_create_size._value[0] = _val(val.itemsToCreateSize)
            self._items_to_create._value = val.itemsToCreate

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def timestamps_to_return(self):
        if self._null:
            return None
        else:
            return self._timestamps_to_return

    @property
    def items_to_create_size(self):
        if self._null:
            return None
        else:
            return self._items_to_create_size

    @property
    def items_to_create(self):
        if self._null:
            return None
        else:
            return self._items_to_create

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @timestamps_to_return.setter
    def timestamps_to_return(self, val: UaTimestampsToReturn):
        self._timestamps_to_return = val
        self._value.timestampsToReturn = val._val

    @items_to_create_size.setter
    def items_to_create_size(self, val: SizeT):
        self._items_to_create_size = val
        self._value.itemsToCreateSize = val._val

    @items_to_create.setter
    def items_to_create(self, val: UaMonitoredItemCreateRequest):
        self._items_to_create = val
        self._value.itemsToCreate = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaCreateMonitoredItemsRequest): NULL" + ("" if n is None else "\n")

        return ("(UaCreateMonitoredItemsRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "timestamps_to_return " + self._timestamps_to_return.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "items_to_create_size " + self._items_to_create_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "items_to_create " + self._items_to_create.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaOpenSecureChannelRequest +++++++++++++++++++++++
class UaOpenSecureChannelRequest(UaType):
    _UA_TYPE = _UA_TYPES._OPENSECURECHANNELREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_OpenSecureChannelRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_OpenSecureChannelRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._client_protocol_version = UaUInt32(val=val.clientProtocolVersion, is_pointer=False)
            self._request_type = UaSecurityTokenRequestType(val=val.requestType, is_pointer=False)
            self._security_mode = UaMessageSecurityMode(val=val.securityMode, is_pointer=False)
            self._client_nonce = UaByteString(val=val.clientNonce, is_pointer=False)
            self._requested_lifetime = UaUInt32(val=val.requestedLifetime, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_OpenSecureChannelRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._client_protocol_version._value[0] = _val(val.clientProtocolVersion)
            self._request_type._value[0] = _val(val.requestType)
            self._security_mode._value[0] = _val(val.securityMode)
            self._client_nonce._value[0] = _val(val.clientNonce)
            self._requested_lifetime._value[0] = _val(val.requestedLifetime)

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def client_protocol_version(self):
        if self._null:
            return None
        else:
            return self._client_protocol_version

    @property
    def request_type(self):
        if self._null:
            return None
        else:
            return self._request_type

    @property
    def security_mode(self):
        if self._null:
            return None
        else:
            return self._security_mode

    @property
    def client_nonce(self):
        if self._null:
            return None
        else:
            return self._client_nonce

    @property
    def requested_lifetime(self):
        if self._null:
            return None
        else:
            return self._requested_lifetime

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @client_protocol_version.setter
    def client_protocol_version(self, val: UaUInt32):
        self._client_protocol_version = val
        self._value.clientProtocolVersion = val._val

    @request_type.setter
    def request_type(self, val: UaSecurityTokenRequestType):
        self._request_type = val
        self._value.requestType = val._val

    @security_mode.setter
    def security_mode(self, val: UaMessageSecurityMode):
        self._security_mode = val
        self._value.securityMode = val._val

    @client_nonce.setter
    def client_nonce(self, val: UaByteString):
        self._client_nonce = val
        self._value.clientNonce = val._val

    @requested_lifetime.setter
    def requested_lifetime(self, val: UaUInt32):
        self._requested_lifetime = val
        self._value.requestedLifetime = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaOpenSecureChannelRequest): NULL" + ("" if n is None else "\n")

        return ("(UaOpenSecureChannelRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "client_protocol_version " + self._client_protocol_version.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "request_type " + self._request_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_mode " + self._security_mode.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "client_nonce " + self._client_nonce.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_lifetime " + self._requested_lifetime.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCloseSessionRequest +++++++++++++++++++++++
class UaCloseSessionRequest(UaType):
    _UA_TYPE = _UA_TYPES._CLOSESESSIONREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CloseSessionRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CloseSessionRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._delete_subscriptions = UaBoolean(val=val.deleteSubscriptions, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CloseSessionRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._delete_subscriptions._value[0] = _val(val.deleteSubscriptions)

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def delete_subscriptions(self):
        if self._null:
            return None
        else:
            return self._delete_subscriptions

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @delete_subscriptions.setter
    def delete_subscriptions(self, val: UaBoolean):
        self._delete_subscriptions = val
        self._value.deleteSubscriptions = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaCloseSessionRequest): NULL" + ("" if n is None else "\n")

        return ("(UaCloseSessionRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "delete_subscriptions " + self._delete_subscriptions.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaSetTriggeringRequest +++++++++++++++++++++++
class UaSetTriggeringRequest(UaType):
    _UA_TYPE = _UA_TYPES._SETTRIGGERINGREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SetTriggeringRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SetTriggeringRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._subscription_id = UaUInt32(val=val.subscriptionId, is_pointer=False)
            self._triggering_item_id = UaUInt32(val=val.triggeringItemId, is_pointer=False)
            self._links_to_add_size = SizeT(val=val.linksToAddSize, is_pointer=False)
            self._links_to_add = UaUInt32(val=val.linksToAdd, is_pointer=True)
            self._links_to_remove_size = SizeT(val=val.linksToRemoveSize, is_pointer=False)
            self._links_to_remove = UaUInt32(val=val.linksToRemove, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SetTriggeringRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._subscription_id._value[0] = _val(val.subscriptionId)
            self._triggering_item_id._value[0] = _val(val.triggeringItemId)
            self._links_to_add_size._value[0] = _val(val.linksToAddSize)
            self._links_to_add._value = val.linksToAdd
            self._links_to_remove_size._value[0] = _val(val.linksToRemoveSize)
            self._links_to_remove._value = val.linksToRemove

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def subscription_id(self):
        if self._null:
            return None
        else:
            return self._subscription_id

    @property
    def triggering_item_id(self):
        if self._null:
            return None
        else:
            return self._triggering_item_id

    @property
    def links_to_add_size(self):
        if self._null:
            return None
        else:
            return self._links_to_add_size

    @property
    def links_to_add(self):
        if self._null:
            return None
        else:
            return self._links_to_add

    @property
    def links_to_remove_size(self):
        if self._null:
            return None
        else:
            return self._links_to_remove_size

    @property
    def links_to_remove(self):
        if self._null:
            return None
        else:
            return self._links_to_remove

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @subscription_id.setter
    def subscription_id(self, val: UaUInt32):
        self._subscription_id = val
        self._value.subscriptionId = val._val

    @triggering_item_id.setter
    def triggering_item_id(self, val: UaUInt32):
        self._triggering_item_id = val
        self._value.triggeringItemId = val._val

    @links_to_add_size.setter
    def links_to_add_size(self, val: SizeT):
        self._links_to_add_size = val
        self._value.linksToAddSize = val._val

    @links_to_add.setter
    def links_to_add(self, val: UaUInt32):
        self._links_to_add = val
        self._value.linksToAdd = val._ptr

    @links_to_remove_size.setter
    def links_to_remove_size(self, val: SizeT):
        self._links_to_remove_size = val
        self._value.linksToRemoveSize = val._val

    @links_to_remove.setter
    def links_to_remove(self, val: UaUInt32):
        self._links_to_remove = val
        self._value.linksToRemove = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaSetTriggeringRequest): NULL" + ("" if n is None else "\n")

        return ("(UaSetTriggeringRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "subscription_id " + self._subscription_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "triggering_item_id " + self._triggering_item_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "links_to_add_size " + self._links_to_add_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "links_to_add " + self._links_to_add.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "links_to_remove_size " + self._links_to_remove_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "links_to_remove " + self._links_to_remove.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBrowseResult +++++++++++++++++++++++
class UaBrowseResult(UaType):
    _UA_TYPE = _UA_TYPES._BROWSERESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BrowseResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BrowseResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
            self._continuation_point = UaByteString(val=val.continuationPoint, is_pointer=False)
            self._references_size = SizeT(val=val.referencesSize, is_pointer=False)
            self._references = UaReferenceDescription(val=val.references, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BrowseResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._status_code._value[0] = _val(val.statusCode)
            self._continuation_point._value[0] = _val(val.continuationPoint)
            self._references_size._value[0] = _val(val.referencesSize)
            self._references._value = val.references

    @property
    def status_code(self):
        if self._null:
            return None
        else:
            return self._status_code

    @property
    def continuation_point(self):
        if self._null:
            return None
        else:
            return self._continuation_point

    @property
    def references_size(self):
        if self._null:
            return None
        else:
            return self._references_size

    @property
    def references(self):
        if self._null:
            return None
        else:
            return self._references

    @status_code.setter
    def status_code(self, val: UaStatusCode):
        self._status_code = val
        self._value.statusCode = val._val

    @continuation_point.setter
    def continuation_point(self, val: UaByteString):
        self._continuation_point = val
        self._value.continuationPoint = val._val

    @references_size.setter
    def references_size(self, val: SizeT):
        self._references_size = val
        self._value.referencesSize = val._val

    @references.setter
    def references(self, val: UaReferenceDescription):
        self._references = val
        self._value.references = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaBrowseResult): NULL" + ("" if n is None else "\n")

        return ("(UaBrowseResult) :\n"
                + "\t" * (1 if n is None else n+1) + "status_code " + self._status_code.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "continuation_point " + self._continuation_point.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "references_size " + self._references_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "references " + self._references.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAddReferencesRequest +++++++++++++++++++++++
class UaAddReferencesRequest(UaType):
    _UA_TYPE = _UA_TYPES._ADDREFERENCESREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AddReferencesRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AddReferencesRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._references_to_add_size = SizeT(val=val.referencesToAddSize, is_pointer=False)
            self._references_to_add = UaAddReferencesItem(val=val.referencesToAdd, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AddReferencesRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._references_to_add_size._value[0] = _val(val.referencesToAddSize)
            self._references_to_add._value = val.referencesToAdd

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def references_to_add_size(self):
        if self._null:
            return None
        else:
            return self._references_to_add_size

    @property
    def references_to_add(self):
        if self._null:
            return None
        else:
            return self._references_to_add

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @references_to_add_size.setter
    def references_to_add_size(self, val: SizeT):
        self._references_to_add_size = val
        self._value.referencesToAddSize = val._val

    @references_to_add.setter
    def references_to_add(self, val: UaAddReferencesItem):
        self._references_to_add = val
        self._value.referencesToAdd = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaAddReferencesRequest): NULL" + ("" if n is None else "\n")

        return ("(UaAddReferencesRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "references_to_add_size " + self._references_to_add_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "references_to_add " + self._references_to_add.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAddNodesItem +++++++++++++++++++++++
class UaAddNodesItem(UaType):
    _UA_TYPE = _UA_TYPES._ADDNODESITEM

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AddNodesItem*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AddNodesItem*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._parent_node_id = UaExpandedNodeId(val=val.parentNodeId, is_pointer=False)
            self._reference_type_id = UaNodeId(val=val.referenceTypeId, is_pointer=False)
            self._requested_new_node_id = UaExpandedNodeId(val=val.requestedNewNodeId, is_pointer=False)
            self._browse_name = UaQualifiedName(val=val.browseName, is_pointer=False)
            self._node_class = UaNodeClass(val=val.nodeClass, is_pointer=False)
            self._node_attributes = UaExtensionObject(val=val.nodeAttributes, is_pointer=False)
            self._type_definition = UaExpandedNodeId(val=val.typeDefinition, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AddNodesItem")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._parent_node_id._value[0] = _val(val.parentNodeId)
            self._reference_type_id._value[0] = _val(val.referenceTypeId)
            self._requested_new_node_id._value[0] = _val(val.requestedNewNodeId)
            self._browse_name._value[0] = _val(val.browseName)
            self._node_class._value[0] = _val(val.nodeClass)
            self._node_attributes._value[0] = _val(val.nodeAttributes)
            self._type_definition._value[0] = _val(val.typeDefinition)

    @property
    def parent_node_id(self):
        if self._null:
            return None
        else:
            return self._parent_node_id

    @property
    def reference_type_id(self):
        if self._null:
            return None
        else:
            return self._reference_type_id

    @property
    def requested_new_node_id(self):
        if self._null:
            return None
        else:
            return self._requested_new_node_id

    @property
    def browse_name(self):
        if self._null:
            return None
        else:
            return self._browse_name

    @property
    def node_class(self):
        if self._null:
            return None
        else:
            return self._node_class

    @property
    def node_attributes(self):
        if self._null:
            return None
        else:
            return self._node_attributes

    @property
    def type_definition(self):
        if self._null:
            return None
        else:
            return self._type_definition

    @parent_node_id.setter
    def parent_node_id(self, val: UaExpandedNodeId):
        self._parent_node_id = val
        self._value.parentNodeId = val._val

    @reference_type_id.setter
    def reference_type_id(self, val: UaNodeId):
        self._reference_type_id = val
        self._value.referenceTypeId = val._val

    @requested_new_node_id.setter
    def requested_new_node_id(self, val: UaExpandedNodeId):
        self._requested_new_node_id = val
        self._value.requestedNewNodeId = val._val

    @browse_name.setter
    def browse_name(self, val: UaQualifiedName):
        self._browse_name = val
        self._value.browseName = val._val

    @node_class.setter
    def node_class(self, val: UaNodeClass):
        self._node_class = val
        self._value.nodeClass = val._val

    @node_attributes.setter
    def node_attributes(self, val: UaExtensionObject):
        self._node_attributes = val
        self._value.nodeAttributes = val._val

    @type_definition.setter
    def type_definition(self, val: UaExpandedNodeId):
        self._type_definition = val
        self._value.typeDefinition = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaAddNodesItem): NULL" + ("" if n is None else "\n")

        return ("(UaAddNodesItem) :\n"
                + "\t" * (1 if n is None else n+1) + "parent_node_id " + self._parent_node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "reference_type_id " + self._reference_type_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_new_node_id " + self._requested_new_node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "browse_name " + self._browse_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "node_class " + self._node_class.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "node_attributes " + self._node_attributes.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "type_definition " + self._type_definition.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaServerStatusDataType +++++++++++++++++++++++
class UaServerStatusDataType(UaType):
    _UA_TYPE = _UA_TYPES._SERVERSTATUSDATATYPE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ServerStatusDataType*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ServerStatusDataType*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._start_time = UaDateTime(val=val.startTime, is_pointer=False)
            self._current_time = UaDateTime(val=val.currentTime, is_pointer=False)
            self._state = UaServerState(val=val.state, is_pointer=False)
            self._build_info = UaBuildInfo(val=val.buildInfo, is_pointer=False)
            self._seconds_till_shutdown = UaUInt32(val=val.secondsTillShutdown, is_pointer=False)
            self._shutdown_reason = UaLocalizedText(val=val.shutdownReason, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ServerStatusDataType")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._start_time._value[0] = _val(val.startTime)
            self._current_time._value[0] = _val(val.currentTime)
            self._state._value[0] = _val(val.state)
            self._build_info._value[0] = _val(val.buildInfo)
            self._seconds_till_shutdown._value[0] = _val(val.secondsTillShutdown)
            self._shutdown_reason._value[0] = _val(val.shutdownReason)

    @property
    def start_time(self):
        if self._null:
            return None
        else:
            return self._start_time

    @property
    def current_time(self):
        if self._null:
            return None
        else:
            return self._current_time

    @property
    def state(self):
        if self._null:
            return None
        else:
            return self._state

    @property
    def build_info(self):
        if self._null:
            return None
        else:
            return self._build_info

    @property
    def seconds_till_shutdown(self):
        if self._null:
            return None
        else:
            return self._seconds_till_shutdown

    @property
    def shutdown_reason(self):
        if self._null:
            return None
        else:
            return self._shutdown_reason

    @start_time.setter
    def start_time(self, val: UaDateTime):
        self._start_time = val
        self._value.startTime = val._val

    @current_time.setter
    def current_time(self, val: UaDateTime):
        self._current_time = val
        self._value.currentTime = val._val

    @state.setter
    def state(self, val: UaServerState):
        self._state = val
        self._value.state = val._val

    @build_info.setter
    def build_info(self, val: UaBuildInfo):
        self._build_info = val
        self._value.buildInfo = val._val

    @seconds_till_shutdown.setter
    def seconds_till_shutdown(self, val: UaUInt32):
        self._seconds_till_shutdown = val
        self._value.secondsTillShutdown = val._val

    @shutdown_reason.setter
    def shutdown_reason(self, val: UaLocalizedText):
        self._shutdown_reason = val
        self._value.shutdownReason = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaServerStatusDataType): NULL" + ("" if n is None else "\n")

        return ("(UaServerStatusDataType) :\n"
                + "\t" * (1 if n is None else n+1) + "start_time " + self._start_time.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "current_time " + self._current_time.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "state " + self._state.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "build_info " + self._build_info.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "seconds_till_shutdown " + self._seconds_till_shutdown.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "shutdown_reason " + self._shutdown_reason.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBrowseNextResponse +++++++++++++++++++++++
class UaBrowseNextResponse(UaType):
    _UA_TYPE = _UA_TYPES._BROWSENEXTRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BrowseNextResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BrowseNextResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaBrowseResult(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BrowseNextResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaBrowseResult):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaBrowseNextResponse): NULL" + ("" if n is None else "\n")

        return ("(UaBrowseNextResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAxisInformation +++++++++++++++++++++++
class UaAxisInformation(UaType):
    _UA_TYPE = _UA_TYPES._AXISINFORMATION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AxisInformation*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AxisInformation*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._engineering_units = UaEUInformation(val=val.engineeringUnits, is_pointer=False)
            self._e_u_range = UaRange(val=val.eURange, is_pointer=False)
            self._title = UaLocalizedText(val=val.title, is_pointer=False)
            self._axis_scale_type = UaAxisScaleEnumeration(val=val.axisScaleType, is_pointer=False)
            self._axis_steps_size = SizeT(val=val.axisStepsSize, is_pointer=False)
            self._axis_steps = UaDouble(val=val.axisSteps, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AxisInformation")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._engineering_units._value[0] = _val(val.engineeringUnits)
            self._e_u_range._value[0] = _val(val.eURange)
            self._title._value[0] = _val(val.title)
            self._axis_scale_type._value[0] = _val(val.axisScaleType)
            self._axis_steps_size._value[0] = _val(val.axisStepsSize)
            self._axis_steps._value = val.axisSteps

    @property
    def engineering_units(self):
        if self._null:
            return None
        else:
            return self._engineering_units

    @property
    def e_u_range(self):
        if self._null:
            return None
        else:
            return self._e_u_range

    @property
    def title(self):
        if self._null:
            return None
        else:
            return self._title

    @property
    def axis_scale_type(self):
        if self._null:
            return None
        else:
            return self._axis_scale_type

    @property
    def axis_steps_size(self):
        if self._null:
            return None
        else:
            return self._axis_steps_size

    @property
    def axis_steps(self):
        if self._null:
            return None
        else:
            return self._axis_steps

    @engineering_units.setter
    def engineering_units(self, val: UaEUInformation):
        self._engineering_units = val
        self._value.engineeringUnits = val._val

    @e_u_range.setter
    def e_u_range(self, val: UaRange):
        self._e_u_range = val
        self._value.eURange = val._val

    @title.setter
    def title(self, val: UaLocalizedText):
        self._title = val
        self._value.title = val._val

    @axis_scale_type.setter
    def axis_scale_type(self, val: UaAxisScaleEnumeration):
        self._axis_scale_type = val
        self._value.axisScaleType = val._val

    @axis_steps_size.setter
    def axis_steps_size(self, val: SizeT):
        self._axis_steps_size = val
        self._value.axisStepsSize = val._val

    @axis_steps.setter
    def axis_steps(self, val: UaDouble):
        self._axis_steps = val
        self._value.axisSteps = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaAxisInformation): NULL" + ("" if n is None else "\n")

        return ("(UaAxisInformation) :\n"
                + "\t" * (1 if n is None else n+1) + "engineering_units " + self._engineering_units.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "e_u_range " + self._e_u_range.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "title " + self._title.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "axis_scale_type " + self._axis_scale_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "axis_steps_size " + self._axis_steps_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "axis_steps " + self._axis_steps.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaApplicationDescription +++++++++++++++++++++++
class UaApplicationDescription(UaType):
    _UA_TYPE = _UA_TYPES._APPLICATIONDESCRIPTION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ApplicationDescription*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ApplicationDescription*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._application_uri = UaString(val=val.applicationUri, is_pointer=False)
            self._product_uri = UaString(val=val.productUri, is_pointer=False)
            self._application_name = UaLocalizedText(val=val.applicationName, is_pointer=False)
            self._application_type = UaApplicationType(val=val.applicationType, is_pointer=False)
            self._gateway_server_uri = UaString(val=val.gatewayServerUri, is_pointer=False)
            self._discovery_profile_uri = UaString(val=val.discoveryProfileUri, is_pointer=False)
            self._discovery_urls_size = SizeT(val=val.discoveryUrlsSize, is_pointer=False)
            self._discovery_urls = UaString(val=val.discoveryUrls, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ApplicationDescription")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._application_uri._value[0] = _val(val.applicationUri)
            self._product_uri._value[0] = _val(val.productUri)
            self._application_name._value[0] = _val(val.applicationName)
            self._application_type._value[0] = _val(val.applicationType)
            self._gateway_server_uri._value[0] = _val(val.gatewayServerUri)
            self._discovery_profile_uri._value[0] = _val(val.discoveryProfileUri)
            self._discovery_urls_size._value[0] = _val(val.discoveryUrlsSize)
            self._discovery_urls._value = val.discoveryUrls

    @property
    def application_uri(self):
        if self._null:
            return None
        else:
            return self._application_uri

    @property
    def product_uri(self):
        if self._null:
            return None
        else:
            return self._product_uri

    @property
    def application_name(self):
        if self._null:
            return None
        else:
            return self._application_name

    @property
    def application_type(self):
        if self._null:
            return None
        else:
            return self._application_type

    @property
    def gateway_server_uri(self):
        if self._null:
            return None
        else:
            return self._gateway_server_uri

    @property
    def discovery_profile_uri(self):
        if self._null:
            return None
        else:
            return self._discovery_profile_uri

    @property
    def discovery_urls_size(self):
        if self._null:
            return None
        else:
            return self._discovery_urls_size

    @property
    def discovery_urls(self):
        if self._null:
            return None
        else:
            return self._discovery_urls

    @application_uri.setter
    def application_uri(self, val: UaString):
        self._application_uri = val
        self._value.applicationUri = val._val

    @product_uri.setter
    def product_uri(self, val: UaString):
        self._product_uri = val
        self._value.productUri = val._val

    @application_name.setter
    def application_name(self, val: UaLocalizedText):
        self._application_name = val
        self._value.applicationName = val._val

    @application_type.setter
    def application_type(self, val: UaApplicationType):
        self._application_type = val
        self._value.applicationType = val._val

    @gateway_server_uri.setter
    def gateway_server_uri(self, val: UaString):
        self._gateway_server_uri = val
        self._value.gatewayServerUri = val._val

    @discovery_profile_uri.setter
    def discovery_profile_uri(self, val: UaString):
        self._discovery_profile_uri = val
        self._value.discoveryProfileUri = val._val

    @discovery_urls_size.setter
    def discovery_urls_size(self, val: SizeT):
        self._discovery_urls_size = val
        self._value.discoveryUrlsSize = val._val

    @discovery_urls.setter
    def discovery_urls(self, val: UaString):
        self._discovery_urls = val
        self._value.discoveryUrls = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaApplicationDescription): NULL" + ("" if n is None else "\n")

        return ("(UaApplicationDescription) :\n"
                + "\t" * (1 if n is None else n+1) + "application_uri " + self._application_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "product_uri " + self._product_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "application_name " + self._application_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "application_type " + self._application_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "gateway_server_uri " + self._gateway_server_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "discovery_profile_uri " + self._discovery_profile_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "discovery_urls_size " + self._discovery_urls_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "discovery_urls " + self._discovery_urls.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaReadRequest +++++++++++++++++++++++
class UaReadRequest(UaType):
    _UA_TYPE = _UA_TYPES._READREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ReadRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ReadRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._max_age = UaDouble(val=val.maxAge, is_pointer=False)
            self._timestamps_to_return = UaTimestampsToReturn(val=val.timestampsToReturn, is_pointer=False)
            self._nodes_to_read_size = SizeT(val=val.nodesToReadSize, is_pointer=False)
            self._nodes_to_read = UaReadValueId(val=val.nodesToRead, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ReadRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._max_age._value[0] = _val(val.maxAge)
            self._timestamps_to_return._value[0] = _val(val.timestampsToReturn)
            self._nodes_to_read_size._value[0] = _val(val.nodesToReadSize)
            self._nodes_to_read._value = val.nodesToRead

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def max_age(self):
        if self._null:
            return None
        else:
            return self._max_age

    @property
    def timestamps_to_return(self):
        if self._null:
            return None
        else:
            return self._timestamps_to_return

    @property
    def nodes_to_read_size(self):
        if self._null:
            return None
        else:
            return self._nodes_to_read_size

    @property
    def nodes_to_read(self):
        if self._null:
            return None
        else:
            return self._nodes_to_read

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @max_age.setter
    def max_age(self, val: UaDouble):
        self._max_age = val
        self._value.maxAge = val._val

    @timestamps_to_return.setter
    def timestamps_to_return(self, val: UaTimestampsToReturn):
        self._timestamps_to_return = val
        self._value.timestampsToReturn = val._val

    @nodes_to_read_size.setter
    def nodes_to_read_size(self, val: SizeT):
        self._nodes_to_read_size = val
        self._value.nodesToReadSize = val._val

    @nodes_to_read.setter
    def nodes_to_read(self, val: UaReadValueId):
        self._nodes_to_read = val
        self._value.nodesToRead = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaReadRequest): NULL" + ("" if n is None else "\n")

        return ("(UaReadRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_age " + self._max_age.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "timestamps_to_return " + self._timestamps_to_return.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_read_size " + self._nodes_to_read_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_read " + self._nodes_to_read.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaActivateSessionRequest +++++++++++++++++++++++
class UaActivateSessionRequest(UaType):
    _UA_TYPE = _UA_TYPES._ACTIVATESESSIONREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ActivateSessionRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ActivateSessionRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._client_signature = UaSignatureData(val=val.clientSignature, is_pointer=False)
            self._client_software_certificates_size = SizeT(val=val.clientSoftwareCertificatesSize, is_pointer=False)
            self._client_software_certificates = UaSignedSoftwareCertificate(val=val.clientSoftwareCertificates,
                                                                             is_pointer=True)
            self._locale_ids_size = SizeT(val=val.localeIdsSize, is_pointer=False)
            self._locale_ids = UaString(val=val.localeIds, is_pointer=True)
            self._user_identity_token = UaExtensionObject(val=val.userIdentityToken, is_pointer=False)
            self._user_token_signature = UaSignatureData(val=val.userTokenSignature, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ActivateSessionRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._client_signature._value[0] = _val(val.clientSignature)
            self._client_software_certificates_size._value[0] = _val(val.clientSoftwareCertificatesSize)
            self._client_software_certificates._value = val.clientSoftwareCertificates
            self._locale_ids_size._value[0] = _val(val.localeIdsSize)
            self._locale_ids._value = val.localeIds
            self._user_identity_token._value[0] = _val(val.userIdentityToken)
            self._user_token_signature._value[0] = _val(val.userTokenSignature)

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def client_signature(self):
        if self._null:
            return None
        else:
            return self._client_signature

    @property
    def client_software_certificates_size(self):
        if self._null:
            return None
        else:
            return self._client_software_certificates_size

    @property
    def client_software_certificates(self):
        if self._null:
            return None
        else:
            return self._client_software_certificates

    @property
    def locale_ids_size(self):
        if self._null:
            return None
        else:
            return self._locale_ids_size

    @property
    def locale_ids(self):
        if self._null:
            return None
        else:
            return self._locale_ids

    @property
    def user_identity_token(self):
        if self._null:
            return None
        else:
            return self._user_identity_token

    @property
    def user_token_signature(self):
        if self._null:
            return None
        else:
            return self._user_token_signature

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @client_signature.setter
    def client_signature(self, val: UaSignatureData):
        self._client_signature = val
        self._value.clientSignature = val._val

    @client_software_certificates_size.setter
    def client_software_certificates_size(self, val: SizeT):
        self._client_software_certificates_size = val
        self._value.clientSoftwareCertificatesSize = val._val

    @client_software_certificates.setter
    def client_software_certificates(self, val: UaSignedSoftwareCertificate):
        self._client_software_certificates = val
        self._value.clientSoftwareCertificates = val._ptr

    @locale_ids_size.setter
    def locale_ids_size(self, val: SizeT):
        self._locale_ids_size = val
        self._value.localeIdsSize = val._val

    @locale_ids.setter
    def locale_ids(self, val: UaString):
        self._locale_ids = val
        self._value.localeIds = val._ptr

    @user_identity_token.setter
    def user_identity_token(self, val: UaExtensionObject):
        self._user_identity_token = val
        self._value.userIdentityToken = val._val

    @user_token_signature.setter
    def user_token_signature(self, val: UaSignatureData):
        self._user_token_signature = val
        self._value.userTokenSignature = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaActivateSessionRequest): NULL" + ("" if n is None else "\n")

        return ("(UaActivateSessionRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "client_signature " + self._client_signature.__str__(1 if n is None else n+1)
                + "\t" * (
                            n + 1) + "client_software_certificates_size " + self._client_software_certificates_size.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "client_software_certificates " + self._client_software_certificates.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "locale_ids_size " + self._locale_ids_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "locale_ids " + self._locale_ids.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_identity_token " + self._user_identity_token.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_token_signature " + self._user_token_signature.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBrowsePathResult +++++++++++++++++++++++
class UaBrowsePathResult(UaType):
    _UA_TYPE = _UA_TYPES._BROWSEPATHRESULT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BrowsePathResult*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BrowsePathResult*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._status_code = UaStatusCode(val=val.statusCode, is_pointer=False)
            self._targets_size = SizeT(val=val.targetsSize, is_pointer=False)
            self._targets = UaBrowsePathTarget(val=val.targets, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BrowsePathResult")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._status_code._value[0] = _val(val.statusCode)
            self._targets_size._value[0] = _val(val.targetsSize)
            self._targets._value = val.targets

    @property
    def status_code(self):
        if self._null:
            return None
        else:
            return self._status_code

    @property
    def targets_size(self):
        if self._null:
            return None
        else:
            return self._targets_size

    @property
    def targets(self):
        if self._null:
            return None
        else:
            return self._targets

    @status_code.setter
    def status_code(self, val: UaStatusCode):
        self._status_code = val
        self._value.statusCode = val._val

    @targets_size.setter
    def targets_size(self, val: SizeT):
        self._targets_size = val
        self._value.targetsSize = val._val

    @targets.setter
    def targets(self, val: UaBrowsePathTarget):
        self._targets = val
        self._value.targets = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaBrowsePathResult): NULL" + ("" if n is None else "\n")

        return ("(UaBrowsePathResult) :\n"
                + "\t" * (1 if n is None else n+1) + "status_code " + self._status_code.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "targets_size " + self._targets_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "targets " + self._targets.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAddNodesRequest +++++++++++++++++++++++
class UaAddNodesRequest(UaType):
    _UA_TYPE = _UA_TYPES._ADDNODESREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AddNodesRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AddNodesRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._nodes_to_add_size = SizeT(val=val.nodesToAddSize, is_pointer=False)
            self._nodes_to_add = UaAddNodesItem(val=val.nodesToAdd, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AddNodesRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._nodes_to_add_size._value[0] = _val(val.nodesToAddSize)
            self._nodes_to_add._value = val.nodesToAdd

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def nodes_to_add_size(self):
        if self._null:
            return None
        else:
            return self._nodes_to_add_size

    @property
    def nodes_to_add(self):
        if self._null:
            return None
        else:
            return self._nodes_to_add

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @nodes_to_add_size.setter
    def nodes_to_add_size(self, val: SizeT):
        self._nodes_to_add_size = val
        self._value.nodesToAddSize = val._val

    @nodes_to_add.setter
    def nodes_to_add(self, val: UaAddNodesItem):
        self._nodes_to_add = val
        self._value.nodesToAdd = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaAddNodesRequest): NULL" + ("" if n is None else "\n")

        return ("(UaAddNodesRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_add_size " + self._nodes_to_add_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_add " + self._nodes_to_add.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBrowseRequest +++++++++++++++++++++++
class UaBrowseRequest(UaType):
    _UA_TYPE = _UA_TYPES._BROWSEREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BrowseRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BrowseRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._view = UaViewDescription(val=val.view, is_pointer=False)
            self._requested_max_references_per_node = UaUInt32(val=val.requestedMaxReferencesPerNode, is_pointer=False)
            self._nodes_to_browse_size = SizeT(val=val.nodesToBrowseSize, is_pointer=False)
            self._nodes_to_browse = UaBrowseDescription(val=val.nodesToBrowse, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BrowseRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._view._value[0] = _val(val.view)
            self._requested_max_references_per_node._value[0] = _val(val.requestedMaxReferencesPerNode)
            self._nodes_to_browse_size._value[0] = _val(val.nodesToBrowseSize)
            self._nodes_to_browse._value = val.nodesToBrowse

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def view(self):
        if self._null:
            return None
        else:
            return self._view

    @property
    def requested_max_references_per_node(self):
        if self._null:
            return None
        else:
            return self._requested_max_references_per_node

    @property
    def nodes_to_browse_size(self):
        if self._null:
            return None
        else:
            return self._nodes_to_browse_size

    @property
    def nodes_to_browse(self):
        if self._null:
            return None
        else:
            return self._nodes_to_browse

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @view.setter
    def view(self, val: UaViewDescription):
        self._view = val
        self._value.view = val._val

    @requested_max_references_per_node.setter
    def requested_max_references_per_node(self, val: UaUInt32):
        self._requested_max_references_per_node = val
        self._value.requestedMaxReferencesPerNode = val._val

    @nodes_to_browse_size.setter
    def nodes_to_browse_size(self, val: SizeT):
        self._nodes_to_browse_size = val
        self._value.nodesToBrowseSize = val._val

    @nodes_to_browse.setter
    def nodes_to_browse(self, val: UaBrowseDescription):
        self._nodes_to_browse = val
        self._value.nodesToBrowse = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaBrowseRequest): NULL" + ("" if n is None else "\n")

        return ("(UaBrowseRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "view " + self._view.__str__(1 if n is None else n+1)
                + "\t" * (
                            n + 1) + "requested_max_references_per_node " + self._requested_max_references_per_node.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_browse_size " + self._nodes_to_browse_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_browse " + self._nodes_to_browse.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaWriteRequest +++++++++++++++++++++++
class UaWriteRequest(UaType):
    _UA_TYPE = _UA_TYPES._WRITEREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_WriteRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_WriteRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._nodes_to_write_size = SizeT(val=val.nodesToWriteSize, is_pointer=False)
            self._nodes_to_write = UaWriteValue(val=val.nodesToWrite, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_WriteRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._nodes_to_write_size._value[0] = _val(val.nodesToWriteSize)
            self._nodes_to_write._value = val.nodesToWrite

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def nodes_to_write_size(self):
        if self._null:
            return None
        else:
            return self._nodes_to_write_size

    @property
    def nodes_to_write(self):
        if self._null:
            return None
        else:
            return self._nodes_to_write

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @nodes_to_write_size.setter
    def nodes_to_write_size(self, val: SizeT):
        self._nodes_to_write_size = val
        self._value.nodesToWriteSize = val._val

    @nodes_to_write.setter
    def nodes_to_write(self, val: UaWriteValue):
        self._nodes_to_write = val
        self._value.nodesToWrite = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaWriteRequest): NULL" + ("" if n is None else "\n")

        return ("(UaWriteRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_write_size " + self._nodes_to_write_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodes_to_write " + self._nodes_to_write.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAddNodesResponse +++++++++++++++++++++++
class UaAddNodesResponse(UaType):
    _UA_TYPE = _UA_TYPES._ADDNODESRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AddNodesResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AddNodesResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaAddNodesResult(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AddNodesResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaAddNodesResult):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaAddNodesResponse): NULL" + ("" if n is None else "\n")

        return ("(UaAddNodesResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAttributeOperand +++++++++++++++++++++++
class UaAttributeOperand(UaType):
    _UA_TYPE = _UA_TYPES._ATTRIBUTEOPERAND

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AttributeOperand*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AttributeOperand*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
            self._alias = UaString(val=val.alias, is_pointer=False)
            self._browse_path = UaRelativePath(val=val.browsePath, is_pointer=False)
            self._attribute_id = UaUInt32(val=val.attributeId, is_pointer=False)
            self._index_range = UaString(val=val.indexRange, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AttributeOperand")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._node_id._value[0] = _val(val.nodeId)
            self._alias._value[0] = _val(val.alias)
            self._browse_path._value[0] = _val(val.browsePath)
            self._attribute_id._value[0] = _val(val.attributeId)
            self._index_range._value[0] = _val(val.indexRange)

    @property
    def node_id(self):
        if self._null:
            return None
        else:
            return self._node_id

    @property
    def alias(self):
        if self._null:
            return None
        else:
            return self._alias

    @property
    def browse_path(self):
        if self._null:
            return None
        else:
            return self._browse_path

    @property
    def attribute_id(self):
        if self._null:
            return None
        else:
            return self._attribute_id

    @property
    def index_range(self):
        if self._null:
            return None
        else:
            return self._index_range

    @node_id.setter
    def node_id(self, val: UaNodeId):
        self._node_id = val
        self._value.nodeId = val._val

    @alias.setter
    def alias(self, val: UaString):
        self._alias = val
        self._value.alias = val._val

    @browse_path.setter
    def browse_path(self, val: UaRelativePath):
        self._browse_path = val
        self._value.browsePath = val._val

    @attribute_id.setter
    def attribute_id(self, val: UaUInt32):
        self._attribute_id = val
        self._value.attributeId = val._val

    @index_range.setter
    def index_range(self, val: UaString):
        self._index_range = val
        self._value.indexRange = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaAttributeOperand): NULL" + ("" if n is None else "\n")

        return ("(UaAttributeOperand) :\n"
                + "\t" * (1 if n is None else n+1) + "node_id " + self._node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "alias " + self._alias.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "browse_path " + self._browse_path.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "attribute_id " + self._attribute_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "index_range " + self._index_range.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDataChangeFilter +++++++++++++++++++++++
class UaDataChangeFilter(UaType):
    _UA_TYPE = _UA_TYPES._DATACHANGEFILTER

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataChangeFilter*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DataChangeFilter*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._trigger = UaDataChangeTrigger(val=val.trigger, is_pointer=False)
            self._deadband_type = UaUInt32(val=val.deadbandType, is_pointer=False)
            self._deadband_value = UaDouble(val=val.deadbandValue, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataChangeFilter")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._trigger._value[0] = _val(val.trigger)
            self._deadband_type._value[0] = _val(val.deadbandType)
            self._deadband_value._value[0] = _val(val.deadbandValue)

    @property
    def trigger(self):
        if self._null:
            return None
        else:
            return self._trigger

    @property
    def deadband_type(self):
        if self._null:
            return None
        else:
            return self._deadband_type

    @property
    def deadband_value(self):
        if self._null:
            return None
        else:
            return self._deadband_value

    @trigger.setter
    def trigger(self, val: UaDataChangeTrigger):
        self._trigger = val
        self._value.trigger = val._val

    @deadband_type.setter
    def deadband_type(self, val: UaUInt32):
        self._deadband_type = val
        self._value.deadbandType = val._val

    @deadband_value.setter
    def deadband_value(self, val: UaDouble):
        self._deadband_value = val
        self._value.deadbandValue = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaDataChangeFilter): NULL" + ("" if n is None else "\n")

        return ("(UaDataChangeFilter) :\n"
                + "\t" * (1 if n is None else n+1) + "trigger " + self._trigger.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "deadband_type " + self._deadband_type.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "deadband_value " + self._deadband_value.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaEndpointDescription +++++++++++++++++++++++
class UaEndpointDescription(UaType):
    _UA_TYPE = _UA_TYPES._ENDPOINTDESCRIPTION

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_EndpointDescription*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_EndpointDescription*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._endpoint_url = UaString(val=val.endpointUrl, is_pointer=False)
            self._server = UaApplicationDescription(val=val.server, is_pointer=False)
            self._server_certificate = UaByteString(val=val.serverCertificate, is_pointer=False)
            self._security_mode = UaMessageSecurityMode(val=val.securityMode, is_pointer=False)
            self._security_policy_uri = UaString(val=val.securityPolicyUri, is_pointer=False)
            self._user_identity_tokens_size = SizeT(val=val.userIdentityTokensSize, is_pointer=False)
            self._user_identity_tokens = UaUserTokenPolicy(val=val.userIdentityTokens, is_pointer=True)
            self._transport_profile_uri = UaString(val=val.transportProfileUri, is_pointer=False)
            self._security_level = UaByte(val=val.securityLevel, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_EndpointDescription")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._endpoint_url._value[0] = _val(val.endpointUrl)
            self._server._value[0] = _val(val.server)
            self._server_certificate._value[0] = _val(val.serverCertificate)
            self._security_mode._value[0] = _val(val.securityMode)
            self._security_policy_uri._value[0] = _val(val.securityPolicyUri)
            self._user_identity_tokens_size._value[0] = _val(val.userIdentityTokensSize)
            self._user_identity_tokens._value = val.userIdentityTokens
            self._transport_profile_uri._value[0] = _val(val.transportProfileUri)
            self._security_level._value[0] = _val(val.securityLevel)

    @property
    def endpoint_url(self):
        if self._null:
            return None
        else:
            return self._endpoint_url

    @property
    def server(self):
        if self._null:
            return None
        else:
            return self._server

    @property
    def server_certificate(self):
        if self._null:
            return None
        else:
            return self._server_certificate

    @property
    def security_mode(self):
        if self._null:
            return None
        else:
            return self._security_mode

    @property
    def security_policy_uri(self):
        if self._null:
            return None
        else:
            return self._security_policy_uri

    @property
    def user_identity_tokens_size(self):
        if self._null:
            return None
        else:
            return self._user_identity_tokens_size

    @property
    def user_identity_tokens(self):
        if self._null:
            return None
        else:
            return self._user_identity_tokens

    @property
    def transport_profile_uri(self):
        if self._null:
            return None
        else:
            return self._transport_profile_uri

    @property
    def security_level(self):
        if self._null:
            return None
        else:
            return self._security_level

    @endpoint_url.setter
    def endpoint_url(self, val: UaString):
        self._endpoint_url = val
        self._value.endpointUrl = val._val

    @server.setter
    def server(self, val: UaApplicationDescription):
        self._server = val
        self._value.server = val._val

    @server_certificate.setter
    def server_certificate(self, val: UaByteString):
        self._server_certificate = val
        self._value.serverCertificate = val._val

    @security_mode.setter
    def security_mode(self, val: UaMessageSecurityMode):
        self._security_mode = val
        self._value.securityMode = val._val

    @security_policy_uri.setter
    def security_policy_uri(self, val: UaString):
        self._security_policy_uri = val
        self._value.securityPolicyUri = val._val

    @user_identity_tokens_size.setter
    def user_identity_tokens_size(self, val: SizeT):
        self._user_identity_tokens_size = val
        self._value.userIdentityTokensSize = val._val

    @user_identity_tokens.setter
    def user_identity_tokens(self, val: UaUserTokenPolicy):
        self._user_identity_tokens = val
        self._value.userIdentityTokens = val._ptr

    @transport_profile_uri.setter
    def transport_profile_uri(self, val: UaString):
        self._transport_profile_uri = val
        self._value.transportProfileUri = val._val

    @security_level.setter
    def security_level(self, val: UaByte):
        self._security_level = val
        self._value.securityLevel = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaEndpointDescription): NULL" + ("" if n is None else "\n")

        return ("(UaEndpointDescription) :\n"
                + "\t" * (1 if n is None else n+1) + "endpoint_url " + self._endpoint_url.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server " + self._server.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_certificate " + self._server_certificate.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_mode " + self._security_mode.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_policy_uri " + self._security_policy_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_identity_tokens_size " + self._user_identity_tokens_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_identity_tokens " + self._user_identity_tokens.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "transport_profile_uri " + self._transport_profile_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_level " + self._security_level.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaDeleteReferencesRequest +++++++++++++++++++++++
class UaDeleteReferencesRequest(UaType):
    _UA_TYPE = _UA_TYPES._DELETEREFERENCESREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DeleteReferencesRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DeleteReferencesRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._references_to_delete_size = SizeT(val=val.referencesToDeleteSize, is_pointer=False)
            self._references_to_delete = UaDeleteReferencesItem(val=val.referencesToDelete, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DeleteReferencesRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._references_to_delete_size._value[0] = _val(val.referencesToDeleteSize)
            self._references_to_delete._value = val.referencesToDelete

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def references_to_delete_size(self):
        if self._null:
            return None
        else:
            return self._references_to_delete_size

    @property
    def references_to_delete(self):
        if self._null:
            return None
        else:
            return self._references_to_delete

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @references_to_delete_size.setter
    def references_to_delete_size(self, val: SizeT):
        self._references_to_delete_size = val
        self._value.referencesToDeleteSize = val._val

    @references_to_delete.setter
    def references_to_delete(self, val: UaDeleteReferencesItem):
        self._references_to_delete = val
        self._value.referencesToDelete = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaDeleteReferencesRequest): NULL" + ("" if n is None else "\n")

        return ("(UaDeleteReferencesRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "references_to_delete_size " + self._references_to_delete_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "references_to_delete " + self._references_to_delete.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaTranslateBrowsePathsToNodeIdsRequest +++++++++++++++++++++++
class UaTranslateBrowsePathsToNodeIdsRequest(UaType):
    _UA_TYPE = _UA_TYPES._TRANSLATEBROWSEPATHSTONODEIDSREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_TranslateBrowsePathsToNodeIdsRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_TranslateBrowsePathsToNodeIdsRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._browse_paths_size = SizeT(val=val.browsePathsSize, is_pointer=False)
            self._browse_paths = UaBrowsePath(val=val.browsePaths, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_TranslateBrowsePathsToNodeIdsRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._browse_paths_size._value[0] = _val(val.browsePathsSize)
            self._browse_paths._value = val.browsePaths

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def browse_paths_size(self):
        if self._null:
            return None
        else:
            return self._browse_paths_size

    @property
    def browse_paths(self):
        if self._null:
            return None
        else:
            return self._browse_paths

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @browse_paths_size.setter
    def browse_paths_size(self, val: SizeT):
        self._browse_paths_size = val
        self._value.browsePathsSize = val._val

    @browse_paths.setter
    def browse_paths(self, val: UaBrowsePath):
        self._browse_paths = val
        self._value.browsePaths = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaTranslateBrowsePathsToNodeIdsRequest): NULL" + ("" if n is None else "\n")

        return ("(UaTranslateBrowsePathsToNodeIdsRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "browse_paths_size " + self._browse_paths_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "browse_paths " + self._browse_paths.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaFindServersResponse +++++++++++++++++++++++
class UaFindServersResponse(UaType):
    _UA_TYPE = _UA_TYPES._FINDSERVERSRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_FindServersResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_FindServersResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._servers_size = SizeT(val=val.serversSize, is_pointer=False)
            self._servers = UaApplicationDescription(val=val.servers, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_FindServersResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._servers_size._value[0] = _val(val.serversSize)
            self._servers._value = val.servers

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def servers_size(self):
        if self._null:
            return None
        else:
            return self._servers_size

    @property
    def servers(self):
        if self._null:
            return None
        else:
            return self._servers

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @servers_size.setter
    def servers_size(self, val: SizeT):
        self._servers_size = val
        self._value.serversSize = val._val

    @servers.setter
    def servers(self, val: UaApplicationDescription):
        self._servers = val
        self._value.servers = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaFindServersResponse): NULL" + ("" if n is None else "\n")

        return ("(UaFindServersResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "servers_size " + self._servers_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "servers " + self._servers.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCreateSessionRequest +++++++++++++++++++++++
class UaCreateSessionRequest(UaType):
    _UA_TYPE = _UA_TYPES._CREATESESSIONREQUEST

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CreateSessionRequest*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CreateSessionRequest*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._request_header = UaRequestHeader(val=val.requestHeader, is_pointer=False)
            self._client_description = UaApplicationDescription(val=val.clientDescription, is_pointer=False)
            self._server_uri = UaString(val=val.serverUri, is_pointer=False)
            self._endpoint_url = UaString(val=val.endpointUrl, is_pointer=False)
            self._session_name = UaString(val=val.sessionName, is_pointer=False)
            self._client_nonce = UaByteString(val=val.clientNonce, is_pointer=False)
            self._client_certificate = UaByteString(val=val.clientCertificate, is_pointer=False)
            self._requested_session_timeout = UaDouble(val=val.requestedSessionTimeout, is_pointer=False)
            self._max_response_message_size = UaUInt32(val=val.maxResponseMessageSize, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CreateSessionRequest")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._request_header._value[0] = _val(val.requestHeader)
            self._client_description._value[0] = _val(val.clientDescription)
            self._server_uri._value[0] = _val(val.serverUri)
            self._endpoint_url._value[0] = _val(val.endpointUrl)
            self._session_name._value[0] = _val(val.sessionName)
            self._client_nonce._value[0] = _val(val.clientNonce)
            self._client_certificate._value[0] = _val(val.clientCertificate)
            self._requested_session_timeout._value[0] = _val(val.requestedSessionTimeout)
            self._max_response_message_size._value[0] = _val(val.maxResponseMessageSize)

    @property
    def request_header(self):
        if self._null:
            return None
        else:
            return self._request_header

    @property
    def client_description(self):
        if self._null:
            return None
        else:
            return self._client_description

    @property
    def server_uri(self):
        if self._null:
            return None
        else:
            return self._server_uri

    @property
    def endpoint_url(self):
        if self._null:
            return None
        else:
            return self._endpoint_url

    @property
    def session_name(self):
        if self._null:
            return None
        else:
            return self._session_name

    @property
    def client_nonce(self):
        if self._null:
            return None
        else:
            return self._client_nonce

    @property
    def client_certificate(self):
        if self._null:
            return None
        else:
            return self._client_certificate

    @property
    def requested_session_timeout(self):
        if self._null:
            return None
        else:
            return self._requested_session_timeout

    @property
    def max_response_message_size(self):
        if self._null:
            return None
        else:
            return self._max_response_message_size

    @request_header.setter
    def request_header(self, val: UaRequestHeader):
        self._request_header = val
        self._value.requestHeader = val._val

    @client_description.setter
    def client_description(self, val: UaApplicationDescription):
        self._client_description = val
        self._value.clientDescription = val._val

    @server_uri.setter
    def server_uri(self, val: UaString):
        self._server_uri = val
        self._value.serverUri = val._val

    @endpoint_url.setter
    def endpoint_url(self, val: UaString):
        self._endpoint_url = val
        self._value.endpointUrl = val._val

    @session_name.setter
    def session_name(self, val: UaString):
        self._session_name = val
        self._value.sessionName = val._val

    @client_nonce.setter
    def client_nonce(self, val: UaByteString):
        self._client_nonce = val
        self._value.clientNonce = val._val

    @client_certificate.setter
    def client_certificate(self, val: UaByteString):
        self._client_certificate = val
        self._value.clientCertificate = val._val

    @requested_session_timeout.setter
    def requested_session_timeout(self, val: UaDouble):
        self._requested_session_timeout = val
        self._value.requestedSessionTimeout = val._val

    @max_response_message_size.setter
    def max_response_message_size(self, val: UaUInt32):
        self._max_response_message_size = val
        self._value.maxResponseMessageSize = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaCreateSessionRequest): NULL" + ("" if n is None else "\n")

        return ("(UaCreateSessionRequest) :\n"
                + "\t" * (1 if n is None else n+1) + "request_header " + self._request_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "client_description " + self._client_description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_uri " + self._server_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "endpoint_url " + self._endpoint_url.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "session_name " + self._session_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "client_nonce " + self._client_nonce.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "client_certificate " + self._client_certificate.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "requested_session_timeout " + self._requested_session_timeout.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_response_message_size " + self._max_response_message_size.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaContentFilterElement +++++++++++++++++++++++
class UaContentFilterElement(UaType):
    _UA_TYPE = _UA_TYPES._CONTENTFILTERELEMENT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ContentFilterElement*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ContentFilterElement*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._filter_operator = UaFilterOperator(val=val.filterOperator, is_pointer=False)
            self._filter_operands_size = SizeT(val=val.filterOperandsSize, is_pointer=False)
            self._filter_operands = UaExtensionObject(val=val.filterOperands, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ContentFilterElement")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._filter_operator._value[0] = _val(val.filterOperator)
            self._filter_operands_size._value[0] = _val(val.filterOperandsSize)
            self._filter_operands._value = val.filterOperands

    @property
    def filter_operator(self):
        if self._null:
            return None
        else:
            return self._filter_operator

    @property
    def filter_operands_size(self):
        if self._null:
            return None
        else:
            return self._filter_operands_size

    @property
    def filter_operands(self):
        if self._null:
            return None
        else:
            return self._filter_operands

    @filter_operator.setter
    def filter_operator(self, val: UaFilterOperator):
        self._filter_operator = val
        self._value.filterOperator = val._val

    @filter_operands_size.setter
    def filter_operands_size(self, val: SizeT):
        self._filter_operands_size = val
        self._value.filterOperandsSize = val._val

    @filter_operands.setter
    def filter_operands(self, val: UaExtensionObject):
        self._filter_operands = val
        self._value.filterOperands = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaContentFilterElement): NULL" + ("" if n is None else "\n")

        return ("(UaContentFilterElement) :\n"
                + "\t" * (1 if n is None else n+1) + "filter_operator " + self._filter_operator.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "filter_operands_size " + self._filter_operands_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "filter_operands " + self._filter_operands.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaTranslateBrowsePathsToNodeIdsResponse +++++++++++++++++++++++
class UaTranslateBrowsePathsToNodeIdsResponse(UaType):
    _UA_TYPE = _UA_TYPES._TRANSLATEBROWSEPATHSTONODEIDSRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_TranslateBrowsePathsToNodeIdsResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_TranslateBrowsePathsToNodeIdsResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaBrowsePathResult(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_TranslateBrowsePathsToNodeIdsResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaBrowsePathResult):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaTranslateBrowsePathsToNodeIdsResponse): NULL" + ("" if n is None else "\n")

        return ("(UaTranslateBrowsePathsToNodeIdsResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaBrowseResponse +++++++++++++++++++++++
class UaBrowseResponse(UaType):
    _UA_TYPE = _UA_TYPES._BROWSERESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_BrowseResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_BrowseResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._results_size = SizeT(val=val.resultsSize, is_pointer=False)
            self._results = UaBrowseResult(val=val.results, is_pointer=True)
            self._diagnostic_infos_size = SizeT(val=val.diagnosticInfosSize, is_pointer=False)
            self._diagnostic_infos = UaDiagnosticInfo(val=val.diagnosticInfos, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_BrowseResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._results_size._value[0] = _val(val.resultsSize)
            self._results._value = val.results
            self._diagnostic_infos_size._value[0] = _val(val.diagnosticInfosSize)
            self._diagnostic_infos._value = val.diagnosticInfos

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def results_size(self):
        if self._null:
            return None
        else:
            return self._results_size

    @property
    def results(self):
        if self._null:
            return None
        else:
            return self._results

    @property
    def diagnostic_infos_size(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos_size

    @property
    def diagnostic_infos(self):
        if self._null:
            return None
        else:
            return self._diagnostic_infos

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @results_size.setter
    def results_size(self, val: SizeT):
        self._results_size = val
        self._value.resultsSize = val._val

    @results.setter
    def results(self, val: UaBrowseResult):
        self._results = val
        self._value.results = val._ptr

    @diagnostic_infos_size.setter
    def diagnostic_infos_size(self, val: SizeT):
        self._diagnostic_infos_size = val
        self._value.diagnosticInfosSize = val._val

    @diagnostic_infos.setter
    def diagnostic_infos(self, val: UaDiagnosticInfo):
        self._diagnostic_infos = val
        self._value.diagnosticInfos = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaBrowseResponse): NULL" + ("" if n is None else "\n")

        return ("(UaBrowseResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results_size " + self._results_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "results " + self._results.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos_size " + self._diagnostic_infos_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "diagnostic_infos " + self._diagnostic_infos.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaCreateSessionResponse +++++++++++++++++++++++
class UaCreateSessionResponse(UaType):
    _UA_TYPE = _UA_TYPES._CREATESESSIONRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CreateSessionResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CreateSessionResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
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

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CreateSessionResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._session_id._value[0] = _val(val.sessionId)
            self._authentication_token._value[0] = _val(val.authenticationToken)
            self._revised_session_timeout._value[0] = _val(val.revisedSessionTimeout)
            self._server_nonce._value[0] = _val(val.serverNonce)
            self._server_certificate._value[0] = _val(val.serverCertificate)
            self._server_endpoints_size._value[0] = _val(val.serverEndpointsSize)
            self._server_endpoints._value = val.serverEndpoints
            self._server_software_certificates_size._value[0] = _val(val.serverSoftwareCertificatesSize)
            self._server_software_certificates._value = val.serverSoftwareCertificates
            self._server_signature._value[0] = _val(val.serverSignature)
            self._max_request_message_size._value[0] = _val(val.maxRequestMessageSize)

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def session_id(self):
        if self._null:
            return None
        else:
            return self._session_id

    @property
    def authentication_token(self):
        if self._null:
            return None
        else:
            return self._authentication_token

    @property
    def revised_session_timeout(self):
        if self._null:
            return None
        else:
            return self._revised_session_timeout

    @property
    def server_nonce(self):
        if self._null:
            return None
        else:
            return self._server_nonce

    @property
    def server_certificate(self):
        if self._null:
            return None
        else:
            return self._server_certificate

    @property
    def server_endpoints_size(self):
        if self._null:
            return None
        else:
            return self._server_endpoints_size

    @property
    def server_endpoints(self):
        if self._null:
            return None
        else:
            return self._server_endpoints

    @property
    def server_software_certificates_size(self):
        if self._null:
            return None
        else:
            return self._server_software_certificates_size

    @property
    def server_software_certificates(self):
        if self._null:
            return None
        else:
            return self._server_software_certificates

    @property
    def server_signature(self):
        if self._null:
            return None
        else:
            return self._server_signature

    @property
    def max_request_message_size(self):
        if self._null:
            return None
        else:
            return self._max_request_message_size

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @session_id.setter
    def session_id(self, val: UaNodeId):
        self._session_id = val
        self._value.sessionId = val._val

    @authentication_token.setter
    def authentication_token(self, val: UaNodeId):
        self._authentication_token = val
        self._value.authenticationToken = val._val

    @revised_session_timeout.setter
    def revised_session_timeout(self, val: UaDouble):
        self._revised_session_timeout = val
        self._value.revisedSessionTimeout = val._val

    @server_nonce.setter
    def server_nonce(self, val: UaByteString):
        self._server_nonce = val
        self._value.serverNonce = val._val

    @server_certificate.setter
    def server_certificate(self, val: UaByteString):
        self._server_certificate = val
        self._value.serverCertificate = val._val

    @server_endpoints_size.setter
    def server_endpoints_size(self, val: SizeT):
        self._server_endpoints_size = val
        self._value.serverEndpointsSize = val._val

    @server_endpoints.setter
    def server_endpoints(self, val: UaEndpointDescription):
        self._server_endpoints = val
        self._value.serverEndpoints = val._ptr

    @server_software_certificates_size.setter
    def server_software_certificates_size(self, val: SizeT):
        self._server_software_certificates_size = val
        self._value.serverSoftwareCertificatesSize = val._val

    @server_software_certificates.setter
    def server_software_certificates(self, val: UaSignedSoftwareCertificate):
        self._server_software_certificates = val
        self._value.serverSoftwareCertificates = val._ptr

    @server_signature.setter
    def server_signature(self, val: UaSignatureData):
        self._server_signature = val
        self._value.serverSignature = val._val

    @max_request_message_size.setter
    def max_request_message_size(self, val: UaUInt32):
        self._max_request_message_size = val
        self._value.maxRequestMessageSize = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaCreateSessionResponse): NULL" + ("" if n is None else "\n")

        return ("(UaCreateSessionResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "session_id " + self._session_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "authentication_token " + self._authentication_token.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "revised_session_timeout " + self._revised_session_timeout.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_nonce " + self._server_nonce.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_certificate " + self._server_certificate.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_endpoints_size " + self._server_endpoints_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_endpoints " + self._server_endpoints.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_software_certificates_size " + self._server_software_certificates_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_software_certificates " + self._server_software_certificates.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_signature " + self._server_signature.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_request_message_size " + self._max_request_message_size.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaContentFilter +++++++++++++++++++++++
class UaContentFilter(UaType):
    _UA_TYPE = _UA_TYPES._CONTENTFILTER

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ContentFilter*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ContentFilter*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._elements_size = SizeT(val=val.elementsSize, is_pointer=False)
            self._elements = UaContentFilterElement(val=val.elements, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ContentFilter")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._elements_size._value[0] = _val(val.elementsSize)
            self._elements._value = val.elements

    @property
    def elements_size(self):
        if self._null:
            return None
        else:
            return self._elements_size

    @property
    def elements(self):
        if self._null:
            return None
        else:
            return self._elements

    @elements_size.setter
    def elements_size(self, val: SizeT):
        self._elements_size = val
        self._value.elementsSize = val._val

    @elements.setter
    def elements(self, val: UaContentFilterElement):
        self._elements = val
        self._value.elements = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaContentFilter): NULL" + ("" if n is None else "\n")

        return ("(UaContentFilter) :\n"
                + "\t" * (1 if n is None else n+1) + "elements_size " + self._elements_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "elements " + self._elements.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaGetEndpointsResponse +++++++++++++++++++++++
class UaGetEndpointsResponse(UaType):
    _UA_TYPE = _UA_TYPES._GETENDPOINTSRESPONSE

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_GetEndpointsResponse*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_GetEndpointsResponse*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._response_header = UaResponseHeader(val=val.responseHeader, is_pointer=False)
            self._endpoints_size = SizeT(val=val.endpointsSize, is_pointer=False)
            self._endpoints = UaEndpointDescription(val=val.endpoints, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_GetEndpointsResponse")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._response_header._value[0] = _val(val.responseHeader)
            self._endpoints_size._value[0] = _val(val.endpointsSize)
            self._endpoints._value = val.endpoints

    @property
    def response_header(self):
        if self._null:
            return None
        else:
            return self._response_header

    @property
    def endpoints_size(self):
        if self._null:
            return None
        else:
            return self._endpoints_size

    @property
    def endpoints(self):
        if self._null:
            return None
        else:
            return self._endpoints

    @response_header.setter
    def response_header(self, val: UaResponseHeader):
        self._response_header = val
        self._value.responseHeader = val._val

    @endpoints_size.setter
    def endpoints_size(self, val: SizeT):
        self._endpoints_size = val
        self._value.endpointsSize = val._val

    @endpoints.setter
    def endpoints(self, val: UaEndpointDescription):
        self._endpoints = val
        self._value.endpoints = val._ptr

    def __str__(self, n=None):
        if self._null:
            return "(UaGetEndpointsResponse): NULL" + ("" if n is None else "\n")

        return ("(UaGetEndpointsResponse) :\n"
                + "\t" * (1 if n is None else n+1) + "response_header " + self._response_header.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "endpoints_size " + self._endpoints_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "endpoints " + self._endpoints.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaEventFilter +++++++++++++++++++++++
class UaEventFilter(UaType):
    _UA_TYPE = _UA_TYPES._EVENTFILTER

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_EventFilter*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_EventFilter*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._select_clauses_size = SizeT(val=val.selectClausesSize, is_pointer=False)
            self._select_clauses = UaSimpleAttributeOperand(val=val.selectClauses, is_pointer=True)
            self._where_clause = UaContentFilter(val=val.whereClause, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_EventFilter")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._select_clauses_size._value[0] = _val(val.selectClausesSize)
            self._select_clauses._value = val.selectClauses
            self._where_clause._value[0] = _val(val.whereClause)

    @property
    def select_clauses_size(self):
        if self._null:
            return None
        else:
            return self._select_clauses_size

    @property
    def select_clauses(self):
        if self._null:
            return None
        else:
            return self._select_clauses

    @property
    def where_clause(self):
        if self._null:
            return None
        else:
            return self._where_clause

    @select_clauses_size.setter
    def select_clauses_size(self, val: SizeT):
        self._select_clauses_size = val
        self._value.selectClausesSize = val._val

    @select_clauses.setter
    def select_clauses(self, val: UaSimpleAttributeOperand):
        self._select_clauses = val
        self._value.selectClauses = val._ptr

    @where_clause.setter
    def where_clause(self, val: UaContentFilter):
        self._where_clause = val
        self._value.whereClause = val._val

    def __str__(self, n=None):
        if self._null:
            return "(UaEventFilter): NULL" + ("" if n is None else "\n")

        return ("(UaEventFilter) :\n"
                + "\t" * (1 if n is None else n+1) + "select_clauses_size " + self._select_clauses_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "select_clauses " + self._select_clauses.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "where_clause " + self._where_clause.__str__(1 if n is None else n+1))
