from ua import *

# new client with default config
client = UaClient()
ret_val = client.connect("opc.tcp://127.0.0.1:4840/")
print(ret_val)

result = client.read_value_attribute(UA_NS0ID.SERVER_SERVERSTATUS_CURRENTTIME)

ret_val = result.status_code
variant = result.value

print(ret_val)

if variant.has_scalar_type(UA_TYPES.DATETIME):
    now = UaDateTime(variant.data)

UaLogger().info(UaLogCategory.USERLAND(), "date is "+str(now.to_struct()))
