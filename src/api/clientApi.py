# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from typing import Callable

import client_service_results as ClientServiceResult
import ua_types


class DefaultAttributes:
    VARIABLE_ATTRIBUTES_DEFAULT = ua_types.UaVariableAttributes(val=lib.UA_VariableAttributes_default)
    VARIABLE_TYPE_ATTRIBUTES_DEFAULT = ua_types.UaVariableTypeAttributes(val=lib.UA_VariableTypeAttributes_default)
    METHOD_ATTRIBUTES_DEFAULT = ua_types.UaMethodAttributes(val=lib.UA_MethodAttributes_default)
    OBJECT_ATTRIBUTES_DEFAULT = ua_types.UaObjectAttributes(val=lib.UA_ObjectAttributes_default)
    OBJECT_TYPE_ATTRIBUTES_DEFAULT = ua_types.UaObjectTypeAttributes(val=lib.UA_ObjectTypeAttributes_default)
    REFERENCE_TYPE_ATTRIBUTES_DEFAULT = ua_types.UaReferenceTypeAttributes(val=lib.UA_ReferenceTypeAttributes_default)
    DATA_TYPE_ATTRIBUTES_DEFAULT = ua_types.UaDataTypeAttributes(val=lib.UA_DataTypeAttributes_default)
    VIEW_ATTRIBUTES_DEFAULT = ua_types.UaViewAttributes(val=lib.UA_ViewAttributes_default)


