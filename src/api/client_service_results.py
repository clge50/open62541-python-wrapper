# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import ua_types


# read service

class ReadNodeIdAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_node_id: ua_types.UaNodeId):
        self.status_code = status_code
        self.out_node_id = out_node_id


class ReadNodeClassAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_node_id: ua_types.UaNodeId):
        self.status_code = status_code
        self.out_node_id = out_node_id


class ReadBrowseNameAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_browse_name: ua_types.UaQualifiedName):
        self.status_code = status_code
        self.out_browse_name = out_browse_name


class ReadDisplayNameAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_display_name: ua_types.UaLocalizedText):
        self.status_code = status_code
        self.out_display_name = out_display_name


class ReadDescriptionAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_description: ua_types.UaLocalizedText):
        self.status_code = status_code
        self.out_description = out_description


class ReadWriteMaskAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_write_mask: ua_types.UaByte):
        self.status_code = status_code
        self.out_write_mask = out_write_mask


class ReadUserWriteMaskAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_user_write_mask: ua_types.UaByte):
        self.status_code = status_code
        self.out_user_write_mask = out_user_write_mask


class ReadIsAbstractAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_is_abstract: ua_types.UaBoolean):
        self.status_code = status_code
        self.out_is_abstract = out_is_abstract


class ReadSymmetricAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_symmetric: ua_types.UaBoolean):
        self.status_code = status_code
        self.out_symmetric = out_symmetric


class ReadInverseNameAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_inverse_name: ua_types.UaLocalizedText):
        self.status_code = status_code
        self.out_inverse_name = out_inverse_name


class ReadContainsNoLoopsAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_contains_no_loops: ua_types.UaBoolean):
        self.status_code = status_code
        self.out_contains_no_loops = out_contains_no_loops


class ReadEventNotifierAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_event_notifier: ua_types.UaByte):
        self.status_code = status_code
        self.out_event_notifier = out_event_notifier


class ReadValueAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, value: ua_types.UaVariant):
        self.status_code = status_code
        self.value = value


class ReadDataTypeAttribute:
    def __init__(self, status_code: ua_types.UaStatusCode, out_data_type: ua_types.UaNodeId):
        self.status_code = status_code
        self.value = out_data_type


class ReadValueRankAttribute:
    def __init__(self, status_code: ua_types.UaStatusCode, out_value_rank: ua_types.UaInt32):
        self.status_code = status_code
        self.value = out_value_rank


# todo: out_array_dimensions is UA_UInt32 **
class ReadArrayDimensionsAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_array_dimensions_size: ua_types.SizeT,
                 out_array_dimensions: ua_types.UaUInt32):
        self.status_code = status_code
        self.out_array_dimensions_size = out_array_dimensions_size
        self.out_array_dimensions = out_array_dimensions


class ReadAccessLevelAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_access_level: ua_types.UaByte):
        self.status_code = status_code
        self.out_access_level = out_access_level


class ReadUserAccessLevelAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_user_access_level: ua_types.UaByte):
        self.status_code = status_code
        self.out_user_access_level = out_user_access_level


class ReadMinimumSamplingIntervalAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_min_sampling_interval: ua_types.UaDouble):
        self.status_code = status_code
        self.out_min_sampling_interval = out_min_sampling_interval


class ReadExecutableAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_executable: ua_types.UaBoolean):
        self.status_code = status_code
        self.out_executable = out_executable


class ReadUserExecutableAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_user_executable: ua_types.UaBoolean):
        self.status_code = status_code
        self.out_user_executable = out_user_executable


class ReadAttributeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out: ua_types.Void, out_data_type: ua_types.UaDataType):
        self.status_code = status_code
        self.out = out
        self.out_data_type = out_data_type


# misc service
# todo: output should be UA_Variant **
class CallResult:
    def __init__(self, status_code: ua_types.UaStatusCode, output_size: ua_types.SizeT, output: ua_types.UaVariant):
        self.status_code = status_code
        self.output_size = output_size
        self.output = output


# add node service

class AddNodeResult:
    def __init__(self, status_code: ua_types.UaStatusCode, out_new_node_id: ua_types.UaNodeId):
        self.status_code = status_code
        self.out_new_node_id = out_new_node_id


# todo: add type of _handle
# async simple service
class AsyncResponse:
    def __init__(self, status_code: ua_types.UaStatusCode, req_id: ua_types.UaUInt32, _handle):
        self.status_code = status_code
        self.req_id = req_id
        self._handle = _handle
