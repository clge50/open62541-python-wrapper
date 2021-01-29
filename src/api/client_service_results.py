# read service

class ReadNodeIdAttributeResult:
    def __init__(self, status_code, out_node_id):
        self.status_code = status_code
        self.out_node_id = out_node_id


class ReadNodeClassAttributeResult:
    def __init__(self, status_code, out_node_id):
        self.status_code = status_code
        self.out_node_id = out_node_id


class ReadBrowseNameAttributeResult:
    def __init__(self, status_code, out_browse_name):
        self.status_code = status_code
        self.out_browse_name = out_browse_name


class ReadDisplayNameAttributeResult:
    def __init__(self, status_code, out_display_name):
        self.status_code = status_code
        self.out_display_name = out_display_name


class ReadDescriptionAttributeResult:
    def __init__(self, status_code, out_description):
        self.status_code = status_code
        self.out_description = out_description


class ReadWriteMaskAttributeResult:
    def __init__(self, status_code, out_write_mask):
        self.status_code = status_code
        self.out_write_mask = out_write_mask


class ReadUserWriteMaskAttributeResult:
    def __init__(self, status_code, out_user_write_mask):
        self.status_code = status_code
        self.out_user_write_mask = out_user_write_mask


class ReadIsAbstractAttributeResult:
    def __init__(self, status_code, out_is_abstract):
        self.status_code = status_code
        self.out_is_abstract = out_is_abstract


class ReadSymmetricAttributeResult:
    def __init__(self, status_code, out_symmetric):
        self.status_code = status_code
        self.out_symmetric = out_symmetric


class ReadInverseNameAttributeResult:
    def __init__(self, status_code, out_inverse_name):
        self.status_code = status_code
        self.out_inverse_name = out_inverse_name


class ReadContainsNoLoopsAttributeResult:
    def __init__(self, status_code, out_contains_no_loops):
        self.status_code = status_code
        self.out_contains_no_loops = out_contains_no_loops


class ReadEventNotifierAttributeResult:
    def __init__(self, status_code, out_event_notifier):
        self.status_code = status_code
        self.out_event_notifier = out_event_notifier


class ReadValueAttributeResult:
    def __init__(self, status_code, value):
        self.status_code = status_code
        self.value = value


class ReadDataTypeAttribute:
    def __init__(self, status_code, out_data_type):
        self.status_code = status_code
        self.value = out_data_type


class ReadValueRankAttribute:
    def __init__(self, status_code, out_value_rank):
        self.status_code = status_code
        self.value = out_value_rank


class ReadArrayDimensionsAttributeResult:
    def __init__(self, status_code, out_array_dimensions_size, out_array_dimensions):
        self.status_code = status_code
        self.out_array_dimensions_size = out_array_dimensions_size
        self.out_array_dimensions = out_array_dimensions


class ReadAccessLevelAttributeResult:
    def __init__(self, status_code, out_access_level):
        self.status_code = status_code
        self.out_access_level = out_access_level


class ReadUserAccessLevelAttributeResult:
    def __init__(self, status_code, out_user_access_level):
        self.status_code = status_code
        self.out_user_access_level = out_user_access_level


class ReadMinimumSamplingIntervalAttributeResult:
    def __init__(self, status_code, out_min_sampling_interval):
        self.status_code = status_code
        self.out_min_sampling_interval = out_min_sampling_interval


class ReadExecutableAttributeResult:
    def __init__(self, status_code, out_executable):
        self.status_code = status_code
        self.out_executable = out_executable


class ReadUserExecutableAttributeResult:
    def __init__(self, status_code, out_user_executable):
        self.status_code = status_code
        self.out_user_executable = out_user_executable


# misc service

class CallResult:
    def __init__(self, status_code, output_size, output):
        self.status_code = status_code
        self.output_size = output_size
        self.output = output


# add node service

class AddNodeResult:
    def __init__(self, status_code, out_new_node_id):
        self.status_code = status_code
        self.out_new_node_id = out_new_node_id
