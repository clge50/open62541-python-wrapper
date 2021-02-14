from intermediateApi import ffi, lib
import client_service_results as ClientServiceResult
from random import seed
from random import randint
seed(2)


class DefaultAttributes:
    VARIABLE_ATTRIBUTES_DEFAULT = lib.UA_VariableAttributes_default
    VARIABLE_TYPE_ATTRIBUTES_DEFAULT = lib.UA_VariableTypeAttributes_default
    METHOD_ATTRIBUTES_DEFAULT = lib.UA_MethodAttributes_default
    OBJECT_ATTRIBUTES_DEFAULT = lib.UA_ObjectAttributes_default
    OBJECT_TYPE_ATTRIBUTES_DEFAULT = lib.UA_ObjectTypeAttributes_default
    REFERENCE_TYPE_ATTRIBUTES_DEFAULT = lib.UA_ReferenceTypeAttributes_default
    DATA_TYPE_ATTRIBUTES_DEFAULT = lib.UA_DataTypeAttributes_default
    VIEW_ATTRIBUTES_DEFAULT = lib.UA_ViewAttributes_default


class UaCallback:

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
        ffi.from_handle(fun)(client, request_id, )

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

class UaClient:
    def __init__(self, config=None):
        if config is None:
            self.ua_client = lib.UA_Client_new()
            self.set_default_config()
        else:
            self.ua_client = lib.UA_Client_newWithConfig(config)

    # connection

    def connect(self, endpoint_url):
        return lib.UA_Client_connect(self.ua_client, endpoint_url)

    def disconnect(self):
        return lib.UA_Client_disconnect(self.ua_client)

    def connect_secure_channel(self, endpoint_url):
        return lib.UA_Client_connectSecureChannel(self.ua_client, endpoint_url)

    def disconnect_secure_channel(self):
        return lib.UA_Client_disconnectSecureChannel(self.ua_client)

    # low level service

    def service_read(self, request):
        return lib.UA_Client_Service_read(self.ua_client, request)

    def service_write(self, request):
        return lib.UA_Client_Service_write(self.ua_client, request)

    def service_call(self, request):
        return lib.UA_Client_Service_call(self.ua_client, request)

    def service_add_nodes(self, request):
        return lib.UA_Client_Service_addNodes(self.ua_client, request)

    def service_add_reference(self, request):
        return lib.UA_Client_Service_addReference(self.ua_client, request)

    def service_delete_nodes(self, request):
        return lib.UA_Client_Service_deleteNodes(self.ua_client, request)

    def service_delete_references(self, request):
        return lib.UA_Client_Service_deleteReferences(self.ua_client, request)

    def service_browse(self, request):
        return lib.UA_Client_Service_browse(self.ua_client, request)

    def service_browse_next(self, request):
        return lib.UA_Client_Service_browseNext(self.ua_client, request)

    def service_translate_browse_paths_to_node_ids(self, request):
        return lib.UA_Client_Service_translateBrowsePathsToNodeIds(self.ua_client, request)

    def service_register_node(self, request):
        return lib.UA_Client_Service_registerNodes(self.ua_client, request)

    def service_unregister_node(self, request):
        return lib.UA_Client_Service_unregisterNodes(self.ua_client, request)

    # high level read service

    def read_node_id_attribute(self, node_id):
        out_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_readNodeIdAttribute(self.ua_client, node_id, out_node_id)
        return ClientServiceResult.ReadNodeIdAttributeResult(status_code, out_node_id)

    def read_node_class_attribute(self, node_id):
        out_node_class = ffi.new("UA_NodeClass*")
        status_code = lib.UA_Client_readNodeClassAttribute(self.ua_client, node_id, out_node_class)
        return ClientServiceResult.ReadNodeClassAttributeResult(status_code, out_node_class)

    def read_browse_name_attribute(self, node_id):
        out_browse_name = ffi.new("UA_QualifiedName*")
        status_code = lib.UA_Client_readBrowseNameAttribute(self.ua_client, node_id, out_browse_name)
        return ClientServiceResult.ReadBrowseNameAttributeResult(status_code, out_browse_name)

    def read_display_name_attribute(self, node_id):
        out_display_name = ffi.new("UA_LocalizedText*")
        status_code = lib.UA_Client_readDisplayNameAttribute(self.ua_client, node_id, out_display_name)
        return ClientServiceResult.ReadDisplayNameAttributeResult(status_code, out_display_name)

    def read_description_attribute(self, node_id):
        out_description = ffi.new("UA_LocalizedText*")
        status_code = lib.UA_Client_readDescriptionAttribute(self.ua_client, node_id, out_description)
        return ClientServiceResult.ReadDescriptionAttributeResult(status_code, out_description)

    def read_write_mask_attribute(self, node_id):
        out_write_mask = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readWriteMaskAttribute(self.ua_client, node_id, out_write_mask)
        return ClientServiceResult.ReadWriteMaskAttributeResult(status_code, out_write_mask)

    def read_user_write_mask_attribute(self, node_id):
        out_user_write_mask = ffi.new("UA_UInt32*")
        status_code = lib.UA_Client_readUserWriteMaskAttribute(self.ua_client, node_id, out_user_write_mask)
        return ClientServiceResult.ReadUserWriteMaskAttributeResult(status_code, out_user_write_mask)

    def read_is_abstract_attribute(self, node_id):
        out_is_abstract = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_readIsAbstractAttribute(self.ua_client, node_id, out_is_abstract)
        return ClientServiceResult.ReadIsAbstractAttributeResult(status_code, out_is_abstract)

    def read_symmetric_attribute(self, node_id):
        out_symmetric = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_readSymmetricAttribute(self.ua_client, node_id, out_symmetric)
        return ClientServiceResult.ReadSymmetricAttributeResult(status_code, out_symmetric)

    def read_inverse_name_attribute(self, node_id):
        out_inverse_name = ffi.new("UA_LocalizedText*")
        status_code = lib.UA_Client_readInverseNameAttribute(self.ua_client, node_id, out_inverse_name)
        return ClientServiceResult.ReadInverseNameAttributeResult(status_code, out_inverse_name)

    def read_contains_no_loops_attribute(self, node_id):
        out_contains_no_loops = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_readContainsNoLoopsAttribute(self.ua_client, node_id, out_contains_no_loops)
        return ClientServiceResult.ReadContainsNoLoopsAttributeResult(status_code, out_contains_no_loops)

    def read_event_notifier_attribute(self, node_id):
        out_event_notifier = ffi.new("UA_Byte*")
        status_code = lib.UA_Client_readEventNotifierAttribute(self.ua_client, node_id, out_event_notifier)
        return ClientServiceResult.ReadEventNotifierAttributeResult(status_code, out_event_notifier)

    def read_value_attribute(self, node_id):
        value = ffi.new("UA_Variant*")
        status_code = lib.UA_Client_readValueAttribute(self.ua_client, node_id, value.value)
        return ClientServiceResult.ReadValueAttributeResult(status_code, value)

    def read_data_type_attribute(self, node_id):
        out_data_type = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_readDataTypeAttribute(self.ua_client, node_id, out_data_type)
        return ClientServiceResult.ReadDataTypeAttribute(status_code, out_data_type)

    def read_value_rank_attribute(self, node_id):
        out_value_rank = ffi.new("UA_Int32*")
        status_code = lib.UA_Client_readValueRankAttribute(self.ua_client, node_id, out_value_rank)
        return ClientServiceResult.ReadValueRankAttribute(status_code, out_value_rank)

    def read_array_dimensions_attribute(self, node_id):
        out_array_dimensions_size = ffi.new("size_t*")
        out_array_dimensions = ffi.new("UA_UInt32**")
        status_code = lib.UA_Client_readArrayDimensionsAttribute(self.ua_client, node_id, out_array_dimensions_size,
                                                                 out_array_dimensions)
        return ClientServiceResult.ReadArrayDimensionsAttributeResult(status_code, out_array_dimensions_size,
                                                                      out_array_dimensions)

    def read_access_level_attribute(self, node_id):
        out_access_level = ffi.new("UA_Byte*")
        status_code = lib.UA_Client_readAccessLevelAttribute(self.ua_client, node_id, out_access_level)
        return ClientServiceResult.ReadAccessLevelAttributeResult(status_code, out_access_level)

    def read_user_access_level_attribute(self, node_id):
        out_user_access_level = ffi.new("UA_Byte*")
        status_code = lib.UA_Client_readUserAccessLevelAttribute(self.ua_client, node_id, out_user_access_level)
        return ClientServiceResult.ReadUserAccessLevelAttributeResult(status_code, out_user_access_level)

    def read_minimum_sampling_interval_attribute(self, node_id):
        out_min_sampling_interval = ffi.new("UA_Double*")
        status_code = lib.UA_Client_readMinimumSamplingIntervalAttribute(self.ua_client, node_id,
                                                                         out_min_sampling_interval)
        return ClientServiceResult.ReadMinimumSamplingIntervalAttributeResult(status_code, out_min_sampling_interval)

    def read_executable_attribute(self, node_id):
        out_executable = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_readExecutableAttribute(self.ua_client, node_id, out_executable)
        return ClientServiceResult.ReadExecutableAttributeResult(status_code, out_executable)

    def read_user_executable_attribute(self, node_id):
        out_user_executable = ffi.new("UA_Boolean*")
        status_code = lib.UA_Client_readUserExecutableAttribute(self.ua_client, node_id, out_user_executable)
        return ClientServiceResult.ReadUserExecutableAttributeResult(status_code, out_user_executable)

    # high level write service

    def write_node_id_attribute(self, node_id, new_node_id):
        return lib.UA_Client_writeNodeIdAttribute(self.ua_client, node_id, new_node_id)

    def write_node_class_attribute(self, node_id, new_node_class):
        return lib.UA_Client_writeNodeClassAttribute(self.ua_client, node_id, new_node_class)

    def write_browse_name_attribute(self, node_id, new_browse_name):
        return lib.UA_Client_writeBrowseNameAttribute(self.ua_client, node_id, new_browse_name)

    def write_display_name_attribute(self, node_id, new_display_name):
        return lib.UA_Client_writeDisplayNameAttribute(self.ua_client, node_id, new_display_name)

    def write_description_attribute(self, node_id, new_description):
        return lib.UA_Client_writeDescriptionAttribute(self.ua_client, node_id, new_description)

    def write_write_mask_attribute(self, node_id, new_write_mask):
        return lib.UA_Client_writeWriteMaskAttribute(self.ua_client, node_id, new_write_mask)

    def write_user_write_mask_attribute(self, node_id, new_user_write_mask):
        return lib.UA_Client_writeUserWriteMaskAttribute(self.ua_client, node_id, new_user_write_mask)

    def write_is_abstract_attribute(self, node_id, new_is_abstract):
        return lib.UA_Client_writeIsAbstractAttribute(self.ua_client, node_id, new_is_abstract)

    def write_symmetric_attribute(self, node_id, new_symmetric):
        return lib.UA_Client_writeSymmetricAttribute(self.ua_client, node_id, new_symmetric)

    def write_inverse_name_attribute(self, node_id, new_inverse_name):
        return lib.UA_Client_writeInverseNameAttribute(self.ua_client, node_id, new_inverse_name)

    def write_contains_no_loops_attribute(self, node_id, new_contains_no_loops):
        return lib.UA_Client_writeContainsNoLoopsAttribute(self.ua_client, node_id, new_contains_no_loops)

    def write_event_notifier_attribute(self, node_id, new_event_notifier):
        return lib.UA_Client_writeEventNotifierAttribute(self.ua_client, node_id, new_event_notifier)

    def write_value_attribute(self, node_id, new_value):
        return lib.UA_Client_writeValueAttribute(self.ua_client, node_id, new_value)

    def write_data_type_attribute(self, node_id, new_data_type):
        return lib.UA_Client_writeDataTypeAttribute(self.ua_client, node_id, new_data_type)

    def write_value_rank_attribute(self, node_id, new_value_rank):
        return lib.UA_Client_writeValueRankAttribute(self.ua_client, node_id, new_value_rank)

    def write_array_dimensions_attribute(self, node_id, new_array_dimensions_size, new_array_dimensions):
        return lib.UA_Client_writeArrayDimensionsAttribute(self.ua_client, node_id, new_array_dimensions_size,
                                                           new_array_dimensions)

    def write_access_level_attribute(self, node_id, new_access_level):
        return lib.UA_Client_writeAccessLevelAttribute(self.ua_client, node_id, new_access_level)

    def write_user_access_level_attribute(self, node_id, new_user_access_level):
        return lib.UA_Client_writeUserAccessLevelAttribute(self.ua_client, node_id, new_user_access_level)

    def write_minimum_sampling_interval_attribute(self, node_id, new_min_interval):
        return lib.UA_Client_writeMinimumSamplingIntervalAttribute(self.ua_client, node_id, new_min_interval)

    def write_executable_attribute(self, node_id, new_executable):
        return lib.UA_Client_writeExecutableAttribute(self.ua_client, node_id, new_executable)

    def write_user_executable_attribute(self, node_id, new_user_executable):
        return lib.UA_Client_writeUserExecutableAttribute(self.ua_client, node_id, new_user_executable)

    # misc high level service

    def call(self, object_id, method_id, input_size, call_input):
        output_size = ffi.new("size_t*")
        output = ffi.new("UA_Variant **")
        status_code = lib.UA_Client_call(self.ua_client, object_id, method_id, input_size, call_input, output_size,
                                         output)
        return ClientServiceResult.CallResult(status_code, output_size, output)

    def add_reference(self, source_node_id, reference_type_id, is_forward, target_server_uri, target_node_id,
                      target_node_class):
        return lib.UA_Client_addReference(self.ua_client, source_node_id, reference_type_id, is_forward,
                                          target_server_uri, target_node_id, target_node_class)

    def delete_reference(self, source_node_id, reference_type_id, is_forward, target_node_id, delete_bidirectional):
        return lib.UA_Client_deleteReference(self.ua_client, source_node_id, reference_type_id, is_forward,
                                             target_node_id, delete_bidirectional)

    def delete_node(self, node_id, delete_target_references):
        return lib.UA_Client_deleteNode(self.ua_client, node_id, delete_target_references)

    # high level add node services

    def add_variable_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition,
                          attr=DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_addVariableNode(self.ua_client, requested_new_node_id, parent_node_id,
                                                    reference_type_id, browse_name, type_definition, attr,
                                                    out_new_node_id)
        return ClientServiceResult.AddNodeResult(status_code, out_new_node_id)

    def add_variable_type_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                               attr=DefaultAttributes.VARIABLE_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_addVariableTypeNode(self.ua_client, requested_new_node_id, parent_node_id,
                                                        reference_type_id, browse_name, attr, out_new_node_id)
        return ClientServiceResult.AddNodeResult(status_code, out_new_node_id)

    def add_object_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition,
                        attr=DefaultAttributes.OBJECT_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_addObjectNode(self.ua_client, requested_new_node_id, parent_node_id,
                                                  reference_type_id, browse_name, type_definition, attr,
                                                  out_new_node_id)
        return ClientServiceResult.AddNodeResult(status_code, out_new_node_id)

    def add_object_type_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                             attr=DefaultAttributes.OBJECT_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_addObjectTypeNode(self.ua_client, requested_new_node_id, parent_node_id,
                                                      reference_type_id, browse_name, attr, out_new_node_id)
        return ClientServiceResult.AddNodeResult(status_code, out_new_node_id)

    def add_view_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                      attr=DefaultAttributes.VIEW_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_addViewNode(self.ua_client, requested_new_node_id, parent_node_id,
                                                reference_type_id, browse_name, attr, out_new_node_id)
        return ClientServiceResult.AddNodeResult(status_code, out_new_node_id)

    def add_reference_type_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                                attr=DefaultAttributes.REFERENCE_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_addReferenceTypeNode(self.ua_client, requested_new_node_id, parent_node_id,
                                                         reference_type_id, browse_name, attr, out_new_node_id)
        return ClientServiceResult.AddNodeResult(status_code, out_new_node_id)

    def add_data_type_node(self, requested_node_id, parent_node_id, reference_type_id, browse_name,
                           attr=DefaultAttributes.DATA_TYPE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_addDataTypeNode(self.ua_client, requested_node_id, parent_node_id,
                                                    reference_type_id, browse_name, attr, out_new_node_id)
        return ClientServiceResult.AddNodeResult(status_code, out_new_node_id)

    def add_method_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name,
                        attr=DefaultAttributes.METHOD_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_addMethodNode(self.ua_client, requested_new_node_id, parent_node_id,
                                                  reference_type_id, browse_name, attr, out_new_node_id)
        return ClientServiceResult.AddNodeResult(status_code, out_new_node_id)

    # utils

    def get_config(self):
        return lib.UA_Client_getConfig(self.ua_client)

    def set_default_config(self):
        lib.UA_ClientConfig_setDefault(self.get_config())

    def find_data_type(self, type_id):
        return lib.UA_Client_findDataType(self.ua_client, type_id)

    def get_endpoints(self, server_url, endpoint_descriptions_size, endpoint_descriptions):
        return lib.UA_Client_getEndpoints(self.ua_client, server_url, endpoint_descriptions_size, endpoint_descriptions)

    def find_servers(self, server_url, server_uris_size, locale_ids_size, locale_ids, registered_servers_size,
                     registered_servers):
        return lib.UA_Client_findServers(self.ua_client, server_url, server_uris_size, locale_ids_size, locale_ids,
                                         registered_servers_size, registered_servers)

    def run_iterate(self, timeout):
        return lib.UA_Client_run_iterate(self.ua_client, timeout)

    #    def find_servers_on_network(self, server_url, starting_record_id, max_records_to_return,
    #                                server_capability_filter_size, server_on_network_size, server_on_network):
    #        return lib.UA_Client_findServersOnNetwork(self.ua_client, server_url, starting_record_id, max_records_to_return,
    #                                                  server_capability_filter_size, server_on_network_size,
    #                                                  server_on_network)

    # async read service
    # todo: improve handling (callback selection for read_callback)
    def send_async_read_request(self, request, read_callback, callback):
        return lib.UA_Client_sendAsyncReadRequest(self.ua_client, request, read_callback, callback, ffi.new("UA_UInt32*"))

    def read_data_type_attribute_async(self, node_id, callback):
        return lib.UA_Client_readDataTypeAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadDataTypeAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_value_attribute_async(self, node_id, callback):
        return lib.UA_Client_readValueAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadValueAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_node_id_attribute_async(self, node_id, callback):
        return lib.UA_Client_readNodeIdAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadNodeIdAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_node_class_attribute_async(self, node_id, callback):
        return lib.UA_Client_readNodeClassAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadNodeClassAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_browse_name_attribute_async(self, node_id, callback):
        return lib.UA_Client_readBrowseNameAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadBrowseNameAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_display_name_attribute_async(self, node_id, callback):
        return lib.UA_Client_readDisplayNameAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadDisplayNameAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_description_attribute_async(self, node_id, callback):
        return lib.UA_Client_readDescriptionAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadDescriptionAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_write_mask_attribute_async(self, node_id, callback):
        return lib.UA_Client_readWriteMaskAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadWriteMaskAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def readUser_write_mask_attribute_async(self, node_id, callback):
        return lib.UA_Client_readUserWriteMaskAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadUserWriteMaskAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_is_abstract_attribute_async(self, node_id, callback):
        return lib.UA_Client_readIsAbstractAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadIsAbstractAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_symmetric_attribute_async(self, node_id, callback):
        return lib.UA_Client_readSymmetricAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadSymmetricAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_inverse_name_attribute_async(self, node_id, callback):
        return lib.UA_Client_readInverseNameAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadInverseNameAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_contains_no_loops_attribute_async(self, node_id, callback):
        return lib.UA_Client_readContainsNoLoopsAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadContainsNoLoopsAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_event_notifier_attribute_async(self, node_id, callback):
        return lib.UA_Client_readEventNotifierAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadEventNotifierAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_value_rank_attribute_async(self, node_id, callback):
        return lib.UA_Client_readValueRankAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadValueRankAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_access_level_attribute_async(self, node_id, callback):
        return lib.UA_Client_readAccessLevelAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadAccessLevelAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_user_access_level_attribute_async(self, node_id, callback):
        return lib.UA_Client_readUserAccessLevelAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadUserAccessLevelAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_minimum_sampling_interval_attribute_async(self, node_id, callback):
        return lib.UA_Client_readMinimumSamplingIntervalAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadMinimumSamplingIntervalAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_historizing_attribute_async(self, node_id, callback):
        return lib.UA_Client_readHistorizingAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadHistorizingAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_executable_attribute_async(self, node_id, callback):
        return lib.UA_Client_readExecutableAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadExecutableAttributeCallback, callback, ffi.new("UA_UInt32*"))

    def read_user_executable_attribute_async(self, node_id, callback):
        return lib.readUserExecutableAttribute_async(self.ua_client, node_id, lib.python_wrapper_UA_ClientAsyncReadUserExecutableAttributeCallback, callback, ffi.new("UA_UInt32*"))

    # async write service
    # UA_Client_sendAsyncWriteRequest(self.ua_client, request, writeCallback, user_data, req_id)
    #
    # UA_Client_writeValueAttribute_async(self.ua_client, node_id, newValue, callback, user_data, req_id)
    #
    # UA_Client_writeNodeIdAttribute_async(self.ua_client, node_id, outNodeId, callback, user_data, req_id)
    #
    # UA_Client_writeNodeClassAttribute_async(self.ua_client, node_id, outNodeClass, callback, user_data, req_id)
    #
    # UA_Client_writeBrowseNameAttribute_async(self.ua_client, node_id, outBrowseName, callback, user_data, req_id)
    #
    # UA_Client_writeDisplayNameAttribute_async(self.ua_client, node_id, outDisplayName, callback, user_data, req_id)
    #
    # UA_Client_writeDescriptionAttribute_async(self.ua_client, node_id, outDescription, callback, user_data, req_id)
    #
    # UA_Client_writeWriteMaskAttribute_async(self.ua_client, node_id, outWriteMask, callback, user_data, req_id)
    #
    # UA_Client_writeUserWriteMaskAttribute_async(self.ua_client, node_id, outUserWriteMask, callback, user_data, req_id)
    #
    # UA_Client_writeIsAbstractAttribute_async(self.ua_client, node_id, outIsAbstract, callback, user_data, req_id)
    #
    # UA_Client_writeSymmetricAttribute_async(self.ua_client, node_id, outSymmetric, callback, user_data, req_id)
    #
    # UA_Client_writeInverseNameAttribute_async(self.ua_client, node_id, outInverseName, callback, user_data, req_id)
    #
    # UA_Client_writeContainsNoLoopsAttribute_async(self.ua_client, node_id, outContainsNoLoops, callback, user_data, req_id)
    #
    # UA_Client_writeEventNotifierAttribute_async(self.ua_client, node_id, outEventNotifier, callback, user_data, req_id)
    #
    # UA_Client_writeDataTypeAttribute_async(self.ua_client, node_id, outDataType, callback, user_data, req_id)
    #
    # UA_Client_writeValueRankAttribute_async(self.ua_client, node_id, outValueRank, callback, user_data, req_id)
    #
    # UA_Client_writeAccessLevelAttribute_async(self.ua_client, node_id, outAccessLevel, callback, user_data, req_id)
    #
    # UA_Client_writeUserAccessLevelAttribute_async(self.ua_client, node_id, outUserAccessLevel, callback, user_data, req_id)
    #
    # UA_Client_writeMinimumSamplingIntervalAttribute_async(self.ua_client, outMinimumSamplingInterval, callback, user_data, req_id)
    #
    # UA_Client_writeHistorizingAttribute_async(self.ua_client, node_id, outHistorizing, callback, user_data, req_id)
    #
    # UA_Client_writeExecutableAttribute_async(self.ua_client, node_id, outExecutable, callback, user_data, req_id)
    #
    # UA_Client_writeUserExecutableAttribute_async(self.ua_client, node_id, outUserExecutable, callback, user_data, req_id)

    # call service
    # __UA_Client_call_async(self.ua_client, const UA_NodeId objectId, const UA_NodeId methodId, size_t inputSize, const UA_Variant *input, UA_ClientAsyncServiceCallback callback, user_data, req_id);
    # UA_Client_call_async(self.ua_client, const UA_NodeId objectId, const UA_NodeId methodId, size_t inputSize, const UA_Variant *input, UA_ClientAsyncCallCallback callback, user_data, req_id);

    # add node service

    async def add_variable_node_async(self, requeste_new_node_id, parent_node_id, reference_type_id, browse_name,
                                      type_definition, callback, user_data, req_id,
                                      attr=DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT):
        out_new_node_id = ffi.new("UA_NodeId*")
        status_code = lib.UA_Client_addVariableNode_async(self.ua_client, requeste_new_node_id, parent_node_id,
                                                          reference_type_id, browse_name, type_definition, attr,
                                                          out_new_node_id, callback, user_data, req_id)
        return ClientServiceResult.AddNodeResult(status_code, out_new_node_id)

    # UA_Client_addVariableTypeNode_async(self.ua_client, const UA_NodeId requestedNewNodeId, const UA_NodeId parentNodeId, const UA_NodeId referenceTypeId, const UA_QualifiedName browseName, const UA_VariableTypeAttributes attr, UA_NodeId *outNewNodeId, UA_ClientAsyncAddNodesCallback callback, user_data, req_id);
    # UA_Client_addObjectNode_async(self.ua_client, const UA_NodeId requestedNewNodeId, const UA_NodeId parentNodeId, const UA_NodeId referenceTypeId, const UA_QualifiedName browseName, const UA_NodeId typeDefinition, const UA_ObjectAttributes attr, UA_NodeId *outNewNodeId, UA_ClientAsyncAddNodesCallback callback, user_data, req_id);
    # UA_Client_addObjectTypeNode_async(self.ua_client, const UA_NodeId requestedNewNodeId, const UA_NodeId parentNodeId, const UA_NodeId referenceTypeId, const UA_QualifiedName browseName, const UA_ObjectTypeAttributes attr, UA_NodeId *outNewNodeId, UA_ClientAsyncAddNodesCallback callback, user_data, req_id);
    # UA_Client_addViewNode_async(self.ua_client, const UA_NodeId requestedNewNodeId, const UA_NodeId parentNodeId, const UA_NodeId referenceTypeId, const UA_QualifiedName browseName, const UA_ViewAttributes attr, UA_NodeId *outNewNodeId, UA_ClientAsyncAddNodesCallback callback, user_data, req_id);
    # UA_Client_addReferenceTypeNode_async(self.ua_client, const UA_NodeId requestedNewNodeId, const UA_NodeId parentNodeId, const UA_NodeId referenceTypeId, const UA_QualifiedName browseName, const UA_ReferenceTypeAttributes attr, UA_NodeId *outNewNodeId, UA_ClientAsyncAddNodesCallback callback, user_data, req_id);
    # UA_Client_addDataTypeNode_async(self.ua_client, const UA_NodeId requestedNewNodeId, const UA_NodeId parentNodeId, const UA_NodeId referenceTypeId, const UA_QualifiedName browseName, const UA_DataTypeAttributes attr, UA_NodeId *outNewNodeId, UA_ClientAsyncAddNodesCallback callback, user_data, req_id);
    # UA_Client_addMethodNode_async(self.ua_client, const UA_NodeId requestedNewNodeId, const UA_NodeId parentNodeId, const UA_NodeId referenceTypeId, const UA_QualifiedName browseName, const UA_MethodAttributes attr, UA_NodeId *outNewNodeId, UA_ClientAsyncAddNodesCallback callback, user_data, req_id);

    # misc
    # UA_Client_sendAsyncBrowseRequest(self.ua_client, UA_BrowseRequest *request, UA_ClientAsyncBrowseCallback browseCallback, user_data, req_id);
