from ua import *


# Example: Hello World Method

def hello_world_method_callback(server, session_id, session_handle, method_id, method_context, object_id,
                                object_context, input_size, input, output_size, output):
    str = UaString("Hello " + UaString(input.data).value)
    UaVariant.set_scalar(output, str, TYPES.STRING)
    UaLogger().info(UaLogCategory.UA_LOGCATEGORY_SERVER, "Hello World was called")
    return UaStatusCode.UA_STATUSCODE_GOOD


def add_hello_world_method(server: UaServer):
    input_argument = UaArgument()
    input_argument.description = UaLocalizedText("en-US", "A String")
    input_argument.name = UaString("MyInput")
    input_argument.data_type = TYPES.STRING.type_id
    input_argument.value_rank = UaValueRanks.SCALAR

    output_argument = UaArgument()
    output_argument.description = UaLocalizedText("en-US", "A String")
    output_argument.name = UaString("MyInput")
    output_argument.data_type = TYPES.STRING.type_id
    output_argument.value_rank = UaValueRanks.SCALAR

    hello_attr = DefaultAttributes.METHOD_ATTRIBUTES_DEFAULT  # todo: put default attributes somewhere else
    hello_attr.description = UaLocalizedText("en-US", "Say `Hello World`")
    hello_attr.display_name = UaLocalizedText("en-US", "Hello World")
    hello_attr.executable = UaBoolean(True)
    hello_attr.user_executable = UaBoolean(True)
    # todo: introduce method in server
    server.add_method_node(server,
                           UaNodeId(1, 62541),
                           NS0ID.OBJECTSFOLDER,
                           NS0ID.HASCOMPONENT,
                           UaQualifiedName("hello world"),
                           hello_attr, hello_world_method_callback, 1, input_argument, 1, output_argument)


# Increase Array Values Method
def inc_int_32_array_method_callback(server, session_id, session_context, method_id, method_context, object_id,
                                     object_context, input_size, input, output_size, output):
    input_array = UaInt32(input.data[0])
    delta = UaInt32(input.data[1])
    # todo: set_scalar should return status code
    retval = output.set_array(input_array, 5, TYPES.INT32)
    if retval is not UaStatusCode.UA_STATUSCODE_GOOD:
        return retval
    output_array = UaUInt32(output.data)
    for i in range(0, input.array_length - 1):
        output_array[i] = input_array[i] + delta
    return UaStatusCode.UA_STATUSCODE_GOOD


def add_inc_int_32_array_method(server: UaServer):
    # two input arguments
    input_arguments = UaArgument(2)
    input_arguments[0].description = UaLocalizedText("en-US", "int32[5] array")
    input_arguments[0].name = UaString("int32 array")
    input_arguments[0].data_type = TYPES.INT32.type_id
    input_arguments[0].value_rank = UaValueRanks.ONE_DIMENSION
    p_input_dimention = 5
    input_arguments[0].array_dimentsions_size = 1
    input_arguments[0].array_dimentsions = p_input_dimention

    input_arguments[1].description = UaLocalizedText("en-US", "int32 delta")
    input_arguments[1].name = UaString("int32 delta")
    input_arguments[1].data_type = TYPES.INT32.type_id
    input_arguments[1].value_rank = UaValueRanks.SCALAR

    # one output argument
    output_argument = UaArgument()
    output_argument.description = UaLocalizedText("en-US", "int32[5] array")
    output_argument.name = UaString("each entry is incremented by the delta")
    output_argument.data_type = TYPES.INT32.type_id
    output_argument.value_rank = UaValueRanks.ONE_DIMENSION
    p_output_dimensions = 5
    output_argument.array_dimensions_size = 1
    output_argument.array_dimensions = p_output_dimensions

    # add the method node
    inc_attr = DefaultAttributes.METHOD_ATTRIBUTES_DEFAULT  # todo: move attributes to their own class
    inc_attr.description = UaLocalizedText("en-US", "IncInt32ArrayValues")
    inc_attr.display_name = UaLocalizedText("en-US", "IncInt32ArrayValues")
    inc_attr.executable = UaBoolean(True)
    inc_attr.user_executable = UaBoolean(True)
    server.add_method_node(server,  # todo: add service to server
                           UaNodeId(1, "IncInt32ArrayValues"),
                           NS0ID.OBJECTSFOLDER,
                           NS0ID.HASCOMPONENT,
                           UaQualifiedName(1, "IncInt32ArrayValues"),
                           inc_attr, inc_int_32_array_method_callback,
                           2, input_arguments, 1, output_argument)


def main():
    server = UaServer()
    add_hello_world_method(server)
    add_inc_int_32_array_method(server)
    retval = server.run(UaBoolean(True))
