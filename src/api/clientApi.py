from intermediateApi import ffi, lib

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

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncTranslateCallback(client, fun, request_id, tr):
        ffi.from_handle(fun)(client, request_id, tr)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncBrowseCallback(client, fun, request_id, wr):
        ffi.from_handle(fun)(client, request_id, wr)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadDataTypeAttributeCallback(client, fun, request_id, var):
        ffi.from_handle(fun)(client, request_id, var)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadNodeIdAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadDescriptionAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadWriteMaskAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadUserWriteMaskAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadIsAbstractAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadSymmetricAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadInverseNameAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadContainsNoLoopsAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadEventNotifierAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadValueRankAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadAccessLevelAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadUserAccessLevelAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadExecutableAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadUserExecutableAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncCallCallback(client, fun, request_id, cr):
        ffi.from_handle(fun)(client, request_id, cr)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadCallback(client, fun, request_id, rr):
        ffi.from_handle(fun)(client, request_id, rr)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadValueAttributeCallback(client, fun, request_id, var):
        ffi.from_handle(fun)(client, request_id, var)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadNodeClassAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadBrowseNameAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadDisplayNameAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadMinimumSamplingIntervalAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncReadHistorizingAttributeCallback(client, fun, request_id, out):
        ffi.from_handle(fun)(client, request_id, out)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncWriteCallback(client, fun, request_id, wr):
        ffi.from_handle(fun)(client, request_id, wr)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncAddNodesCallback(client, fun, request_id, ar):
        ffi.from_handle(fun)(client, request_id, ar)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ClientAsyncServiceCallback(client, fun, request_id, response):
        ffi.from_handle(fun)(client, request_id, response)

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_NodeIteratorCallback(child_id, is_inverse, reference_type_id, fun):
        ffi.from_handle(fun)(child_id, is_inverse, reference_type_id, fun)


