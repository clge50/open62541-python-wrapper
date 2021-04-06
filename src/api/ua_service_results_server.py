# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from ua_types_clientconfig import *


class NodeIdResult:
    def __init__(self, status_code: UaStatusCode, out_node: UaNodeId):
        self.status_code = status_code
        self.out_node = out_node


class AddMethodNodeResult:
    def __init__(self, output_arg_size: SizeT, output_args: UaArgument, status_code: UaStatusCode,
                 out_new_node_id: UaNodeId):
        self.status_code = status_code
        self.output_args = output_args
        self.output_arg_size = output_arg_size
        self.out_new_node_id = out_new_node_id


class EventResult:
    def __init__(self, status_code: UaStatusCode, out_event: UaByteString):
        self.status_code = status_code
        self.out_event = out_event


class NodeClassResult:
    def __init__(self, status_code: UaStatusCode, node_class: UaNodeClass):
        self.status_code = status_code
        self.node_class = node_class


class BrowseNameResult:
    def __init__(self, status_code: UaStatusCode, out_name: UaQualifiedName):
        self.status_code = status_code
        self.out_name = out_name


class LocalizedTextResult:
    def __init__(self, status_code: UaStatusCode, out_name: UaLocalizedText):
        self.status_code = status_code
        self.out_name = out_name


class UInt32Result:
    def __init__(self, status_code: UaStatusCode, out_number: UaUInt32):
        self.status_code = status_code
        self.out_number = out_number


class BooleanResult:
    def __init__(self, status_code: UaStatusCode, out_bool: UaBoolean):
        self.status_code = status_code
        self.out_bool = out_bool


class ByteResult:
    def __init__(self, status_code: UaStatusCode, out_byte: UaByte):
        self.status_code = status_code
        self.out_byte = out_byte


class VariantResult:
    def __init__(self, status_code: UaStatusCode, out_variant: UaVariant):
        self.status_code = status_code
        self.out_variant = out_variant


class DoubleResult:
    def __init__(self, status_code: UaStatusCode, out_double: UaDouble):
        self.status_code = status_code
        self.out_double = out_double


class BrowseResultResult:
    def __init__(self, status_code: UaStatusCode, out_browse_result: UaBrowseResult):
        self.status_code = status_code
        self.out_browse_result = out_browse_result
