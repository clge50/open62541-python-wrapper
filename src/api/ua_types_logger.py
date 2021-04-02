# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_types_generated_structs import *
from ua_types_parent import _ptr, _val


# +++++++++++++++++++ UaLogCategory +++++++++++++++++++++++
class UaLogCategory(UaType):
    val_to_string = dict([
        (0, "UA_LOGCATEGORY_NETWORK"),
        (1, "UA_LOGCATEGORY_SECURECHANNEL"),
        (2, "UA_LOGCATEGORY_SESSION"),
        (3, "UA_LOGCATEGORY_SERVER"),
        (4, "UA_LOGCATEGORY_CLIENT"),
        (5, "UA_LOGCATEGORY_USERLAND"),
        (6, "UA_LOGCATEGORY_SECURITYPOLICY")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_LogCategory*", val._ptr)
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

    @staticmethod
    def NETWORK():
        return UaLogCategory(0)

    @staticmethod
    def SECURECHANNEL():
        return UaLogCategory(1)

    @staticmethod
    def SESSION():
        return UaLogCategory(2)

    @staticmethod
    def SERVER():
        return UaLogCategory(3)

    @staticmethod
    def CLIENT():
        return UaLogCategory(4)

    @staticmethod
    def USERLAND():
        return UaLogCategory(5)

    @staticmethod
    def SECURITYPOLICY():
        return UaLogCategory(6)

    def __str__(self, n=None):
        return f"(UaLogCategory): {self.val_to_string[self._val]} ({str(self._val)})" + ("" if n is None else "\n")


# +++++++++++++++++++ UaLogLevel +++++++++++++++++++++++
class UaLogLevel(UaType):
    val_to_string = dict([
        (0, "UA_LOGLEVEL_TRACE"),
        (1, "UA_LOGLEVEL_DEBUG"),
        (2, "UA_LOGLEVEL_INFO"),
        (3, "UA_LOGLEVEL_WARNING"),
        (4, "UA_LOGLEVEL_ERROR"),
        (5, "UA_LOGLEVEL_FATAL")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_LogLevel*", val._ptr)
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

    @staticmethod
    def TRACE():
        return UaLogLevel(0)

    @staticmethod
    def DEBUG():
        return UaLogLevel(1)

    @staticmethod
    def INFO():
        return UaLogLevel(2)

    @staticmethod
    def WARNING():
        return UaLogLevel(3)

    @staticmethod
    def ERROR():
        return UaLogLevel(4)

    @staticmethod
    def FATAL():
        return UaLogLevel(5)

    def __str__(self, n=None):
        return f"(UaLogLevel): {self.val_to_string[self._val]} ({str(self._val)})" + ("" if n is None else "\n")


# +++++++++++++++++++ UaLogger +++++++++++++++++++++++
class UaLogger(UaType):
    def __init__(self, log_level: UaLogLevel = None, val=lib.UA_Log_Stdout, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Logger*", val._ptr)
        elif log_level is not None:
            val = lib.UA_Log_Stdout_withLevel(log_level._val)
        super().__init__(val=val, is_pointer=is_pointer)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Logger")
        else:
            self._value[0] = _val(val)

    def __str__(self, n=None):
        return "\t" * n + str(self._val)

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
