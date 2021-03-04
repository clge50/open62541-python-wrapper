from ua import *

a = UaSByte(13)
b = UaSByte(3)
c = UaDouble(3.0)

# Numeric types can be compared
print(c < b)
print(a <= b)
print(c == b)
print(a > b)
print(c < b)

# The python value can be accessed via .value
print(c.value)

string = UaString("a string")
print(string.value)
# The str method is implemented as well but with formatting so the structs are displayed nicely
print(string)

now = UaDateTimeStruct.now()
print(now)
