# read service

class Read_node_id_attribute:
	def __init__(self, status_code, out_node_id):
		self.status_code
		self.out_node_id

class Read_node_class_attribute_wrapper:
	def __init__(self, status_code, out_node_id):
		self.status_code
		self.out_node_id

class Read_browse_name_attribute_wrapper:
	def __init__(self, status_code, out_browse_name):
		self.status_code
		self.out_browse_name

class Read_display_name_attribute_wrapper:
	def __init__(self, status_code, out_display_name):
		self.status_code
		self.out_display_name

class Read_description_attribute_wrapper:
	def __init__(self, status_code, out_description):
		self.status_code
		self.out_description

class Read_write_mask_attribute_wrapper:
	def __init__(self, status_code, out_write_mask):
		self.status_code
		self.out_write_mask

class Read_user_write_mask_attribute_wrapper:
	def __init__(self, status_code, out_user_write_mask):
		self.status_code
		self.out_user_write_mask

class Read_is_abstract_attribute_wrapper:
	def __init__(self, status_code, out_is_abstract):
		self.status_code
		self.out_is_abstract

class Read_symmetric_attribute_wrapper:
	def __init__(self, status_code, out_symmetric):
		self.status_code
		self.out_symmetric

class Read_inverse_name_attribute_wrapper:
	def __init__(self, status_code, out_inverse_name):
		self.status_code
		self.out_inverse_name

class Read_contains_no_loops_attribute_wrapper:
	def __init__(self, status_code, out_contains_no_loops):
		self.status_code
		self.out_contains_no_loops

class Read_event_notifier_attribute_wrapper:
	def __init__(self, status_code, out_event_notifier):
		self.status_code
		self.out_event_notifier

class Read_value_attribute_wrapper:
	def __init__(self, status_code, value):
		self.status_code
		self.value

class Read_array_dimensions_attribute_wrapper:
	def __init__(self, status_code, out_array_dimensions_size, out_array_dimensions):
		self.status_code
		self.out_array_dimensions_size
		self.out_array_dimensions

class Read_access_level_attribute_wrapper:
	def __init__(self, status_code, out_access_level):
		self.status_code
		self.out_access_level

class Read_user_access_level_attribute_wrapper:
	def __init__(self, status_code):
		self.status_code

class Read_minimum_sampling_interval_attribute_wrapper:
	def __init__(self, status_code, out_min_sampling_interval):
		self.status_code
		self.out_min_sampling_interval

class Read_executable_attribute_wrapper:
	def __init__(self, status_code, out_executable):
		self.status_code
		self.out_executable

class Read_user_executable_attribute_wrapper:
	def __init__(self, status_code):
		self.status_code


# misc service

class Call_wrapper:
	def __init__(self, status_code):
		self.status_code

# add node service

class Add_node_wrapper:
	def __init__(self, status_code, out_new_node_id):
		self.status_code
		self.out_new_node_id