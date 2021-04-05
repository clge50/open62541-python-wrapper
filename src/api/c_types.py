# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_types_parent import *
from ua_types_parent import _ptr, _val, _is_null, _is_ptr


# TODO: use from and new_handle
# +++++++++++++++++++ Void +++++++++++++++++++++++
class Void(UaType):
    def __init__(self, data=None, val=None, is_pointer=True):
        if data is not None:
            val = ffi.new_handle(data)
        elif val is None:
            val = ffi.NULL

        super().__init__(ffi.cast("void*", _ptr(val)), is_pointer)

    # TODO: Should this be possible? Where/which references will be changed?
    def _set_value(self, val):
        self._value = ffi.cast("void*", _val(val))

    @staticmethod
    def NULL():
        return Void(val=ffi.NULL)

    @property
    def data(self):
        if type(self._ptr) is type(Void(ffi.NULL)._ptr):
            return self._ptr
        else:
            return ffi.from_handle(self._ptr)

    def __str__(self, n=None):
        if self._null:
            return "(Void): NULL" + ("" if n is None else "\n")
        else:
            return "(Void): " + str(self.data) + ("" if n is None else "\n")


# +++++++++++++++++++ SizeT +++++++++++++++++++++++
class SizeT(UaType):
    def __init__(self, val=None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("size_t*", val._ptr)
        if val is None:
            super().__init__(ffi.new("size_t*"), is_pointer)
        else:
            if is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("size_t*", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "size_t")
        else:
            self._value[0] = ffi.cast("size_t", _val(val))

    @property
    def value(self):
        return int(self._val)
    
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
        return SizeT(self.value + (other._val if isinstance(other, UaType) else other))

    def __sub__(self, other):
        return SizeT(self.value - (other._val if isinstance(other, UaType) else other))

    def __mul__(self, other):
        return SizeT(self.value - (other._val if isinstance(other, UaType) else other))

    def __floordiv__(self, other):
        return SizeT(self.value // (other._val if isinstance(other, UaType) else other))

    def __mod__(self, other):
        return SizeT(self.value % (other._val if isinstance(other, UaType) else other))

    def __or__(self, other):
        return SizeT(self._val | (other._val if isinstance(other, UaType) else other))

    def __and__(self, other):
        return SizeT(self._val & (other._val if isinstance(other, UaType) else other))

    def __xor__(self, other):
        return SizeT(self._val ^ (other._val if isinstance(other, UaType) else other))

    def __str__(self, n=None):
        return "(SizeT): " + str(self._val) + ("" if n is None else "\n")


# +++++++++++++++++++ CString +++++++++++++++++++++++
class CString(UaType):
    def __init__(self, p_val: str = "", is_pointer=True, val=None):
        if type(val) is Void:
            val = ffi.cast("char[]", val._ptr)
        p_val = bytes(p_val, "utf-8")
        if val is None:
            super().__init__(ffi.new("char[]", p_val), is_pointer)
            self._p_value = p_val
        else:
            super().__init__(val, is_pointer)
            if self._null:
                self._p_value = None
            else:
                self._p_value = ffi.string(val)

    @property
    def value(self):
        return self._p_value

    @value.setter
    def value(self, val: bytes):
        self._p_value = val
        self._value = ffi.new("char[]", self._p_value)

    def __str__(self, n=None):
        return "(CString): " + str(self.value) + ("" if n is None else "\n")

    def __add__(self, other):
        if isinstance(other, CString):
            return CString(self.value + other.value)
        else:
            return CString(self.value + other)

    def __mul__(self, other: int):
        return CString(self.value * other)
    
    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        if isinstance(other, CString):
            return self.value != other.value
        else:
            return self.value != other
