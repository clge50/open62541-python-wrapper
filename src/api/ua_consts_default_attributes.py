# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from intermediateApi import ffi, lib
from typing import Callable

import ua_service_results_client as ClientServiceResult
from ua_types_clientconfig import *


class UA_ATTRIBUTES_DEFAULT:
    VARIABLE = UaVariableAttributes(val=lib.UA_VariableAttributes_default)
    VARIABLE_TYPE = UaVariableTypeAttributes(val=lib.UA_VariableTypeAttributes_default)
    METHOD = UaMethodAttributes(val=lib.UA_MethodAttributes_default)
    OBJECT = UaObjectAttributes(val=lib.UA_ObjectAttributes_default)
    OBJECT_TYPE = UaObjectTypeAttributes(val=lib.UA_ObjectTypeAttributes_default)
    REFERENCE_TYPE = UaReferenceTypeAttributes(val=lib.UA_ReferenceTypeAttributes_default)
    DATA_TYPE = UaDataTypeAttributes(val=lib.UA_DataTypeAttributes_default)
    VIEW = UaViewAttributes(val=lib.UA_ViewAttributes_default)
