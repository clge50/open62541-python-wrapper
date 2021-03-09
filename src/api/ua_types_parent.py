# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import re
from intermediateApi import ffi, lib

x = ffi.new("UA_Int32[12]")
x[9] = 3

def _is_ptr(val):
    if "*" in str(val) or "[" in str(val):
        return True
    else:
        return False


def _is_null(val):
    return "NULL" in re.sub(r"'.*?'", "", str(val))


def _get_c_type(val):
    c_type = str(val).split("'")[1]
    return re.sub(r"[^A-Za-z1-9_ ]", "", c_type, re.ASCII).strip()

# if val is a primitive type, then _ptr returns a pointer to a COPY of the value!!!
def _ptr(val, c_type=""):
    if c_type == "":
        c_type = str(val).split("'")[1]
        c_type = re.sub(r"[^A-Za-z1-9_ ]", "", c_type, re.ASCII).strip()
    if _is_null(val):
        return ffi.NULL
    if "&" in str(val):
        return ffi.addressof(val)
    if "*" in str(val) or "[" in str(val):
        return val
    else:
        try:
            return ffi.cast(c_type + "*", ffi.addressof(val))
        except TypeError:
            return ffi.new(c_type + "*", val)


def _val(val, c_type=""):
    if not _is_ptr(val):
        return val
    if c_type != "":
        return ffi.cast(c_type+"*", val)[0]
    return val[0]


# _value should always be a pointer
# to get a pointer call ._ptr to get the value call ._val
# TODO: Idea -> free the passed memory when ever a primitive type is copied in _ptr.
#  Then all base types hold their owner.
class UaType:
    def __init__(self, val, is_pointer=False):
        if not is_pointer:
            val = _ptr(val)
        self._value = val
        self._is_pointer = is_pointer
        self._null = _is_null(val)

    @property
    def _val(self):
        return self._value[0]

    @property
    def _ptr(self):
        return self._value

    def __str__(self, n=0):
        return str(self._val)


