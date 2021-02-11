from intermediateApi import lib, ffi


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

### recently added
    def read(self, item, timestamps):
        return lib.UA_Server_read(self.ua_server, item, timestamps)
    
    def writeDataValue(self, nodeId, value):
        return lib.UA_Server_writeDataValue(self.ua_server, nodeId, value)
    
    def writeDataType(self, nodeId, dataType):
        return lib.UA_Server_writeDataTyoe(self.ua_server, nodeId, dataType)

    ## useful?
    def writeValueRank(self, nodeId, valueRank):
        return lib.UA_Server_writeValueRank(self.ua_server, nodeId, valueRank)

    def writeArrayDimensions(self, nodeId, arrayDimensions):
        return lib.UA_Server_writeArrayDimensions(self.ua_server, nodeId, arrayDimensions)

    def writeAccessLevel(self, nodeId, accessLevel):
        return lib.UA_Server_writeAccessLevel(self.ua_server, nodeId, accessLevel)

    def writeMinimumSamplingInterval(self, nodeId, minimumSamplingInterval):
        return lib.UA_Server_writeMinimumSamplingInterval(self.ua_server, nodeId, minimumSamplingInterval)

    ## def writeHistorizing

    def writeExecutable(self, nodeId, executable):
        return UA_Server_writeExecutable(self.ua_server, nodeId, executable)

    # node management
    #def browse(self, maxReferences, bd):
    #    return UA_Server_browse(self.ua_server, maxReferences, bd)
    
    def browseNext(self, releaseContinuationPoint, continuationPoint):
        return lib.UA_server__browseNext(self.ua_server, releaseContinuationPoint, continuationPoint)

    ## pointer issues?
    def browseRecursive(self, bd, resultsSize, results):
        return lib.UA_Server_browseRecursive(self.ua_server, bd, resultsSize, results)

    def translateBrowsePathToNodeIds(self, browsePath):
        return lib.UA_Server_translateBrowsePathToNodeIds(self.ua_server, browsePath)

    def writeObjectProperty(self, objectId, propertyName, value):
        return lib.UA_Server_writeObjectProperty(self.ua_server, objectId, propertyName, value)

    def writeObjectProperty_scalar(self, objectId, propertyName, value, dataType):
        return lib.UA_Server_writeObjectProperty_scalar(self.ua_server, objectId, propertyName, value, dataType)

    def readObjectProperty(self, objectId, propertyName, value):
        return UA_Server_readObjectProperty(self.ua_server, objectId, propertyName, value)

    def call(self, request):
        return UA_Server_call(self.ua_server, request)

    def addDataSourceVariableNode(self, requestedNewNodeId, parentNodeId, referenceTypeId, browseName, typeDefinition, attr, dataSource, nodeContext, outNewNodeId):
        return A_Server_addDataSourceVariableNode(self.ua_server, requestedNewNodeId, parentNodeId, referenceTypeId, browseName, typeDefinition, attr, dataSource, nodeContext, outNewNodeId)

    def addMethodNodeEx(self, requestedNewNodeId, parentNodeId, referenceTypeId, browseName, attr, method, inputArgumentsSize, inputArguments,  inputArgumentsRequestedNewNodeId, inputArgumentsOutNewNodeId, outputArgumentsSize, outputAarguments,  outputArgumentsRequestedNewNodeId, outputArgumentsOutNewNodeId, nodeContext, outNewNodeId):
        return li.UA_Server_addMethodNodeEx(self.ua_server, requestedNewNodeId, parentNodeId, referenceTypeId, browseName, attr, method, inputArgumentsSize, inputArguments,  inputArgumentsRequestedNewNodeId, inputArgumentsOutNewNodeId, outputArgumentsSize, outputAarguments,  outputArgumentsRequestedNewNodeId, outputArgumentsOutNewNodeId, nodeContext, outNewNodeId)

    def addNode_finish(self, nodeId):
        return lib.UA_Server_addNode_finish(self.ua_server, nodeId)

    def addNode_begin(self, nodeClass,  requestedNewNodeId,  parentNodeId,  referenceTypeId, browseName, typeDefinition, attr, attributeType, nodeContext, outNewNodeId):
        return lib.UA_Server_addNode_begin(self.ua_server, nodeClass,  requestedNewNodeId,  parentNodeId,  referenceTypeId, browseName, typeDefinition, attr, attributeType, nodeContext, outNewNodeId)

    def addMethodNode_finish(self, nodeId, method, inputArgumentsSize, inputArguments, outputArgumentsSize, outputArguments):
        return lib.UA_Server_addMethodNode_finish(self.ua_server, nodeId, method, inputArgumentsSize, inputArguments, outputArgumentsSize, outputArguments)
    
    def deleteNode(self, nodeId, deleteReferences):
        return lib.UA_Server_deleteNode(self.ua_server, nodeId, deleteReferences)

    def addReference(self , sourceId, refTypeId, targetId, isForward):
        return lib .UA_Server_addReference(self.ua_server , sourceId, refTypeId, targetId, isForward)

    def deleteReference(self, sourceNodeId, referenceTypeId,  isForward, targetNodeId, deleteBidirectional):
        return lib.UA_Server_deleteReference(self.ua_server, sourceNodeId, referenceTypeId,  isForward, targetNodeId, deleteBidirectional)

    # node management
    #def findDataType(self, typeId):
    #    return lib.UA_Server_findDataType(self.ua_server, typeId)

    def addVariableNode(self, requestedNewNodeId, parentNodeId, referenceTypeId, browseName, typeDefinition, attr, nodeContext, outNewNodeId):
        return lib.UA_Server_addVariableNode(self.ua_server, requestedNewNodeId, parentNodeId, referenceTypeId, browseName, typeDefinition, attr, nodeContext, outNewNodeId)