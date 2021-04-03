from ua import *

l = UaList(size=5, ua_class=Void)
l[0] = UaInt32(4)
print(UaInt32(l[0]))
UaInt32()