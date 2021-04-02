# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import re
from intermediateApi import ffi, lib


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
        return ffi.cast(c_type + "*", val)[0]
    return val[0]


class UaType:
    """Root Wrapper class for all c/open62541 types

    UaType is the parent wrapper class for all non trivial c based open62541 types (native c types such as size_t and
    void* as well as ua types e.g. `UA_Int32`. The general idea of the UaType-system is that it in order to guarantee
    that both pointer types (e.g. `UA_Int32*`) as well as non pointer values (e.g. `UA_Int32`) all open62541 based values
    are stored as a pointer in _value.

    Developers that work on the open62541 python wrapper can work with UaTypes by using the `._ptr` method to get a
    pointer to the c value or `._val` to get a dereferenced value. CFFI should take care of the memory management by
    itself in most cases: once the "owner" of a pointer is no longer referenced (e.g. when setting a new value in
    _value) the garbage collector will take care of it. This does however not mean that developers don't have to
    think about memory management. Developers always have to consider what is happening to the owner of memory.
    Especially when working with delayed access to pointers, e.g. callback functions, developers always need to make
    sure that the owner of the memory that the pointer points to survives until it was made sure that open62541 will
    no longer attempt to access the memory. Else there will be segmentation faults and other memory errors/bugs.
    """

    def __init__(self, val, is_pointer=False):
        """Root constructor for c/open62541 types

        When working on the open62541 python wrapper itself rather than interacting with it as a user you will often
        encounter cases in which you have to wrap c/open62541 types. All classes which inherit from UaType will allow
        you to do so via this root constructor.

        Args:
            val (c/open62541 type): The c/open62541 based type as retrieved via CFFI which shall be wrapped. The
                specialised constructors of non abstract types will allow you to omit `val` in order to instanciate a new
                object without pre existing c value counterpart
            is_pointer (bool): indicates if the passed val is in pointer
                or dereferenced form to allow the constructor to store the data consistently. The standard value is `False`

        Example:
            `raw_value = UaStatusCode(val=lib.UA_Server_writeDataValue(...))`
                here the `lib.UA_Server_writeDataValue(...)` function returns a `UA_StatusCode`. To wrap it we use the
                constructor of UaStatusCode which inherits from UaType. We assign the c based value to `val` and don't
                explicitly set `is_pointer` because `val` is of type `UA_StatusCode` rather than `UA_StatusCode*`
                and the default value for `is_pointer` is `False`.
        """
        if not is_pointer:
            val = _ptr(val)
        self._value = val
        self._is_pointer = is_pointer
        self._null = _is_null(val)

    @property
    def _val(self):
        """
        Used to access the dereferenced value of a c/ua type
        """
        return self._value[0]

    @property
    def _ptr(self):
        """
        Used to access the pointer of a c/ua type
        """
        return self._value

    def __str__(self, n=None):
        return str(self._val)
