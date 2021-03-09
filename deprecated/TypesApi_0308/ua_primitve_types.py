# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier

from typing import Union, List

from intermediateApi import ffi, lib
from ua_common import *
from ua_types_parent import _ptr, _val, _is_null, _is_ptr


# +++++++++++++++++++ UaBoolean +++++++++++++++++++++++
class UaBoolean(UaType):
    def __init__(self, val: Union[Void, bool, List[bool]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_Boolean*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Boolean*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Boolean[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Boolean*", _val(val)), is_pointer)

    @property
    def value(self):
        return bool(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Boolean")
        else:
            self._value[0] = ffi.cast("UA_Boolean", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaBoolean) : NULL\n"
        else:
            return "(UaBoolean): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val


# +++++++++++++++++++ UaSByte +++++++++++++++++++++++
class UaSByte(UaType):
    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_SByte*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_SByte*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_SByte[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_SByte*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_SByte")
        else:
            self._value[0] = ffi.cast("UA_SByte", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaSByte) : NULL\n"
        else:
            return "(UaSByte): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaByte +++++++++++++++++++++++
class UaByte(UaType):
    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_Byte*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Byte*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Byte[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Byte*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Byte")
        else:
            self._value[0] = ffi.cast("UA_Byte", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaSByte) : NULL\n"
        else:
            return "(UaByte): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaInt16 +++++++++++++++++++++++
class UaInt16(UaType):
    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_Int16*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Int16*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Int16[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Int16*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int16")
        else:
            self._value[0] = ffi.cast("UA_Int16", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaInt16) : NULL\n"
        else:
            return "(UaInt16): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaUInt16 +++++++++++++++++++++++
class UaUInt16(UaType):
    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_UInt16*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_UInt16*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_UInt16[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_UInt16*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt16")
        else:
            self._value[0] = ffi.cast("UA_UInt16", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaUInt16) : NULL\n"
        else:
            return "(UaUInt16): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaInt32 +++++++++++++++++++++++
class UaInt32(UaType):
    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_Int32*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Int32*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Int32[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Int32*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int32")
        else:
            self._value[0] = ffi.cast("UA_Int32", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaInt32) : NULL\n"
        else:
            return "(UaInt32): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaUInt32 +++++++++++++++++++++++
class UaUInt32(UaType):
    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_UInt32*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_UInt32*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_UInt32[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_UInt32*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt32")
        else:
            self._value[0] = ffi.cast("UA_UInt32", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaUInt32) : NULL\n"
        else:
            return "(UaUInt32): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaInt64 +++++++++++++++++++++++
class UaInt64(UaType):
    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_Int64*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Int64*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Int64[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Int64*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Int64")
        else:
            self._value[0] = ffi.cast("UA_Int64", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaInt64) : NULL\n"
        else:
            return "(UaInt64): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaUInt64 +++++++++++++++++++++++
class UaUInt64(UaType):
    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_UInt64*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_UInt64*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_UInt64[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_UInt64*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_UInt64")
        else:
            self._value[0] = ffi.cast("UA_UInt64", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaUInt64) : NULL\n"
        else:
            return "(UaUInt64): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaFloat +++++++++++++++++++++++
class UaFloat(UaType):
    def __init__(self, val: Union[Void, float, List[float]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_Float*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_Float*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Float[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Float*", _val(val)), is_pointer)

    @property
    def value(self):
        return float(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Float")
        else:
            self._value[0] = ffi.cast("UA_Float", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaFloat) : NULL\n"
        else:
            return "(UaFloat): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaDouble +++++++++++++++++++++++
# TODO: Array handling for all other types
class UaDouble(UaType):
    def __init__(self, val: Union[Void, float, List[float]] = None,  size: int = None, is_pointer=False):
        if type(val) is Void:
            if size is None:
                val = ffi.cast("UA_Double*", val._ptr)
            else:
                val = ffi.cast(f"UA_Double[{size}]", val._ptr)
                is_pointer = True
        if val is None:
            super().__init__(ffi.new("UA_Double*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_Double[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_Double*", _val(val)), is_pointer)
        self._size = size

    @property
    def value(self):
        if self._size is None:
            return float(self._val)
        return ffi.unpack(self._ptr, self._size)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Double")
        else:
            self._value[0] = ffi.cast("UA_Double", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaDouble) : NULL\n"
        else:
            return "(UaDouble): " + str(self._val) + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val


# +++++++++++++++++++ UaStatusCode +++++++++++++++++++++++
class UaStatusCode(UaType):
    UA_STATUSCODE_INFOTYPE_DATAVALUE = 0x00000400
    UA_STATUSCODE_INFOBITS_OVERFLOW = 0x00000080
    UA_STATUSCODE_GOOD = 0x00000000
    UA_STATUSCODE_UNCERTAIN = 0x40000000
    UA_STATUSCODE_BAD = 0x80000000
    UA_STATUSCODE_BADUNEXPECTEDERROR = 0x80010000
    UA_STATUSCODE_BADINTERNALERROR = 0x80020000
    UA_STATUSCODE_BADOUTOFMEMORY = 0x80030000
    UA_STATUSCODE_BADRESOURCEUNAVAILABLE = 0x80040000
    UA_STATUSCODE_BADCOMMUNICATIONERROR = 0x80050000
    UA_STATUSCODE_BADENCODINGERROR = 0x80060000
    UA_STATUSCODE_BADDECODINGERROR = 0x80070000
    UA_STATUSCODE_BADENCODINGLIMITSEXCEEDED = 0x80080000
    UA_STATUSCODE_BADREQUESTTOOLARGE = 0x80B80000
    UA_STATUSCODE_BADRESPONSETOOLARGE = 0x80B90000
    UA_STATUSCODE_BADUNKNOWNRESPONSE = 0x80090000
    UA_STATUSCODE_BADTIMEOUT = 0x800A0000
    UA_STATUSCODE_BADSERVICEUNSUPPORTED = 0x800B0000
    UA_STATUSCODE_BADSHUTDOWN = 0x800C0000
    UA_STATUSCODE_BADSERVERNOTCONNECTED = 0x800D0000
    UA_STATUSCODE_BADSERVERHALTED = 0x800E0000
    UA_STATUSCODE_BADNOTHINGTODO = 0x800F0000
    UA_STATUSCODE_BADTOOMANYOPERATIONS = 0x80100000
    UA_STATUSCODE_BADTOOMANYMONITOREDITEMS = 0x80DB0000
    UA_STATUSCODE_BADDATATYPEIDUNKNOWN = 0x80110000
    UA_STATUSCODE_BADCERTIFICATEINVALID = 0x80120000
    UA_STATUSCODE_BADSECURITYCHECKSFAILED = 0x80130000
    UA_STATUSCODE_BADCERTIFICATEPOLICYCHECKFAILED = 0x81140000
    UA_STATUSCODE_BADCERTIFICATETIMEINVALID = 0x80140000
    UA_STATUSCODE_BADCERTIFICATEISSUERTIMEINVALID = 0x80150000
    UA_STATUSCODE_BADCERTIFICATEHOSTNAMEINVALID = 0x80160000
    UA_STATUSCODE_BADCERTIFICATEURIINVALID = 0x80170000
    UA_STATUSCODE_BADCERTIFICATEUSENOTALLOWED = 0x80180000
    UA_STATUSCODE_BADCERTIFICATEISSUERUSENOTALLOWED = 0x80190000
    UA_STATUSCODE_BADCERTIFICATEUNTRUSTED = 0x801A0000
    UA_STATUSCODE_BADCERTIFICATEREVOCATIONUNKNOWN = 0x801B0000
    UA_STATUSCODE_BADCERTIFICATEISSUERREVOCATIONUNKNOWN = 0x801C0000
    UA_STATUSCODE_BADCERTIFICATEREVOKED = 0x801D0000
    UA_STATUSCODE_BADCERTIFICATEISSUERREVOKED = 0x801E0000
    UA_STATUSCODE_BADCERTIFICATECHAININCOMPLETE = 0x810D0000
    UA_STATUSCODE_BADUSERACCESSDENIED = 0x801F0000
    UA_STATUSCODE_BADIDENTITYTOKENINVALID = 0x80200000
    UA_STATUSCODE_BADIDENTITYTOKENREJECTED = 0x80210000
    UA_STATUSCODE_BADSECURECHANNELIDINVALID = 0x80220000
    UA_STATUSCODE_BADINVALIDTIMESTAMP = 0x80230000
    UA_STATUSCODE_BADNONCEINVALID = 0x80240000
    UA_STATUSCODE_BADSESSIONIDINVALID = 0x80250000
    UA_STATUSCODE_BADSESSIONCLOSED = 0x80260000
    UA_STATUSCODE_BADSESSIONNOTACTIVATED = 0x80270000
    UA_STATUSCODE_BADSUBSCRIPTIONIDINVALID = 0x80280000
    UA_STATUSCODE_BADREQUESTHEADERINVALID = 0x802A0000
    UA_STATUSCODE_BADTIMESTAMPSTORETURNINVALID = 0x802B0000
    UA_STATUSCODE_BADREQUESTCANCELLEDBYCLIENT = 0x802C0000
    UA_STATUSCODE_BADTOOMANYARGUMENTS = 0x80E50000
    UA_STATUSCODE_BADLICENSEEXPIRED = 0x810E0000
    UA_STATUSCODE_BADLICENSELIMITSEXCEEDED = 0x810F0000
    UA_STATUSCODE_BADLICENSENOTAVAILABLE = 0x81100000
    UA_STATUSCODE_GOODSUBSCRIPTIONTRANSFERRED = 0x002D0000
    UA_STATUSCODE_GOODCOMPLETESASYNCHRONOUSLY = 0x002E0000
    UA_STATUSCODE_GOODOVERLOAD = 0x002F0000
    UA_STATUSCODE_GOODCLAMPED = 0x00300000
    UA_STATUSCODE_BADNOCOMMUNICATION = 0x80310000
    UA_STATUSCODE_BADWAITINGFORINITIALDATA = 0x80320000
    UA_STATUSCODE_BADNODEIDINVALID = 0x80330000
    UA_STATUSCODE_BADNODEIDUNKNOWN = 0x80340000
    UA_STATUSCODE_BADATTRIBUTEIDINVALID = 0x80350000
    UA_STATUSCODE_BADINDEXRANGEINVALID = 0x80360000
    UA_STATUSCODE_BADINDEXRANGENODATA = 0x80370000
    UA_STATUSCODE_BADDATAENCODINGINVALID = 0x80380000
    UA_STATUSCODE_BADDATAENCODINGUNSUPPORTED = 0x80390000
    UA_STATUSCODE_BADNOTREADABLE = 0x803A0000
    UA_STATUSCODE_BADNOTWRITABLE = 0x803B0000
    UA_STATUSCODE_BADOUTOFRANGE = 0x803C0000
    UA_STATUSCODE_BADNOTSUPPORTED = 0x803D0000
    UA_STATUSCODE_BADNOTFOUND = 0x803E0000
    UA_STATUSCODE_BADOBJECTDELETED = 0x803F0000
    UA_STATUSCODE_BADNOTIMPLEMENTED = 0x80400000
    UA_STATUSCODE_BADMONITORINGMODEINVALID = 0x80410000
    UA_STATUSCODE_BADMONITOREDITEMIDINVALID = 0x80420000
    UA_STATUSCODE_BADMONITOREDITEMFILTERINVALID = 0x80430000
    UA_STATUSCODE_BADMONITOREDITEMFILTERUNSUPPORTED = 0x80440000
    UA_STATUSCODE_BADFILTERNOTALLOWED = 0x80450000
    UA_STATUSCODE_BADSTRUCTUREMISSING = 0x80460000
    UA_STATUSCODE_BADEVENTFILTERINVALID = 0x80470000
    UA_STATUSCODE_BADCONTENTFILTERINVALID = 0x80480000
    UA_STATUSCODE_BADFILTEROPERATORINVALID = 0x80C10000
    UA_STATUSCODE_BADFILTEROPERATORUNSUPPORTED = 0x80C20000
    UA_STATUSCODE_BADFILTEROPERANDCOUNTMISMATCH = 0x80C30000
    UA_STATUSCODE_BADFILTEROPERANDINVALID = 0x80490000
    UA_STATUSCODE_BADFILTERELEMENTINVALID = 0x80C40000
    UA_STATUSCODE_BADFILTERLITERALINVALID = 0x80C50000
    UA_STATUSCODE_BADCONTINUATIONPOINTINVALID = 0x804A0000
    UA_STATUSCODE_BADNOCONTINUATIONPOINTS = 0x804B0000
    UA_STATUSCODE_BADREFERENCETYPEIDINVALID = 0x804C0000
    UA_STATUSCODE_BADBROWSEDIRECTIONINVALID = 0x804D0000
    UA_STATUSCODE_BADNODENOTINVIEW = 0x804E0000
    UA_STATUSCODE_BADNUMERICOVERFLOW = 0x81120000
    UA_STATUSCODE_BADSERVERURIINVALID = 0x804F0000
    UA_STATUSCODE_BADSERVERNAMEMISSING = 0x80500000
    UA_STATUSCODE_BADDISCOVERYURLMISSING = 0x80510000
    UA_STATUSCODE_BADSEMPAHOREFILEMISSING = 0x80520000
    UA_STATUSCODE_BADREQUESTTYPEINVALID = 0x80530000
    UA_STATUSCODE_BADSECURITYMODEREJECTED = 0x80540000
    UA_STATUSCODE_BADSECURITYPOLICYREJECTED = 0x80550000
    UA_STATUSCODE_BADTOOMANYSESSIONS = 0x80560000
    UA_STATUSCODE_BADUSERSIGNATUREINVALID = 0x80570000
    UA_STATUSCODE_BADAPPLICATIONSIGNATUREINVALID = 0x80580000
    UA_STATUSCODE_BADNOVALIDCERTIFICATES = 0x80590000
    UA_STATUSCODE_BADIDENTITYCHANGENOTSUPPORTED = 0x80C60000
    UA_STATUSCODE_BADREQUESTCANCELLEDBYREQUEST = 0x805A0000
    UA_STATUSCODE_BADPARENTNODEIDINVALID = 0x805B0000
    UA_STATUSCODE_BADREFERENCENOTALLOWED = 0x805C0000
    UA_STATUSCODE_BADNODEIDREJECTED = 0x805D0000
    UA_STATUSCODE_BADNODEIDEXISTS = 0x805E0000
    UA_STATUSCODE_BADNODECLASSINVALID = 0x805F0000
    UA_STATUSCODE_BADBROWSENAMEINVALID = 0x80600000
    UA_STATUSCODE_BADBROWSENAMEDUPLICATED = 0x80610000
    UA_STATUSCODE_BADNODEATTRIBUTESINVALID = 0x80620000
    UA_STATUSCODE_BADTYPEDEFINITIONINVALID = 0x80630000
    UA_STATUSCODE_BADSOURCENODEIDINVALID = 0x80640000
    UA_STATUSCODE_BADTARGETNODEIDINVALID = 0x80650000
    UA_STATUSCODE_BADDUPLICATEREFERENCENOTALLOWED = 0x80660000
    UA_STATUSCODE_BADINVALIDSELFREFERENCE = 0x80670000
    UA_STATUSCODE_BADREFERENCELOCALONLY = 0x80680000
    UA_STATUSCODE_BADNODELETERIGHTS = 0x80690000
    UA_STATUSCODE_UNCERTAINREFERENCENOTDELETED = 0x40BC0000
    UA_STATUSCODE_BADSERVERINDEXINVALID = 0x806A0000
    UA_STATUSCODE_BADVIEWIDUNKNOWN = 0x806B0000
    UA_STATUSCODE_BADVIEWTIMESTAMPINVALID = 0x80C90000
    UA_STATUSCODE_BADVIEWPARAMETERMISMATCH = 0x80CA0000
    UA_STATUSCODE_BADVIEWVERSIONINVALID = 0x80CB0000
    UA_STATUSCODE_UNCERTAINNOTALLNODESAVAILABLE = 0x40C00000
    UA_STATUSCODE_GOODRESULTSMAYBEINCOMPLETE = 0x00BA0000
    UA_STATUSCODE_BADNOTTYPEDEFINITION = 0x80C80000
    UA_STATUSCODE_UNCERTAINREFERENCEOUTOFSERVER = 0x406C0000
    UA_STATUSCODE_BADTOOMANYMATCHES = 0x806D0000
    UA_STATUSCODE_BADQUERYTOOCOMPLEX = 0x806E0000
    UA_STATUSCODE_BADNOMATCH = 0x806F0000
    UA_STATUSCODE_BADMAXAGEINVALID = 0x80700000
    UA_STATUSCODE_BADSECURITYMODEINSUFFICIENT = 0x80E60000
    UA_STATUSCODE_BADHISTORYOPERATIONINVALID = 0x80710000
    UA_STATUSCODE_BADHISTORYOPERATIONUNSUPPORTED = 0x80720000
    UA_STATUSCODE_BADINVALIDTIMESTAMPARGUMENT = 0x80BD0000
    UA_STATUSCODE_BADWRITENOTSUPPORTED = 0x80730000
    UA_STATUSCODE_BADTYPEMISMATCH = 0x80740000
    UA_STATUSCODE_BADMETHODINVALID = 0x80750000
    UA_STATUSCODE_BADARGUMENTSMISSING = 0x80760000
    UA_STATUSCODE_BADNOTEXECUTABLE = 0x81110000
    UA_STATUSCODE_BADTOOMANYSUBSCRIPTIONS = 0x80770000
    UA_STATUSCODE_BADTOOMANYPUBLISHREQUESTS = 0x80780000
    UA_STATUSCODE_BADNOSUBSCRIPTION = 0x80790000
    UA_STATUSCODE_BADSEQUENCENUMBERUNKNOWN = 0x807A0000
    UA_STATUSCODE_GOODRETRANSMISSIONQUEUENOTSUPPORTED = 0x00DF0000
    UA_STATUSCODE_BADMESSAGENOTAVAILABLE = 0x807B0000
    UA_STATUSCODE_BADINSUFFICIENTCLIENTPROFILE = 0x807C0000
    UA_STATUSCODE_BADSTATENOTACTIVE = 0x80BF0000
    UA_STATUSCODE_BADALREADYEXISTS = 0x81150000
    UA_STATUSCODE_BADTCPSERVERTOOBUSY = 0x807D0000
    UA_STATUSCODE_BADTCPMESSAGETYPEINVALID = 0x807E0000
    UA_STATUSCODE_BADTCPSECURECHANNELUNKNOWN = 0x807F0000
    UA_STATUSCODE_BADTCPMESSAGETOOLARGE = 0x80800000
    UA_STATUSCODE_BADTCPNOTENOUGHRESOURCES = 0x80810000
    UA_STATUSCODE_BADTCPINTERNALERROR = 0x80820000
    UA_STATUSCODE_BADTCPENDPOINTURLINVALID = 0x80830000
    UA_STATUSCODE_BADREQUESTINTERRUPTED = 0x80840000
    UA_STATUSCODE_BADREQUESTTIMEOUT = 0x80850000
    UA_STATUSCODE_BADSECURECHANNELCLOSED = 0x80860000
    UA_STATUSCODE_BADSECURECHANNELTOKENUNKNOWN = 0x80870000
    UA_STATUSCODE_BADSEQUENCENUMBERINVALID = 0x80880000
    UA_STATUSCODE_BADPROTOCOLVERSIONUNSUPPORTED = 0x80BE0000
    UA_STATUSCODE_BADCONFIGURATIONERROR = 0x80890000
    UA_STATUSCODE_BADNOTCONNECTED = 0x808A0000
    UA_STATUSCODE_BADDEVICEFAILURE = 0x808B0000
    UA_STATUSCODE_BADSENSORFAILURE = 0x808C0000
    UA_STATUSCODE_BADOUTOFSERVICE = 0x808D0000
    UA_STATUSCODE_BADDEADBANDFILTERINVALID = 0x808E0000
    UA_STATUSCODE_UNCERTAINNOCOMMUNICATIONLASTUSABLEVALUE = 0x408F0000
    UA_STATUSCODE_UNCERTAINLASTUSABLEVALUE = 0x40900000
    UA_STATUSCODE_UNCERTAINSUBSTITUTEVALUE = 0x40910000
    UA_STATUSCODE_UNCERTAININITIALVALUE = 0x40920000
    UA_STATUSCODE_UNCERTAINSENSORNOTACCURATE = 0x40930000
    UA_STATUSCODE_UNCERTAINENGINEERINGUNITSEXCEEDED = 0x40940000
    UA_STATUSCODE_UNCERTAINSUBNORMAL = 0x40950000
    UA_STATUSCODE_GOODLOCALOVERRIDE = 0x00960000
    UA_STATUSCODE_BADREFRESHINPROGRESS = 0x80970000
    UA_STATUSCODE_BADCONDITIONALREADYDISABLED = 0x80980000
    UA_STATUSCODE_BADCONDITIONALREADYENABLED = 0x80CC0000
    UA_STATUSCODE_BADCONDITIONDISABLED = 0x80990000
    UA_STATUSCODE_BADEVENTIDUNKNOWN = 0x809A0000
    UA_STATUSCODE_BADEVENTNOTACKNOWLEDGEABLE = 0x80BB0000
    UA_STATUSCODE_BADDIALOGNOTACTIVE = 0x80CD0000
    UA_STATUSCODE_BADDIALOGRESPONSEINVALID = 0x80CE0000
    UA_STATUSCODE_BADCONDITIONBRANCHALREADYACKED = 0x80CF0000
    UA_STATUSCODE_BADCONDITIONBRANCHALREADYCONFIRMED = 0x80D00000
    UA_STATUSCODE_BADCONDITIONALREADYSHELVED = 0x80D10000
    UA_STATUSCODE_BADCONDITIONNOTSHELVED = 0x80D20000
    UA_STATUSCODE_BADSHELVINGTIMEOUTOFRANGE = 0x80D30000
    UA_STATUSCODE_BADNODATA = 0x809B0000
    UA_STATUSCODE_BADBOUNDNOTFOUND = 0x80D70000
    UA_STATUSCODE_BADBOUNDNOTSUPPORTED = 0x80D80000
    UA_STATUSCODE_BADDATALOST = 0x809D0000
    UA_STATUSCODE_BADDATAUNAVAILABLE = 0x809E0000
    UA_STATUSCODE_BADENTRYEXISTS = 0x809F0000
    UA_STATUSCODE_BADNOENTRYEXISTS = 0x80A00000
    UA_STATUSCODE_BADTIMESTAMPNOTSUPPORTED = 0x80A10000
    UA_STATUSCODE_GOODENTRYINSERTED = 0x00A20000
    UA_STATUSCODE_GOODENTRYREPLACED = 0x00A30000
    UA_STATUSCODE_UNCERTAINDATASUBNORMAL = 0x40A40000
    UA_STATUSCODE_GOODNODATA = 0x00A50000
    UA_STATUSCODE_GOODMOREDATA = 0x00A60000
    UA_STATUSCODE_BADAGGREGATELISTMISMATCH = 0x80D40000
    UA_STATUSCODE_BADAGGREGATENOTSUPPORTED = 0x80D50000
    UA_STATUSCODE_BADAGGREGATEINVALIDINPUTS = 0x80D60000
    UA_STATUSCODE_BADAGGREGATECONFIGURATIONREJECTED = 0x80DA0000
    UA_STATUSCODE_GOODDATAIGNORED = 0x00D90000
    UA_STATUSCODE_BADREQUESTNOTALLOWED = 0x80E40000
    UA_STATUSCODE_BADREQUESTNOTCOMPLETE = 0x81130000
    UA_STATUSCODE_BADTICKETREQUIRED = 0x811F0000
    UA_STATUSCODE_BADTICKETINVALID = 0x81200000
    UA_STATUSCODE_GOODEDITED = 0x00DC0000
    UA_STATUSCODE_GOODPOSTACTIONFAILED = 0x00DD0000
    UA_STATUSCODE_UNCERTAINDOMINANTVALUECHANGED = 0x40DE0000
    UA_STATUSCODE_GOODDEPENDENTVALUECHANGED = 0x00E00000
    UA_STATUSCODE_BADDOMINANTVALUECHANGED = 0x80E10000
    UA_STATUSCODE_UNCERTAINDEPENDENTVALUECHANGED = 0x40E20000
    UA_STATUSCODE_BADDEPENDENTVALUECHANGED = 0x80E30000
    UA_STATUSCODE_GOODEDITED_DEPENDENTVALUECHANGED = 0x01160000
    UA_STATUSCODE_GOODEDITED_DOMINANTVALUECHANGED = 0x01170000
    UA_STATUSCODE_GOODEDITED_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED = 0x01180000
    UA_STATUSCODE_BADEDITED_OUTOFRANGE = 0x81190000
    UA_STATUSCODE_BADINITIALVALUE_OUTOFRANGE = 0x811A0000
    UA_STATUSCODE_BADOUTOFRANGE_DOMINANTVALUECHANGED = 0x811B0000
    UA_STATUSCODE_BADEDITED_OUTOFRANGE_DOMINANTVALUECHANGED = 0x811C0000
    UA_STATUSCODE_BADOUTOFRANGE_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED = 0x811D0000
    UA_STATUSCODE_BADEDITED_OUTOFRANGE_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED = 0x811E0000
    UA_STATUSCODE_GOODCOMMUNICATIONEVENT = 0x00A70000
    UA_STATUSCODE_GOODSHUTDOWNEVENT = 0x00A80000
    UA_STATUSCODE_GOODCALLAGAIN = 0x00A90000
    UA_STATUSCODE_GOODNONCRITICALTIMEOUT = 0x00AA0000
    UA_STATUSCODE_BADINVALIDARGUMENT = 0x80AB0000
    UA_STATUSCODE_BADCONNECTIONREJECTED = 0x80AC0000
    UA_STATUSCODE_BADDISCONNECT = 0x80AD0000
    UA_STATUSCODE_BADCONNECTIONCLOSED = 0x80AE0000
    UA_STATUSCODE_BADINVALIDSTATE = 0x80AF0000
    UA_STATUSCODE_BADENDOFSTREAM = 0x80B00000
    UA_STATUSCODE_BADNODATAAVAILABLE = 0x80B10000
    UA_STATUSCODE_BADWAITINGFORRESPONSE = 0x80B20000
    UA_STATUSCODE_BADOPERATIONABANDONED = 0x80B30000
    UA_STATUSCODE_BADEXPECTEDSTREAMTOBLOCK = 0x80B40000
    UA_STATUSCODE_BADWOULDBLOCK = 0x80B50000
    UA_STATUSCODE_BADSYNTAXERROR = 0x80B60000
    UA_STATUSCODE_BADMAXCONNECTIONSREACHED = 0x80B70000

    val_to_string = dict([
        (0x00000400, "UA_STATUSCODE_INFOTYPE_DATAVALUE"),
        (0x00000080, "UA_STATUSCODE_INFOBITS_OVERFLOW"),
        (0x00000000, "UA_STATUSCODE_GOOD"),
        (0x40000000, "UA_STATUSCODE_UNCERTAIN"),
        (0x80000000, "UA_STATUSCODE_BAD"),
        (0x80010000, "UA_STATUSCODE_BADUNEXPECTEDERROR"),
        (0x80020000, "UA_STATUSCODE_BADINTERNALERROR"),
        (0x80030000, "UA_STATUSCODE_BADOUTOFMEMORY"),
        (0x80040000, "UA_STATUSCODE_BADRESOURCEUNAVAILABLE"),
        (0x80050000, "UA_STATUSCODE_BADCOMMUNICATIONERROR"),
        (0x80060000, "UA_STATUSCODE_BADENCODINGERROR"),
        (0x80070000, "UA_STATUSCODE_BADDECODINGERROR"),
        (0x80080000, "UA_STATUSCODE_BADENCODINGLIMITSEXCEEDED"),
        (0x80B80000, "UA_STATUSCODE_BADREQUESTTOOLARGE"),
        (0x80B90000, "UA_STATUSCODE_BADRESPONSETOOLARGE"),
        (0x80090000, "UA_STATUSCODE_BADUNKNOWNRESPONSE"),
        (0x800A0000, "UA_STATUSCODE_BADTIMEOUT"),
        (0x800B0000, "UA_STATUSCODE_BADSERVICEUNSUPPORTED"),
        (0x800C0000, "UA_STATUSCODE_BADSHUTDOWN"),
        (0x800D0000, "UA_STATUSCODE_BADSERVERNOTCONNECTED"),
        (0x800E0000, "UA_STATUSCODE_BADSERVERHALTED"),
        (0x800F0000, "UA_STATUSCODE_BADNOTHINGTODO"),
        (0x80100000, "UA_STATUSCODE_BADTOOMANYOPERATIONS"),
        (0x80DB0000, "UA_STATUSCODE_BADTOOMANYMONITOREDITEMS"),
        (0x80110000, "UA_STATUSCODE_BADDATATYPEIDUNKNOWN"),
        (0x80120000, "UA_STATUSCODE_BADCERTIFICATEINVALID"),
        (0x80130000, "UA_STATUSCODE_BADSECURITYCHECKSFAILED"),
        (0x81140000, "UA_STATUSCODE_BADCERTIFICATEPOLICYCHECKFAILED"),
        (0x80140000, "UA_STATUSCODE_BADCERTIFICATETIMEINVALID"),
        (0x80150000, "UA_STATUSCODE_BADCERTIFICATEISSUERTIMEINVALID"),
        (0x80160000, "UA_STATUSCODE_BADCERTIFICATEHOSTNAMEINVALID"),
        (0x80170000, "UA_STATUSCODE_BADCERTIFICATEURIINVALID"),
        (0x80180000, "UA_STATUSCODE_BADCERTIFICATEUSENOTALLOWED"),
        (0x80190000, "UA_STATUSCODE_BADCERTIFICATEISSUERUSENOTALLOWED"),
        (0x801A0000, "UA_STATUSCODE_BADCERTIFICATEUNTRUSTED"),
        (0x801B0000, "UA_STATUSCODE_BADCERTIFICATEREVOCATIONUNKNOWN"),
        (0x801C0000, "UA_STATUSCODE_BADCERTIFICATEISSUERREVOCATIONUNKNOWN"),
        (0x801D0000, "UA_STATUSCODE_BADCERTIFICATEREVOKED"),
        (0x801E0000, "UA_STATUSCODE_BADCERTIFICATEISSUERREVOKED"),
        (0x810D0000, "UA_STATUSCODE_BADCERTIFICATECHAININCOMPLETE"),
        (0x801F0000, "UA_STATUSCODE_BADUSERACCESSDENIED"),
        (0x80200000, "UA_STATUSCODE_BADIDENTITYTOKENINVALID"),
        (0x80210000, "UA_STATUSCODE_BADIDENTITYTOKENREJECTED"),
        (0x80220000, "UA_STATUSCODE_BADSECURECHANNELIDINVALID"),
        (0x80230000, "UA_STATUSCODE_BADINVALIDTIMESTAMP"),
        (0x80240000, "UA_STATUSCODE_BADNONCEINVALID"),
        (0x80250000, "UA_STATUSCODE_BADSESSIONIDINVALID"),
        (0x80260000, "UA_STATUSCODE_BADSESSIONCLOSED"),
        (0x80270000, "UA_STATUSCODE_BADSESSIONNOTACTIVATED"),
        (0x80280000, "UA_STATUSCODE_BADSUBSCRIPTIONIDINVALID"),
        (0x802A0000, "UA_STATUSCODE_BADREQUESTHEADERINVALID"),
        (0x802B0000, "UA_STATUSCODE_BADTIMESTAMPSTORETURNINVALID"),
        (0x802C0000, "UA_STATUSCODE_BADREQUESTCANCELLEDBYCLIENT"),
        (0x80E50000, "UA_STATUSCODE_BADTOOMANYARGUMENTS"),
        (0x810E0000, "UA_STATUSCODE_BADLICENSEEXPIRED"),
        (0x810F0000, "UA_STATUSCODE_BADLICENSELIMITSEXCEEDED"),
        (0x81100000, "UA_STATUSCODE_BADLICENSENOTAVAILABLE"),
        (0x002D0000, "UA_STATUSCODE_GOODSUBSCRIPTIONTRANSFERRED"),
        (0x002E0000, "UA_STATUSCODE_GOODCOMPLETESASYNCHRONOUSLY"),
        (0x002F0000, "UA_STATUSCODE_GOODOVERLOAD"),
        (0x00300000, "UA_STATUSCODE_GOODCLAMPED"),
        (0x80310000, "UA_STATUSCODE_BADNOCOMMUNICATION"),
        (0x80320000, "UA_STATUSCODE_BADWAITINGFORINITIALDATA"),
        (0x80330000, "UA_STATUSCODE_BADNODEIDINVALID"),
        (0x80340000, "UA_STATUSCODE_BADNODEIDUNKNOWN"),
        (0x80350000, "UA_STATUSCODE_BADATTRIBUTEIDINVALID"),
        (0x80360000, "UA_STATUSCODE_BADINDEXRANGEINVALID"),
        (0x80370000, "UA_STATUSCODE_BADINDEXRANGENODATA"),
        (0x80380000, "UA_STATUSCODE_BADDATAENCODINGINVALID"),
        (0x80390000, "UA_STATUSCODE_BADDATAENCODINGUNSUPPORTED"),
        (0x803A0000, "UA_STATUSCODE_BADNOTREADABLE"),
        (0x803B0000, "UA_STATUSCODE_BADNOTWRITABLE"),
        (0x803C0000, "UA_STATUSCODE_BADOUTOFRANGE"),
        (0x803D0000, "UA_STATUSCODE_BADNOTSUPPORTED"),
        (0x803E0000, "UA_STATUSCODE_BADNOTFOUND"),
        (0x803F0000, "UA_STATUSCODE_BADOBJECTDELETED"),
        (0x80400000, "UA_STATUSCODE_BADNOTIMPLEMENTED"),
        (0x80410000, "UA_STATUSCODE_BADMONITORINGMODEINVALID"),
        (0x80420000, "UA_STATUSCODE_BADMONITOREDITEMIDINVALID"),
        (0x80430000, "UA_STATUSCODE_BADMONITOREDITEMFILTERINVALID"),
        (0x80440000, "UA_STATUSCODE_BADMONITOREDITEMFILTERUNSUPPORTED"),
        (0x80450000, "UA_STATUSCODE_BADFILTERNOTALLOWED"),
        (0x80460000, "UA_STATUSCODE_BADSTRUCTUREMISSING"),
        (0x80470000, "UA_STATUSCODE_BADEVENTFILTERINVALID"),
        (0x80480000, "UA_STATUSCODE_BADCONTENTFILTERINVALID"),
        (0x80C10000, "UA_STATUSCODE_BADFILTEROPERATORINVALID"),
        (0x80C20000, "UA_STATUSCODE_BADFILTEROPERATORUNSUPPORTED"),
        (0x80C30000, "UA_STATUSCODE_BADFILTEROPERANDCOUNTMISMATCH"),
        (0x80490000, "UA_STATUSCODE_BADFILTEROPERANDINVALID"),
        (0x80C40000, "UA_STATUSCODE_BADFILTERELEMENTINVALID"),
        (0x80C50000, "UA_STATUSCODE_BADFILTERLITERALINVALID"),
        (0x804A0000, "UA_STATUSCODE_BADCONTINUATIONPOINTINVALID"),
        (0x804B0000, "UA_STATUSCODE_BADNOCONTINUATIONPOINTS"),
        (0x804C0000, "UA_STATUSCODE_BADREFERENCETYPEIDINVALID"),
        (0x804D0000, "UA_STATUSCODE_BADBROWSEDIRECTIONINVALID"),
        (0x804E0000, "UA_STATUSCODE_BADNODENOTINVIEW"),
        (0x81120000, "UA_STATUSCODE_BADNUMERICOVERFLOW"),
        (0x804F0000, "UA_STATUSCODE_BADSERVERURIINVALID"),
        (0x80500000, "UA_STATUSCODE_BADSERVERNAMEMISSING"),
        (0x80510000, "UA_STATUSCODE_BADDISCOVERYURLMISSING"),
        (0x80520000, "UA_STATUSCODE_BADSEMPAHOREFILEMISSING"),
        (0x80530000, "UA_STATUSCODE_BADREQUESTTYPEINVALID"),
        (0x80540000, "UA_STATUSCODE_BADSECURITYMODEREJECTED"),
        (0x80550000, "UA_STATUSCODE_BADSECURITYPOLICYREJECTED"),
        (0x80560000, "UA_STATUSCODE_BADTOOMANYSESSIONS"),
        (0x80570000, "UA_STATUSCODE_BADUSERSIGNATUREINVALID"),
        (0x80580000, "UA_STATUSCODE_BADAPPLICATIONSIGNATUREINVALID"),
        (0x80590000, "UA_STATUSCODE_BADNOVALIDCERTIFICATES"),
        (0x80C60000, "UA_STATUSCODE_BADIDENTITYCHANGENOTSUPPORTED"),
        (0x805A0000, "UA_STATUSCODE_BADREQUESTCANCELLEDBYREQUEST"),
        (0x805B0000, "UA_STATUSCODE_BADPARENTNODEIDINVALID"),
        (0x805C0000, "UA_STATUSCODE_BADREFERENCENOTALLOWED"),
        (0x805D0000, "UA_STATUSCODE_BADNODEIDREJECTED"),
        (0x805E0000, "UA_STATUSCODE_BADNODEIDEXISTS"),
        (0x805F0000, "UA_STATUSCODE_BADNODECLASSINVALID"),
        (0x80600000, "UA_STATUSCODE_BADBROWSENAMEINVALID"),
        (0x80610000, "UA_STATUSCODE_BADBROWSENAMEDUPLICATED"),
        (0x80620000, "UA_STATUSCODE_BADNODEATTRIBUTESINVALID"),
        (0x80630000, "UA_STATUSCODE_BADTYPEDEFINITIONINVALID"),
        (0x80640000, "UA_STATUSCODE_BADSOURCENODEIDINVALID"),
        (0x80650000, "UA_STATUSCODE_BADTARGETNODEIDINVALID"),
        (0x80660000, "UA_STATUSCODE_BADDUPLICATEREFERENCENOTALLOWED"),
        (0x80670000, "UA_STATUSCODE_BADINVALIDSELFREFERENCE"),
        (0x80680000, "UA_STATUSCODE_BADREFERENCELOCALONLY"),
        (0x80690000, "UA_STATUSCODE_BADNODELETERIGHTS"),
        (0x40BC0000, "UA_STATUSCODE_UNCERTAINREFERENCENOTDELETED"),
        (0x806A0000, "UA_STATUSCODE_BADSERVERINDEXINVALID"),
        (0x806B0000, "UA_STATUSCODE_BADVIEWIDUNKNOWN"),
        (0x80C90000, "UA_STATUSCODE_BADVIEWTIMESTAMPINVALID"),
        (0x80CA0000, "UA_STATUSCODE_BADVIEWPARAMETERMISMATCH"),
        (0x80CB0000, "UA_STATUSCODE_BADVIEWVERSIONINVALID"),
        (0x40C00000, "UA_STATUSCODE_UNCERTAINNOTALLNODESAVAILABLE"),
        (0x00BA0000, "UA_STATUSCODE_GOODRESULTSMAYBEINCOMPLETE"),
        (0x80C80000, "UA_STATUSCODE_BADNOTTYPEDEFINITION"),
        (0x406C0000, "UA_STATUSCODE_UNCERTAINREFERENCEOUTOFSERVER"),
        (0x806D0000, "UA_STATUSCODE_BADTOOMANYMATCHES"),
        (0x806E0000, "UA_STATUSCODE_BADQUERYTOOCOMPLEX"),
        (0x806F0000, "UA_STATUSCODE_BADNOMATCH"),
        (0x80700000, "UA_STATUSCODE_BADMAXAGEINVALID"),
        (0x80E60000, "UA_STATUSCODE_BADSECURITYMODEINSUFFICIENT"),
        (0x80710000, "UA_STATUSCODE_BADHISTORYOPERATIONINVALID"),
        (0x80720000, "UA_STATUSCODE_BADHISTORYOPERATIONUNSUPPORTED"),
        (0x80BD0000, "UA_STATUSCODE_BADINVALIDTIMESTAMPARGUMENT"),
        (0x80730000, "UA_STATUSCODE_BADWRITENOTSUPPORTED"),
        (0x80740000, "UA_STATUSCODE_BADTYPEMISMATCH"),
        (0x80750000, "UA_STATUSCODE_BADMETHODINVALID"),
        (0x80760000, "UA_STATUSCODE_BADARGUMENTSMISSING"),
        (0x81110000, "UA_STATUSCODE_BADNOTEXECUTABLE"),
        (0x80770000, "UA_STATUSCODE_BADTOOMANYSUBSCRIPTIONS"),
        (0x80780000, "UA_STATUSCODE_BADTOOMANYPUBLISHREQUESTS"),
        (0x80790000, "UA_STATUSCODE_BADNOSUBSCRIPTION"),
        (0x807A0000, "UA_STATUSCODE_BADSEQUENCENUMBERUNKNOWN"),
        (0x00DF0000, "UA_STATUSCODE_GOODRETRANSMISSIONQUEUENOTSUPPORTED"),
        (0x807B0000, "UA_STATUSCODE_BADMESSAGENOTAVAILABLE"),
        (0x807C0000, "UA_STATUSCODE_BADINSUFFICIENTCLIENTPROFILE"),
        (0x80BF0000, "UA_STATUSCODE_BADSTATENOTACTIVE"),
        (0x81150000, "UA_STATUSCODE_BADALREADYEXISTS"),
        (0x807D0000, "UA_STATUSCODE_BADTCPSERVERTOOBUSY"),
        (0x807E0000, "UA_STATUSCODE_BADTCPMESSAGETYPEINVALID"),
        (0x807F0000, "UA_STATUSCODE_BADTCPSECURECHANNELUNKNOWN"),
        (0x80800000, "UA_STATUSCODE_BADTCPMESSAGETOOLARGE"),
        (0x80810000, "UA_STATUSCODE_BADTCPNOTENOUGHRESOURCES"),
        (0x80820000, "UA_STATUSCODE_BADTCPINTERNALERROR"),
        (0x80830000, "UA_STATUSCODE_BADTCPENDPOINTURLINVALID"),
        (0x80840000, "UA_STATUSCODE_BADREQUESTINTERRUPTED"),
        (0x80850000, "UA_STATUSCODE_BADREQUESTTIMEOUT"),
        (0x80860000, "UA_STATUSCODE_BADSECURECHANNELCLOSED"),
        (0x80870000, "UA_STATUSCODE_BADSECURECHANNELTOKENUNKNOWN"),
        (0x80880000, "UA_STATUSCODE_BADSEQUENCENUMBERINVALID"),
        (0x80BE0000, "UA_STATUSCODE_BADPROTOCOLVERSIONUNSUPPORTED"),
        (0x80890000, "UA_STATUSCODE_BADCONFIGURATIONERROR"),
        (0x808A0000, "UA_STATUSCODE_BADNOTCONNECTED"),
        (0x808B0000, "UA_STATUSCODE_BADDEVICEFAILURE"),
        (0x808C0000, "UA_STATUSCODE_BADSENSORFAILURE"),
        (0x808D0000, "UA_STATUSCODE_BADOUTOFSERVICE"),
        (0x808E0000, "UA_STATUSCODE_BADDEADBANDFILTERINVALID"),
        (0x408F0000, "UA_STATUSCODE_UNCERTAINNOCOMMUNICATIONLASTUSABLEVALUE"),
        (0x40900000, "UA_STATUSCODE_UNCERTAINLASTUSABLEVALUE"),
        (0x40910000, "UA_STATUSCODE_UNCERTAINSUBSTITUTEVALUE"),
        (0x40920000, "UA_STATUSCODE_UNCERTAININITIALVALUE"),
        (0x40930000, "UA_STATUSCODE_UNCERTAINSENSORNOTACCURATE"),
        (0x40940000, "UA_STATUSCODE_UNCERTAINENGINEERINGUNITSEXCEEDED"),
        (0x40950000, "UA_STATUSCODE_UNCERTAINSUBNORMAL"),
        (0x00960000, "UA_STATUSCODE_GOODLOCALOVERRIDE"),
        (0x80970000, "UA_STATUSCODE_BADREFRESHINPROGRESS"),
        (0x80980000, "UA_STATUSCODE_BADCONDITIONALREADYDISABLED"),
        (0x80CC0000, "UA_STATUSCODE_BADCONDITIONALREADYENABLED"),
        (0x80990000, "UA_STATUSCODE_BADCONDITIONDISABLED"),
        (0x809A0000, "UA_STATUSCODE_BADEVENTIDUNKNOWN"),
        (0x80BB0000, "UA_STATUSCODE_BADEVENTNOTACKNOWLEDGEABLE"),
        (0x80CD0000, "UA_STATUSCODE_BADDIALOGNOTACTIVE"),
        (0x80CE0000, "UA_STATUSCODE_BADDIALOGRESPONSEINVALID"),
        (0x80CF0000, "UA_STATUSCODE_BADCONDITIONBRANCHALREADYACKED"),
        (0x80D00000, "UA_STATUSCODE_BADCONDITIONBRANCHALREADYCONFIRMED"),
        (0x80D10000, "UA_STATUSCODE_BADCONDITIONALREADYSHELVED"),
        (0x80D20000, "UA_STATUSCODE_BADCONDITIONNOTSHELVED"),
        (0x80D30000, "UA_STATUSCODE_BADSHELVINGTIMEOUTOFRANGE"),
        (0x809B0000, "UA_STATUSCODE_BADNODATA"),
        (0x80D70000, "UA_STATUSCODE_BADBOUNDNOTFOUND"),
        (0x80D80000, "UA_STATUSCODE_BADBOUNDNOTSUPPORTED"),
        (0x809D0000, "UA_STATUSCODE_BADDATALOST"),
        (0x809E0000, "UA_STATUSCODE_BADDATAUNAVAILABLE"),
        (0x809F0000, "UA_STATUSCODE_BADENTRYEXISTS"),
        (0x80A00000, "UA_STATUSCODE_BADNOENTRYEXISTS"),
        (0x80A10000, "UA_STATUSCODE_BADTIMESTAMPNOTSUPPORTED"),
        (0x00A20000, "UA_STATUSCODE_GOODENTRYINSERTED"),
        (0x00A30000, "UA_STATUSCODE_GOODENTRYREPLACED"),
        (0x40A40000, "UA_STATUSCODE_UNCERTAINDATASUBNORMAL"),
        (0x00A50000, "UA_STATUSCODE_GOODNODATA"),
        (0x00A60000, "UA_STATUSCODE_GOODMOREDATA"),
        (0x80D40000, "UA_STATUSCODE_BADAGGREGATELISTMISMATCH"),
        (0x80D50000, "UA_STATUSCODE_BADAGGREGATENOTSUPPORTED"),
        (0x80D60000, "UA_STATUSCODE_BADAGGREGATEINVALIDINPUTS"),
        (0x80DA0000, "UA_STATUSCODE_BADAGGREGATECONFIGURATIONREJECTED"),
        (0x00D90000, "UA_STATUSCODE_GOODDATAIGNORED"),
        (0x80E40000, "UA_STATUSCODE_BADREQUESTNOTALLOWED"),
        (0x81130000, "UA_STATUSCODE_BADREQUESTNOTCOMPLETE"),
        (0x811F0000, "UA_STATUSCODE_BADTICKETREQUIRED"),
        (0x81200000, "UA_STATUSCODE_BADTICKETINVALID"),
        (0x00DC0000, "UA_STATUSCODE_GOODEDITED"),
        (0x00DD0000, "UA_STATUSCODE_GOODPOSTACTIONFAILED"),
        (0x40DE0000, "UA_STATUSCODE_UNCERTAINDOMINANTVALUECHANGED"),
        (0x00E00000, "UA_STATUSCODE_GOODDEPENDENTVALUECHANGED"),
        (0x80E10000, "UA_STATUSCODE_BADDOMINANTVALUECHANGED"),
        (0x40E20000, "UA_STATUSCODE_UNCERTAINDEPENDENTVALUECHANGED"),
        (0x80E30000, "UA_STATUSCODE_BADDEPENDENTVALUECHANGED"),
        (0x01160000, "UA_STATUSCODE_GOODEDITED_DEPENDENTVALUECHANGED"),
        (0x01170000, "UA_STATUSCODE_GOODEDITED_DOMINANTVALUECHANGED"),
        (0x01180000, "UA_STATUSCODE_GOODEDITED_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED"),
        (0x81190000, "UA_STATUSCODE_BADEDITED_OUTOFRANGE"),
        (0x811A0000, "UA_STATUSCODE_BADINITIALVALUE_OUTOFRANGE"),
        (0x811B0000, "UA_STATUSCODE_BADOUTOFRANGE_DOMINANTVALUECHANGED"),
        (0x811C0000, "UA_STATUSCODE_BADEDITED_OUTOFRANGE_DOMINANTVALUECHANGED"),
        (0x811D0000, "UA_STATUSCODE_BADOUTOFRANGE_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED"),
        (0x811E0000, "UA_STATUSCODE_BADEDITED_OUTOFRANGE_DOMINANTVALUECHANGED_DEPENDENTVALUECHANGED"),
        (0x00A70000, "UA_STATUSCODE_GOODCOMMUNICATIONEVENT"),
        (0x00A80000, "UA_STATUSCODE_GOODSHUTDOWNEVENT"),
        (0x00A90000, "UA_STATUSCODE_GOODCALLAGAIN"),
        (0x00AA0000, "UA_STATUSCODE_GOODNONCRITICALTIMEOUT"),
        (0x80AB0000, "UA_STATUSCODE_BADINVALIDARGUMENT"),
        (0x80AC0000, "UA_STATUSCODE_BADCONNECTIONREJECTED"),
        (0x80AD0000, "UA_STATUSCODE_BADDISCONNECT"),
        (0x80AE0000, "UA_STATUSCODE_BADCONNECTIONCLOSED"),
        (0x80AF0000, "UA_STATUSCODE_BADINVALIDSTATE"),
        (0x80B00000, "UA_STATUSCODE_BADENDOFSTREAM"),
        (0x80B10000, "UA_STATUSCODE_BADNODATAAVAILABLE"),
        (0x80B20000, "UA_STATUSCODE_BADWAITINGFORRESPONSE"),
        (0x80B30000, "UA_STATUSCODE_BADOPERATIONABANDONED"),
        (0x80B40000, "UA_STATUSCODE_BADEXPECTEDSTREAMTOBLOCK"),
        (0x80B50000, "UA_STATUSCODE_BADWOULDBLOCK"),
        (0x80B60000, "UA_STATUSCODE_BADSYNTAXERROR"),
        (0x80B70000, "UA_STATUSCODE_BADMAXCONNECTIONSREACHED")])

    def __init__(self, val: Union[Void, int, List[int]] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("UA_StatusCode*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_StatusCode*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_StatusCode[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_StatusCode*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_StatusCode")
        else:
            self._value[0] = ffi.cast("UA_StatusCode", _val(val))

    def __str__(self, n=0):
        if self._null:
            return "(UaStatusCode) : NULL\n"
        else:
            return "(UaStatusCode): " + UaStatusCode.val_to_string[self._val] + "\n"

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val

    def __gt__(self, other):
        return self._val > other._val

    def __lt__(self, other):
        return self._val < other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __le__(self, other):
        return self._val <= other._val

    def is_bad(self):
        return lib.UA_StatusCode_isBad(self._val)

    def is_good(self):
        return not lib.UA_StatusCode_isBad(self._val)