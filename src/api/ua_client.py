# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from typing import Callable

import ua_service_results_client as ClientServiceResult
from ua_consts_default_attributes import UA_ATTRIBUTES_DEFAULT
from ua_types_clientconfig import *
from ua_types_list import *


class _ClientCallback:
    """Aggregates static callback functions which execute the actual user submitted python callbacks

    _ClientCallback holds c type callback implementations which are being used to call the actual callback
    functions which have been submitted by the wrappy(o6) user. This is a workaround for the problem of not being able
    to create c function implementations at runtime.

    Note:
        Client callbacks are handled differently than server callbacks by wrappy(o6).
        This is the case because client callbacks are mostly utilized in asynchronous service calls which support the
        submission of `void* userData`. Through these generic parameters the actual
        python callback are being passed which can then be executed by static callback functions.
    """

    _callbacks = set()
    """
    Note:
        In order to prevent cases in which the owner of a callback handle "dies" prematurely which would cause 
        segmentation faults, wrappy(o6) enters all callback handles in the `_callbacks` set. This way the owner 
        of the memory will not be garbage collected automatically after the callback was triggered/unregistered. 
        Naturally the downside to this is that the memory will be cluttered if the client runs for a long time. If this 
        causes issues for API users they would currently need to implement a solution themselves to remove no longer 
        needed functions from the map. Users can find the registered handles in the `_handle` field which is contained in 
        the asynchronous service responses. 
    """

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncTranslateCallback(client, fun, request_id, tr):
        ffi.from_handle(fun)(UaClient(val=client),
                             UaUInt32(val=request_id, is_pointer=False),
                             UaTranslateBrowsePathsToNodeIdsResponse(val=tr, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncBrowseCallback(client, fun, request_id, wr):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaBrowseResponse(val=wr, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadDataTypeAttributeCallback(client, fun, request_id, var):
        ffi.from_handle(fun)(UaClient(val=client),
                             UaUInt32(val=request_id, is_pointer=False),
                             UaNodeId(val=var, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadNodeIdAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaNodeId(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadDescriptionAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaLocalizedText(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadWriteMaskAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaUInt32(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadUserWriteMaskAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaUInt32(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadIsAbstractAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaBoolean(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadSymmetricAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaBoolean(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadInverseNameAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaLocalizedText(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadContainsNoLoopsAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaBoolean(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadEventNotifierAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaByte(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadValueRankAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaInt32(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadAccessLevelAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaByte(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadUserAccessLevelAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaByte(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadExecutableAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaBoolean(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadUserExecutableAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaBoolean(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncCallCallback(client, fun, request_id, cr):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaCallResponse(val=cr, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadCallback(client, fun, request_id, rr):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaReadResponse(val=rr, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadValueAttributeCallback(client, fun, request_id, var):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaVariant(val=var, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadNodeClassAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaNodeClass(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadBrowseNameAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaQualifiedName(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadDisplayNameAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaLocalizedText(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadMinimumSamplingIntervalAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaDouble(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadHistorizingAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaBoolean(val=out, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncWriteCallback(client, fun, request_id, wr):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaWriteResponse(val=wr, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncAddNodesCallback(client, fun, request_id, ar):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             UaAddNodesResponse(val=ar, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncServiceCallback(client, fun, request_id, response):
        ffi.from_handle(fun)(UaClient(val=client), UaUInt32(val=request_id, is_pointer=False),
                             Void(val=response, is_pointer=False))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_NodeIteratorCallback(child_id, is_inverse, reference_type_id, fun):
        ffi.from_handle(fun)(UaNodeId(val=child_id, is_pointer=False),
                             UaBoolean(val=is_inverse, is_pointer=False),
                             UaNodeId(val=reference_type_id, is_pointer=False))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientCallback(client, fun):
        ffi.from_handle(fun)(UaClient(val=client))


class UaClient:
    def __init__(self, config: UaClientConfig = None, val=None):
        if val is not None:
            self.ua_client = val
        elif config is None:
            self.ua_client = lib.UA_Client_new()
            self.set_default_config()
        else:
            self.ua_client = lib.UA_Client_newWithConfig(config)

    # connection

    def connect(self, endpoint_url: str = 'opc.tcp://localhost:4840'):
        status_code = lib.UA_Client_connect(self.ua_client, bytes(endpoint_url, 'utf-8'))
        return UaStatusCode(val=status_code)

    def disconnect(self):
        status_code = lib.UA_Client_disconnect(self.ua_client)
        return UaStatusCode(val=status_code)

    def connect_secure_channel(self, endpoint_url: str = 'opc.tcp://localhost:4840'):
        status_code = lib.UA_Client_connectSecureChannel(self.ua_client, bytes(endpoint_url, 'utf-8'))
        return UaStatusCode(val=status_code)

    def disconnect_secure_channel(self):
        return UaStatusCode(val=lib.UA_Client_disconnectSecureChannel(self.ua_client))

    # low level service

    def service_read(self, request: UaReadRequest):
        ua_read_response = lib.UA_Client_Service_read(self.ua_client, request._val)
        return UaReadResponse(val=ua_read_response)

    def service_write(self, request: UaWriteRequest):
        ua_write_response = lib.UA_Client_Service_write(self.ua_client, request._val)
        return UaWriteResponse(val=ua_write_response)

    def service_call(self, request: UaCallRequest):
        ua_call_response = lib.UA_Client_Service_call(self.ua_client, request._val)
        return UaCallResponse(val=ua_call_response)

    def service_add_nodes(self, request: UaAddNodesRequest):
        ua_add_nodes_response = lib.UA_Client_Service_addNodes(self.ua_client, request._val)
        return UaAddNodesResponse(val=ua_add_nodes_response)

    def service_add_reference(self, request: UaAddReferencesRequest):
        ua_add_references_response = lib.UA_Client_Service_addReference(self.ua_client, request._val)
        return UaAddReferencesResponse(val=ua_add_references_response)

    def service_delete_nodes(self, request: UaDeleteNodesRequest):
        ua_delete_nodes_response = lib.UA_Client_Service_deleteNodes(self.ua_client, request._val)
        return UaDeleteNodesResponse(val=ua_delete_nodes_response)

    def service_delete_references(self, request: UaDeleteReferencesRequest):
        ua_delete_references_response = lib.UA_Client_Service_deleteReferences(self.ua_client, request._val)
        return UaDeleteReferencesResponse(val=ua_delete_references_response)

    def service_browse(self, request: UaBrowseRequest):
        ua_browse_response = lib.UA_Client_Service_browse(self.ua_client, request._val)
        return UaBrowseResponse(val=ua_browse_response)

    def service_browse_next(self, request: UaBrowseNextRequest):
        ua_browse_next_response = lib.UA_Client_Service_browseNext(self.ua_client, request._val)
        return UaBrowseNextResponse(val=ua_browse_next_response)

    def service_translate_browse_paths_to_node_ids(self, request: UaTranslateBrowsePathsToNodeIdsRequest):
        ua_translate_browse_paths_to_node_ids_response = lib.UA_Client_Service_translateBrowsePathsToNodeIds(
            self.ua_client, request._val)
        return UaTranslateBrowsePathsToNodeIdsResponse(val=ua_translate_browse_paths_to_node_ids_response)

    def service_register_node(self, request: UaRegisterNodesRequest):
        ua_register_nodes_response = lib.UA_Client_Service_registerNodes(self.ua_client, request._val)
        return UaRegisterNodesResponse(val=ua_register_nodes_response)

    def service_unregister_node(self, request: UaUnregisterNodesRequest):
        ua_unregister_nodes_response = lib.UA_Client_Service_unregisterNodes(self.ua_client, request._val)
        return UaUnregisterNodesResponse(val=ua_unregister_nodes_response)

    # high level read service
    def __read_attribute(self, node_id: UaNodeId, attribute_id: UaNodeId):
        out = Void()
        out_data_type = UaDataType()
        status_code = lib.__UA_Client_readAttribute(self.ua_client, node_id._ptr, attribute_id._val, out._ptr,
                                                    out_data_type._ptr)
        out_data_type._update()
        return ClientServiceResult.ReadAttributeResult(UaStatusCode(val=status_code), out, out_data_type)

    def read_node_id_attribute(self, node_id: UaNodeId):
        out_node_id = UaNodeId()
        status_code = lib.UA_Client_readNodeIdAttribute(self.ua_client, node_id._val, out_node_id._ptr)
        out_node_id._update()
        return ClientServiceResult.ReadNodeIdAttributeResult(UaStatusCode(val=status_code), out_node_id)

    def read_node_class_attribute(self, node_id: UaNodeId):
        out_node_class = UaNodeClass()
        status_code = lib.UA_Client_readNodeClassAttribute(self.ua_client, node_id._val, out_node_class._ptr)
        return ClientServiceResult.ReadNodeClassAttributeResult(UaStatusCode(val=status_code), out_node_class)

    def read_browse_name_attribute(self, node_id: UaNodeId):
        out_browse_name = UaQualifiedName()
        status_code = lib.UA_Client_readBrowseNameAttribute(self.ua_client, node_id._val, out_browse_name._ptr)
        out_browse_name._update()
        return ClientServiceResult.ReadBrowseNameAttributeResult(UaStatusCode(val=status_code),
                                                                 out_browse_name)

    def read_display_name_attribute(self, node_id: UaNodeId):
        out_display_name = UaLocalizedText()
        status_code = lib.UA_Client_readDisplayNameAttribute(self.ua_client, node_id._val, out_display_name._ptr)
        out_display_name._update()
        return ClientServiceResult.ReadDisplayNameAttributeResult(UaStatusCode(val=status_code),
                                                                  out_display_name)

    def read_description_attribute(self, node_id: UaNodeId):
        out_description = UaLocalizedText()
        status_code = lib.UA_Client_readDescriptionAttribute(self.ua_client, node_id._val, out_description._ptr)
        out_description._update()
        return ClientServiceResult.ReadDescriptionAttributeResult(UaStatusCode(val=status_code),
                                                                  out_description)

    def read_write_mask_attribute(self, node_id: UaNodeId):
        out_write_mask = UaUInt32()
        status_code = lib.UA_Client_readWriteMaskAttribute(self.ua_client, node_id._val, out_write_mask._ptr)
        return ClientServiceResult.ReadWriteMaskAttributeResult(UaStatusCode(val=status_code), out_write_mask)

    def read_user_write_mask_attribute(self, node_id: UaNodeId):
        out_user_write_mask = UaUInt32()
        status_code = lib.UA_Client_readUserWriteMaskAttribute(self.ua_client, node_id._val, out_user_write_mask._ptr)
        return ClientServiceResult.ReadUserWriteMaskAttributeResult(UaStatusCode(val=status_code),
                                                                    out_user_write_mask)

    def read_is_abstract_attribute(self, node_id: UaNodeId):
        out_is_abstract = UaBoolean()
        status_code = lib.UA_Client_readIsAbstractAttribute(self.ua_client, node_id._val, out_is_abstract._ptr)
        return ClientServiceResult.ReadIsAbstractAttributeResult(UaStatusCode(val=status_code),
                                                                 out_is_abstract)

    def read_symmetric_attribute(self, node_id: UaNodeId):
        out_symmetric = UaBoolean()
        status_code = lib.UA_Client_readSymmetricAttribute(self.ua_client, node_id._val, out_symmetric._ptr)
        return ClientServiceResult.ReadSymmetricAttributeResult(UaStatusCode(val=status_code), out_symmetric)

    def read_inverse_name_attribute(self, node_id: UaNodeId):
        out_inverse_name = UaLocalizedText()
        status_code = lib.UA_Client_readInverseNameAttribute(self.ua_client, node_id._val, out_inverse_name._ptr)
        out_inverse_name._update()
        return ClientServiceResult.ReadInverseNameAttributeResult(UaStatusCode(val=status_code),
                                                                  out_inverse_name)

    def read_contains_no_loops_attribute(self, node_id: UaNodeId):
        out_contains_no_loops = UaBoolean()
        status_code = lib.UA_Client_readContainsNoLoopsAttribute(self.ua_client, node_id._val,
                                                                 out_contains_no_loops._ptr)
        return ClientServiceResult.ReadContainsNoLoopsAttributeResult(UaStatusCode(val=status_code),
                                                                      out_contains_no_loops)

    def read_event_notifier_attribute(self, node_id: UaNodeId):
        out_event_notifier = UaByte()
        status_code = lib.UA_Client_readEventNotifierAttribute(self.ua_client, node_id._val, out_event_notifier._ptr)
        return ClientServiceResult.ReadEventNotifierAttributeResult(UaStatusCode(val=status_code),
                                                                    out_event_notifier)

    def read_value_attribute(self, node_id: UaNodeId):
        value = UaVariant()
        status_code = lib.UA_Client_readValueAttribute(self.ua_client, node_id._val, value._ptr)
        value._update()
        return ClientServiceResult.ReadValueAttributeResult(UaStatusCode(val=status_code), value)

    def read_data_type_attribute(self, node_id: UaNodeId):
        out_data_type = UaNodeId()
        status_code = lib.UA_Client_readDataTypeAttribute(self.ua_client, node_id._val, out_data_type._ptr)
        out_data_type._update()
        return ClientServiceResult.ReadDataTypeAttribute(UaStatusCode(val=status_code), out_data_type)

    def read_value_rank_attribute(self, node_id: UaNodeId):
        out_value_rank = UaInt32()
        status_code = lib.UA_Client_readValueRankAttribute(self.ua_client, node_id._val, out_value_rank._ptr)
        return ClientServiceResult.ReadValueRankAttribute(UaStatusCode(val=status_code), out_value_rank)

    # todo: use UaList for out_array_dimensions"
    def read_array_dimensions_attribute(self, node_id: UaNodeId):
        out_array_dimensions_size = SizeT()
        out_array_dimensions = ffi.new("UA_UInt32 **")
        status_code = lib.UA_Client_readArrayDimensionsAttribute(self.ua_client, node_id._val,
                                                                 out_array_dimensions_size._ptr,
                                                                 out_array_dimensions)
        return ClientServiceResult.ReadArrayDimensionsAttributeResult(UaStatusCode(val=status_code),
                                                                      out_array_dimensions_size,
                                                                      out_array_dimensions)  # todo: fix return value

    def read_access_level_attribute(self, node_id: UaNodeId):
        out_access_level = UaByte()
        status_code = lib.UA_Client_readAccessLevelAttribute(self.ua_client, node_id._val, out_access_level._ptr)
        return ClientServiceResult.ReadAccessLevelAttributeResult(UaStatusCode(val=status_code),
                                                                  out_access_level)

    def read_user_access_level_attribute(self, node_id: UaNodeId):
        out_user_access_level = UaByte()
        status_code = lib.UA_Client_readUserAccessLevelAttribute(self.ua_client, node_id._val,
                                                                 out_user_access_level._ptr)
        return ClientServiceResult.ReadUserAccessLevelAttributeResult(UaStatusCode(val=status_code),
                                                                      out_user_access_level)

    def read_minimum_sampling_interval_attribute(self, node_id: UaNodeId):
        out_min_sampling_interval = UaDouble()
        status_code = lib.UA_Client_readMinimumSamplingIntervalAttribute(self.ua_client, node_id._val,
                                                                         out_min_sampling_interval._ptr)
        return ClientServiceResult.ReadMinimumSamplingIntervalAttributeResult(UaStatusCode(val=status_code),
                                                                              out_min_sampling_interval)

    def read_executable_attribute(self, node_id: UaNodeId):
        out_executable = UaBoolean()
        status_code = lib.UA_Client_readExecutableAttribute(self.ua_client, node_id._val, out_executable._ptr)
        return ClientServiceResult.ReadExecutableAttributeResult(UaStatusCode(val=status_code), out_executable)

    def read_user_executable_attribute(self, node_id: UaNodeId):
        out_user_executable = UaBoolean()
        status_code = lib.UA_Client_readUserExecutableAttribute(self.ua_client, node_id._val, out_user_executable._ptr)
        return ClientServiceResult.ReadUserExecutableAttributeResult(UaStatusCode(val=status_code),
                                                                     out_user_executable)

    # high level write service

    def write_node_id_attribute(self, node_id: UaNodeId, new_node_id: UaNodeId):
        status_code = lib.UA_Client_writeNodeIdAttribute(self.ua_client, node_id._val, new_node_id._ptr)
        new_node_id._update()
        return UaStatusCode(val=status_code)

    def write_node_class_attribute(self, node_id: UaNodeId, new_node_class: UaNodeClass):
        status_code = lib.UA_Client_writeNodeClassAttribute(self.ua_client, node_id._val, new_node_class._ptr)
        return UaStatusCode(val=status_code)

    def write_browse_name_attribute(self, node_id: UaNodeId, new_browse_name: UaQualifiedName):
        status_code = lib.UA_Client_writeBrowseNameAttribute(self.ua_client, node_id._val, new_browse_name._ptr)
        return UaStatusCode(val=status_code)

    def write_display_name_attribute(self, node_id: UaNodeId, new_display_name: UaLocalizedText):
        status_code = lib.UA_Client_writeDisplayNameAttribute(self.ua_client, node_id._val, new_display_name._ptr)
        return UaStatusCode(val=status_code)

    def write_description_attribute(self, node_id: UaNodeId, new_description: UaLocalizedText):
        status_code = lib.UA_Client_writeDescriptionAttribute(self.ua_client, node_id._val, new_description._ptr)
        return UaStatusCode(val=status_code)

    def write_write_mask_attribute(self, node_id: UaNodeId, new_write_mask: UaUInt32):
        status_code = lib.UA_Client_writeWriteMaskAttribute(self.ua_client, node_id._val, new_write_mask._ptr)
        return UaStatusCode(val=status_code)

    def write_user_write_mask_attribute(self, node_id: UaNodeId, new_user_write_mask: UaUInt32):
        status_code = lib.UA_Client_writeUserWriteMaskAttribute(self.ua_client, node_id._val, new_user_write_mask._ptr)
        return UaStatusCode(val=status_code)

    def write_is_abstract_attribute(self, node_id: UaNodeId, new_is_abstract: UaBoolean):
        status_code = lib.UA_Client_writeIsAbstractAttribute(self.ua_client, node_id._val, new_is_abstract._ptr)
        return UaStatusCode(val=status_code)

    def write_symmetric_attribute(self, node_id: UaNodeId, new_symmetric: UaBoolean):
        status_code = lib.UA_Client_writeSymmetricAttribute(self.ua_client, node_id._val, new_symmetric._ptr)
        return UaStatusCode(val=status_code)

    def write_inverse_name_attribute(self, node_id: UaNodeId, new_inverse_name: UaLocalizedText):
        status_code = lib.UA_Client_writeInverseNameAttribute(self.ua_client, node_id._val, new_inverse_name._ptr)
        return UaStatusCode(val=status_code)

    def write_contains_no_loops_attribute(self, node_id: UaNodeId, new_contains_no_loops: UaBoolean):
        status_code = lib.UA_Client_writeContainsNoLoopsAttribute(self.ua_client, node_id._val,
                                                                  new_contains_no_loops._ptr)
        return UaStatusCode(val=status_code)

    def write_event_notifier_attribute(self, node_id: UaNodeId, new_event_notifier: UaByte):
        status_code = lib.UA_Client_writeEventNotifierAttribute(self.ua_client, node_id._val, new_event_notifier._ptr)
        return UaStatusCode(val=status_code)

    def write_value_attribute(self, node_id: UaNodeId, new_value: UaVariant):
        status_code = lib.UA_Client_writeValueAttribute(self.ua_client, node_id._val, new_value._ptr)
        return UaStatusCode(val=status_code)

    def write_data_type_attribute(self, node_id: UaNodeId, new_data_type: UaNodeId):
        status_code = lib.UA_Client_writeDataTypeAttribute(self.ua_client, node_id._val, new_data_type._ptr)
        return UaStatusCode(val=status_code)

    def write_value_rank_attribute(self, node_id: UaNodeId, new_value_rank: UaInt32):
        status_code = lib.UA_Client_writeValueRankAttribute(self.ua_client, node_id._val, new_value_rank._ptr)
        return UaStatusCode(val=status_code)

    def write_array_dimensions_attribute(self, node_id: UaNodeId, new_array_dimensions_size: SizeT,
                                         new_array_dimensions: UaUInt32):
        status_code = lib.UA_Client_writeArrayDimensionsAttribute(self.ua_client, node_id._val,
                                                                  new_array_dimensions_size._val,
                                                                  new_array_dimensions._ptr)
        return UaStatusCode(val=status_code)

    def write_access_level_attribute(self, node_id: UaNodeId, new_access_level: UaByte):
        status_code = lib.UA_Client_writeAccessLevelAttribute(self.ua_client, node_id._val, new_access_level._ptr)
        return UaStatusCode(val=status_code)

    def write_user_access_level_attribute(self, node_id: UaNodeId, new_user_access_level: UaByte):
        status_code = lib.UA_Client_writeUserAccessLevelAttribute(self.ua_client, node_id._val,
                                                                  new_user_access_level._ptr)
        return UaStatusCode(val=status_code)

    def write_minimum_sampling_interval_attribute(self, node_id: UaNodeId,
                                                  new_min_interval: UaDouble):
        status_code = lib.UA_Client_writeMinimumSamplingIntervalAttribute(self.ua_client, node_id._val,
                                                                          new_min_interval._ptr)
        return UaStatusCode(val=status_code)

    def write_executable_attribute(self, node_id: UaNodeId, new_executable: UaBoolean):
        status_code = lib.UA_Client_writeExecutableAttribute(self.ua_client, node_id._val, new_executable._ptr)
        return UaStatusCode(val=status_code)

    def write_user_executable_attribute(self, node_id: UaNodeId, new_user_executable: UaBoolean):
        status_code = lib.UA_Client_writeUserExecutableAttribute(self.ua_client, node_id._val, new_user_executable._ptr)
        return UaStatusCode(val=status_code)

    # misc high level service

    def call(self, object_id: UaNodeId, method_id: UaNodeId,
             call_input: Union[UaList, UaVariant]):
        output_size = SizeT()

        input_size = SizeT(1)
        if type(call_input) is UaList:
            input_size = SizeT(call_input._size)

        # Todo: use UaList
        output = ffi.new("UA_Variant **")
        status_code = lib.UA_Client_call(self.ua_client, object_id._val, method_id._val, input_size._val,
                                         call_input._ptr, output_size._ptr,
                                         output)
        return ClientServiceResult.CallResult(UaStatusCode(val=status_code), output_size,
                                              UaList(val=output[0], size=output_size,
                                                     ua_class=UaVariant))  # todo: list handling has to be adapted here

    def add_reference(self, source_node_id: UaNodeId, reference_type_id: UaNodeId,
                      is_forward: UaBoolean,
                      target_server_uri: UaString, target_node_id: UaExpandedNodeId,
                      target_node_class: UaNodeClass):
        status_code = lib.UA_Client_addReference(self.ua_client, source_node_id._val, reference_type_id._val,
                                                 is_forward._val,
                                                 target_server_uri._val, target_node_id._val, target_node_class._val)
        return UaStatusCode(val=status_code)

    def delete_reference(self, source_node_id: UaNodeId, reference_type_id: UaNodeId,
                         is_forward: UaBoolean,
                         target_node_id: UaExpandedNodeId, delete_bidirectional: UaBoolean):
        status_code = lib.UA_Client_deleteReference(self.ua_client, source_node_id._val, reference_type_id._val,
                                                    is_forward._val,
                                                    target_node_id._val, delete_bidirectional._val)
        return UaStatusCode(val=status_code)

    def delete_node(self, node_id: UaNodeId, delete_target_references: UaBoolean):
        status_code = lib.UA_Client_deleteNode(self.ua_client, node_id._val, delete_target_references._val)
        return UaStatusCode(val=status_code)

    # high level add node services

    def add_variable_node(self, parent_node_id: UaNodeId,
                          reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                          type_definition: UaNodeId,
                          requested_new_node_id: UaNodeId = None,
                          attr: UaVariableAttributes = None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.VARIABLE

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        out_new_node_id = UaNodeId()
        status_code = lib.UA_Client_addVariableNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                    reference_type_id._val, browse_name._val, type_definition._val,
                                                    attr._val,
                                                    out_new_node_id._ptr)
        out_new_node_id._update()
        return ClientServiceResult.AddNodeResult(UaStatusCode(val=status_code), out_new_node_id)

    def add_variable_type_node(self, parent_node_id: UaNodeId,
                               reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                               requested_new_node_id: UaNodeId = None,
                               attr: UaVariableTypeAttributes = None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.VARIABLE_TYPE

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        out_new_node_id = UaNodeId()
        status_code = lib.UA_Client_addVariableTypeNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                        reference_type_id._val, browse_name._val, attr._val,
                                                        out_new_node_id._ptr)
        out_new_node_id._update()
        return ClientServiceResult.AddNodeResult(UaStatusCode(val=status_code), out_new_node_id)

    def add_object_node(self, parent_node_id: UaNodeId,
                        reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                        type_definition: UaNodeId,
                        requested_new_node_id: UaNodeId = None,
                        attr: UaObjectAttributes = None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.OBJECT

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        out_new_node_id = UaNodeId()
        status_code = lib.UA_Client_addObjectNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                  reference_type_id._val, browse_name._val, type_definition._val,
                                                  attr._val,
                                                  out_new_node_id._ptr)
        out_new_node_id._update()
        return ClientServiceResult.AddNodeResult(UaStatusCode(val=status_code), out_new_node_id)

    def add_object_type_node(self, parent_node_id: UaNodeId,
                             reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                             requested_new_node_id: UaNodeId = None,
                             attr: UaObjectTypeAttributes = None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.OBJECT_TYPE

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        out_new_node_id = UaNodeId()
        status_code = lib.UA_Client_addObjectTypeNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                      reference_type_id._val, browse_name._val, attr._val,
                                                      out_new_node_id._ptr)
        out_new_node_id._update()
        return ClientServiceResult.AddNodeResult(UaStatusCode(val=status_code), out_new_node_id)

    def add_view_node(self, parent_node_id: UaNodeId,
                      reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                      requested_new_node_id: UaNodeId = None,
                      attr: UaViewAttributes = None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.VIEW

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        out_new_node_id = UaNodeId()
        status_code = lib.UA_Client_addViewNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                reference_type_id._val, browse_name._val, attr._val,
                                                out_new_node_id._ptr)
        out_new_node_id._update()
        return ClientServiceResult.AddNodeResult(UaStatusCode(val=status_code), out_new_node_id)

    def add_reference_type_node(self, parent_node_id: UaNodeId,
                                reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                                requested_new_node_id: UaNodeId = None,
                                attr: UaReferenceTypeAttributes = None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.REFERENCE_TYPE

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        out_new_node_id = UaNodeId()
        status_code = lib.UA_Client_addReferenceTypeNode(self.ua_client, requested_new_node_id._val,
                                                         parent_node_id._val,
                                                         reference_type_id._val, browse_name._val, attr._val,
                                                         out_new_node_id._ptr)
        out_new_node_id._update()
        return ClientServiceResult.AddNodeResult(UaStatusCode(val=status_code), out_new_node_id)

    def add_data_type_node(self, parent_node_id: UaNodeId,
                           reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                           requested_new_node_id: UaNodeId = None,
                           attr: UaDataTypeAttributes = None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.DATA_TYPE

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        out_new_node_id = UaNodeId()
        status_code = lib.UA_Client_addDataTypeNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                    reference_type_id._val, browse_name._val, attr._val,
                                                    out_new_node_id._ptr)
        out_new_node_id._update()
        return ClientServiceResult.AddNodeResult(UaStatusCode(val=status_code), out_new_node_id)

    def add_method_node(self, parent_node_id: UaNodeId,
                        reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                        requested_new_node_id: UaNodeId = None,
                        attr: UaMethodAttributes = None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.METHOD

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        out_new_node_id = UaNodeId()
        status_code = lib.UA_Client_addMethodNode(self.ua_client, requested_new_node_id._val, parent_node_id._val,
                                                  reference_type_id._val, browse_name._val, attr._val,
                                                  out_new_node_id._ptr)
        out_new_node_id._update()
        return ClientServiceResult.AddNodeResult(UaStatusCode(val=status_code), out_new_node_id)

    # utils
    # todo: wrap config once UA_Logger type is available
    def get_config(self):
        return lib.UA_Client_getConfig(self.ua_client)

    # todo: adapt once UA_Logger type is available and get_config has been wrapped
    def set_default_config(self):
        lib.UA_ClientConfig_setDefault(self.get_config())

    def find_data_type(self, type_id: UaNodeId):
        return UaDataType(val=lib.UA_Client_findDataType(self.ua_client, type_id._ptr), is_pointer=True)

    # todo: endpoint_descriptions is of type UA_EndpointDescription** --> array with multiple entries?
    def get_endpoints(self, server_url: str, endpoint_descriptions_size: SizeT,
                      endpoint_descriptions: UaApplicationDescription):
        status_code = lib.UA_Client_getEndpoints(self.ua_client, server_url, endpoint_descriptions_size,
                                                 endpoint_descriptions)
        return UaStatusCode(val=status_code)

    # todo: registered_servers is of type UA_ApplicationDescription ** --> array with multiple entries?
    def find_servers(self, server_url: str, server_uris_size: SizeT, locale_ids_size: SizeT,
                     locale_ids: UaString, registered_servers_size: SizeT,
                     registered_servers: UaApplicationDescription):
        status_code = lib.UA_Client_findServers(self.ua_client, server_url, server_uris_size, locale_ids_size,
                                                locale_ids,
                                                registered_servers_size, registered_servers)
        return UaStatusCode(val=status_code)

    def run_iterate(self, timeout: UaUInt32):
        status_code = lib.UA_Client_run_iterate(self.ua_client, timeout._val)
        return UaStatusCode(val=status_code)

    #    def find_servers_on_network(self, server_url, starting_record_id, max_records_to_return,
    #                                server_capability_filter_size, server_on_network_size, server_on_network):
    #        return lib.UA_Client_findServersOnNetwork(self.ua_client, server_url, starting_record_id, max_records_to_return,
    #                                                  server_capability_filter_size, server_on_network_size,
    #                                                  server_on_network)

    # ASYNC
    # important remark: In order to work with asyncronous functions you absolutely have to make sure to keep a variable alive which holds the _handle value of the response until you are done with the callback.
    # if the reference is lost prematurely, CFFI will garbage collect the void* handle of the callback function as it has no owner anymore! You could for example add the handle to a dictonary which stores all active callbacks and remove it once it's no longer needed

    # async read service
    def send_async_read_request(self, request: UaReadRequest,
                                callback: Callable[['UaClient', UaUInt32, UaVariant], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_sendAsyncReadRequest(self.ua_client,
                                                         request._ptr,
                                                         lib.python_wrapper_UA_ClientAsyncReadCallback,
                                                         _handle,
                                                         req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def __read_attribute_async(self, node_id: UaNodeId, attribute_id: UaAttributeId,
                               callback: Callable[['UaClient', UaUInt32, Void], None]):
        out_data_type = UaDataType()
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.__UA_Client_readAttribute_async(self.ua_client,
                                                          node_id._ptr,
                                                          attribute_id._val,
                                                          out_data_type._ptr,
                                                          lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                          _handle,
                                                          req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_data_type_attribute_async(self, node_id: UaNodeId,
                                       callback: Callable[['UaClient', UaUInt32, UaNodeId], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readDataTypeAttribute_async(self.ua_client,
                                                                node_id._val,
                                                                lib.python_wrapper_UA_ClientAsyncReadDataTypeAttributeCallback,
                                                                _handle,
                                                                req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_value_attribute_async(self, node_id: UaNodeId,
                                   callback: Callable[['UaClient', UaUInt32, UaVariant], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readValueAttribute_async(self.ua_client,
                                                             node_id._val,
                                                             lib.python_wrapper_UA_ClientAsyncReadValueAttributeCallback,
                                                             _handle,
                                                             req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_node_id_attribute_async(self, node_id: UaNodeId,
                                     callback: Callable[['UaClient', UaUInt32, UaNodeId], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readNodeIdAttribute_async(self.ua_client,
                                                              node_id._val,
                                                              lib.python_wrapper_UA_ClientAsyncReadNodeIdAttributeCallback,
                                                              _handle,
                                                              req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_node_class_attribute_async(self, node_id: UaNodeId,
                                        callback: Callable[
                                            ['UaClient', UaUInt32, UaNodeClass], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readNodeClassAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 lib.python_wrapper_UA_ClientAsyncReadNodeClassAttributeCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_browse_name_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, UaQualifiedName], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readBrowseNameAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  lib.python_wrapper_UA_ClientAsyncReadBrowseNameAttributeCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_display_name_attribute_async(self, node_id: UaNodeId,
                                          callback: Callable[
                                              ['UaClient', UaUInt32, UaLocalizedText], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readDisplayNameAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadDisplayNameAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_description_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, UaLocalizedText], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readDescriptionAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadDescriptionAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_write_mask_attribute_async(self, node_id: UaNodeId,
                                        callback: Callable[['UaClient', UaUInt32, UaUInt32], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readWriteMaskAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 lib.python_wrapper_UA_ClientAsyncReadWriteMaskAttributeCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_user_write_mask_attribute_async(self, node_id: UaNodeId,
                                             callback: Callable[
                                                 ['UaClient', UaUInt32, UaUInt32], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readUserWriteMaskAttribute_async(self.ua_client,
                                                                     node_id._val,
                                                                     lib.python_wrapper_UA_ClientAsyncReadUserWriteMaskAttributeCallback,
                                                                     _handle,
                                                                     req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_is_abstract_attribute_async(self, node_id: UaNodeId,
                                         callback: Callable[['UaClient', UaUInt32, UaBoolean], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readIsAbstractAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  lib.python_wrapper_UA_ClientAsyncReadIsAbstractAttributeCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_symmetric_attribute_async(self, node_id: UaNodeId,
                                       callback: Callable[['UaClient', UaUInt32, UaBoolean], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readSymmetricAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 lib.python_wrapper_UA_ClientAsyncReadSymmetricAttributeCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_inverse_name_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, UaLocalizedText], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readInverseNameAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadInverseNameAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_contains_no_loops_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, UaBoolean], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readContainsNoLoopsAttribute_async(self.ua_client,
                                                                       node_id._val,
                                                                       lib.python_wrapper_UA_ClientAsyncReadContainsNoLoopsAttributeCallback,
                                                                       _handle,
                                                                       req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_event_notifier_attribute_async(self, node_id: UaNodeId,
                                            callback: Callable[['UaClient', UaUInt32, UaByte], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readEventNotifierAttribute_async(self.ua_client,
                                                                     node_id._val,
                                                                     lib.python_wrapper_UA_ClientAsyncReadEventNotifierAttributeCallback,
                                                                     _handle,
                                                                     req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_value_rank_attribute_async(self, node_id: UaNodeId,
                                        callback: Callable[['UaClient', UaUInt32, UaUInt32], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readValueRankAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 lib.python_wrapper_UA_ClientAsyncReadValueRankAttributeCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_access_level_attribute_async(self, node_id: UaNodeId,
                                          callback: Callable[['UaClient', UaUInt32, UaByte], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readAccessLevelAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadAccessLevelAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_user_access_level_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, UaByte], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readUserAccessLevelAttribute_async(self.ua_client,
                                                                       node_id._val,
                                                                       lib.python_wrapper_UA_ClientAsyncReadUserAccessLevelAttributeCallback,
                                                                       _handle,
                                                                       req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_minimum_sampling_interval_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, UaDouble], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readMinimumSamplingIntervalAttribute_async(self.ua_client,
                                                                               node_id._val,
                                                                               lib.python_wrapper_UA_ClientAsyncReadMinimumSamplingIntervalAttributeCallback,
                                                                               _handle,
                                                                               req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_historizing_attribute_async(self, node_id: UaNodeId,
                                         callback: Callable[['UaClient', UaUInt32, UaBoolean], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readHistorizingAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   lib.python_wrapper_UA_ClientAsyncReadHistorizingAttributeCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_executable_attribute_async(self, node_id: UaNodeId,
                                        callback: Callable[['UaClient', UaUInt32, UaBoolean], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_readExecutableAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  lib.python_wrapper_UA_ClientAsyncReadExecutableAttributeCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def read_user_executable_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, UaBoolean], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.readUserExecutableAttribute_async(self.ua_client,
                                                            node_id._val,
                                                            lib.python_wrapper_UA_ClientAsyncReadUserExecutableAttributeCallback,
                                                            _handle,
                                                            req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    # async write service
    def send_async_write_request(self, request: UaWriteRequest,
                                 callback: Callable[['UaClient', UaUInt32, UaWriteResponse], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_sendAsyncWriteRequest(self.ua_client,
                                                          request._ptr,
                                                          lib.python_wrapper_UA_ClientAsyncWriteCallback,
                                                          _handle,
                                                          req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def __write_attribute_async(self, node_id: UaNodeId, attribute_id: UaAttributeId,
                                _in: Void,
                                in_data_type: UaDataType,
                                callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.__UA_Client_writeAttribute_async(self.ua_client,
                                                           node_id._ptr,
                                                           attribute_id._val,
                                                           _in._ptr,
                                                           in_data_type._ptr,
                                                           lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                           _handle,
                                                           req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_value_attribute_async(self, node_id: UaNodeId, new_value: UaVariant,
                                    callback: Callable[
                                        ['UaClient', UaUInt32, UaWriteResponse], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        status_code = lib.UA_Client_writeValueAttribute_async(self.ua_client,
                                                              node_id._val,
                                                              new_value._ptr,
                                                              lib.python_wrapper_UA_ClientAsyncWriteCallback,
                                                              _handle,
                                                              req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_node_id_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_node_id = UaNodeId()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeNodeIdAttribute_async(self.ua_client,
                                                               node_id._val,
                                                               out_node_id._ptr,
                                                               lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                               _handle,
                                                               req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_node_class_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_node_class = UaNodeClass()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeNodeClassAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  out_node_class._ptr,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_browse_name_attribute_async(self, node_id: UaNodeId,
                                          callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_browse_name = UaQualifiedName()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeBrowseNameAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   out_browse_name._ptr,
                                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_display_name_attribute_async(self, node_id: UaNodeId,
                                           callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_display_name = UaLocalizedText()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeDisplayNameAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    out_display_name._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_description_attribute_async(self, node_id: UaNodeId,
                                          callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_description = UaLocalizedText()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeDescriptionAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    out_description._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_write_mask_attribute_async(self, node_id: UaNodeId,
                                         callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_write_mask = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeWriteMaskAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  out_write_mask._ptr,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_user_write_mask_attribute_async(self, node_id: UaNodeId,
                                              callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_user_write_mask = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeUserWriteMaskAttribute_async(self.ua_client,
                                                                      node_id._val,
                                                                      out_user_write_mask._ptr,
                                                                      lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                      _handle,
                                                                      req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_is_abstract_attribute_async(self, node_id: UaNodeId,
                                          callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_is_abstract = UaBoolean()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeIsAbstractAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   out_is_abstract._ptr,
                                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_symmetric_attribute_async(self, node_id: UaNodeId,
                                        callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_symmetric = UaBoolean()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeSymmetricAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  out_symmetric._ptr,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_inverse_name_attribute_async(self, node_id: UaNodeId,
                                           callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_inverse_name = UaLocalizedText()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeInverseNameAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    out_inverse_name._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_contains_no_loops_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_contains_no_loops = UaBoolean()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeContainsNoLoopsAttribute_async(self.ua_client,
                                                                        node_id._val,
                                                                        out_contains_no_loops._ptr,
                                                                        lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                        _handle,
                                                                        req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_event_notifier_attribute_async(self, node_id: UaNodeId,
                                             callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_event_notifier = UaByte()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeEventNotifierAttribute_async(self.ua_client,
                                                                      node_id._val,
                                                                      out_event_notifier._ptr,
                                                                      lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                      _handle,
                                                                      req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_data_type_attribute_async(self, node_id: UaNodeId,
                                        callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_data_type = UaNodeId()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeDataTypeAttribute_async(self.ua_client,
                                                                 node_id._val,
                                                                 out_data_type._ptr,
                                                                 lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                 _handle,
                                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_value_rank_attribute_async(self, node_id: UaNodeId,
                                         callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_value_rank = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeValueRankAttribute_async(self.ua_client,
                                                                  node_id._val,
                                                                  out_value_rank._ptr,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  _handle,
                                                                  req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_access_level_attribute_async(self, node_id: UaNodeId,
                                           callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_access_level = UaByte()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeAccessLevelAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    out_access_level._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_user_access_level_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_user_access_level = UaByte()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeUserAccessLevelAttribute_async(self.ua_client,
                                                                        node_id._val,
                                                                        out_user_access_level._ptr,
                                                                        lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                        _handle,
                                                                        req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    # todo: check if this is correct. this is different in the synchronous version. the naming of out_minimum_sampling_interval suggests that it is a return value but I think it is evaluated by the service again as an argument
    # for now we adapted the naming to match the syncronous version
    # could be the case that new_min_interval is altered by open62541 --> check this to see if we need to make a copy to prevent side effect
    def write_minimum_sampling_interval_attribute_async(self, node_id: UaNodeId, callback: Callable[
        ['UaClient', UaUInt32, Void], None],
                                                        new_min_interval: UaDouble):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeMinimumSamplingIntervalAttribute_async(self.ua_client,
                                                                                node_id._val,
                                                                                new_min_interval._val,
                                                                                lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                                _handle,
                                                                                req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    # todo: check if this is correct. this is different in the synchronous version
    # for now adapted naming to match syncronous method as this seems to make the most sense
    # could be the case that new_historizing is altered by open62541 --> check this to see if we need to make a copy to prevent side effect
    def write_historizing_attribute_async(self, node_id: UaNodeId,
                                          callback: Callable[['UaClient', UaUInt32, Void], None],
                                          new_historizing: UaBoolean):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeHistorizingAttribute_async(self.ua_client,
                                                                    node_id._val,
                                                                    new_historizing._ptr,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    _handle,
                                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_executable_attribute_async(self, node_id: UaNodeId,
                                         callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_executable = UaBoolean()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeExecutableAttribute_async(self.ua_client,
                                                                   node_id._val,
                                                                   out_executable._ptr,
                                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                   _handle,
                                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def write_user_executable_attribute_async(self, node_id: UaNodeId,
                                              callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        out_user_executable = UaBoolean()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_writeUserExecutableAttribute_async(self.ua_client,
                                                                       node_id._val,
                                                                       out_user_executable._ptr,
                                                                       lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                       _handle,
                                                                       req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    # call service
    # todo: can we get rid of input_size, calculate it ourselves and hide it from users?
    def _call_async(self, object_id: UaNodeId, method_id: UaNodeId, input_size: SizeT,
                    _input: UaVariant,
                    callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.__UA_Client_call_async(self.ua_client,
                                                 object_id._val,
                                                 method_id._val,
                                                 input_size._val,
                                                 _input._ptr,
                                                 lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                 _handle,
                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    # todo: can we get rid of input_size, calculate it ourselves and hide it from users?
    def call_async(self, object_id: UaNodeId, method_id: UaNodeId, input_size: SizeT,
                   _input: UaVariant,
                   callback: Callable[['UaClient', UaUInt32, UaCallResponse], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.__UA_Client_call_async(self.ua_client,
                                                 object_id._val,
                                                 method_id._val,
                                                 input_size._val,
                                                 _input._ptr,
                                                 lib.python_wrapper_UA_ClientAsyncCallCallback,
                                                 _handle,
                                                 req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    # add node service
    def add_variable_node_async(self, parent_node_id: UaNodeId,
                                reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                                type_definition: UaNodeId,
                                callback: Callable[['UaClient', UaUInt32, UaAddNodesResponse], None],
                                requested_new_node_id: UaNodeId = None,
                                attr: UaVariableAttributes = UA_ATTRIBUTES_DEFAULT.VARIABLE):

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        out_new_node_id = UaNodeId()
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
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
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def __add_node_async(self, node_class: UaNodeClass,
                         parent_node_id: UaNodeId, reference_type_id: UaNodeId,
                         browse_name: UaQualifiedName, type_definition: UaNodeId, attr,
                         attribute_type: UaDataType,
                         callback: Callable[['UaClient', UaUInt32, Void], None],
                         requested_new_node_id: UaNodeId = None):

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)

        out_new_node_id = UaNodeId()
        req_id = UaUInt32()
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
                                                    _handle,
                                                    req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def add_variable_type_node_async(self, parent_node_id: UaNodeId,
                                     reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                                     callback: Callable[
                                         ['UaClient', UaUInt32, UaAddNodesResponse], None],
                                     requested_new_node_id: UaNodeId = None,
                                     attr=None):

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.VARIABLE_TYPE

        out_new_node_id = UaNodeId()
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
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
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def add_object_node_async(self, parent_node_id: UaNodeId,
                              reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                              type_definition: UaNodeId,
                              callback: Callable[['UaClient', UaUInt32, UaAddNodesResponse], None],
                              requested_new_node_id: UaNodeId = None,
                              attr=None):

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.OBJECT

        out_new_node_id = UaNodeId()
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
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
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def add_object_type_node_async(self, parent_node_id: UaNodeId,
                                   reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                                   callback: Callable[
                                       ['UaClient', UaUInt32, UaAddNodesResponse], None],
                                   requested_new_node_id: UaNodeId = None,
                                   attr=None):

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.OBJECT_TYPE

        out_new_node_id = UaNodeId()
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
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
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def add_view_node_async(self, parent_node_id: UaNodeId,
                            reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                            callback: Callable[['UaClient', UaUInt32, UaAddNodesResponse], None],
                            requested_new_node_id: UaNodeId = None,
                            attr=None):

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.VIEW

        out_new_node_id = UaNodeId()
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
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
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def add_reference_type_node_async(self, parent_node_id: UaNodeId,
                                      reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                                      callback: Callable[
                                          ['UaClient', UaUInt32, UaAddNodesResponse], None],
                                      requested_new_node_id: UaNodeId = None,
                                      attr=None):
        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.REFERENCE_TYPE

        out_new_node_id = UaNodeId()
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
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
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def add_data_type_node_async(self, parent_node_id: UaNodeId,
                                 reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                                 callback: Callable[['UaClient', UaUInt32, UaAddNodesResponse], None],
                                 requested_new_node_id: UaNodeId = None,
                                 attr=None):
        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.DATA_TYPE

        out_new_node_id = UaNodeId()
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
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
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def add_method_node_async(self, parent_node_id: UaNodeId,
                              reference_type_id: UaNodeId, browse_name: UaQualifiedName,
                              callback: Callable[['UaClient', UaUInt32, UaAddNodesResponse], None],
                              requested_new_node_id: UaNodeId = None,
                              attr=None):

        if requested_new_node_id is None:
            requested_new_node_id = UaNodeId(val=UaNodeId.NULL)

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.METHOD

        out_new_node_id = UaNodeId()
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
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
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    # browse service
    def send_async_browse_request(self, request: UaBrowseRequest,
                                  callback: Callable[['UaClient', UaUInt32, UaBrowseResponse], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_sendAsyncBrowseRequest(self.ua_client,
                                                           request,
                                                           lib.python_wrapper_UA_ClientAsyncBrowseCallback,
                                                           _handle,
                                                           req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    # misc
    def add_timed_callback(self, callback: Callable[['UaClient', Void], None],
                           date: UaDateTime, callback_id):
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_addTimedCallback(self.ua_client,
                                                     lib.python_wrapper_UA_ClientCallback,
                                                     _handle,
                                                     date._val,
                                                     callback_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), None, _handle)

    def add_repeated_callback(self, callback: Callable[['UaClient', Void], None],
                              interval_ms: UaDouble,
                              callback_id: UaUInt64):
        status_code = lib.UA_Client_addRepeatedCallback(self.ua_client,
                                                        lib.python_wrapper_UA_ClientCallback,
                                                        ffi.new_handle(callback),
                                                        interval_ms._val,
                                                        callback_id._ptr)
        return UaStatusCode(val=status_code)

    def change_repeated_callback_interval(self, callback_id: UaUInt64, interval_ms: UaDouble):
        lib.UA_Client_changeRepeatedCallbackInterval(self.ua_client, callback_id._val, interval_ms._val)

    def remove_callback(self, callback_id: UaUInt64):
        lib.UA_Client_removeCallback(self.ua_client, callback_id)

    def renew_secure_channel(self):
        status_code = lib.UA_Client_renewSecureChannel(self.ua_client)
        return UaStatusCode(val=status_code)

    def __async_service_ex(self, request: Void, request_type: UaDataType,
                           response_type: UaDataType, callback: Callable[['UaClient', UaUInt32, Void], None],
                           timeout: UaInt32):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.__UA_Client_AsyncServiceEx(self.ua_client,
                                                     request._ptr,
                                                     request_type._ptr,
                                                     lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                     response_type._ptr,
                                                     _handle,
                                                     req_id._ptr,
                                                     timeout._val)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), None, _handle)

    # todo: not not usable at the moment --> fix
    def get_state(self):
        channel_state = UaSecureChannelState()
        session_state = UaSessionState()
        connect_status = None  # todo: there is no UaConnectSatus() yet
        return lib.UA_Client_getState(self.ua_client, channel_state, session_state,
                                      connect_status)  # todo: create response wrapper

    def get_context(self):
        return Void(val=lib.UA_Client_getContext(self.ua_client), is_pointer=True)

    def modify_async_callback(self, req_id: UaUInt32,
                              callback: Callable[['UaClient', UaUInt32, Void], None]):
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_modifyAsyncCallback(self.ua_client,
                                                        req_id._val,
                                                        _handle,
                                                        lib.python_wrapper_UA_ClientAsyncServiceCallback)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def __service(self, request: Void, request_type: UaDataType, response: Void,
                  response_type: UaDataType):
        status_code = lib.__UA_Client_Service(self.ua_client,
                                              request._ptr,
                                              request_type._ptr,
                                              response._ptr,
                                              response_type._ptr)
        return UaStatusCode(val=status_code)

    def __async_service(self, request: Void, request_type: UaDataType, response_type: Void,
                        callback: Callable[['UaClient', UaUInt32, Void], None]):
        req_id = UaUInt32()
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.__UA_Client_AsyncService(self.ua_client,
                                                   request._ptr,
                                                   request_type._ptr,
                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                   response_type._ptr,
                                                   _handle,
                                                   req_id._ptr)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), req_id, _handle)

    def namespace_get_index(self, namespace_uri: UaString, namespace_index: UaUInt16):
        status_code = lib.UA_Client_NamespaceGetIndex(self.ua_client,
                                                      namespace_uri._ptr,
                                                      namespace_index._ptr)
        return UaStatusCode(val=status_code)

    def for_each_child_node_call(self, parent_node_id: UaNodeId,
                                 callback: Callable[[UaNodeId, UaBoolean, UaNodeId], None]):
        _handle = ffi.new_handle(callback)
        _ClientCallback._callbacks.add(_handle)
        status_code = lib.UA_Client_forEachChildNodeCall(self.ua_client,
                                                         parent_node_id._val,
                                                         lib.python_wrapper_UA_NodeIteratorCallback,
                                                         _handle)
        return ClientServiceResult.AsyncResponse(UaStatusCode(val=status_code), None, _handle)
