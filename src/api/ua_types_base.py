# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#    Copyright 2021 Christian Lange, Stella Maidorn, Daniel Nier
from typing import Any
from ua_consts_data_types import *
from intermediateApi import ffi, lib
from ua_types_primitve import *
from ua_types_list import *
from ua_types_parent import _ptr, _val, _is_null, _is_ptr


# -------------------------------------------------------------
# --------------------------- Enums ---------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaNodeIdType +++++++++++++++++++++++
class UaNodeIdType(UaType):
    val_to_string = dict([
        (0, "UA_NODEIDTYPE_NUMERIC"),
        (3, "UA_NODEIDTYPE_STRING"),
        (4, "UA_NODEIDTYPE_GUID"),
        (5, "UA_NODEIDTYPE_BYTESTRING")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("enum UA_NodeIdType*", val._ptr)
        if val is None:
            super().__init__(ffi.new("enum UA_NodeIdType*"), is_pointer)
        else:
            super().__init__(ffi.cast("enum UA_NodeIdType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "enum UA_NodeIdType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def NUMERIC():
        return UaNodeIdType(0)

    @staticmethod
    def STRING():
        return UaNodeIdType(3)

    @staticmethod
    def GUID():
        return UaNodeIdType(4)

    @staticmethod
    def BYTESTRING():
        return UaNodeIdType(5)

    def __str__(self, n=0):
        return f"(UaNodeIdType): {self.val_to_string[self._val]} ({str(self._val)})\n"


# +++++++++++++++++++ UaVariantStorageType +++++++++++++++++++++++
class UaVariantStorageType(UaType):
    val_to_string = dict([
        (0, "UA_VARIANT_DATA"),
        (1, "UA_VARIANT_DATA_NODELETE")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_VariantStorageType*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_VariantStorageType*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_VariantStorageType", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_VariantStorageType")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def DATA():
        return UaVariantStorageType(0)

    @staticmethod
    def DATA_NODELETE():
        return UaVariantStorageType(1)

    def __str__(self, n=0):
        return f"(UaVariantStorageType): {self.val_to_string[self._val]} ({str(self._val)})\n"

# +++++++++++++++++++ UaExtensionObjectEncoding +++++++++++++++++++++++
class UaExtensionObjectEncoding(UaType):
    val_to_string = dict([
        (0, "UA_EXTENSIONOBJECT_ENCODED_NOBODY"),
        (1, "UA_EXTENSIONOBJECT_ENCODED_BYTESTRING"),
        (2, "UA_EXTENSIONOBJECT_ENCODED_XML"),
        (3, "UA_EXTENSIONOBJECT_DECODED"),
        (4, "UA_EXTENSIONOBJECT_DECODED_NODELETE")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_ExtensionObjectEncoding*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_ExtensionObjectEncoding*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_ExtensionObjectEncoding", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_ExtensionObjectEncoding")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def ENCODED_NOBODY():
        return UaExtensionObjectEncoding(0)

    @staticmethod
    def ENCODED_BYTESTRING():
        return UaExtensionObjectEncoding(1)

    @staticmethod
    def ENCODED_XML():
        return UaExtensionObjectEncoding(2)

    @staticmethod
    def DECODED():
        return UaExtensionObjectEncoding(3)

    @staticmethod
    def DECODED_NODELETE():
        return UaExtensionObjectEncoding(4)

    def __str__(self, n=0):
        return f"(UaExtensionObjectEncoding): {self.val_to_string[self._val]} ({str(self._val)})\n"

# +++++++++++++++++++ UaDataTypeKind +++++++++++++++++++++++
class UaDataTypeKind(UaType):
    val_to_string = dict([
            (0, "UA_DATATYPEKIND_BOOLEAN"),
            (1, "UA_DATATYPEKIND_SBYTE"),
            (2, "UA_DATATYPEKIND_BYTE"),
            (3, "UA_DATATYPEKIND_INT16"),
            (4, "UA_DATATYPEKIND_UINT16"),
            (5, "UA_DATATYPEKIND_INT32"),
            (6, "UA_DATATYPEKIND_UINT32"),
            (7, "UA_DATATYPEKIND_INT64"),
            (8, "UA_DATATYPEKIND_UINT64"),
            (9, "UA_DATATYPEKIND_FLOAT"),
            (10, "UA_DATATYPEKIND_DOUBLE"),
            (11, "UA_DATATYPEKIND_STRING"),
            (12, "UA_DATATYPEKIND_DATETIME"),
            (13, "UA_DATATYPEKIND_GUID"),
            (14, "UA_DATATYPEKIND_BYTESTRING"),
            (15, "UA_DATATYPEKIND_XMLELEMENT"),
            (16, "UA_DATATYPEKIND_NODEID"),
            (17, "UA_DATATYPEKIND_EXPANDEDNODEID"),
            (18, "UA_DATATYPEKIND_STATUSCODE"),
            (19, "UA_DATATYPEKIND_QUALIFIEDNAME"),
            (20, "UA_DATATYPEKIND_LOCALIZEDTEXT"),
            (21, "UA_DATATYPEKIND_EXTENSIONOBJECT"),
            (22, "UA_DATATYPEKIND_DATAVALUE"),
            (23, "UA_DATATYPEKIND_VARIANT"),
            (24, "UA_DATATYPEKIND_DIAGNOSTICINFO"),
            (25, "UA_DATATYPEKIND_DECIMAL"),
            (26, "UA_DATATYPEKIND_ENUM"),
            (27, "UA_DATATYPEKIND_STRUCTURE"),
            (28, "UA_DATATYPEKIND_OPTSTRUCT"),
            (29, "UA_DATATYPEKIND_UNION"),
            (30, "UA_DATATYPEKIND_BITFIELDCLUSTER")])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_DataTypeKind*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_DataTypeKind*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_DataTypeKind", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "UA_DataTypeKind")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    @staticmethod
    def BOOLEAN():
        return UaDataTypeKind(0)

    @staticmethod
    def SBYTE():
        return UaDataTypeKind(1)

    @staticmethod
    def BYTE():
        return UaDataTypeKind(2)

    @staticmethod
    def INT16():
        return UaDataTypeKind(3)

    @staticmethod
    def UINT16():
        return UaDataTypeKind(4)

    @staticmethod
    def INT32():
        return UaDataTypeKind(5)

    @staticmethod
    def UINT32():
        return UaDataTypeKind(6)

    @staticmethod
    def INT64():
        return UaDataTypeKind(7)

    @staticmethod
    def UINT64():
        return UaDataTypeKind(8)

    @staticmethod
    def FLOAT():
        return UaDataTypeKind(9)

    @staticmethod
    def DOUBLE():
        return UaDataTypeKind(10)

    @staticmethod
    def STRING():
        return UaDataTypeKind(11)

    @staticmethod
    def DATETIME():
        return UaDataTypeKind(12)

    @staticmethod
    def GUID():
        return UaDataTypeKind(13)

    @staticmethod
    def BYTESTRING():
        return UaDataTypeKind(14)

    @staticmethod
    def XMLELEMENT():
        return UaDataTypeKind(15)

    @staticmethod
    def NODEID():
        return UaDataTypeKind(16)

    @staticmethod
    def EXPANDEDNODEID():
        return UaDataTypeKind(17)

    @staticmethod
    def STATUSCODE():
        return UaDataTypeKind(18)

    @staticmethod
    def QUALIFIEDNAME():
        return UaDataTypeKind(19)

    @staticmethod
    def LOCALIZEDTEXT():
        return UaDataTypeKind(20)

    @staticmethod
    def EXTENSIONOBJECT():
        return UaDataTypeKind(21)

    @staticmethod
    def DATAVALUE():
        return UaDataTypeKind(22)

    @staticmethod
    def VARIANT():
        return UaDataTypeKind(23)

    @staticmethod
    def DIAGNOSTICINFO():
        return UaDataTypeKind(24)

    @staticmethod
    def DECIMAL():
        return UaDataTypeKind(25)

    @staticmethod
    def ENUM():
        return UaDataTypeKind(26)

    @staticmethod
    def STRUCTURE():
        return UaDataTypeKind(27)

    @staticmethod
    def OPTSTRUCT():
        return UaDataTypeKind(28)

    @staticmethod
    def UNION():
        return UaDataTypeKind(29)

    @staticmethod
    def BITFIELDCLUSTER():
        return UaDataTypeKind(30)

    def __str__(self, n=0):
        return f"(UaDataTypeKind): {self.val_to_string[self._val]} ({str(self._val)})\n"


# -------------------------------------------------------------
# -------------------------- Structs --------------------------
# -------------------------------------------------------------

# +++++++++++++++++++ UaString +++++++++++++++++++++++
class UaString(UaType):
    UA_TYPE = UA_TYPES.STRING

    def __init__(self, val: Union[str, Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_String*", val._ptr)
        elif type(val) is str or type(val) is bytes:
            val = ffi.new("UA_String*", lib.UA_String_fromChars(bytes(val, 'utf-8')))
        elif type(val) is not None:
            if not is_pointer:
                val = ffi.new("UA_String*", val)
        else:
            val = ffi.new("UA_String*")

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._length = SizeT(val=val.length, is_pointer=False)
            self._data = UaByte(val=val.data, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    # TODO: Rather make new UaString?
    #   -> not sure where the pointer is directed and if there is enough memory for evtually more bytes than befor
    #   -> memory management for alloced memory from UA_String_fromChars

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_String")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._length._value[0] = _val(val.length)
            self._data._value = val.data

    @property
    def length(self):
        if self._null:
            return None
        else:
            return self._length

    @property
    def data(self):
        if self._null:
            return None
        else:
            return self._data

    def __eq__(self, ua_string):
        return lib.UA_String_equal(self._ptr, ua_string._ptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return UaString(self.value + other.value)

    def __mul__(self, other: int):
        return UaString(self.value * other)

    def equal_ignore_case(self, ua_string):
        return lib.UA_String_equal_ignorecase(self._ptr, ua_string._ptr)

    @property
    def value(self) -> str:
        if self._null:
            return "NULL"
        return ffi.string(ffi.cast(f"char[{self.length._val}]", self.data._ptr), self.length._val).decode("utf-8")

    def __str__(self, n=0):
        return "(UaString): " + self.value + "\n"


# +++++++++++++++++++ UaByteString +++++++++++++++++++++++
UaByteString = UaString

# +++++++++++++++++++ UaXmlElement +++++++++++++++++++++++
UaXmlElement = UaString


# +++++++++++++++++++ UaDateTime +++++++++++++++++++++++
class UaDateTime(UaType):
    UA_TYPE = UA_TYPES.DATETIME

    def __init__(self, val: Union[int, List[int], Void] = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_DateTime*", val._ptr)
        if val is None:
            super().__init__(ffi.new("UA_DateTime*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("UA_DateTime[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("UA_DateTime*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DateTime")
        else:
            self._value[0] = ffi.cast("UA_DateTime", _val(val))

    def __str__(self, n=0):
        return "(UaDateTime): " + str(self._val) + "\n"

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

    def to_struct(self):
        return UaDateTimeStruct(val=lib.UA_DateTime_toStruct(self._val))

    @staticmethod
    def now():
        return UaDateTime(lib.UA_DateTime_now())


# +++++++++++++++++++ UaDateTimeStruct +++++++++++++++++++++++
# TODO: Methods from types.h
class UaDateTimeStruct(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DateTimeStruct*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DateTimeStruct*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._nano_sec = UaUInt16(val=val.nanoSec, is_pointer=False)
            self._micro_sec = UaUInt16(val=val.microSec, is_pointer=False)
            self._milli_sec = UaUInt16(val=val.milliSec, is_pointer=False)
            self._sec = UaUInt16(val=val.sec, is_pointer=False)
            self._min = UaUInt16(val=val.min, is_pointer=False)
            self._hour = UaUInt16(val=val.hour, is_pointer=False)
            self._day = UaUInt16(val=val.day, is_pointer=False)
            self._month = UaUInt16(val=val.month, is_pointer=False)
            self._year = UaUInt16(val=val.year, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self.__value = _ptr(val, "UA_DateTimeStruct")
        else:
            self.__value[0] = _val(val)

        if not _is_null(val):
            self._nano_sec._value[0] = _val(val.nanoSec)
            self._micro_sec._value[0] = _val(val.microSec)
            self._milli_sec._value[0] = _val(val.milliSec)
            self._sec._value[0] = _val(val.sec)
            self._min._value[0] = _val(val.min)
            self._hour._value[0] = _val(val.hour)
            self._day._value[0] = _val(val.day)
            self._month._value[0] = _val(val.month)
            self._year._value[0] = _val(val.year)

    @property
    def nano_sec(self):
        if self._null:
            return None
        else:
            return self._nano_sec

    @property
    def micro_sec(self):
        if self._null:
            return None
        else:
            return self._micro_sec

    @property
    def milli_sec(self):
        if self._null:
            return None
        else:
            return self._milli_sec

    @property
    def sec(self):
        if self._null:
            return None
        else:
            return self._sec

    @property
    def min(self):
        if self._null:
            return None
        else:
            return self._min

    @property
    def hour(self):
        if self._null:
            return None
        else:
            return self._hour

    @property
    def day(self):
        if self._null:
            return None
        else:
            return self._day

    @property
    def month(self):
        if self._null:
            return None
        else:
            return self._month

    @property
    def year(self):
        if self._null:
            return None
        else:
            return self._year

    @nano_sec.setter
    def nano_sec(self, val: UaUInt16):
        self._nano_sec = val
        self._value.nanoSec = val._val

    @micro_sec.setter
    def micro_sec(self, val: UaUInt16):
        self._micro_sec = val
        self._value.microSec = val._val

    @milli_sec.setter
    def milli_sec(self, val: UaUInt16):
        self._milli_sec = val
        self._value.milliSec = val._val

    @sec.setter
    def sec(self, val: UaUInt16):
        self._sec = val
        self._value.sec = val._val

    @min.setter
    def min(self, val: UaUInt16):
        self._min = val
        self._value.min = val._val

    @hour.setter
    def hour(self, val: UaUInt16):
        self._hour = val
        self._value.hour = val._val

    @day.setter
    def day(self, val: UaUInt16):
        self._day = val
        self._value.day = val._val

    @month.setter
    def month(self, val: UaUInt16):
        self._month = val
        self._value.month = val._val

    @year.setter
    def year(self, val: UaUInt16):
        self._year = val
        self._value.year = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaDateTimeStruct) : NULL\n"

        return ("(UaDateTimeStruct) :\n" +
                "\t" * (n + 1) + f"{self._year.value}-{self._month.value:02d}-{self._day.value:02d} " +
                f"{self._hour.value:02d}:{self._min.value:02d}:{self._sec.value:02d}." +
                f"{self._milli_sec.value:03d}.{self._micro_sec.value:03d}.{self._nano_sec.value:03d}\n")

    def to_primitive(self):
        return UaDateTime(lib.UA_DateTime_fromStruct(self._val))

    @staticmethod
    def now():
        return UaDateTime.now().to_struct()


# +++++++++++++++++++ UaGuid +++++++++++++++++++++++
class UaGuid(UaType):
    UA_TYPE = UA_TYPES.GUID

    NULL = lib.UA_GUID_NULL

    # random guid

    def __init__(self, string: str = "", val: Void = None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_Guid*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_Guid*", val._ptr)
        elif string != "":
            val = ffi.new("UA_Guid*", lib.UA_GUID(bytes(string, 'utf-8')))
            if val == UaGuid.NULL:
                raise ValueError(
                    f""""{string}" has to be formatted like: 
        "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", with X in [0..9, A..F]""")

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._data1 = UaUInt32(val=val.data1, is_pointer=False)
            self._data2 = UaUInt16(val=val.data2, is_pointer=False)
            self._data3 = UaUInt16(val=val.data3, is_pointer=False)
            self._data4 = UaByte(val=val.data4, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self.__value = _ptr(val, "UA_Guid")
        else:
            self.__value[0] = _val(val)

        if not _is_null(val):
            self._data1._value[0] = _val(val.data1)
            self._data2._value[0] = _val(val.data2)
            self._data3._value[0] = _val(val.data3)
            self._data4._value = val.data4

    @property
    def data1(self):
        if self._null:
            return None
        else:
            return self._data1

    @property
    def data2(self):
        if self._null:
            return None
        else:
            return self._data2

    @property
    def data3(self):
        if self._null:
            return None
        else:
            return self._data3

    @property
    def data4(self):
        if self._null:
            return None
        else:
            return self._data4

    # @data1.setter
    # def data1(self, val):
    #     self._data1 = val
    #     self._value.data1 = val._val
    #
    # @data2.setter
    # def data2(self, val):
    #     self._data2 = val
    #     self._value.data2 = val._val
    #
    # @data3.setter
    # def data3(self, val):
    #     self._data3 = val
    #     self._value.data3 = val._val
    #
    # @data4.setter
    # def data4(self, val):
    #     self._data4 = val
    #     self._value.data4 = val._ptr

    def __eq__(self, other):
        return lib.UA_Guid_equal(self._ptr, other._ptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self, n=0):
        if self._null:
            return "(UaGuid) : NULL\n"

        d1 = '{0:0{1}X}'.format(self._data1._val, 8)
        d2 = '{0:0{1}X}'.format(self._data2._val, 4)
        d3 = '{0:0{1}X}'.format(self._data3._val, 4)
        d4 = ""
        for i in range(2):
            d4 += '{0:0{1}X}'.format(self._data4._ptr[i], 2)
        d5 = ""
        for i in range(2, 8):
            d5 += '{0:0{1}X}'.format(self._data4._ptr[i], 2)

        return "(UaGuid): " + f"{d1}-{d2}-{d3}-{d4}-{d5}" + "\n"

    @staticmethod
    def random():
        Randomize.ua_random_seed(UaDateTime.now()._val)
        return UaGuid(val=lib.UA_Guid_random())


# +++++++++++++++++++ UaNodeId +++++++++++++++++++++++
class UaNodeId(UaType):
    UA_TYPE = UA_TYPES.NODEID

    NULL = lib.UA_NODEID_NULL

    # TODO: refactor
    # TODO: Memory management
    def __init__(self,
                 ns_index: Union[int, UaUInt16] = None,
                 ident: Union[int, UaUInt32, str, bytearray, UaString, UaGuid, UaByteString] = None,
                 is_pointer=False,
                 val: Void = None):
        if val is None:
            val = ffi.new("UA_NodeId*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_NodeId*", val._ptr)
        elif ns_index is not None and ident is not None:
            if type(ns_index) is int:
                if type(ident) is int:
                    val = lib.UA_NODEID_NUMERIC(ns_index, ident)
                elif type(ident) is UaUInt32:
                    val = lib.UA_NODEID_NUMERIC(ns_index, ident._val)
                elif type(ident) is str:
                    val = lib.UA_NODEID_STRING_ALLOC(ns_index, bytes(ident, 'utf-8'))
                elif type(ident) is bytearray:
                    val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index, ident)
                elif type(ident) is UaString:
                    val = lib.UA_NODEID_STRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
                elif type(ident) is UaGuid:
                    val = lib.UA_NODEID_GUID(ns_index, ident._val)
                elif type(ident) is UaByteString:
                    val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
                else:
                    raise TypeError(f"ident={ident} has invalid type, must be int, UaUInt32, "
                                    f"str, bytearray, UaString, UaGuid or UaByteString")
            elif type(ns_index) is UaUInt16:
                if type(ident) is int:
                    val = lib.UA_NODEID_NUMERIC(ns_index._val, ident)
                elif type(ident) is UaUInt32:
                    val = lib.UA_NODEID_NUMERIC(ns_index._val, ident._val)
                elif type(ident) is str:
                    val = lib.UA_NODEID_STRING_ALLOC(ns_index._val, bytes(ident, 'utf-8'))
                elif type(ident) is bytearray:
                    val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index._val, ident)
                elif type(ident) is UaString:
                    val = lib.UA_NODEID_STRING_ALLOC(ns_index._val, bytes(str(ident), 'utf-8'))
                elif type(ident) is UaGuid:
                    val = lib.A_NODEID_GUID(ns_index._val, ident._val)
                elif type(ident) is UaByteString:
                    val = lib.UA_NODEID_BYTESTRING_ALLOC(ns_index._val, bytes(str(ident), 'utf-8'))
                else:
                    raise TypeError(f"ident={ident} has invalid type, must be int, UaUInt32, "
                                    f"str, bytearray, UaString, UaGuid or UaByteString")
            else:
                raise TypeError(f"ns_index={ns_index} has invalid type, must be UaUInt16 or int")

            val = ffi.new("UA_NodeId*", val)

        super().__init__(val=val, is_pointer=is_pointer)
        if not self._null:
            self._namespace_index = UaUInt16(val=val.namespaceIndex, is_pointer=False)
            self._identifier_type = UaNodeIdType(val=val.identifierType, is_pointer=False)

            # TODO: refactor
            if self._identifier_type._val == 0:
                self._identifier = UaUInt32(val=val.identifier.numeric)
            elif self._identifier_type._val == 1:
                self._identifier = UaUInt32(val=val.identifier.numeric)
            elif self._identifier_type._val == 2:
                self._identifier = UaUInt32(val=val.identifier.numeric)
            elif self._identifier_type._val == 3:
                self._identifier = UaString(val=val.identifier.string)
            elif self._identifier_type._val == 4:
                self._identifier = UaGuid(val=val.identifier.guid)
            elif self._identifier_type._val == 5:
                self._identifier = UaByteString(val=val.identifier.byteString)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if not _is_null(val):
            if self._is_pointer:
                self._value = _ptr(val, "UA_NodeId")
            else:
                self._value[0] = _val(val)
            self._namespace_index._value[0] = _val(val.namespaceIndex)
            self._identifier_type._value[0] = _val(val.identifierType)
            cases = {
                0: val.identifier.numeric,
                1: val.identifier.numeric,
                2: val.identifier.numeric,
                3: val.identifier.string,
                4: val.identifier.guid,
                5: val.identifier.byteString
            }
            self._identifier._value[0] = cases[self._identifier_type._value]

    @property
    def namespace_index(self):
        if self._null:
            return None
        return self._namespace_index

    @namespace_index.setter
    def namespace_index(self, val):
        self._namespace_index = val
        self._value.namespaceIndex = val._val

    @property
    def identifier_type(self):
        if self._null:
            return None
        return self._identifier_type

    # @identifier_type.setter
    # def identifier_type(self, val):
    #     self._identifier_type = val
    #     self._value.identifierType = val._val

    @property
    def identifier(self):
        if self._null:
            return None
        return self._identifier

    # @identifier.setter
    # def identifier(self, val):
    #     self._identifier = val
    #     self._value.identifier = val._val

    def __str__(self, n=0):
        if self._null:
            return "NULL"
        return ("(UaNodeId) :\n" +
                "\t" * (n + 1) + "namespace_index" + self._namespace_index.__str__(n + 1) +
                "\t" * (n + 1) + "identifier_type" + self._identifier_type.__str__(n + 1) +
                "\t" * (n + 1) + "identifier" + self._identifier.__str__(n + 1))

    def __eq__(self, other):
        return lib.UA_NodeId_equal(self._ptr, other._ptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_null(self):
        return lib.UA_NodeId_isNull(self._ptr)


# +++++++++++++++++++ UaExpandedNodeId +++++++++++++++++++++++
class UaExpandedNodeId(UaType):
    UA_TYPE = UA_TYPES.EXPANDEDNODEID

    NULL = lib.UA_EXPANDEDNODEID_NULL

    # TODO: refactor
    # TODO: Memory management
    def __init__(self,
                 ns_index: Union[int, UaUInt16] = None,
                 ident: Union[int, UaUInt32, str, bytearray, UaString, UaGuid, UaByteString] = None,
                 is_pointer=False,
                 val: Void = None):

        if val is None:
            val = ffi.new("UA_ExpandedNodeId*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_ExpandedNodeId*", val._ptr)
        elif ns_index is not None and ident is not None:
            if type(ns_index) is int:
                if type(ident) is int:
                    val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index, ident)
                elif type(ident) is UaUInt32:
                    val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index, ident._val)
                elif type(ident) is str:
                    val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index, bytes(ident, 'utf-8'))
                elif type(ident) is bytearray:
                    val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index, ident)
                elif type(ident) is UaString:
                    val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
                elif type(ident) is UaGuid:
                    val = lib.A_EXPANDEDNODEID_GUID(ns_index, ident._val)
                elif type(ident) is UaByteString:
                    val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index, bytes(str(ident), 'utf-8'))
                else:
                    raise TypeError(f"ident={ident} has invalid type, must be int, UaUInt32, "
                                    f"str, bytearray, UaString, UaGuid or UaByteString")
            elif type(ns_index) is UaUInt16:
                if type(ident) is int:
                    val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index._val, ident)
                elif type(ident) is UaUInt32:
                    val = lib.UA_EXPANDEDNODEID_NUMERIC(ns_index._val, ident._val)
                elif type(ident) is str:
                    val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index._val, bytes(ident, 'utf-8'))
                elif type(ident) is bytearray:
                    val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index._val, ident)
                elif type(ident) is UaString:
                    val = lib.UA_EXPANDEDNODEID_STRING_ALLOC(ns_index._val, bytes(str(ident), 'utf-8'))
                elif type(ident) is UaGuid:
                    val = lib.A_EXPANDEDNODEID_GUID(ns_index._val, ident._val)
                elif type(ident) is UaByteString:
                    val = lib.UA_EXPANDEDNODEID_BYTESTRING_ALLOC(ns_index._val, bytes(str(ident), 'utf-8'))
                else:
                    raise TypeError(f"ident={ident} has invalid type, must be int, UaUInt32, "
                                    f"str, bytearray, UaString, UaGuid or UaByteString")
            else:
                raise TypeError(f"ns_index={ns_index} has invalid type, must be UaUInt16 or int")

            val = ffi.new("UA_ExpandedNodeId*", val)

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._node_id = UaNodeId(val=val.nodeId, is_pointer=False)
            self._namespace_uri = UaString(val=val.namespaceUri, is_pointer=False)
            self._server_index = UaUInt32(val=val.serverIndex, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ExpandedNodeId")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._node_id._value[0] = _val(val.nodeId)
            self._namespace_uri._value[0] = _val(val.namespaceUri)
            self._server_index._value[0] = _val(val.serverIndex)

    @property
    def node_id(self):
        if self._null:
            return None
        else:
            return self._node_id

    @property
    def namespace_uri(self):
        if self._null:
            return None
        else:
            return self._namespace_uri

    @property
    def server_index(self):
        if self._null:
            return None
        else:
            return self._server_index

    @node_id.setter
    def node_id(self, val: UaNodeId):
        self._node_id = val
        self._value.nodeId = val._val

    @namespace_uri.setter
    def namespace_uri(self, val: UaString):
        self._namespace_uri = val
        self._value.namespaceUri = val._val

    @server_index.setter
    def server_index(self, val: UaUInt32):
        self._server_index = val
        self._value.serverIndex = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaExpandedNodeId) : NULL\n"

        return ("(UaExpandedNodeId) :\n" +
                "\t" * (n + 1) + "node_id" + self._node_id.__str__(n + 1) +
                "\t" * (n + 1) + "namespace_uri" + self._namespace_uri.__str__(n + 1) +
                "\t" * (n + 1) + "server_index" + self._server_index.__str__(n + 1))

    def is_local(self):
        return lib.UA_ExpandedNodeId_isLocal(self._ptr)

    def __eq__(self, other):
        return lib.UA_ExpandedNodeId_equal(self._ptr, other._ptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return lib.UA_ExpandedNodeId_order(self._ptr, other._ptr) == 1

    def __lt__(self, other):
        return lib.UA_ExpandedNodeId_order(self._ptr, other._ptr) == -1

    def __ge__(self, other):
        return lib.UA_ExpandedNodeId_order(self._ptr, other._ptr) in [1, 0]

    def __le__(self, other):
        return lib.UA_ExpandedNodeId_order(self._ptr, other._ptr) in [-1, 0]

    def __hash__(self):
        return lib.UA_ExpandedNodeId_hash(self._ptr)


# +++++++++++++++++++ UaQualifiedName +++++++++++++++++++++++
class UaQualifiedName(UaType):
    UA_TYPE = UA_TYPES.QUALIFIEDNAME

    def __init__(self,
                 ns_index: Union[int, UaUInt16] = None,
                 string: Union[str, UaString] = None,
                 val: Void = None,
                 is_pointer=False):
        if val is None:
            val = ffi.new("UA_QualifiedName*")
        # TODO: refactor
        # TODO: Memory management
        if isinstance(val, UaType):
            val = ffi.cast("UA_QualifiedName*", val._ptr)
        elif ns_index is not None and string is not None:
            if type(ns_index) is int:
                if type(string) is str:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index, bytes(string, "utf-8"))
                elif type(string) is UaString:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index, bytes(str(string), "utf-8"))
                else:
                    raise AttributeError(f"string={type(string)} has to be str or UaString")
            elif type(ns_index) is UaUInt16:
                if type(string) is str:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index._val, bytes(string, "utf-8"))
                elif type(string) is UaString:
                    val = lib.UA_QUALIFIEDNAME_ALLOC(ns_index._val, bytes(str(string), "utf-8"))
                else:
                    raise AttributeError(f"string={string} has to be str or UaString")
            else:
                raise AttributeError(f"ns_index={ns_index} has to be int or UaUInt16")

            val = ffi.new("UA_QualifiedName*", val)

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._namespace_index = UaUInt16(val=val.namespaceIndex, is_pointer=False)
            self._name = UaString(val=val.name, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_QualifiedName")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._namespace_index._value[0] = _val(val.namespaceIndex)
            self._name._value[0] = _val(val.name)

    @property
    def namespace_index(self):
        if self._null:
            return None
        else:
            return self._namespace_index

    @property
    def name(self):
        if self._null:
            return None
        else:
            return self._name

    @namespace_index.setter
    def namespace_index(self, val: UaUInt16):
        self._namespace_index = val
        self._value.namespaceIndex = val._val

    @name.setter
    def name(self, val: UaString):
        self._name = val
        self._value.name = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaQualifiedName) : NULL\n"

        return ("(UaQualifiedName) :\n" +
                "\t" * (n + 1) + "namespace_index" + self._namespace_index.__str__(n + 1) +
                "\t" * (n + 1) + "name" + self._name.__str__(n + 1))

    def is_null(self):
        return lib.UA_QualifiedName_isNull(self._ptr)

    def __hash__(self):
        return lib.UA_QualifiedName_hash(self._ptr)

    def __eq__(self, other):
        return lib.UA_QualifiedName_equal(self._ptr, other.__value)


# +++++++++++++++++++ UaLocalizedText +++++++++++++++++++++++
class UaLocalizedText(UaType):
    UA_TYPE = UA_TYPES.LOCALIZEDTEXT

    # TODO: refactor
    # TODO: Memory management
    def __init__(self,
                 locale: Union[str, UaString] = None,
                 text: Union[str, UaString] = None,
                 val: Void = None,
                 is_pointer=False):
        if val is None:
            ffi.new("UA_LocalizedText*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_LocalizedText*", val._ptr)
        elif locale is not None and text is not None:
            if type(locale) is str:
                if type(text) is str:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale, "utf-8"), bytes(text, "utf-8"))
                elif type(text) is UaString:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale, "utf-8"), bytes(text.value, "utf-8"))
                else:
                    raise AttributeError(f"text={text} has to be str or UaString")
            elif type(locale) is UaString:
                if type(text) is str:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale.value, "utf-8"), bytes(text, "utf-8"))
                elif type(text) is UaString:
                    val = lib.UA_LOCALIZEDTEXT_ALLOC(bytes(locale.value, "utf-8"),
                                                     bytes(text.value, "utf-8"))
                else:
                    raise AttributeError(f"text={text} has to be str or UaString")
            else:
                raise AttributeError(f"locale={locale} has to be str or UaUInt16")

            val = ffi.new("UA_LocalizedText*", val)

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._locale = UaString(val=val.locale, is_pointer=False)
            self._text = UaString(val=val.text, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_LocalizedText")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._locale._value[0] = _val(val.locale)
            self._text._value[0] = _val(val.text)

    @property
    def locale(self):
        if self._null:
            return None
        else:
            return self._locale

    @property
    def text(self):
        if self._null:
            return None
        else:
            return self._text

    @locale.setter
    def locale(self, val: UaString):
        self._locale = val
        self._value.locale = val._val

    @text.setter
    def text(self, val: UaString):
        self._text = val
        self._value.text = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaLocalizedText) : NULL\n"

        return ("(UaLocalizedText) :\n" +
                "\t" * (n + 1) + "locale" + self._locale.__str__(n + 1) +
                "\t" * (n + 1) + "text" + self._text.__str__(n + 1))


