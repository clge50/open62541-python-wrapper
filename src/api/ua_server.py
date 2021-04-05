# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import time
import threading
from intermediateApi import lib, ffi
from typing import Tuple

import ua_service_results_server as ServerServiceResults
from ua_types_clientconfig import *
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

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_CertificateVerification_verifyCertificate(verification_context, certificate):
        UaCertificateVerification._verify_certificate(Void(val=verification_context, is_pointer=True),
                                                      UaByteString(val=certificate, is_pointer=True))
    
    
    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_SecurityPolicy_verifyApplicationURI(verification_context, certificate, application_uri):
        UaCertificateVerification._verify_application_uri(Void(val=verification_context, is_pointer=True),
                                                          UaByteString(val=certificate, is_pointer=True),
                                                          UaString(val=application_uri))
    
    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_CertificateVerification_clear(vc):
        UaCertificateVerification._clear(UaCertificateVerification(val=vc, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_clear(ns_ctx):
        UaNodestore._clear(Void(val=ns_ctx, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_newNode(ns_ctx, node_class):
        UaNodestore._new_node(Void(val=ns_ctx, is_pointer=True),
                              UaNodeClass(val=node_class))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_deleteNode(ns_ctx, node):
        UaNodestore._delete_node(Void(val=ns_ctx, is_pointer=True),
                                 UaNode(val=node, is_pointer=False))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_getNode(ns_ctx, node_id):
        UaNodestore._get_node(Void(val=ns_ctx, is_pointer=True),
                              UaNodeId(val=node_id, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_releaseNode(ns_ctx, node):
        UaNodestore._release_node(Void(val=ns_ctx, is_pointer=True),
                                  UaNode(val=node, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_getNodeCopy(ns_ctx, node_id, out_node):
        UaNodestore._get_node_copy(Void(val=ns_ctx, is_pointer=True),
                                   UaNodeId(val=node_id, is_pointer=True),
                                   UaList(val=out_node))  # todo: might not work. it's a UA_Node**

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_insertNode(ns_ctx, node, added_node_id):
        UaNodestore._insert_node(Void(val=ns_ctx, is_pointer=True),
                                 UaNode(val=node, is_pointer=True),
                                 UaNodeId(val=added_node_id, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_replaceNode(ns_ctx, node):
        UaNodestore._replace_node(Void(val=ns_ctx, is_pointer=True),
                                  UaNode(val=node, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_removeNode(ns_ctx, node_id):
        UaNodestore._remove_node(Void(val=ns_ctx, is_pointer=True),
                                 UaNodeId(val=node_id, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_getReferenceTypeId(ns_ctx, ref_type_index):
        UaNodestore._get_reference_type_id(Void(val=ns_ctx, is_pointer=True),
                                           UaByte(val=ref_type_index, is_pointer=False))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_Nodestore_iterate(ns_ctx, visitor, visitor_ctx):
        UaNodestore._iterate(Void(val=ns_ctx, is_pointer=True),
                             # todo: add UaNodeStoreVisitor
                             Void(val=visitor),
                             Void(val=visitor_ctx, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_clear(ac):
        UaAccessControl._clear(UaAccessControl(val=ac, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_activateSession(server, ac, endpoint_description,
                                                         secure_channel_remote_certificate, session_id,
                                                         user_identity_token, session_context):
        
        return UaAccessControl._activate_session(UaServer(val=server),
                                                 UaAccessControl(val=ac, is_pointer=True),
                                                 UaEndpointDescription(val=endpoint_description, is_pointer=True),
                                                 UaByteString(val=secure_channel_remote_certificate, is_pointer=True),
                                                 UaNodeId(val=session_id, is_pointer=True),
                                                 UaList(session_context))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_closeSession(server, ac, session_id, session_context):
        
        UaAccessControl._close_session(UaServer(val=server),
                                       UaAccessControl(val=ac, is_pointer=True),
                                       UaNodeId(val=session_id, is_pointer=True),
                                       Void(val=session_context, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_getUserRightsMask(server, ac, session_id, session_context, node_id,
                                                           node_context):
        
        return UaAccessControl._get_user_rights_mask(UaServer(val=server),
                                                     UaAccessControl(val=ac, is_pointer=True),
                                                     UaNodeId(val=session_id, is_pointer=True),
                                                     Void(val=session_context, is_pointer=True),
                                                     UaNodeId(val=node_id, is_pointer=True),
                                                     Void(val=node_context, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_getUserAccessLevel(server, ac, session_id, session_context, node_id,
                                                            node_context):

        return UaAccessControl._get_user_access_level(UaServer(val=server),
                                                      UaAccessControl(val=ac, is_pointer=True),
                                                      UaNodeId(val=session_id, is_pointer=True),
                                                      Void(val=session_context, is_pointer=True),
                                                      UaNodeId(val=node_id, is_pointer=True),
                                                      Void(val=node_context, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_getUserExecutable(server, ac, session_id, session_context, method_id,
                                                           method_context):

        return UaAccessControl._get_user_executable(UaServer(val=server),
                                                    UaAccessControl(val=ac, is_pointer=True),
                                                    UaNodeId(val=session_id, is_pointer=True),
                                                    Void(val=session_context, is_pointer=True),
                                                    UaNodeId(val=method_id, is_pointer=True),
                                                    Void(val=method_context, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_getUserExecutableOnObject(server, ac, session_id, session_context, method_id,
                                                                   method_context, object_id, object_context):

        return UaAccessControl._get_user_executable_on_object(UaServer(val=server),
                                                              UaAccessControl(val=ac, is_pointer=True),
                                                              UaNodeId(val=session_id, is_pointer=True),
                                                              Void(val=session_context, is_pointer=True),
                                                              UaNodeId(val=method_id, is_pointer=True),
                                                              Void(val=method_context, is_pointer=True),
                                                              UaNodeId(val=object_id, is_pointer=True),
                                                              Void(val=object_context, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_allowAddNode(server, ac, session_id, session_context, item):

        return UaAccessControl._allow_add_node(UaServer(val=server),
                                               UaAccessControl(val=ac, is_pointer=True),
                                               UaNodeId(val=session_id, is_pointer=True),
                                               Void(val=session_context, is_pointer=True),
                                               UaAddNodesItem(val=item, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_allowAddReference(server, ac, session_id, session_context, item):

        return UaAccessControl._allow_add_reference(UaServer(val=server),
                                                    UaAccessControl(val=ac, is_pointer=True),
                                                    UaNodeId(val=session_id, is_pointer=True),
                                                    Void(val=session_context, is_pointer=True),
                                                    UaAddReferencesItem(val=item, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_allowDeleteNode(server, ac, session_id, session_context, item):

        return UaAccessControl._allow_delete_node(UaServer(val=server),
                                                  UaAccessControl(val=ac, is_pointer=True),
                                                  UaNodeId(val=session_id, is_pointer=True),
                                                  Void(val=session_context, is_pointer=True),
                                                  UaDeleteNodesItem(val=item, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_allowDeleteReference(server, ac, session_id, session_context, item):

        return UaAccessControl._allow_delete_reference(UaServer(val=server),
                                                       UaAccessControl(val=ac, is_pointer=True),
                                                       UaNodeId(val=session_id, is_pointer=True),
                                                       Void(val=session_context, is_pointer=True),
                                                       UaDeleteReferencesItem(val=item, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_AccessControl_allowBrowseNode(server, ac, session_id, session_context):

        return UaAccessControl._allow_browse_node(UaServer(val=server),
                                                  UaAccessControl(val=ac, is_pointer=True),
                                                  UaNodeId(val=session_id, is_pointer=True),
                                                  Void(val=session_context, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_GlobalNodeLifecycle_constructor(server, session_id, session_context, node_id, node_context):

        return UaGlobalNodeLifecycle._constructor(UaServer(val=server),
                                                  UaNodeId(val=session_id, is_pointer=True),
                                                  Void(val=session_context, is_pointer=True),
                                                  UaNodeId(val=node_id, is_pointer=True),
                                                  UaList(val=node_context))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_GlobalNodeLifecycle_destructor(server, session_id, session_context, node_id, node_context):

        return UaGlobalNodeLifecycle._destructor(UaServer(val=server),
                                                 UaNodeId(val=session_id, is_pointer=True),
                                                 Void(val=session_context, is_pointer=True),
                                                 UaNodeId(val=node_id, is_pointer=True),
                                                 Void(val=node_context, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_GlobalNodeLifecycle_createOptionalChild(server, session_id, session_context, source_node_id,
                                                                   target_parent_node_id, reference_type_id):

        return UaGlobalNodeLifecycle._create_optional_child(UaServer(val=server),
                                                            UaNodeId(val=session_id, is_pointer=True),
                                                            Void(val=session_context, is_pointer=True),
                                                            UaNodeId(val=source_node_id, is_pointer=True),
                                                            UaNodeId(val=target_parent_node_id, is_pointer=True),
                                                            UaNodeId(val=reference_type_id, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_GlobalNodeLifecycle_generateChildNodeId(server, session_id, session_context, source_node_id,
                                                                   target_parent_node_id, reference_type_id,
                                                                   target_node_id):

        return UaGlobalNodeLifecycle._generate_child_node_id(UaServer(val=server),
                                                             UaNodeId(val=session_id, is_pointer=True),
                                                             Void(val=session_context, is_pointer=True),
                                                             UaNodeId(val=target_parent_node_id, is_pointer=True),
                                                             UaNodeId(val=reference_type_id, is_pointer=True),
                                                             UaNodeId(val=target_node_id, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_ServerNetworkLayer_start(nl, logger, custom_host_name):
        return UaServerNetworkLayer._start(UaServerNetworkLayer(val=nl),
                                           UaLogger(val=logger, is_pointer=True),
                                           UaString(val=custom_host_name, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_ServerNetworkLayer_listen(nl, server, timeout):
        return UaServerNetworkLayer._listen(UaServerNetworkLayer(val=nl), UaServer(val=server),
                                            UaUInt16(val=timeout, is_pointer=False))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_ServerNetworkLayer_stop(nl, server):
        return UaServerNetworkLayer._stop(UaServerNetworkLayer(val=nl, is_pointer=True), UaServer(val=server))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_ServerNetworkLayer_clear(nl):
        return UaServerNetworkLayer._clear(UaServerNetworkLayer(val=nl))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_SecurityPolicy_updateCertificateAndPrivateKey(policy, new_certificate, new_private_key):
        return UaSecurityPolicy._update_certificate_and_private_key(UaSecurityPolicy(val=policy, is_pointer=True),
                                                                    UaByteString(val=new_certificate, is_pointer=False),
                                                                    UaByteString(val=new_private_key, is_pointer=False))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_SecurityPolicy_clear(policy):
        UaSecurityPolicy._clear(UaSecurityPolicy(val=policy, is_pointer=True))

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_NodeTypeLifecycle_constructor(server, session_id, session_context, type_node_id,
                                                         type_node_context, node_id, node_context):

        status_code = UaNodeTypeLifecycle._constructor(UaServer(val=server),
                                                       UaNodeId(val=session_id, is_pointer=True),
                                                       Void(val=session_context, is_pointer=True),
                                                       UaNodeId(val=type_node_id, is_pointer=True),
                                                       Void(val=type_node_context, is_pointer=True),
                                                       UaNodeId(val=node_id, is_pointer=True),
                                                       Void(val=node_context))
        return status_code._val

    @staticmethod
    @ffi.def_extern()
    def _python_wrapper_UA_NodeTypeLifecycle_destructor(server, session_id, session_context, type_node_id,
                                                        type_node_context, node_id, node_context):

        UaNodeTypeLifecycle._destructor(UaServer(val=server),
                                        UaNodeId(val=session_id, is_pointer=True),
                                        Void(val=session_context, is_pointer=True),
                                        UaNodeId(val=type_node_id, is_pointer=True),
                                        Void(val=type_node_context, is_pointer=True),
                                        UaNodeId(val=node_id, is_pointer=True),
                                        Void(val=node_context))

class UaServer:
    """
    This class is used to create and manage servers as well as invoking services
    """
    # Typehint for users. Developers could also set val to a UA_Server.
    def __init__(self, val: Union[UaServerConfig, int, Tuple[str, int]] = None):
        self._running = UaBoolean(False)
        if val is None:
            self.ua_server = lib.UA_Server_new()
            self.set_default_config()
        elif type(val) is int:
            self.ua_server = lib.UA_Server_new()
            self.set_minimal_config(UaInt16(val))
        elif type(val) is tuple:
            hostname = val[0]
            port = val[1]
            self.ua_server = lib.UA_Server_new()
            self.set_minimal_config(UaInt16(port))
            self.set_hostname(hostname)
        elif type(val) is UaServerConfig:
            self.ua_server = lib.UA_Server_newWithConfig(val._ptr)
        else:
            self.ua_server = val

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, running: Union[bool, UaBoolean]):
        if isinstance(running, UaBoolean):
            running = running.value
        self._running._value[0] = running

    def run(self):
        self.running = True
        ret_val = lib.UA_Server_run(self.ua_server, self.running._value)
        return UaStatusCode(val=ret_val)

    def run_async(self, daemon=False):
        t = threading.Thread(target=self.run, daemon=daemon)
        t.start()
        time.sleep(0.50)
        return t

    def run_shutdown(self):
        raw_result = lib.UA_Server_run_shutdown(self.ua_server)
        return UaStatusCode(val=raw_result)

    def set_hostname(self, hostname: Union[UaString, str]):
        if type(hostname) is str:
            hostname = UaString(hostname)
        self.get_config().custom_hostname = hostname

    def get_config(self):
        return UaServerConfig(val=lib.UA_Server_getConfig(self.ua_server))

    def run_startup(self):
        raw_value = lib.UA_Server_run_startup(self.ua_server)
        return UaStatusCode(val=raw_value)

    def run_iterate(self, wait_internal: UaBoolean = UaBoolean(True)):
        raw_value = lib.UA_Server_run_iterate(self.ua_server, wait_internal._val)
        return UaUInt16(val=raw_value)

    def set_minimal_config(self, port_number: UaInt16, certificate: UaByteString = None):
        if certificate is None:
            certificate = Void.NULL()
        raw_result = lib.UA_ServerConfig_setMinimal(self.get_config()._ptr, port_number._val, certificate._ptr)
        return UaStatusCode(val=raw_result)

    def set_default_config(self):
        raw_result = lib.UA_ServerConfig_setDefault(self.get_config()._ptr)

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

    def browse(self, max_refs: UaUInt32):
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

        return ServerServiceResults.NodeIdResult(UaStatusCode(status_code),
                                                 out_node_id)  # out_node must not be None

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
