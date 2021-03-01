import ua_types

class NodeIdResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_node:ua_types.UaNodeId):
        self.status_code = status_code
        self.out_node = out_node

class AddMethodNodeResult:
    def __init__(self, output_arg_size, output_args, status_code:ua_types.UaStatusCode):
        self.status_code = status_code
        self.output_args = output_args
        self.output_arg_size = output_arg_size

class EventResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_event:ua_types.UaByteString):
        self.status_code = status_code
        self.out_event = out_event

class NodeClassResult:
    def __init__(self, status_code:ua_types.UaStatusCode, node_class:ua_types.UaNodeClass):
        self.status_code = status_code
        self.node_class = node_class

class BrowseNameResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_name:ua_types.UaQualifiedName):
        self.status_code = status_code
        self.out_name = out_name

class LocalizedTextResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_name:ua_types.UaLocalizedText):
        self.status_code = status_code
        self.out_name = out_name

class UInt32Result:
    def __init__(self, status_code:ua_types.UaStatusCode, out_number:ua_types.UaUInt32):
        self.status_code = status_code
        self.out_number = out_number

class BooleanResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_bool:ua_types.UaBoolean):
        self.status_code = status_code
        self.out_bool = out_bool

class ByteResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_byte:ua_types.UaByte):
        self.status_code = status_code
        self.out_byte = out_byte

class VariantResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_variant:ua_types.UaVariant):
        self.status_code = status_code
        self.out_variant = out_variant

class DoubleResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_double:ua_types.UaDouble):
        self.status_code = status_code
        self.out_double = out_double

class BrowseResultResult:
    def __init__(self, status_code):ua_types.UaStatusCode, out_browse_result:ua_types:UaBrowseResult):
        self.status_code = status_code
        self.out_browse_result = out_browse_result
