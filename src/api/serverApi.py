# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import lib, ffi
import server_service_results as ServerServiceResults
from ua_types import *
import typing

VARIABLE_ATTRIBUTES_DEFAULT = UaVariableAttributes(val=lib.UA_VariableAttributes_default)


class _ServerCallback:
    """These static c type callback implementations are used to call the actual callback functions which have been
    submitted by the open62541 user """

    callbacks_dict: typing.Dict[str, any] = dict()

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_DataSourceReadCallback(server, session_id, session_context, node_id, node_context,
                                                 include_source_time_stamp, numeric_range, value):
        callbacks_dict_key = str(UaNodeId(val=node_id))
        return _ServerCallback.callbacks_dict[callbacks_dict_key].read_callback(UaServer(val=server),
                                                                                UaNodeId(val=session_id,
                                                                                         is_pointer=True),
                                                                                Void(val=session_context,
                                                                                     is_pointer=True),
                                                                                UaNodeId(val=node_id, is_pointer=True),
                                                                                Void(val=node_context, is_pointer=True),
                                                                                UaBoolean(val=include_source_time_stamp,
                                                                                          is_pointer=False),
                                                                                UaNumericRange(val=numeric_range,
                                                                                               is_pointer=True),
                                                                                UaDataValue(val=value, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_DataSourceWriteCallback(server, session_id,
                                                  session_context, node_id,
                                                  node_context, numeric_range,
                                                  value):
        callbacks_dict_key = str(UaNodeId(val=node_id))
        return _ServerCallback.callbacks_dict[callbacks_dict_key].write_callback(UaServer(val=server),
                                                                                 UaNodeId(val=session_id,
                                                                                          is_pointer=True),
                                                                                 Void(val=session_context,
                                                                                      is_pointer=True),
                                                                                 UaNodeId(val=node_id, is_pointer=True),
                                                                                 Void(val=node_context,
                                                                                      is_pointer=True),
                                                                                 UaNumericRange(val=numeric_range,
                                                                                                is_pointer=True),
                                                                                 UaDataValue(val=value,
                                                                                             is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ValueCallbackOnReadCallback(server, session_id,
                                                      session_context, node_id,
                                                      node_context, numeric_range,
                                                      value):
        callbacks_dict_key = str(UaNodeId(val=node_id))
        _ServerCallback.callbacks_dict[callbacks_dict_key].read_callback(UaServer(val=server),
                                                                         UaNodeId(val=session_id, is_pointer=True),
                                                                         Void(val=session_context, is_pointer=True),
                                                                         UaNodeId(val=node_id, is_pointer=True),
                                                                         Void(val=node_context, is_pointer=True),
                                                                         UaNumericRange(val=numeric_range,
                                                                                        is_pointer=True),
                                                                         UaDataValue(val=value, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_ValueCallbackOnWriteCallback(server, session_id,
                                                       session_context, node_id,
                                                       node_context, numeric_range,
                                                       value):
        callbacks_dict_key = str(UaNodeId(val=node_id))
        _ServerCallback.callbacks_dict[callbacks_dict_key].write_callback(UaServer(val=server),
                                                                          UaNodeId(val=session_id, is_pointer=True),
                                                                          Void(val=session_context, is_pointer=True),
                                                                          UaNodeId(val=node_id, is_pointer=True),
                                                                          Void(val=node_context, is_pointer=True),
                                                                          UaNumericRange(val=numeric_range,
                                                                                         is_pointer=True),
                                                                          UaDataValue(val=value, is_pointer=True))

    # todo: ExternalValueCallback is missing


class UaServer:

    def __init__(self, config=None, val=None):
        if val is not None:
            self.ua_server = val
        elif config is None:
            self.ua_server = lib.UA_Server_new()
            self.set_default_config()
        else:
            self.ua_server = lib.UA_Server_newWithConfig(config._ptr)

    def run(self, running: UaBoolean):
        raw_result = lib.UA_Server_run(self.ua_server, running._ptr)
        return UaStatusCode(val=raw_result)

    def run_shutdown(self):
        raw_result = lib.UA_Server_run_shutdown(self.ua_server)
        return UaStatusCode(val=raw_result)

    def getConfig(self):
        # TODO: UaServerConfig is missing
        return lib.UA_Server_getConfig(self.ua_server)

    def run_startup(self):
        raw_value = lib.UA_Server_run_startup(self.ua_server)
        return UaStatusCode(val=raw_value)

    def run_iterate(self, wait_internal: UaBoolean):
        raw_value = lib.UA_Server_run_iterate(self.ua_server, wait_internal._val)
        return UaUInt16(val=raw_value)

    # TODO:
    #    def delete(self):
    #        return lib.UA_Server_delete(self.ua_server)

    def set_minimal_config(self, port_number: UaInt16, certificate: UaByteString):
        raw_result = lib.UA_ServerConfig_setMinimal(self.getConfig(), port_number._val, certificate._ptr)
        return UaStatusCode(val=raw_result)

    def set_default_config(self):
        raw_result = lib.UA_ServerConfig_setDefault(self.getConfig())
        return UaStatusCode(val=raw_result)

    ###
    ### Write Functions
    ###

    def write(self, value: UaDataValue):
        raw_result = lib.UA_Server_write(self.ua_server, value._ptr)
        value._update()
        return UaStatusCode(val=raw_result)

    def write_value(self, node_id: UaNodeId, value: UaVariant):
        raw_result = lib.UA_Server_writeValue(self.ua_server, node_id._val, value._val)
        return UaStatusCode(val=raw_result)

    def write_data_value(self, node_id: UaNodeId, value: UaDataValue):
        raw_value = lib.UA_Server_writeDataValue(self.ua_server, node_id._val, value._val)
        return UaStatusCode(val=raw_value)

    def write_data_type(self, node_id: UaNodeId, data_type: UaDataValue):
        raw_value = lib.UA_Server_writeDataType(self.ua_server, node_id._val, data_type._val)
        return UaStatusCode(val=raw_value)

    def write_value_rank(self, node_id: UaNodeId, value_rank: UaInt32):
        raw_value = lib.UA_Server_writeValueRank(self.ua_server, node_id._val, value_rank._val)
        return UaStatusCode(val=raw_value)

    def write_array_dimensions(self, node_id: UaNodeId, array_dimensions: UaVariant):
        raw_value = lib.UA_Server_writeArrayDimensions(self.ua_server, node_id._val, array_dimensions._val)
        return UaStatusCode(val=raw_value)

    def write_access_level(self, node_id: UaNodeId, access_level: UaByte):
        raw_value = lib.UA_Server_writeAccessLevel(self.ua_server, node_id._val, access_level._val)
        return UaStatusCode(val=raw_value)

    def write_minimum_sampling_interval(self, node_id: UaNodeId, minimum_sampling_interval: UaDouble):
        raw_value = lib.UA_Server_writeMinimumSamplingInterval(self.ua_server, node_id._val,
                                                               minimum_sampling_interval._val)
        return UaStatusCode(val=raw_value)

    def write_executable(self, node_id: UaNodeId, executable: UaBoolean):
        raw_value = lib.UA_Server_writeExecutable(self.ua_server, node_id._val, executable._val)
        return UaStatusCode(val=raw_value)

    def write_object_property(self, object_id: UaNodeId, property_name: UaQualifiedName,
                              value: UaDataValue):
        raw_value = lib.UA_Server_writeObjectProperty(self.ua_server, object_id._val, property_name._val, value._val)
        return UaStatusCode(val=raw_value)

    def write_object_property_scalar(self,
                                     object_id: UaNodeId,
                                     property_name: UaQualifiedName,
                                     value: UaDataValue,
                                     data_type: UaDataType):
        raw_value = lib.UA_Server_writeObjectProperty_scalar(self.ua_server, object_id._val, property_name._val,
                                                             value._ptr, data_type._ptr)
        value._update()
        data_type._update()
        return UaStatusCode(val=raw_value)

    ###
    ### Read Functions
    ###

    def read(self, item: UaReadValueId, timestamps: UaTimestampsToReturn):
        raw_result = lib.UA_Server_read(self.ua_server, item._ptr, timestamps._val)
        item._update()
        return UaDataValue(val=raw_result)

    def read_object_property(self, object_id: UaNodeId, property_name: UaQualifiedName,
                             value: UaDataValue):
        raw_value = lib.UA_Server_readObjectProperty(self.ua_server, object_id._val, property_name._val, value._ptr)
        value._update()
        return UaStatusCode(val=raw_value)

    def read_node_id(self, node_id: UaNodeId):
        out_node_id = UaNodeId()
        status_code = lib.UA_Server_readNodeId(self.ua_server, node_id._val, out_node_id._ptr)
        out_node_id._update()
        return ServerServiceResults.NodeIdResult(status_code, out_node_id._ptr)

    def read_node_class(self, node_id: UaNodeId):
        out_node_class = UaNodeClass()
        status_code = lib.UA_Server_readNodeClass(self.ua_server, node_id._val, out_node_class._ptr)
        return ServerServiceResults.NodeClassResult(status_code, out_node_class._ptr)

    def read_browse_name(self, node_id: UaNodeId):
        out_browse_name = UaQualifiedName()
        status_code = lib.UA_Server_readBrowseName(self.ua_server, node_id._val, out_browse_name._ptr)
        out_browse_name._update()
        return ServerServiceResults.BrowseNameResult(status_code, out_browse_name)

    def read_display_name(self, node_id: UaNodeId):
        out_display_name = UaLocalizedText()
        status_code = lib.UA_Server_readDisplayName(self.ua_server, node_id._val, out_display_name._ptr)
        out_display_name._update()
        return ServerServiceResults.LocalizedTextResult(status_code, out_display_name._ptr)

    def read_description(self, node_id: UaNodeId):
        out_description = UaLocalizedText()
        status_code = lib.UA_Server_readDescription(self.ua_server, node_id._val, out_description._ptr)
        out_description._update()
        return ServerServiceResults.LocalizedTextResult(status_code, out_description._ptr)

    def read_write_mask(self, node_id: UaNodeId):
        out_write_mask = UaUInt32()
        status_code = lib.UA_Server_readWriteMask(self.ua_server, node_id._val, out_write_mask._ptr)
        return ServerServiceResults.UInt32Result(status_code, out_write_mask._ptr)

    def read_is_abstract(self, node_id: UaNodeId):
        out_is_abstract = UaBoolean()
        status_code = lib.UA_Server_readIsAbstract(self.ua_server, node_id._val, out_is_abstract._ptr)
        return ServerServiceResults.BooleanResult(status_code, out_is_abstract._ptr)

    def read_symmetric(self, node_id: UaNodeId):
        out_symmetric = UaBoolean()
        status_code = lib.UA_Server_readSymmetric(self.ua_server, node_id._val, out_symmetric._ptr)
        return ServerServiceResults.BooleanResult(status_code, out_symmetric._ptr)

    def read_inverse_name(self, node_id: UaNodeId):
        out_name = UaLocalizedText()
        status_code = lib.UA_Server_readInverseName(self.ua_server, node_id._val, out_name._ptr)
        out_name._update()
        return ServerServiceResults.LocalizedTextResult(status_code, out_name._ptr)

    def read_contains_no_loops(self, node_id: UaNodeId):
        out_no_loops = UaBoolean()
        status_code = lib.UA_Server_readContainsNoLoops(self.ua_server, node_id._val, out_no_loops._ptr)
        return ServerServiceResults.BooleanResult(status_code, out_no_loops._ptr)

    def read_event_notifier(self, node_id: UaNodeId):
        out_event_notifier = UaByte()
        status_code = lib.UA_Server_readEventNotifier(self.ua_server, node_id._val, out_event_notifier._ptr)
        return ServerServiceResults.ByteResult(status_code, out_event_notifier._ptr)

    def read_value(self, node_id: UaNodeId):
        out_value = UaVariant()
        status_code = lib.UA_Server_readValue(self.ua_server, node_id._val, out_value._ptr)
        out_value._update()
        return ServerServiceResults.VariantResult(status_code, out_value._ptr)

    def read_data_type(self, node_id: UaNodeId):
        out_type = UaNodeId()
        status_code = lib.UA_Server_readDataType(self.ua_server, node_id._val, out_type._ptr)
        out_type._update()
        return ServerServiceResults.NodeIdResult(status_code, out_type._ptr)

    def read_value_rank(self, node_id: UaNodeId):
        out_rank = UaUInt32()
        status_code = lib.UA_Server_readValueRank(self.ua_server, node_id._val, out_rank._ptr)
        return ServerServiceResults.UInt32Result(status_code, out_rank._ptr)

    def read_array_dimensions(self, node_id: UaNodeId):
        out_dim = UaVariant()
        status_code = lib.UA_Server_readArrayDimensions(self.ua_server, node_id._val, out_dim._ptr)
        out_dim._update()
        return ServerServiceResults.VariantResult(status_code, out_dim._ptr)

    def read_access_level(self, node_id: UaNodeId):
        out_level = UaByte()
        status_code = lib.UA_Server_readAccessLevel(self.ua_server, node_id._val, out_level._ptr)
        return ServerServiceResults.ByteResult(status_code, out_level._ptr)

    def read_minimum_sampling_interval(self, node_id: UaNodeId):
        out_interval = UaDouble()
        status_code = lib.UA_Server_readMinimumSamplingInterval(self.ua_server, node_id._val, out_interval._ptr)
        return ServerServiceResults.DoubleResult(status_code, out_interval._ptr)

    def read_executable(self, node_id: UaNodeId):
        out_exe = UaBoolean()
        status_code = lib.UA_Server_readExecutable(self.ua_server, node_id._val, out_exe._ptr)
        return ServerServiceResults.BooleanResult(status_code, out_exe._ptr)

    # def read_historizing():  TODO: to be implemented...

    ###
    ### Browse Functions
    ###

    def browse(self, max_refs: UaUInt32):  # TODO: implement UaBrowseDescription
        out_bd = UaBrowseDescription()
        status_code = lib.UA_Server_browse(self.ua_server, max_refs._val, out_bd._ptr)
        out_bd._update()
        return ServerServiceResults.BrowseResultResult(status_code, out_bd._ptr)

    def browse_next(self, release_continuation_point: UaBoolean, continuation_point: UaByteString):
        raw_value = lib.UA_Server_browseNext(self.ua_server, release_continuation_point._val, continuation_point._ptr)
        continuation_point._update()
        return UaBrowseResult(val=raw_value)

    def translate_browse_path_to_node_ids(self, browse_path: UaBrowsePath):
        raw_value = lib.UA_Server_translateBrowsePathToNodeIds(self.ua_server, browse_path._ptr)
        browse_path._update()
        return UaBrowsePathResult(val=raw_value)

    ###
    ### Misc Functions
    ###

    def call(self, request: UaCallMethodRequest):
        raw_value = lib.UA_Server_call(self.ua_server, request._ptr)
        request._update()
        return UaCallMethodResult(val=raw_value)

    def add_data_source_variable_node(self,
                                      requested_new_node_id: UaNodeId,
                                      parent_node_id: UaNodeId,
                                      reference_type_id: UaNodeId,
                                      browse_name: UaQualifiedName,
                                      type_definition: UaNodeId,
                                      data_source: UaDataSource,
                                      attr: UaVariableAttributes = None,
                                      node_context=None):

        out_node_id = UaNodeId()

        if attr is None:
            attr = VARIABLE_ATTRIBUTES_DEFAULT

        if node_context is not None:
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        # todo: requested_new_node_id currently mustn't be NULL or this doesn't work
        _ServerCallback.callbacks_dict[str(requested_new_node_id)] = data_source

        status_code = lib.UA_Server_addDataSourceVariableNode(self.ua_server, requested_new_node_id._val,
                                                              parent_node_id._val, reference_type_id._val,
                                                              browse_name._val, type_definition._val, attr._val,
                                                              data_source._val, node_context, out_node_id._ptr)
        out_node_id._update()

        # todo: update dict entry with out node id

        return ServerServiceResults.NodeIdResult(UaStatusCode(status_code),
                                                 out_node_id)  # TODO: out_node not None?

    def delete_node(self, node_id: UaNodeId, delete_references: UaBoolean):
        raw_result = lib.UA_Server_deleteNode(self.ua_server, node_id._val, delete_references._val)
        return UaStatusCode(val=raw_result)

    def add_reference(self,
                      source_id: UaNodeId,
                      ref_type_id: UaNodeId,
                      target_id: UaNodeId,
                      is_forward: UaBoolean):

        raw_result = lib.UA_Server_addReference(self.ua_server, source_id._val, ref_type_id._val, target_id._val,
                                                is_forward._val)
        return UaStatusCode(val=raw_result)

    def delete_reference(self,
                         source_node_id: UaNodeId,
                         reference_type_id: UaNodeId,
                         is_forward: UaBoolean,
                         target_node_id: UaNodeId,
                         delete_bidirectional: UaBoolean):

        raw_result = lib.UA_Server_deleteReference(self.ua_server, source_node_id._val, reference_type_id._val,
                                                   is_forward._val, target_node_id._val, delete_bidirectional._val)
        return UaStatusCode(val=raw_result)

    def add_variable_node(self,
                          requested_new_node_id: UaNodeId,
                          parent_node_id: UaNodeId,
                          reference_type_id: UaNodeId,
                          browse_name: UaQualifiedName,
                          type_definition: UaNodeId,
                          attr=None,
                          node_context=None):

        if attr is None:
            attr = VARIABLE_ATTRIBUTES_DEFAULT

        out_node_id = UaNodeId()

        # TODO: test
        if node_context is not ffi.NULL:
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        status_code = lib.UA_Server_addVariableNode(self.ua_server, requested_new_node_id._val, parent_node_id._val,
                                                    reference_type_id._val, browse_name._val, type_definition._val,
                                                    attr._val, node_context, out_node_id._ptr)
        out_node_id._update()
        return ServerServiceResults.NodeIdResult(UaStatusCode(status_code), out_node_id)

    def add_variable_type_node(self,
                               requested_new_node_id: UaNodeId,
                               parent_node_id: UaNodeId,
                               reference_type_id: UaNodeId,
                               browse_name: UaQualifiedName,
                               type_definition: UaNodeId,
                               attr: UaNodeAttributes = None,
                               node_context=None):

        if attr is None:
            attr = VARIABLE_ATTRIBUTES_DEFAULT

        out_node_id = UaNodeId()

        # TODO: test
        if node_context is not ffi.NULL:
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        status_code = lib.UA_Server_addVariableTypeNode(self.ua_server, requested_new_node_id._val, parent_node_id._val,
                                                        reference_type_id._val, browse_name._val, type_definition._val,
                                                        attr._val, node_context, out_node_id._ptr)
        out_node_id._update()
        return ServerServiceResults.NodeIdResult(UaStatusCode(status_code), out_node_id)

    def add_object_node(self,
                        requested_new_node_id: UaNodeId,
                        parent_node_id: UaNodeId,
                        reference_type_id: UaNodeId,
                        browse_name: UaQualifiedName,
                        type_definition: UaNodeId,
                        attr: UaNodeAttributes = None,
                        node_context=None):

        if attr is None:
            attr = VARIABLE_ATTRIBUTES_DEFAULT

        out_node_id = UaNodeId()

        # TODO: test
        if node_context is not None:
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        status_code = lib.UA_Server_addObjectNode(self.ua_server, requested_new_node_id._val, parent_node_id._val,
                                                  reference_type_id._val, browse_name._val, type_definition._val,
                                                  attr._val, node_context._ptr, out_node_id._ptr)
        out_node_id._update()
        return ServerServiceResults.NodeIdResult(UaStatusCode(status_code), out_node_id)

    def add_object_type_node(self,
                             requested_new_node_id: UaNodeId,
                             parent_node_id: UaNodeId,
                             reference_type_id: UaNodeId,
                             browse_name: UaQualifiedName,
                             type_definition: UaNodeId,
                             attr: UaNodeAttributes = None,
                             node_context=None):

        if attr is None:
            attr = VARIABLE_ATTRIBUTES_DEFAULT

        out_node_id = UaNodeId()

        # TODO: test
        if node_context is not None:
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        status_code = lib.UA_Server_addObjectTypeNode(self.ua_server, requested_new_node_id._val, parent_node_id._val,
                                                      reference_type_id._val, browse_name._val, type_definition._val,
                                                      attr._val, node_context._ptr, out_node_id._ptr)

        out_node_id._update()
        return ServerServiceResults.NodeIdResult(UaStatusCode(status_code), out_node_id)

    # TODO: implement and test:
    # def add_method_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, method, input_arg_size, input_args, output_arg_size, output_args, out_new_node_id, attr = VARIABLE_ATTRIBUTES_DEFAULT, node_context = None):
    #    out_node_id = ffi.new("UA_NodeId *")

    #    if node_context is not None:
    #        node_context = ffi.new_handle(node_context)
    #    else:
    #        node_context = ffi.NULL

    #    status_code = lib.UA_Server_addMethodNode()
    #    return ServerServiceResults.AddMethodNodeResult(UaStatusCode(status_code), output_arg_size, output_args, out_node)

    def set_node_type_lifecycle(self, node_id: UaNodeId,
                                lifecycle: UaNodeTypeLifecycle):
        raw_result = lib.UA_Server_addNodeTypeLifecycle(self.ua_server, node_id._val, lifecycle._val)
        return UaStatusCode(val=raw_result)

    def trigger_event(self, node_id: UaNodeId, origin_id: UaNodeId,
                      out_event_id: UaByteString, delete_event_node: UaBoolean):
        raw_result = lib.UA_Server_triggerEvent(self.ua_server, node_id._val, origin_id._val, out_event_id._ptr,
                                                delete_event_node._val)
        out_event_id._update()
        return UaStatusCode(val=raw_result)

    def set_variable_node_value_callback(self, node_id: UaNodeId,
                                         callback: UaValueCallback):
        _ServerCallback.callbacks_dict[str(node_id)] = callback
        raw_result = lib.UA_Server_setVariableNode_valueCallback(self.ua_server, node_id._val, callback._val)

        return UaStatusCode(val=raw_result)

    def set_variable_node_value_backend(self, node_id: UaNodeId,
                                        callback: UaValueBackend):
        raw_result = lib.UA_Server_setVariableNode_valueBackend(self.ua_server, node_id._val, callback._val)
        return UaStatusCode(val=raw_result)

    def create_condition(self,
                         condition_id: UaNodeId,
                         condition_type: UaNodeId,
                         condition_name: UaQualifiedName,
                         condition_source: UaNodeId,
                         hierarchical_reference_type: UaNodeId):

        out_node_id = ffi.new("UA_NodeId *")

        status_code = lib.UA_Server_createCondition(self.ua_server, condition_id._val, condition_type._val,
                                                    condition_name._val, condition_source._val,
                                                    hierarchical_reference_type._val, out_node_id._ptr)
        out_node_id._update()
        return ServerServiceResults.NodeIdResult(UaStatusCode(status_code), out_node_id)

    def set_condition_field(self, condition: UaNodeId, value: UaVariant,
                            field_name: UaQualifiedName):
        raw_result = lib.UA_Server_setConditionField(self.ua_server, condition._val, value._ptr, field_name._val)
        value._update()
        return UaStatusCode(val=raw_result)

    def set_condition_variable_field_property(self,
                                              condition: UaNodeId,
                                              value: UaVariant,
                                              var_field_name: UaQualifiedName,
                                              var_property_name: UaQualifiedName):

        raw_result = lib.UA_Server_setConditionVariableFieldProperty(self.ua_server, condition._val, value._ptr,
                                                                     var_field_name._val, var_property_name._val)
        value._update()
        return UaStatusCode(val=raw_result)

    def trigger_condition_event(self, condition: UaNodeId, condition_source: UaNodeId):
        out_event_id = UaByteString()
        status_code = lib.UA_Server_triggerConditionEvent(self.ua_server, condition._val, condition_source._val,
                                                          out_event_id._ptr)
        out_event_id._update()
        return ServerServiceResults.EventResult(status_code, out_event_id)

    def set_condition_two_state_variable_callback(self,
                                                  condition: UaNodeId,
                                                  condition_source: UaNodeId,
                                                  remove_branch: UaBoolean,
                                                  callback: UaTwoStateVariableChangeCallback,
                                                  callback_type: UaTwoStateVariableCallbackType):  # TODO: implement UaTwoStateVariableCallbackType and UaTwoStateVariableChangeCallback

        raw_result = lib.UA_Server_setConditionTwoStateVariableCallback(self.ua_server, condition, condition_source,
                                                                        remove_branch, callback, callback_type)
        return UaStatusCode(raw_result)
