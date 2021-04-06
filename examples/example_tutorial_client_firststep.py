# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from ua import *


def read_time():
    result = client.read_value_attribute(UA_NS0ID.SERVER_SERVERSTATUS_CURRENTTIME)

    status_code = result.status_code
    variant = result.value

    print(status_code)

    if variant.has_scalar_type(UA_TYPES.DATETIME):
        now = UaDateTime(variant.data)

    UaLogger().info(UaLogCategory.USERLAND(), "date is " + str(now.to_struct()))


# new client with default config
client = UaClient()
ret_val = client.connect("opc.tcp://127.0.0.1:4840/")
print(ret_val)
read_time()
