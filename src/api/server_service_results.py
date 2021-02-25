class AddNodeAttributeResult:
    def __init__(self, status_code, out_node):
        self.status_code = status_code
        self.out_node = out_node

class AddMethodNodeResult:
    def __init__(self, output_arg_size, output_args, status_code):
        self.status_code = status_code
        self.output_args = output_args
        self.output_arg_size = output_arg_size
        