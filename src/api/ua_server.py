# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import time
import threading
from intermediateApi import lib, ffi
import ua_service_results_server as ServerServiceResults
from ua_types import *
from ua_types_list import *
from ua_consts_default_attributes import UA_ATTRIBUTES_DEFAULT
import typing


class _ServerCallback:
    """
    This class holds c type callback implementations which are being used to call the actual callback functions which
    have been submitted by the open62541 user. This is a workaround for the problem of not being able to create c
    function implementations at runtime.

    Warning:
        The current handling of server based callback function introduces a multitude of problems. In the longterm
        it should probably be reimplemented. The issue is the following: In terms of creating function pointers CFFI
        offers multiple approached (see https://cffi.readthedocs.io/en/latest/using.html#extern-python-new-style-callbacks).
        The recommended way is outlined in "Extern 'Python' and void* arguments. The basic concept is to add
        a function definition with the desired parameters and return type for the callback to ffi.cdef() and mark it as
        `extern "Python"`. This definition can then be implemented in python by defining a function which uses the same
        name and annotating it with `@ffi.def_extern()`. The problem is that per function that has been defined via
        `ffi.cdef(...)` only one implementation can be created via python. Any attempt to create a second implementation
        using the same name and annotating it with `@ffi.def_extern()` will lead to the prior implementation being
        overwritten.

        In theory it could be possible to solve the issue by using "Callbacks (old style)" (
        https://cffi.readthedocs.io/en/latest/using.html#callbacks-old-style) but CFFI strongly advises against using
        this as it introduces numerous security issues and can lead to the program crashing, especially when forking.

        In the initial implementation we have utilized the recommended "Extern 'Python' (new-style callbacks)" (can
        be found in the "definitions" files, e.g. "nodestore" and created a single static callback implementation for
        each required open62541 c callback type. The sole purpose of these static functions is to call the actual
        dynamic python callback function which has been passed by the API user and to wrap all function parameters to
        ensure usability. As the functions are static and most of them do not have any parameters that can be used to
        "smuggle in" python function pointers, the current workaround for server callbacks involves storing the
        python callbacks that shall be called in a global dictionary and retrieving them via a unique key (often
        bound to node_ids). There is currently no implicit memory management for it and the API user has to clean it
        up manually if needed. Furthermore, at the time of the implementation there was a lack of resources to test a
        lot of different flows of registering callback methods. It can therefore very well be the cases that there
        are flows in which the registration in the map or the retrieval does not work properly which will lead to
        exceptions. Also, the callback data is not stored within the corresponding nodes, e.g. the method node and
        therefore cannot be persisted even if the node structure is preserved and would be needed to be persisted
        separatly.

        It could very well be the case that CFFI will offer a solution to the general problem in the future (
        >v1.14.5) or that there is a better way of handling the issue with what is there already.

    Example:
        Let's illustrate how the server callback workaround works by using an example (method node): When
        calling `add_method_node` the passed python callback is stored in `_ServerCallback.callbacks_dict` (ua_server
        module). meanwhile we pass only `lib.python_wrapper_UA_MethodCallback`.

    .. code-block:: python
       :emphasize-lines: 29,33

        def add_method_node(self, requested_new_node_id: UaNodeId, parent_node_id: UaNodeId, reference_type_id: UaNodeId,
                    browse_name: UaQualifiedName,
                    method: Callable[
                        ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNodeId, Void, UaList,
                            UaList], UaStatusCode], input_arg: Union[UaArgument, UaList],
                    output_arg: Union[UaArgument, UaList], attr: UaVariableAttributes = None,
                    node_context=None):
            if attr is None:
                attr = UA_ATTRIBUTES_DEFAULT.VARIABLE

            out_new_node_id = UaNodeId()

            if node_context is not None:
                node_context = ffi.new_handle(node_context)
            else:
                node_context = ffi.NULL

            if isinstance(input_arg, UaList):
                input_length = SizeT(len(input_arg))
            else:
                input_length = SizeT(1)

            if isinstance(output_arg, UaList):
                output_length = SizeT(len(output_arg))
            else:
                output_length = SizeT(1)

            # add python callback in dict using the requested_new_node_id as the key
            _ServerCallback.callbacks_dict[str(requested_new_node_id)] = method

            status_code = lib.UA_Server_addMethodNode(self.ua_server, requested_new_node_id._val, parent_node_id._val,
                                                      reference_type_id._val, browse_name._val, attr._val,
                                                      lib.python_wrapper_UA_MethodCallback,
                                                      input_length._val, input_arg._ptr, output_length._val,
                                                      output_arg._ptr, node_context, out_new_node_id._ptr)
            return ServerServiceResults.AddMethodNodeResult(output_length, output_arg, UaStatusCode(status_code),
                                                            out_new_node_id)


    When it is time for triggering the callback, open62541 will call the static
    `lib.python_wrapper_UA_MethodCallback` which has been defined in the definitions file "nodestore".

    .. code-block::

        typedef UA_StatusCode (*UA_MethodCallback)(UA_Server *server, const UA_NodeId *sessionId,
                     void *sessionContext, const UA_NodeId *methodId,
                     void *methodContext, const UA_NodeId *objectId,
                     void *objectContext, size_t inputSize,
                     const UA_Variant *input, size_t outputSize,
                     UA_Variant *output);

        extern "Python" UA_StatusCode python_wrapper_UA_MethodCallback(UA_Server *server, const UA_NodeId *sessionId,
                     void *sessionContext, const UA_NodeId *methodId,
                     void *methodContext, const UA_NodeId *objectId,
                     void *objectContext, size_t inputSize,
                     const UA_Variant *input, size_t outputSize,
                     UA_Variant *output);

    The function is implemented in python by `python_wrapper_UA_MethodCallback` in _ServerCallback. It's only purpose
    is to perform a lookup in `_ServerCallback.callbacks_dict` to find the python callback and then call it while
    wrapping all c/open62541 cffi parameters.

    .. code-block:: python

        @staticmethod
        @ffi.def_extern()
        def python_wrapper_UA_MethodCallback(server, session_id, session_context, method_id, method_context, object_id,
                                    object_context, input_size, _input, output_size, output):
        # lookup python callback function
        callbacks_dict_key = str(UaNodeId(val=method_id))

        # call python callback function and wrap all c/open62541 cffi parameters
        return _ServerCallback.callbacks_dict[callbacks_dict_key](UaServer(val=server),
                                                    UaNodeId(val=session_id, is_pointer=True),
                                                    Void(val=session_context, is_pointer=True),
                                                    UaNodeId(val=method_id, is_pointer=True),
                                                    Void(val=method_context, is_pointer=True),
                                                    UaNodeId(val=object_id, is_pointer=True),
                                                    Void(val=object_context, is_pointer=True),
                                                    UaList(val=_input, size=input_size,
                                                            ua_class=UaVariant),
                                                    UaList(val=output, size=output_size,
                                                            ua_class=UaVariant))._val
    """

    callbacks_dict: typing.Dict[str, any] = dict()
    """
    This dictionary is used to register and lookup callback functions. 
    """

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
                                                                                UaDataValue(val=value,
                                                                                            is_pointer=True))._val

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
                                                                                             is_pointer=True))._val

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

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_MethodCallback(server, session_id, session_context, method_id, method_context, object_id,
                                         object_context, input_size, _input, output_size, output):
        callbacks_dict_key = str(UaNodeId(val=method_id))

        return _ServerCallback.callbacks_dict[callbacks_dict_key](UaServer(val=server),
                                                                  UaNodeId(val=session_id, is_pointer=True),
                                                                  Void(val=session_context, is_pointer=True),
                                                                  UaNodeId(val=method_id, is_pointer=True),
                                                                  Void(val=method_context, is_pointer=True),
                                                                  UaNodeId(val=object_id, is_pointer=True),
                                                                  Void(val=object_context, is_pointer=True),
                                                                  UaList(val=_input, size=input_size,
                                                                         ua_class=UaVariant),
                                                                  UaList(val=output, size=output_size,
                                                                         ua_class=UaVariant))._val

    @staticmethod
    @ffi.def_extern()
    def python_wrapper_UA_Server_DataChangeNotificationCallback(server,
                                                                monitored_item_id,
                                                                monitored_item_context,
                                                                node_id,
                                                                node_context,
                                                                attribute_id,
                                                                value):
        callbacks_dict_key = str(UaNodeId(val=node_id)) + str(UaUInt32(attribute_id))
        _ServerCallback.callbacks_dict[callbacks_dict_key](UaServer(val=server),
                                                           UaUInt32(val=monitored_item_id),
                                                           Void(val=monitored_item_context, is_pointer=True),
                                                           UaNodeId(val=node_id, is_pointer=True),
                                                           Void(val=node_context, is_pointer=True),
                                                           UaUInt32(val=attribute_id),
                                                           UaDataValue(val=value, is_pointer=True))

    # todo: ExternalValueCallback is missing

    # @staticmethod
    # @ffi.def_extern()
    # def python_wrapper_UA_NodeTypeLifecycle_constructor(server,
    #                                                     session_id,
    #                                                     session_context,
    #                                                     type_node_id,
    #                                                     type_node_context,
    #                                                     node_id,
    #                                                     node_context):
    #     return UaStatusCode(val=UaNodeTypeLifecycle._constructor_callback(UaServer(val=server),
    #                                                                       UaNodeId(val=session_id),
    #                                                                       Void(val=session_context),
    #                                                                       UaNodeId(val=type_node_id),
    #                                                                       Void(val=type_node_context),
    #                                                                       UaNodeId(val=node_id),
    #                                                                       Void(val=node_context)))
    #
    # @staticmethod
    # @ffi.def_extern()
    # def python_wrapper_UA_NodeTypeLifecycle_destructor(server,
    #                                                    session_id,
    #                                                    session_context,
    #                                                    type_node_id,
    #                                                    type_node_context,
    #                                                    node_id,
    #                                                    node_context):
    #     UaNodeTypeLifecycle._destructor_callback(UaServer(val=server),
    #                                              UaNodeId(val=session_id),
    #                                              Void(val=session_context),
    #                                              UaNodeId(val=type_node_id),
    #                                              Void(val=type_node_context),
    #                                              UaNodeId(val=node_id),
    #                                              Void(val=node_context))


