from intermediateApi import lib, ffi
import server_service_results as ServerServiceResults


class UaServer:
    def __init__(self, config=None):
        if config is None:
            self.ua_server = lib.UA_Server_new()
            self.set_default_config()
        else:
            self.ua_server = lib.UA_Server_newWithConfig(config)

    def run( self, running):
        return lib.UA_Server_run( self.ua_server, running)

    def run_shutdown(self):
        return lib.UA_Server_run_shutdown(self.ua_server)

    def getConfig(self):
        return lib.UA_Server_getConfig(self.ua_server)

    def run_startup(self):
        return lib.UA_Server_run_startup(self.ua_server)

    def run_iterate(self, wait_internal):
        return lib.UA_Server_run_iterate(self.ua_server, wait_internal)

    #    def delete(self):
    #        return lib.UA_Server_delete(self.ua_server)

    def set_minimal_config(self, port_number, certificate):
        return lib.UA_ServerConfig_setMinimal(self.getConfig(), port_number, certificate)

    def set_default_config(self):
        return lib.UA_ServerConfig_setDefault(self.getConfig())


#########
###
### new
###


    def read(self, item, timestamps):
        return lib.UA_Server_read(self.ua_server, item, timestamps)

    def write(self, value):
        return lib.UA_Server_write(self.ua_server, value)

    def write_value(self, node_id, value):
        return lib.UA_Server_writeValue(self.ua_server, node_id, value)
    
    def write_data_value(self, node_id, value):
        return lib.UA_Server_writeDataValue(self.ua_server, node_id, value)
    
    def write_data_type(self, node_id, data_type):
        return lib.UA_Server_writeDataType(self.ua_server, node_id, data_type)

    def write_value_rank(self, node_id, value_rank):
        return lib.UA_Server_writeValueRank(self.ua_server, node_id, value_rank)

    def write_array_dimensions(self, node_id, array_dimensions):
        return lib.UA_Server_writeArrayDimensions(self.ua_server, node_id, array_dimensions)

    def write_access_level(self, node_id, access_level):
        return lib.UA_Server_writeAccessLevel(self.ua_server, node_id, access_level)

    def write_minimum_sampling_interval(self, node_id, minimum_sampling_interval):
        return lib.UA_Server_writeMinimumSamplingInterval(self.ua_server, node_id, minimum_sampling_interval)

    def write_executable(self, node_id, executable):
        return lib.UA_Server_writeExecutable(self.ua_server, node_id, executable)
 
    def browse_next(self, release_continuation_point, continuation_point):
        return lib.UA_Server_browseNext(self.ua_server, release_continuation_point, continuation_point)

    def translate_browse_path_to_node_ids(self, browse_path):
        return lib.UA_Server_translateBrowsePathToNodeIds(self.ua_server, browse_path)

    def write_object_property(self, object_id, property_name, value):
        return lib.UA_Server_writeObjectProperty(self.ua_server, object_id, property_name, value)

    def write_object_property_scalar(self, object_id, property_name, value, data_type):
        return lib.UA_Server_writeObjectProperty_scalar(self.ua_server, object_id, property_name, value, data_type)

    def read_object_property(self, object_id, property_name, value):
        return lib.UA_Server_readObjectProperty(self.ua_server, object_id, property_name, value)

    def call(self, request):
        return lib.UA_Server_call(self.ua_server, request)

    def add_data_source_variable_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition, attr, data_source, outNewnode_id, node_context = None):
        out_node = ffi.new("UA_node_id *")

        # TODO: test
        if node_context != None: 
           node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        status_code = lib.UA_Server_addDataSourceVariableNode(self.ua_server, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition, attr, data_source, node_context, outnode)
        return ServerServiceResults.AddNodeAttributeResult(status_code, node_context)

    def delete_node(self, node_id, delete_references):
        return lib.UA_Server_deleteNode(self.ua_server, node_id, delete_references)

    def add_reference(self , source_id, ref_type_id, target_id, is_forward):
        return lib.UA_Server_addReference(self.ua_server , source_id, ref_type_id, target_id, is_forward)

    def delete_reference(self, source_node_id, reference_type_id,  is_forward, target_node_id, delete_bidirectional):
        return lib.UA_Server_deleteReference(self.ua_server, sourcenode_id, reference_type_id,  isForward, targetnode_id, deleteBidirectional)   

    def add_variable_node(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition, attr, out_new_node_id, node_context = None):
        out_node_id = ffi.new("UA_NodeId *")
                
        # TODO: test
        if node_context != None: 
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL
        
        status_code = lib.UA_Server_addVariableNode(self.ua_server, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition, attr, node_context, out_node_id)
        return ServerServiceResults.AddNodeAttributeResult(status_code, node_context)


    #######
    #
    # node management functions
    #
    #def browse(self, maxReferences, bd):
    #    return lib.UA_Server_browse(self.ua_server, maxReferences, bd)

    #def browseRecursive(self, bd, resultsSize, results):
    #   return lib.UA_Server_browseRecursive(self.ua_server, bd, resultsSize, results)

    #def finddata_type(self, typeId):
    #    return lib.UA_Server_finddata_type(self.ua_server, typeId)

    #def addMethodNodeEx(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, attr, method, input_arguments_size, input_arguments,  input_arguments_requested_newnode_id, input_arguments_out_newnode_id, output_arguments_size, output_arguments,  output_arguments_requested_newnode_id, output_arguments_out_new_node_id, node_context, outNewnode_id):
    #    return lib.UA_Server_addMethodNodeEx(self.ua_server, requestedNewnode_id, parentnode_id, reference_type_id, browse_name, attr, method, inputArgumentsSize, inputArguments,  inputArgumentsRequestedNewnode_id, inputArgumentsOutNewnode_id, outputArgumentsSize, outputAarguments,  outputArgumentsRequestedNewnode_id, outputArgumentsOutNewnode_id, node_context, outNewnode_id)

    #def addNode_finish(self, node_id):
    #    return lib.UA_Server_addNode_finish(self.ua_server, node_id)

    #def addNode_begin(self, nodeClass,  requestedNewnode_id,  parentnode_id,  reference_type_id, browse_name, type_definition, attr, attributeType, node_context, outNewnode_id):
    #     outnode = ffi.new("UA_node_id *")
    #    return lib.UA_Server_addNode_begin(self.ua_server, nodeClass,  requestedNewnode_id,  parentnode_id,  reference_type_id, browse_name, type_definition, attr, attributeType, node_context, outnode)

    #def addMethodNode_finish(self, node_id, method, inputArgumentsSize, inputArguments, outputArgumentsSize, outputArguments):
    #    return lib.UA_Server_addMethodNode_finish(self.ua_server, node_id, method, inputArgumentsSize, inputArguments, outputArgumentsSize, outputArguments)
    

    #######
    #
    # skipping historizing for now...
    #

    # def writeHistorizing
