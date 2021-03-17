import sys

sys.path.append("../build/open62541")
from ua import *


def variables_basics():
    i = UaInt32(5)
    j = UaInt32(i.value)

    s = UaString("test")
    s2 = UaString(s.value)

    s3 = UaString("test2")

    print(f"s == s2: {s == s2}")
    print(f"s2 == s3: {s3 == s2}")

    rr = UaReadRequest()
    rr.request_header.timestamp = UaDateTime.now()
    rr.nodes_to_read = UaList(size=5, ua_class=UaReadValueId)
    rr.nodes_to_read_size = SizeT(len(rr.nodes_to_read))
    rr2 = UaReadRequest(rr)
    rr.nodes_to_read_size = SizeT(7)

    print(str(rr2.nodes_to_read_size))


def variables_nodeids():
    id1 = UaNodeId(1, 42)
    id1.namespace_index = UaInt32(3)
    id2 = UaNodeId(1, "testid")
    id3 = UaNodeId(2, UaGuid("11111111-2222-3333-4444-555555555555"))
    id4 = UaNodeId(1, UaGuid.random())

    print(id4)


def variables_variants():
    v = UaVariant()
    i = UaInt32(42)
    v.set_scalar(i, UA_TYPES.INT32)

    v2 = UaVariant(v)

    v3 = UaVariant()
    d = UaList([1.0, 2.0, 3.0,
                4.0, 5.0, 6.0,
                7.0, 8.0, 9.0])
    v3.set_array(d, SizeT(9), UA_TYPES.DOUBLE)
    v3.array_dimensions = UaUInt32([3, 3])
    v3.array_dimensions_size = SizeT(2)

    print(f"Has array type double: {v3.has_array_type(UA_TYPES.DOUBLE)}")
    print(f"Array: {UaList(v3.data, 9, UaDouble).value}")


variables_basics()
variables_nodeids()
variables_variants()
