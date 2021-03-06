# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from ua_consts_status_codes import UA_STATUSCODES
from ua_types_logger import *
from ua_types_parent import _ptr, _val, _is_null, _get_c_type, _is_ptr
from typing import Callable, Dict


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

    def __str__(self, n=None):
        if self._null:
            return "(aa_entry): NULL" + ("" if n is None else "\n")

        return ("(aa_entry) :\n"
                + "\t" * (1 if n is None else n+1) + "left " + self._left.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "right " + self._right.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "int " + self._int.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaNode +++++++++++++++++++++++
class UaNode(UaType):
    # TODO: add union members

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Node *"), is_pointer)
        else:
            super().__init__(ffi.new("UA_Node *"), _val(val), is_pointer)


# +++++++++++++++++++ UaCertificateVerification +++++++++++++++++++++++
class UaCertificateVerification(UaType):
    _verify_certificate = None
    _verify_application_uri = None
    _clear = None

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_CertificateVerification*")
            super().__init__(val=val, is_pointer=is_pointer)
            self._context = Void(val=val.context, is_pointer=True)
            self._verify_certificate = None
            self._verify_application_uri = None
            self._clear = None

        elif isinstance(val, UaType):
            val = ffi.cast("UA_CertificateVerification*", val._ptr)
            super().__init__(val=val, is_pointer=is_pointer)
            self._context = Void(val=val.context, is_pointer=True)
            self._verify_certificate = lambda a, b: UA_STATUSCODES.GOOD
            self._verify_application_uri = lambda a, b: UA_STATUSCODES.GOOD
            self._clear = lambda a: None
            # todo: raise exeption if neither nor

    def _update(self):
        self.__init__(val=self._ptr)

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
    def verify_certificate(self, val: Callable[[Void, UaByteString], UaStatusCode]):
        UaCertificateVerification._verify_certificate = val
        self._value.verifyCertificate = lib._python_wrapper_UA_CertificateVerification_verifyCertificate

    @verify_application_uri.setter
    def verify_application_uri(self, val: Callable[[Void, UaByteString, UaString], UaStatusCode]):
        UaCertificateVerification._verify_application_uri = val
        self._value.verifyApplicationURI = lib._python_wrapper_UA_SecurityPolicy_verifyApplicationURI

    @clear.setter
    def clear(self, val: Callable[[], None]):
        UaCertificateVerification._clear = val
        self._value.clear = lib._python_wrapper_UA_CertificateVerification_clear

    def __str__(self, n=None):
        if self._null:
            return "(UaCertificateVerification): NULL" + ("" if n is None else "\n")

        return ("(UaCertificateVerification) :\n"
                + "\t" * (1 if n is None else n+1) + "context " + self._context.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "verify_certificate " + self._verify_certificate.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "verify_application_uri " + self._verify_application_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "clear " + self._clear.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaNodestore +++++++++++++++++++++++
class UaNodestore(UaType):
    _clear = None
    _new_node = None
    _delete_node = None
    _get_node = None
    _release_node = None
    _get_node_copy = None
    _insert_node = None
    _replace_node = None
    _remove_node = None
    _get_reference_type_id = None
    _iterate = None

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_Nodestore*")
            super().__init__(val=val, is_pointer=is_pointer)
            self._context = Void(val=val.context, is_pointer=True)
            UaNodestore._clear = None
            UaNodestore._new_node = None
            UaNodestore._delete_node = None
            UaNodestore._get_node = None
            UaNodestore._release_node = None
            UaNodestore._get_node_copy = None
            UaNodestore._insert_node = None
            UaNodestore._replace_node = None
            UaNodestore._remove_node = None
            UaNodestore._get_reference_type_id = None
            UaNodestore._iterate = None

        elif isinstance(val, UaType):
            val = ffi.cast("UA_Nodestore*", val._ptr)
            super().__init__(val=val, is_pointer=is_pointer)
            self._context = Void(val=val.context, is_pointer=True)
            UaNodestore._clear = lambda a: None
            UaNodestore._new_node = lambda a, b: UaNode()
            UaNodestore._delete_node = lambda a, b: None
            UaNodestore._get_node = lambda a, b: UaNode()
            UaNodestore._release_node = lambda a, b: None
            UaNodestore._get_node_copy = lambda a, b, c: UA_STATUSCODES.GOOD
            UaNodestore._insert_node = lambda a, b, c: UA_STATUSCODES.GOOD
            UaNodestore._replace_node = lambda a, b: UA_STATUSCODES.GOOD
            UaNodestore._remove_node = lambda a, b: UA_STATUSCODES.GOOD
            UaNodestore._get_reference_type_id = lambda a, b: UaNodeId()
            UaNodestore._iterate = lambda a, b, c: None

    def _update(self):
        self.__init__(val=self._ptr)

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
    def clear(self, val: Callable[[Void], None]):
        self._clear = val
        self._value.clear = lib._python_wrapper_UA_Nodestore_clear

    @new_node.setter
    def new_node(self, val: Callable[[Void, UaNodeClass], UaNode]):
        self._new_node = val
        self._value.newNode = lib._python_wrapper_UA_Nodestore_newNode

    @delete_node.setter
    def delete_node(self, val: Callable[[Void, UaNodeId], None]):
        self._delete_node = val
        self._value.deleteNode = lib._python_wrapper_UA_Nodestore_deleteNode

    @get_node.setter
    def get_node(self, val: Callable[[Void, UaNodeId], UaNode]):
        self._get_node = val
        self._value.getNode = lib._python_wrapper_UA_Nodestore_getNode

    @release_node.setter
    def release_node(self, val: Callable[[Void, UaNode], None]):
        self._release_node = val
        self._value.releaseNode = lib._python_wrapper_UA_Nodestore_releaseNode

    @get_node_copy.setter
    def get_node_copy(self, val: Callable[[Void, UaNodeId, UaList], UaStatusCode]):
        self._get_node_copy = val
        self._value.getNodeCopy = lib._python_wrapper_UA_Nodestore_getNodeCopy

    @insert_node.setter
    def insert_node(self, val: Callable[[Void, UaNode, UaNodeId], UaStatusCode]):
        self._insert_node = val
        self._value.insertNode = lib._python_wrapper_UA_Nodestore_insertNode

    @replace_node.setter
    def replace_node(self, val: Callable[[Void, UaNode], UaStatusCode]):
        self._replace_node = val
        self._value.replaceNode = lib._python_wrapper_UA_Nodestore_replaceNode

    @remove_node.setter
    def remove_node(self, val: Callable[[Void, UaNodeId], UaStatusCode]):
        self._remove_node = val
        self._value.removeNode = lib._python_wrapper_UA_Nodestore_removeNode

    @get_reference_type_id.setter
    def get_reference_type_id(self, val: Callable[[Void, UaByte], UaNodeId]):
        self._get_reference_type_id = val
        self._value.getReferenceTypeId = lib._python_wrapper_UA_Nodestore_getReferenceTypeId

    @iterate.setter
    # todo: add UaNodeStoreVisitor instead of Any
    def iterate(self, val: Callable[[Void, Any, Void], None]):
        self._iterate = val
        self._value.iterate = lib._python_wrapper_UA_Nodestore_iterate

    def __str__(self, n=None):
        if self._null:
            return "(UaNodestore): NULL" + ("" if n is None else "\n")

        return ("(UaNodestore) :\n"
                + "\t" * (1 if n is None else n+1) + "context " + self._context.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "clear " + self._clear.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "new_node " + self._new_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "delete_node " + self._delete_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "get_node " + self._get_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "release_node " + self._release_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "get_node_copy " + self._get_node_copy.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "insert_node " + self._insert_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "replace_node " + self._replace_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "remove_node " + self._remove_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "get_reference_type_id " + self._get_reference_type_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "iterate " + self._iterate.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaAccessControl +++++++++++++++++++++++
class UaAccessControl(UaType):
    _clear = None
    _activate_session = None
    _close_session = None
    _get_user_rights_mask = None
    _get_user_access_level = None
    _get_user_executable = None
    _get_user_executable_on_object = None
    _allow_add_node = None
    _allow_add_reference = None
    _allow_delete_node = None
    _allow_delete_reference = None
    _allow_browse_node = None

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_AccessControl*")
            super().__init__(val=val, is_pointer=is_pointer)
            self._context = Void(val=val.context, is_pointer=True)
            UaAccessControl._clear = None
            self._user_token_policies_size = SizeT(val=val.userTokenPoliciesSize, is_pointer=False)
            self._user_token_policies = UaUserTokenPolicy(val=val.userTokenPolicies, is_pointer=True)
            UaAccessControl._activate_session = None
            UaAccessControl._close_session = None
            UaAccessControl._get_user_rights_mask = None
            UaAccessControl._get_user_access_level = None
            UaAccessControl._get_user_executable = None
            UaAccessControl._get_user_executable_on_object = None
            UaAccessControl._allow_add_node = None
            UaAccessControl._allow_add_reference = None
            UaAccessControl._allow_delete_node = None
            UaAccessControl._allow_delete_reference = None
            UaAccessControl._allow_browse_node = None
        if isinstance(val, UaType):
            val = ffi.cast("UA_AccessControl*", val._ptr)
            super().__init__(val=val, is_pointer=is_pointer)
            self._context = Void(val=val.context, is_pointer=True)
            UaAccessControl._clear = lambda a: None
            self._user_token_policies_size = SizeT(val=val.userTokenPoliciesSize, is_pointer=False)
            self._user_token_policies = UaUserTokenPolicy(val=val.userTokenPolicies, is_pointer=True)
            UaAccessControl._activate_session = lambda a, b, c, d, e, f, g: UA_STATUSCODES.GOOD
            UaAccessControl._close_session = lambda a, b, c, d: None
            UaAccessControl._get_user_rights_mask = lambda a, b, c, d, e, f: UaUInt32()
            UaAccessControl._get_user_access_level = lambda a, b, c, d, e, f: UaBoolean()
            UaAccessControl._get_user_executable = lambda a, b, c, d, e, f: UaBoolean()
            UaAccessControl._get_user_executable_on_object = lambda a, b, c, d, e, f, g, h: UaBoolean()
            UaAccessControl._allow_add_node = lambda a, b, c, d, e: UaBoolean()
            UaAccessControl._allow_add_reference = lambda a, b, c, d, e: UaBoolean()
            UaAccessControl._allow_delete_node = lambda a, b, c, d, e: UaBoolean()
            UaAccessControl._allow_delete_reference = lambda a, b, c, d, e: UaBoolean()
            UaAccessControl._allow_browse_node = lambda a, b, c, d, e, f: UaBoolean()

    def _update(self):
        self.__init__(val=self._ptr)

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
    def clear(self, val: Callable[['UaAccessControl'], None]):
        UaAccessControl._clear = val
        self._value.clear = lib._python_wrapper_UA_AccessControl_clear

    @user_token_policies_size.setter
    def user_token_policies_size(self, val: SizeT):
        self._user_token_policies_size = val
        self._value.userTokenPoliciesSize = val._val

    @user_token_policies.setter
    def user_token_policies(self, val: UaUserTokenPolicy):
        self._user_token_policies = val
        self._value.userTokenPolicies = val._ptr

    @activate_session.setter
    def activate_session(self, val: Callable[
        ['UaServer', 'UaAccessControl', UaEndpointDescription, UaByteString, UaNodeId, UaExtensionObject,
         UaList], UaStatusCode]):
        UaAccessControl._activate_session = val
        self._value.activateSession = lib._python_wrapper_UA_AccessControl_closeSession

    @close_session.setter
    def close_session(self, val: Callable[['UaServer', 'UaAccessControl', UaNodeId, Void], None]):
        UaAccessControl._close_session = val
        self._value.closeSession = lib._python_wrapper_UA_AccessControl_closeSession

    @get_user_rights_mask.setter
    def get_user_rights_mask(self,
                             val: Callable[['UaServer', 'UaAccessControl', UaNodeId, Void, UaNodeId, Void], UaUInt32]):
        UaAccessControl._get_user_rights_mask = val
        self._value.getUserRightsMask = lib._python_wrapper_UA_AccessControl_getUserRightsMask

    @get_user_access_level.setter
    def get_user_access_level(self,
                              val: Callable[['UaServer', 'UaAccessControl', UaNodeId, Void, UaNodeId, Void], UaByte]):
        UaAccessControl._get_user_access_level = val
        self._value.getUserAccessLevel = lib._python_wrapper_UA_AccessControl_getUserAccessLevel

    @get_user_executable.setter
    def get_user_executable(self,
                            val: Callable[['UaServer', 'UaAccessControl', UaNodeId, Void, UaNodeId, Void], UaBoolean]):
        UaAccessControl._get_user_executable = val
        self._value.getUserExecutable = lib._python_wrapper_UA_AccessControl_getUserExecutable

    @get_user_executable_on_object.setter
    def get_user_executable_on_object(self, val: Callable[
        ['UaServer', 'UaAccessControl', UaNodeId, Void, UaNodeId, Void, UaNodeId, Void], UaBoolean]):
        UaAccessControl._get_user_executable_on_object = val
        self._value.getUserExecutableOnObject = lib._python_wrapper_UA_AccessControl_getUserExecutableOnObject

    @allow_add_node.setter
    def allow_add_node(self, val: Callable[['UaServer', 'UaAccessControl', UaNodeId, Void, UaAddNodesItem], UaBoolean]):
        UaAccessControl._allow_add_node = val
        self._value.allowAddNode = lib._python_wrapper_UA_AccessControl_getUserExecutableOnObject

    @allow_add_reference.setter
    def allow_add_reference(self, val: Callable[
        ['UaServer', 'UaAccessControl', UaNodeId, Void, UaAddReferencesItem], UaBoolean]):
        UaAccessControl._allow_add_reference = val
        self._value.allowAddReference = lib._python_wrapper_UA_AccessControl_allowAddNode

    @allow_delete_node.setter
    def allow_delete_node(self,
                          val: Callable[['UaServer', 'UaAccessControl', UaNodeId, Void, UaDeleteNodesItem], UaBoolean]):
        UaAccessControl._allow_delete_node = val
        self._value.allowDeleteNode = lib._python_wrapper_UA_AccessControl_allowDeleteNode

    @allow_delete_reference.setter
    def allow_delete_reference(self, val: Callable[
        ['UaServer', 'UaAccessControl', UaNodeId, Void, UaDeleteReferencesItem], UaBoolean]):
        UaAccessControl._allow_delete_reference = val
        self._value.allowDeleteReference = lib._python_wrapper_UA_AccessControl_allowDeleteReference

    @allow_browse_node.setter
    def allow_browse_node(self,
                          val: Callable[['UaServer', 'UaAccessControl', UaNodeId, Void, UaNodeId, Void], UaBoolean]):
        UaAccessControl._allow_browse_node = val
        self._value.allowBrowseNode = lib._python_wrapper_UA_AccessControl_allowBrowseNode

    def __str__(self, n=None):
        if self._null:
            return "(UaAccessControl): NULL" + ("" if n is None else "\n")

        return ("(UaAccessControl) :\n"
                + "\t" * (1 if n is None else n+1) + "context " + self._context.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "clear " + self._clear.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_token_policies_size " + self._user_token_policies_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "user_token_policies " + self._user_token_policies.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "activate_session " + self._activate_session.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "close_session " + self._close_session.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "get_user_rights_mask " + self._get_user_rights_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "get_user_access_level " + self._get_user_access_level.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "get_user_executable " + self._get_user_executable.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "get_user_executable_on_object " + self._get_user_executable_on_object.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "allow_add_node " + self._allow_add_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "allow_add_reference " + self._allow_add_reference.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "allow_delete_node " + self._allow_delete_node.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "allow_delete_reference " + self._allow_delete_reference.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "allow_browse_node " + self._allow_browse_node.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaGlobalNodeLifecycle +++++++++++++++++++++++
class UaGlobalNodeLifecycle(UaType):
    _constructor = None
    _destructor = None
    _create_optional_child = None
    _generate_child_node_id = None

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_GlobalNodeLifecycle*")
            super().__init__(val=val, is_pointer=is_pointer)
            UaGlobalNodeLifecycle._constructor = None
            UaGlobalNodeLifecycle._destructor = None
            UaGlobalNodeLifecycle._create_optional_child = None
            UaGlobalNodeLifecycle._generate_child_node_id = None

        if isinstance(val, UaType):
            val = ffi.cast("UA_GlobalNodeLifecycle*", val._ptr)
            super().__init__(val=val, is_pointer=is_pointer)
            UaGlobalNodeLifecycle._constructor = lambda a, b, c, d, e: UA_STATUSCODES.GOOD
            UaGlobalNodeLifecycle._destructor = lambda a, b, c, d, e: None
            UaGlobalNodeLifecycle._create_optional_child = lambda a, b, c, d, e, f: UaBoolean()
            UaGlobalNodeLifecycle._generate_child_node_id = lambda a, b, c, d, e, f, g: UA_STATUSCODES.GOOD

    # todo: else -> exception

    def _update(self):
        self.__init__(val=self._ptr)

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
        def constructor(self, val: Callable[['UaServer', UaNodeId, Void, UaNodeId, UaList], UaStatusCode]):
            UaGlobalNodeLifecycle._constructor = val
            self._value.constructor = lib._python_wrapper_UA_GlobalNodeLifecycle_constructor

        @destructor.setter
        def destructor(self, val: Callable[['UaServer', UaNodeId, Void, UaNodeId, Void], None]):
            UaGlobalNodeLifecycle._destructor = val
            self._value.destructor = lib._python_wrapper_UA_GlobalNodeLifecycle_destructor

        @create_optional_child.setter
        def create_optional_child(self, val: Callable[
            ['UaServer', UaNodeId, Void, UaNodeId, UaNodeId, UaNodeId], UaStatusCode]):
            UaGlobalNodeLifecycle._create_optional_child = val
            self._value.createOptionalChild = lib._python_wrapper_UA_GlobalNodeLifecycle_createOptionalChild

        @generate_child_node_id.setter
        def generate_child_node_id(self, val: Callable[
            ['UaServer', UaNodeId, Void, UaNodeId, UaNodeId, UaNodeId, UaNodeId], UaStatusCode]):
            UaGlobalNodeLifecycle._generate_child_node_id = val
            self._value.generateChildNodeId = lib._python_wrapper_UA_GlobalNodeLifecycle_generateChildNodeId

        def __str__(self, n=None):
            if self._null:
                return "(UaGlobalNodeLifecycle): NULL" + ("" if n is None else "\n")

            return ("(UaGlobalNodeLifecycle) :\n"
                    + "\t" * (1 if n is None else n+1) + "constructor " + self._constructor.__str__(1 if n is None else n+1)
                    + "\t" * (1 if n is None else n+1) + "destructor " + self._destructor.__str__(1 if n is None else n+1)
                    + "\t" * (1 if n is None else n+1) + "create_optional_child " + self._create_optional_child.__str__(1 if n is None else n+1)
                    + "\t" * (1 if n is None else n+1) + "generate_child_node_id " + self._generate_child_node_id.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaServerNetworkLayer +++++++++++++++++++++++
class UaServerNetworkLayer(UaType):
    _start = None
    _listen = None
    _stop = None
    _clear = None

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ServerNetworkLayer*")
            super().__init__(val=val, is_pointer=is_pointer)
            self._handle = Void(val=val.handle, is_pointer=True)
            self._statistics = UaNetworkStatistics(val=val.statistics, is_pointer=True)
            self._discovery_url = UaString(val=val.discoveryUrl, is_pointer=False)
            self._local_connection_config = UaConnectionConfig(val=val.localConnectionConfig, is_pointer=False)
            self._start = None
            self._listen = None
            self._stop = None
            self._clear = None
        if isinstance(val, UaType):
            val = ffi.cast("UA_ServerNetworkLayer*", val._ptr)
            super().__init__(val=val, is_pointer=is_pointer)
            self._handle = Void(val=val.handle, is_pointer=True)
            self._statistics = UaNetworkStatistics(val=val.statistics, is_pointer=True)
            self._discovery_url = UaString(val=val.discoveryUrl, is_pointer=False)
            self._local_connection_config = UaConnectionConfig(val=val.localConnectionConfig, is_pointer=False)
            self._start = lambda a, b, c: UA_STATUSCODES.GOOD
            self._listen = lambda a, b, c: UA_STATUSCODES.GOOD
            self._stop = lambda a, b: None
            self._clear = lambda a: None

    def _update(self):
        self.__init__(val=self._ptr)

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
    def start(self, val: Callable[['UaServerNetworkLayer', UaLogger], UaStatusCode]):
        UaServerNetworkLayer._start = val
        self._value.start = lib._python_wrapper_UA_ServerNetworkLayer_start

    @listen.setter
    def listen(self, val: Callable[['UaServerNetworkLayer', 'UaServer'], UaStatusCode]):
        UaServerNetworkLayer._listen = val
        self._value.listen = lib._python_wrapper_UA_ServerNetworkLayer_listen

    @stop.setter
    def stop(self, val: Callable[['UaServerNetworkLayer', 'UaServer'], None]):
        UaServerNetworkLayer._stop = val
        self._value.stop = lib._python_wrapper_UA_ServerNetworkLayer_stop

    @clear.setter
    def clear(self, val: Callable[['UaServerNetworkLayer'], None]):
        UaServerNetworkLayer._clear = val
        self._value.clear = lib._python_wrapper_UA_ServerNetworkLayer_clear

    def __str__(self, n=None):
        if self._null:
            return "(UaServerNetworkLayer): NULL" + ("" if n is None else "\n")

        return ("(UaServerNetworkLayer) :\n"
                + "\t" * (1 if n is None else n+1) + "handle " + self._handle.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "statistics " + self._statistics.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "discovery_url " + self._discovery_url.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "local_connection_config " + self._local_connection_config.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "start " + self._start.__str__()
                + "\t" * (1 if n is None else n+1) + "listen " + self._listen.__str__()
                + "\t" * (1 if n is None else n+1) + "stop " + self._stop.__str__()
                + "\t" * (1 if n is None else n+1) + "clear " + self._clear.__str__())

    # +++++++++++++++++++ UaSecurityPolicy +++++++++++++++++++++++


class UaSecurityPolicy(UaType):
    _update_certificate_and_private_key = None
    _clear = None

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_SecurityPolicy*")
            super().__init__(val=val, is_pointer=is_pointer)
            self._policy_context = Void(val=val.policyContext, is_pointer=True)
            self._policy_uri = UaByteString(val=val.policyUri, is_pointer=False)
            self._local_certificate = UaByteString(val=val.localCertificate, is_pointer=False)
            self._asymmetric_module = UaSecurityPolicyAsymmetricModule(val=val.asymmetricModule, is_pointer=False)
            self._symmetric_module = UaSecurityPolicySymmetricModule(val=val.symmetricModule, is_pointer=False)
            self._certificate_signing_algorithm = UaSecurityPolicySignatureAlgorithm(
                val=val.certificateSigningAlgorithm, is_pointer=False)
            self._channel_module = UaSecurityPolicyChannelModule(val=val.channelModule, is_pointer=False)
            self._logger = UaLogger(val=val.logger, is_pointer=True)
            self._update_certificate_and_private_key = None
            self._clear = None
        if isinstance(val, UaType):
            val = ffi.cast("UA_SecurityPolicy*", val._ptr)
            super().__init__(val=val, is_pointer=is_pointer)
            self._policy_context = Void(val=val.policyContext, is_pointer=True)
            self._policy_uri = UaByteString(val=val.policyUri, is_pointer=False)
            self._local_certificate = UaByteString(val=val.localCertificate, is_pointer=False)
            self._asymmetric_module = UaSecurityPolicyAsymmetricModule(val=val.asymmetricModule, is_pointer=False)
            self._symmetric_module = UaSecurityPolicySymmetricModule(val=val.symmetricModule, is_pointer=False)
            self._certificate_signing_algorithm = UaSecurityPolicySignatureAlgorithm(
                val=val.certificateSigningAlgorithm, is_pointer=False)
            self._channel_module = UaSecurityPolicyChannelModule(val=val.channelModule, is_pointer=False)
            self._logger = UaLogger(val=val.logger, is_pointer=True)
            self._update_certificate_and_private_key = lambda a, b, c: UA_STATUSCODES.GOOD
            self._clear = lambda a: None

    def _update(self):
        self.__init__(val=self._ptr)

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
    def update_certificate_and_private_key(self, val: Callable[
        ['UaSecurityPolicy', UaByteString, UaByteString], UaStatusCode]):
        UaSecurityPolicy._update_certificate_and_private_key = val
        self._value.updateCertificateAndPrivateKey = lib._python_wrapper_UA_SecurityPolicy_updateCertificateAndPrivateKey

    @clear.setter
    def clear(self, val: Callable[['UaSecurityPolicy'], None]):
        UaSecurityPolicy._clear = val
        self._value.clear = lib._python_wrapper_UA_SecurityPolicy_clear

    def __str__(self, n=None):
        if self._null:
            return "(UaSecurityPolicy): NULL" + ("" if n is None else "\n")

        return ("(UaSecurityPolicy) :\n"
                + "\t" * (1 if n is None else n+1) + "policy_context " + self._policy_context.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "policy_uri " + self._policy_uri.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "local_certificate " + self._local_certificate.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "asymmetric_module " + self._asymmetric_module.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "symmetric_module " + self._symmetric_module.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "certificate_signing_algorithm " + self._certificate_signing_algorithm.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "channel_module " + self._channel_module.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "logger " + self._logger.__str__(1 if n is None else n+1)
                + "\t" * (
                        n + 1) + "update_certificate_and_private_key " + self._update_certificate_and_private_key.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "clear " + self._clear.__str__(1 if n is None else n+1))


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

    def __str__(self, n=None):
        if self._null:
            return "(UaConnectionConfig): NULL" + ("" if n is None else "\n")

        return ("(UaConnectionConfig) :\n"
                + "\t" * (1 if n is None else n+1) + "protocol_version " + self._protocol_version.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "recv_buffer_size " + self._recv_buffer_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "send_buffer_size " + self._send_buffer_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "local_max_message_size " + self._local_max_message_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "remote_max_message_size " + self._remote_max_message_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "local_max_chunk_count " + self._local_max_chunk_count.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "remote_max_chunk_count " + self._remote_max_chunk_count.__str__(1 if n is None else n+1))

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

    def __str__(self, n=None):
        if self._null:
            return "(UaSecurityPolicyAsymmetricModule): NULL" + ("" if n is None else "\n")

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

    def __str__(self, n=None):
        if self._null:
            return "(UaSecurityPolicySymmetricModule): NULL" + ("" if n is None else "\n")

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

    def __str__(self, n=None):
        if self._null:
            return "(UaSecurityPolicyChannelModule): NULL" + ("" if n is None else "\n")

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

    def __str__(self, n=None):
        if self._null:
            return "(UaSecurityPolicySignatureAlgorithm): NULL" + ("" if n is None else "\n")

        return ("(UaSecurityPolicySignatureAlgorithm) :\n")


# +++++++++++++++++++ UaNodeTypeLifecycle +++++++++++++++++++++++
class UaNodeTypeLifecycle(UaType):
    _constructor = None
    _destructor = None

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NodeTypeLifecycle*")
            super().__init__(val=val, is_pointer=is_pointer)
            self._constructor = None
            self._destructor = None
        if isinstance(val, UaType):
            val = ffi.cast("UA_NodeTypeLifecycle*", val._ptr)
            super().__init__(val=val, is_pointer=is_pointer)
            self._constructor = lambda a, b, c, d, e, f, g: UA_STATUSCODES.GOOD
            self._destructor = lambda a, b, c, d, e, f, g: UA_STATUSCODES.GOOD

    def _update(self):
        self.__init__(val=self._ptr)

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
    def constructor(self, val: Callable[['UaServer', UaNodeId, Void, UaNodeId, Void, UaNodeId, UaList], UaStatusCode]):
        UaNodeTypeLifecycle._constructor = val
        self._value.constructor = lib._python_wrapper_UA_NodeTypeLifecycle_constructor

    @destructor.setter
    def destructor(self, val: Callable[['UaServer', UaNodeId, Void, UaNodeId, Void, UaNodeId, UaList], UaStatusCode]):
        UaNodeTypeLifecycle._destructor = val
        self._value.destructor = lib._python_wrapper_UA_NodeTypeLifecycle_destructor

    def __str__(self, n=None):
        if self._null:
            return "(UaNodeTypeLifecycle): NULL" + ("" if n is None else "\n")

        return ("(UaNodeTypeLifecycle) :\n"
                + "\t" * (1 if n is None else n+1) + "constructor " + self._constructor.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "destructor " + self._destructor.__str__(1 if n is None else n+1))


# # Only one implementation at a time
# class UaNodeTypeLifecycle(UaType):
#     @staticmethod
#     def _constructor_callback(a, b, c, d, e, f, g): return UA_STATUSCODES.GOOD
#     @staticmethod
#     def _destructor_callback(a, b, c, d, e, f, g): pass
#
#     def __init__(self, val=None, is_pointer=False):
#         if val is None:
#             super().__init__(val=ffi.new("UA_NodeTypeLifecycle*"), is_pointer=is_pointer)
#             self._uses_python_constructor_callback = True
#             self._uses_python_destructor_callback = True
#             self._value.constructor = lib.python_wrapper_UA_NodeTypeLifecycle_constructor
#             self._value.destructor = lib.python_wrapper_UA_NodeTypeLifecycle_destructor
#         else:
#             super().__init__(val=val, is_pointer=is_pointer)
#             self._uses_python_constructor_callback = False
#             self._uses_python_destructor_callback = False
#
#     @property
#     def constructor(self):
#         return UaNodeTypeLifecycle._constructor_callback
#
#     @property
#     def destructor(self):
#         return UaNodeTypeLifecycle._destructor_callback
#
#     @constructor.setter
#     def constructor(self, val: Callable[
#         ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNodeId, Void], UaStatusCode]):
#         UaNodeTypeLifecycle._constructor_callback = val
#         self._value.constructor = lib.python_wrapper_UA_NodeTypeLifecycle_constructor
#         self._uses_python_constructor_callback = True
#
#     @destructor.setter
#     def destructor(self, val: Callable[
#         ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNodeId, Void], None]):
#         UaNodeTypeLifecycle._destructor_callback = val
#         self._value.write = lib.python_wrapper_UA_NodeTypeLifecycle_destructor
#         self._uses_python_destructor_callback = True

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

    def __str__(self, n=None):
        if self._null:
            return "(UaNodeReferenceKind): NULL" + ("" if n is None else "\n")

        return ("(UaNodeReferenceKind) :\n"
                + "\t" * (1 if n is None else n+1) + "id_tree_root " + self._id_tree_root.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "name_tree_root " + self._name_tree_root.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "reference_type_index " + self._reference_type_index.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_inverse " + self._is_inverse.__str__(1 if n is None else n+1))


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

    def __str__(self, n=None):
        if self._null:
            return "(UaNodeHead): NULL" + ("" if n is None else "\n")

        return ("(UaNodeHead) :\n"
                + "\t" * (1 if n is None else n+1) + "node_id " + self._node_id.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "node_class " + self._node_class.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "browse_name " + self._browse_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "display_name " + self._display_name.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "description " + self._description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "write_mask " + self._write_mask.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "references_size " + self._references_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "references " + self._references.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "context " + self._context.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "constructed " + self._constructed.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaMethodNode +++++++++++++++++++++++
class UaMethodNode(UaType):
    _callbacks_dict: Dict[str, any] = dict()

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_MethodNode*")
            super().__init__(val=val, is_pointer=is_pointer)
            self._head = UaNodeHead(val=val.head, is_pointer=False)
            self._executable = UaBoolean(val=val.executable, is_pointer=False)
            self._method = None
        if isinstance(val, UaType):
            val = ffi.cast("UA_MethodNode*", val._ptr)
            super().__init__(val=val, is_pointer=is_pointer)
            self._head = UaNodeHead(val=val.head, is_pointer=False)
            self._executable = UaBoolean(val=val.executable, is_pointer=False)
            self._method = lambda a, b, c, d, e, f, g, h, i, j, k: UA_STATUSCODES.GOOD

    def _update(self):
        self.__init__(val=self._ptr)

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
    def method(self, val: Callable[
        ['UaServer', UaNodeId, Void, UaNodeId, Void, UaNodeId, Void, UaList,
         UaList], UaStatusCode]):
        self._method = val
        UaMethodNode._callbacks_dict[str(self)] = val
        self._value.method = lib._python_wrapper_UA_MethodCallback

    def __str__(self, n=None):
        if self._null:
            return "(UaMethodNode): NULL" + ("" if n is None else "\n")

        return ("(UaMethodNode) :\n"
                + "\t" * (1 if n is None else n+1) + "head " + self._head.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "executable " + self._executable.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "method " + self._method.__str__(1 if n is None else n+1))


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

    def __str__(self, n=None):
        if self._null:
            return "(UaObjectNode): NULL" + ("" if n is None else "\n")

        return ("(UaObjectNode) :\n"
                + "\t" * (1 if n is None else n+1) + "head " + self._head.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "event_notifier " + self._event_notifier.__str__(1 if n is None else n+1))


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

    def __str__(self, n=None):
        if self._null:
            return "(UaObjectTypeNode): NULL" + ("" if n is None else "\n")

        return ("(UaObjectTypeNode) :\n"
                + "\t" * (1 if n is None else n+1) + "head " + self._head.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_abstract " + self._is_abstract.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "lifecycle " + self._lifecycle.__str__(1 if n is None else n+1))


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

    def __str__(self, n=None):
        if self._null:
            return "(UaReferenceTypeSet): NULL" + ("" if n is None else "\n")

        return ("(UaReferenceTypeSet) :\n"
                + "\t" * (1 if n is None else n+1) + "bits " + self._bits.__str__(1 if n is None else n+1))


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

    def __str__(self, n=None):
        if self._null:
            return "(UaDataTypeNode): NULL" + ("" if n is None else "\n")

        return ("(UaDataTypeNode) :\n"
                + "\t" * (1 if n is None else n+1) + "head " + self._head.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "is_abstract " + self._is_abstract.__str__(1 if n is None else n+1))


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

    def __str__(self, n=None):
        if self._null:
            return "(UaViewNode): NULL" + ("" if n is None else "\n")

        return ("(UaViewNode) :\n"
                + "\t" * (1 if n is None else n+1) + "head " + self._head.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "event_notifier " + self._event_notifier.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "contains_no_loops " + self._contains_no_loops.__str__(1 if n is None else n+1))


# +++++++++++++++++++ UaServerConfig +++++++++++++++++++++++
class UaServerConfig(UaType):
    r"""

    Warning:
        Function pointers that are part of classes that are used by UaServerConfig make use of a workaround in order to
        work with the CFFI limitation of only being able to attach a single python implementation to a c function
        which has been defined with 'extern "python"'. While for some other areas it is possible to smuggle functions
        which have been created by the API user in e.g. via a dictionary or a void* argument user_data, this is not
        possible for most of the functions used in this module's classes. The way it is handled (solved would be too
        strong of a word) currently is that per function pointer definition only a single python function can exist
        at the same time.

    Example:
        the class `UaNodeTypeLifecycle` has two function pointer based fields, a constructor and a destructor functions.
        The following extern "Python" definitions have been added to `api/definitions/nodestore`:

    .. code-block:: c

        extern "Python" UA_StatusCode _python_wrapper_UA_NodeTypeLifecycle_constructor(UA_Server *server,
                                     const UA_NodeId *sessionId, void *sessionContext,
                                     const UA_NodeId *typeNodeId, void *typeNodeContext,
                                     const UA_NodeId *nodeId, void **nodeContext);
        extern "Python" void _python_wrapper_UA_NodeTypeLifecycle_destructor(UA_Server *server,
                                const UA_NodeId *sessionId, void *sessionContext,
                                const UA_NodeId *typeNodeId, void *typeNodeContext,
                                const UA_NodeId *nodeId, void **nodeContext);

    UaNodeTypeLifecycle contains one static python implementation for each of those two functions. When using the setter
    for any of the two function fields the passed python function pointer will be stored in either of the static
    variables `_constructor` or `_destructor` on the python side and on the c side of things one of the static
    functions. `lib._python_wrapper_UA_NodeTypeLifecycle_constructor` or
    `_python_wrapper_UA_NodeTypeLifecycle_destructor` will be registered. If one of these functions is called by
    open62541, it will call the corresponding `_constructor` or `_destructor` function. Each time a new
    `UaNodeTypeLifecycle` is created via it's `__init__` function or if the setter for the function pointers are being
    called the old global values will be deleted. All instances of `UaNodeTypeLifecycle` which were created via wrappy(o6)
    rather than being retrieved from a sever will therefore have the same functions attached to them.

    .. code-block:: python

        class UaNodeTypeLifecycle(UaType):
        # the python functions are stored in these global variables
        _constructor = None
        _destructor = None

        # static python methods which call the globally stored python functions
        @staticmethod
        @ffi.def_extern()
        def _python_wrapper_UA_NodeTypeLifecycle_constructor(server, session_id, session_context, type_node_id,
                                                             type_node_context, node_id, node_context):

            return UaNodeTypeLifecycle._constructor(server,
                                                    UaNodeId(val=session_id, is_pointer=True),
                                                    Void(val=session_context, is_pointer=True),
                                                    UaNodeId(val=type_node_id, is_pointer=True),
                                                    Void(val=type_node_context, is_pointer=True),
                                                    UaNodeId(val=node_id, is_pointer=True),
                                                    UaList(val=node_context))

        @staticmethod
        @ffi.def_extern()
        def _python_wrapper_UA_NodeTypeLifecycle_destructor(server, session_id, session_context, type_node_id,
                                                            type_node_context, node_id, node_context):

            UaNodeTypeLifecycle._destructor(server,
                                            UaNodeId(val=session_id, is_pointer=True),
                                            Void(val=session_context, is_pointer=True),
                                            UaNodeId(val=type_node_id, is_pointer=True),
                                            Void(val=type_node_context, is_pointer=True),
                                            UaNodeId(val=node_id, is_pointer=True),
                                            UaList(val=node_context))

        def __init__(self, val=None, is_pointer=False):
            if val is None:
                val = ffi.new("UA_NodeTypeLifecycle*")
                super().__init__(val=val, is_pointer=is_pointer)
                self._constructor = None
                self._destructor = None
            if isinstance(val, UaType):
                val = ffi.cast("UA_NodeTypeLifecycle*", val._ptr)
                super().__init__(val=val, is_pointer=is_pointer)
                # makeshift functions are stored in the global variables if the `UaNodeTypeLifecycle` instance was created
                # via an existing c pointer/struct
                self._constructor = lambda a, b, c, d, e, f, g: UA_STATUSCODES.GOOD
                self._destructor = lambda a, b, c, d, e, f, g: UA_STATUSCODES.GOOD

        def _update(self):
            self.__init__(val=self._ptr)

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

        # the setters register the passed functions in the global variables and register the static functions that call
        # them in c/open62541
        @constructor.setter
        def constructor(self, val: Callable[['UaServer', UaNodeId, Void, UaNodeId, Void, UaNodeId, UaList], UaStatusCode]):
            UaNodeTypeLifecycle._constructor = val
            self._value.constructor = lib._python_wrapper_UA_NodeTypeLifecycle_constructor

        @destructor.setter
        def destructor(self, val: Callable[['UaServer', UaNodeId, Void, UaNodeId, Void, UaNodeId, UaList], UaStatusCode]):
            UaNodeTypeLifecycle._destructor = val
            self._value.destructor = lib._python_wrapper_UA_NodeTypeLifecycle_destructor

        def __str__(self, n=None):
            if self._null:
                return "(UaNodeTypeLifecycle): NULL" + ("" if n is None else "\n")

            return ("(UaNodeTypeLifecycle) :\n"
                    + "\t" * (1 if n is None else n+1) + "constructor " + self._constructor.__str__(1 if n is None else n+1)
                    + "\t" * (1 if n is None else n+1) + "destructor " + self._destructor.__str__(1 if n is None else n+1))

    Addressing this issue is all but trivial. CFFI offers a way to dynamically create function pointers at runtime
    via the deprecated `Callbacks (old style)` approach but heavily urges developers not to use it as it supposedly
    can be abused for code injection, is not stable on certain systems and can crash in multi threaded programs (see
    https://cffi.readthedocs.io/en/latest/using.html#callbacks-old-style). Therefore didn't further pursue this
    possibility.

    note:
        A possibility which could be further explored but which would still would leave a bitter taste would be to
        implement a ring buffer for each function pointer type: Instead of creating a single `extern "python"` function,
        wrappy(o6)'s make script could ask users to configure how many function pointers per type they would like to be
        able to use in parallel. The make script could then generate files containing the `extern "python"`functions and
        define as many per type (e.g. and e.g. adding incrementing numbers as suffix) as configured by the user and could
        also create matching python functions with CFFI's `@ffi.def_extern()` decorator. Each `@ffi.def_extern()` would
        need to know where to find it's implementation which has been defined by the API user. The wrapper functions and
        the implementations could for example be stored in tuples in a ring buffer. Each time a function is registered,
        the current tuple would need to get updated and once the last available tuple has been reached wrappy(o6) would
        need to start overwriting the oldest entries again. As mentioned, this approach would still be far from perfect
        as it would require the user to know upfront how many function pointer of which type they want to be able to use
        in parallel. Not only would it be a hassle to configure it, but it would also lead to problems if the user's
        requirements change. This would require a recompilation and e.g. a restart of a server.
    """

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ServerConfig*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ServerConfig*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._logger = UaLogger(val=val.logger, is_pointer=False)
            self._build_info = UaBuildInfo(val=val.buildInfo, is_pointer=False)
            self._application_description = UaApplicationDescription(val=val.applicationDescription, is_pointer=False)
            self._server_certificate = UaByteString(val=val.serverCertificate, is_pointer=False)
            self._shutdown_delay = UaDouble(val=val.shutdownDelay, is_pointer=False)
            self._verify_request_timestamp = UaRuleHandling(val=val.verifyRequestTimestamp, is_pointer=False)
            self._allow_empty_variables = UaRuleHandling(val=val.allowEmptyVariables, is_pointer=False)
            self._custom_data_types = UaDataTypeArray(val=val.customDataTypes, is_pointer=True)
            self._network_layers_size = SizeT(val=val.networkLayersSize, is_pointer=False)
            self._network_layers = UaServerNetworkLayer(val=val.networkLayers, is_pointer=True)
            self._custom_hostname = UaString(val=val.customHostname, is_pointer=False)
            self._security_policies_size = SizeT(val=val.securityPoliciesSize, is_pointer=False)
            self._security_policies = UaSecurityPolicy(val=val.securityPolicies, is_pointer=True)
            self._endpoints_size = SizeT(val=val.endpointsSize, is_pointer=False)
            self._endpoints = UaEndpointDescription(val=val.endpoints, is_pointer=True)
            self._security_policy_none_discovery_only = UaBoolean(val=val.securityPolicyNoneDiscoveryOnly,
                                                                  is_pointer=False)
            self._node_lifecycle = UaGlobalNodeLifecycle(val=val.nodeLifecycle, is_pointer=False)
            self._access_control = UaAccessControl(val=val.accessControl, is_pointer=False)
            self._nodestore = UaNodestore(val=val.nodestore, is_pointer=False)
            self._certificate_verification = UaCertificateVerification(val=val.certificateVerification,
                                                                       is_pointer=False)
            self._max_secure_channels = UaUInt16(val=val.maxSecureChannels, is_pointer=False)
            self._max_security_token_lifetime = UaUInt32(val=val.maxSecurityTokenLifetime, is_pointer=False)
            self._max_sessions = UaUInt16(val=val.maxSessions, is_pointer=False)
            self._max_session_timeout = UaDouble(val=val.maxSessionTimeout, is_pointer=False)
            self._max_nodes_per_read = UaUInt32(val=val.maxNodesPerRead, is_pointer=False)
            self._max_nodes_per_write = UaUInt32(val=val.maxNodesPerWrite, is_pointer=False)
            self._max_nodes_per_method_call = UaUInt32(val=val.maxNodesPerMethodCall, is_pointer=False)
            self._max_nodes_per_browse = UaUInt32(val=val.maxNodesPerBrowse, is_pointer=False)
            self._max_nodes_per_register_nodes = UaUInt32(val=val.maxNodesPerRegisterNodes, is_pointer=False)
            self._max_nodes_per_translate_browse_paths_to_node_ids = UaUInt32(
                val=val.maxNodesPerTranslateBrowsePathsToNodeIds, is_pointer=False)
            self._max_nodes_per_node_management = UaUInt32(val=val.maxNodesPerNodeManagement, is_pointer=False)
            self._max_monitored_items_per_call = UaUInt32(val=val.maxMonitoredItemsPerCall, is_pointer=False)
            self._max_references_per_node = UaUInt32(val=val.maxReferencesPerNode, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ServerConfig")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._logger._value[0] = _val(val.logger)
            self._build_info._value[0] = _val(val.buildInfo)
            self._application_description._value[0] = _val(val.applicationDescription)
            self._server_certificate._value[0] = _val(val.serverCertificate)
            self._shutdown_delay._value[0] = _val(val.shutdownDelay)
            self._verify_request_timestamp._value[0] = _val(val.verifyRequestTimestamp)
            self._allow_empty_variables._value[0] = _val(val.allowEmptyVariables)
            self._custom_data_types._value = val.customDataTypes
            self._network_layers_size._value[0] = _val(val.networkLayersSize)
            self._network_layers._value = val.networkLayers
            self._custom_hostname._value[0] = _val(val.customHostname)
            self._security_policies_size._value[0] = _val(val.securityPoliciesSize)
            self._security_policies._value = val.securityPolicies
            self._endpoints_size._value[0] = _val(val.endpointsSize)
            self._endpoints._value = val.endpoints
            self._security_policy_none_discovery_only._value[0] = _val(val.securityPolicyNoneDiscoveryOnly)
            self._node_lifecycle._value[0] = _val(val.nodeLifecycle)
            self._access_control._value[0] = _val(val.accessControl)
            self._nodestore._value[0] = _val(val.nodestore)
            self._certificate_verification._value[0] = _val(val.certificateVerification)
            self._max_secure_channels._value[0] = _val(val.maxSecureChannels)
            self._max_security_token_lifetime._value[0] = _val(val.maxSecurityTokenLifetime)
            self._max_sessions._value[0] = _val(val.maxSessions)
            self._max_session_timeout._value[0] = _val(val.maxSessionTimeout)
            self._max_nodes_per_read._value[0] = _val(val.maxNodesPerRead)
            self._max_nodes_per_write._value[0] = _val(val.maxNodesPerWrite)
            self._max_nodes_per_method_call._value[0] = _val(val.maxNodesPerMethodCall)
            self._max_nodes_per_browse._value[0] = _val(val.maxNodesPerBrowse)
            self._max_nodes_per_register_nodes._value[0] = _val(val.maxNodesPerRegisterNodes)
            self._max_nodes_per_translate_browse_paths_to_node_ids._value[0] = _val(
                val.maxNodesPerTranslateBrowsePathsToNodeIds)
            self._max_nodes_per_node_management._value[0] = _val(val.maxNodesPerNodeManagement)
            self._max_monitored_items_per_call._value[0] = _val(val.maxMonitoredItemsPerCall)
            self._max_references_per_node._value[0] = _val(val.maxReferencesPerNode)

    @property
    def logger(self):
        if self._null:
            return None
        else:
            return self._logger

    @property
    def build_info(self):
        if self._null:
            return None
        else:
            return self._build_info

    @property
    def application_description(self):
        if self._null:
            return None
        else:
            return self._application_description

    @property
    def server_certificate(self):
        if self._null:
            return None
        else:
            return self._server_certificate

    @property
    def shutdown_delay(self):
        if self._null:
            return None
        else:
            return self._shutdown_delay

    @property
    def verify_request_timestamp(self):
        if self._null:
            return None
        else:
            return self._verify_request_timestamp

    @property
    def allow_empty_variables(self):
        if self._null:
            return None
        else:
            return self._allow_empty_variables

    @property
    def custom_data_types(self):
        if self._null:
            return None
        else:
            return self._custom_data_types

    @property
    def network_layers_size(self):
        if self._null:
            return None
        else:
            return self._network_layers_size

    @property
    def network_layers(self):
        if self._null:
            return None
        else:
            return self._network_layers

    @property
    def custom_hostname(self):
        if self._null:
            return None
        else:
            return self._custom_hostname

    @property
    def security_policies_size(self):
        if self._null:
            return None
        else:
            return self._security_policies_size

    @property
    def security_policies(self):
        if self._null:
            return None
        else:
            return self._security_policies

    @property
    def endpoints_size(self):
        if self._null:
            return None
        else:
            return self._endpoints_size

    @property
    def endpoints(self):
        if self._null:
            return None
        else:
            return self._endpoints

    @property
    def security_policy_none_discovery_only(self):
        if self._null:
            return None
        else:
            return self._security_policy_none_discovery_only

    @property
    def node_lifecycle(self):
        if self._null:
            return None
        else:
            return self._node_lifecycle

    @property
    def access_control(self):
        if self._null:
            return None
        else:
            return self._access_control

    @property
    def nodestore(self):
        if self._null:
            return None
        else:
            return self._nodestore

    @property
    def certificate_verification(self):
        if self._null:
            return None
        else:
            return self._certificate_verification

    @property
    def max_secure_channels(self):
        if self._null:
            return None
        else:
            return self._max_secure_channels

    @property
    def max_security_token_lifetime(self):
        if self._null:
            return None
        else:
            return self._max_security_token_lifetime

    @property
    def max_sessions(self):
        if self._null:
            return None
        else:
            return self._max_sessions

    @property
    def max_session_timeout(self):
        if self._null:
            return None
        else:
            return self._max_session_timeout

    @property
    def max_nodes_per_read(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_read

    @property
    def max_nodes_per_write(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_write

    @property
    def max_nodes_per_method_call(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_method_call

    @property
    def max_nodes_per_browse(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_browse

    @property
    def max_nodes_per_register_nodes(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_register_nodes

    @property
    def max_nodes_per_translate_browse_paths_to_node_ids(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_translate_browse_paths_to_node_ids

    @property
    def max_nodes_per_node_management(self):
        if self._null:
            return None
        else:
            return self._max_nodes_per_node_management

    @property
    def max_monitored_items_per_call(self):
        if self._null:
            return None
        else:
            return self._max_monitored_items_per_call

    @property
    def max_references_per_node(self):
        if self._null:
            return None
        else:
            return self._max_references_per_node

    @logger.setter
    def logger(self, val: UaLogger):
        self._logger = val
        self._value.logger = val._val

    @build_info.setter
    def build_info(self, val: UaBuildInfo):
        self._build_info = val
        self._value.buildInfo = val._val

    @application_description.setter
    def application_description(self, val: UaApplicationDescription):
        self._application_description = val
        self._value.applicationDescription = val._val

    @server_certificate.setter
    def server_certificate(self, val: UaByteString):
        self._server_certificate = val
        self._value.serverCertificate = val._val

    @shutdown_delay.setter
    def shutdown_delay(self, val: UaDouble):
        self._shutdown_delay = val
        self._value.shutdownDelay = val._val

    @verify_request_timestamp.setter
    def verify_request_timestamp(self, val: UaRuleHandling):
        self._verify_request_timestamp = val
        self._value.verifyRequestTimestamp = val._val

    @allow_empty_variables.setter
    def allow_empty_variables(self, val: UaRuleHandling):
        self._allow_empty_variables = val
        self._value.allowEmptyVariables = val._val

    @custom_data_types.setter
    def custom_data_types(self, val: UaDataTypeArray):
        self._custom_data_types = val
        self._value.customDataTypes = val._ptr

    @network_layers_size.setter
    def network_layers_size(self, val: SizeT):
        self._network_layers_size = val
        self._value.networkLayersSize = val._val

    @network_layers.setter
    def network_layers(self, val: UaServerNetworkLayer):
        self._network_layers = val
        self._value.networkLayers = val._ptr

    @custom_hostname.setter
    def custom_hostname(self, val: UaString):
        self._custom_hostname = val
        self._value.customHostname = val._val

    @security_policies_size.setter
    def security_policies_size(self, val: SizeT):
        self._security_policies_size = val
        self._value.securityPoliciesSize = val._val

    @security_policies.setter
    def security_policies(self, val: UaSecurityPolicy):
        self._security_policies = val
        self._value.securityPolicies = val._ptr

    @endpoints_size.setter
    def endpoints_size(self, val: SizeT):
        self._endpoints_size = val
        self._value.endpointsSize = val._val

    @endpoints.setter
    def endpoints(self, val: UaEndpointDescription):
        self._endpoints = val
        self._value.endpoints = val._ptr

    @security_policy_none_discovery_only.setter
    def security_policy_none_discovery_only(self, val: UaBoolean):
        self._security_policy_none_discovery_only = val
        self._value.securityPolicyNoneDiscoveryOnly = val._val

    @node_lifecycle.setter
    def node_lifecycle(self, val: UaGlobalNodeLifecycle):
        self._node_lifecycle = val
        self._value.nodeLifecycle = val._val

    @access_control.setter
    def access_control(self, val: UaAccessControl):
        self._access_control = val
        self._value.accessControl = val._val

    @nodestore.setter
    def nodestore(self, val: UaNodestore):
        self._nodestore = val
        self._value.nodestore = val._val

    @certificate_verification.setter
    def certificate_verification(self, val: UaCertificateVerification):
        self._certificate_verification = val
        self._value.certificateVerification = val._val

    @max_secure_channels.setter
    def max_secure_channels(self, val: UaUInt16):
        self._max_secure_channels = val
        self._value.maxSecureChannels = val._val

    @max_security_token_lifetime.setter
    def max_security_token_lifetime(self, val: UaUInt32):
        self._max_security_token_lifetime = val
        self._value.maxSecurityTokenLifetime = val._val

    @max_sessions.setter
    def max_sessions(self, val: UaUInt16):
        self._max_sessions = val
        self._value.maxSessions = val._val

    @max_session_timeout.setter
    def max_session_timeout(self, val: UaDouble):
        self._max_session_timeout = val
        self._value.maxSessionTimeout = val._val

    @max_nodes_per_read.setter
    def max_nodes_per_read(self, val: UaUInt32):
        self._max_nodes_per_read = val
        self._value.maxNodesPerRead = val._val

    @max_nodes_per_write.setter
    def max_nodes_per_write(self, val: UaUInt32):
        self._max_nodes_per_write = val
        self._value.maxNodesPerWrite = val._val

    @max_nodes_per_method_call.setter
    def max_nodes_per_method_call(self, val: UaUInt32):
        self._max_nodes_per_method_call = val
        self._value.maxNodesPerMethodCall = val._val

    @max_nodes_per_browse.setter
    def max_nodes_per_browse(self, val: UaUInt32):
        self._max_nodes_per_browse = val
        self._value.maxNodesPerBrowse = val._val

    @max_nodes_per_register_nodes.setter
    def max_nodes_per_register_nodes(self, val: UaUInt32):
        self._max_nodes_per_register_nodes = val
        self._value.maxNodesPerRegisterNodes = val._val

    @max_nodes_per_translate_browse_paths_to_node_ids.setter
    def max_nodes_per_translate_browse_paths_to_node_ids(self, val: UaUInt32):
        self._max_nodes_per_translate_browse_paths_to_node_ids = val
        self._value.maxNodesPerTranslateBrowsePathsToNodeIds = val._val

    @max_nodes_per_node_management.setter
    def max_nodes_per_node_management(self, val: UaUInt32):
        self._max_nodes_per_node_management = val
        self._value.maxNodesPerNodeManagement = val._val

    @max_monitored_items_per_call.setter
    def max_monitored_items_per_call(self, val: UaUInt32):
        self._max_monitored_items_per_call = val
        self._value.maxMonitoredItemsPerCall = val._val

    @max_references_per_node.setter
    def max_references_per_node(self, val: UaUInt32):
        self._max_references_per_node = val
        self._value.maxReferencesPerNode = val._val

    @staticmethod
    def get_default_with_port(self, port_number: UaInt16, certificate: UaByteString = None):
        if certificate is None:
            certificate = Void.NULL()
        config = UaServerConfig()
        status_code = UaStatusCode(val=lib.UA_ServerConfig_setMinimal(config._ptr, port_number._val, certificate._ptr))
        if status_code.is_bad():
            raise SystemError("UA_ServerConfig_setDefault returned with " + str(status_code))
        config._update()
        return config

    @staticmethod
    def get_default(self):
        config = UaServerConfig()
        status_code = UaStatusCode(val=lib.UA_ServerConfig_setDefault(config._ptr))
        if status_code.is_bad():
            raise SystemError("UA_ServerConfig_setDefault returned with " + str(status_code))
        config._update()
        return config

    def __str__(self, n=None):
        if self._null:
            return "(UaServerConfig): NULL" + ("" if n is None else "\n")

        return ("(UaServerConfig) :\n"
                + "\t" * (1 if n is None else n+1) + "logger " + self._logger.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "build_info " + self._build_info.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "application_description " + self._application_description.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "server_certificate " + self._server_certificate.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "shutdown_delay " + self._shutdown_delay.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "verify_request_timestamp " + self._verify_request_timestamp.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "allow_empty_variables " + self._allow_empty_variables.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "custom_data_types " + self._custom_data_types.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "network_layers_size " + self._network_layers_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "network_layers " + self._network_layers.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "custom_hostname " + self._custom_hostname.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_policies_size " + self._security_policies_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "security_policies " + self._security_policies.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "endpoints_size " + self._endpoints_size.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "endpoints " + self._endpoints.__str__(1 if n is None else n+1)
                + "\t" * (
                        n + 1) + "security_policy_none_discovery_only " + self._security_policy_none_discovery_only.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "node_lifecycle " + self._node_lifecycle.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "access_control " + self._access_control.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "nodestore " + self._nodestore.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "certificate_verification " + self._certificate_verification.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_secure_channels " + self._max_secure_channels.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_security_token_lifetime " + self._max_security_token_lifetime.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_sessions " + self._max_sessions.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_session_timeout " + self._max_session_timeout.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_nodes_per_read " + self._max_nodes_per_read.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_nodes_per_write " + self._max_nodes_per_write.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_nodes_per_method_call " + self._max_nodes_per_method_call.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_nodes_per_browse " + self._max_nodes_per_browse.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_nodes_per_register_nodes " + self._max_nodes_per_register_nodes.__str__(1 if n is None else n+1)
                + "\t" * (
                        n + 1) + "max_nodes_per_translate_browse_paths_to_node_ids " + self._max_nodes_per_translate_browse_paths_to_node_ids.__str__(
                    n + 1)
                + "\t" * (1 if n is None else n+1) + "max_nodes_per_node_management " + self._max_nodes_per_node_management.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_monitored_items_per_call " + self._max_monitored_items_per_call.__str__(1 if n is None else n+1)
                + "\t" * (1 if n is None else n+1) + "max_references_per_node " + self._max_references_per_node.__str__(1 if n is None else n+1))
