# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_types_logger import *
from ua_types_parent import _ptr, _val, _is_null, _get_c_type, _is_ptr
from typing import Callable


# TODO: remove placeholder when implmentaion of callbacks is done
class c_fun(UaType):
    def __init__(self, val, is_pointer):
        super.__init__(val, is_pointer)


# +++++++++++++++++++ aa_entry +++++++++++++++++++++++
class aa_entry(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("struct aa_entrry*")
        if isinstance(val, UaType):
            val = ffi.cast("struct aa_entrry*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._left = aa_entry(val=val.left, is_pointer=True)
            self._right = aa_entry(val=val.right, is_pointer=True)
            self._int = UaUInt32(val=val.int, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "aa_entry")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._left._value = val.left
            self._right._value = val.right
            self._int._value[0] = _val(val.int)

    @property
    def left(self):
        if self._null:
            return None
        else:
            return self._left

    @property
    def right(self):
        if self._null:
            return None
        else:
            return self._right

    @property
    def int(self):
        if self._null:
            return None
        else:
            return self._int

    @left.setter
    def left(self, val: 'aa_entry'):
        self._left = val
        self._value.left = val._ptr

    @right.setter
    def right(self, val: 'aa_entry'):
        self._right = val
        self._value.right = val._ptr

    @int.setter
    def int(self, val: UaUInt32):
        self._int = val
        self._value.int = val._val

    def __str__(self, n=0):
        if self._null:
            return "(aa_entry) : NULL\n"

        return ("(aa_entry) :\n"
                + "\t" * (n + 1) + "left" + self._left.__str__(n + 1)
                + "\t" * (n + 1) + "right" + self._right.__str__(n + 1)
                + "\t" * (n + 1) + "int" + self._int.__str__(n + 1))


# +++++++++++++++++++ UaNode +++++++++++++++++++++++
class UaNode(UaType):
    # TODO: add union members

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Node *"), is_pointer)
        else:
            super().__init__(ffi.new("UA_Node *"), _val(val), is_pointer)


# +++++++++++++++++++ UaTwoStateVariableCallbackType +++++++++++++++++++++++
class UaTwoStateVariableCallbackType(UaType):
    def __init__(self):
        super().__init__(None)


# +++++++++++++++++++ UaTwoStateVariableChangeCallback +++++++++++++++++++++++
class UaTwoStateVariableChangeCallback(UaType):
    def __init__(self):
        super().__init__(None)


# +++++++++++++++++++ UaCertificateVerification +++++++++++++++++++++++
class UaCertificateVerification(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CertificateVerification*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_CertificateVerification*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._context = Void(val=val.context, is_pointer=True)
            self._verify_certificate = c_fun(val=val.verifyCertificate, is_pointer=True)
            self._verify_application_uri = c_fun(val=val.verifyApplicationURI, is_pointer=True)
            self._clear = c_fun(val=val.clear, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_CertificateVerification")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._context._value = val.context
            self._verify_certificate._value = val.verifyCertificate
            self._verify_application_uri._value = val.verifyApplicationURI
            self._clear._value = val.clear

    @property
    def context(self):
        if self._null:
            return None
        else:
            return self._context

    @property
    def verify_certificate(self):
        if self._null:
            return None
        else:
            return self._verify_certificate

    @property
    def verify_application_uri(self):
        if self._null:
            return None
        else:
            return self._verify_application_uri

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear

    @context.setter
    def context(self, val: Void):
        self._context = val
        self._value.context = val._ptr

    @verify_certificate.setter
    def verify_certificate(self, val: c_fun):
        self._verify_certificate = val
        self._value.verifyCertificate = val._ptr

    @verify_application_uri.setter
    def verify_application_uri(self, val: c_fun):
        self._verify_application_uri = val
        self._value.verifyApplicationURI = val._ptr

    @clear.setter
    def clear(self, val: c_fun):
        self._clear = val
        self._value.clear = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaCertificateVerification) : NULL\n"

        return ("(UaCertificateVerification) :\n"
                + "\t" * (n + 1) + "context" + self._context.__str__(n + 1)
                + "\t" * (n + 1) + "verify_certificate" + self._verify_certificate.__str__(n + 1)
                + "\t" * (n + 1) + "verify_application_uri" + self._verify_application_uri.__str__(n + 1)
                + "\t" * (n + 1) + "clear" + self._clear.__str__(n + 1))


# +++++++++++++++++++ UaNodestore +++++++++++++++++++++++
class UaNodestore(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_Nodestore*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_Nodestore*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._context = Void(val=val.context, is_pointer=True)
            self._clear = c_fun(val=val.clear, is_pointer=True)
            self._new_node = c_fun(val=val.newNode, is_pointer=True)
            self._delete_node = c_fun(val=val.deleteNode, is_pointer=True)
            self._get_node = c_fun(val=val.getNode, is_pointer=True)
            self._release_node = c_fun(val=val.releaseNode, is_pointer=True)
            self._get_node_copy = c_fun(val=val.getNodeCopy, is_pointer=True)
            self._insert_node = c_fun(val=val.insertNode, is_pointer=True)
            self._replace_node = c_fun(val=val.replaceNode, is_pointer=True)
            self._remove_node = c_fun(val=val.removeNode, is_pointer=True)
            self._get_reference_type_id = c_fun(val=val.getReferenceTypeId, is_pointer=True)
            self._iterate = c_fun(val=val.iterate, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Nodestore")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._context._value = val.context
            self._clear._value = val.clear
            self._new_node._value = val.newNode
            self._delete_node._value = val.deleteNode
            self._get_node._value = val.getNode
            self._release_node._value = val.releaseNode
            self._get_node_copy._value = val.getNodeCopy
            self._insert_node._value = val.insertNode
            self._replace_node._value = val.replaceNode
            self._remove_node._value = val.removeNode
            self._get_reference_type_id._value = val.getReferenceTypeId
            self._iterate._value = val.iterate

    @property
    def context(self):
        if self._null:
            return None
        else:
            return self._context

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear

    @property
    def new_node(self):
        if self._null:
            return None
        else:
            return self._new_node

    @property
    def delete_node(self):
        if self._null:
            return None
        else:
            return self._delete_node

    @property
    def get_node(self):
        if self._null:
            return None
        else:
            return self._get_node

    @property
    def release_node(self):
        if self._null:
            return None
        else:
            return self._release_node

    @property
    def get_node_copy(self):
        if self._null:
            return None
        else:
            return self._get_node_copy

    @property
    def insert_node(self):
        if self._null:
            return None
        else:
            return self._insert_node

    @property
    def replace_node(self):
        if self._null:
            return None
        else:
            return self._replace_node

    @property
    def remove_node(self):
        if self._null:
            return None
        else:
            return self._remove_node

    @property
    def get_reference_type_id(self):
        if self._null:
            return None
        else:
            return self._get_reference_type_id

    @property
    def iterate(self):
        if self._null:
            return None
        else:
            return self._iterate

    @context.setter
    def context(self, val: Void):
        self._context = val
        self._value.context = val._ptr

    @clear.setter
    def clear(self, val: c_fun):
        self._clear = val
        self._value.clear = val._ptr

    @new_node.setter
    def new_node(self, val: c_fun):
        self._new_node = val
        self._value.newNode = val._ptr

    @delete_node.setter
    def delete_node(self, val: c_fun):
        self._delete_node = val
        self._value.deleteNode = val._ptr

    @get_node.setter
    def get_node(self, val: c_fun):
        self._get_node = val
        self._value.getNode = val._ptr

    @release_node.setter
    def release_node(self, val: c_fun):
        self._release_node = val
        self._value.releaseNode = val._ptr

    @get_node_copy.setter
    def get_node_copy(self, val: c_fun):
        self._get_node_copy = val
        self._value.getNodeCopy = val._ptr

    @insert_node.setter
    def insert_node(self, val: c_fun):
        self._insert_node = val
        self._value.insertNode = val._ptr

    @replace_node.setter
    def replace_node(self, val: c_fun):
        self._replace_node = val
        self._value.replaceNode = val._ptr

    @remove_node.setter
    def remove_node(self, val: c_fun):
        self._remove_node = val
        self._value.removeNode = val._ptr

    @get_reference_type_id.setter
    def get_reference_type_id(self, val: c_fun):
        self._get_reference_type_id = val
        self._value.getReferenceTypeId = val._ptr

    @iterate.setter
    def iterate(self, val: c_fun):
        self._iterate = val
        self._value.iterate = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaNodestore) : NULL\n"

        return ("(UaNodestore) :\n"
                + "\t" * (n + 1) + "context" + self._context.__str__(n + 1)
                + "\t" * (n + 1) + "clear" + self._clear.__str__(n + 1)
                + "\t" * (n + 1) + "new_node" + self._new_node.__str__(n + 1)
                + "\t" * (n + 1) + "delete_node" + self._delete_node.__str__(n + 1)
                + "\t" * (n + 1) + "get_node" + self._get_node.__str__(n + 1)
                + "\t" * (n + 1) + "release_node" + self._release_node.__str__(n + 1)
                + "\t" * (n + 1) + "get_node_copy" + self._get_node_copy.__str__(n + 1)
                + "\t" * (n + 1) + "insert_node" + self._insert_node.__str__(n + 1)
                + "\t" * (n + 1) + "replace_node" + self._replace_node.__str__(n + 1)
                + "\t" * (n + 1) + "remove_node" + self._remove_node.__str__(n + 1)
                + "\t" * (n + 1) + "get_reference_type_id" + self._get_reference_type_id.__str__(n + 1)
                + "\t" * (n + 1) + "iterate" + self._iterate.__str__(n + 1))


# +++++++++++++++++++ UaAccessControl +++++++++++++++++++++++
class UaAccessControl(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AccessControl*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_AccessControl*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._context = Void(val=val.context, is_pointer=True)
            self._clear = c_fun(val=val.clear, is_pointer=True)
            self._user_token_policies_size = SizeT(val=val.userTokenPoliciesSize, is_pointer=False)
            self._user_token_policies = UaUserTokenPolicy(val=val.userTokenPolicies, is_pointer=True)
            self._activate_session = c_fun(val=val.activateSession, is_pointer=True)
            self._close_session = c_fun(val=val.closeSession, is_pointer=True)
            self._get_user_rights_mask = c_fun(val=val.getUserRightsMask, is_pointer=True)
            self._get_user_access_level = c_fun(val=val.getUserAccessLevel, is_pointer=True)
            self._get_user_executable = c_fun(val=val.getUserExecutable, is_pointer=True)
            self._get_user_executable_on_object = c_fun(val=val.getUserExecutableOnObject, is_pointer=True)
            self._allow_add_node = c_fun(val=val.allowAddNode, is_pointer=True)
            self._allow_add_reference = c_fun(val=val.allowAddReference, is_pointer=True)
            self._allow_delete_node = c_fun(val=val.allowDeleteNode, is_pointer=True)
            self._allow_delete_reference = c_fun(val=val.allowDeleteReference, is_pointer=True)
            self._allow_browse_node = c_fun(val=val.allowBrowseNode, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_AccessControl")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._context._value = val.context
            self._clear._value = val.clear
            self._user_token_policies_size._value[0] = _val(val.userTokenPoliciesSize)
            self._user_token_policies._value = val.userTokenPolicies
            self._activate_session._value = val.activateSession
            self._close_session._value = val.closeSession
            self._get_user_rights_mask._value = val.getUserRightsMask
            self._get_user_access_level._value = val.getUserAccessLevel
            self._get_user_executable._value = val.getUserExecutable
            self._get_user_executable_on_object._value = val.getUserExecutableOnObject
            self._allow_add_node._value = val.allowAddNode
            self._allow_add_reference._value = val.allowAddReference
            self._allow_delete_node._value = val.allowDeleteNode
            self._allow_delete_reference._value = val.allowDeleteReference
            self._allow_browse_node._value = val.allowBrowseNode

    @property
    def context(self):
        if self._null:
            return None
        else:
            return self._context

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear

    @property
    def user_token_policies_size(self):
        if self._null:
            return None
        else:
            return self._user_token_policies_size

    @property
    def user_token_policies(self):
        if self._null:
            return None
        else:
            return self._user_token_policies

    @property
    def activate_session(self):
        if self._null:
            return None
        else:
            return self._activate_session

    @property
    def close_session(self):
        if self._null:
            return None
        else:
            return self._close_session

    @property
    def get_user_rights_mask(self):
        if self._null:
            return None
        else:
            return self._get_user_rights_mask

    @property
    def get_user_access_level(self):
        if self._null:
            return None
        else:
            return self._get_user_access_level

    @property
    def get_user_executable(self):
        if self._null:
            return None
        else:
            return self._get_user_executable

    @property
    def get_user_executable_on_object(self):
        if self._null:
            return None
        else:
            return self._get_user_executable_on_object

    @property
    def allow_add_node(self):
        if self._null:
            return None
        else:
            return self._allow_add_node

    @property
    def allow_add_reference(self):
        if self._null:
            return None
        else:
            return self._allow_add_reference

    @property
    def allow_delete_node(self):
        if self._null:
            return None
        else:
            return self._allow_delete_node

    @property
    def allow_delete_reference(self):
        if self._null:
            return None
        else:
            return self._allow_delete_reference

    @property
    def allow_browse_node(self):
        if self._null:
            return None
        else:
            return self._allow_browse_node

    @context.setter
    def context(self, val: Void):
        self._context = val
        self._value.context = val._ptr

    @clear.setter
    def clear(self, val: c_fun):
        self._clear = val
        self._value.clear = val._ptr

    @user_token_policies_size.setter
    def user_token_policies_size(self, val: SizeT):
        self._user_token_policies_size = val
        self._value.userTokenPoliciesSize = val._val

    @user_token_policies.setter
    def user_token_policies(self, val: UaUserTokenPolicy):
        self._user_token_policies = val
        self._value.userTokenPolicies = val._ptr

    @activate_session.setter
    def activate_session(self, val: c_fun):
        self._activate_session = val
        self._value.activateSession = val._ptr

    @close_session.setter
    def close_session(self, val: c_fun):
        self._close_session = val
        self._value.closeSession = val._ptr

    @get_user_rights_mask.setter
    def get_user_rights_mask(self, val: c_fun):
        self._get_user_rights_mask = val
        self._value.getUserRightsMask = val._ptr

    @get_user_access_level.setter
    def get_user_access_level(self, val: c_fun):
        self._get_user_access_level = val
        self._value.getUserAccessLevel = val._ptr

    @get_user_executable.setter
    def get_user_executable(self, val: c_fun):
        self._get_user_executable = val
        self._value.getUserExecutable = val._ptr

    @get_user_executable_on_object.setter
    def get_user_executable_on_object(self, val: c_fun):
        self._get_user_executable_on_object = val
        self._value.getUserExecutableOnObject = val._ptr

    @allow_add_node.setter
    def allow_add_node(self, val: c_fun):
        self._allow_add_node = val
        self._value.allowAddNode = val._ptr

    @allow_add_reference.setter
    def allow_add_reference(self, val: c_fun):
        self._allow_add_reference = val
        self._value.allowAddReference = val._ptr

    @allow_delete_node.setter
    def allow_delete_node(self, val: c_fun):
        self._allow_delete_node = val
        self._value.allowDeleteNode = val._ptr

    @allow_delete_reference.setter
    def allow_delete_reference(self, val: c_fun):
        self._allow_delete_reference = val
        self._value.allowDeleteReference = val._ptr

    @allow_browse_node.setter
    def allow_browse_node(self, val: c_fun):
        self._allow_browse_node = val
        self._value.allowBrowseNode = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaAccessControl) : NULL\n"

        return ("(UaAccessControl) :\n"
                + "\t" * (n + 1) + "context" + self._context.__str__(n + 1)
                + "\t" * (n + 1) + "clear" + self._clear.__str__(n + 1)
                + "\t" * (n + 1) + "user_token_policies_size" + self._user_token_policies_size.__str__(n + 1)
                + "\t" * (n + 1) + "user_token_policies" + self._user_token_policies.__str__(n + 1)
                + "\t" * (n + 1) + "activate_session" + self._activate_session.__str__(n + 1)
                + "\t" * (n + 1) + "close_session" + self._close_session.__str__(n + 1)
                + "\t" * (n + 1) + "get_user_rights_mask" + self._get_user_rights_mask.__str__(n + 1)
                + "\t" * (n + 1) + "get_user_access_level" + self._get_user_access_level.__str__(n + 1)
                + "\t" * (n + 1) + "get_user_executable" + self._get_user_executable.__str__(n + 1)
                + "\t" * (n + 1) + "get_user_executable_on_object" + self._get_user_executable_on_object.__str__(n + 1)
                + "\t" * (n + 1) + "allow_add_node" + self._allow_add_node.__str__(n + 1)
                + "\t" * (n + 1) + "allow_add_reference" + self._allow_add_reference.__str__(n + 1)
                + "\t" * (n + 1) + "allow_delete_node" + self._allow_delete_node.__str__(n + 1)
                + "\t" * (n + 1) + "allow_delete_reference" + self._allow_delete_reference.__str__(n + 1)
                + "\t" * (n + 1) + "allow_browse_node" + self._allow_browse_node.__str__(n + 1))


# +++++++++++++++++++ UaGlobalNodeLifecycle +++++++++++++++++++++++
class UaGlobalNodeLifecycle(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_GlobalNodeLifecycle*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_GlobalNodeLifecycle*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._constructor = c_fun(val=val.constructor, is_pointer=True)
            self._destructor = c_fun(val=val.destructor, is_pointer=True)
            self._create_optional_child = c_fun(val=val.createOptionalChild, is_pointer=True)
            self._generate_child_node_id = c_fun(val=val.generateChildNodeId, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_GlobalNodeLifecycle")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._constructor._value = val.constructor
            self._destructor._value = val.destructor
            self._create_optional_child._value = val.createOptionalChild
            self._generate_child_node_id._value = val.generateChildNodeId

    @property
    def constructor(self):
        if self._null:
            return None
        else:
            return self._constructor

    @property
    def destructor(self):
        if self._null:
            return None
        else:
            return self._destructor

    @property
    def create_optional_child(self):
        if self._null:
            return None
        else:
            return self._create_optional_child

    @property
    def generate_child_node_id(self):
        if self._null:
            return None
        else:
            return self._generate_child_node_id

    @constructor.setter
    def constructor(self, val: c_fun):
        self._constructor = val
        self._value.constructor = val._ptr

    @destructor.setter
    def destructor(self, val: c_fun):
        self._destructor = val
        self._value.destructor = val._ptr

    @create_optional_child.setter
    def create_optional_child(self, val: c_fun):
        self._create_optional_child = val
        self._value.createOptionalChild = val._ptr

    @generate_child_node_id.setter
    def generate_child_node_id(self, val: c_fun):
        self._generate_child_node_id = val
        self._value.generateChildNodeId = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaGlobalNodeLifecycle) : NULL\n"

        return ("(UaGlobalNodeLifecycle) :\n"
                + "\t" * (n + 1) + "constructor" + self._constructor.__str__(n + 1)
                + "\t" * (n + 1) + "destructor" + self._destructor.__str__(n + 1)
                + "\t" * (n + 1) + "create_optional_child" + self._create_optional_child.__str__(n + 1)
                + "\t" * (n + 1) + "generate_child_node_id" + self._generate_child_node_id.__str__(n + 1))


# +++++++++++++++++++ UaServerNetworkLayer +++++++++++++++++++++++
class UaServerNetworkLayer(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ServerNetworkLayer*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ServerNetworkLayer*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._handle = Void(val=val.handle, is_pointer=True)
            self._statistics = UaNetworkStatistics(val=val.statistics, is_pointer=True)
            self._discovery_url = UaString(val=val.discoveryUrl, is_pointer=False)
            self._local_connection_config = UaConnectionConfig(val=val.localConnectionConfig, is_pointer=False)
            self._start = c_fun(val=val.start, is_pointer=True)
            self._listen = c_fun(val=val.listen, is_pointer=True)
            self._stop = c_fun(val=val.stop, is_pointer=True)
            self._clear = c_fun(val=val.clear, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ServerNetworkLayer")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._handle._value = val.handle
            self._statistics._value = val.statistics
            self._discovery_url._value[0] = _val(val.discoveryUrl)
            self._local_connection_config._value[0] = _val(val.localConnectionConfig)
            self._start._value = val.start
            self._listen._value = val.listen
            self._stop._value = val.stop
            self._clear._value = val.clear

    @property
    def handle(self):
        if self._null:
            return None
        else:
            return self._handle

    @property
    def statistics(self):
        if self._null:
            return None
        else:
            return self._statistics

    @property
    def discovery_url(self):
        if self._null:
            return None
        else:
            return self._discovery_url

    @property
    def local_connection_config(self):
        if self._null:
            return None
        else:
            return self._local_connection_config

    @property
    def start(self):
        if self._null:
            return None
        else:
            return self._start

    @property
    def listen(self):
        if self._null:
            return None
        else:
            return self._listen

    @property
    def stop(self):
        if self._null:
            return None
        else:
            return self._stop

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear

    @handle.setter
    def handle(self, val: Void):
        self._handle = val
        self._value.handle = val._ptr

    @statistics.setter
    def statistics(self, val: UaNetworkStatistics):
        self._statistics = val
        self._value.statistics = val._ptr

    @discovery_url.setter
    def discovery_url(self, val: UaString):
        self._discovery_url = val
        self._value.discoveryUrl = val._val

    @local_connection_config.setter
    def local_connection_config(self, val: 'UaConnectionConfig'):
        self._local_connection_config = val
        self._value.localConnectionConfig = val._val

    @start.setter
    def start(self, val: c_fun):
        self._start = val
        self._value.start = val._ptr

    @listen.setter
    def listen(self, val: c_fun):
        self._listen = val
        self._value.listen = val._ptr

    @stop.setter
    def stop(self, val: c_fun):
        self._stop = val
        self._value.stop = val._ptr

    @clear.setter
    def clear(self, val: c_fun):
        self._clear = val
        self._value.clear = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaServerNetworkLayer) : NULL\n"

        return ("(UaServerNetworkLayer) :\n"
                + "\t" * (n + 1) + "handle" + self._handle.__str__(n + 1)
                + "\t" * (n + 1) + "statistics" + self._statistics.__str__(n + 1)
                + "\t" * (n + 1) + "discovery_url" + self._discovery_url.__str__(n + 1)
                + "\t" * (n + 1) + "local_connection_config" + self._local_connection_config.__str__(n + 1)
                + "\t" * (n + 1) + "start" + self._start.__str__(n + 1)
                + "\t" * (n + 1) + "listen" + self._listen.__str__(n + 1)
                + "\t" * (n + 1) + "stop" + self._stop.__str__(n + 1)
                + "\t" * (n + 1) + "clear" + self._clear.__str__(n + 1))


# +++++++++++++++++++ UaSecurityPolicy +++++++++++++++++++++++
class UaSecurityPolicy(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SecurityPolicy*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SecurityPolicy*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._policy_context = Void(val=val.policyContext, is_pointer=True)
            self._policy_uri = UaByteString(val=val.policyUri, is_pointer=False)
            self._local_certificate = UaByteString(val=val.localCertificate, is_pointer=False)
            self._asymmetric_module = UaSecurityPolicyAsymmetricModule(val=val.asymmetricModule, is_pointer=False)
            self._symmetric_module = UaSecurityPolicySymmetricModule(val=val.symmetricModule, is_pointer=False)
            self._certificate_signing_algorithm = UaSecurityPolicySignatureAlgorithm(
                val=val.certificateSigningAlgorithm, is_pointer=False)
            self._channel_module = UaSecurityPolicyChannelModule(val=val.channelModule, is_pointer=False)
            self._logger = UaLogger(val=val.logger, is_pointer=True)
            self._update_certificate_and_private_key = c_fun(val=val.updateCertificateAndPrivateKey, is_pointer=True)
            self._clear = c_fun(val=val.clear, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SecurityPolicy")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._policy_context._value = val.policyContext
            self._policy_uri._value[0] = _val(val.policyUri)
            self._local_certificate._value[0] = _val(val.localCertificate)
            self._asymmetric_module._value[0] = _val(val.asymmetricModule)
            self._symmetric_module._value[0] = _val(val.symmetricModule)
            self._certificate_signing_algorithm._value[0] = _val(val.certificateSigningAlgorithm)
            self._channel_module._value[0] = _val(val.channelModule)
            self._logger._value = val.logger
            self._update_certificate_and_private_key._value = val.updateCertificateAndPrivateKey
            self._clear._value = val.clear

    @property
    def policy_context(self):
        if self._null:
            return None
        else:
            return self._policy_context

    @property
    def policy_uri(self):
        if self._null:
            return None
        else:
            return self._policy_uri

    @property
    def local_certificate(self):
        if self._null:
            return None
        else:
            return self._local_certificate

    @property
    def asymmetric_module(self):
        if self._null:
            return None
        else:
            return self._asymmetric_module

    @property
    def symmetric_module(self):
        if self._null:
            return None
        else:
            return self._symmetric_module

    @property
    def certificate_signing_algorithm(self):
        if self._null:
            return None
        else:
            return self._certificate_signing_algorithm

    @property
    def channel_module(self):
        if self._null:
            return None
        else:
            return self._channel_module

    @property
    def logger(self):
        if self._null:
            return None
        else:
            return self._logger

    @property
    def update_certificate_and_private_key(self):
        if self._null:
            return None
        else:
            return self._update_certificate_and_private_key

    @property
    def clear(self):
        if self._null:
            return None
        else:
            return self._clear

    @policy_context.setter
    def policy_context(self, val: Void):
        self._policy_context = val
        self._value.policyContext = val._ptr

    @policy_uri.setter
    def policy_uri(self, val: UaByteString):
        self._policy_uri = val
        self._value.policyUri = val._val

    @local_certificate.setter
    def local_certificate(self, val: UaByteString):
        self._local_certificate = val
        self._value.localCertificate = val._val

    @asymmetric_module.setter
    def asymmetric_module(self, val: 'UaSecurityPolicyAsymmetricModule'):
        self._asymmetric_module = val
        self._value.asymmetricModule = val._val

    @symmetric_module.setter
    def symmetric_module(self, val: 'UaSecurityPolicySymmetricModule'):
        self._symmetric_module = val
        self._value.symmetricModule = val._val

    @certificate_signing_algorithm.setter
    def certificate_signing_algorithm(self, val: 'UaSecurityPolicySignatureAlgorithm'):
        self._certificate_signing_algorithm = val
        self._value.certificateSigningAlgorithm = val._val

    @channel_module.setter
    def channel_module(self, val: 'UaSecurityPolicyChannelModule'):
        self._channel_module = val
        self._value.channelModule = val._val

    @logger.setter
    def logger(self, val: UaLogger):
        self._logger = val
        self._value.logger = val._ptr

    @update_certificate_and_private_key.setter
    def update_certificate_and_private_key(self, val: c_fun):
        self._update_certificate_and_private_key = val
        self._value.updateCertificateAndPrivateKey = val._ptr

    @clear.setter
    def clear(self, val: c_fun):
        self._clear = val
        self._value.clear = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaSecurityPolicy) : NULL\n"

        return ("(UaSecurityPolicy) :\n"
                + "\t" * (n + 1) + "policy_context" + self._policy_context.__str__(n + 1)
                + "\t" * (n + 1) + "policy_uri" + self._policy_uri.__str__(n + 1)
                + "\t" * (n + 1) + "local_certificate" + self._local_certificate.__str__(n + 1)
                + "\t" * (n + 1) + "asymmetric_module" + self._asymmetric_module.__str__(n + 1)
                + "\t" * (n + 1) + "symmetric_module" + self._symmetric_module.__str__(n + 1)
                + "\t" * (n + 1) + "certificate_signing_algorithm" + self._certificate_signing_algorithm.__str__(n + 1)
                + "\t" * (n + 1) + "channel_module" + self._channel_module.__str__(n + 1)
                + "\t" * (n + 1) + "logger" + self._logger.__str__(n + 1)
                + "\t" * (
                            n + 1) + "update_certificate_and_private_key" + self._update_certificate_and_private_key.__str__(
                    n + 1)
                + "\t" * (n + 1) + "clear" + self._clear.__str__(n + 1))


# +++++++++++++++++++ UaConnectionConfig +++++++++++++++++++++++
class UaConnectionConfig(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ConnectionConfig*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ConnectionConfig*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._protocol_version = UaUInt32(val=val.protocolVersion, is_pointer=False)
            self._recv_buffer_size = UaUInt32(val=val.recvBufferSize, is_pointer=False)
            self._send_buffer_size = UaUInt32(val=val.sendBufferSize, is_pointer=False)
            self._local_max_message_size = UaUInt32(val=val.localMaxMessageSize, is_pointer=False)
            self._remote_max_message_size = UaUInt32(val=val.remoteMaxMessageSize, is_pointer=False)
            self._local_max_chunk_count = UaUInt32(val=val.localMaxChunkCount, is_pointer=False)
            self._remote_max_chunk_count = UaUInt32(val=val.remoteMaxChunkCount, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ConnectionConfig")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._protocol_version._value[0] = _val(val.protocolVersion)
            self._recv_buffer_size._value[0] = _val(val.recvBufferSize)
            self._send_buffer_size._value[0] = _val(val.sendBufferSize)
            self._local_max_message_size._value[0] = _val(val.localMaxMessageSize)
            self._remote_max_message_size._value[0] = _val(val.remoteMaxMessageSize)
            self._local_max_chunk_count._value[0] = _val(val.localMaxChunkCount)
            self._remote_max_chunk_count._value[0] = _val(val.remoteMaxChunkCount)

    @property
    def protocol_version(self):
        if self._null:
            return None
        else:
            return self._protocol_version

    @property
    def recv_buffer_size(self):
        if self._null:
            return None
        else:
            return self._recv_buffer_size

    @property
    def send_buffer_size(self):
        if self._null:
            return None
        else:
            return self._send_buffer_size

    @property
    def local_max_message_size(self):
        if self._null:
            return None
        else:
            return self._local_max_message_size

    @property
    def remote_max_message_size(self):
        if self._null:
            return None
        else:
            return self._remote_max_message_size

    @property
    def local_max_chunk_count(self):
        if self._null:
            return None
        else:
            return self._local_max_chunk_count

    @property
    def remote_max_chunk_count(self):
        if self._null:
            return None
        else:
            return self._remote_max_chunk_count

    @protocol_version.setter
    def protocol_version(self, val: UaUInt32):
        self._protocol_version = val
        self._value.protocolVersion = val._val

    @recv_buffer_size.setter
    def recv_buffer_size(self, val: UaUInt32):
        self._recv_buffer_size = val
        self._value.recvBufferSize = val._val

    @send_buffer_size.setter
    def send_buffer_size(self, val: UaUInt32):
        self._send_buffer_size = val
        self._value.sendBufferSize = val._val

    @local_max_message_size.setter
    def local_max_message_size(self, val: UaUInt32):
        self._local_max_message_size = val
        self._value.localMaxMessageSize = val._val

    @remote_max_message_size.setter
    def remote_max_message_size(self, val: UaUInt32):
        self._remote_max_message_size = val
        self._value.remoteMaxMessageSize = val._val

    @local_max_chunk_count.setter
    def local_max_chunk_count(self, val: UaUInt32):
        self._local_max_chunk_count = val
        self._value.localMaxChunkCount = val._val

    @remote_max_chunk_count.setter
    def remote_max_chunk_count(self, val: UaUInt32):
        self._remote_max_chunk_count = val
        self._value.remoteMaxChunkCount = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaConnectionConfig) : NULL\n"

        return ("(UaConnectionConfig) :\n"
                + "\t" * (n + 1) + "protocol_version" + self._protocol_version.__str__(n + 1)
                + "\t" * (n + 1) + "recv_buffer_size" + self._recv_buffer_size.__str__(n + 1)
                + "\t" * (n + 1) + "send_buffer_size" + self._send_buffer_size.__str__(n + 1)
                + "\t" * (n + 1) + "local_max_message_size" + self._local_max_message_size.__str__(n + 1)
                + "\t" * (n + 1) + "remote_max_message_size" + self._remote_max_message_size.__str__(n + 1)
                + "\t" * (n + 1) + "local_max_chunk_count" + self._local_max_chunk_count.__str__(n + 1)
                + "\t" * (n + 1) + "remote_max_chunk_count" + self._remote_max_chunk_count.__str__(n + 1))


# +++++++++++++++++++ UaSecurityPolicyAsymmetricModule +++++++++++++++++++++++
class UaSecurityPolicyAsymmetricModule(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SecurityPolicyAsymmetricModule*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SecurityPolicyAsymmetricModule*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)


    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SecurityPolicyAsymmetricModule")
        else:
            self._value[0] = _val(val)


    def __str__(self, n=0):
        if self._null:
            return "(UaSecurityPolicyAsymmetricModule) : NULL\n"

        return ("(UaSecurityPolicyAsymmetricModule) :\n")


# +++++++++++++++++++ UaSecurityPolicySymmetricModule +++++++++++++++++++++++
class UaSecurityPolicySymmetricModule(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SecurityPolicySymmetricModule*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SecurityPolicySymmetricModule*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)


    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SecurityPolicySymmetricModule")
        else:
            self._value[0] = _val(val)

    def __str__(self, n=0):
        if self._null:
            return "(UaSecurityPolicySymmetricModule) : NULL\n"

        return ("(UaSecurityPolicySymmetricModule) :\n")


# +++++++++++++++++++ UaSecurityPolicyChannelModule +++++++++++++++++++++++
class UaSecurityPolicyChannelModule(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SecurityPolicyChannelModule*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SecurityPolicyChannelModule*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)


    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SecurityPolicyChannelModule")
        else:
            self._value[0] = _val(val)

    def __str__(self, n=0):
        if self._null:
            return "(UaSecurityPolicyChannelModule) : NULL\n"

        return "(UaSecurityPolicyChannelModule) :\n"


# +++++++++++++++++++ UaSecurityPolicySignatureAlgorithm +++++++++++++++++++++++
class UaSecurityPolicySignatureAlgorithm(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SecurityPolicySignatureAlgorithm*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_SecurityPolicySignatureAlgorithm*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)


    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SecurityPolicySignatureAlgorithm")
        else:
            self._value[0] = _val(val)
    def __str__(self, n=0):
        if self._null:
            return "(UaSecurityPolicySignatureAlgorithm) : NULL\n"

        return ("(UaSecurityPolicySignatureAlgorithm) :\n")


# +++++++++++++++++++ UaNodeTypeLifecycle +++++++++++++++++++++++
class UaNodeTypeLifecycle(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NodeTypeLifecycle*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_NodeTypeLifecycle*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._constructor = c_fun(val=val.constructor, is_pointer=True)
            self._destructor = c_fun(val=val.destructor, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NodeTypeLifecycle")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._constructor._value = val.constructor
            self._destructor._value = val.destructor

    @property
    def constructor(self):
        if self._null:
            return None
        else:
            return self._constructor

    @property
    def destructor(self):
        if self._null:
            return None
        else:
            return self._destructor

    @constructor.setter
    def constructor(self, val: c_fun):
        self._constructor = val
        self._value.constructor = val._ptr

    @destructor.setter
    def destructor(self, val: c_fun):
        self._destructor = val
        self._value.destructor = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaNodeTypeLifecycle) : NULL\n"

        return ("(UaNodeTypeLifecycle) :\n"
                + "\t" * (n + 1) + "constructor" + self._constructor.__str__(n + 1)
                + "\t" * (n + 1) + "destructor" + self._destructor.__str__(n + 1))


# +++++++++++++++++++ UaNodeReferenceKind +++++++++++++++++++++++
class UaNodeReferenceKind(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NodeReferenceKind*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_NodeReferenceKind*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._id_tree_root = aa_entry(val=val.idTreeRoot, is_pointer=True)
            self._name_tree_root = aa_entry(val=val.nameTreeRoot, is_pointer=True)
            self._reference_type_index = UaByte(val=val.referenceTypeIndex, is_pointer=False)
            self._is_inverse = UaBoolean(val=val.isInverse, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NodeReferenceKind")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._id_tree_root._value = val.idTreeRoot
            self._name_tree_root._value = val.nameTreeRoot
            self._reference_type_index._value[0] = _val(val.referenceTypeIndex)
            self._is_inverse._value[0] = _val(val.isInverse)

    @property
    def id_tree_root(self):
        if self._null:
            return None
        else:
            return self._id_tree_root

    @property
    def name_tree_root(self):
        if self._null:
            return None
        else:
            return self._name_tree_root

    @property
    def reference_type_index(self):
        if self._null:
            return None
        else:
            return self._reference_type_index

    @property
    def is_inverse(self):
        if self._null:
            return None
        else:
            return self._is_inverse

    @id_tree_root.setter
    def id_tree_root(self, val: aa_entry):
        self._id_tree_root = val
        self._value.idTreeRoot = val._ptr

    @name_tree_root.setter
    def name_tree_root(self, val: aa_entry):
        self._name_tree_root = val
        self._value.nameTreeRoot = val._ptr

    @reference_type_index.setter
    def reference_type_index(self, val: UaByte):
        self._reference_type_index = val
        self._value.referenceTypeIndex = val._val

    @is_inverse.setter
    def is_inverse(self, val: UaBoolean):
        self._is_inverse = val
        self._value.isInverse = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaNodeReferenceKind) : NULL\n"

        return ("(UaNodeReferenceKind) :\n"
                + "\t" * (n + 1) + "id_tree_root" + self._id_tree_root.__str__(n + 1)
                + "\t" * (n + 1) + "name_tree_root" + self._name_tree_root.__str__(n + 1)
                + "\t" * (n + 1) + "reference_type_index" + self._reference_type_index.__str__(n + 1)
                + "\t" * (n + 1) + "is_inverse" + self._is_inverse.__str__(n + 1))


# +++++++++++++++++++ UaNodeHead +++++++++++++++++++++++
class UaNodeHead(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NodeHead*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_NodeHead*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
            self._node_class = UaNodeClass(val=val.nodeClass, is_pointer=False)
            self._browse_name = UaQualifiedName(val=val.browseName, is_pointer=False)
            self._display_name = UaLocalizedText(val=val.displayName, is_pointer=False)
            self._description = UaLocalizedText(val=val.description, is_pointer=False)
            self._write_mask = UaUInt32(val=val.writeMask, is_pointer=False)
            self._references_size = SizeT(val=val.referencesSize, is_pointer=False)
            self._references = UaNodeReferenceKind(val=val.references, is_pointer=True)
            self._context = Void(val=val.context, is_pointer=True)
            self._constructed = UaBoolean(val=val.constructed, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NodeHead")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._node_id._value[0] = _val(val.nodeId)
            self._node_class._value[0] = _val(val.nodeClass)
            self._browse_name._value[0] = _val(val.browseName)
            self._display_name._value[0] = _val(val.displayName)
            self._description._value[0] = _val(val.description)
            self._write_mask._value[0] = _val(val.writeMask)
            self._references_size._value[0] = _val(val.referencesSize)
            self._references._value = val.references
            self._context._value = val.context
            self._constructed._value[0] = _val(val.constructed)

    @property
    def node_id(self):
        if self._null:
            return None
        else:
            return self._node_id

    @property
    def node_class(self):
        if self._null:
            return None
        else:
            return self._node_class

    @property
    def browse_name(self):
        if self._null:
            return None
        else:
            return self._browse_name

    @property
    def display_name(self):
        if self._null:
            return None
        else:
            return self._display_name

    @property
    def description(self):
        if self._null:
            return None
        else:
            return self._description

    @property
    def write_mask(self):
        if self._null:
            return None
        else:
            return self._write_mask

    @property
    def references_size(self):
        if self._null:
            return None
        else:
            return self._references_size

    @property
    def references(self):
        if self._null:
            return None
        else:
            return self._references

    @property
    def context(self):
        if self._null:
            return None
        else:
            return self._context

    @property
    def constructed(self):
        if self._null:
            return None
        else:
            return self._constructed

    @node_id.setter
    def node_id(self, val: UaNodeId):
        self._node_id = val
        self._value.nodeId = val._val

    @node_class.setter
    def node_class(self, val: UaNodeClass):
        self._node_class = val
        self._value.nodeClass = val._val

    @browse_name.setter
    def browse_name(self, val: UaQualifiedName):
        self._browse_name = val
        self._value.browseName = val._val

    @display_name.setter
    def display_name(self, val: UaLocalizedText):
        self._display_name = val
        self._value.displayName = val._val

    @description.setter
    def description(self, val: UaLocalizedText):
        self._description = val
        self._value.description = val._val

    @write_mask.setter
    def write_mask(self, val: UaUInt32):
        self._write_mask = val
        self._value.writeMask = val._val

    @references_size.setter
    def references_size(self, val: SizeT):
        self._references_size = val
        self._value.referencesSize = val._val

    @references.setter
    def references(self, val: UaNodeReferenceKind):
        self._references = val
        self._value.references = val._ptr

    @context.setter
    def context(self, val: Void):
        self._context = val
        self._value.context = val._ptr

    @constructed.setter
    def constructed(self, val: UaBoolean):
        self._constructed = val
        self._value.constructed = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaNodeHead) : NULL\n"

        return ("(UaNodeHead) :\n"
                + "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1)
                + "\t" * (n + 1) + "node_class" + self._node_class.__str__(n + 1)
                + "\t" * (n + 1) + "browse_name" + self._browse_name.__str__(n + 1)
                + "\t" * (n + 1) + "display_name" + self._display_name.__str__(n + 1)
                + "\t" * (n + 1) + "description" + self._description.__str__(n + 1)
                + "\t" * (n + 1) + "write_mask" + self._write_mask.__str__(n + 1)
                + "\t" * (n + 1) + "references_size" + self._references_size.__str__(n + 1)
                + "\t" * (n + 1) + "references" + self._references.__str__(n + 1)
                + "\t" * (n + 1) + "context" + self._context.__str__(n + 1)
                + "\t" * (n + 1) + "constructed" + self._constructed.__str__(n + 1))


# +++++++++++++++++++ UaMethodNode +++++++++++++++++++++++
class UaMethodNode(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_MethodNode*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_MethodNode*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._head = UaNodeHead(val=val.head, is_pointer=False)
            self._executable = UaBoolean(val=val.executable, is_pointer=False)
            self._method = c_fun(val=val.method, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_MethodNode")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._head._value[0] = _val(val.head)
            self._executable._value[0] = _val(val.executable)
            self._method._value[0] = _val(val.method)

    @property
    def head(self):
        if self._null:
            return None
        else:
            return self._head

    @property
    def executable(self):
        if self._null:
            return None
        else:
            return self._executable

    @property
    def method(self):
        if self._null:
            return None
        else:
            return self._method

    @head.setter
    def head(self, val: UaNodeHead):
        self._head = val
        self._value.head = val._val

    @executable.setter
    def executable(self, val: UaBoolean):
        self._executable = val
        self._value.executable = val._val

    @method.setter
    def method(self, val: c_fun):
        self._method = val
        self._value.method = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaMethodNode) : NULL\n"

        return ("(UaMethodNode) :\n"
                + "\t" * (n + 1) + "head" + self._head.__str__(n + 1)
                + "\t" * (n + 1) + "executable" + self._executable.__str__(n + 1)
                + "\t" * (n + 1) + "method" + self._method.__str__(n + 1))


# +++++++++++++++++++ UaObjectNode +++++++++++++++++++++++
class UaObjectNode(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ObjectNode*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ObjectNode*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._head = UaNodeHead(val=val.head, is_pointer=False)
            self._event_notifier = UaByte(val=val.eventNotifier, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ObjectNode")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._head._value[0] = _val(val.head)
            self._event_notifier._value[0] = _val(val.eventNotifier)

    @property
    def head(self):
        if self._null:
            return None
        else:
            return self._head

    @property
    def event_notifier(self):
        if self._null:
            return None
        else:
            return self._event_notifier

    @head.setter
    def head(self, val: UaNodeHead):
        self._head = val
        self._value.head = val._val

    @event_notifier.setter
    def event_notifier(self, val: UaByte):
        self._event_notifier = val
        self._value.eventNotifier = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaObjectNode) : NULL\n"

        return ("(UaObjectNode) :\n"
                + "\t" * (n + 1) + "head" + self._head.__str__(n + 1)
                + "\t" * (n + 1) + "event_notifier" + self._event_notifier.__str__(n + 1))


# +++++++++++++++++++ UaObjectTypeNode +++++++++++++++++++++++
class UaObjectTypeNode(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ObjectTypeNode*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ObjectTypeNode*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._head = UaNodeHead(val=val.head, is_pointer=False)
            self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)
            self._lifecycle = UaNodeTypeLifecycle(val=val.lifecycle, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ObjectTypeNode")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._head._value[0] = _val(val.head)
            self._is_abstract._value[0] = _val(val.isAbstract)
            self._lifecycle._value[0] = _val(val.lifecycle)

    @property
    def head(self):
        if self._null:
            return None
        else:
            return self._head

    @property
    def is_abstract(self):
        if self._null:
            return None
        else:
            return self._is_abstract

    @property
    def lifecycle(self):
        if self._null:
            return None
        else:
            return self._lifecycle

    @head.setter
    def head(self, val: UaNodeHead):
        self._head = val
        self._value.head = val._val

    @is_abstract.setter
    def is_abstract(self, val: UaBoolean):
        self._is_abstract = val
        self._value.isAbstract = val._val

    @lifecycle.setter
    def lifecycle(self, val: UaNodeTypeLifecycle):
        self._lifecycle = val
        self._value.lifecycle = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaObjectTypeNode) : NULL\n"

        return ("(UaObjectTypeNode) :\n"
                + "\t" * (n + 1) + "head" + self._head.__str__(n + 1)
                + "\t" * (n + 1) + "is_abstract" + self._is_abstract.__str__(n + 1)
                + "\t" * (n + 1) + "lifecycle" + self._lifecycle.__str__(n + 1))


# +++++++++++++++++++ UaReferenceTypeSet +++++++++++++++++++++++
class UaReferenceTypeSet(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ReferenceTypeSet*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ReferenceTypeSet*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._bits = UaUInt32(val=val.bits, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ReferenceTypeSet")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._bits._value = val.bits

    @property
    def bits(self):
        if self._null:
            return None
        else:
            return self._bits

    @bits.setter
    def bits(self, val: UaUInt32):
        self._bits = val
        self._value.bits = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaReferenceTypeSet) : NULL\n"

        return ("(UaReferenceTypeSet) :\n"
                + "\t" * (n + 1) + "bits" + self._bits.__str__(n + 1))

# +++++++++++++++++++ UaDataTypeNode +++++++++++++++++++++++

class UaDataTypeNode(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataTypeNode*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DataTypeNode*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._head = UaNodeHead(val=val.head, is_pointer=False)
            self._is_abstract = UaBoolean(val=val.isAbstract, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataTypeNode")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._head._value[0] = _val(val.head)
            self._is_abstract._value[0] = _val(val.isAbstract)

    @property
    def head(self):
        if self._null:
            return None
        else:
            return self._head

    @property
    def is_abstract(self):
        if self._null:
            return None
        else:
            return self._is_abstract

    @head.setter
    def head(self, val: UaNodeHead):
        self._head = val
        self._value.head = val._val

    @is_abstract.setter
    def is_abstract(self, val: UaBoolean):
        self._is_abstract = val
        self._value.isAbstract = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaDataTypeNode) : NULL\n"

        return ("(UaDataTypeNode) :\n"
                + "\t" * (n + 1) + "head" + self._head.__str__(n + 1)
                + "\t" * (n + 1) + "is_abstract" + self._is_abstract.__str__(n + 1))


# +++++++++++++++++++ UaViewNode +++++++++++++++++++++++
class UaViewNode(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ViewNode*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ViewNode*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._head = UaNodeHead(val=val.head, is_pointer=False)
            self._event_notifier = UaByte(val=val.eventNotifier, is_pointer=False)
            self._contains_no_loops = UaBoolean(val=val.containsNoLoops, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ViewNode")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._head._value[0] = _val(val.head)
            self._event_notifier._value[0] = _val(val.eventNotifier)
            self._contains_no_loops._value[0] = _val(val.containsNoLoops)

    @property
    def head(self):
        if self._null:
            return None
        else:
            return self._head

    @property
    def event_notifier(self):
        if self._null:
            return None
        else:
            return self._event_notifier

    @property
    def contains_no_loops(self):
        if self._null:
            return None
        else:
            return self._contains_no_loops

    @head.setter
    def head(self, val: UaNodeHead):
        self._head = val
        self._value.head = val._val

    @event_notifier.setter
    def event_notifier(self, val: UaByte):
        self._event_notifier = val
        self._value.eventNotifier = val._val

    @contains_no_loops.setter
    def contains_no_loops(self, val: UaBoolean):
        self._contains_no_loops = val
        self._value.containsNoLoops = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaViewNode) : NULL\n"

        return ("(UaViewNode) :\n"
                + "\t" * (n + 1) + "head" + self._head.__str__(n + 1)
                + "\t" * (n + 1) + "event_notifier" + self._event_notifier.__str__(n + 1)
                + "\t" * (n + 1) + "contains_no_loops" + self._contains_no_loops.__str__(n + 1))
