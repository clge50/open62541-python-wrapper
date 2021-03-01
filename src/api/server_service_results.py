import ua_types

class AddNodeAttributeResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_node:ua_types.UaNodeId):
        self.status_code = status_code
        self.out_node = out_node

class AddMethodNodeResult:
    def __init__(self, output_arg_size, output_args, status_code:ua_types.UaStatusCode):
        self.status_code = status_code
        self.output_args = output_args
        self.output_arg_size = output_arg_size

class AddConditionEventResult:
    def __init__(self, status_code:ua_types.UaStatusCode, out_event:ua_types.UaByteString)
        self.status_code = status_code
        self.out_event = out_event