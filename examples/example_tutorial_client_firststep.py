from ua import *

# new client with default config
client = UaClient()
ret_val = client.connect("opc.tcp://127.0.0.1:4841/")
print(ret_val)


def read_time():
    result = client.read_value_attribute(UA_NS0ID.SERVER_SERVERSTATUS_CURRENTTIME)

    status_code = result.status_code
    variant = result.value

    print(status_code)

    if variant.has_scalar_type(UA_TYPES.DATETIME):
        now = UaDateTime(variant.data)

    UaLogger().info(UaLogCategory.USERLAND(), "date is " + str(now.to_struct()))


iterate = True
while iterate:
    if input() == "x":
        iterate = False
    read_time()
