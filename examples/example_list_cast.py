from ua import *

# An ``UaList`` object represents a list (although it does not actually inherits from ``list``) and as such
# provides indexed access (reading an writing).
# An UaList holds it's content (``val``) its number of elements (``size``) and its base type in the from of an
# UaType subclass.
# Not all those attributes have to be passed to the init method. There are several options of creating a list.

# UaLists from Lists of Python primitives and strings.
int_list = UaList([1, 2, 3])
print(int_list)
string_list = UaList(["abc", "def"])
# The UaList wraps an array of c type instances.
print(string_list)
# Only once an indexed access is performed the array's entry is wrapped in an UaType.
print(string_list[1])

# For developers, this allows an easy usage coherent to other UaTypes by just using ._ptr to get the pointer
# to the first array item. Also UaLists can be created from c types. Then size and ua_class has to be provided
# as well since they cannot be guessed from the raw c type. There is an optional parameter list_of_pointers which
# is False per default. It encodes whether the content of the wrapped array are pointers to instances or the instances

# Void is the only exception for this. In this case it's an array of void pointers. Any type instance can be assigned
# since it is internally processed as a pointer.

# lists
l = UaList(size=5, ua_class=UaVariant, list_of_pointers=True)
l[0] = UaVariant()
print(UaVariant(l[0]))
UaInt32()
