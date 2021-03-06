# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

import ua_types_clientconfig


# read service

class ReadNodeIdAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_node_id: ua_types_clientconfig.UaNodeId):
        self.status_code = status_code
        self.out_node_id = out_node_id


class ReadNodeClassAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_node_id: ua_types_clientconfig.UaNodeId):
        self.status_code = status_code
        self.out_node_id = out_node_id


class ReadBrowseNameAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_browse_name: ua_types_clientconfig.UaQualifiedName):
        self.status_code = status_code
        self.out_browse_name = out_browse_name


class ReadDisplayNameAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_display_name: ua_types_clientconfig.UaLocalizedText):
        self.status_code = status_code
        self.out_display_name = out_display_name


class ReadDescriptionAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_description: ua_types_clientconfig.UaLocalizedText):
        self.status_code = status_code
        self.out_description = out_description


class ReadWriteMaskAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_write_mask: ua_types_clientconfig.UaUInt32):
        self.status_code = status_code
        self.out_write_mask = out_write_mask


class ReadUserWriteMaskAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_user_write_mask: ua_types_clientconfig.UaUInt32):
        self.status_code = status_code
        self.out_user_write_mask = out_user_write_mask


class ReadIsAbstractAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_is_abstract: ua_types_clientconfig.UaBoolean):
        self.status_code = status_code
        self.out_is_abstract = out_is_abstract


class ReadSymmetricAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_symmetric: ua_types_clientconfig.UaBoolean):
        self.status_code = status_code
        self.out_symmetric = out_symmetric


class ReadInverseNameAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_inverse_name: ua_types_clientconfig.UaLocalizedText):
        self.status_code = status_code
        self.out_inverse_name = out_inverse_name


class ReadContainsNoLoopsAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_contains_no_loops: ua_types_clientconfig.UaBoolean):
        self.status_code = status_code
        self.out_contains_no_loops = out_contains_no_loops


class ReadEventNotifierAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_event_notifier: ua_types_clientconfig.UaByte):
        self.status_code = status_code
        self.out_event_notifier = out_event_notifier


class ReadValueAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, value: ua_types_clientconfig.UaVariant):
        self.status_code = status_code
        self.value = value


class ReadDataTypeAttribute:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_data_type: ua_types_clientconfig.UaNodeId):
        self.status_code = status_code
        self.value = out_data_type


class ReadValueRankAttribute:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_value_rank: ua_types_clientconfig.UaInt32):
        self.status_code = status_code
        self.value = out_value_rank


class ReadArrayDimensionsAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode,
                 out_array_dimensions: ua_types_clientconfig.UaList):
        self.status_code = status_code
        self.out_array_dimensions = out_array_dimensions


class ReadAccessLevelAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_access_level: ua_types_clientconfig.UaByte):
        self.status_code = status_code
        self.out_access_level = out_access_level


class ReadUserAccessLevelAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_user_access_level: ua_types_clientconfig.UaByte):
        self.status_code = status_code
        self.out_user_access_level = out_user_access_level


class ReadMinimumSamplingIntervalAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_min_sampling_interval: ua_types_clientconfig.UaDouble):
        self.status_code = status_code
        self.out_min_sampling_interval = out_min_sampling_interval


class ReadExecutableAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_executable: ua_types_clientconfig.UaBoolean):
        self.status_code = status_code
        self.out_executable = out_executable


class ReadUserExecutableAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_user_executable: ua_types_clientconfig.UaBoolean):
        self.status_code = status_code
        self.out_user_executable = out_user_executable


class ReadAttributeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out: ua_types_clientconfig.Void, out_data_type: ua_types_clientconfig.UaDataType):
        self.status_code = status_code
        self.out = out
        self.out_data_type = out_data_type


# misc service
# misc service
class CallResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, output_size: ua_types_clientconfig.SizeT, output: ua_types_clientconfig.UaList):
        self.status_code = status_code
        self.output_size = output_size
        self.output = output


# add node service

class AddNodeResult:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, out_new_node_id: ua_types_clientconfig.UaNodeId):
        self.status_code = status_code
        self.out_new_node_id = out_new_node_id


# async simple service
class AsyncResponse:
    def __init__(self, status_code: ua_types_clientconfig.UaStatusCode, req_id: ua_types_clientconfig.UaUInt32, _handle):
        self.status_code = status_code
        self.req_id = req_id
        self._handle = _handle
