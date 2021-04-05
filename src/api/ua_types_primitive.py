# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from typing import Union, List
from ua_consts_types_raw import _UA_TYPES
from intermediateApi import ffi, lib
from ua_types_common import *
from ua_types_parent import _ptr, _val, _is_null, _is_ptr


# +++++++++++++++++++ UaBoolean +++++++++++++++++++++++
class UaBoolean(UaType):
    _UA_TYPE = _UA_TYPES._BOOLEAN

    def __init__(self, val: Union[Void, bool, List[bool]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Boolean*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Boolean*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Boolean[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Boolean*", _val(val)), is_pointer)

    @property
    def value(self):
        return bool(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Boolean")
        else:
            self._value[0] = ffi.cast("UA_Boolean", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaBoolean) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaBoolean): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)


# +++++++++++++++++++ UaSByte +++++++++++++++++++++++
class UaSByte(UaType):
    _UA_TYPE = _UA_TYPES._SBYTE

    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_SByte*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_SByte*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_SByte[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_SByte*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SByte")
        else:
            self._value[0] = ffi.cast("UA_SByte", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaSByte) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaSByte): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaSByte(self.value + (int(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaSByte(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaSByte(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __floordiv__(self, other):
        return UaSByte(self.value // (int(other._val) if isinstance(other, UaType) else other))

    def __mod__(self, other):
        return UaSByte(self.value % (int(other._val) if isinstance(other, UaType) else other))

    def __or__(self, other):
        return UaSByte(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return UaSByte(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return UaSByte(self._val ^ (other._val if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaByte +++++++++++++++++++++++
class UaByte(UaType):
    _UA_TYPE = _UA_TYPES._BYTE

    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Byte*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Byte*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Byte[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Byte*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Byte")
        else:
            self._value[0] = ffi.cast("UA_Byte", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaSByte) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaByte): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaByte(self.value + (int(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaByte(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaByte(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __floordiv__(self, other):
        return UaByte(self.value // (int(other._val) if isinstance(other, UaType) else other))

    def __mod__(self, other):
        return UaByte(self.value % (int(other._val) if isinstance(other, UaType) else other))

    def __or__(self, other):
        return UaByte(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return UaByte(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return UaByte(self._val ^ (other._val if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaInt16 +++++++++++++++++++++++
class UaInt16(UaType):
    _UA_TYPE = _UA_TYPES._INT16

    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Int16*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Int16*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Int16[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Int16*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int16")
        else:
            self._value[0] = ffi.cast("UA_Int16", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaInt16) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaInt16): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaInt16(self.value + (int(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaInt16(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaInt16(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __floordiv__(self, other):
        return UaInt16(self.value // (int(other._val) if isinstance(other, UaType) else other))

    def __mod__(self, other):
        return UaInt16(self.value % (int(other._val) if isinstance(other, UaType) else other))

    def __or__(self, other):
        return UaByte(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return UaByte(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return UaByte(self._val ^ (other._val if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaUInt16 +++++++++++++++++++++++
class UaUInt16(UaType):
    _UA_TYPE = _UA_TYPES._UINT16

    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_UInt16*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_UInt16*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_UInt16[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_UInt16*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt16")
        else:
            self._value[0] = ffi.cast("UA_UInt16", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaUInt16) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaUInt16): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaUInt16(self.value + (int(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaUInt16(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaUInt16(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __floordiv__(self, other):
        return UaUInt16(self.value // (int(other._val) if isinstance(other, UaType) else other))

    def __mod__(self, other):
        return UaUInt16(self.value % (int(other._val) if isinstance(other, UaType) else other))

    def __or__(self, other):
        return UaUInt16(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return UaUInt16(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return UaUInt16(self._val ^ (other._val if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaInt32 +++++++++++++++++++++++
class UaInt32(UaType):
    _UA_TYPE = _UA_TYPES._INT32

    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Int32*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Int32*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Int32[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Int32*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int32")
        else:
            self._value[0] = ffi.cast("UA_Int32", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaInt32) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaInt32): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaInt32(self.value + (int(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaInt32(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaInt32(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __floordiv__(self, other):
        return UaInt32(self.value // (int(other._val) if isinstance(other, UaType) else other))

    def __mod__(self, other):
        return UaInt32(self.value % (int(other._val) if isinstance(other, UaType) else other))

    def __or__(self, other):
        return UaInt32(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return UaInt32(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return UaInt32(self._val ^ (other._val if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaUInt32 +++++++++++++++++++++++
class UaUInt32(UaType):
    _UA_TYPE = _UA_TYPES._UINT32

    def __init__(self, val=None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_UInt32*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_UInt32*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_UInt32[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_UInt32*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt32")
        else:
            self._value[0] = ffi.cast("UA_UInt32", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaUInt32) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaUInt32): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaUInt32(self.value + (int(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaUInt32(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaUInt32(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __floordiv__(self, other):
        return UaUInt32(self.value // (int(other._val) if isinstance(other, UaType) else other))

    def __mod__(self, other):
        return UaUInt32(self.value % (int(other._val) if isinstance(other, UaType) else other))

    def __or__(self, other):
        return UaUInt32(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return UaUInt32(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return UaUInt32(self._val ^ (other._val if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaInt64 +++++++++++++++++++++++
class UaInt64(UaType):
    _UA_TYPE = _UA_TYPES._INT64

    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Int64*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Int64*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Int64[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Int64*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int64")
        else:
            self._value[0] = ffi.cast("UA_Int64", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaInt64) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaInt64): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaInt64(self.value + (int(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaInt64(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaInt64(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __floordiv__(self, other):
        return UaInt64(self.value // (int(other._val) if isinstance(other, UaType) else other))

    def __mod__(self, other):
        return UaInt64(self.value % (int(other._val) if isinstance(other, UaType) else other))

    def __or__(self, other):
        return UaUInt32(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return UaUInt32(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return UaUInt32(self._val ^ (other._val if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaUInt64 +++++++++++++++++++++++
class UaUInt64(UaType):
    _UA_TYPE = _UA_TYPES._UINT64

    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_UInt64*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_UInt64*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_UInt64[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_UInt64*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt64")
        else:
            self._value[0] = ffi.cast("UA_UInt64", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaUInt64) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaUInt64): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaUInt64(self.value + (int(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaUInt64(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaUInt64(self.value - (int(other._val) if isinstance(other, UaType) else other))

    def __floordiv__(self, other):
        return UaUInt64(self.value // (int(other._val) if isinstance(other, UaType) else other))

    def __mod__(self, other):
        return UaUInt64(self.value % (int(other._val) if isinstance(other, UaType) else other))

    def __or__(self, other):
        return UaUInt64(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return UaUInt64(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return UaUInt64(self._val ^ (other._val if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaFloat +++++++++++++++++++++++
class UaFloat(UaType):
    _UA_TYPE = _UA_TYPES._FLOAT

    def __init__(self, val: Union[Void, float, List[float]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Float*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Float*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Float[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Float*", _val(val)), is_pointer)

    @property
    def value(self):
        return float(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Float")
        else:
            self._value[0] = ffi.cast("UA_Float", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaFloat) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaFloat): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaFloat(self.value + (float(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaFloat(self.value - (float(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaFloat(self.value - (float(other._val) if isinstance(other, UaType) else other))

    def __truediv__(self, other):
        return UaFloat(self.value / (float(other._val) if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaDouble +++++++++++++++++++++++
class UaDouble(UaType):
    _UA_TYPE = _UA_TYPES._DOUBLE

    def __init__(self, val=None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Double*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Double*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Double[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Double*", _val(val)), is_pointer)

    @property
    def value(self):
        return float(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Double")
        else:
            self._value[0] = ffi.cast("UA_Double", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaDouble) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaDouble): " + str(self._val) + ("" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __add__(self, other):
        return UaDouble(self.value + (float(other._val) if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return UaDouble(self.value - (float(other._val) if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return UaDouble(self.value - (float(other._val) if isinstance(other, UaType) else other))

    def __truediv__(self, other):
        return UaDouble(self.value / (float(other._val) if isinstance(other, UaType) else other))


# +++++++++++++++++++ UaStatusCode +++++++++++++++++++++++
class UaStatusCode(UaType):
    _UA_TYPE = _UA_TYPES._STATUSCODE

    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_StatusCode*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_StatusCode*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_StatusCode[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_StatusCode*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    @value.setter
    def value(self, val):
        self._value[0] = val

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_StatusCode")
        else:
            self._value[0] = ffi.cast("UA_StatusCode", _val(val))

    def __str__(self, n=None):
        if self._null:
            return "(UaStatusCode) : NULL" + ("" if n is None else "\n")
        else:
            return "(UaStatusCode): " + ffi.string(lib.UA_StatusCode_name(self._val)).decode("utf-8") + (
                "" if n is None else "\n")

    def __eq__(self, other):
        return self._val == (other._val if isinstance(other, UaType) else other)

    def __ne__(self, other):
        return self._val != (other._val if isinstance(other, UaType) else other)

    def __gt__(self, other):
        return self._val > (other._val if isinstance(other, UaType) else other)

    def __lt__(self, other):
        return self._val < (other._val if isinstance(other, UaType) else other)

    def __ge__(self, other):
        return self._val >= (other._val if isinstance(other, UaType) else other)

    def __le__(self, other):
        return self._val <= (other._val if isinstance(other, UaType) else other)

    def __or__(self, other):
        return UaStatusCode(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return UaStatusCode(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return UaStatusCode(self._val ^ (other._val if isinstance(other, UaType) else other))

    def is_bad(self):
        return lib.UA_StatusCode_isBad(self._val)

    def is_good(self):
        return not lib.UA_StatusCode_isBad(self._val)


# +++++++++++++++++++ UaString +++++++++++++++++++++++
class UaString(UaType):
    _UA_TYPE = _UA_TYPES._STRING

    def __init__(self, val: Union[str, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_String*", val._ptr)
        elif type(val) is str:
            val = ffi.new("UA_String*", lib.UA_String_fromChars(bytes(val, 'utf-8')))
        elif type(val) is bytes:
            val = ffi.new("UA_String*", lib.UA_String_fromChars(val))
        elif type(val) is not None:
            if not is_pointer:
                val = ffi.new("UA_String*", val)
        else:
            val = ffi.new("UA_String*")

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._length = SizeT(val=val.length, is_pointer=False)
            self._data = UaByte(val=val.data, is_pointer=True)
            if _is_null(self._data):
                self._null = True

    def _update(self):
        self.__init__(val=self._ptr)

    # Rather make new UaString?
    #   -> not sure where the pointer is directed and if there is enough memory for evtually more bytes than befor
    #   -> memory management for alloced memory from UA_String_fromChars
    #
    # def _set_value(self, val):
    #     if self._is_pointer:
    #         self._value = _ptr(val, "UA_String")
    #     else:
    #         self._value[0] = _val(val)
    #
    #     if not _is_null(val):
    #         self._length._value[0] = _val(val.length)
    #         self._data._value = val.data

    @property
    def length(self):
        if self._null:
            return None
        else:
            return self._length

    @property
    def data(self):
        if self._null:
            return None
        else:
            return self._data

    def __eq__(self, ua_string):
        return lib.UA_String_equal(self._ptr, ua_string._ptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return UaString(self.value + other.value)

    def __mul__(self, other: int):
        return UaString(self.value * other)

    def equal_ignore_case(self, ua_string):
        return lib.UA_String_equal_ignorecase(self._ptr, ua_string._ptr)

    @property
    def value(self) -> str:
        if self._null:
            return "NULL"
        return ffi.string(ffi.cast(f"char[{self.length._val}]", self.data._ptr), self.length._val).decode("utf-8")

    def __str__(self, n=None):
        return "(UaString): " + self.value + ("" if n is None else "\n")


# +++++++++++++++++++ UaByteString +++++++++++++++++++++++
class UaByteString(UaString):
    _UA_TYPE = _UA_TYPES._BYTESTRING

    def __init__(self, val: Union[str, bytes, Void] = None, is_pointer=False):
        super().__init__(val, is_pointer)

    @property
    def value(self) -> bytes:
        if self._null:
            return "NULL"
        return ffi.string(ffi.cast(f"char[{self.length._val}]", self.data._ptr), self.length._val)


# +++++++++++++++++++ UaXmlElement +++++++++++++++++++++++
class UaXmlElement(UaString):
    _UA_TYPE = _UA_TYPES._XMLELEMENT

    def __init__(self, val: Union[str, bytes, Void] = None, is_pointer=False):
        super().__init__(val, is_pointer)

