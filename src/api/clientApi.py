from intermediateApi import ffi, lib

class DefaultAttributes:

	VARIABLE_ATTRIBUTES_DEFAULT = lib.UA_VariableAttributes_default
	VARIABLE_TYPE_ATTRIBUTES_DEFAULT = lib.UA_VariableTypeAttributes_default
	METHOD_ATTRIBUTED_DEFAULT = lib.UA_MethodAttributes_default
	OBJECT_ATTRIBUTES_DEFAULT = lib.UA_ObjectAttributes_default
	OBJECT_TYPE_ATTRIBUTES_DEFAULT = lib.UA_ObjectTypeAttributes_default
	REFERENCE_TYPE_ATTRIBUTES_DEFAULT = lib.UA_ReferenceTypeAttributes_default
	DATA_TYPE_ATTRIBUTES_DEFAULT = lib.UA_DataTypeAttributes_default
	VIEW_ATTRIBUTES_DEFAULT = lib.UA_ViewAttributes_default


class UaClient:
	def __init__(self):
		self.ua_client = lib.UA_Client_new()
		self.set_default_config()


	# connection

	def connect(self, address):
		return lib.UA_Client_connect(self.ua_client, address)


	# read service

	def read_node_id_attribute(self, node_id, out_node_id):
		return lib.UA_Client_readNodeIdAttribute(self.ua_client, node_id, out_node_id)

	def read_node_class_attribute(self, node_id, out_node_class):
		return lib.UA_Client_readNodeClassAttribute(self.ua_client, node_id, out_node_class)

	def read_browse_name_attribute(self, node_id, out_browse_name):
		return lib.UA_Client_readBrowseNameAttribute(self.ua_client, node_id, out_browse_name);
		
	def read_display_name_attribute(self, node_id, out_display_name):
		return lib.UA_Client_readDisplayNameAttribute(self.ua_client, node_id, out_display_name)

	def read_display_name_attribute(self, node_id, out_display_name):
		return lib.UA_Client_readDisplayNameAttribute(self.ua_client, node_id, out_display_name)

	def read_description_attribute(self, node_id, out_description):
		return lib.UA_Client_readDescriptionAttribute(self.ua_client, node_id, out_description)

	def read_write_mask_attribute(self, node_id, out_write_mask):
		return lib.UA_Client_readWriteMaskAttribute(self.ua_client, node_id, out_write_mask)

	def read_user_write_mask_attribute(self, node_id, out_user_write_mask):
		return lib.UA_Client_readUserWriteMaskAttribute(self.ua_client, node_id, out_user_write_mask)

	def read_is_abstract_attribute(self, node_id, out_is_abstract):
		return lib.UA_Client_readIsAbstractAttribute(self.ua_client, node_id, out_is_abstract)

	def read_symmetric_attribute(self, node_id, out_symmetric):
		return lib.UA_Client_readSymmetricAttribute(self.ua_client, node_id, out_symmetric)

	def read_inverse_name_attribute(self, node_id, out_inverse_name):
		return lib.UA_Client_readInverseNameAttribute(self.ua_client, node_id, out_inverse_name)

	def read_contains_no_loops_attribute(self, node_id, out_contains_no_loops):
		return lib.UA_Client_readContainsNoLoopsAttribute(self.ua_client, node_id, out_contains_no_loops)

	def read_event_notifier_attribute(self, node_id, out_event_notifier):
		return lib.UA_Client_readEventNotifierAttribute(self.ua_client, node_id, out_event_notifier)

	def read_value_attribute(self, nodeId, value):
		return lib.UA_Client_readValueAttribute(self.ua_client, nodeId, value.value)

	def read_data_type_attribute(self, node_id, out_data_type):
		return lib.UA_Client_readDataTypeAttribute(self.ua_client, node_id, out_data_type)

	def read_value_rank_attribute(self, node_id, out_value_rank):
		return lib.UA_Client_readValueRankAttribute(self.ua_client, node_id, out_value_rank)

	def read_array_dimensions_attribute(self, node_id, out_array_dimensions_size, out_array_dimensions):
		return lib.UA_Client_readArrayDimensionsAttribute(self.ua_client, node_id, out_array_dimensions_size, out_array_dimensions)

	def read_access_level_attribute(self, node_id, out_access_level):
		return lib.UA_Client_readAccessLevelAttribute(self.ua_client, node_id, out_access_level)

	def read_user_access_level_attribute(self, node_id, out_user_access_level):
		return lib.UA_Client_readUserAccessLevelAttribute(self.ua_client, node_id, out_user_access_level)

	def read_minimum_sampling_interval_attribute(self, node_id, out_min_sampling_interval):
		return lib.UA_Client_readMinimumSamplingIntervalAttribute(self.ua_client, node_id, out_min_sampling_interval)

	def read_executable_attribute(self, node_id, out_executable):
		return lib.UA_Client_readExecutableAttribute(self.ua_client, node_id, out_executable)

	def read_user_executable_attribute(self, node_id, out_user_executable):
		return lib.UA_Client_readUserExecutableAttribute(self.ua_client, node_id, out_user_executable)


	# write service

	def writeNodeIdAttribute(self, node_id, new_node_id):
		return lib.UA_Client_writeNodeIdAttribute(self.ua_client, node_id, new_node_id)

	def writeNodeClassAttribute(self, node_id, new_node_class):
		return lib.UA_Client_writeNodeClassAttribute(self.ua_client, node_id, new_node_class)

	def writeBrowseNameAttribute(self, node_id, new_browse_name):
		return lib.UA_Client_writeBrowseNameAttribute(self.ua_client, node_id, new_browse_name)

	def writeDisplayNameAttribute(self, node_id, new_display_name):
		return lib.UA_Client_writeDisplayNameAttribute(self.ua_client, node_id, new_display_name)

	def writeDescriptionAttribute(self, node_id, new_description):
		return lib.UA_Client_writeDescriptionAttribute(self.ua_client, node_id, new_description)

	def writeWriteMaskAttribute(self, node_id, new_write_mask):
		return lib.UA_Client_writeWriteMaskAttribute(self.ua_client, node_id, new_write_mask)

	def writeUserWriteMaskAttribute(self, node_id, new_user_write_mask):
		return lib.UA_Client_writeUserWriteMaskAttribute(self.ua_client, node_id, new_user_write_mask)

	def writeIsAbstractAttribute(self, node_id, new_is_abstract):
		return lib.UA_Client_writeIsAbstractAttribute(self.ua_client, node_id, new_is_abstract)

	def writeSymmetricAttribute(self, node_id, new_symmetric):
		return lib.UA_Client_writeSymmetricAttribute(self.ua_client, node_id, new_symmetric)

	def writeInverseNameAttribute(self, node_id, new_inverse_name):
		return lib.UA_Client_writeInverseNameAttribute(self.ua_client, node_id, new_inverse_name)

	def writeInverseNameAttribute(self, node_id, new_inverse_name):
		return lib.UA_Client_writeInverseNameAttribute(self.ua_client, node_id, new_inverse_name)

	def writeContainsNoLoopsAttribute(self, node_id, new_contains_no_loops):
		return lib.UA_Client_writeContainsNoLoopsAttribute(self.ua_client, node_id, new_contains_no_loops)

	def writeEventNotifierAttribute(self, node_id, new_event_notifier):
		return lib.UA_Client_writeEventNotifierAttribute(self.ua_client, node_id, new_event_notifier)

	def writeValueAttribute(self, node_id, new_value):
		return lib.UA_Client_writeValueAttribute(self.ua_client, node_id, new_value)

	def writeDataTypeAttribute(self, node_id, new_data_type):
		return lib.UA_Client_writeDataTypeAttribute(self.ua_client, node_id, new_data_type)

	def writeValueRankAttribute(self, node_id, new_value_rank):
		return lib.UA_Client_writeValueRankAttribute(self.ua_client, node_id, new_value_rank)

	def writeArrayDimensionsAttribute(self, node_id, new_array_dimensions_size, new_array_dimensions):
		return lib.UA_Client_writeArrayDimensionsAttribute(self.ua_client, node_id, new_array_dimensions_size, new_array_dimensions)

	def writeAccessLevelAttribute(self, node_id, new_access_level):
		return lib.UA_Client_writeAccessLevelAttribute(self.ua_client, node_id, new_access_level)

	def writeUserAccessLevelAttribute(self, node_id, new_user_access_level):
		return lib.UA_Client_writeUserAccessLevelAttribute(self.ua_client, node_id, new_user_access_level)

	def writeMinimumSamplingIntervalAttribute(self, node_id, new_min_interval):
		return lib.UA_Client_writeMinimumSamplingIntervalAttribute(self.ua_client, node_id, new_min_interval)

	def writeExecutableAttribute(self, node_id, new_executable):
		return lib.UA_Client_writeExecutableAttribute(self.ua_client, node_id, new_executable)

	def writeUserExecutableAttribute(self, node_id, new_user_executable):
		return lib.UA_Client_writeUserExecutableAttribute(self.ua_client, node_id, new_user_executable)


	# misc service calls

	def call(self, object_id, method_id, input_size, input, output_size, output):
		return lib.UA_Client_call(self.ua_client, object_id, method_id, input_size, input, output_size, output)

	def addReference(self, source_node_id, reference_type_id, is_forward, target_server_uri, target_node_id, target_node_class):
		return lib.UA_Client_addReference(self.ua_client, source_node_id, reference_type_id, is_forward, target_server_uri, target_node_id, target_node_class)

	def deleteReference(self, source_node_id, reference_type_id, is_forward, targetNode_id, delete_bidirectional):
		return lib.UA_Client_deleteReference(self.ua_client, source_node_id, reference_type_id, is_forward, targetNode_id, delete_bidirectional);

	def deleteNode(self, node_id, delete_target_references):
		return lib.UA_Client_deleteNode(self.ua_client, node_id, delete_target_references)


	# add node services

	def addVariableNode(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition, out_new_node_id, attr = DefaultAttributes.VARIABLE_ATTRIBUTES_DEFAULT):
		return lib.UA_Client_addVariableNode(self.ua_client, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition, attr, out_new_node_id);

	def addVariableTypeNode(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, out_new_node_id, attr = DefaultAttributes.VARIABLE_TYPE_ATTRIBUTES_DEFAULT):
		return lib.UA_Client_addVariableTypeNode(self.ua_client, requested_new_node_id, parent_node_id, reference_type_id, browse_name, attr, out_new_node_id)

	def addObjectNode(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition, out_new_node_id, attr = DefaultAttributes.OBJECT_ATTRIBUTES_DEFAULT):
		return lib.UA_Client_addObjectNode(self.ua_client, requested_new_node_id, parent_node_id, reference_type_id, browse_name, type_definition, attr, out_new_node_id)

	def addObjectTypeNode(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, out_new_node_id, attr = DefaultAttributes.OBJECT_TYPE_ATTRIBUTES_DEFAULT):
		return lib.UA_Client_addObjectTypeNode(self.ua_client, requested_new_node_id, parent_node_id, reference_type_id, browse_name, attr, out_new_node_id)

	def addViewNode(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, out_new_node_id, attr = DefaultAttributes.VIEW_ATTRIBUTES_DEFAULT):
		return lib.UA_Client_addViewNode(self.ua_client, requested_new_node_id, parent_node_id, reference_type_id, browse_name, attr, out_new_node_id)

	def addReferenceTypeNode(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, out_new_node_id, attr = DefaultAttributes.REFERENCE_TYPE_ATTRIBUTES_DEFAULT):
		return lib.UA_Client_addReferenceTypeNode(self.ua_client, requested_new_node_id, parent_node_id, reference_type_id, browse_name, attr, out_new_node_id)

	def addDataTypeNode(self, requested_node_id, parent_node_id, reference_type_id, browse_name, out_new_node_id, attr = DefaultAttributes.DATA_TYPE_ATTRIBUTES_DEFAULT):
		return lib.UA_Client_addDataTypeNode(self.ua_client, requested_node_id, parent_node_id, reference_type_id, browse_name, attr, out_new_node_id)

	def addMethodNode(self, requested_new_node_id, parent_node_id, reference_type_id, browse_name, out_new_node_id, attr = DefaultAttributes.METHOD_ATTRIBUTED_DEFAULT):
		return lib.UA_Client_addMethodNode(self.ua_client, requested_new_node_id, parent_node_id, reference_type_id, browse_name, attr, out_new_node_id)


	# utils

	def get_config(self):
		return lib.UA_Client_getConfig(self.ua_client)

	def set_default_config(self):
		lib.UA_ClientConfig_setDefault(self.get_config())

	def find_data_type(self, type_id):
		return lib.UA_Client_findDataType(self.ua_client, type_id);