# +++++++++++++++++++ UaNumericRangeDimension +++++++++++++++++++++++
class UaNumericRangeDimension(UaType):
    def __init__(self, val: Void = None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NumericRangeDimension*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_NumericRangeDimension*", val._ptr)

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._min = UaUInt32(val=val.min, is_pointer=False)
            self._max = UaUInt32(val=val.max, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NumericRangeDimension")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._min._value[0] = _val(val.min)
            self._max._value[0] = _val(val.max)

    @property
    def min(self):
        if self._null:
            return None
        else:
            return self._min

    @property
    def max(self):
        if self._null:
            return None
        else:
            return self._max

    @min.setter
    def min(self, val: UaUInt32):
        self._min = val
        self._value.min = val._val

    @max.setter
    def max(self, val: UaUInt32):
        self._max = val
        self._value.max = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaNumericRangeDimension) : NULL\n"

        return ("(UaNumericRangeDimension) :\n" +
                "\t" * (n + 1) + "min" + self._min.__str__(n + 1) +
                "\t" * (n + 1) + "max" + self._max.__str__(n + 1))


# +++++++++++++++++++ UaNumericRange +++++++++++++++++++++++
class UaNumericRange(UaType):
    def __init__(self, val: Void = None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_NumericRange*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_NumericRange*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._dimensions_size = SizeT(val=val.dimensionsSize, is_pointer=False)
            self._dimensions = UaNumericRangeDimension(val=val.dimensions, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_NumericRange")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._dimensions_size._value[0] = _val(val.dimensionsSize)
            self._dimensions._value = val.dimensions

    @property
    def dimensions_size(self):
        if self._null:
            return None
        else:
            return self._dimensions_size

    @property
    def dimensions(self):
        if self._null:
            return None
        else:
            return self._dimensions

    @dimensions_size.setter
    def dimensions_size(self, val: SizeT):
        self._dimensions_size = val
        self._value.dimensionsSize = val._val

    @dimensions.setter
    def dimensions(self, val: UaNumericRangeDimension):
        self._dimensions = val
        self._value.dimensions = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaNumericRange) : NULL\n"

        return ("(UaNumericRange) :\n" +
                "\t" * (n + 1) + "dimensions_size" + self._dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "dimensions" + self._dimensions.__str__(n + 1))


# +++++++++++++++++++ UaVariant +++++++++++++++++++++++
class UaVariant(UaType):
    UA_TYPE = UA_TYPES.VARIANT

    def __init__(self, val: Void = None, is_pointer=False):
        if isinstance(val, UaType):
            val = ffi.cast("UA_Variant*", val._ptr)
        elif val is None:
            val = ffi.new("UA_Variant*")
            lib.UA_Variant_init(_ptr(val))

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._type = UaDataType(val=val.type, is_pointer=True)
            self._storage_type = UaVariantStorageType(val=val.storageType, is_pointer=False)
            self._array_length = SizeT(val=val.arrayLength, is_pointer=False)
            self._data = Void(val=val.data, is_pointer=True)
            self._array_dimensions_size = SizeT(val=val.arrayDimensionsSize, is_pointer=False)
            self._array_dimensions = UaUInt32(val=val.arrayDimensions, is_pointer=True)
            self._array_dimensions._size = self._array_dimensions_size._val

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_Variant")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._type._value = val.type
            self._storage_type._value[0] = _val(val.storageType)
            self._array_length._value[0] = _val(val.arrayLength)
            self._data._value = val.data
            self._array_dimensions_size._value[0] = _val(val.arrayDimensionsSize)
            self._array_dimensions._value = val.arrayDimensions

    @property
    def type(self):
        if self._null:
            return None
        else:
            return self._type

    @property
    def storage_type(self):
        if self._null:
            return None
        else:
            return self._storage_type

    @property
    def array_length(self):
        if self._null:
            return None
        else:
            return self._array_length

    @property
    def data(self):
        if self._null:
            return None
        else:
            return self._data

    @property
    def array_dimensions_size(self):
        if self._null:
            return None
        else:
            return self._array_dimensions_size

    @property
    def array_dimensions(self):
        if self._null:
            return None
        else:
            return self._array_dimensions

    @type.setter
    def type(self, val: 'UaDataType'):
        self._type = val
        self._value.type = val._ptr

    @storage_type.setter
    def storage_type(self, val: UaVariantStorageType):
        self._storage_type = val
        self._value.storageType = val._val

    @array_length.setter
    def array_length(self, val: SizeT):
        self._array_length = val
        self._value.arrayLength = val._val

    # TODO: Document this!
    # ---> it only works if val is of the correct subclass of uatype or ualist with correctly
    # set class attribute respectively
    @data.setter
    def data(self, val: UaType):
        if type(val) is UaType or not isinstance(val, UaType):
            raise TypeError("'val' has to be an instance of a child class of UaType.")
        if isinstance(val, UaList):
            if val.ua_type is None:
                raise TypeError("if 'val' is a UaList the attribute ua_type has to be set correctly.")
            self.set_array(val, len(val), val.ua_type)
        else:
            self.set_scalar(val, val.UA_TYPE)

    @array_dimensions_size.setter
    def array_dimensions_size(self, val: SizeT):
        self._array_dimensions_size = val
        self._value.arrayDimensionsSize = val._val

    @array_dimensions.setter
    def array_dimensions(self, val: UaUInt32):
        self._array_dimensions = val
        self._value.arrayDimensions = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaVariant) : NULL\n"

        return ("(UaVariant) :\n" +
                "\t" * (n + 1) + "type" + self._type.__str__(n + 1) +
                "\t" * (n + 1) + "storage_type" + self._storage_type.__str__(n + 1) +
                "\t" * (n + 1) + "array_length" + self._array_length.__str__(n + 1) +
                "\t" * (n + 1) + "data" + self._data.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions_size" + self._array_dimensions_size.__str__(n + 1) +
                "\t" * (n + 1) + "array_dimensions" + self._array_dimensions.__str__(n + 1))

    def is_empty(self):
        return lib.UA_Variant_isEmpty(self._ptr)

    def is_scalar(self):
        return lib.UA_Variant_isScalar(self._ptr)

    def has_scalar_type(self, data_type: 'UaDataType'):
        return lib.UA_Variant_hasScalarType(self._ptr, data_type._ptr)

    def has_array_type(self, data_type: 'UaDataType'):
        return lib.UA_Variant_hasArrayType(self._ptr, data_type._ptr)

    # data is the python object matching the data_type or an void ptr
    def set_scalar(self, data: Any, data_type: 'UaDataType'):
        self.__mem_protect = data._ptr
        status_code = lib.UA_Variant_setScalarCopy(self._ptr, self.__mem_protect, data_type._ptr)
        self._update()
        return UaStatusCode(val=status_code)

    def set_array(self, array: Any, size: Union[int, SizeT], data_type: 'UaDataType'):
        if type(size) is int:
            size = SizeT(size)
        if type(size) is not SizeT:
            raise AttributeError(f"size={size} has to be int or SizeT")
        self.__mem_protect = array._ptr
        status_code = lib.UA_Variant_setArrayCopy(self._ptr, self.__mem_protect, size._val, data_type._ptr)
        status_code = UaStatusCode(val=status_code)
        if not status_code.is_bad():
            self._update()
            return status_code
        else:
            raise Exception(f"An Error occured - {str(status_code)}")

    def copy_range_to(self, variant: 'UaVariant', num_range: UaNumericRange):
        # TODO: might cause memory problems!
        status_code = lib.UA_Variant_copyRange(self._ptr, variant._ptr, num_range._val)
        status_code = UaStatusCode(val=status_code)
        if not status_code.is_bad():
            self._update()
            return status_code
        else:
            raise AttributeError(f"An Error occured - {str(status_code)}")

    def copy(self, variant: 'UaVariant'):
        # TODO: might cause memory problems!
        status_code = lib.UA_Variant_copy(self._ptr, variant._ptr)
        status_code = UaStatusCode(val=status_code)
        if not status_code.is_bad():
            self._update()
            return status_code
        else:
            raise AttributeError(f"An Error occured - {str(status_code)}")

    def set_range_copy(self, array: Any, size: Union[int, SizeT], num_range: UaNumericRange):
        if size is int:
            size = SizeT(size)
        elif size is not SizeT:
            raise AttributeError(f"size={size} has to be int or SizeT")
        self.__mem_protect = array._ptr
        status_code = lib.UA_Variant_setRangeCopy(self._ptr, self.__mem_protect, size, num_range._val)
        status_code = UaStatusCode(val=status_code)
        if not status_code.is_bad():
            self._update()
            return status_code
        else:
            raise AttributeError(f"An Error occured - {str(status_code)}")


# +++++++++++++++++++ UaDataValue +++++++++++++++++++++++
class UaDataValue(UaType):
    UA_TYPE = UA_TYPES.DATAVALUE

    def __init__(self, val: Void = None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataValue*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DataValue*", val._ptr)

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._variant = UaVariant(val=val.value, is_pointer=False)
            self._source_timestamp = UaDateTime(val=val.sourceTimestamp, is_pointer=False)
            self._server_timestamp = UaDateTime(val=val.serverTimestamp, is_pointer=False)
            self._source_picoseconds = UaUInt16(val=val.sourcePicoseconds, is_pointer=False)
            self._server_picoseconds = UaUInt16(val=val.serverPicoseconds, is_pointer=False)
            self._status = UaStatusCode(val=val.status, is_pointer=False)
            self._has_variant = UaBoolean(val=val.hasValue, is_pointer=False)
            self._has_status = UaBoolean(val=val.hasStatus, is_pointer=False)
            self._has_source_timestamp = UaBoolean(val=val.hasSourceTimestamp, is_pointer=False)
            self._has_server_timestamp = UaBoolean(val=val.hasServerTimestamp, is_pointer=False)
            self._has_source_picoseconds = UaBoolean(val=val.hasSourcePicoseconds, is_pointer=False)
            self._has_server_picoseconds = UaBoolean(val=val.hasServerPicoseconds, is_pointer=False)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataValue")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._variant._value[0] = _val(val.value)
            self._source_timestamp._value[0] = _val(val.sourceTimestamp)
            self._server_timestamp._value[0] = _val(val.serverTimestamp)
            self._source_picoseconds._value[0] = _val(val.sourcePicoseconds)
            self._server_picoseconds._value[0] = _val(val.serverPicoseconds)
            self._status._value[0] = _val(val.status)
            self._has_variant._value[0] = _val(val.hasValue)
            self._has_status._value[0] = _val(val.hasStatus)
            self._has_source_timestamp._value[0] = _val(val.hasSourceTimestamp)
            self._has_server_timestamp._value[0] = _val(val.hasServerTimestamp)
            self._has_source_picoseconds._value[0] = _val(val.hasSourcePicoseconds)
            self._has_server_picoseconds._value[0] = _val(val.hasServerPicoseconds)

    @property
    def variant(self):
        if self._null:
            return None
        return self._variant

    @property
    def source_timestamp(self):
        if self._null:
            return None
        else:
            return self._source_timestamp

    @property
    def server_timestamp(self):
        if self._null:
            return None
        else:
            return self._server_timestamp

    @property
    def source_picoseconds(self):
        if self._null:
            return None
        else:
            return self._source_picoseconds

    @property
    def server_picoseconds(self):
        if self._null:
            return None
        else:
            return self._server_picoseconds

    @property
    def status(self):
        if self._null:
            return None
        else:
            return self._status

    @property
    def has_variant(self):
        if self._null:
            return None
        return self._has_variant

    @property
    def has_status(self):
        if self._null:
            return None
        else:
            return self._has_status

    @property
    def has_source_timestamp(self):
        if self._null:
            return None
        else:
            return self._has_source_timestamp

    @property
    def has_server_timestamp(self):
        if self._null:
            return None
        else:
            return self._has_server_timestamp

    @property
    def has_source_picoseconds(self):
        if self._null:
            return None
        else:
            return self._has_source_picoseconds

    @property
    def has_server_picoseconds(self):
        if self._null:
            return None
        else:
            return self._has_server_picoseconds

    @variant.setter
    def variant(self, val):
        self._variant = val
        self._value.value = val._val

    @source_timestamp.setter
    def source_timestamp(self, val):
        self._source_timestamp = val
        self._value.sourceTimestamp = val._val

    @server_timestamp.setter
    def server_timestamp(self, val):
        self._server_timestamp = val
        self._value.serverTimestamp = val._val

    @source_picoseconds.setter
    def source_picoseconds(self, val):
        self._source_picoseconds = val
        self._value.sourcePicoseconds = val._val

    @server_picoseconds.setter
    def server_picoseconds(self, val):
        self._server_picoseconds = val
        self._value.serverPicoseconds = val._val

    @status.setter
    def status(self, val):
        self._status = val
        self._value.status = val._val

    @has_variant.setter
    def has_variant(self, val):
        self._has_variant = val
        self._value.hasValue = val._val

    @has_status.setter
    def has_status(self, val):
        self._has_status = val
        self._value.hasStatus = val._val

    @has_source_timestamp.setter
    def has_source_timestamp(self, val):
        self._has_source_timestamp = val
        self._value.hasSourceTimestamp = val._val

    @has_server_timestamp.setter
    def has_server_timestamp(self, val):
        self._has_server_timestamp = val
        self._value.hasServerTimestamp = val._val

    @has_source_picoseconds.setter
    def has_source_picoseconds(self, val):
        self._has_source_picoseconds = val
        self._value.hasSourcePicoseconds = val._val

    @has_server_picoseconds.setter
    def has_server_picoseconds(self, val):
        self._has_server_picoseconds = val
        self._value.hasServerPicoseconds = val._val

    def __str__(self, n=0):
        if self._null:
            return "(UaDataValue) : NULL\n"

        return ("(UaDataValue) :\n" +
                "\t" * (n + 1) + "variant" + self._variant.__str__(n + 1) +
                "\t" * (n + 1) + "source_timestamp" + self._source_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "server_timestamp" + self._server_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "source_picoseconds" + self._source_picoseconds.__str__(n + 1) +
                "\t" * (n + 1) + "server_picoseconds" + self._server_picoseconds.__str__(n + 1) +
                "\t" * (n + 1) + "status" + self._status.__str__(n + 1) +
                "\t" * (n + 1) + "has_variant" + self._has_variant.__str__(n + 1) +
                "\t" * (n + 1) + "has_status" + self._has_status.__str__(n + 1) +
                "\t" * (n + 1) + "has_source_timestamp" + self._has_source_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "has_server_timestamp" + self._has_server_timestamp.__str__(n + 1) +
                "\t" * (n + 1) + "has_source_picoseconds" + self._has_source_picoseconds.__str__(n + 1) +
                "\t" * (n + 1) + "has_server_picoseconds" + self._has_server_picoseconds.__str__(n + 1))


class UaExtensionObject(UaType):
    UA_TYPE = UA_TYPES.EXTENSIONOBJECT

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_ExtensionObject*")
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._encoding = UaExtensionObjectEncoding(val=val.encoding)
            if self._encoding._val in [0, 1, 2]:
                self._type = UaNodeId(val=val.content.encoded.typeId)
                self._data = UaByteString(val=val.content.encoded.body)
            elif self._encoding._val in [3, 4]:
                self._type = UaDataType(val=val.content.decoded.type, is_pointer=True)
                self._data = Void(val=val.content.encoded.body)
            else:
                raise ValueError(f"Encoding does not exist.")

        # TODO: might cause trouble since at _value[0] might not be enough memory for an other encoding type

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_ExtensionObject")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._encoding._value[0] = _val(val.encoding)
            if self._encoding in [0, 1, 2]:
                self._type = UaNodeId(val=val.content.encoded.typeId)
                self._data = UaByteString(val=val.content.encoded.body)
            elif self._encoding in [3, 4]:
                self._type = UaDataType(val=val.content.decoded.type, is_pointer=True)
                self._data = Void(val=val.content.encoded.body)
            else:
                raise ValueError(f"Encoding does not exist.")

    @property
    def type(self):
        if self._null:
            return None
        return self._type

    # @type.setter
    # def type(self, val):
    #     if self._encoding._val in [0, 1, 2] and type(val) not in UaNodeId:
    #         raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaNodeId")
    #     if self._encoding._val in [3, 4] and type(val) not in UaDataType:
    #         raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaDataType")
    #     self._type = val
    #     self._value.type = val._val if self._encoding._val < 3 else val._ptr

    @property
    def data(self):
        if self._null:
            return None
        return self._data

    # @data.setter
    # def data(self, val):
    #     if self._encoding._val in [0, 1, 2] and type(val) is not UaByteString:
    #         raise AttributeError(f"encoding is {str(self._encoding)} so value must be in UaNodeId")
    #     if self._encoding._val in [3, 4] and type(val) is not Void:
    #         val = Void(val)
    #
    #     self._data = val
    #     self._value.data = val._val if self._encoding._value < 3 else val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaExtensionObject) : NULL\n"

        return ("(UaExtensionObject) :\n" +
                "\t" * (n + 1) + "encoding" + self._encoding.__str__(n + 1) +
                "\t" * (n + 1) + "type" + self._type.__str__(n + 1) +
                "\t" * (n + 1) + "data" + self._data.__str__(n + 1))


# +++++++++++++++++++ UaDiagnosticInfo +++++++++++++++++++++++
class UaDiagnosticInfo(UaType):
    UA_TYPE = UA_TYPES.DIAGNOSTICINFO

    def __init__(self, val: Void = None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DiagnosticInfo*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DiagnosticInfo*", val._ptr)

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._has_symbolic_id = UaBoolean(val=val.hasSymbolicId, is_pointer=False)
            self._has_namespace_uri = UaBoolean(val=val.hasNamespaceUri, is_pointer=False)
            self._has_localized_text = UaBoolean(val=val.hasLocalizedText, is_pointer=False)
            self._has_locale = UaBoolean(val=val.hasLocale, is_pointer=False)
            self._has_additional_info = UaBoolean(val=val.hasAdditionalInfo, is_pointer=False)
            self._has_inner_status_code = UaBoolean(val=val.hasInnerStatusCode, is_pointer=False)
            self._has_inner_diagnostic_info = UaBoolean(val=val.hasInnerDiagnosticInfo, is_pointer=False)
            self._symbolic_id = UaInt32(val=val.symbolicId, is_pointer=False)
            self._namespace_uri = UaInt32(val=val.namespaceUri, is_pointer=False)
            self._localized_text = UaInt32(val=val.localizedText, is_pointer=False)
            self._locale = UaInt32(val=val.locale, is_pointer=False)
            self._additional_info = UaString(val=val.additionalInfo, is_pointer=False)
            self._inner_status_code = UaStatusCode(val=val.innerStatusCode, is_pointer=False)
            self._inner_diagnostic_info = UaDiagnosticInfo(val=val.innerDiagnosticInfo, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DiagnosticInfo")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._has_symbolic_id._value[0] = _val(val.hasSymbolicId)
            self._has_namespace_uri._value[0] = _val(val.hasNamespaceUri)
            self._has_localized_text._value[0] = _val(val.hasLocalizedText)
            self._has_locale._value[0] = _val(val.hasLocale)
            self._has_additional_info._value[0] = _val(val.hasAdditionalInfo)
            self._has_inner_status_code._value[0] = _val(val.hasInnerStatusCode)
            self._has_inner_diagnostic_info._value[0] = _val(val.hasInnerDiagnosticInfo)
            self._symbolic_id._value[0] = _val(val.symbolicId)
            self._namespace_uri._value[0] = _val(val.namespaceUri)
            self._localized_text._value[0] = _val(val.localizedText)
            self._locale._value[0] = _val(val.locale)
            self._additional_info._value[0] = _val(val.additionalInfo)
            self._inner_status_code._value[0] = _val(val.innerStatusCode)
            self._inner_diagnostic_info._value = val.innerDiagnosticInfo

    # TODO: probably there is null if there is a property has_... -> if primitive no problem
    @property
    def has_symbolic_id(self):
        if self._null:
            return None
        else:
            return self._has_symbolic_id

    @property
    def has_namespace_uri(self):
        if self._null:
            return None
        else:
            return self._has_namespace_uri

    @property
    def has_localized_text(self):
        if self._null:
            return None
        else:
            return self._has_localized_text

    @property
    def has_locale(self):
        if self._null:
            return None
        else:
            return self._has_locale

    @property
    def has_additional_info(self):
        if self._null:
            return None
        else:
            return self._has_additional_info

    @property
    def has_inner_status_code(self):
        if self._null:
            return None
        else:
            return self._has_inner_status_code

    @property
    def has_inner_diagnostic_info(self):
        if self._null:
            return None
        else:
            return self._has_inner_diagnostic_info

    @property
    def symbolic_id(self):
        if self._null:
            return None
        else:
            return self._symbolic_id

    @property
    def namespace_uri(self):
        if self._null:
            return None
        else:
            return self._namespace_uri

    @property
    def localized_text(self):
        if self._null:
            return None
        else:
            return self._localized_text

    @property
    def locale(self):
        if self._null:
            return None
        else:
            return self._locale

    @property
    def additional_info(self):
        if self._null:
            return None
        else:
            return self._additional_info

    @property
    def inner_status_code(self):
        if self._null:
            return None
        else:
            return self._inner_status_code

    @property
    def inner_diagnostic_info(self):
        if self._null:
            return None
        else:
            return self._inner_diagnostic_info

    # @has_symbolic_id.setter
    # def has_symbolic_id(self, val):
    #     self._has_symbolic_id = val
    #     self._value.hasSymbolicId = val._val
    #
    # @has_namespace_uri.setter
    # def has_namespace_uri(self, val):
    #     self._has_namespace_uri = val
    #     self._value.hasNamespaceUri = val._val
    #
    # @has_localized_text.setter
    # def has_localized_text(self, val):
    #     self._has_localized_text = val
    #     self._value.hasLocalizedText = val._val
    #
    # @has_locale.setter
    # def has_locale(self, val):
    #     self._has_locale = val
    #     self._value.hasLocale = val._val
    #
    # @has_additional_info.setter
    # def has_additional_info(self, val):
    #     self._has_additional_info = val
    #     self._value.hasAdditionalInfo = val._val
    #
    # @has_inner_status_code.setter
    # def has_inner_status_code(self, val):
    #     self._has_inner_status_code = val
    #     self._value.hasInnerStatusCode = val._val
    #
    # @has_inner_diagnostic_info.setter
    # def has_inner_diagnostic_info(self, val):
    #     self._has_inner_diagnostic_info = val
    #     self._value.hasInnerDiagnosticInfo = val._val
    #
    # @symbolic_id.setter
    # def symbolic_id(self, val):
    #     self._symbolic_id = val
    #     self._value.symbolicId = val._val
    #
    # @namespace_uri.setter
    # def namespace_uri(self, val):
    #     self._namespace_uri = val
    #     self._value.namespaceUri = val._val
    #
    # @localized_text.setter
    # def localized_text(self, val):
    #     self._localized_text = val
    #     self._value.localizedText = val._val
    #
    # @locale.setter
    # def locale(self, val):
    #     self._locale = val
    #     self._value.locale = val._val
    #
    # @additional_info.setter
    # def additional_info(self, val):
    #     self._additional_info = val
    #     self._value.additionalInfo = val._val
    #
    # @inner_status_code.setter
    # def inner_status_code(self, val):
    #     self._inner_status_code = val
    #     self._value.innerStatusCode = val._val
    #
    # @inner_diagnostic_info.setter
    # def inner_diagnostic_info(self, val):
    #     self._inner_diagnostic_info = val
    #     self._value.innerDiagnosticInfo = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaDiagnosticInfo) : NULL\n"

        return ("(UaDiagnosticInfo) :\n" +
                "\t" * (n + 1) + "has_symbolic_id" + self._has_symbolic_id.__str__(n + 1) +
                "\t" * (n + 1) + "has_namespace_uri" + self._has_namespace_uri.__str__(n + 1) +
                "\t" * (n + 1) + "has_localized_text" + self._has_localized_text.__str__(n + 1) +
                "\t" * (n + 1) + "has_locale" + self._has_locale.__str__(n + 1) +
                "\t" * (n + 1) + "has_additional_info" + self._has_additional_info.__str__(n + 1) +
                "\t" * (n + 1) + "has_inner_status_code" + self._has_inner_status_code.__str__(n + 1) +
                "\t" * (n + 1) + "has_inner_diagnostic_info" + self._has_inner_diagnostic_info.__str__(n + 1) +
                "\t" * (n + 1) + "symbolic_id" + self._symbolic_id.__str__(n + 1) +
                "\t" * (n + 1) + "namespace_uri" + self._namespace_uri.__str__(n + 1) +
                "\t" * (n + 1) + "localized_text" + self._localized_text.__str__(n + 1) +
                "\t" * (n + 1) + "locale" + self._locale.__str__(n + 1) +
                "\t" * (n + 1) + "additional_info" + self._additional_info.__str__(n + 1) +
                "\t" * (n + 1) + "inner_status_code" + self._inner_status_code.__str__(n + 1) +
                "\t" * (n + 1) + "inner_diagnostic_info" + self._inner_diagnostic_info.__str__(n + 1))


# +++++++++++++++++++ UaDataTypeMember +++++++++++++++++++++++
class UaDataTypeMember(UaType):
    def __init__(self, val: Void = None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataTypeMember*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DataTypeMember*", val._ptr)

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._member_type_index = UaUInt16(val=val.memberTypeIndex, is_pointer=False)
            self._padding = UaByte(val=val.padding, is_pointer=False)
            self._namespace_zero = UaBoolean(val=val.namespaceZero, is_pointer=False)
            self._is_array = UaBoolean(val=val.isArray, is_pointer=False)
            self._is_optional = UaBoolean(val=val.isOptional, is_pointer=False)
            self._member_name = CString(val=val.memberName, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataTypeMember")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._member_type_index._value[0] = _val(val.memberTypeIndex)
            self._padding._value[0] = _val(val.padding)
            self._namespace_zero._value[0] = _val(val.namespaceZero)
            self._is_array._value[0] = _val(val.isArray)
            self._is_optional._value[0] = _val(val.isOptional)
            self._member_name._value = val.memberName

    @property
    def member_type_index(self):
        if self._null:
            return None
        else:
            return self._member_type_index

    @property
    def padding(self):
        if self._null:
            return None
        else:
            return self._padding

    @property
    def namespace_zero(self):
        if self._null:
            return None
        else:
            return self._namespace_zero

    @property
    def is_array(self):
        if self._null:
            return None
        else:
            return self._is_array

    @property
    def is_optional(self):
        if self._null:
            return None
        else:
            return self._is_optional

    @property
    def member_name(self):
        if self._null:
            return None
        else:
            return self._member_name

    @member_type_index.setter
    def member_type_index(self, val: UaUInt16):
        self._member_type_index = val
        self._value.memberTypeIndex = val._val

    @padding.setter
    def padding(self, val: UaByte):
        self._padding = val
        self._value.padding = val._val

    @namespace_zero.setter
    def namespace_zero(self, val: UaBoolean):
        self._namespace_zero = val
        self._value.namespaceZero = val._val

    @is_array.setter
    def is_array(self, val: UaBoolean):
        self._is_array = val
        self._value.isArray = val._val

    @is_optional.setter
    def is_optional(self, val: UaBoolean):
        self._is_optional = val
        self._value.isOptional = val._val

    @member_name.setter
    def member_name(self, val: CString):
        self._member_name = val
        self._value.memberName = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaDataTypeMember) : NULL\n"

        return ("(UaDataTypeMember) :\n" +
                "\t" * (n + 1) + "member_type_index" + self._member_type_index.__str__(n + 1) +
                "\t" * (n + 1) + "padding" + self._padding.__str__(n + 1) +
                "\t" * (n + 1) + "namespace_zero" + self._namespace_zero.__str__(n + 1) +
                "\t" * (n + 1) + "is_array" + self._is_array.__str__(n + 1) +
                "\t" * (n + 1) + "is_optional" + self._is_optional.__str__(n + 1) +
                "\t" * (n + 1) + "member_name" + self._member_name.__str__(n + 1))


# +++++++++++++++++++ UaDataType +++++++++++++++++++++++
class UaDataType(UaType):
    def __init__(self, val: Void = None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataType*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DataType*", val._ptr)

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._type_id = UaNodeId(val=val.typeId, is_pointer=False)
            self._binary_encoding_id = UaNodeId(val=val.binaryEncodingId, is_pointer=False)
            self._mem_size = UaUInt16(val=val.memSize, is_pointer=False)
            self._type_index = UaUInt16(val=val.typeIndex, is_pointer=False)
            self._type_kind = UaUInt32(val=val.typeKind, is_pointer=False)
            self._pointer_free = UaUInt32(val=val.pointerFree, is_pointer=False)
            self._overlayable = UaUInt32(val=val.overlayable, is_pointer=False)
            self._members_size = UaUInt32(val=val.membersSize, is_pointer=False)
            self._members = UaDataTypeMember(val=val.members, is_pointer=True)
            self._type_name = CString(val=val.typeName, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataType")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._type_id._value[0] = _val(val.typeId)
            self._binary_encoding_id._value[0] = _val(val.binaryEncodingId)
            self._mem_size._value[0] = _val(val.memSize)
            self._type_index._value[0] = _val(val.typeIndex)
            self._type_kind._value[0] = _val(val.typeKind)
            self._pointer_free._value[0] = _val(val.pointerFree)
            self._overlayable._value[0] = _val(val.overlayable)
            self._members_size._value[0] = _val(val.membersSize)
            self._members._value = val.members
            self._type_name._value = val.typeName

    @property
    def type_id(self):
        if self._null:
            return None
        else:
            return self._type_id

    @property
    def binary_encoding_id(self):
        if self._null:
            return None
        else:
            return self._binary_encoding_id

    @property
    def mem_size(self):
        if self._null:
            return None
        else:
            return self._mem_size

    @property
    def type_index(self):
        if self._null:
            return None
        else:
            return self._type_index

    @property
    def type_kind(self):
        if self._null:
            return None
        else:
            return self._type_kind

    @property
    def pointer_free(self):
        if self._null:
            return None
        else:
            return self._pointer_free

    @property
    def overlayable(self):
        if self._null:
            return None
        else:
            return self._overlayable

    @property
    def members_size(self):
        if self._null:
            return None
        else:
            return self._members_size

    @property
    def members(self):
        if self._null:
            return None
        else:
            return self._members

    @property
    def type_name(self):
        if self._null:
            return None
        else:
            return self._type_name

    @type_id.setter
    def type_id(self, val: UaNodeId):
        self._type_id = val
        self._value.typeId = val._val

    @binary_encoding_id.setter
    def binary_encoding_id(self, val: UaNodeId):
        self._binary_encoding_id = val
        self._value.binaryEncodingId = val._val

    @mem_size.setter
    def mem_size(self, val: UaUInt16):
        self._mem_size = val
        self._value.memSize = val._val

    @type_index.setter
    def type_index(self, val: UaUInt16):
        self._type_index = val
        self._value.typeIndex = val._val

    @type_kind.setter
    def type_kind(self, val: UaUInt32):
        self._type_kind = val
        self._value.typeKind = val._val

    @pointer_free.setter
    def pointer_free(self, val: UaUInt32):
        self._pointer_free = val
        self._value.pointerFree = val._val

    @overlayable.setter
    def overlayable(self, val: UaUInt32):
        self._overlayable = val
        self._value.overlayable = val._val

    @members_size.setter
    def members_size(self, val: UaUInt32):
        self._members_size = val
        self._value.membersSize = val._val

    @members.setter
    def members(self, val: UaDataTypeMember):
        self._members = val
        self._value.members = val._ptr

    @type_name.setter
    def type_name(self, val: CString):
        self._type_name = val
        self._value.typeName = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaDataType) : NULL\n"

        return ("(UaDataType) :\n" +
                "\t" * (n + 1) + "type_id" + self._type_id.__str__(n + 1) +
                "\t" * (n + 1) + "binary_encoding_id" + self._binary_encoding_id.__str__(n + 1) +
                "\t" * (n + 1) + "mem_size" + self._mem_size.__str__(n + 1) +
                "\t" * (n + 1) + "type_index" + self._type_index.__str__(n + 1) +
                "\t" * (n + 1) + "type_kind" + self._type_kind.__str__(n + 1) +
                "\t" * (n + 1) + "pointer_free" + self._pointer_free.__str__(n + 1) +
                "\t" * (n + 1) + "overlayable" + self._overlayable.__str__(n + 1) +
                "\t" * (n + 1) + "members_size" + self._members_size.__str__(n + 1) +
                "\t" * (n + 1) + "members" + self._members.__str__(n + 1) +
                "\t" * (n + 1) + "type_name" + self._type_name.__str__(n + 1))

    def is_numeric(self):
        return lib.UA_DataType_isNumeric(self._ptr)

    @staticmethod
    def find_by_node_id(type_id: UaNodeId):
        return UaDataType(val=ffi.new("UA_DataType*", lib.UA_findDataType(type_id._ptr)), is_pointer=True)

    # TODO: generic type handling!!!
    # ----> init, copy, new, array_new, array_copy should be methods of a class, which represent members of an in an
    # attribute provided UaDataType
    # returns void ptr
    def new_instance(self):
        return lib.UA_new(self._ptr)

    # TODO: handling difficult, cast to something?
    def new_array(self, size: SizeT):
        return Void(val=lib.UA_Array_new(size._val, self._ptr))


# +++++++++++++++++++ UaDataTypeArray +++++++++++++++++++++++
class UaDataTypeArray(UaType):
    def __init__(self, val: Void = None, is_pointer=False):
        if val is None:
            val = ffi.new("UA_DataTypeArray*")
        if isinstance(val, UaType):
            val = ffi.cast("UA_DataTypeArray*", val._ptr)

        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
            self._next = UaDataTypeArray(val=val.next, is_pointer=True)
            self._types_size = SizeT(val=val.typesSize, is_pointer=False)
            self._types = UaDataType(val=val.types, is_pointer=True)

    def _update(self):
        self.__init__(val=self._ptr)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "UA_DataTypeArray")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
            self._next._value = val.next
            self._types_size._value[0] = _val(val.typesSize)
            self._types._value = val.types

    @property
    def next(self):
        if self._null:
            return None
        else:
            return self._next

    @property
    def types_size(self):
        if self._null:
            return None
        else:
            return self._types_size

    @property
    def types(self):
        if self._null:
            return None
        else:
            return self._types

    @next.setter
    def next(self, val: 'UaDataTypeArray'):
        self._next = val
        self._value.next = val._ptr

    @types_size.setter
    def types_size(self, val: SizeT):
        self._types_size = val
        self._value.typesSize = val._val

    @types.setter
    def types(self, val: UaDataType):
        self._types = val
        self._value.types = val._ptr

    def __str__(self, n=0):
        if self._null:
            return "(UaDataTypeArray) : NULL\n"

        return ("(UaDataTypeArray) :\n" +
                "\t" * (n + 1) + "next" + self._next.__str__(n + 1) +
                "\t" * (n + 1) + "types_size" + self._types_size.__str__(n + 1) +
                "\t" * (n + 1) + "types" + self._types.__str__(n + 1))


class Randomize:
    @staticmethod
    def random_uint_32():
        return UaUInt32(val=lib.UA_UInt32_random())

    @staticmethod
    def ua_random_seed(seed: int):
        lib.UA_random_seed(ffi.cast("UA_UInt64", seed))
