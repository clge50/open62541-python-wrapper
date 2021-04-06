# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

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

#This is how to use enums
session_state = UaSessionState.ACTIVATED()
print(session_state)

now = UaDateTimeStruct.now()
print(now)