class _UaCallback:
    """These static c type callback implementations are used to call the actual callback functions which have been
    submitted by the open62541 user """

    # todo: it might cause problems that we always create a new client wrapper instead of granting access to the same client wrapper object that has made the async call.

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncTranslateCallback(client, fun, request_id, tr):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(ua_client, ua_types.UaUInt32(request_id),
                             ua_types.UaTranslateBrowsePathsToNodeIdsResponse(tr))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncBrowseCallback(client, fun, request_id, wr):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaBrowseResponse(wr))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadDataTypeAttributeCallback(client, fun, request_id, var):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaNodeId(var))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadNodeIdAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(ua_client, ua_types.UaUInt32(request_id), ua_types.UaNodeId(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadDescriptionAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaLocalizedText(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadWriteMaskAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaUInt32(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadUserWriteMaskAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaUInt32(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadIsAbstractAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaBoolean(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadSymmetricAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaBoolean(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadInverseNameAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaLocalizedText(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadContainsNoLoopsAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaBoolean(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadEventNotifierAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaByte(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadValueRankAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaInt32(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadAccessLevelAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaByte(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadUserAccessLevelAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaByte(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadExecutableAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaBoolean(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadUserExecutableAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaBoolean(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncCallCallback(client, fun, request_id, cr):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaCallResponse(cr))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadCallback(client, fun, request_id, rr):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaReadResponse(rr))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadValueAttributeCallback(client, fun, request_id, var):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaVariant(var))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadNodeClassAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaNodeClass(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadBrowseNameAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaQualifiedName(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadDisplayNameAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaLocalizedText(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadMinimumSamplingIntervalAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaDouble(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadHistorizingAttributeCallback(client, fun, request_id, out):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaBoolean(out))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncWriteCallback(client, fun, request_id, wr):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaWriteResponse(wr))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncAddNodesCallback(client, fun, request_id, ar):
        ua_client = UaClient()
        ua_client.ua_client = client
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.UaAddNodesResponse(ar))

    # todo: response is void* --> ua_types.Void --> handling is not good
    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncServiceCallback(client, fun, request_id, response):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(client, ua_types.UaUInt32(request_id), ua_types.Void(response))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_NodeIteratorCallback(child_id, is_inverse, reference_type_id, fun):
        ffi.from_handle(fun)(ua_types.UaNodeId(child_id), ua_types.UaBoolean(is_inverse),
                             ua_types.UaNodeId(reference_type_id))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientCallback(client, fun):
        ua_client = UaClient()
        ua_client.ua_client = client
        ffi.from_handle(fun)(ua_client, ua_types.UaNodeId(child_id))


class UaClient:
    def __init__(self, config: ua_types.UaClientConfig = None):
        if config is None:
            self.ua_client = lib.UA_Client_new()
            self.set_default_config()
        else:
            self.ua_client = lib.UA_Client_newWithConfig(config)

    # connection

    def connect(self, endpoint_url: str):
        status_code = lib.UA_Client_connect(self.ua_client, bytes(endpoint_url, 'utf-8'))
        return ua_types.UaStatusCode(val=status_code)

    def disconnect(self):
        status_code = lib.UA_Client_disconnect(self.ua_client)
        return ua_types.UaStatusCode(val=status_code)

    def connect_secure_channel(self, endpoint_url: str):
        status_code = lib.UA_Client_connectSecureChannel(self.ua_client, bytes(endpoint_url, 'utf-8'))
        return ua_types.UaStatusCode(val=status_code)

    def disconnect_secure_channel(self):
        return ua_types.UaStatusCode(val=lib.UA_Client_disconnectSecureChannel(self.ua_client))

    # low level service

    def service_read(self, request: ua_types.UaReadRequest):
        ua_read_response = lib.UA_Client_Service_read(self.ua_client, request._val)
        return ua_types.UaReadResponse(val=ua_read_response)

    def service_write(self, request: ua_types.UaWriteRequest):
        ua_write_response = lib.UA_Client_Service_write(self.ua_client, request._val)
        return ua_types.UaWriteResponse(val=ua_write_response)

    def service_call(self, request: ua_types.UaCallRequest):
        ua_call_response = lib.UA_Client_Service_call(self.ua_client, request._val)
        return ua_types.UaCallResponse(val=ua_call_response)

    def service_add_nodes(self, request: ua_types.UaAddNodesRequest):
        ua_add_nodes_response = lib.UA_Client_Service_addNodes(self.ua_client, request._val)
        return ua_types.UaAddNodesResponse(val=ua_add_nodes_response)

    def service_add_reference(self, request: ua_types.UaAddReferencesRequest):
        ua_add_references_response = lib.UA_Client_Service_addReference(self.ua_client, request._val)
        return ua_types.UaAddReferencesResponse(val=ua_add_references_response)

    def service_delete_nodes(self, request: ua_types.UaDeleteNodesRequest):
        ua_delete_nodes_response = lib.UA_Client_Service_deleteNodes(self.ua_client, request._val)
        return ua_types.UaDeleteNodesResponse(val=ua_delete_nodes_response)

    def service_delete_references(self, request: ua_types.UaDeleteReferencesRequest):
        ua_delete_references_response = lib.UA_Client_Service_deleteReferences(self.ua_client, request._val)
        return ua_types.UaDeleteReferencesResponse(val=ua_delete_references_response)

    def service_browse(self, request: ua_types.UaBrowseRequest):
        ua_browse_response = lib.UA_Client_Service_browse(self.ua_client, request._val)
        return ua_types.UaBrowseResponse(val=ua_browse_response)

    def service_browse_next(self, request: ua_types.UaBrowseNextRequest):
        ua_browse_next_response = lib.UA_Client_Service_browseNext(self.ua_client, request._val)
        return ua_types.UaBrowseNextResponse(val=ua_browse_next_response)

    def service_translate_browse_paths_to_node_ids(self, request: ua_types.UaTranslateBrowsePathsToNodeIdsRequest):
        ua_translate_browse_paths_to_node_ids_response = lib.UA_Client_Service_translateBrowsePathsToNodeIds(
            self.ua_client, request._val)
        return ua_types.UaTranslateBrowsePathsToNodeIdsResponse(val=ua_translate_browse_paths_to_node_ids_response)

    def service_register_node(self, request: ua_types.UaRegisterNodesRequest):
        ua_register_nodes_response = lib.UA_Client_Service_registerNodes(self.ua_client, request._val)
        return ua_types.UaRegisterNodesResponse(val=ua_register_nodes_response)

    def service_unregister_node(self, request: ua_types.UaUnregisterNodesRequest):
        ua_unregister_nodes_response = lib.UA_Client_Service_unregisterNodes(self.ua_client, request._val)
        return ua_types.UaUnregisterNodesResponse(val=ua_unregister_nodes_response)

    # high level read service
    # todo: this doesn't really work because out is a void pointer. variable has to be created dynamically depending on type
    # also needs generic result class object as result
    def __read_attribute(self, node_id: ua_types.UaNodeId, attribute_id: ua_types.UaNodeId):
        out = ua_types.Void()
        out_data_type = ua_types.UaDataType
        status_code = lib.__UA_Client_readAttribute(self.ua_client, node_id._ptr, attribute_id._val, out._ptr,
                                                    out_data_type._ptr)
        return ClientServiceResult.ReadAttributeResult(ua_types.UaStatusCode(val=status_code), out, out_data_type)

    def read_node_id_attribute(self, node_id: ua_types.UaNodeId):
        out_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_readNodeIdAttribute(self.ua_client, node_id._val, out_node_id._ptr)
        return ClientServiceResult.ReadNodeIdAttributeResult(ua_types.UaStatusCode(val=status_code), out_node_id)

    def read_node_class_attribute(self, node_id: ua_types.UaNodeId):
        out_node_class = ua_types.UaNodeClass()
        status_code = lib.UA_Client_readNodeClassAttribute(self.ua_client, node_id._val, out_node_class._ptr)
        return ClientServiceResult.ReadNodeClassAttributeResult(ua_types.UaStatusCode(val=status_code), out_node_class)

    def read_browse_name_attribute(self, node_id: ua_types.UaNodeId):
        out_browse_name = ua_types.UaQualifiedName()
        status_code = lib.UA_Client_readBrowseNameAttribute(self.ua_client, node_id._val, out_browse_name._ptr)
        return ClientServiceResult.ReadBrowseNameAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                 out_browse_name)

    def read_display_name_attribute(self, node_id: ua_types.UaNodeId):
        out_display_name = ua_types.UaLocalizedText()
        status_code = lib.UA_Client_readDisplayNameAttribute(self.ua_client, node_id._val, out_display_name._ptr)
        return ClientServiceResult.ReadDisplayNameAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                  out_display_name)

    def read_description_attribute(self, node_id: ua_types.UaNodeId):
        out_description = ua_types.UaLocalizedText()
        status_code = lib.UA_Client_readDescriptionAttribute(self.ua_client, node_id._val, out_description._ptr)
        return ClientServiceResult.ReadDescriptionAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                  out_description)

    def read_write_mask_attribute(self, node_id: ua_types.UaNodeId):
        out_write_mask = ua_types.UaUInt32()
        status_code = lib.UA_Client_readWriteMaskAttribute(self.ua_client, node_id._val, out_write_mask._ptr)
        return ClientServiceResult.ReadWriteMaskAttributeResult(ua_types.UaStatusCode(val=status_code), out_write_mask)

    def read_user_write_mask_attribute(self, node_id: ua_types.UaNodeId):
        out_user_write_mask = ua_types.UaUInt32()
        status_code = lib.UA_Client_readUserWriteMaskAttribute(self.ua_client, node_id._val, out_user_write_mask._ptr)
        return ClientServiceResult.ReadUserWriteMaskAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                    out_user_write_mask)

    def read_is_abstract_attribute(self, node_id: ua_types.UaNodeId):
        out_is_abstract = ua_types.UaBoolean()
        status_code = lib.UA_Client_readIsAbstractAttribute(self.ua_client, node_id._val, out_is_abstract._ptr)
        return ClientServiceResult.ReadIsAbstractAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                 out_is_abstract)

    def read_symmetric_attribute(self, node_id: ua_types.UaNodeId):
        out_symmetric = ua_types.UaBoolean()
        status_code = lib.UA_Client_readSymmetricAttribute(self.ua_client, node_id._val, out_symmetric._ptr)
        return ClientServiceResult.ReadSymmetricAttributeResult(ua_types.UaStatusCode(val=status_code), out_symmetric)

    def read_inverse_name_attribute(self, node_id: ua_types.UaNodeId):
        out_inverse_name = ua_types.UaLocalizedText()
        status_code = lib.UA_Client_readInverseNameAttribute(self.ua_client, node_id._val, out_inverse_name._ptr)
        return ClientServiceResult.ReadInverseNameAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                  out_inverse_name)

    def read_contains_no_loops_attribute(self, node_id: ua_types.UaNodeId):
        out_contains_no_loops = ua_types.UaBoolean()
        status_code = lib.UA_Client_readContainsNoLoopsAttribute(self.ua_client, node_id._val,
                                                                 out_contains_no_loops._ptr)
        return ClientServiceResult.ReadContainsNoLoopsAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                      out_contains_no_loops)

    def read_event_notifier_attribute(self, node_id: ua_types.UaNodeId):
        out_event_notifier = ua_types.UaByte()
        status_code = lib.UA_Client_readEventNotifierAttribute(self.ua_client, node_id._val, out_event_notifier._ptr)
        return ClientServiceResult.ReadEventNotifierAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                    out_event_notifier)

    def read_value_attribute(self, node_id: ua_types.UaNodeId):
        value = ua_types.UaVariant()
        status_code = lib.UA_Client_readValueAttribute(self.ua_client, node_id._val, value._ptr)
        return ClientServiceResult.ReadValueAttributeResult(ua_types.UaStatusCode(val=status_code), value)

    def read_data_type_attribute(self, node_id: ua_types.UaNodeId):
        out_data_type = ua_types.UaNodeId()
        status_code = lib.UA_Client_readDataTypeAttribute(self.ua_client, node_id._val, out_data_type._ptr)
        return ClientServiceResult.ReadDataTypeAttribute(ua_types.UaStatusCode(val=status_code), out_data_type)

    def read_value_rank_attribute(self, node_id: ua_types.UaNodeId):
        out_value_rank = ua_types.UaUInt32()
        status_code = lib.UA_Client_readValueRankAttribute(self.ua_client, node_id._val, out_value_rank._ptr)
        return ClientServiceResult.ReadValueRankAttribute(ua_types.UaStatusCode(val=status_code), out_value_rank)

    def read_array_dimensions_attribute(self, node_id: ua_types.UaNodeId):
        out_array_dimensions_size = ua_types.SizeT()
        out_array_dimensions = ua_types.UaUInt32()
        status_code = lib.UA_Client_readArrayDimensionsAttribute(self.ua_client, node_id._val,
                                                                 out_array_dimensions_size._ptr,
                                                                 out_array_dimensions._ptr)
        return ClientServiceResult.ReadArrayDimensionsAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                      out_array_dimensions_size,
                                                                      out_array_dimensions)

    def read_access_level_attribute(self, node_id: ua_types.UaNodeId):
        out_access_level = ua_types.UaByte()
        status_code = lib.UA_Client_readAccessLevelAttribute(self.ua_client, node_id._val, out_access_level._ptr)
        return ClientServiceResult.ReadAccessLevelAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                  out_access_level)

    def read_user_access_level_attribute(self, node_id: ua_types.UaNodeId):
        out_user_access_level = ua_types.UaByte()
        status_code = lib.UA_Client_readUserAccessLevelAttribute(self.ua_client, node_id._val,
                                                                 out_user_access_level._ptr)
        return ClientServiceResult.ReadUserAccessLevelAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                      out_user_access_level)

    def read_minimum_sampling_interval_attribute(self, node_id: ua_types.UaNodeId):
        out_min_sampling_interval = ua_types.UaDouble()
        status_code = lib.UA_Client_readMinimumSamplingIntervalAttribute(self.ua_client, node_id._val,
                                                                         out_min_sampling_interval._ptr)
        return ClientServiceResult.ReadMinimumSamplingIntervalAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                              out_min_sampling_interval)

    def read_executable_attribute(self, node_id: ua_types.UaNodeId):
        out_executable = ua_types.UaBoolean()
        status_code = lib.UA_Client_readExecutableAttribute(self.ua_client, node_id._val, out_executable._ptr)
        return ClientServiceResult.ReadExecutableAttributeResult(ua_types.UaStatusCode(val=status_code), out_executable)

    def read_user_executable_attribute(self, node_id: ua_types.UaNodeId):
        out_user_executable = ua_types.UaBoolean()
        status_code = lib.UA_Client_readUserExecutableAttribute(self.ua_client, node_id._val, out_user_executable._ptr)
        return ClientServiceResult.ReadUserExecutableAttributeResult(ua_types.UaStatusCode(val=status_code),
                                                                     out_user_executable)

    # high level write service

    def write_node_id_attribute(self, node_id: ua_types.UaNodeId, new_node_id: ua_types.UaNodeId):
        status_code = lib.UA_Client_writeNodeIdAttribute(self.ua_client, node_id._val, new_node_id._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_node_class_attribute(self, node_id: ua_types.UaNodeId, new_node_class: ua_types.UaNodeClass):
        status_code = lib.UA_Client_writeNodeClassAttribute(self.ua_client, node_id._val, new_node_class._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_browse_name_attribute(self, node_id: ua_types.UaNodeId, new_browse_name: ua_types.UaQualifiedName):
        status_code = lib.UA_Client_writeBrowseNameAttribute(self.ua_client, node_id._val, new_browse_name._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_display_name_attribute(self, node_id: ua_types.UaNodeId, new_display_name: ua_types.UaLocalizedText):
        status_code = lib.UA_Client_writeDisplayNameAttribute(self.ua_client, node_id._val, new_display_name._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_description_attribute(self, node_id: ua_types.UaNodeId, new_description: ua_types.UaLocalizedText):
        status_code = lib.UA_Client_writeDescriptionAttribute(self.ua_client, node_id._val, new_description._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_write_mask_attribute(self, node_id: ua_types.UaNodeId, new_write_mask: ua_types.UaUInt32):
        status_code = lib.UA_Client_writeWriteMaskAttribute(self.ua_client, node_id._val, new_write_mask._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_user_write_mask_attribute(self, node_id: ua_types.UaNodeId, new_user_write_mask: ua_types.UaUInt32):
        status_code = lib.UA_Client_writeUserWriteMaskAttribute(self.ua_client, node_id._val, new_user_write_mask._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_is_abstract_attribute(self, node_id: ua_types.UaNodeId, new_is_abstract: ua_types.UaBoolean):
        status_code = lib.UA_Client_writeIsAbstractAttribute(self.ua_client, node_id._val, new_is_abstract._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_symmetric_attribute(self, node_id: ua_types.UaNodeId, new_symmetric: ua_types.UaBoolean):
        status_code = lib.UA_Client_writeSymmetricAttribute(self.ua_client, node_id._val, new_symmetric._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_inverse_name_attribute(self, node_id: ua_types.UaNodeId, new_inverse_name: ua_types.UaLocalizedText):
        status_code = lib.UA_Client_writeInverseNameAttribute(self.ua_client, node_id._val, new_inverse_name._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_contains_no_loops_attribute(self, node_id: ua_types.UaNodeId, new_contains_no_loops: ua_types.UaBoolean):
        status_code = lib.UA_Client_writeContainsNoLoopsAttribute(self.ua_client, node_id._val,
                                                                  new_contains_no_loops._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_event_notifier_attribute(self, node_id: ua_types.UaNodeId, new_event_notifier: ua_types.UaByte):
        status_code = lib.UA_Client_writeEventNotifierAttribute(self.ua_client, node_id._val, new_event_notifier._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_value_attribute(self, node_id: ua_types.UaNodeId, new_value: ua_types.UaVariant):
        status_code = lib.UA_Client_writeValueAttribute(self.ua_client, node_id._val, new_value._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_data_type_attribute(self, node_id: ua_types.UaNodeId, new_data_type: ua_types.UaNodeId):
        status_code = lib.UA_Client_writeDataTypeAttribute(self.ua_client, node_id._val, new_data_type._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_value_rank_attribute(self, node_id: ua_types.UaNodeId, new_value_rank: ua_types.UaInt32):
        status_code = lib.UA_Client_writeValueRankAttribute(self.ua_client, node_id._val, new_value_rank._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_array_dimensions_attribute(self, node_id: ua_types.UaNodeId, new_array_dimensions_size: ua_types.SizeT,
                                         new_array_dimensions: ua_types.UaUInt32):
        status_code = lib.UA_Client_writeArrayDimensionsAttribute(self.ua_client, node_id._val,
                                                                  new_array_dimensions_size._val,
                                                                  new_array_dimensions._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_access_level_attribute(self, node_id: ua_types.UaNodeId, new_access_level: ua_types.UaByte):
        status_code = lib.UA_Client_writeAccessLevelAttribute(self.ua_client, node_id._val, new_access_level._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_user_access_level_attribute(self, node_id: ua_types.UaNodeId, new_user_access_level: ua_types.UaByte):
        status_code = lib.UA_Client_writeUserAccessLevelAttribute(self.ua_client, node_id._val,
                                                                  new_user_access_level._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_minimum_sampling_interval_attribute(self, node_id: ua_types.UaNodeId,
                                                  new_min_interval: ua_types.UaDouble):
        status_code = lib.UA_Client_writeMinimumSamplingIntervalAttribute(self.ua_client, node_id._val,
                                                                          new_min_interval._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_executable_attribute(self, node_id: ua_types.UaNodeId, new_executable: ua_types.UaBoolean):
        status_code = lib.UA_Client_writeExecutableAttribute(self.ua_client, node_id._val, new_executable._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_user_executable_attribute(self, node_id: ua_types.UaNodeId, new_user_executable: ua_types.UaBoolean):
        status_code = lib.UA_Client_writeUserExecutableAttribute(self.ua_client, node_id._val, new_user_executable._ptr)
        return ua_types.UaStatusCode(val=status_code)

    # misc high level service

    def call(self, object_id: ua_types.UaNodeId, method_id: ua_types.UaNodeId, input_size: ua_types.SizeT,
             call_input: ua_types.UaVariant):
        output_size = ua_types.SizeT()
        # Todo: output has to be ** --> this is a problem for our type system atm
        output = ffi.new("UA_Variant **")
        status_code = lib.UA_Client_call(self.ua_client, object_id._val, method_id._val, input_size._val,
                                         call_input._ptr, output_size._ptr,
                                         output)
        return ClientServiceResult.CallResult(ua_types.UaStatusCode(val=status_code), output_size,
                                              ua_types.UaVariant(val=output[0][0]))

    def add_reference(self, source_node_id: ua_types.UaNodeId, reference_type_id: ua_types.UaNodeId,
                      is_forward: ua_types.UaBoolean,
                      target_server_uri: ua_types.UaString, target_node_id: ua_types.UaExpandedNodeId,
                      target_node_class: ua_types.UaNodeClass):
        status_code = lib.UA_Client_addReference(self.ua_client, source_node_id._val, reference_type_id._val,
                                                 is_forward._val,
                                                 target_server_uri._val, target_node_id._val, target_node_class._val)
        return ua_types.UaStatusCode(val=status_code)

    def delete_reference(self, source_node_id: ua_types.UaNodeId, reference_type_id: ua_types.UaNodeId,
                         is_forward: ua_types.UaBoolean,
                         target_node_id: ua_types.UaExpandedNodeId, delete_bidirectional: ua_types.UaBoolean):
        status_code = lib.UA_Client_deleteReference(self.ua_client, source_node_id._val, reference_type_id._val,
                                                    is_forward._val,
                                                    target_node_id._val, delete_bidirectional._val)
        return ua_types.UaStatusCode(val=status_code)

    def delete_node(self, node_id: ua_types.UaNodeId, delete_target_references: ua_types.UaBoolean):
        status_code = lib.UA_Client_deleteNode(self.ua_client, node_id._val, delete_target_references._val)
        return ua_types.UaStatusCode(val=status_code)

    # high level add node services

    def add_variable_node(self, requested_new_node_id: ua_types.UaNodeId, parent_node_id: ua_types.UaNodeId,
                          reference_type_id: ua_types.UaNodeId, browse_name: ua_types.UaQualifiedName,
                          type_definition: ua_types.UaNodeId,
                          attr: ua_types.UaVariableAttributes = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_addVariableNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                    reference_type_id._val, browse_name._val, type_definition._val,
                                                    attr._val,
                                                    out_new_node_id._ptr)
        return ClientServiceResult.AddNodeResult(ua_types.UaStatusCode(val=status_code), out_new_node_id)

    def add_variable_type_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                               attr: ua_types.UaVariableTypeAttributes = DefaultAttributes.VARIABLE_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_addVariableTypeNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                        reference_type_id._val, browse_name._val, attr._val,
                                                        out_new_node_id._ptr)
        return ClientServiceResult.AddNodeResult(ua_types.UaStatusCode(val=status_code), out_new_node_id)

    def add_object_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition,
                        attr: ua_types.UaObjectAttributes = DefaultAttributes.OBJECT_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_addObjectNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                  reference_type_id._val, browse_name._val, type_definition._val,
                                                  attr._val,
                                                  out_new_node_id._ptr)
        return ClientServiceResult.AddNodeResult(ua_types.UaStatusCode(val=status_code), out_new_node_id)

    def add_object_type_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                             attr: ua_types.UaObjectTypeAttributes = DefaultAttributes.OBJECT_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_addObjectTypeNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                      reference_type_id._val, browse_name._val, attr._val,
                                                      out_new_node_id._ptr)
        return ClientServiceResult.AddNodeResult(ua_types.UaStatusCode(val=status_code), out_new_node_id)

    def add_view_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                      attr: ua_types.UaViewAttributes = DefaultAttributes.VIEW_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_addViewNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                reference_type_id._val, browse_name._val, attr._val,
                                                out_new_node_id._ptr)
        return ClientServiceResult.AddNodeResult(ua_types.UaStatusCode(val=status_code), out_new_node_id)

    def add_reference_type_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                                attr: ua_types.UaReferenceTypeAttributes = DefaultAttributes.REFERENCE_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_addReferenceTypeNode(self.ua_client, requested_new_node_id._val,
                                                         parent_node_id._val,
                                                         reference_type_id._val, browse_name._val, attr._val,
                                                         out_new_node_id._ptr)
        return ClientServiceResult.AddNodeResult(ua_types.UaStatusCode(val=status_code), out_new_node_id)

    def add_data_type_node(self, requested_node_id, parent_node_id, reference_type_id, browse_name,
                           attr: ua_types.UaDataTypeAttributes = DefaultAttributes.DATA_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_addDataTypeNode(self.ua_client, requested_node_id._val, parent_node_id._val,
                                                    reference_type_id._val, browse_name._val, attr._val,
                                                    out_new_node_id._ptr)
        return ClientServiceResult.AddNodeResult(ua_types.UaStatusCode(val=status_code), out_new_node_id)

    def add_method_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                        attr: ua_types.UaMethodAttributes = DefaultAttributes.METHOD_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_addMethodNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                  reference_type_id._val, browse_name._val, attr._val,
                                                  out_new_node_id._ptr)
        return ClientServiceResult.AddNodeResult(ua_types.UaStatusCode(val=status_code), out_new_node_id)

    # utils
    def get_config(self):
        return lib.UA_Client_getConfig(self.ua_client)

    def set_default_config(self):
        lib.UA_ClientConfig_setDefault(self.get_config())

    def find_data_type(self, type_id):
        return ua_types.UaDataType(lib.UA_Client_findDataType(self.ua_client, type_id), is_pointer=True)

    def get_endpoints(self, server_url, endpoint_descriptions_size, endpoint_descriptions):
        status_code = lib.UA_Client_getEndpoints(self.ua_client, server_url, endpoint_descriptions_size,
                                                 endpoint_descriptions)
        return ua_types.UaStatusCode(val=status_code)

    def find_servers(self, server_url, server_uris_size, locale_ids_size, locale_ids, registered_servers_size,
                     registered_servers):
        status_code = lib.UA_Client_findServers(self.ua_client, server_url, server_uris_size, locale_ids_size,
                                                locale_ids,
                                                registered_servers_size, registered_servers)
        return ua_types.UaStatusCode(val=status_code)

    def run_iterate(self, timeout):
        status_code = lib.UA_Client_run_iterate(self.ua_client, timeout)
        return ua_types.UaStatusCode(val=status_code)

    #    def find_servers_on_network(self, server_url, starting_record_id, max_records_to_return,
    #                                server_capability_filter_size, server_on_network_size, server_on_network):
    #        return lib.UA_Client_findServersOnNetwork(self.ua_client, server_url, starting_record_id, max_records_to_return,
    #                                                  server_capability_filter_size, server_on_network_size,
    #                                                  server_on_network)

    # ASYNC
    # important remark: In order to work with asyncronous functions you absolutely have to make sure to keep a variable alive which holds the _handle value of the response until you are done with the callback.
    # if the reference is lost prematurely, CFFI will garbage collect the void* handle of the callback function as it has no owner anymore! You could for example add the handle to a dictonary which stores all active callbacks and remove it once it's no longer needed

    # async read service
    def send_async_read_request(self, request: ua_types.UaReadRequest,
                                callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaVariant], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_sendAsyncReadRequest(self.ua_client,
                                                         request._ptr,
                                                         lib.python_wrapper_UA_ClientAsyncReadCallback,
                                                         _handle,
                                                         req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def __read_attribute_async(self, node_id: ua_types.UaNodeId, attribute_id: ua_types.UaAttributeId,
                               callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        out_data_type = ua_types.UaDataType()
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.__UA_Client_readAttribute_async(self.ua_client,
                                                          node_id._ptr,
                                                          attribute_id._val,
                                                          out_data_type._ptr,
                                                          lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                          _handle,
                                                          req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_data_type_attribute_async(self, node_id: ua_types.UaNodeId,
                                       callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaNodeId], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readDataTypeAttribute_async(self.ua_client,
                                                                node_id._val,
                                                                lib.python_wrapper_UA_ClientAsyncReadDataTypeAttributeCallback,
                                                                _handle,
                                                                req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_value_attribute_async(self, node_id: ua_types.UaNodeId,
                                   callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaVariant], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readValueAttribute_async(self.ua_client,
                                                             node_id._val,
                                                             lib.python_wrapper_UA_ClientAsyncReadValueAttributeCallback,
                                                             _handle,
                                                             req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_node_id_attribute_async(self, node_id: ua_types.UaNodeId,
                                     callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaNodeId], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readNodeIdAttribute_async(self.ua_client,
                                                              node_id._val,
                                                              lib.python_wrapper_UA_ClientAsyncReadNodeIdAttributeCallback,
                                                              _handle,
                                                              req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_node_class_attribute_async(self, node_id: ua_types.UaNodeId,
                                        callback: Callable[
                                            ['UaClient', ua_types.UaUInt32, ua_types.UaNodeClass], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readNodeClassAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 lib.python_wrapper_UA_ClientAsyncReadNodeClassAttributeCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_browse_name_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.UaQualifiedName], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readBrowseNameAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  lib.python_wrapper_UA_ClientAsyncReadBrowseNameAttributeCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_display_name_attribute_async(self, node_id: ua_types.UaNodeId,
                                          callback: Callable[
                                              ['UaClient', ua_types.UaUInt32, ua_types.UaLocalizedText], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readDisplayNameAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadDisplayNameAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_description_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.UaLocalizedText], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readDescriptionAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadDescriptionAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_write_mask_attribute_async(self, node_id: ua_types.UaNodeId,
                                        callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaUInt32], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readWriteMaskAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 lib.python_wrapper_UA_ClientAsyncReadWriteMaskAttributeCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_user_write_mask_attribute_async(self, node_id: ua_types.UaNodeId,
                                             callback: Callable[
                                                 ['UaClient', ua_types.UaUInt32, ua_types.UaUInt32], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readUserWriteMaskAttribute_async(self.ua_client,
                                                                     node_id._val,
                                                                     lib.python_wrapper_UA_ClientAsyncReadUserWriteMaskAttributeCallback,
                                                                     _handle,
                                                                     req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_is_abstract_attribute_async(self, node_id: ua_types.UaNodeId,
                                         callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaBoolean], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readIsAbstractAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  lib.python_wrapper_UA_ClientAsyncReadIsAbstractAttributeCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_symmetric_attribute_async(self, node_id: ua_types.UaNodeId,
                                       callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaBoolean], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readSymmetricAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 lib.python_wrapper_UA_ClientAsyncReadSymmetricAttributeCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_inverse_name_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.UaLocalizedText], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readInverseNameAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadInverseNameAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_contains_no_loops_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.UaBoolean], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readContainsNoLoopsAttribute_async(self.ua_client,
                                                                       node_id._val,
                                                                       lib.python_wrapper_UA_ClientAsyncReadContainsNoLoopsAttributeCallback,
                                                                       _handle,
                                                                       req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_event_notifier_attribute_async(self, node_id: ua_types.UaNodeId,
                                            callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaByte], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readEventNotifierAttribute_async(self.ua_client,
                                                                     node_id._val,
                                                                     lib.python_wrapper_UA_ClientAsyncReadEventNotifierAttributeCallback,
                                                                     _handle,
                                                                     req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_value_rank_attribute_async(self, node_id: ua_types.UaNodeId,
                                        callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaUInt32], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readValueRankAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 lib.python_wrapper_UA_ClientAsyncReadValueRankAttributeCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_access_level_attribute_async(self, node_id: ua_types.UaNodeId,
                                          callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaByte], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readAccessLevelAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadAccessLevelAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_user_access_level_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.UaByte], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readUserAccessLevelAttribute_async(self.ua_client,
                                                                       node_id._val,
                                                                       lib.python_wrapper_UA_ClientAsyncReadUserAccessLevelAttributeCallback,
                                                                       _handle,
                                                                       req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_minimum_sampling_interval_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.UaDouble], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readMinimumSamplingIntervalAttribute_async(self.ua_client,
                                                                               node_id._val,
                                                                               lib.python_wrapper_UA_ClientAsyncReadMinimumSamplingIntervalAttributeCallback,
                                                                               _handle,
                                                                               req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_historizing_attribute_async(self, node_id: ua_types.UaNodeId,
                                         callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaBoolean], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readHistorizingAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadHistorizingAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_executable_attribute_async(self, node_id: ua_types.UaNodeId,
                                        callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaBoolean], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_readExecutableAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  lib.python_wrapper_UA_ClientAsyncReadExecutableAttributeCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def read_user_executable_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.UaBoolean], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.readUserExecutableAttribute_async(self.ua_client,
                                                            node_id._val,
                                                            lib.python_wrapper_UA_ClientAsyncReadUserExecutableAttributeCallback,
                                                            _handle,
                                                            req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    # async write service
    def send_async_write_request(self, request: ua_types.UaWriteRequest,
                                 callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaWriteResponse], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_sendAsyncWriteRequest(self.ua_client,
                                                          request._ptr,
                                                          lib.python_wrapper_UA_ClientAsyncWriteCallback,
                                                          _handle,
                                                          req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    # todo: how to handle _in (*void)?
    def __write_attribute_async(self, node_id: ua_types.UaNodeId, attribute_id: ua_types.UaAttributeId,
                                _in: ua_types.Void,
                                in_data_type: ua_types.UaDataType,
                                callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        status_code = lib.__UA_Client_writeAttribute_async(self.ua_client,
                                                           node_id._ptr,
                                                           attribute_id._val,
                                                           _in._ptr,
                                                           in_data_type._ptr,
                                                           lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                           ffi.new_handle(callback),
                                                           req_id._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def write_value_attribute_async(self, node_id: ua_types.UaNodeId, new_value: ua_types.UaVariant,
                                    callback: Callable[
                                        ['UaClient', ua_types.UaUInt32, ua_types.UaWriteResponse], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeValueAttribute_async(self.ua_client,
                                                              node_id._val,
                                                              new_value._ptr,
                                                              lib.python_wrapper_UA_ClientAsyncWriteCallback,
                                                              _handle,
                                                              req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_node_id_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_node_id = ua_types.UaNodeId()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeNodeIdAttribute_async(self.ua_client,
                                                               node_id._val,
                                                               out_node_id._ptr,
                                                               lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                               _handle,
                                                               req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_node_class_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_node_class = ua_types.UaNodeClass()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeNodeClassAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  out_node_class._ptr,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_browse_name_attribute_async(self, node_id: ua_types.UaNodeId,
                                          callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_browse_name = ua_types.UaQualifiedName()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeBrowseNameAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   out_browse_name._ptr,
                                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_display_name_attribute_async(self, node_id: ua_types.UaNodeId,
                                           callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_display_name = ua_types.UaLocalizedText()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeDisplayNameAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    out_display_name._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_description_attribute_async(self, node_id: ua_types.UaNodeId,
                                          callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_description = ua_types.UaLocalizedText()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeDescriptionAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    out_description._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_write_mask_attribute_async(self, node_id: ua_types.UaNodeId,
                                         callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_write_mask = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeWriteMaskAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  out_write_mask._ptr,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_user_write_mask_attribute_async(self, node_id: ua_types.UaNodeId,
                                              callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_user_write_mask = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeUserWriteMaskAttribute_async(self.ua_client,
                                                                      node_id._val,
                                                                      out_user_write_mask._ptr,
                                                                      lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                      _handle,
                                                                      req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_is_abstract_attribute_async(self, node_id: ua_types.UaNodeId,
                                          callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_is_abstract = ua_types.UaBoolean()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeIsAbstractAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   out_is_abstract._ptr,
                                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_symmetric_attribute_async(self, node_id: ua_types.UaNodeId,
                                        callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_symmetric = ua_types.UaBoolean()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeSymmetricAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  out_symmetric._ptr,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_inverse_name_attribute_async(self, node_id: ua_types.UaNodeId,
                                           callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_inverse_name = ua_types.UaLocalizedText()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeInverseNameAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    out_inverse_name._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_contains_no_loops_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_contains_no_loops = ua_types.UaBoolean()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeContainsNoLoopsAttribute_async(self.ua_client,
                                                                        node_id._val,
                                                                        out_contains_no_loops._ptr,
                                                                        lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                        _handle,
                                                                        req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_event_notifier_attribute_async(self, node_id: ua_types.UaNodeId,
                                             callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_event_notifier = ua_types.UaByte()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeEventNotifierAttribute_async(self.ua_client,
                                                                      node_id._val,
                                                                      out_event_notifier._ptr,
                                                                      lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                      _handle,
                                                                      req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_data_type_attribute_async(self, node_id: ua_types.UaNodeId,
                                        callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_data_type = ua_types.UaNodeId()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeDataTypeAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 out_data_type._ptr,
                                                                 lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_value_rank_attribute_async(self, node_id: ua_types.UaNodeId,
                                         callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_value_rank = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeValueRankAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  out_value_rank._ptr,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_access_level_attribute_async(self, node_id: ua_types.UaNodeId,
                                           callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_access_level = ua_types.UaByte()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeAccessLevelAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    out_access_level._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_user_access_level_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_user_access_level = ua_types.UaByte()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeUserAccessLevelAttribute_async(self.ua_client,
                                                                        node_id._val,
                                                                        out_user_access_level._ptr,
                                                                        lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                        _handle,
                                                                        req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    # todo: check if this is correct. this is different in the synchronous version. the naming of out_minimum_sampling_interval suggests that it is a return value but I think it is evaluated by the service again as an argument
    # for now we adapted the naming to match the syncronous version
    # could be the case that new_min_interval is altered by open62541 --> check this to see if we need to make a copy to prevent side effect
    def write_minimum_sampling_interval_attribute_async(self, node_id: ua_types.UaNodeId, callback: Callable[
        ['UaClient', ua_types.UaUInt32, ua_types.Void], None],
                                                        new_min_interval: ua_types.UaDouble):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeMinimumSamplingIntervalAttribute_async(self.ua_client,
                                                                                node_id._val,
                                                                                new_min_interval._val,
                                                                                lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                                _handle,
                                                                                req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    # todo: check if this is correct. this is different in the synchronous version
    # for now adapted naming to match syncronous method as this seems to make the most sense
    # could be the case that new_historizing is altered by open62541 --> check this to see if we need to make a copy to prevent side effect
    def write_historizing_attribute_async(self, node_id: ua_types.UaNodeId,
                                          callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None],
                                          new_historizing: ua_types.UaBoolean):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeHistorizingAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    new_historizing._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_executable_attribute_async(self, node_id: ua_types.UaNodeId,
                                         callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_executable = ua_types.UaBoolean()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeExecutableAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   out_executable._ptr,
                                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def write_user_executable_attribute_async(self, node_id: ua_types.UaNodeId,
                                              callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        out_user_executable = ua_types.UaBoolean()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeUserExecutableAttribute_async(self.ua_client,
                                                                       node_id._val,
                                                                       out_user_executable._ptr,
                                                                       lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                       _handle,
                                                                       req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    # call service
    # todo: can we get rid of input_size, calculate it ourselves and hide it from users?
    def _call_async(self, object_id: ua_types.UaNodeId, method_id: ua_types.UaNodeId, input_size: ua_types.SizeT,
                    _input: ua_types.UaVariant,
                    callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.__UA_Client_call_async(self.ua_client,
                                                 object_id._val,
                                                 method_id._val,
                                                 input_size._val,
                                                 _input._ptr,
                                                 lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                 _handle,
                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    # todo: can we get rid of input_size, calculate it ourselves and hide it from users?
    def call_async(self, object_id: ua_types.UaNodeId, method_id: ua_types.UaNodeId, input_size: ua_types.SizeT,
                   _input: ua_types.UaVariant,
                   callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaCallResponse], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.__UA_Client_call_async(self.ua_client,
                                                 object_id._val,
                                                 method_id._val,
                                                 input_size._val,
                                                 _input._ptr,
                                                 lib.python_wrapper_UA_ClientAsyncCallCallback,
                                                 _handle,
                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    # add node service
    def add_variable_node_async(self, requested_new_node_id: ua_types.UaNodeId, parent_node_id: ua_types.UaNodeId,
                                reference_type_id: ua_types.UaNodeId, browse_name: ua_types.UaQualifiedName,
                                type_definition: ua_types.UaNodeId,
                                callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaAddNodesResponse], None],
                                attr: ua_types.UaVariableAttributes = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_addVariableNode_async(self.ua_client,
                                                          requested_new_node_id._val,
                                                          parent_node_id._val,
                                                          reference_type_id._val,
                                                          browse_name._val,
                                                          type_definition._val,
                                                          attr._val,
                                                          out_new_node_id._ptr,
                                                          lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                          _handle,
                                                          req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def __add_node_async(self, node_class: ua_types.UaNodeClass, requested_new_node_id: ua_types.UaNodeId,
                         parent_node_id: ua_types.UaNodeId, reference_type_id: ua_types.UaNodeId,
                         browse_name: ua_types.UaQualifiedName, type_definition: ua_types.UaNodeId, attr,
                         attribute_type: ua_types.UaDataType,
                         callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        out_new_node_id = ua_types.UaNodeId()
        req_id = ua_types.UaUInt32()
        status_code = lib.__UA_Client_addNode_async(self.ua_client,
                                                    node_class._val,
                                                    requested_new_node_id._val,
                                                    parent_node_id._val,
                                                    reference_type_id._val,
                                                    browse_name._val,
                                                    type_definition._val,
                                                    attr._ptr,
                                                    attribute_type._ptr,
                                                    out_new_node_id._ptr,
                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                    ffi.new_handle(callback),
                                                    # todo: this crashed because the memory gets freed as the owner lives on stackframe and is destroyed after function call
                                                    req_id._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def add_variable_type_node_async(self, requested_new_node_id: ua_types.UaNodeId, parent_node_id: ua_types.UaNodeId,
                                     reference_type_id: ua_types.UaNodeId, browse_name: ua_types.UaQualifiedName,
                                     callback: Callable[
                                         ['UaClient', ua_types.UaUInt32, ua_types.UaAddNodesResponse], None],
                                     attr=DefaultAttributes.VARIABLE_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_addVariableTypeNode_async(self.ua_client,
                                                              requested_new_node_id._val,
                                                              parent_node_id._val,
                                                              reference_type_id._val,
                                                              browse_name._val,
                                                              attr._val,
                                                              out_new_node_id._ptr,
                                                              lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                              _handle,
                                                              req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def add_object_node_async(self, requested_new_node_id: ua_types.UaNodeId, parent_node_id: ua_types.UaNodeId,
                              reference_type_id: ua_types.UaNodeId, browse_name: ua_types.UaQualifiedName,
                              type_definition: ua_types.UaNodeId,
                              callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaAddNodesResponse], None],
                              attr=DefaultAttributes.OBJECT_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_addObjectNode_async(self.ua_client,
                                                        requested_new_node_id._val,
                                                        parent_node_id._val,
                                                        reference_type_id._val,
                                                        browse_name._val,
                                                        type_definition._val,
                                                        attr._val,
                                                        out_new_node_id._ptr,
                                                        lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                        _handle,
                                                        req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def add_object_type_node_async(self, requested_new_node_id: ua_types.UaNodeId, parent_node_id: ua_types.UaNodeId,
                                   reference_type_id: ua_types.UaNodeId, browse_name: ua_types.UaQualifiedName,
                                   callback: Callable[
                                       ['UaClient', ua_types.UaUInt32, ua_types.UaAddNodesResponse], None],
                                   attr=DefaultAttributes.OBJECT_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_addObjectTypeNode_async(self.ua_client,
                                                            requested_new_node_id._val,
                                                            parent_node_id._val,
                                                            reference_type_id._val,
                                                            browse_name._val,
                                                            attr._val,
                                                            out_new_node_id._ptr,
                                                            lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                            _handle,
                                                            req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def add_view_node_async(self, requested_new_node_id: ua_types.UaNodeId, parent_node_id: ua_types.UaNodeId,
                            reference_type_id: ua_types.UaNodeId, browse_name: ua_types.UaQualifiedName,
                            callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaAddNodesResponse], None],
                            attr=DefaultAttributes.VIEW_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_addViewNode_async(self.ua_client,
                                                      requested_new_node_id._val,
                                                      parent_node_id._val,
                                                      reference_type_id._val,
                                                      browse_name._val,
                                                      attr._val,
                                                      out_new_node_id._ptr,
                                                      lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                      _handle,
                                                      req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def add_reference_type_node_async(self, requested_new_node_id: ua_types.UaNodeId, parent_node_id: ua_types.UaNodeId,
                                      reference_type_id: ua_types.UaNodeId, browse_name: ua_types.UaQualifiedName,
                                      callback: Callable[
                                          ['UaClient', ua_types.UaUInt32, ua_types.UaAddNodesResponse], None],
                                      attr=DefaultAttributes.REFERENCE_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_addReferenceTypeNode_async(self.ua_client,
                                                               requested_new_node_id._val,
                                                               parent_node_id._val,
                                                               reference_type_id._val,
                                                               browse_name._val,
                                                               attr._val,
                                                               out_new_node_id._ptr,
                                                               lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                               _handle,
                                                               req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def add_data_type_node_async(self, requested_new_node_id: ua_types.UaNodeId, parent_node_id: ua_types.UaNodeId,
                                 reference_type_id: ua_types.UaNodeId, browse_name: ua_types.UaQualifiedName,
                                 callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaAddNodesResponse], None],
                                 attr=DefaultAttributes.DATA_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_addDataTypeNode_async(self,
                                                          requested_new_node_id._val,
                                                          parent_node_id._val,
                                                          reference_type_id._val,
                                                          browse_name._val,
                                                          attr._val,
                                                          out_new_node_id._ptr,
                                                          lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                          _handle,
                                                          req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    def add_method_node_async(self, requested_new_node_id: ua_types.UaNodeId, parent_node_id: ua_types.UaNodeId,
                              reference_type_id: ua_types.UaNodeId, browse_name: ua_types.UaQualifiedName,
                              callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaAddNodesResponse], None],
                              attr=DefaultAttributes.METHOD_ATTRIBUTES_DEFAULT):
        out_new_node_id = ua_types.UaNodeId()
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_addMethodNode_async(self.ua_client,
                                                        requested_new_node_id._val,
                                                        parent_node_id._val,
                                                        reference_type_id._val,
                                                        browse_name._val,
                                                        attr._val,
                                                        out_new_node_id._ptr,
                                                        lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                        _handle,
                                                        req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    # browse service
    def send_async_browse_request(self, request: ua_types.UaBrowseRequest,
                                  callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.UaBrowseResponse], None]):
        req_id = ua_types.UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_sendAsyncBrowseRequest(self.ua_client,
                                                           request,
                                                           lib.python_wrapper_UA_ClientAsyncBrowseCallback,
                                                           _handle,
                                                           req_id._ptr)
        return ClientServiceResult.AsyncResponse(ua_types.UaStatusCode(val=status_code), req_id, _handle)

    # misc
    def add_timed_callback(self, callback: Callable[['UaClient', ua_types.Void], None],
                           date: ua_types.UaDateTime, callback_id):
        status_code = lib.UA_Client_addTimedCallback(self.ua_client,
                                                     lib.python_wrapper_UA_ClientCallback,
                                                     ffi.new_handle(callback),
                                                     date._val,
                                                     callback_id._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def add_repeated_callback(self, callback: Callable[['UaClient', ua_types.Void], None],
                              interval_ms: ua_types.UaDouble,
                              callback_id: ua_types.UaUInt64):
        status_code = lib.UA_Client_addRepeatedCallback(self.ua_client,
                                                        lib.python_wrapper_UA_ClientCallback,
                                                        ffi.new_handle(callback),
                                                        interval_ms._val,
                                                        callback_id._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def change_repeated_callback_interval(self, callback_id: ua_types.UaUInt64, interval_ms: ua_types.UaDouble):
        lib.UA_Client_changeRepeatedCallbackInterval(self.ua_client, callback_id._val, interval_ms._val)

    def remove_callback(self, callback_id: ua_types.UaUInt64):
        lib.UA_Client_removeCallback(self.ua_client, callback_id)

    def renew_secure_channel(self):
        status_code = lib.UA_Client_renewSecureChannel(self.ua_client)
        return ua_types.UaStatusCode(val=status_code)

    # todo: how to handle void * request? not really usable at the moment
    def __async_service_ex(self, request: ua_types.Void, request_type: ua_types.UaDataType,
                           response_type: ua_types.UaDataType, callback, timeout: ua_types.UaInt32):
        req_id = ua_types.UaUInt32()
        status_code = lib.__UA_Client_AsyncServiceEx(self.ua_client,
                                                     request._ptr,
                                                     request_type._ptr,
                                                     lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                     response_type._ptr,
                                                     ffi.new_handle(callback),
                                                     req_id._ptr,
                                                     timeout._val)
        return ua_types.UaStatusCode(val=status_code)

        # todo: wrap response

    # todo: not not usable at the moment --> fix
    def get_state(self):
        channel_state = ua_types.UaSecureChannelState()
        session_state = ua_types.UaSessionState()
        connect_status = None  # todo: there is no ua_types.UaConnectSatus() yet
        return lib.UA_Client_getState(self.ua_client, channel_state, session_state,
                                      connect_status)  # todo: create response wrapper

    # todo: wrap response. Problem: return type is void*
    def get_context(self):
        return ua_types.Void(val=lib.UA_Client_getContext(self.ua_client))

    # todo: we don't understand how this function is supposed to work. does it find the correct request via the URL and overwrites the corresponding callback?
    def modify_async_callback(self, req_id: ua_types.UaUInt32,
                              callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        status_code = lib.UA_Client_modifyAsyncCallback(self.ua_client,
                                                        req_id._val,
                                                        ffi.new_handle(callback),
                                                        lib.python_wrapper_UA_ClientAsyncServiceCallback)
        return ua_types.UaStatusCode(val=status_code)

    # todo: request and response have type void* --> not usable atm
    def __service(self, request: ua_types.Void, request_type: ua_types.UaDataType, response: ua_types.Void,
                  response_type: ua_types.UaDataType):
        status_code = lib.__UA_Client_Service(self.ua_client,
                                              request._ptr,
                                              request_type._ptr,
                                              response._ptr,
                                              response_type._ptr)
        return ua_types.UaStatusCode(val=status_code)

    # todo: request and response have type void* --> not usable atm
    def __async_service(self, request: ua_types.Void, request_type: ua_types.UaDataType, response_type: ua_types.Void,
                        callback: Callable[['UaClient', ua_types.UaUInt32, ua_types.Void], None]):
        req_id = ua_types.UaUInt32()
        status_code = lib.__UA_Client_AsyncService(self.ua_client,
                                                   request._ptr,
                                                   request_type._ptr,
                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                   response_type._ptr,
                                                   ffi.new_handle(callback),
                                                   req_id._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def namespace_get_index(self, namespace_uri: ua_types.UaString, namespace_index: ua_types.UaUInt16):
        status_code = lib.UA_Client_NamespaceGetIndex(self.ua_client,
                                                      namespace_uri._ptr,
                                                      namespace_index._ptr)
        return ua_types.UaStatusCode(val=status_code)

    def for_each_child_node_call(self, parent_node_id: ua_types.UaNodeId,
                                 callback: Callable[[ua_types.UaNodeId, ua_types.UaBoolean, ua_types.UaNodeId], None]):
        status_code = lib.UA_Client_forEachChildNodeCall(self.ua_client,
                                                         parent_node_id._val,
                                                         lib.python_wrapper_UA_NodeIteratorCallback,
                                                         ffi.new_handle(callback))
        return ua_types.UaStatusCode(val=status_code)
