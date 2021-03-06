# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from ua_types_primitive import UaByte, UaUInt32

class UaAccessLevelMasks:
    READ = UaByte(1)
    WRITE = UaByte(2)
    HISTORYREAD = UaByte(4)
    HISTORYWRITE = UaByte(8)
    SEMANTICCHANGE = UaByte(16)
    STATUSWRITE = UaByte(32)
    TIMESTAMPWRITE = UaByte(64)


class UaWriteMask:
    ACCESSLEVEL = UaUInt32(1)
    ARRRAYDIMENSIONS = UaUInt32(2)
    BROWSENAME = UaUInt32(4)
    CONTAINSNOLOOPS = UaUInt32(8)
    DATATYPE = UaUInt32(16)
    DESCRIPTION = UaUInt32(32)
    DISPLAYNAME = UaUInt32(64)
    EVENTNOTIFIER = UaUInt32(128)
    EXECUTABLE = UaUInt32(256)
    HISTORIZING = UaUInt32(512)
    INVERSENAME = UaUInt32(1024)
    ISABSTRACT = UaUInt32(2048)
    MINIMUMSAMPLINGINTERVAL = UaUInt32(4096)
    NODECLASS = UaUInt32(2*MINIMUMSAMPLINGINTERVAL._val)
    NODEID = UaUInt32(2*NODECLASS._val)
    SYMMETRIC = UaUInt32(2*NODEID._val)
    USERACCESSLEVEL = UaUInt32(2*SYMMETRIC._val)
    USEREXECUTABLE = UaUInt32(2*USERACCESSLEVEL._val)
    USERWRITEMASK = UaUInt32(2*USEREXECUTABLE._val)
    VALUERANK = UaUInt32(2*USERWRITEMASK._val)
    WRITEMASK = UaUInt32(2*VALUERANK._val)
    VALUEFORVARIABLETYPE = UaUInt32(2*WRITEMASK._val)
