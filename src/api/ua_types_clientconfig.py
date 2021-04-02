# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_types_logger import *
from ua_types_serverconfig import *
from ua_types_callback import *
from ua_types_parent import _ptr, _val, _is_null, _get_c_type, _is_ptr
from typing import Callable


# +++++++++++++++++++ UaClientConfig +++++++++++++++++++++++
class UaClientConfig(UaType):
    def __init__(self, val=None, is_pointer=False):
        if isinstance(val, UaType):
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
            return "(UaClientConfig) : NULL" + ("" if n is None else "\n")

        return ("(UaClientConfig) :\n" +
                "\t" * (1 if n is None else n+1) + "logger " + self._logger.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "timeout " + self._timeout.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "client_description " + self._client_description.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "user_identity_token " + self._user_identity_token.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "security_mode. " + self._security_mode.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "security_policy_uri " + self._security_policy_uri.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "endpoint " + self._endpoint.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "user_token_policy " + self._user_token_policy.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "secure_channel_life_time " + self._secure_channel_life_time.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "requested_session_timeout " + self._requested_session_timeout.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "connectivity_check_interval " + self._connectivity_check_interval.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "connectivity_check_interval " + self._connectivity_check_interval.__str__(1 if n is None else n+1) +
                "\t" * (1 if n is None else n+1) + "custom_data_types " + self._custom_data_types.__str__(1 if n is None else n+1))
