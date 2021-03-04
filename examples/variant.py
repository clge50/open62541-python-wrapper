import sys
import time

from ua_types import _ptr

sys.path.append("../build/open62541")
from ua_types import *
from ua_data_types import TYPES
from intermediateApi import ffi, lib

# UA_Variant v;
# UA_Int32 i = 42;
# UA_Variant_setScalar(&v, &i, &UA_TYPES[UA_TYPES_INT32]);
#
# /* Make a copy */
# UA_Variant v2;
# UA_Variant_copy(&v, &v2);
# UA_Variant_clear(&v2);
#
# /* Set an array value */
# UA_Variant v3;
# UA_Double d[9] = {1.0, 2.0, 3.0,
#                   4.0, 5.0, 6.0,
#                   7.0, 8.0, 9.0};
# UA_Variant_setArrayCopy(&v3, d, 9, &UA_TYPES[UA_TYPES_DOUBLE]);
#
# /* Set array dimensions */
# v3.arrayDimensions = (UA_UInt32 *)UA_Array_new(2, &UA_TYPES[UA_TYPES_UINT32]);
# v3.arrayDimensionsSize = 2;
# v3.arrayDimensions[0] = 3;
# v3.arrayDimensions[1] = 3;
# UA_Variant_clear(&v)

v = UaVariant()
i = UaInt32(42)
v.set_scalar(i, TYPES.INT32)

v2 = UaVariant()
v2.copy(v)

v3 = UaVariant()
d = [1.1, 1.2, 1.3,
     2.1, 2.2, 2.3,
     3.1, 3.2, 3.3]
d = UaDouble(d)

v3.set_array(d, SizeT(9), TYPES.DOUBLE)
v3.array_dimensions = UaUInt32([3, 3])
v3.array_dimensions_size = SizeT(2)

print(v3.has_array_type(TYPES.DOUBLE))
data = ffi.cast("UA_Double[9]", v3._data._value)
data = ffi.unpack(data, 9)
print(data)

a = UaSByte(13)
b = UaSByte(3)
c = UaDouble(3.0)
print(c < b)
print(a <= b)
print(c == b)
print(a < b)
print(c < b)

print(c.value)








