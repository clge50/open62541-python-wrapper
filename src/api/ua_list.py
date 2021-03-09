# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_base_types import *
from ua_types_parent import _ptr, _val, _is_null, _get_c_type, _is_ptr


class UaList(UaType):
    def __init__(self, val=None, size=None, ua_class=None):
        c_type = ""
        if type(val) is list:
            if ua_class is None:
                if type(val[0]) is int:
                    c_type = "UA_Int64"
                    ua_class = UaInt64
                elif type(val[0]) is float:
                    c_type = "UA_Double"
                    ua_class = UaDouble
                elif type(val[0]) is str:
                    c_type = "UA_String"
                    ua_class = UaString
                elif type(val[0]) is bool:
                    c_type = "UA_Boolean"
                    ua_class = "UaString"
            elif isinstance(ua_class(), UaType):
                c_type = _get_c_type(ua_class()._ptr)
            else:
                raise AttributeError("'ua_class' has to be None or a Subclass of UaType.")

            array = ffi.new(f"{c_type}[]", val)
            size = len(val)

        else:
            if isinstance(ua_class(), UaType):
                c_type = _get_c_type(ua_class()._ptr)
            else:
                raise AttributeError("'ua_class' has do be None or a subclass of UaType.")

            if size is None:
                raise AttributeError("if 'val' is not a python list 'size' has to be set.")

            array = ffi.cast(f"{c_type}[{size}]", val)

        super().__init__(val=array, is_pointer=True)
        self._size = size
        self._ua_type = ua_class
        self._c_type = c_type

    @property
    def _ptr_ptr(self):
        return ffi.new(f"{self._c_type}**", self._value)

    @property
    def ua_type(self):
        return self._ua_type

    @property
    def value(self):
        return ffi.unpack(self._ptr, self._size)

    def __len__(self):
        return self._size

    def __setitem__(self, index: int, value):
        if 0 > index or index > self._size:
            raise KeyError("index out of bound")
        if isinstance(value, UaType):
            self._ptr[index] = value._ptr

    def __getitem__(self, index):
        if isinstance(index, int):
            if 0 > index or index > self._size:
                raise KeyError("index out of bound")
            return self._ua_type(val=self._ptr[index])
        elif isinstance(index, slice):
            UaList(self.value[index], ua_class=self._ua_type)
        else:
            raise AttributeError("invalid indexing")
