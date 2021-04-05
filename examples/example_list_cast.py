from ua import *

# An ``UaList`` object represents a list (although it does not actually inherits from ``list``) and as such
# provides indexed access (reading an writing).
# An UaList holds it's content (``val``) its number of elements (``size``) and its base type in the from of an
# UaType subclass.
# Not all those attributes have to be passed to the init method. There are several options of creating a list.

# When a UaLists from is created from a lists of Python primitives or strings neither ua_class nor size has to be passed
# the init method.
int64_list = UaList([1, 2, 3])
# Per default the type of integers is set to UaInt64, the type of floats to UaDouble and of strings to UaString.
# The default can be changed by setting the ua_class parameter.
bytes_list = UaList([1, 2, 3], ua_class=UaByte)
print(int64_list[2])
print(bytes_list[2])

string_list = UaList(["abc", "def"])
bytes_list = UaList(["abc", "def"], UaByteString)
print(string_list[1])
print(bytes_list[1])


# The UaList wraps an array of c type instances. For primitive types cffi automatically interprets them as python
# primitives:
print(int64_list)
# This does not work for other types:
print(string_list)
# Only once an indexed access is performed the array's entry is wrapped in an UaType.
print(string_list[1])
# For developers, this allows an easy usage coherent to other UaTypes by just using ._ptr to get the pointer
# to the first array item. Also UaLists can be created from c types. Then size and ua_class has to be provided
# as well since they cannot be guessed from the raw c type. There is an optional parameter list_of_pointers which
# is False per default. It encodes whether the content of the wrapped array are pointers to instances
# or the instances themselves. As a consequence list_of_pointers has to be set true if using void.

list_void = UaList(size=3, ua_class=Void, list_of_pointers=True)
variant = UaVariant()
variant.data = UaInt32(42)
list_void[1] = variant
# This: l[1].data = UaInt32(42)
# does not work since l[1] here in Python is a Void a as such has no attribute data

node_id = UaNodeId(2, "a_node_id")
list_void[0] = node_id
number = UaDouble(3.141593)
list_void[2] = number
# For reasons of memory protection the variables have to be saved explicitly in local variables.
# See the documentation regarding memory management.


# for the same reason all entries have to be casted to print them.
print(f"list_void[0] {UaNodeId(list_void[0])}")
print(f"list_void[1] {UaVariant(list_void[1])}")
print(f"list_void[2] {UaDouble(list_void[2])}")


