from ua import *


# Example: Hello World Method

def hello_world_method_callback(server: UaServer,
                                session_id: UaNodeId,
                                session_context: Void, method_id: UaNodeId, method_context: Void,
                                object_id: UaNodeId,
                                object_context: Void,
                                input_arg: UaList,
                                output_arg: UaList):
    str = UaString("Hello " + UaString(input_arg[
                                           0].data).value)  # todo: implement "magic method" for Ua_String concat. allow user to use Strings and implicitly map to UaStrings when needed
    UaVariant.set_scalar(output_arg[0], str, UA_TYPES.STRING)  # todo: can we call set_scalar implicitly to improve UX?
    # todo: would be nice if the user could just write the following: output_arg[0] = "Hello " + input_arg[0] and we do some "magic" to make it happen
    UaLogger().info(UaLogCategory.SERVER(), "Hello World was called")
    return UA_STATUSCODES.GOOD


def add_hello_world_method(server: UaServer):
    input_argument = UaArgument()  # todo: introduce builder pattern for UA types to allow for concise code? --> UaArgument().description(...).name(...)
    input_argument.description = UaLocalizedText("en-US", "A String")
    input_argument.name = UaString("MyInput")
    input_argument.data_type = UA_TYPES.STRING.type_id
    input_argument.value_rank = UaValueRanks.SCALAR

    output_argument = UaArgument()
    output_argument.description = UaLocalizedText("en-US", "A String")
    output_argument.name = UaString("MyOutput")
    output_argument.data_type = UA_TYPES.STRING.type_id
    output_argument.value_rank = UaValueRanks.SCALAR

    hello_attr = UA_ATTRIBUTES_DEFAULT.METHOD
    hello_attr.description = UaLocalizedText("en-US", "Say `Hello World`")
    hello_attr.display_name = UaLocalizedText("en-US", "Hello World")
    hello_attr.executable = UaBoolean(True)
    hello_attr.user_executable = UaBoolean(True)
    server.add_method_node(UaNodeId(1, 62541),
                           UA_NS0ID.OBJECTSFOLDER,
                           UA_NS0ID.HASCOMPONENT,
                           UaQualifiedName(1, "hello world"),
                           hello_world_method_callback,
                           input_argument,
                           output_argument, attr=hello_attr)


# Increase Array Values Method
def inc_int_32_array_method_callback(server: UaServer,
                                     session_id: UaNodeId,
                                     session_context: Void, method_id: UaNodeId, method_context: Void,
                                     object_id: UaNodeId,
                                     object_context: Void,
                                     input_arg: UaList,
                                     output_arg: UaList):
    delta = UaInt32(input_arg[1].data)
    size = SizeT(5)
    lst = UaList(input_arg[0].data, size, UaInt32)
    res_list = UaList(ua_class=UaInt32, size=5)
    for i in range(0, len(lst)):
        res_list[i] = UaInt32(lst[i].value + delta.value)
    output_arg[0].set_array(res_list, size, UA_TYPES.INT32)
    return UA_STATUSCODES.GOOD


def add_inc_int_32_array_method(server: UaServer):
    # two input arguments
    input_arguments = UaList(ua_class=UaArgument, size=2)
    input_arguments[0].description = UaLocalizedText("en-US", "int32[5] array")
    input_arguments[0].name = UaString("int32 array")
    input_arguments[0].data_type = UA_TYPES.INT32.type_id
    input_arguments[0].value_rank = UaValueRanks.ONE_DIMENSION
    input_arguments[0].array_dimensions_size = SizeT(1)
    input_arguments[0].array_dimensions = UaUInt32(5)

    input_arguments[1].description = UaLocalizedText("en-US", "int32 delta")
    input_arguments[1].name = UaString("int32 delta")
    input_arguments[1].data_type = UA_TYPES.INT32.type_id
    input_arguments[1].value_rank = UaValueRanks.SCALAR

    # one output argument
    output_argument = UaArgument()
    output_argument.description = UaLocalizedText("en-US", "int32[5] array")
    output_argument.name = UaString("each entry is incremented by the delta")
    output_argument.data_type = UA_TYPES.INT32.type_id
    output_argument.value_rank = UaValueRanks.ONE_DIMENSION
    p_output_dimensions = UaUInt32(5)
    output_argument.array_dimensions_size = SizeT(1)
    output_argument.array_dimensions = p_output_dimensions

    # add the method node
    inc_attr = UA_ATTRIBUTES_DEFAULT.METHOD
    inc_attr.description = UaLocalizedText("en-US", "IncInt32ArrayValues")
    inc_attr.display_name = UaLocalizedText("en-US", "IncInt32ArrayValues")
    inc_attr.executable = UaBoolean(True)  # todo: adapt setter to allow to pass python bool instead of UaBoolean
    inc_attr.user_executable = UaBoolean(True)
    server.add_method_node(UaNodeId(1, "IncInt32ArrayValues"),
                           UA_NS0ID.OBJECTSFOLDER,
                           UA_NS0ID.HASCOMPONENT,
                           UaQualifiedName(1, "IncInt32ArrayValues"),
                           inc_int_32_array_method_callback, input_arguments, output_argument, attr=inc_attr)


server = UaServer()
add_hello_world_method(server)
add_inc_int_32_array_method(server)
retval = server.run(UaBoolean(True))