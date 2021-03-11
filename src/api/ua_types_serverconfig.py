# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_types_logger import *
from ua_types_parent import _ptr, _val, _is_null, _get_c_type, _is_ptr
from typing import Callable


# +++++++++++++++++++ UaConnectionConfig +++++++++++++++++++++++
class UaConnectionConfig(UaType):
    def __init__(self, val=None, is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        if not self._null:
            self._protocol_version = UaUInt32(val=val.protocol_version, is_pointer=False)
            self._recv_buffer_size = UaUInt32(val=val.recv_buffer_size, is_pointer=False)
            self._send_buffer_size = UaUInt32(val=val.send_buffer_size, is_pointer=False)
            self._local_max_message_size = UaUInt32(val=val.local_max_message_size, is_pointer=False)
            self._remote_max_message_size = UaUInt32(val=val.remote_max_message_size, is_pointer=False)
            self._local_max_chunk_count = UaUInt32(val=val.local_max_chunk_count, is_pointer=False)
            self._remote_max_chunk_count = UaUInt32(val=val.remote_max_chunk_count, is_pointer=False)

    @property
    def protocol_version(self):
        if self._null:
            return None
        else:
            return self._protocol_version

    @property
    def recv_buffer_size(self):
        if self._null:
            return None
        else:
            return self._recv_buffer_size

    @property
    def send_buffer_size(self):
        if self._null:
            return None
        else:
            return self._send_buffer_size

    @property
    def local_max_message_size(self):
        if self._null:
            return None
        else:
            return self._local_max_message_size

    @property
    def remote_max_message_size(self):
        if self._null:
            return None
        else:
            return self._remote_max_message_size

    @property
    def local_max_chunk_count(self):
        if self._null:
            return None
        else:
            return self._local_max_chunk_count

    @property
    def remote_max_chunk_count(self):
        if self._null:
            return None
        else:
            return self._remote_max_chunk_count


# +++++++++++++++++++ UaServerNetworkLayer +++++++++++++++++++++++
class UaSecurityPolicy(UaType):
    def __init__(self, val=None, is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        if not self._null:
            self._policy_context = Void(val=val.policy_context, is_pointer=True)
            self._policy_url = UaByteString(val=val.policy_url, is_pointer=False)
            self._local_certificate = UaByteString(val=val.local_certificate, is_pointer=False)
            self._asymmetric_module = UaSecurityPolicyAsymmetricModule(val=val.asymmetric_module, is_pointer=False)
            self._symmetric_module = UaSecurityPolicySymmetricModule(val=val.symmetric_module, is_pointer=False)
            self._certificate_signing_algorithm = UaSecurityPolicySignatureAlgorithm(
                val=val.certificate_signing_algorithm, is_pointer=False)
            self._channel_module = UaSecurityPolicyChannelModule(val=val.channel_module, is_pointer=False)
            self._logger = UaLogger(val=val.logger, is_pointer=True)
            self._update_certificate_and_private_key = UaStatusCode(
                val=val.UaSecurityPolicy(val=val.update_certificate_and_private_key, is_pointer=True), is_pointer=False)
            self._clear = Void(val=val.UaSecurityPolicy(val=val.clear, is_pointer=True), is_pointer=False)

    @property
    def policy_context(self):
        if self._null:
            return None
        else:
            return self._policy_context

    @property
    def policy_url(self):
        if self._null:
            return None
        else:
            return self._policy_url

    @property
    def local_certificate(self):
        if self._null:
            return None
        else:
            return self._local_certificate

    @property
    def asymmetric_module(self):
        if self._null:
            return None
        else:
            return self._asymmetric_module

    @property
    def symmetric_module(self):
        if self._null:
            return None
        else:
            return self._symmetric_module

    @property
    def certificate_signing_algorithm(self):
        if self._null:
            return None
        else:
            return self._certificate_signing_algorithm

    @property
    def channel_module(self):
        if self._null:
            return None
        else:
            return self._channel_module

    @property
    def logger(self):
        if self._null:
            return None
        else:
            return self._logger

    @property
    def update_certificate_and_private_key(self):
        if self._null:
            return None
        else:
            return self._update_certificate_and_private_key

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear


# +++++++++++++++++++ UaServerNetworkLayer +++++++++++++++++++++++
class UaServerNetworkLayer(UaType):
    def __init__(self, val=None, is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        if not self._null:
            self._handle = Void(val=val.handle, is_pointer=True)
            self._statistics = UaNetworkStatistics(val=val.statistics, is_pointer=True)
            self._discovery_url = UaString(val=val.discovery_url, is_pointer=False)
            self._local_connection_config = UaConnectionConfig(val=val.local_connection_config, is_pointer=False)
            self._start = UaStatusCode(val=val.UaServerNetworkLayer(val=val.start, is_pointer=True), is_pointer=False)
            self._listen = UaStatusCode(val=val.UaServerNetworkLayer(val=val.listen, is_pointer=True), is_pointer=False)
            self._stop = Void(UaServerNetworkLayer(val=val.stop, is_pointer=True), is_pointer=False)
            self._clear = Void(UaServerNetworkLayer(val=val.clear, is_pointer=True), is_pointer=False)

    @property
    def handle(self):
        if self._null:
            return None
        else:
            return self._handle

    @property
    def statistics(self):
        if self._null:
            return None
        else:
            return self._statistics

    @property
    def discovery_url(self):
        if self._null:
            return None
        else:
            return self._discovery_url

    @property
    def local_connection_config(self):
        if self._null:
            return None
        else:
            return self._local_connection_config

    @property
    def start(self):
        if self._null:
            return None
        else:
            return self._start

    @property
    def listen(self):
        if self._null:
            return None
        else:
            return self._listen

    @property
    def stop(self):
        if self._null:
            return None
        else:
            return self._stop

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear


# +++++++++++++++++++ UaGlobalNodeLifecycle +++++++++++++++++++++++
class UaGlobalNodeLifecycle(UaType):
    def __init__(self, val=None, is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        if not self._null:
            self._constructor = UaStatusCode(val=val.UaGlobalNodeLifecycle(val=val.costructor, is_pointer=True),
                                             is_pointer=False)
            self._destructor = Void(val=val.UaGlobalNodeLifecycle(val=val.destructor, is_pointer=True),
                                    is_pointer=False)
            self._create_optional_child = UaBoolean(
                val=val.UaGlobalNodeLifecycle(val=val.create_optional_child, is_pointer=True), is_pointer=False)
            self._generate_child_node_id = UaStatusCode(
                val=val.UaGlobalNodeLifecycle(val=val.generate_child_node_id, is_pointer=True), is_pointer=False)

    @property
    def constructor(self):
        if self._null:
            return None
        else:
            return self._constructor

    @property
    def destructor(self):
        if self._null:
            return None
        else:
            return self._destructor

    @property
    def create_optional_child(self):
        if self._null:
            return None
        else:
            return self._create_optional_child

    @property
    def generate_child_node_id(self):
        if self._null:
            return None
        else:
            return self._generate_child_node_id


# +++++++++++++++++++ UaNode +++++++++++++++++++++++
class UaNode(UaType):
    # TODO: add union members

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Node *"), is_pointer)
        else:
            super().__init__(ffi.new("UA_Node *"), _val(val), is_pointer)


# +++++++++++++++++++ UaNodestore +++++++++++++++++++++++
class UaNodestore(UaType):
    def __init__(self, val=None, is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._context = Void(val=val.context, is_pointer=True)
            self._clear = Void(val=val.UaAccessControl(val=val.clear, is_pointer=True), is_pointer=False)
            self._new_node = UaNode(val=val.UaNodestore(val=val.new_node, is_pointer=True), is_pointer=True)
            self._delete_node = Void(val=val.UaNodestore(val=val.delete_node, is_pointer=True), is_pointer=False)
            self._get_node = UaNode(val=val.UaNodestore(val=val.get_node, is_pointer=True), is_pointer=True)
            self._release_node = Void(val=val.UaNodestore(val=val.release_node, is_pointer=True), is_pointer=False)
            self._get_node_copy = UaStatusCode(val=val.UaNodestore(val=val.get_node_copy, is_pointer=True),
                                               is_pointer=False)
            self._insert_node = UaStatusCode(val=val.UaNodestore(val=val.insert_node, is_pointer=True),
                                             is_pointer=False)
            self._replace_node = UaStatusCode(val=val.UaNodestore(val=val.replace_node, is_pointer=True),
                                              is_pointer=False)
            self._remove_node = UaStatusCode(val=val.UaNodestore(val=val.remove_node, is_pointer=True),
                                             is_pointer=False)
            self._get_reference_type_id = UaNodeId(val=val.UaNodestore(val=val.get_reference_type_id, is_pointer=True),
                                                   is_pointer=True)
            self._iterate = Void(val=val.UaNodestore(val=val.iterate, is_pointer=True), is_pointer=False)

    @property
    def context(self):
        if self._null:
            return None
        else:
            return self._context

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear

    @property
    def new_node(self):
        if self._null:
            return None
        else:
            return self._new_node

    @property
    def delete_node(self):
        if self._null:
            return None
        else:
            return self._delete_node

    @property
    def get_node(self):
        if self._null:
            return None
        else:
            return self._get_node

    @property
    def release_node(self):
        if self._null:
            return None
        else:
            return self._release_node

    @property
    def get_node_copy(self):
        if self._null:
            return None
        else:
            return self._get_node_copy

    @property
    def insert_node(self):
        if self._null:
            return None
        else:
            return self._insert_node

    @property
    def replace_node(self):
        if self._null:
            return None
        else:
            return self._replace_node

    @property
    def remove_node(self):
        if self._null:
            return None
        else:
            return self._remove_node

    @property
    def get_reference_type_id(self):
        if self._null:
            return None
        else:
            return self._get_reference_type_id

    @property
    def iterate(self):
        if self._null:
            return None
        else:
            return self._iterate


# +++++++++++++++++++ UaCertificateVerification +++++++++++++++++++++++
class UaCertificateVerification(UaType):
    def __init__(self, val=None, is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._context = Void(val=val.context, is_pointer=True)
            self._verify_certificate = UaStatusCode(
                val=val.UaCertificateVerification(val=val.verify_certificate, is_pointer=True), is_pointer=False)
            self._verify_application_uri = UaStatusCode(
                val=val.UaCertificateVerification(val=val.verify_application_uri, is_pointer=True), is_pointer=False)
            self._clear = Void(val=val.UaAccessCertificateVerification(val=val.clear, is_pointer=True), is_pointer=False)

    @property
    def context(self):
        if self._null:
            return None
        else:
            return self._context

    @property
    def verify_certificate(self):
        if self._null:
            return None
        else:
            return self._verify_certificate

    @property
    def verify_application_uri(self):
        if self._null:
            return None
        else:
            return self._verify_application_uri

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear


# +++++++++++++++++++ UaAccessControl +++++++++++++++++++++++
class UaAccessControl(UaType):
    def __init__(self, val=None, is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._context = Void(val=val.context, is_pointer=True)
            self._clear = Void(val=val.UaAccessControl(val=val.clear, is_pointer=True), is_pointer=False)
            self._user_token_policy_size = SizeT(val=val.user_token_policy_size, is_pointer=False)
            self._user_token_policies = UaUserTokenPolicy(val=val.user_token_policies, is_pointer=True)
            self._activate_session = UaStatusCode(val=val.UaAccessControl(val=val.activate_session, is_pointer=True),
                                                  is_pointer=False)
            self._close_session = Void(val=val.UaAccessControl(val=val.close_session, is_pointer=True),
                                       is_pointer=False)

            self._get_user_rights_mask = UaUInt32(
                val=val.UaAccessControl(val=val.get_user_rights_mask, is_pointer=True),
                is_pointer=False)
            self._get_user_access_level = UaByte(
                val=val.UaAccessControl(val=val.get_user_access_level, is_pointer=True),
                is_pointer=False)
            self._get_user_executable = UaBoolean(val=val.UaAccessControl(val=val.get_user_executable, is_pointer=True),
                                                  is_pointer=False)
            self._get_user_executable_on_object = UaBoolean(
                val=val.UaAccessControl(val=val.get_user_executable_on_object, is_pointer=True),
                is_pointer=False)
            self._allow_add_node = UaBoolean(val=val.UaAccessControl(val=val.allow_add_node, is_pointer=True),
                                             is_pointer=False)
            self._allow_add_reference = UaBoolean(val=val.UaAccessControl(val=val.allow_add_reference, is_pointer=True),
                                                  is_pointer=False)
            self._allow_delete_node = UaBoolean(val=val.UaAccessControl(val=val.allow_delete_node, is_pointer=True),
                                                is_pointer=False)
            self._allow_delete_reference = UaBoolean(
                val=val.UaAccessControl(val=val.allow_delete_reference, is_pointer=True),
                is_pointer=False)
            self._allow_browse_node = UaBoolean(val=val.UaAccessControl(val=val.allow_browse_node, is_pointer=True),
                                                is_pointer=False)

            # if UA_ENABLE_SUBSCRIPTIONS:
            #    self._allow_transfer_subscription = UaBoolean(
            #        val=val.UaAccessControl(val=val.allow_transfer_subscription, is_pointer=True),
            #        is_pointer=False)
            # @property
            # def allow_transfer_subscription(self):
            #     if self._null:
            #         return None
            #     else:
            #         return self._allow_transfer_subscription

            # if UA_ENABLE_HISTORIZING:
            #   self._allow_history_update_update_data = UaBoolean(val=val.UaAccessControl(val=val.allow_history_update_update_data, is_pointer=True),
            #                                                   is_pointer=False)
            #   self._allow_history_update_delete_raw_modified = UaBoolean(val=val.UaAccessControl(val=val.allow_history_update_delete_raw_modified, is_pointer=True),
            #                                                   is_pointer=False)
            #
            # @property
            #   def allow_history_update_update_data(self):
            #       if self._null:
            #           return None
            #       else:
            #           return self._allow_history_update_update_data
            #
            # @property
            #   def allow_history_update_delete_raw_modified(self):
            #       if self._null:
            #           return None
            #       else:
            #           return self._allow_history_update_delete_raw_modified
            #

    @property
    def context(self):
        if self._null:
            return None
        else:
            return self._context

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear

    @property
    def user_token_policy_size(self):
        if self._null:
            return None
        else:
            return self._user_token_policy_size

    @property
    def user_token_policies(self):
        if self._null:
            return None
        else:
            return self._user_token_policies

    @property
    def activate_session(self):
        if self._null:
            return None
        else:
            return self._activate_session

    @property
    def close_session(self):
        if self._null:
            return None
        else:
            return self._close_session

    @property
    def get_user_rights_mask(self):
        if self._null:
            return None
        else:
            return self._get_user_rights_mask

    @property
    def get_user_access_level(self):
        if self._null:
            return None
        else:
            return self.get_user_access_level

    @property
    def get_user_executable(self):
        if self._null:
            return None
        else:
            return self._get_user_executable

    @property
    def get_user_executable_on_object(self):
        if self._null:
            return None
        else:
            return self._get_user_executable_on_object

    @property
    def allow_add_node(self):
        if self._null:
            return None
        else:
            return self._allow_add_node

    @property
    def allow_add_reference(self):
        if self._null:
            return None
        else:
            return self._allow_add_reference

    @property
    def allow_delete_node(self):
        if self._null:
            return None
        else:
            return self._allow_delete_node

    @property
    def allow_delete_reference(self):
        if self._null:
            return None
        else:
            return self._allow_delete_reference

    @property
    def allow_browse_node(self):
        if self._null:
            return None
        else:
            return self._allow_browse_node


# +++++++++++++++++++ UaServerConfig +++++++++++++++++++++++
class UaServerConfig(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ServerConfig*")
            lib.UA_ServerConfig_setDefault(val)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._logger = UaSimpleAttributeOperand(val=val.logger, is_pointer=False)
            self._build_info = UaBuildInfo(val=val.build_info, is_pointer=False)
            self._app_description = UaApplicationDescription(val=val.app_description, is_pointer=False)
            self._server_cert = UaByteString(val=val.server_cert, is_pointer=False)
            self._shutdown_delay = UaDouble(val=val.shutdown_delay, is_pointer=False)
            self._verify_req_timestamp = UaRuleHandling(val=val.verify_req_timestamp, is_pointer=False)
            self._allow_empty_vars = UaRuleHandling(val=val.allow_empty_vars, is_pointer=False)
            self._custom_data_types = UaDataTypeArray(val=val.custom_data_types, is_pointer=True)

            self._network_layer_size = SizeT(val=val.network_layer_size, is_pointer=False)
            self._network_layers = UaServerNetworkLayer(val=val.network_layers, is_pointer=True)
            self._custom_hostname = UaString(val=val.custom_hostname, is_pointer=False)

            self._security_policies_size = SizeT(val=val.security_policies_size, is_pointer=False)
            self._security_policy = UaSecurityPolicy(val=val.security_policy, is_pointer=True)

            self._endpoints_size = SizeT(val=val.endpoints_size, is_pointer=False)
            self._endpoints = UaEndpointDescription(val=val.endpoints, is_pointer=True)
            self._security_policy_none_discovery_only = UaBoolean(val=val.security_policy_none_iscovery_only,
                                                                  is_pointer=False)
            self._node_lifecycle = UaGlobalNodeLifecycle(val=val.node_lifecycle, is_pointer=False)
            self._access_control = UaAccessControl(val=val.access_control, is_pointer=False)

            self._nodestore = UaNodestore(val=val.nodestore, is_pointer=False)

            self._certificate_verification = UaCertificateVerification(val=val.certificate_verification,
                                                                       is_pointer=False)

            self._max_security_channels = UaUInt16(val=val.max_security_channels, is_pointer=False)
            self._max_security_token_lifetime = UaUInt32(val=val.max_security_token_lifetime, is_pointer=False)

            self._max_nodes_per_read = UaUInt32(val=val.max_nodes_per_read, is_pointer=False)
            self._max_nodes_per_write = UaUInt32(val=val.max_nodes_per_write, is_pointer=False)
            self._max_nodes_per_method_call = UaUInt32(val=val.max_nodes_per_method_call, is_pointer=False)
            self._max_nodes_per_browse = UaUInt32(val=val.max_nodes_per_browse, is_pointer=False)
            self._max_nodes_per_register_nodes = UaUInt32(val=val.max_nodes_per_register_nodes, is_pointer=False)
            self._max_nodes_per_translate_browse_paths_to_node_ids = \
                UaUInt32(val=val.max_nodes_per_translate_browse_paths_to_node_ids, is_pointer=False)
            self._max_nodes_per_node_management = UaUInt32(val=val.max_nodes_per_node_management, is_pointer=False)
            self._max_monitored_items_per_call = UaUInt32(val=val.max_monitored_items_per_call, is_pointer=False)
            self._max_references_per_node = UaUInt32(val=val.max_references_per_node, is_pointer=False)

            self._max_monitored_items = UaUInt32(val=val.max_monitored_items, is_pointer=False)
            self._max_monitored_items_per_subscription = UaUInt32(val=val.max_monitored_items_per_subscription,
                                                                  is_pointer=False)

            self._sampling_interval_limits = UaDurationRange(val=val.sampling_interval_limits, is_pointer=False)
            self._queue_size_limits = UaUInt32Range(val=val.queue_size_limits, is_pointer=False)
            self._max_publish_req_per_session = UaUInt32(val=val.max_publish_req_per_session, is_pointer=False)

            # if UA_ENABLE_SUBSCRIPTIONS:
            #    self._max_subscriptions = UaUInt32(val=val.max_subscriptions, is_pointer=False)
            #    self._max_subscriptions_per_session = UaUInt32(val=val.max_subscriptions_per_session, is_pointer=False)
            #    self._publishing_interval_limits = UaDurationRange(val=val.publishing_interval_limits, is_pointer=False)
            #    self._life_time_counter_limits = UaUInt32Range(val=val.life_time_counter_limits, is_pointer=False)
            #    self._keep_alive_count_limits = UaUInt32Range(val=val.keep_alive_count_limits, is_pointer=False)
            #    self._max_notifications_per_publish = UaUInt32(val=val.max_notifications_per_publish, is_pointer=False)
            #    self._enable_retransmission_queue = UaBoolean(val=val.enable_retransmission_queue, is_pointer=False)
            #    self._max_retransmission_queue_size = UaUInt32(val=val.max_retransmission_queue_size, is_pointer=False)

            self._max_monitored_item_register_callback = UaServerConfig(val=val.max_monitored_item_register_callback,
                                                                        is_pointer=True)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ServerConfig")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._logger._value[0] = _val(val.logger)
            self._build_info._value[0] = _val(val.build_info)
            self._app_description._value[0] = _val(val.app_description)
            self._server_cert._value[0] = _val(val.server_cert)
            self._shutdown_delay._value[0] = _val(val.shutdown_delay)
            self._verify_req_timestamp._value[0] = _val(val.verify_req_timestamp)
            self._allow_empty_vars._value[0] = _val(val.allow_empty_vars)
            self._custom_data_types._value = _val(val.custom_data_types)

            self._network_layer_size._value[0] = _val(val.network_layer_size)
            self._network_layers._value._value[0] = _val(val.network_layers)
            self._custom_hostname._value[0] = _val(val.custom_hostname)

            self._security_policies_size._value[0] = _val(val.security_policies_size)
            self._security_policy._value = _val(val.security_policy)

            self._endpoints_size._value[0] = _val(val.endpoints_size)
            self._endpoints._value = _val(val.endpoints)
            self._security_policy_none_discovery_only._value[0] = _val(val.security_policy_none_iscovery_only)
            self._node_lifecycle._value[0] = _val(val.node_lifecycle)
            self._access_control._value[0] = _val(val.access_control)

            self._nodestore._value[0] = _val(val.nodestore)

            self._certificate_verification._value[0] = _val(val.certificate_verification)

            self._max_security_channels._value[0] = _val(val.max_security_channels)
            self._max_security_token_lifetime._value[0] = _val(val.max_security_token_lifetime)

            self._max_nodes_per_read._value[0] = _val(val.max_nodes_per_read)
            self._max_nodes_per_write._value[0] = _val(val.max_nodes_per_write)
            self._max_nodes_per_method_call._value[0] = _val(val.max_nodes_per_method_call)
            self._max_nodes_per_browse._value[0] = _val(val.max_nodes_per_browse)
            self._max_nodes_per_register_nodes._value[0] = _val(val.max_nodes_per_register_nodes)
            self._max_nodes_per_translate_browse_paths_to_node_ids._value[0] = _val(val.max_nodes_per_translate_browse_paths_to_node_ids)
            self._max_nodes_per_node_management._value[0] = _val(val.max_nodes_per_node_management)
            self._max_monitored_items_per_call._value[0] = _val(val.max_monitored_items_per_call)
            self._max_references_per_node._value[0] = _val(val.max_references_per_node)

            self._max_monitored_items._value[0] = _val(val.max_monitored_items)
            self._max_monitored_items_per_subscription._value[0] = _val(val.max_monitored_items_per_subscription)

            self._sampling_interval_limits._value[0] = _val(val.sampling_interval_limits)
            self._queue_size_limits._value[0] = _val(val.queue_size_limits)
            self._max_publish_req_per_session._value[0] = _val(val.max_publish_req_per_session)

            self._max_monitored_item_register_callback._value = _val(val.max_monitored_item_register_callback)


    @property
    def logger(self):
        if self._null:
            return None
        else:
            return self._logger

    @property
    def build_info(self):
        if self._null:
            return None
        else:
            return self._build_info

    @property
    def app_description(self):
        if self._null:
            return None
        else:
            return self._app_description

    @property
    def server_cert(self):
        if self._null:
            return None
        else:
            return self._server_cert

    @property
    def shutdown_delay(self):
        if self._null:
            return None
        else:
            return self._shutdown_delay

    @property
    def verify_req_timestamp(self):
        if self._null:
            return None
        else:
            return self._verify_req_timestamp

    @property
    def allow_empty_vars(self):
        if self._null:
            return None
        else:
            return self._allow_empty_vars

    @property
    def custom_data_types(self):
        if self._null:
            return None
        else:
            return self._custom_data_types

    @property
    def network_layer_size(self):
        if self._null:
            return None
        else:
            return self._network_layer_size

    @property
    def network_layers(self):
        if self._null:
            return None
        else:
            return self._network_layers

    @property
    def custom_hostname(self):
        if self._null:
            return None
        else:
            return self._custom_hostname

    @property
    def security_policies_size(self):
        if self._null:
            return None
        else:
            return self._security_policies_size

    @property
    def security_policy(self):
        if self._null:
            return None
        else:
            return self._security_policy

    @property
    def endpoints_size(self):
        if self._null:
            return None
        else:
            return self._endpoints_size

    @property
    def endpoints(self):
        if self._null:
            return None
        else:
            return self._endpoints

    @property
    def security_policy_none_discovery_only(self):
        if self._null:
            return None
        else:
            return self._security_policy_none_discovery_only

    @property
    def node_lifecycle(self):
        if self._null:
            return None
        else:
            return self._node_lifecycle

    @property
    def access_control(self):
        if self._null:
            return None
        else:
            return self._access_control

    @property
    def nodestore(self):
        if self._null:
            return None
        else:
            return self._nodestore

    @property
    def certificate_verification(self):
        if self._null:
            return None
        else:
            return self._certificate_verification

    @property
    def max_security_channels(self):
        if self._null:
            return None
        else:
            return self._max_security_channels

    @property
    def max_security_token_lifetime(self):
        if self._null:
            return None
        else:
            return self._max_security_token_lifetime

    @property
    def max_nodes_per_read(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_read

    @property
    def max_nodes_per_write(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_write

    @property
    def max_nodes_per_method_call(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_method_call

    @property
    def max_nodes_per_browse(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_browse

    @property
    def max_nodes_per_register_nodes(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_register_nodes

    @property
    def max_nodes_per_translate_browse_paths_to_node_ids(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_translate_browse_paths_to_node_ids

    @property
    def max_nodes_per_node_management(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_node_management

    @property
    def max_monitored_items_per_call(self):
        if self._null:
            return None
        else:
            return self._max_monitored_items_per_call

    @property
    def max_references_per_node(self):
        if self._null:
            return None
        else:
            return self._max_references_per_node

    @property
    def max_monitored_items(self):
        if self._null:
            return None
        else:
            return self._max_monitored_items

    @property
    def max_monitored_items_per_subscription(self):
        if self._null:
            return None
        else:
            return self._max_monitored_items_per_subscription

    @property
    def sampling_interval_limits(self):
        if self._null:
            return None
        else:
            return self._sampling_interval_limits

    @property
    def queue_size_limits(self):
        if self._null:
            return None
        else:
            return self._queue_size_limits

    @property
    def max_publish_req_per_session(self):
        if self._null:
            return None
        else:
            return self._max_publish_req_per_session

    @property
    def max_monitored_item_register_callback(self):
        if self._null:
            return None
        else:
            return self._max_monitored_item_register_callback

    @logger.setter
    def logger(self, val: UaSimpleAttributeOperand):
        self._logger = val
        self._value.logger = val._val


# ++++++++++++++++++++ protos +++++++++++++++++++++++
class UaSecurityPolicyAsymmetricModule(UaType):
    def __init__(self):
        super().__init__(None)


class UaSecurityPolicySymmetricModule(UaType):
    def __init__(self):
        super().__init__(None)


class UaSecurityPolicySignatureAlgorithm(UaType):
    def __init__(self):
        super().__init__(None)


class UaSecurityPolicyChannelModule(UaType):
    def __init__(self):
        super().__init__(None)


class UaNodeTypeLifecycle(UaType):
    def __init__(self):
        super().__init__(None)


class UaTwoStateVariableCallbackType(UaType):
    def __init__(self):
        super().__init__(None)


class UaTwoStateVariableChangeCallback(UaType):
    def __init__(self):
        super().__init__(None)