class UaClient:
    def __init__(self, config=None):
        if config is None:
            self.ua_client = lib.UA_Client_new()
            self.set_default_config()
        else:
            self.ua_client = lib.UA_Client_newWithConfig(config)

    # connection

    def connect(self, endpoint_url: str):
        raw_result = lib.UA_Client_connect(self.ua_client, bytes(endpoint_url, 'utf-8'))
        return ua_types.UaStatusCode(val=raw_result)

    def disconnect(self):
        raw_result = lib.UA_Client_disconnect(self.ua_client)
        return ua_types.UaStatusCode(val=raw_result)

    def connect_secure_channel(self, endpoint_url: str):
        raw_result = lib.UA_Client_connectSecureChannel(self.ua_client, bytes(endpoint_url, 'utf-8'))
        return ua_types.UaStatusCode(val=raw_result)

    def disconnect_secure_channel(self):
        return ua_types.UaStatusCode(val=lib.UA_Client_disconnectSecureChannel(self.ua_client))

    # low level service

    def service_read(self, request: ua_types.UaReadRequest):
        raw_result = lib.UA_Client_Service_read(self.ua_client, request._val)
        return ua_types.UaReadResponse(val=raw_result)

    def service_write(self, request: ua_types.UaWriteRequest):
        raw_result = lib.UA_Client_Service_write(self.ua_client, request._val)
        return ua_types.UaWriteResponse(val=raw_result)

    def service_call(self, request: ua_types.UaCallRequest):
        raw_result = lib.UA_Client_Service_call(self.ua_client, request._val)
        return ua_types.UaCallResponse(val=raw_result)

    def service_add_nodes(self, request: ua_types.UaAddNodesRequest):
        raw_result = lib.UA_Client_Service_addNodes(self.ua_client, request._val)
        return ua_types.UaAddNodesResponse(val=raw_result)

    def service_add_reference(self, request: ua_types.UaAddReferencesRequest):
        raw_result = lib.UA_Client_Service_addReference(self.ua_client, request._val)
        return ua_types.UaAddReferencesResponse(val=raw_result)

    def service_delete_nodes(self, request: ua_types.UaDeleteNodesRequest):
        raw_result = lib.UA_Client_Service_deleteNodes(self.ua_client, request._val)
        return ua_types.UaDeleteNodesResponse(val=raw_result)

    def service_delete_references(self, request: ua_types.UaDeleteReferencesRequest):
        raw_result = lib.UA_Client_Service_deleteReferences(self.ua_client, request._val)
        return ua_types.UaDeleteReferencesResponse(val=raw_result)

    def service_browse(self, request: ua_types.UaBrowseRequest):
        raw_result = lib.UA_Client_Service_browse(self.ua_client, request._val)
        return ua_types.UaBrowseResponse(val=raw_result)

    def service_browse_next(self, request: ua_types.UaBrowseNextRequest):
        raw_result = lib.UA_Client_Service_browseNext(self.ua_client, request._val)
        return ua_types.UaBrowseNextResponse(val=raw_result)

    def service_translate_browse_paths_to_node_ids(self, request: ua_types.UaTranslateBrowsePathsToNodeIdsRequest):
        raw_result = lib.UA_Client_Service_translateBrowsePathsToNodeIds(self.ua_client, request._val)
        return ua_types.UaTranslateBrowsePathsToNodeIdsResponse(val=raw_result)

    def service_register_node(self, request: ua_types.UaRegisterNodesRequest):
        raw_result = lib.UA_Client_Service_registerNodes(self.ua_client, request._val)
        return ua_types.UaRegisterNodesResponse(val=raw_result)

    def service_unregister_node(self, request: ua_types.UaUnregisterNodesRequest):
        raw_result = lib.UA_Client_Service_unregisterNodes(self.ua_client, request._val)
        return ua_types.UaUnregisterNodesResponse(val=raw_result)

    # high level read service
    # todo: this doesn't really work because out is a void pointer. variable has to be created dynamically depending on type
    # also needs generic result class object as result
    def __read_attribute(self, node_id, attribute_id, out, out_data_type):
        status_code = lib.__UA_Client_readAttribute(self.ua_client, node_id, attribute_id, out, out_data_type)
        return status_code

    def read_node_id_attribute(self, node_id: ua_types.UaNodeId):
        out_node_id = ua_types.UaNodeId()
        status_code = lib.UA_Client_readNodeIdAttribute(self.ua_client, node_id._val, out_node_id._ptr)
        return ClientServiceResult.ReadNodeIdAttributeResult(ua_types.UaStatusCode(status_code), out_node_id)

    def read_node_class_attribute(self, node_id: ua_types.UaNodeId):
        out_node_class = ua_types.UaNodeClass()
        status_code = lib.UA_Client_readNodeClassAttribute(self.ua_client, node_id._val, out_node_class._ptr)
        return ClientServiceResult.ReadNodeClassAttributeResult(ua_types.UaStatusCode(status_code), out_node_class)

    def read_browse_name_attribute(self, node_id: ua_types.UaNodeId):
        out_browse_name = ua_types.UaQualifiedName()
        status_code = lib.UA_Client_readBrowseNameAttribute(self.ua_client, node_id._val, out_browse_name._ptr)
        return ClientServiceResult.ReadBrowseNameAttributeResult(ua_types.UaStatusCode(status_code), out_browse_name)

    def read_display_name_attribute(self, node_id: ua_types.UaNodeId):
        out_display_name = ua_types.UaLocalizedText()
        status_code = lib.UA_Client_readDisplayNameAttribute(self.ua_client, node_id._val, out_display_name._ptr)
        return ClientServiceResult.ReadDisplayNameAttributeResult(ua_types.UaStatusCode(status_code), out_display_name)

    def read_description_attribute(self, node_id: ua_types.UaNodeId):
        out_description = ua_types.UaLocalizedText()
        status_code = lib.UA_Client_readDescriptionAttribute(self.ua_client, node_id._val, out_description._ptr)
        return ClientServiceResult.ReadDescriptionAttributeResult(ua_types.UaStatusCode(status_code), out_description)

    def read_write_mask_attribute(self, node_id: ua_types.UaNodeId):
        out_write_mask = ua_types.UaUInt32()
        status_code = lib.UA_Client_readWriteMaskAttribute(self.ua_client, node_id._val, out_write_mask._ptr)
        return ClientServiceResult.ReadWriteMaskAttributeResult(ua_types.UaStatusCode(status_code), out_write_mask)

    def read_user_write_mask_attribute(self, node_id: ua_types.UaNodeId):
        out_user_write_mask = ua_types.UaUInt32()
        status_code = lib.UA_Client_readUserWriteMaskAttribute(self.ua_client, node_id._val, out_user_write_mask._ptr)
        return ClientServiceResult.ReadUserWriteMaskAttributeResult(ua_types.UaStatusCode(status_code),
                                                                    out_user_write_mask)

    def read_is_abstract_attribute(self, node_id: ua_types.UaNodeId):
        out_is_abstract = ua_types.UaBoolean()
        status_code = lib.UA_Client_readIsAbstractAttribute(self.ua_client, node_id._val, out_is_abstract._ptr)
        return ClientServiceResult.ReadIsAbstractAttributeResult(ua_types.UaStatusCode(status_code), out_is_abstract)

    def read_symmetric_attribute(self, node_id: ua_types.UaNodeId):
        out_symmetric = ua_types.UaBoolean()
        status_code = lib.UA_Client_readSymmetricAttribute(self.ua_client, node_id._val, out_symmetric._ptr)
        return ClientServiceResult.ReadSymmetricAttributeResult(ua_types.UaStatusCode(status_code), out_symmetric)

    def read_inverse_name_attribute(self, node_id: ua_types.UaNodeId):
        out_inverse_name = ua_types.UaLocalizedText()
        status_code = lib.UA_Client_readInverseNameAttribute(self.ua_client, node_id._val, out_inverse_name._ptr)
        return ClientServiceResult.ReadInverseNameAttributeResult(ua_types.UaStatusCode(status_code), out_inverse_name)

    def read_contains_no_loops_attribute(self, node_id: ua_types.UaNodeId):
        out_contains_no_loops = ua_types.UaBoolean()
        status_code = lib.UA_Client_readContainsNoLoopsAttribute(self.ua_client, node_id._val,
                                                                 out_contains_no_loops._ptr)
        return ClientServiceResult.ReadContainsNoLoopsAttributeResult(ua_types.UaStatusCode(status_code),
                                                                      out_contains_no_loops)

    def read_event_notifier_attribute(self, node_id: ua_types.UaNodeId):
        out_event_notifier = ua_types.UaByte()
        status_code = lib.UA_Client_readEventNotifierAttribute(self.ua_client, node_id._val, out_event_notifier._ptr)
        return ClientServiceResult.ReadEventNotifierAttributeResult(ua_types.UaStatusCode(status_code),
                                                                    out_event_notifier)

    def read_value_attribute(self, node_id: ua_types.UaNodeId):
        value = ua_types.UaVariant()
        status_code = lib.UA_Client_readValueAttribute(self.ua_client, node_id._val, value._ptr)
        return ClientServiceResult.ReadValueAttributeResult(ua_types.UaStatusCode(status_code), value)

    def read_data_type_attribute(self, node_id: ua_types.UaNodeId):
        out_data_type = ua_types.UaNodeId()
        status_code = lib.UA_Client_readDataTypeAttribute(self.ua_client, node_id._val, out_data_type._ptr)
        return ClientServiceResult.ReadDataTypeAttribute(ua_types.UaStatusCode(status_code), out_data_type)

    def read_value_rank_attribute(self, node_id: ua_types.UaNodeId):
        out_value_rank = ua_types.UaUInt32()
        status_code = lib.UA_Client_readValueRankAttribute(self.ua_client, node_id._val, out_value_rank._ptr)
        return ClientServiceResult.ReadValueRankAttribute(ua_types.UaStatusCode(status_code), out_value_rank)

    def read_array_dimensions_attribute(self, node_id: ua_types.UaNodeId):
        out_array_dimensions_size = ua_types.SizeT()
        out_array_dimensions = ua_types.UaUInt32()
        status_code = lib.UA_Client_readArrayDimensionsAttribute(self.ua_client, node_id._val,
                                                                 out_array_dimensions_size._ptr,
                                                                 out_array_dimensions._ptr)
        return ClientServiceResult.ReadArrayDimensionsAttributeResult(ua_types.UaStatusCode(status_code),
                                                                      out_array_dimensions_size,
                                                                      out_array_dimensions)

    def read_access_level_attribute(self, node_id: ua_types.UaNodeId):
        out_access_level = ua_types.UaByte()
        status_code = lib.UA_Client_readAccessLevelAttribute(self.ua_client, node_id._val, out_access_level._ptr)
        return ClientServiceResult.ReadAccessLevelAttributeResult(ua_types.UaStatusCode(status_code), out_access_level)

    def read_user_access_level_attribute(self, node_id: ua_types.UaNodeId):
        out_user_access_level = ua_types.UaByte()
        status_code = lib.UA_Client_readUserAccessLevelAttribute(self.ua_client, node_id._val,
                                                                 out_user_access_level._ptr)
        return ClientServiceResult.ReadUserAccessLevelAttributeResult(ua_types.UaStatusCode(status_code),
                                                                      out_user_access_level)

    def read_minimum_sampling_interval_attribute(self, node_id: ua_types.UaNodeId):
        out_min_sampling_interval = ua_types.UaDouble()
        status_code = lib.UA_Client_readMinimumSamplingIntervalAttribute(self.ua_client, node_id._val,
                                                                         out_min_sampling_interval._ptr)
        return ClientServiceResult.ReadMinimumSamplingIntervalAttributeResult(ua_types.UaStatusCode(status_code),
                                                                              out_min_sampling_interval)

    def read_executable_attribute(self, node_id: ua_types.UaNodeId):
        out_executable = ua_types.UaBoolean()
        status_code = lib.UA_Client_readExecutableAttribute(self.ua_client, node_id._val, out_executable._ptr)
        return ClientServiceResult.ReadExecutableAttributeResult(status_code, out_executable)

    def read_user_executable_attribute(self, node_id: ua_types.UaNodeId):
        out_user_executable = ua_types.UaBoolean()
        status_code = lib.UA_Client_readUserExecutableAttribute(self.ua_client, node_id._val, out_user_executable._ptr)
        return ClientServiceResult.ReadUserExecutableAttributeResult(ua_types.UaStatusCode(status_code),
                                                                     out_user_executable)

    # high level write service

    def write_node_id_attribute(self, node_id: ua_types.UaNodeId, new_node_id: ua_types.UaNodeId):
        raw_result = lib.UA_Client_writeNodeIdAttribute(self.ua_client, node_id._val, new_node_id._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_node_class_attribute(self, node_id: ua_types.UaNodeId, new_node_class: ua_types.UaNodeClass):
        raw_result = lib.UA_Client_writeNodeClassAttribute(self.ua_client, node_id._val, new_node_class._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_browse_name_attribute(self, node_id: ua_types.UaNodeId, new_browse_name: ua_types.UaQualifiedName):
        raw_result = lib.UA_Client_writeBrowseNameAttribute(self.ua_client, node_id._val, new_browse_name._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_display_name_attribute(self, node_id: ua_types.UaNodeId, new_display_name: ua_types.UaLocalizedText):
        raw_result = lib.UA_Client_writeDisplayNameAttribute(self.ua_client, node_id._val, new_display_name._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_description_attribute(self, node_id: ua_types.UaNodeId, new_description: ua_types.UaLocalizedText):
        raw_result = lib.UA_Client_writeDescriptionAttribute(self.ua_client, node_id._val, new_description._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_write_mask_attribute(self, node_id: ua_types.UaNodeId, new_write_mask: ua_types.UaUInt32):
        raw_result = lib.UA_Client_writeWriteMaskAttribute(self.ua_client, node_id._val, new_write_mask._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_user_write_mask_attribute(self, node_id: ua_types.UaNodeId, new_user_write_mask: ua_types.UaUInt32):
        raw_result = lib.UA_Client_writeUserWriteMaskAttribute(self.ua_client, node_id._val, new_user_write_mask._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_is_abstract_attribute(self, node_id: ua_types.UaNodeId, new_is_abstract: ua_types.UaBoolean):
        raw_result = lib.UA_Client_writeIsAbstractAttribute(self.ua_client, node_id._val, new_is_abstract._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_symmetric_attribute(self, node_id: ua_types.UaNodeId, new_symmetric: ua_types.UaBoolean):
        raw_result = lib.UA_Client_writeSymmetricAttribute(self.ua_client, node_id._val, new_symmetric._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_inverse_name_attribute(self, node_id: ua_types.UaNodeId, new_inverse_name: ua_types.UaLocalizedText):
        raw_result = lib.UA_Client_writeInverseNameAttribute(self.ua_client, node_id._val, new_inverse_name._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_contains_no_loops_attribute(self, node_id: ua_types.UaNodeId, new_contains_no_loops: ua_types.UaBoolean):
        raw_result = lib.UA_Client_writeContainsNoLoopsAttribute(self.ua_client, node_id._val,
                                                                 new_contains_no_loops._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_event_notifier_attribute(self, node_id: ua_types.UaNodeId, new_event_notifier: ua_types.UaByte):
        raw_result = lib.UA_Client_writeEventNotifierAttribute(self.ua_client, node_id._val, new_event_notifier._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_value_attribute(self, node_id: ua_types.UaNodeId, new_value: ua_types.UaVariant):
        raw_result = lib.UA_Client_writeValueAttribute(self.ua_client, node_id._val, new_value._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_data_type_attribute(self, node_id: ua_types.UaNodeId, new_data_type: ua_types.UaNodeId):
        raw_result = lib.UA_Client_writeDataTypeAttribute(self.ua_client, node_id._val, new_data_type._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_value_rank_attribute(self, node_id: ua_types.UaNodeId, new_value_rank: ua_types.UaInt32):
        raw_result = lib.UA_Client_writeValueRankAttribute(self.ua_client, node_id._val, new_value_rank._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_array_dimensions_attribute(self, node_id: ua_types.UaNodeId, new_array_dimensions_size: ua_types.SizeT,
                                         new_array_dimensions: ua_types.UaUInt32):
        raw_result = lib.UA_Client_writeArrayDimensionsAttribute(self.ua_client, node_id._val,
                                                                 new_array_dimensions_size._val,
                                                                 new_array_dimensions._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_access_level_attribute(self, node_id: ua_types.UaNodeId, new_access_level: ua_types.UaByte):
        raw_result = lib.UA_Client_writeAccessLevelAttribute(self.ua_client, node_id._val, new_access_level._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_user_access_level_attribute(self, node_id: ua_types.UaNodeId, new_user_access_level: ua_types.UaByte):
        raw_result = lib.UA_Client_writeUserAccessLevelAttribute(self.ua_client, node_id._val,
                                                                 new_user_access_level._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_minimum_sampling_interval_attribute(self, node_id: ua_types.UaNodeId,
                                                  new_min_interval: ua_types.UaDouble):
        raw_result = lib.UA_Client_writeMinimumSamplingIntervalAttribute(self.ua_client, node_id._val,
                                                                         new_min_interval._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_executable_attribute(self, node_id: ua_types.UaNodeId, new_executable: ua_types.UaBoolean):
        raw_result = lib.UA_Client_writeExecutableAttribute(self.ua_client, node_id._val, new_executable._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_user_executable_attribute(self, node_id: ua_types.UaNodeId, new_user_executable: ua_types.UaBoolean):
        raw_result = lib.UA_Client_writeUserExecutableAttribute(self.ua_client, node_id._val, new_user_executable._ptr)
        return ua_types.UaStatusCode(val=raw_result)

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
    # todo: integrate config in type system
    def get_config(self):
        return lib.UA_Client_getConfig(self.ua_client)

    def set_default_config(self):
        lib.UA_ClientConfig_setDefault(self.get_config())

    def find_data_type(self, type_id):
        return ua_types.UaDataType(lib.UA_Client_findDataType(self.ua_client, type_id), is_pointer=True)

    def get_endpoints(self, server_url, endpoint_descriptions_size, endpoint_descriptions):
        raw_result = lib.UA_Client_getEndpoints(self.ua_client, server_url, endpoint_descriptions_size,
                                                endpoint_descriptions)
        return ua_types.UaStatusCode(val=raw_result)

    def find_servers(self, server_url, server_uris_size, locale_ids_size, locale_ids, registered_servers_size,
                     registered_servers):
        raw_result = lib.UA_Client_findServers(self.ua_client, server_url, server_uris_size, locale_ids_size,
                                               locale_ids,
                                               registered_servers_size, registered_servers)
        return ua_types.UaStatusCode(val=raw_result)

    def run_iterate(self, timeout):
        raw_result = lib.UA_Client_run_iterate(self.ua_client, timeout)
        return ua_types.UaStatusCode(val=raw_result)

    #    def find_servers_on_network(self, server_url, starting_record_id, max_records_to_return,
    #                                server_capability_filter_size, server_on_network_size, server_on_network):
    #        return lib.UA_Client_findServersOnNetwork(self.ua_client, server_url, starting_record_id, max_records_to_return,
    #                                                  server_capability_filter_size, server_on_network_size,
    #                                                  server_on_network)

    # async read service
    def send_async_read_request(self, request, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_sendAsyncReadRequest(self.ua_client, request,
                                                         lib.python_wrapper_UA_ClientAsyncReadCallback, callback,
                                                         req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def __read_attribute_async(self, node_id, attribute_id, callback):
        out_data_type = ffi.new("UA_DataType*")
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.__UA_Client_readAttribute_async(self.ua_client, node_id, attribute_id, out_data_type,
                                                          lib.python_wrapper_UA_ClientAsyncServiceCallback, callback,
                                                          req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_data_type_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readDataTypeAttribute_async(self.ua_client, node_id,
                                                                lib.python_wrapper_UA_ClientAsyncReadDataTypeAttributeCallback,
                                                                callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_value_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readValueAttribute_async(self.ua_client, node_id,
                                                             lib.python_wrapper_UA_ClientAsyncReadValueAttributeCallback,
                                                             callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_node_id_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readNodeIdAttribute_async(self.ua_client, node_id,
                                                              lib.python_wrapper_UA_ClientAsyncReadNodeIdAttributeCallback,
                                                              callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_node_class_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readNodeClassAttribute_async(self.ua_client, node_id,
                                                                 lib.python_wrapper_UA_ClientAsyncReadNodeClassAttributeCallback,
                                                                 callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_browse_name_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readBrowseNameAttribute_async(self.ua_client, node_id,
                                                                  lib.python_wrapper_UA_ClientAsyncReadBrowseNameAttributeCallback,
                                                                  callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_display_name_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readDisplayNameAttribute_async(self.ua_client, node_id,
                                                                   lib.python_wrapper_UA_ClientAsyncReadDisplayNameAttributeCallback,
                                                                   callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_description_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readDescriptionAttribute_async(self.ua_client, node_id,
                                                                   lib.python_wrapper_UA_ClientAsyncReadDescriptionAttributeCallback,
                                                                   callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_write_mask_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readWriteMaskAttribute_async(self.ua_client, node_id,
                                                                 lib.python_wrapper_UA_ClientAsyncReadWriteMaskAttributeCallback,
                                                                 callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def readUser_write_mask_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readUserWriteMaskAttribute_async(self.ua_client, node_id,
                                                                     lib.python_wrapper_UA_ClientAsyncReadUserWriteMaskAttributeCallback,
                                                                     callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_is_abstract_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readIsAbstractAttribute_async(self.ua_client, node_id,
                                                                  lib.python_wrapper_UA_ClientAsyncReadIsAbstractAttributeCallback,
                                                                  callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_symmetric_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readSymmetricAttribute_async(self.ua_client, node_id,
                                                                 lib.python_wrapper_UA_ClientAsyncReadSymmetricAttributeCallback,
                                                                 callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_inverse_name_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readInverseNameAttribute_async(self.ua_client, node_id,
                                                                   lib.python_wrapper_UA_ClientAsyncReadInverseNameAttributeCallback,
                                                                   callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_contains_no_loops_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readContainsNoLoopsAttribute_async(self.ua_client, node_id,
                                                                       lib.python_wrapper_UA_ClientAsyncReadContainsNoLoopsAttributeCallback,
                                                                       callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_event_notifier_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readEventNotifierAttribute_async(self.ua_client, node_id,
                                                                     lib.python_wrapper_UA_ClientAsyncReadEventNotifierAttributeCallback,
                                                                     callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_value_rank_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readValueRankAttribute_async(self.ua_client, node_id,
                                                                 lib.python_wrapper_UA_ClientAsyncReadValueRankAttributeCallback,
                                                                 callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_access_level_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readAccessLevelAttribute_async(self.ua_client, node_id,
                                                                   lib.python_wrapper_UA_ClientAsyncReadAccessLevelAttributeCallback,
                                                                   callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_user_access_level_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readUserAccessLevelAttribute_async(self.ua_client, node_id,
                                                                       lib.python_wrapper_UA_ClientAsyncReadUserAccessLevelAttributeCallback,
                                                                       callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_minimum_sampling_interval_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readMinimumSamplingIntervalAttribute_async(self.ua_client, node_id,
                                                                               lib.python_wrapper_UA_ClientAsyncReadMinimumSamplingIntervalAttributeCallback,
                                                                               callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_historizing_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readHistorizingAttribute_async(self.ua_client, node_id,
                                                                   lib.python_wrapper_UA_ClientAsyncReadHistorizingAttributeCallback,
                                                                   callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_executable_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readExecutableAttribute_async(self.ua_client, node_id,
                                                                  lib.python_wrapper_UA_ClientAsyncReadExecutableAttributeCallback,
                                                                  callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def read_user_executable_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.readUserExecutableAttribute_async(self.ua_client, node_id,
                                                            lib.python_wrapper_UA_ClientAsyncReadUserExecutableAttributeCallback,
                                                            callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    # async write service
    def send_async_write_request(self, request, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_sendAsyncWriteRequest(self.ua_client, request,
                                                          lib.python_wrapper_UA_ClientAsyncWriteCallback, callback,
                                                          req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def __write_attribute_async(self, node_id, attribute_id, _in, in_data_type, callback):
        req_id = ffi.new("UA_UInt32*")
        return lib.__UA_Client_writeAttribute_async(self.ua_client, node_id, attribute_id, _in, in_data_type,
                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback, callback, req_id)

    def write_value_attribute_async(self, node_id, new_value, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_writeValueAttribute_async(self.ua_client, node_id, new_value,
                                                              lib.python_wrapper_UA_ClientAsyncWriteCallback, callback,
                                                              req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_node_id_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_writeNodeIdAttribute_async(self.ua_client, node_id, out_node_id,
                                                               lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                               callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_node_class_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_node_class = ffi.new("UA_NodeClass*")
        status_code = lib.UA_Client_writeNodeClassAttribute_async(self.ua_client, node_id, out_node_class,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_browse_name_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_browse_name = ffi.new("UA_QualifiedName*")
        status_code = lib.UA_Client_writeBrowseNameAttribute_async(self.ua_client, node_id, out_browse_name,
                                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                   callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_display_name_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_display_name = ffi.new("UA_LocalizedText*")
        status_code = lib.UA_Client_writeDisplayNameAttribute_async(self.ua_client, node_id, out_display_name,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_description_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_description = ffi.new("UA_LocalizedText*")
        status_code = lib.UA_Client_writeDescriptionAttribute_async(self.ua_client, node_id, out_description,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_write_mask_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_write_mask = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_writeWriteMaskAttribute_async(self.ua_client, node_id, out_write_mask,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_user_write_mask_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_user_write_mask = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_writeUserWriteMaskAttribute_async(self.ua_client, node_id, out_user_write_mask,
                                                                      lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                      callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_is_abstract_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_is_abstract = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_writeIsAbstractAttribute_async(self.ua_client, node_id, out_is_abstract,
                                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                   callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_symmetric_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_symmetric = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_writeSymmetricAttribute_async(self.ua_client, node_id, out_symmetric,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_inverse_name_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_inverse_name = ffi.new("UA_LocalizedText*")
        status_code = lib.UA_Client_writeInverseNameAttribute_async(self.ua_client, node_id, out_inverse_name,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_contains_no_loops_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_contains_no_loops = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_writeContainsNoLoopsAttribute_async(self.ua_client, node_id, out_contains_no_loops,
                                                                        lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                        callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_event_notifier_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_event_notifier = ffi.new("UA_Byte*")
        status_code = lib.UA_Client_writeEventNotifierAttribute_async(self.ua_client, node_id, out_event_notifier,
                                                                      lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                      callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_data_type_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_data_type = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_writeDataTypeAttribute_async(self.ua_client, node_id, out_data_type,
                                                                 lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                 callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_value_rank_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_value_rank = ffi.new("UA_Int32*")
        status_code = lib.UA_Client_writeValueRankAttribute_async(self.ua_client, node_id, out_value_rank,
                                                                  lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                  callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_access_level_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_access_level = ffi.new("UA_Byte*")
        status_code = lib.UA_Client_writeAccessLevelAttribute_async(self.ua_client, node_id, out_access_level,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_user_access_level_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_user_access_level = ffi.new("UA_Byte*")
        status_code = lib.UA_Client_writeUserAccessLevelAttribute_async(self.ua_client, node_id, out_user_access_level,
                                                                        lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                        callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    # todo: check if this is correct. this is different in the synchronous version. the naming of out_minimum_sampling_interval suggests that it is a return value but I think it is evaluated by the service again as an argument
    def write_minimum_sampling_interval_attribute_async(self, node_id, callback, out_minimum_sampling_interval):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_writeMinimumSamplingIntervalAttribute_async(self.ua_client, node_id,
                                                                                out_minimum_sampling_interval,
                                                                                lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                                callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    # todo: check if this is correct. this is different in the synchronous version
    def write_historizing_attribute_async(self, node_id, callback, out_historizing):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_writeHistorizingAttribute_async(self.ua_client, node_id, out_historizing,
                                                                    lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                    callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_executable_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_executable = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_writeExecutableAttribute_async(self.ua_client, node_id, out_executable,
                                                                   lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                   callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def write_user_executable_attribute_async(self, node_id, callback):
        req_id = ffi.new("UA_UInt32*")
        out_user_executable = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_writeUserExecutableAttribute_async(self.ua_client, node_id, out_user_executable,
                                                                       lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                                                       callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    # call service
    # todo: can we get rid of input_size, calculate it ourselves and hide it from users?
    def _call_async(self, object_id, method_id, input_size, _input, callback, req_id):
        return lib.__UA_Client_call_async(self.ua_client, object_id, method_id, input_size, _input,
                                          lib.python_wrapper_UA_ClientAsyncServiceCallback, callback, req_id)

    # todo: can we get rid of input_size, calculate it ourselves and hide it from users?
    def call_async(self, object_id, method_id, input_size, _input, callback, req_id):
        return lib.__UA_Client_call_async(self.ua_client, object_id, method_id, input_size, _input,
                                          lib.python_wrapper_UA_ClientAsyncCallCallback, callback, req_id)

    # add node service
    def add_variable_node_async(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                                type_definition, callback, attr=DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_addVariableNode_async(self.ua_client, requested_new_node_id, parent_node_id,
                                                          reference_type_id, browse_name, type_definition, attr,
                                                          out_new_node_id,
                                                          lib.python_wrapper_UA_ClientAsyncAddNodesCallback, callback,
                                                          req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id)

    def __add_node_async(self, node_class, requested_new_node_id, parent_node_id, reference_type_id,
                         browse_name, type_definition, attr, attribute_type, callback):
        out_new_node_id = ffi.new("UA_NodeId*")
        req_id = ffi.new("UA_UInt32*")
        return lib.__UA_Client_addNode_async(self.ua_client, node_class, requested_new_node_id, parent_node_id,
                                             reference_type_id, browse_name, type_definition, attr, attribute_type,
                                             out_new_node_id, lib.python_wrapper_UA_ClientAsyncServiceCallback,
                                             callback, req_id)

    def add_variable_type_node_async(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                                     callback, attr=DefaultAttributes.VARIABLE_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_addVariableTypeNode_async(self.ua_client, requested_new_node_id, parent_node_id,
                                                              reference_type_id, browse_name, attr, out_new_node_id,
                                                              lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                              callback,
                                                              req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def add_object_node_async(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                              type_definition, callback, attr=DefaultAttributes.OBJECT_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_addObjectNode_async(self.ua_client, requested_new_node_id, parent_node_id,
                                                        reference_type_id, browse_name, type_definition, attr,
                                                        out_new_node_id,
                                                        lib.python_wrapper_UA_ClientAsyncAddNodesCallback, callback,
                                                        req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def add_object_type_node_async(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                                   callback, attr=DefaultAttributes.OBJECT_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_addObjectTypeNode_async(self.ua_client, requested_new_node_id, parent_node_id,
                                                            reference_type_id, browse_name, attr, out_new_node_id,
                                                            lib.python_wrapper_UA_ClientAsyncAddNodesCallback, callback,
                                                            req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def add_view_node_async(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, callback,
                            attr=DefaultAttributes.VIEW_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_addViewNode_async(self.ua_client, requested_new_node_id, parent_node_id,
                                                      reference_type_id, browse_name, attr, out_new_node_id,
                                                      lib.python_wrapper_UA_ClientAsyncAddNodesCallback, callback,
                                                      req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def add_reference_type_node_async(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                                      callback, attr=DefaultAttributes.REFERENCE_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_addReferenceTypeNode_async(self.ua_client, requested_new_node_id, parent_node_id,
                                                               reference_type_id, browse_name, attr, out_new_node_id,
                                                               lib.python_wrapper_UA_ClientAsyncAddNodesCallback,
                                                               callback, req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def add_data_type_node_async(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                                 callback, attr=DefaultAttributes.DATA_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_addDataTypeNode_async(self, requested_new_node_id, parent_node_id,
                                                          reference_type_id, browse_name, attr, out_new_node_id,
                                                          lib.python_wrapper_UA_ClientAsyncAddNodesCallback, callback,
                                                          req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def add_method_node_async(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                              callback, attr=DefaultAttributes.METHOD_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_addMethodNode_async(self.ua_client, requested_new_node_id, parent_node_id,
                                                        reference_type_id, browse_name, attr, out_new_node_id,
                                                        lib.python_wrapper_UA_ClientAsyncAddNodesCallback, callback,
                                                        req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    # browse service
    def send_async_browse_request(self, request, callback):
        req_id = ffi.new("UA_UInt32*")
        return lib.UA_Client_sendAsyncBrowseRequest(self.ua_client, request,
                                                    lib.python_wrapper_UA_ClientAsyncBrowseCallback, callback, req_id)

    # misc

    def UA_Client_sendAsyncBrowseRequest(self, request, callback):
        req_id = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_sendAsyncBrowseRequest(self.ua_client, request,
                                                           lib.python_wrapper_UA_ClientAsyncBrowseCallback, callback,
                                                           req_id)
        return ClientServiceResult.AsyncResponse(status_code, req_id[0])

    def add_timed_callback(self, callback, date, callback_id):
        return lib.UA_Client_addTimedCallback(self.ua_client, lib.python_wrapper_UA_ClientCallback, callback, date,
                                              callback_id)

    def add_repeated_callback(self, callback, interval_ms, callback_id):
        return lib.UA_Client_addRepeatedCallback(self.ua_client, lib.python_wrapper_UA_ClientCallback, callback,
                                                 interval_ms, callback_id)

    def change_repeated_callback_interval(self, callback_id, interval_ms):
        lib.UA_Client_removeCallback(self.ua_client, callback_id, interval_ms)

    def renew_secure_channel(self):
        return lib.UA_Client_renewSecureChannel(self.ua_client)

    def __async_service_ex(self, request, request_type, response_type, callback, timeout):
        req_id = ffi.new("UA_UInt32*")
        return lib.__UA_Client_AsyncServiceEx(self.ua_client, request, request_type,
                                              lib.python_wrapper_UA_ClientAsyncServiceCallback, response_type, callback,
                                              req_id, timeout)

    def get_state(self, channel_state, session_state, connect_status):
        return lib.UA_Client_getState(self.ua_client, channel_state, session_state, connect_status)

    def get_context(self):
        return lib.UA_Client_getContext(self.ua_client)

    def modify_async_callback(self, callback):
        req_id = ffi.new("UA_UInt32*")
        return lib.UA_Client_modifyAsyncCallback(self.ua_client, req_id, callback,
                                                 lib.python_wrapper_UA_ClientAsyncServiceCallback)

    def __service(self, request, request_type, response, response_type):
        return lib.__UA_Client_Service(self.ua_client, request, request_type, response, response_type)

    def __async_service(self, request, request_type, response_type, callback):
        req_id = ffi.new("UA_UInt32*")
        return lib.__UA_Client_AsyncService(self.ua_client, request, request_type,
                                            lib.python_wrapper_UA_ClientAsyncServiceCallback, response_type, callback,
                                            req_id)

    def namespace_get_index(self, namespace_uri, namespace_index):
        return lib.UA_Client_NamespaceGetIndex(self.ua_client, namespace_uri, namespace_index)


def for_each_child_node_call(self, parent_node_id, callback):
    return lib.UA_Client_forEachChildNodeCall(self.ua_client, parent_node_id,
                                              lib.python_wrapper_UA_NodeIteratorCallback, callback)
