# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_types_logger import *
from ua_types_parent import _ptr, _val, _is_null, _get_c_type, _is_ptr
from typing import Callable
from ua_consts_status_codes import *


# +++++++++++++++++++ UaValueBackendType +++++++++++++++++++++++
class UaValueBackendType(UaType):
    val_to_string = dict([
        (0, "UA_VALUEBACKENDTYPE_NONE"),
        (1, "UA_VALUEBACKENDTYPE_INTERNAL"),
        (2, "UA_VALUEBACKENDTYPE_DATA_SOURCE_CALLBACK"),
        (3, "UA_VALUEBACKENDTYPE_EXTERNAL")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_ValueBackendType*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_ValueBackendType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_ValueBackendType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_ValueBackendType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def NONE():
        return UaValueBackendType(0)

    @staticmethod
    def INTERNAL():
        return UaValueBackendType(1)

    @staticmethod
    def DATA_SOURCE_CALLBACK():
        return UaValueBackendType(2)

    @staticmethod
    def EXTERNAL():
        return UaValueBackendType(3)

    def __str__(self, n=0):
        return f"(UaValueBackendType): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaValueCallback +++++++++++++++++++++++
class UaValueCallback(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(val=ffi.new("UA_ValueCallback*"), is_pointer=is_pointer)
            self._value[0].onRead = lib.python_wrapper_UA_ValueCallbackOnReadCallback
            self._value[0].onWrite = lib.python_wrapper_UA_ValueCallbackOnWriteCallback
            self._read_callback = lambda a, b, c, d, e, f, g: None
            self._write_callback = lambda a, b, c, d, e, f, g: None
            self._uses_python_read_callback = True
            self._uses_python_write_callback = True
        else:
            super().__init__(val=val, is_pointer=is_pointer)
            self._read_callback = lambda a, b, c, d, e, f, g: None
            self._write_callback = lambda a, b, c, d, e, f, g: None
            self._uses_python_read_callback = False
            self._uses_python_write_callback = False

    @property
    def read_callback(self):
        if self._null:
            return None
        return self._read_callback

    @property
    def write_callback(self):
        if self._null:
            return None
        return self._write_callback

    @property
    def uses_python_read_callback(self):
        return self._uses_python_read_callback

    @property
    def uses_python_write_callback(self):
        return self._uses_python_write_callback

    @read_callback.setter
    def read_callback(self, read_callback: Callable[
        ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNumericRange, UaDataValue], None]):
        self._read_callback = read_callback
        self._value.onRead = lib.python_wrapper_UA_ValueCallbackOnReadCallback
        self._uses_python_read_callback = True

    @write_callback.setter
    def write_callback(self, write_callback: Callable[
        ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNumericRange, UaDataValue], None]):
        self._write_callback = write_callback
        self._value.onWrite = lib.python_wrapper_UA_ValueCallbackOnWriteCallback
        self._uses_python_write_callback = True

    def __str__(self, n=0):
        if self._null:
            return "(UaValueCallback): NULL\n"

        return ("(UaValueCallback):\n" +
                "\t" * (n + 1) + "read_callback" + str(self._read_callback) +
                "\t" * (n + 1) + "write_callback" + str(self._write_callback) + "\n")


class UaValueBackend(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ValueBackend*")
        super().__init__(val=val, is_pointer=is_pointer)
        self._backend_type = UaValueBackendType(val=val.backendType)
        if val.backendType is lib.UA_VALUEBACKENDTYPE_NONE:
            pass
        elif val.backendType is lib.UA_VALUEBACKENDTYPE_INTERNAL:
            self._data_value = UaDataValue(val=val.backend.internal.value)
            self._callback = UaValueCallback(val=val.backend.internal.callback)
            self._data_source = None
        elif val.backendType is lib.UA_VALUEBACKENDTYPE_DATA_SOURCE_CALLBACK:
            self._data_source = UaDataSource(val=val.backend.dataSource)
            self._data_value = None
            self._callback = None
        elif val.backendType is lib.UA_VALUEBACKENDTYPE_EXTERNAL:
            self._data_value = UaDataValue(val=val.backend.external.value[0], is_pointer=True)
            self._callback = UaExternalValueCallback(val=val.backend.external.callback)
            self._data_source = None
            # todo: val.backend.internal.value is **

        else:
            raise ValueError(f"Encoding does not exist.")

    def _update(self):
        self.__init__(val=self._ptr)

    @property
    def backend_type(self):
        if self._null:
            return None
        return self._backend_type

    @property
    def data_value(self):
        if self._null:
            return None
        return self._data_value

    @property
    def callback(self):
        if self._null:
            return None
        return self._callback

    @property
    def data_source(self):
        if self._null:
            return None
        return self._data_source

    def set_none(self):
        self._value = ffi.new("UA_ValueBackend*")
        self._value.backendType = lib.UA_VALUEBACKENDTYPE_NONE

    def set_internal(self, data_value: UaDataValue, callback: UaValueCallback = None):
        self._value = ffi.new("UA_ValueBackend*")
        self._value.backendType = lib.UA_VALUEBACKENDTYPE_INTERNAL
        self._data_value = data_value
        self._value.backend.internal.value = data_value._val
        self._callback = callback
        self._data_source = None
        if callback is not None:
            self._value.backend.internal.callback = callback._val

    def set_external(self, data_value: UaDataValue, callback: 'UaExternalValueCallback' = None):
        self._value = ffi.new("UA_ValueBackend*")
        self._value.backendType = lib.UA_VALUEBACKENDTYPE_EXTERNAL
        self._data_value = data_value
        self._value.backend.external.value = ffi.new("UA_DataValue **", data_value._ptr)
        self._callback = callback
        self._data_source = None
        if callback is not None:
            self._value.backend.external.callback = callback._val

    def set_data_source(self, data_source: 'UaDataSource'):
        self._value = ffi.new("UA_ValueBackend*")
        self._value.backendType = lib.UA_VALUEBACKENDTYPE_DATA_SOURCE_CALLBACK
        self._data_source = data_source
        self._value.backend.dataSource = data_source._val
        self._data_value = None
        self._callback = None

    # todo: check backend type and only print relevant fields
    def __str__(self, n=0):
        if self._null:
            return "(UaValueBackend): NULL\n"

        return ("(UaValueBackend):\n" +
                "\t" * (n + 1) + "backend_type" + str(self._backend_type) +
                "\t" * (n + 1) + "data_value" + str(self._data_value) +
                "\t" * (n + 1) + "callback" + str(self._callback) +
                "\t" * (n + 1) + "data_source" + str(self._data_source) + "\n")


class UaExternalValueCallback(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(val=ffi.new("UA_ExternalValueCallback*"), is_pointer=is_pointer)
            # todo: create callbacks
            self._value[0].onRead = lib.python_wrapper_UA_ExternalValueCallbackNotificationReadCallback
            self._value[0].onWrite = lib.python_wrapper_UA_ExternalValueCallbackUserWriteCallback
            self._read_callback = lambda a, b, c, d, e, f: UA_STATUSCODES.GOOD
            self._write_callback = lambda a, b, c, d, e, f, h: UA_STATUSCODES.GOOD
            self._uses_python_read_callback = True
            self._uses_python_write_callback = True
        else:
            super().__init__(val=val, is_pointer=is_pointer)
            self._read_callback = lambda a, b, c, d, e, f: UA_STATUSCODES.GOOD
            self._write_callback = lambda a, b, c, d, e, f, h: UA_STATUSCODES.GOOD
            self._uses_python_read_callback = False
            self._uses_python_write_callback = False

    @property
    def read_callback(self):
        if self._null:
            return None
        return self._read_callback

    @property
    def write_callback(self):
        if self._null:
            return None
        return self._write_callback

    @read_callback.setter
    def read_callback(self, read_callback: Callable[
        ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNumericRange], UaStatusCode]):
        self._read_callback = read_callback
        self._value.read = lib.python_wrapper_UA_ExternalValueCallbackNotificationReadCallback
        self._uses_python_read_callback = True

    @write_callback.setter
    def write_callback(self, write_callback: Callable[
        ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNumericRange, UaDataValue], UaStatusCode]):
        self._write_callback = write_callback
        self._value.write = lib.python_wrapper_UA_ExternalValueCallbackUserWriteCallback
        self._uses_python_write_callback = True


# +++++++++++++++++++ UaValueBackendType +++++++++++++++++++++++
class UaValueBackendType(UaType):
    val_to_string = dict([
        (0, "UA_VALUEBACKENDTYPE_NONE"),
        (1, "UA_VALUEBACKENDTYPE_INTERNAL"),
        (2, "UA_VALUEBACKENDTYPE_DATA_SOURCE_CALLBACK"),
        (3, "UA_VALUEBACKENDTYPE_EXTERNAL")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_ValueBackendType*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_ValueBackendType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_ValueBackendType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_ValueBackendType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def NONE():
        return UaValueBackendType(0)

    @staticmethod
    def INTERNAL():
        return UaValueBackendType(1)

    @staticmethod
    def DATA_SOURCE_CALLBACK():
        return UaValueBackendType(2)

    @staticmethod
    def EXTERNAL():
        return UaValueBackendType(3)

    def __str__(self, n=0):
        return f"(UaValueBackendType): {self.val_to_string[self._val]} ({str(self._val)})\n"


class UaDataSource(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(val=ffi.new("UA_DataSource*"), is_pointer=is_pointer)
            self._uses_python_read_callback = True
            self._uses_python_write_callback = True
            self._value.read = lib.python_wrapper_UA_DataSourceReadCallback
            self._value.write = lib.python_wrapper_UA_DataSourceWriteCallback
            self._read_callback = lambda a, b, c, d, e, f, g, h: UA_STATUSCODES.GOOD
            self._write_callback = lambda a, b, c, d, e, f, g: UA_STATUSCODES.GOOD
        else:
            super().__init__(val=val, is_pointer=is_pointer)
            self._uses_python_read_callback = False
            self._uses_python_write_callback = False
            self._read_callback = lambda a, b, c, d, e, f, g, h: UA_STATUSCODES.GOOD
            self._write_callback = lambda a, b, c, d, e, f, g: UA_STATUSCODES.GOOD

    @property
    def read_callback(self):
        return self._read_callback

    @property
    def write_callback(self):
        return self._write_callback

    @property
    def uses_python_read_callback(self):
        return self._uses_python_read_callback

    @property
    def uses_python_write_callback(self):
        return self._uses_python_write_callback

    @read_callback.setter
    def read_callback(self, val: Callable[
        ['UaServer', UaNodeId, Void, UaNodeId, Void, UaBoolean, UaNumericRange, UaDataValue], UaStatusCode]):
        self._read_callback = val
        self._value.read = lib.python_wrapper_UA_DataSourceReadCallback
        self._uses_python_read_callback = True

    @write_callback.setter
    def write_callback(self, val: Callable[
        ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNumericRange, UaDataValue], UaStatusCode]):
        self._write_callback = val
        self._value.write = lib.python_wrapper_UA_DataSourceWriteCallback
        self._uses_python_write_callback = True

    def __str__(self, n=0):
        if self._null:
            return "(UA_DataSource) : NULL\n"

        return ("(UA_DataSource) :\n" +
                "\t" * (n + 1) + "read_callback" + str(self._read_callback) +
                "\t" * (n + 1) + "write_callback" + str(self._write_callback) + "\n")


class UaNodeTypeLifecycle():
    def __init__(self):
        pass
