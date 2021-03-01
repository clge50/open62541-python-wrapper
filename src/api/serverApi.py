from intermediateApi import lib, ffi
import server_service_results as ServerServiceResults
import ua_types
    
    
VARIABLE_ATTRIBUTES_DEFAULT = lib.UA_VariableAttributes_default


class UaServer:
    def __init__(self, config=None):
        if config is None:
            self.ua_server = lib.UA_Server_new()
            self.set_default_config()
        else:
            self.ua_server = lib.UA_Server_newWithConfig(config)

    def run( self, running:ua_types.UaBoolean):
        raw_result = lib.UA_Server_run( self.ua_server, running)
        return ua_types.UaStatusCode(val=raw_result)

    def run_shutdown(self):
        raw_result = lib.UA_Server_run_shutdown(self.ua_server)
        return ua_types.UaStatusCode(val=raw_result)

    def getConfig(self):
          # UaServerConfig is missing
        return lib.UA_Server_getConfig(self.ua_server)

    def run_startup(self):
        raw_value = lib.UA_Server_run_startup(self.ua_server)
        return ua_types.UaStatusCode(val=raw_result)

    def run_iterate(self, wait_internal:ua_types.UaBoolean):
        raw_value = lib.UA_Server_run_iterate(self.ua_server, wait_internal._val)
        return ua_types.UaUInt16(val=raw_value)

    #    def delete(self):
    #        return lib.UA_Server_delete(self.ua_server)

    def set_minimal_config(self, port_number:ua_types.UaInt16, certificate:ua_types.UaByteString):
        raw_result = lib.UA_ServerConfig_setMinimal(self.getConfig(), port_number._val, certificate._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def set_default_config(self):
        raw_result = lib.UA_ServerConfig_setDefault(self.getConfig())
        return ua_types.UaStatusCode(val=raw_result)


#########
###
### new
###


    def read(self, item:ua_types.UaReadValueId, timestamps:ua_types.UaTimestampsToReturn):
        raw_result = lib.UA_Server_read(self.ua_server, item._ptr, timestamps._val)
        return ua_types.UaDataValue(val=raw_result)

    def write(self, value:ua_types.UaDataValue):
        raw_result = lib.UA_Server_write(self.ua_server, value._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def write_value(self, node_id: ua_types.UaNodeId, value:ua_types.UaDataValue):
        raw_result = lib.UA_Server_writeValue(self.ua_server, node_id, value)
        return ua_types.UaStatusCode(val=raw_result)
    
    def write_data_value(self, node_id: ua_types.UaNodeId, value:ua_types.UaDataValue):
        raw_value = lib.UA_Server_writeDataValue(self.ua_server, node_id._val, value._val)
        return ua_types.UaStatusCode(val=raw_result)
    
    def write_data_type(self, node_id: ua_types.UaNodeId, data_type:ua_types.UaDataValue):
        raw_value =  lib.UA_Server_writeDataType(self.ua_server, node_id._val, data_type._val)
        return ua_types.UaStatusCode(val=raw_result)

    def write_value_rank(self, node_id: ua_types.UaNodeId, value_rank:ua_types.UaInt32):
        raw_value =  lib.UA_Server_writeValueRank(self.ua_server, node_id._val, value_rank._val)
        return ua_types.UaStatusCode(val=raw_result)

    def write_array_dimensions(self, node_id: ua_types.UaNodeId, array_dimensions:ua_types.UaVariant):
        raw_value =  lib.UA_Server_writeArrayDimensions(self.ua_server, node_id._val, array_dimensions._val)
        return ua_types.UaStatusCode(val=raw_result)

    def write_access_level(self, node_id: ua_types.UaNodeId, access_level:ua_types.UaByte):
        raw_value =  lib.UA_Server_writeAccessLevel(self.ua_server, node_id._val, access_level._val)
        return ua_types.UaStatusCode(val=raw_result)

    def write_minimum_sampling_interval(self, node_id: ua_types.UaNodeId, minimum_sampling_interval:ua_types.UaDouble):
        raw_value =  lib.UA_Server_writeMinimumSamplingInterval(self.ua_server, node_id._val, minimum_sampling_interval._val)
        return ua_types.UaStatusCode(val=raw_result)

    def write_executable(self, node_id: ua_types.UaNodeId, executable:ua_types.UaBoolean):
        raw_value =  lib.UA_Server_writeExecutable(self.ua_server, node_id._val, executable._val)
        return ua_types.UaStatusCode(val=raw_result)
 
    def browse_next(self, release_continuation_point:ua_types.UaBoolean, continuation_point:ua_types.UaByteString):
        raw_value =  lib.UA_Server_browseNext(self.ua_server, release_continuation_point._val, continuation_point._ptr)
        return ua_types.UaBrowseResult(val=raw_result)

    def translate_browse_path_to_node_ids(self, browse_path:ua_types.UaBrowsePath):
        raw_value =  lib.UA_Server_translateBrowsePathToNodeIds(self.ua_server, browse_path._ptr)
        return ua_types.UaBrowsePathResult(val=raw_result)

    def write_object_property(self, object_id:ua_types.UaNodeId, property_name:ua_types.UaQualifiedName, value:ua_types.UaDataValue):
        raw_value =  lib.UA_Server_writeObjectProperty(self.ua_server, object_id._val, property_name._val, value._val)
        return ua_types.UaStatusCode(val=raw_result)

    def write_object_property_scalar(self, object_id:ua_types.UaNodeId, property_name:ua_types.UaQualifiedName, value:ua_types.UaDataValue, data_type:ua_types.UaDataType):
        raw_value =  lib.UA_Server_writeObjectProperty_scalar(self.ua_server, object_id._val, property_name._val, value._ptr, data_type._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def read_object_property(self, object_id:ua_types.UaNodeId, property_name:ua_types.UaQualifiedName, value:ua_types.UaDataValue):
        raw_value =  lib.UA_Server_readObjectProperty(self.ua_server, object_id._val, property_name._val, value._ptr)
        return ua_types.UaStatusCode(val=raw_result)

    def call(self, request:ua_types.UaCallMethodRequest):
        raw_value =  lib.UA_Server_call(self.ua_server, request._ptr)
        return ua_types.UaCallMethodResult(val=raw_result)

    def add_data_source_variable_node(self, requested_new_node_id: ua_types.UaNodeId, 
    parent_node_id: ua_types.UaNodeId, reference_type_id: ua_types.UaNodeId, browse_name:ua_types.UaQualifiedName, 
    type_definition:ua_types.UaNodeId, data_source, 
    attr:ua_types.UaVariableAttributes = VARIABLE_ATTRIBUTES_DEFAULT, node_context = None): # TODO:UaDataSource is missing
        out_node_id = ffi.new("UA_NodeId *")

        # TODO: test
        if node_context is not None: 
           node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        status_code = lib.UA_Server_addDataSourceVariableNode(self.ua_server, requested_new_node_id._val, parent_node_id._val, reference_type_id._val, browse_name._val, type_definition._val, attr._val, data_source._val, node_context._ptr, out_node_id._ptr)
        return ServerServiceResults.AddNodeAttributeResult(ua_types.UaStatusCode(status_code), out_node_id) # TODO: out_node not None?

    def delete_node(self, node_id:ua_types.UaNodeId, delete_references:ua_types.UaBoolean):
        raw_result = lib.UA_Server_deleteNode(self.ua_server, node_id._val, delete_references._val)
        return ua_types.UaStatusCode(val=raw_result)


    def add_reference(self , source_id:ua_types.UaNodeId, ref_type_id:ua_types.UaNodeId, target_id:ua_types.UaNodeId, is_forward:ua_types.UaBoolean):
        raw_result = lib.UA_Server_addReference(self.ua_server , source_id._val, ref_type_id._val, target_id._val, is_forward._val)
        return ua_types.UaStatusCode(val=raw_result)


    def delete_reference(self, source_node_id:ua_types.UaNodeId, reference_type_id:ua_types.UaNodeId,  is_forward:ua_types.UaBoolean, target_node_id:ua_types.UaNodeId, delete_bidirectional):
        raw_result = lib.UA_Server_deleteReference(self.ua_server, sourcenode_id._val, reference_type_id._val,  isForward._val, targetnode_id._val, deleteBidirectional._val)   
        return ua_types.UaStatusCode(val=raw_result)

    def add_variable_node(self, requested_new_node_id:ua_types.UaNodeId, 
    parent_node_id:ua_types.UaNodeId, reference_type_id:ua_types.UaNodeId, 
    browse_name:ua_types.UaQualifiedName, type_definition:ua_types.UaNodeId, 
    attr = VARIABLE_ATTRIBUTES_DEFAULT, node_context = None):
        out_node_id = ffi.new("UA_NodeId *")
                
        # TODO: test
        if node_context is not None: 
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL
        
        status_code = lib.UA_Server_addVariableNode(self.ua_server, requested_new_node_id._val, parent_node_id._val, reference_type_id._val, browse_name._val, type_definition._val, attr, node_context, out_node_id)
        return ServerServiceResults.AddNodeAttributeResult(ua_types.UaStatusCode(status_code), out_node_id)

    def add_variable_type_node(self, requested_new_node_id:ua_types.UaNodeId, parent_node_id:ua_types.UaNodeId, reference_type_id:ua_types.UaNodeId, browse_name:ua_types.UaQualifiedName, type_definition:ua_types.UaNodeId, attr:ua_types.UaNodeAttributes = VARIABLE_ATTRIBUTES_DEFAULT, node_context = None):
        out_node_id = ffi.new("UA_NodeId *")
                
        # TODO: test
        if node_context is not None: 
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL
        
        status_code = lib.UA_Server_addVariableTypeNode(self.ua_server, requested_new_node_id._val, parent_node_id._val, reference_type_id._val, browse_name._val, type_definition._val, attr, node_context, out_node_id._ptr)
        return ServerServiceResults.AddNodeAttributeResult(ua_types.UaStatusCode(status_code), out_node)

    def add_object_node(self, requested_new_node_id:ua_types.UaNodeId, parent_node_id:ua_types.UaNodeId, reference_type_id:ua_types.UaNodeId, browse_name:ua_types.UaQualifiedName, type_definition:ua_types.UaNodeId, attr:ua_types.UaNodeAttributes = VARIABLE_ATTRIBUTES_DEFAULT, node_context = None):
        out_node_id = ffi.new("UA_NodeId *")
                
        # TODO: test
        if node_context is not None: 
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL
        
        status_code = lib.UA_Server_addObjectNode(self.ua_server, requested_new_node_id._val, parent_node_id._val, reference_type_id._val, browse_name._val, type_definition._val, attr._val, node_context._ptr, out_node_id._ptr)
        return ServerServiceResults.AddNodeAttributeResult(ua_types.UaStatusCode(status_code), out_node)

    def add_object_type_node(self, requested_new_node_id:ua_types.UaNodeId, parent_node_id:ua_types.UaNodeId, reference_type_id:ua_types.UaNodeId, browse_name:ua_types.UaQualifiedName, type_definition:ua_types.UaNodeId, attr:ua_types.UaNodeAttributes = VARIABLE_ATTRIBUTES_DEFAULT, node_context = None):
        out_node_id = ffi.new("UA_NodeId *")
                
        # TODO: test
        if node_context is not None: 
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL
        
        status_code = lib.UA_Server_addObjectTypeNode(self.ua_server, requested_new_node_id._val, parent_node_id._val, reference_type_id._val, browse_name._val, type_definition._val, attr._val, node_context._ptr, out_node_id._ptr)
        return ServerServiceResults.AddNodeAttributeResult(ua_types.UaStatusCode(status_code), out_node)

    # TODO: test
    #def add_method_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, method, input_arg_size, input_args, output_arg_size, output_args, out_new_node_id, attr = VARIABLE_ATTRIBUTES_DEFAULT, node_context = None):
    #    out_node_id = ffi.new("UA_NodeId *")

        
    #    if node_context is not None: 
    #        node_context = ffi.new_handle(node_context)
    #    else:
    #        node_context = ffi.NULL

    #    status_code = lib.UA_Server_addMethodNode()
    #    return ServerServiceResults.AddMethodNodeResult(ua_types.UaStatusCode(status_code), output_arg_size, output_args, out_node)
        
    def set_node_type_lifecycle(self, node_id:ua_types.UaNodeId, lifecycle:ua_types.UaNodeTypeLifecycle): # TODO: lifecycle is of type UA_NodeTypeLifecycle
        raw_result = lib.UA_Server_addNodeTypeLifecycle(self.ua_server,node_id._val, lifecycle._val)
        return ua_types.StatusCode(val=raw_result)

    def trigger_event(self, node_id:ua_types.UaNodeId, origin_id:ua_types.UaNodeId, out_event_id:ua_type.UaByteString, delete_event_node:ua_types.UaBoolean):
        raw_result = lib.UA_Server_triggerEvent(self.ua_server, node_id._val, origin_id._val, out_event_id._ptr, delete_event_node._val)
        return ua_types.StatusCode(val=raw_result)

    def set_variable_node_value_callback(self, node_id:ua_types.UaNodeId, callback:ua_types.UaValueCallback): #TODO: callback is of type UA_ValueCallback
        raw_result = lib.UA_Server_setVariableNode_valueCallback(self.ua_server, node_id._val, callback._val)
        return ua_types.StatusCode(val=raw_result)

    def set_variable_node_value_backend(self, node_id:ua_types.UaNodeId, callback:ua_types.UaValueBackend): #TODO: callback is of type UA_ValueBackend
        raw_result = lib.UA_Server_setVariableNode_valuebackend(self.ua_server, node_id._val, callback._val)
        return ua_types.StatusCode(val=raw_result)

    def create_condition(self, condition_id:ua_types.UaNodeId, condition_type:ua_types.UaNodeId, condition_name:ua_types.UaQualifiedName, condition_source:ua_types.UaNodeId, hierarchical_reference_type:ua_types.UaNodeId):
        out_node_id = ffi.new("UA_NodeId *")

        status_code = lib.UA_Server_createCondition(self.ua_server, condition_id._val, condition_type._val, condition_name._val, condition_source._val, hierarchical_reference_type._val, out_node_id._ptr)
        return ServerServiceResults.AddNodeAttributeResult(ua_types.UaStatusCode(status_code), out_node_id)

    def set_condition_field(self, condition:ua_types.UaNodeId, value:ua_types.UaVariant, field_name:ua_types.UaQualifiedName):
        raw_result = lib.UA_Server_setConditionField(self.ua_server, condition._val, value._ptr, field_name._val)
        return ua_types.StatusCode(val=raw_result)

    def set_condition_variable_field_property(self, condition:ua_types.UaNodeId, value:ua_types.UaVariant, var_field_name:ua_types.UaQualifiedName, var_property_name:ua_types.UaQualifiedName):
        raw_result = lib.UA_Server_setConditionVariableFieldProperty(self.ua_server, condition._val, value._ptr, var_field_name._val, var_property_name._val)
        return ua_types.StatusCode(val=raw_result)

    def trigger_condition_event(self, condition:ua_types.UaNodeId, condition_source:ua_types.UaNodeId):
        out_event_id = ffi.new("UA_ByteString *")
        status_code = lib.UA_Server_triggerConditionEvent(self.ua_server, condition._val, condition_source._val, out_event_id._ptr)
        return ServerServiceResults.AddConditionEventResult(status_code, out_event_id)

    def set_condition_two_state_variable_callback(self, condition:ua_types.UaNodeId, condition_source:ua_types.UaNodeId, remove_branch:ua_types.UaBoolean, callback:ua_types:UaTwoStateVariableChangeCallback, callback_type:ua_types:UaTwoStateVariableCallbackType)
        raw_result = lib.UA_Server_setConditionTwoStateVariableCallback(self.ua_server, condition, condition_source, remove_branch, callback, callback_type)
        return ua_types.UaStatusCode(raw_result)