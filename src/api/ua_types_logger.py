# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_types_generated_structs import *
from ua_types_parent import _ptr, _val

# +++++++++++++++++++ UaLogCategory +++++++++++++++++++++++
class UaLogCategory(UaType):
    UA_LOGCATEGORY_NETWORK = 0
    UA_LOGCATEGORY_SECURECHANNEL = 1
    UA_LOGCATEGORY_SESSION = 2
    UA_LOGCATEGORY_SERVER = 3
    UA_LOGCATEGORY_CLIENT = 4
    UA_LOGCATEGORY_USERLAND = 5
    UA_LOGCATEGORY_SECURITYPOLICY = 6

    val_to_string = dict([
        (0, "UA_LOGCATEGORY_NETWORK"),
        (1, "UA_LOGCATEGORY_SECURECHANNEL"),
        (2, "UA_LOGCATEGORY_SESSION"),
        (3, "UA_LOGCATEGORY_SERVER"),
        (4, "UA_LOGCATEGORY_CLIENT"),
        (5, "UA_LOGCATEGORY_USERLAND"),
        (6, "UA_LOGCATEGORY_SECURITYPOLICY")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_LogCategory*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_LogCategory", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_LogCategory")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaLogCategory): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaLogLevel +++++++++++++++++++++++
class UaLogLevel(UaType):
    UA_LOGLEVEL_TRACE = 0
    UA_LOGLEVEL_DEBUG = 1
    UA_LOGLEVEL_INFO = 2
    UA_LOGLEVEL_WARNING = 3
    UA_LOGLEVEL_ERROR = 4
    UA_LOGLEVEL_FATAL = 5

    val_to_string = dict([
        (0, "UA_LOGLEVEL_TRACE"),
        (1, "UA_LOGLEVEL_DEBUG"),
        (2, "UA_LOGLEVEL_INFO"),
        (3, "UA_LOGLEVEL_WARNING"),
        (4, "UA_LOGLEVEL_ERROR"),
        (5, "UA_LOGLEVEL_FATAL")])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_LogLevel*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_LogLevel", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_LogLevel")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self, n=0):
        return f"(UaLogLevel): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaLogger +++++++++++++++++++++++
class UaLogger(UaType):
    def __init__(self, log_level: UaLogLevel=None, val=lib.UA_Log_Stdout, is_pointer=False):
        if log_level is not None:
            val = lib.UA_Log_Stdout_withLevel(log_level._val)
        super().__init__(val=val, is_pointer=is_pointer)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Logger")
        else:
            self._value[0] = _val(val)

    def __str__(self, n=0):
        return "\t"*n + str(self._val)

    def trace(self, category: UaLogCategory, msg: str):
        lib.UA_LOG_TRACE(self._ptr, category._val, CString(msg)._ptr)

    def debug(self, category: UaLogCategory, msg: str):
        lib.UA_LOG_DEBUG(self._ptr, category._val, CString(msg)._ptr)

    def info(self, category: UaLogCategory, msg: str):
        lib.UA_LOG_INFO(self._ptr, category._val, CString(msg)._ptr)

    def warning(self, category: UaLogCategory, msg: str):
        lib.UA_LOG_WARNING(self._ptr, category._val, CString(msg)._ptr)

    def error(self, category: UaLogCategory, msg: str):
        lib.UA_LOG_ERROR(self._ptr, category._val, CString(msg)._ptr)

    # see definitions/log -> Problem with va_list
    # @staticmethod
    # #the context seems to be an open todo in open62541
    # def stdout_log(level: UaLogLevel, category: UaLogCategory, msg: str, context=ffi.NULL):
    #     # TODO: something like: pass msg as format string and parse to bytestring + va_list
    #     lib.UA_Log_Stdout_log(context, level._val, category._val, UaString(msg)._ptr, ffi.NULL)