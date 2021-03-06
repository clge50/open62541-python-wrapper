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

        super().__init__(ffi.cast("void*", _ptr(val)), is_pointer)

    # TODO: Should this be possible? Where/which references will be changed?
    def _set_value(self, val):
        self._value = ffi.cast("void*", _val(val))

    @property
    def data(self):
        return ffi.from_handle(self._ptr)

    def __str__(self, n=0):
        if self._null:
            return "(Void): NULL\n"
        else:
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
                super().__init__(ffi.new("size_t*", _val(val)), is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "size_t")
        else:
            self._value[0] = ffi.cast("size_t", _val(val))

    def __str__(self, n=0):
        return "(SizeT): " + str(self._value) + "\n"


# +++++++++++++++++++ CString +++++++++++++++++++++++
class CString(UaType):
    def __init__(self, p_val: str = "", is_pointer=True, val=None):
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