class UaServer:
    """
    This class is used to create and manage servers as well as invoking services
    """

    def __init__(self, config=None, val=None):
        self._running = UaBoolean(False)
        if val is not None:
            self.ua_server = val
        elif config is None:
            self.ua_server = lib.UA_Server_new()
            self.set_default_config()
        else:
            self.ua_server = lib.UA_Server_newWithConfig(config._ptr)

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, running: Union[bool, UaBoolean]):
        if isinstance(running, UaBoolean):
            running = running.value
        self._running._value[0] = running

    # def __set_server_shutdown(self):
    #     if self.ua_server.endTime != 0:
    #         return False
    #     if self.ua_server.config.shutdownDelay == 0:
    #         return True
    #     lib.UA_LOG_WARNING(self.ua_server.config.logger, lib.UA_LOGCATEGORY_SERVER,
    #                        "Shutting down the server with a delay of %i ms",
    #                        self.ua_server.config.shutdownDelay)
    #     self.ua_server.endTime = (lib.UA_DateTime_now() +
    #                               (self.ua_server.config.shutdownDelay * lib.UA_DATETIME_MSEC))
    #     return False
    #
    # def __test_shut_down_condition(self):
    #     if self.ua_server.endTime == 0:
    #         return False
    #     return lib.UA_DateTime_now() > self.ua_server.endTime

    def run(self):
        self.running = True
        ret_val = lib.UA_Server_run(self.ua_server, self.running._value)
        return UaStatusCode(val=ret_val)
        # ret_val = lib.UA_Server_run_startup(self.ua_server)
        # if ret_val != UA_STATUSCODES.GOOD._val:
        #     return UaStatusCode(val=ret_val)
        #
        # while not self.__test_shut_down_condition():
        #     lib.UA_Server_run_iterate(self.ua_server, True)
        #     if not self._running.value:
        #         if self.__set_server_shutdown():
        #             break
        #
        # ret_val = lib.UA_Server_run_shutdown(self.ua_server)
        # return UaStatusCode(val=ret_val)

    def run_async(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        time.sleep(0.50)

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

    def write(self, value: UaWriteValue):
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
        return ServerServiceResults.NodeIdResult(UaStatusCode(val=status_code), out_node_id)

    def read_node_class(self, node_id: UaNodeId):
        out_node_class = UaNodeClass()
        status_code = lib.UA_Server_readNodeClass(self.ua_server, node_id._val, out_node_class._ptr)
        return ServerServiceResults.NodeClassResult(UaStatusCode(val=status_code), out_node_class)

    def read_browse_name(self, node_id: UaNodeId):
        out_browse_name = UaQualifiedName()
        status_code = lib.UA_Server_readBrowseName(self.ua_server, node_id._val, out_browse_name._ptr)
        out_browse_name._update()
        return ServerServiceResults.BrowseNameResult(UaStatusCode(val=status_code), out_browse_name)

    def read_display_name(self, node_id: UaNodeId):
        out_display_name = UaLocalizedText()
        status_code = lib.UA_Server_readDisplayName(self.ua_server, node_id._val, out_display_name._ptr)
        out_display_name._update()
        return ServerServiceResults.LocalizedTextResult(UaStatusCode(val=status_code), out_display_name)

    def read_description(self, node_id: UaNodeId):
        out_description = UaLocalizedText()
        status_code = lib.UA_Server_readDescription(self.ua_server, node_id._val, out_description._ptr)
        out_description._update()
        return ServerServiceResults.LocalizedTextResult(UaStatusCode(val=status_code), out_description)

    def read_write_mask(self, node_id: UaNodeId):
        out_write_mask = UaUInt32()
        status_code = lib.UA_Server_readWriteMask(self.ua_server, node_id._val, out_write_mask._ptr)
        return ServerServiceResults.UInt32Result(UaStatusCode(val=status_code), out_write_mask)

    def read_is_abstract(self, node_id: UaNodeId):
        out_is_abstract = UaBoolean()
        status_code = lib.UA_Server_readIsAbstract(self.ua_server, node_id._val, out_is_abstract._ptr)
        return ServerServiceResults.BooleanResult(UaStatusCode(val=status_code), out_is_abstract)

    def read_symmetric(self, node_id: UaNodeId):
        out_symmetric = UaBoolean()
        status_code = lib.UA_Server_readSymmetric(self.ua_server, node_id._val, out_symmetric._ptr)
        return ServerServiceResults.BooleanResult(UaStatusCode(val=status_code), out_symmetric)

    def read_inverse_name(self, node_id: UaNodeId):
        out_name = UaLocalizedText()
        status_code = lib.UA_Server_readInverseName(self.ua_server, node_id._val, out_name._ptr)
        out_name._update()
        return ServerServiceResults.LocalizedTextResult(UaStatusCode(val=status_code), out_name)

    def read_contains_no_loops(self, node_id: UaNodeId):
        out_no_loops = UaBoolean()
        status_code = lib.UA_Server_readContainsNoLoops(self.ua_server, node_id._val, out_no_loops._ptr)
        return ServerServiceResults.BooleanResult(UaStatusCode(val=status_code), out_no_loops)

    def read_event_notifier(self, node_id: UaNodeId):
        out_event_notifier = UaByte()
        status_code = lib.UA_Server_readEventNotifier(self.ua_server, node_id._val, out_event_notifier._ptr)
        return ServerServiceResults.ByteResult(UaStatusCode(val=status_code), out_event_notifier)

    def read_value(self, node_id: UaNodeId):
        out_value = UaVariant()
        status_code = lib.UA_Server_readValue(self.ua_server, node_id._val, out_value._ptr)
        out_value._update()
        return ServerServiceResults.VariantResult(UaStatusCode(val=status_code), out_value)

    def read_data_type(self, node_id: UaNodeId):
        out_type = UaNodeId()
        status_code = lib.UA_Server_readDataType(self.ua_server, node_id._val, out_type._ptr)
        out_type._update()
        return ServerServiceResults.NodeIdResult(UaStatusCode(val=status_code), out_type)

    def read_value_rank(self, node_id: UaNodeId):
        out_rank = UaUInt32()
        status_code = lib.UA_Server_readValueRank(self.ua_server, node_id._val, out_rank._ptr)
        return ServerServiceResults.UInt32Result(UaStatusCode(val=status_code), out_rank)

    def read_array_dimensions(self, node_id: UaNodeId):
        out_dim = UaVariant()
        status_code = lib.UA_Server_readArrayDimensions(self.ua_server, node_id._val, out_dim._ptr)
        out_dim._update()
        return ServerServiceResults.VariantResult(UaStatusCode(val=status_code), out_dim)

    def read_access_level(self, node_id: UaNodeId):
        out_level = UaByte()
        status_code = lib.UA_Server_readAccessLevel(self.ua_server, node_id._val, out_level._ptr)
        return ServerServiceResults.ByteResult(UaStatusCode(val=status_code), out_level)

    def read_minimum_sampling_interval(self, node_id: UaNodeId):
        out_interval = UaDouble()
        status_code = lib.UA_Server_readMinimumSamplingInterval(self.ua_server, node_id._val, out_interval._ptr)
        return ServerServiceResults.DoubleResult(UaStatusCode(val=status_code), out_interval)

    def read_executable(self, node_id: UaNodeId):
        out_exe = UaBoolean()
        status_code = lib.UA_Server_readExecutable(self.ua_server, node_id._val, out_exe._ptr)
        return ServerServiceResults.BooleanResult(UaStatusCode(val=status_code), out_exe)

    ###
    ### Browse Functions
    ###

    def browse(self, max_refs: UaUInt32):  # TODO: implement UaBrowseDescription
        out_bd = UaBrowseDescription()
        status_code = lib.UA_Server_browse(self.ua_server, max_refs._val, out_bd._ptr)
        out_bd._update()
        return ServerServiceResults.BrowseResultResult(UaStatusCode(val=status_code), out_bd)

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
            attr = UA_ATTRIBUTES_DEFAULT.VARIABLE

        if node_context is not None:
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        # todo: requested_new_node_id currently mustn't be NULL or this doesn't work

        # only has to be added to dict if python callbacks are used instead of only c callbacks
        if data_source.uses_python_read_callback or data_source.uses_python_write_callback:
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
                      target_id: UaExpandedNodeId,
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
            attr = UA_ATTRIBUTES_DEFAULT.VARIABLE

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
            attr = UA_ATTRIBUTES_DEFAULT.VARIABLE

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
                        attr: UaObjectAttributes = None,
                        node_context=None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.VARIABLE

        out_node_id = UaNodeId()

        # TODO: test
        if node_context is not None:
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        status_code = lib.UA_Server_addObjectNode(self.ua_server, requested_new_node_id._val, parent_node_id._val,
                                                  reference_type_id._val, browse_name._val, type_definition._val,
                                                  attr._val, node_context, out_node_id._ptr)
        out_node_id._update()
        return ServerServiceResults.NodeIdResult(UaStatusCode(status_code), out_node_id)

    def add_object_type_node(self,
                             requested_new_node_id: UaNodeId,
                             parent_node_id: UaNodeId,
                             reference_type_id: UaNodeId,
                             browse_name: UaQualifiedName,
                             attr: UaObjectTypeAttributes = None,
                             node_context=None):

        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.VARIABLE

        out_node_id = UaNodeId()

        # TODO: test
        if node_context is not None:
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        status_code = lib.UA_Server_addObjectTypeNode(self.ua_server, requested_new_node_id._val, parent_node_id._val,
                                                      reference_type_id._val, browse_name._val,
                                                      attr._val, node_context, out_node_id._ptr)

        out_node_id._update()
        return ServerServiceResults.NodeIdResult(UaStatusCode(status_code), out_node_id)

    def add_method_node(self, requested_new_node_id: UaNodeId, parent_node_id: UaNodeId, reference_type_id: UaNodeId,
                        browse_name: UaQualifiedName,
                        method: Callable[
                            ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNodeId, Void, UaList,
                             UaList], UaStatusCode], input_arg: Union[UaArgument, UaList],
                        output_arg: Union[UaArgument, UaList], attr: UaVariableAttributes = None,
                        node_context=None):
        if attr is None:
            attr = UA_ATTRIBUTES_DEFAULT.VARIABLE

        out_new_node_id = UaNodeId()

        if node_context is not None:
            node_context = ffi.new_handle(node_context)
        else:
            node_context = ffi.NULL

        if isinstance(input_arg, UaList):
            input_length = SizeT(len(input_arg))
        else:
            input_length = SizeT(1)

        if isinstance(output_arg, UaList):
            output_length = SizeT(len(output_arg))
        else:
            output_length = SizeT(1)

        _ServerCallback.callbacks_dict[str(requested_new_node_id)] = method

        status_code = lib.UA_Server_addMethodNode(self.ua_server, requested_new_node_id._val, parent_node_id._val,
                                                  reference_type_id._val, browse_name._val, attr._val,
                                                  lib.python_wrapper_UA_MethodCallback,
                                                  input_length._val, input_arg._ptr, output_length._val,
                                                  output_arg._ptr, node_context, out_new_node_id._ptr)
        return ServerServiceResults.AddMethodNodeResult(output_length, output_arg, UaStatusCode(status_code),
                                                        out_new_node_id)

    def trigger_event(self, node_id: UaNodeId, origin_id: UaNodeId,
                      out_event_id: UaByteString, delete_event_node: UaBoolean):
        raw_result = lib.UA_Server_triggerEvent(self.ua_server, node_id._val, origin_id._val, out_event_id._ptr,
                                                delete_event_node._val)
        out_event_id._update()
        return UaStatusCode(val=raw_result)

    def set_variable_node_value_callback(self, node_id: UaNodeId,
                                         callback: UaValueCallback):

        if callback.uses_python_read_callback or callback.uses_python_write_callback:
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

        out_node_id = UaNodeId()

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

    def create_data_change_monitored_item(self,
                                          timestamps_to_return: UaTimestampsToReturn,
                                          item: UaMonitoredItemCreateRequest,
                                          monitored_item_context: Void,
                                          callback: Callable[['UaServer',
                                                              UaUInt32,
                                                              Void,
                                                              UaNodeId,
                                                              Void,
                                                              UaUInt32,
                                                              UaDataValue],
                                                             None]):

        _ServerCallback.callbacks_dict[str(item.item_to_monitor.node_id) +
                                       str(item.item_to_monitor.attribute_id)] = callback

        return UaMonitoredItemCreateResult(
            val=lib.UA_Server_createDataChangeMonitoredItem(
                self.ua_server,
                timestamps_to_return._val,
                item._val,
                monitored_item_context._ptr,
                lib.python_wrapper_UA_Server_DataChangeNotificationCallback))

    def set_node_type_lifecycle(self, node_id: UaNodeId, lifecycle: UaNodeTypeLifecycle):
        return UaStatusCode(val=lib.UA_Server_setNodeTypeLifecycle(self.ua_server, node_id._val, lifecycle._val))
