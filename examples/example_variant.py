import sys
sys.path.append("../build/open62541")
from ua import *
from intermediateApi import ffi

v = UaVariant()
i = UaInt32(42)
v.set_scalar(i, TYPES.INT32)

v2 = UaVariant()
v2.copy(v)

v3 = UaVariant()
dr = [1.1, 1.2, 1.3,
     2.1, 2.2, 2.3,
     3.1, 3.2, 3.3]
d = UaDouble(dr)

x = ffi.cast("UA_Double*", ffi.new("UA_Double[]", dr))
print(x[4])
data = ffi.cast("UA_Double[9]", x)
f = ffi.new("UA_Double**", data)
f[0][4] = 42.0
print(f[0][4])

v3.set_array(d, SizeT(9), TYPES.DOUBLE)
v3.array_dimensions = UaUInt32([3, 3])
v3.array_dimensions_size = SizeT(2)

# Using ffi to test if the data is stored correctly
print(v3.has_array_type(TYPES.DOUBLE))
print(UaList(v3.data, 9, UaDouble).value)
