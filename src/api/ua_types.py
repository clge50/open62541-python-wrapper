# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_types_logger import *
from ua_types_parent import _ptr, _val, _is_null
from typing import Callable


# +++++++++++++++++++ UaClientConfig +++++++++++++++++++++++
class UaClientConfig(UaType):
    def __init__(self, val=None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_ClientConfig*", val._ptr)
        if val is None:
            val = ffi.new("UA_ClientConfig*")
            lib.UA_ClientConfig_setDefault(val)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._client_context = Void(val=val.clientContext, is_pointer=True)
            self._logger = UaLogger(val=val.logger, is_pointer=False)
            self._timeout = UaUInt32(val=val.timeout, is_pointer=False)
            self._client_description = UaUInt32(val=val.clientDescription, is_pointer=False)
            self._user_identity_token = UaUserIdentityToken(val=val.userIdentityToken, is_pointer=False)
            self._security_mode = UaMessageSecurityMode(val=val.securityMode, is_pointer=False)
            self._security_policy_uri = UaString(val=val.securityPolicyUri, is_pointer=False)
            self._endpoint = UaEndpointDescription(val=val.endpoint, is_pointer=False)
            self._user_token_policy = UaUserTokenPolicy(val=val.userTokenPolicy, is_pointer=False)
            self._secure_channel_life_time = UaUInt32(val=val.secureChannelLifeTime, is_pointer=False)
            self._requested_session_timeout = UaUInt32(val=val.requestedSessionTimeout, is_pointer=False)
            self._connectivity_check_interval = UaUInt32(val=val.connectivityCheckInterval, is_pointer=False)
            self._custom_data_types = UaDataTypeArray(val=val.customDataTypes, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ClientConfig")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._client_context = val.clientContext
            self._logger._value[0] = _val(val.logger)
            self._timeout._value[0] = _val(val.timeout)
            self._client_description._value[0] = _val(val.clientDescription)
            self._user_identity_token._value[0] = _val(val.userIdentityToken)
            self._security_mode._value[0] = _val(val.securityMode)
            self._security_policy_uri._value[0] = _val(val.securityPolicyUri)
            self._endpoint._value[0] = _val(val.endpoint)
            self._user_token_policy._value[0] = _val(val.userTokenPolicy)
            self._secure_channel_life_time._value[0] = _val(val.secureChannelLifeTime)
            self._requested_session_timeout._value[0] = _val(val.requestedSessionTimeout)
            self._connectivity_check_interval._value[0] = _val(val.connectivityCheckInterval)
            self._custom_data_types = val.customDataTypes

    @property
    def client_context(self):
        if self._null:
            return None
        else:
            return self._client_context

    @property
    def logger(self):
        if self._null:
            return None
        else:
            return self._logger

    @property
    def timeout(self):
        if self._null:
            return None
        else:
            return self._timeout

    @property
    def client_description(self):
        if self._null:
            return None
        else:
            return self._client_description

    @property
    def user_identity_token(self):
        if self._null:
            return None
        else:
            return self._user_identity_token

    @property
    def security_mode(self):
        if self._null:
            return None
        else:
            return self.security_mode

    @property
    def security_policy_uri(self):
        if self._null:
            return None
        else:
            return self._security_policy_uri

    @property
    def endpoint(self):
        if self._null:
            return None
        else:
            return self._endpoint

    @property
    def user_token_policy(self):
        if self._null:
            return None
        else:
            return self._user_token_policy

    @property
    def secure_channel_life_time(self):
        if self._null:
            return None
        else:
            return self._secure_channel_life_time

    @property
    def requested_session_timeout(self):
        if self._null:
            return None
        else:
            return self._requested_session_timeout

    @property
    def connectivity_check_interval(self):
        if self._null:
            return None
        else:
            return self._connectivity_check_interval

    @property
    def custom_data_types(self):
        if self._null:
            return None
        else:
            return self._custom_data_types

    @client_context.setter
    def client_context(self, val: Void):
        self._client_context = val
        self._value.clientContext = val._ptr

    @logger.setter
    def logger(self, val: UaSimpleAttributeOperand):
        self._logger = val
        self._value.logger = val._val

    @timeout.setter
    def timeout(self, val: UaUInt32):
        self._timeout = val
        self._value.timeout = val._val

    @client_description.setter
    def client_description(self, val: UaUInt32):
        self._client_description = val
        self._value.clientDescription = val._val

    @user_identity_token.setter
    def user_identity_token(self, val: UaUserIdentityToken):
        self._user_identity_token = val
        self._value.userIdentityToken = val._val

    @security_mode.setter
    def security_mode(self, val: UaMessageSecurityMode):
        self._security_mode = val
        self._value.securityMode = val._val

    @security_policy_uri.setter
    def security_policy_uri(self, val: UaString):
        self._security_policy_uri = val
        self._value.securityPolicyUri = val._val

    @endpoint.setter
    def endpoint(self, val: UaEndpointDescription):
        self._endpoint = val
        self._value.endpoint = val._val

    @user_token_policy.setter
    def user_token_policy(self, val: UaUserTokenPolicy):
        self._user_token_policy = val
        self._value.userTokenPolicy = val._val

    @secure_channel_life_time.setter
    def secure_channel_life_time(self, val: UaUInt32):
        self.secure_channel_life_time = val
        self._value.secureChannelLifeTime = val._val

    @requested_session_timeout.setter
    def requested_session_timeout(self, val: UaUInt32):
        self._requested_session_timeout = val
        self._value.requestedSessionTimeout = val._val

    @connectivity_check_interval.setter
    def connectivity_check_interval(self, val: UaUInt32):
        self._connectivity_check_interval = val
        self._value.connectivityCheckInterval = val._val

    @custom_data_types.setter
    def custom_data_types(self, val: UaDataTypeArray):
        self._custom_data_types = val
        self._value.customDataTypes = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaClientConfig) : NULL\n"

        return ("(UaClientConfig) :\n" +
                "\t" * (n + 1) + "logger" + self._logger.__str__(n + 1) +
                "\t" * (n + 1) + "timeout" + self._timeout.__str__(n + 1) +
                "\t" * (n + 1) + "client_description" + self._client_description.__str__(n + 1) +
                "\t" * (n + 1) + "user_identity_token" + self._user_identity_token.__str__(n + 1) +
                "\t" * (n + 1) + "security_mode." + self._security_mode.__str__(n + 1) +
                "\t" * (n + 1) + "security_policy_uri" + self._security_policy_uri.__str__(n + 1) +
                "\t" * (n + 1) + "endpoint" + self._endpoint.__str__(n + 1) +
                "\t" * (n + 1) + "user_token_policy" + self._user_token_policy.__str__(n + 1) +
                "\t" * (n + 1) + "secure_channel_life_time" + self._secure_channel_life_time.__str__(n + 1) +
                "\t" * (n + 1) + "requested_session_timeout" + self._requested_session_timeout.__str__(n + 1) +
                "\t" * (n + 1) + "connectivity_check_interval" + self._connectivity_check_interval.__str__(n + 1) +
                "\t" * (n + 1) + "connectivity_check_interval" + self._connectivity_check_interval.__str__(n + 1) +
                "\t" * (n + 1) + "custom_data_types" + self._custom_data_types.__str__(n + 1))


# ++++++++++++++++++++ protos +++++++++++++++++++++++

class UaValueCallback(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(val=ffi.new("UA_ValueCallback*"), is_pointer=is_pointer)
            self._value[0].onRead = lib.python_wrapper_UA_ValueCallbackOnReadCallback
            self._value[0].onWrite = lib.python_wrapper_UA_ValueCallbackOnWriteCallback
            self.read_callback = lambda a, b, c, d, e, f, g: None
            self.write_callback = lambda a, b, c, d, e, f, g: None
            self._uses_python_read_callback = True
            self._uses_python_write_callback = True
        else:
            super().__init__(val=val, is_pointer=is_pointer)
            self.read_callback = None
            self.write_callback = None
            self._uses_python_read_callback = False
            self._uses_python_write_callback = False

    @property
    def read_callback(self):
        if self._null:
            return None
        return self.read_callback

    @property
    def write_callback(self):
        if self._null:
            return None
        return self.write_callback

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
                "\t" * (n + 1) + "read_callback" + str(self.read_callback) +
                "\t" * (n + 1) + "write_callback" + str(self.write_callback) + "\n")


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
            self.read_callback = lambda a, b, c, d, e, f: UaStatusCode.UA_STATUSCODE_GOOD
            self.write_callback = lambda a, b, c, d, e, f, h: UaStatusCode.UA_STATUSCODE_GOOD
            self._uses_python_read_callback = True
            self._uses_python_write_callback = True
        else:
            super().__init__(val=val, is_pointer=is_pointer)
            self.read_callback = None
            self.write_callback = None
            self._uses_python_read_callback = False
            self._uses_python_write_callback = False

    @property
    def read_callback(self):
        if self._null:
            return None
        return self.read_callback

    @property
    def write_callback(self):
        if self._null:
            return None
        return self.write_callback

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


class UaValueBackendType(UaType):
    UA_VALUEBACKENDTYPE_NONE = 0
    UA_VALUEBACKENDTYPE_INTERNAL = 1
    UA_VALUEBACKENDTYPE_DATA_SOURCE_CALLBACK = 2
    UA_VALUEBACKENDTYPE_EXTERNAL = 3

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
            self._read_callback = lambda a, b, c, d, e, f, g, h: UaStatusCode.UA_STATUSCODE_GOOD
            self._write_callback = lambda a, b, c, d, e, f, g: UaStatusCode.UA_STATUSCODE_GOOD
        else:
            super().__init__(val=val, is_pointer=is_pointer)
            self._uses_python_read_callback = False
            self._uses_python_write_callback = False
            self._value.read = val.read
            self._value.write = val.write
            self._read_callback = None
            self._write_callback = None

    @property
    def read_callback(self):
        return self._read_callback

    @property
    def write_callback(self):
        return self._write_callback

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


class UaTwoStateVariableCallbackType(UaType):
    def __init__(self):
        return None


class UaTwoStateVariableChangeCallback(UaType):
    def __init__(self):
        return None
