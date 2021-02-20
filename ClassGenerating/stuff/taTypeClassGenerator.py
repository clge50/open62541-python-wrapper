import xml.etree.ElementTree as ET
import re
import inflection

# attribute_to_type is a dict {"<attributename>": ("<attributename>", <is pointer>)...}
# The use of this class generator is base on two assumptions:
#   1. syntax: the struct name starts with UA_
#   2. semantics: there were already python classes generated for all nested types of the struct
#       -> especially: there are classes for the base types (as stop for the recursion)

#TODO? cannot handle const attributes!!!
def ua_struct_class_generator(struct_name: str, attribute_to_type: dict):
    tab = "    "
    empty = ""
    pointer_str = ", is_pointer=True"
    class_str = f"""# +++++++++++++++++++ {to_python_class_name(struct_name)} +++++++++++++++++++++++
"""
    class_str += """class """ + to_python_class_name(struct_name) + f"""(UaType):
    def __init__(self, val=ffi.new("{struct_name}*"), is_pointer=False):
        super().__init__(val, {struct_name}, is_pointer)\n"""

    for attribute, typename in attribute_to_type.items():
        class_str += f"{tab * 2}self._{inflection.underscore(attribute)} = " \
                     f"{to_python_class_name(typename[0])}(val=val.{attribute}{pointer_str if typename[1] else empty})\n"
    class_str += f"{tab}\n"

    for attribute, typename in attribute_to_type.items():
        class_str += f"""
    @property
    def {inflection.underscore(attribute)}(self):
        return self._{inflection.underscore(attribute)}

    @{inflection.underscore(attribute)}.setter
    def {inflection.underscore(attribute)}(self, val):
        self._{inflection.underscore(attribute)} = val
        self._value.{attribute} = val.value
"""

    class_str += (f"""
    def __str__(self, n=0):
        return ("\\t"*n + "{to_python_class_name(struct_name)}:\\n" + """ +
                  " +".join(map(lambda s: f"\n{tab*4}self._{s}.str_helper(n+1)",
                                map(lambda s: inflection.underscore(s), attribute_to_type.keys()))) +
                  f")\n")

    return class_str


def ua_enum_class_generator(enum_name: str, ident_to_val: dict):
    tab = "    "
    quotes = "\""
    newline = "\n"
    class_str = f"""# +++++++++++++++++++ {to_python_class_name(enum_name)} +++++++++++++++++++++++
"""
    class_str += f"""class {to_python_class_name(enum_name)}(UaType):
{newline.join(map(lambda ident: f"{tab}{ident} = {ident_to_val[ident]}", ident_to_val.keys()))}

    val_to_string = dict([
{f",{newline}".join(map(lambda ident: f"{tab}{tab}({ident_to_val[ident]}, {quotes + ident + quotes})", ident_to_val.keys()))}])

    def __init__(self, p_val=0, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("{enum_name}*", p_val), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, {enum_name}, is_pointer)
            self._p_value = self._value[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, p_val):
        if p_val in self.val_to_string.keys():
            self._p_value = p_val
            super().__init__(ffi.new("{enum_name}*", p_val), self._is_pointer)
        else:
            raise OverflowError(f"{{val}} is not a valid member of this class")

    def __str__(self, n=0):
        return "\\t"*n + "f"{to_python_class_name(enum_name)}: {{self.val_to_string[self._p_value]}} ({{str(self._p_value)}})\\n"
"""
    return class_str


def to_python_class_name(open62541_name: str):
    if open62541_name[0:3] == "UA_":
        return open62541_name.replace("UA_", "Ua")
    elif "size_t" in open62541_name:
        print(open62541_name)
        return "SizeT"
    elif "char" in open62541_name:
        print(open62541_name)
        return "CString"
    else:
        return inflection.underscore(open62541_name)


def defs_from_xml():
    tree = ET.parse('Opc.Ua.Types.bsd')
    root = tree.getroot()
    enums = []
    structs = []

    for child in root:
        if "EnumeratedType" in child.tag:
            enums.append(child)
        elif "StructuredType" in child.tag:
            structs.append(child)

    enums2 = []
    for e in enums:
        attribute_value_list = []
        for c in e:
            try:
                attribute_value_list.append(
                    (f"UA_{e.attrib['Name']}_{c.attrib['Name']}".upper(), int(c.attrib['Value'])))
            except KeyError:
                pass
        enums2.append(('UA_' + e.attrib['Name'], dict(attribute_value_list)))

    structs2 = []
    for e in structs:
        attribute_type_list = []
        for c in e:
            try:
                attribute_type_list.append((c.attrib['Name'], c.attrib['TypeName'].replace("opc:", "UA_")))
            except KeyError:
                pass
        structs2.append(('UA_' + e.attrib['Name'], dict(attribute_type_list)))

    enums = dict(enums2)
    structs = dict(structs2)

    return structs, enums


def get_attr_to_type(s: str):
    attr_type = []

    for line in s.splitlines():
        is_pointer = False
        if "*" in line:
            is_pointer = True
            line = line.replace("*", "")
        line = line.replace(";", "").strip()
        pair = line.split(" ")
        pair = (pair[1], (pair[0], is_pointer))
        attr_type.append(pair)

    return dict(attr_type)


def get_attr_to_val(s: str):
    attr_val = []

    for line in s.splitlines():
        line = line.replace(",", "").strip()
        pair = line.split(" = ")
        pair = (pair[0], int(pair[1], 0))
        attr_val.append(pair)

    return dict(attr_val)


def get_type_name(s: str):
    return s.replace("}", "").replace(";", "").strip()


def defs_from_h():
    types_generated = """

typedef enum {
 UA_ATTRIBUTEID_NODEID = 1,
 UA_ATTRIBUTEID_NODECLASS = 2,
 UA_ATTRIBUTEID_BROWSENAME = 3,
 UA_ATTRIBUTEID_DISPLAYNAME = 4,
 UA_ATTRIBUTEID_DESCRIPTION = 5,
 UA_ATTRIBUTEID_WRITEMASK = 6,
 UA_ATTRIBUTEID_USERWRITEMASK = 7,
 UA_ATTRIBUTEID_ISABSTRACT = 8,
 UA_ATTRIBUTEID_SYMMETRIC = 9,
 UA_ATTRIBUTEID_INVERSENAME = 10,
 UA_ATTRIBUTEID_CONTAINSNOLOOPS = 11,
 UA_ATTRIBUTEID_EVENTNOTIFIER = 12,
 UA_ATTRIBUTEID_VALUE = 13,
 UA_ATTRIBUTEID_DATATYPE = 14,
 UA_ATTRIBUTEID_VALUERANK = 15,
 UA_ATTRIBUTEID_ARRAYDIMENSIONS = 16,
 UA_ATTRIBUTEID_ACCESSLEVEL = 17,
 UA_ATTRIBUTEID_USERACCESSLEVEL = 18,
 UA_ATTRIBUTEID_MINIMUMSAMPLINGINTERVAL = 19,
 UA_ATTRIBUTEID_HISTORIZING = 20,
 UA_ATTRIBUTEID_EXECUTABLE = 21,
 UA_ATTRIBUTEID_USEREXECUTABLE = 22,
 UA_ATTRIBUTEID_DATATYPEDEFINITION = 23,
 UA_ATTRIBUTEID_ROLEPERMISSIONS = 24,
 UA_ATTRIBUTEID_USERROLEPERMISSIONS = 25,
 UA_ATTRIBUTEID_ACCESSRESTRICTIONS = 26,
 UA_ATTRIBUTEID_ACCESSLEVELEX = 27
} UA_AttributeId;


typedef enum {
 UA_RULEHANDLING_DEFAULT = 0,
 UA_RULEHANDLING_ABORT = 1,
 UA_RULEHANDLING_WARN = 2,
 UA_RULEHANDLING_ACCEPT = 3,
} UA_RuleHandling;


typedef enum {
 UA_ORDER_LESS = -1,
 UA_ORDER_EQ = 0,
 UA_ORDER_MORE = 1
} UA_Order;


typedef enum {
 UA_SECURECHANNELSTATE_CLOSED = 0,
 UA_SECURECHANNELSTATE_HEL_SENT = 1,
 UA_SECURECHANNELSTATE_HEL_RECEIVED = 2,
 UA_SECURECHANNELSTATE_ACK_SENT = 3,
 UA_SECURECHANNELSTATE_ACK_RECEIVED = 4,
 UA_SECURECHANNELSTATE_OPN_SENT = 5,
 UA_SECURECHANNELSTATE_OPEN = 6,
 UA_SECURECHANNELSTATE_CLOSING = 7
} UA_SecureChannelState;


typedef enum {
 UA_SESSIONSTATE_CLOSED = 0,
 UA_SESSIONSTATE_CREATE_REQUESTED = 1,
 UA_SESSIONSTATE_CREATED = 2,
 UA_SESSIONSTATE_ACTIVATE_REQUESTED = 3,
 UA_SESSIONSTATE_ACTIVATED = 4,
 UA_SESSIONSTATE_CLOSING = 5
} UA_SessionState;


typedef struct {
 size_t currentConnectionCount;
 size_t cumulatedConnectionCount;
 size_t rejectedConnectionCount;
 size_t connectionTimeoutCount;
 size_t connectionAbortCount;
} UA_NetworkStatistics;


typedef struct {
 size_t currentChannelCount;
 size_t cumulatedChannelCount;
 size_t rejectedChannelCount;
 size_t channelTimeoutCount;
 size_t channelAbortCount;
 size_t channelPurgeCount;
} UA_SecureChannelStatistics;


typedef struct {
 size_t currentSessionCount;
 size_t cumulatedSessionCount;
 size_t securityRejectedSessionCount;
 size_t rejectedSessionCount;
 size_t sessionTimeoutCount;
 size_t sessionAbortCount;
} UA_SessionStatistics;


typedef struct UA_DateTimeStruct {
 UA_UInt16 nanoSec;
 UA_UInt16 microSec;
 UA_UInt16 milliSec;
 UA_UInt16 sec;
 UA_UInt16 min;
 UA_UInt16 hour;
 UA_UInt16 day;
 UA_UInt16 month;
 UA_UInt16 year;
} UA_DateTimeStruct;



typedef struct {
 UA_UInt32 data1;
 UA_UInt16 data2;
 UA_UInt16 data3;
 UA_Byte data4[8];
} UA_Guid;


typedef enum UA_NodeIdType {
 UA_NODEIDTYPE_NUMERIC = 0,
 UA_NODEIDTYPE_STRING = 3,
 UA_NODEIDTYPE_GUID = 4,
 UA_NODEIDTYPE_BYTESTRING = 5
};


typedef struct {
 UA_NodeId nodeId;
 UA_String namespaceUri;
 UA_UInt32 serverIndex;
} UA_ExpandedNodeId;


typedef struct {
 UA_UInt16 namespaceIndex;
 UA_String name;
} UA_QualifiedName;


typedef struct {
 UA_String locale;
 UA_String text;
} UA_LocalizedText;



typedef struct {
 UA_UInt32 min;
 UA_UInt32 max;
} UA_NumericRangeDimension;


typedef struct {
 size_t dimensionsSize;
 UA_NumericRangeDimension *dimensions;
} UA_NumericRange;



typedef enum {
 UA_VARIANT_DATA = 0,
 UA_VARIANT_DATA_NODELETE = 1
} UA_VariantStorageType;

typedef struct {
 const UA_DataType *type;
 UA_VariantStorageType storageType;
 size_t arrayLength;
 void *data;
 size_t arrayDimensionsSize;
 UA_UInt32 *arrayDimensions;
} UA_Variant;


typedef enum {
 UA_EXTENSIONOBJECT_ENCODED_NOBODY = 0,
 UA_EXTENSIONOBJECT_ENCODED_BYTESTRING = 1,
 UA_EXTENSIONOBJECT_ENCODED_XML = 2,
 UA_EXTENSIONOBJECT_DECODED = 3,
 UA_EXTENSIONOBJECT_DECODED_NODELETE = 4
} UA_ExtensionObjectEncoding;



typedef struct {
 UA_Variant value;
 UA_DateTime sourceTimestamp;
 UA_DateTime serverTimestamp;
 UA_UInt16 sourcePicoseconds;
 UA_UInt16 serverPicoseconds;
 UA_StatusCode status;
 UA_Boolean hasValue;
 UA_Boolean hasStatus;
 UA_Boolean hasSourceTimestamp;
 UA_Boolean hasServerTimestamp;
 UA_Boolean hasSourcePicoseconds;
 UA_Boolean hasServerPicoseconds;
} UA_DataValue;



typedef struct UA_DiagnosticInfo {
 UA_Boolean hasSymbolicId;
 UA_Boolean hasNamespaceUri;
 UA_Boolean hasLocalizedText;
 UA_Boolean hasLocale;
 UA_Boolean hasAdditionalInfo;
 UA_Boolean hasInnerStatusCode;
 UA_Boolean hasInnerDiagnosticInfo;
 UA_Int32 symbolicId;
 UA_Int32 namespaceUri;
 UA_Int32 localizedText;
 UA_Int32 locale;
 UA_String additionalInfo;
 UA_StatusCode innerStatusCode;
 struct UA_DiagnosticInfo *innerDiagnosticInfo;
} UA_DiagnosticInfo;



typedef struct {
 UA_UInt16 memberTypeIndex;
 UA_Byte padding;
 UA_Boolean namespaceZero;
 UA_Boolean isArray;
 UA_Boolean isOptional;
 const char *memberName;

} UA_DataTypeMember;



typedef enum {
 UA_DATATYPEKIND_BOOLEAN = 0,
 UA_DATATYPEKIND_SBYTE = 1,
 UA_DATATYPEKIND_BYTE = 2,
 UA_DATATYPEKIND_INT16 = 3,
 UA_DATATYPEKIND_UINT16 = 4,
 UA_DATATYPEKIND_INT32 = 5,
 UA_DATATYPEKIND_UINT32 = 6,
 UA_DATATYPEKIND_INT64 = 7,
 UA_DATATYPEKIND_UINT64 = 8,
 UA_DATATYPEKIND_FLOAT = 9,
 UA_DATATYPEKIND_DOUBLE = 10,
 UA_DATATYPEKIND_STRING = 11,
 UA_DATATYPEKIND_DATETIME = 12,
 UA_DATATYPEKIND_GUID = 13,
 UA_DATATYPEKIND_BYTESTRING = 14,
 UA_DATATYPEKIND_XMLELEMENT = 15,
 UA_DATATYPEKIND_NODEID = 16,
 UA_DATATYPEKIND_EXPANDEDNODEID = 17,
 UA_DATATYPEKIND_STATUSCODE = 18,
 UA_DATATYPEKIND_QUALIFIEDNAME = 19,
 UA_DATATYPEKIND_LOCALIZEDTEXT = 20,
 UA_DATATYPEKIND_EXTENSIONOBJECT = 21,
 UA_DATATYPEKIND_DATAVALUE = 22,
 UA_DATATYPEKIND_VARIANT = 23,
 UA_DATATYPEKIND_DIAGNOSTICINFO = 24,
 UA_DATATYPEKIND_DECIMAL = 25,
 UA_DATATYPEKIND_ENUM = 26,
 UA_DATATYPEKIND_STRUCTURE = 27,
 UA_DATATYPEKIND_OPTSTRUCT = 28,
 UA_DATATYPEKIND_UNION = 29,
 UA_DATATYPEKIND_BITFIELDCLUSTER = 30
} UA_DataTypeKind;



typedef struct {
 UA_NodeId typeId;
 UA_NodeId binaryEncodingId;
 UA_UInt16 memSize;
 UA_UInt16 typeIndex;
 UA_UInt32 typeKind;
 UA_UInt32 pointerFree;
 UA_UInt32 overlayable;
 UA_UInt32 membersSize;
 UA_DataTypeMember *members;
 char *typeName;
} UA_DataType;



typedef struct UA_DataTypeArray {
 struct UA_DataTypeArray *next;
 size_t typesSize;
 UA_DataType *types;
} UA_DataTypeArray;


    
    
    """
    res = re.findall(r"typedef enum \{\n((.*,\n)*.*\n)(.*?;\n)",
                     types_generated)
    res = map(lambda x: (get_type_name(x[2]),
                         get_attr_to_val(x[0])),
              res)
    enum_list = list(res)
    res = re.findall(r"typedef struct \{\n((.*;\n)*?)(\}.*?;\n)",
                     types_generated)
    res = map(lambda x: (get_type_name(x[2]),
                         get_attr_to_type(x[0])),
              res)

    struct_list = list(res)
    return struct_list, enum_list


struct_list, enum_list = defs_from_h()
print(struct_list)
print(enum_list)

type_classes = "".join(map(lambda pair: ua_enum_class_generator(pair[0], pair[1]), enum_list))
type_classes += "\n\n".join(map(lambda pair: ua_struct_class_generator(pair[0], pair[1]), struct_list))

print(ua_struct_class_generator(struct_list[0][0], struct_list[0][1]))

var = [('UA_NetworkStatistics',
        {'currentConnectionCount': ('size_t', False), 'cumulatedConnectionCount': ('size_t', False),
         'rejectedConnectionCount': ('size_t', False), 'connectionTimeoutCount': ('size_t', False),
         'connectionAbortCount': ('size_t', False)}), ('UA_SecureChannelStatistics',
                                                       {'currentChannelCount': ('size_t', False),
                                                        'cumulatedChannelCount': ('size_t', False),
                                                        'rejectedChannelCount': ('size_t', False),
                                                        'channelTimeoutCount': ('size_t', False),
                                                        'channelAbortCount': ('size_t', False),
                                                        'channelPurgeCount': ('size_t', False)}), (
       'UA_SessionStatistics', {'currentSessionCount': ('size_t', False), 'cumulatedSessionCount': ('size_t', False),
                                'securityRejectedSessionCount': ('size_t', False),
                                'rejectedSessionCount': ('size_t', False), 'sessionTimeoutCount': ('size_t', False),
                                'sessionAbortCount': ('size_t', False)}), ('UA_Guid', {'data1': ('UA_UInt32', False),
                                                                                       'data2': ('UA_UInt16', False),
                                                                                       'data3': ('UA_UInt16', False),
                                                                                       'data4[8]': ('UA_Byte', False)}),
       ('UA_ExpandedNodeId',
        {'nodeId': ('UA_NodeId', False), 'namespaceUri': ('UA_String', False), 'serverIndex': ('UA_UInt32', False)}),
       ('UA_QualifiedName', {'namespaceIndex': ('UA_UInt16', False), 'name': ('UA_String', False)}),
       ('UA_LocalizedText', {'locale': ('UA_String', False), 'text': ('UA_String', False)}),
       ('UA_NumericRangeDimension', {'min': ('UA_UInt32', False), 'max': ('UA_UInt32', False)}),
       ('UA_NumericRange', {'dimensionsSize': ('size_t', False), 'dimensions': ('UA_NumericRangeDimension', True)}), (
       'UA_Variant', {'UA_DataType': ('const', True), 'storageType': ('UA_VariantStorageType', False),
                      'arrayLength': ('size_t', False), 'data': ('void', True),
                      'arrayDimensionsSize': ('size_t', False), 'arrayDimensions': ('UA_UInt32', True)}), (
       'UA_DataValue', {'value': ('UA_Variant', False), 'sourceTimestamp': ('UA_DateTime', False),
                        'serverTimestamp': ('UA_DateTime', False), 'sourcePicoseconds': ('UA_UInt16', False),
                        'serverPicoseconds': ('UA_UInt16', False), 'status': ('UA_StatusCode', False),
                        'hasValue': ('UA_Boolean', False), 'hasStatus': ('UA_Boolean', False),
                        'hasSourceTimestamp': ('UA_Boolean', False), 'hasServerTimestamp': ('UA_Boolean', False),
                        'hasSourcePicoseconds': ('UA_Boolean', False), 'hasServerPicoseconds': ('UA_Boolean', False)}),
       ('UA_DataType',
        {'typeId': ('UA_NodeId', False), 'binaryEncodingId': ('UA_NodeId', False), 'memSize': ('UA_UInt16', False),
         'typeIndex': ('UA_UInt16', False), 'typeKind': ('UA_UInt32', False), 'pointerFree': ('UA_UInt32', False),
         'overlayable': ('UA_UInt32', False), 'membersSize': ('UA_UInt32', False),
         'members': ('UA_DataTypeMember', True), 'typeName': ('char', True)})]
var = [('UA_AttributeId', {'UA_ATTRIBUTEID_NODEID': 1, 'UA_ATTRIBUTEID_NODECLASS': 2, 'UA_ATTRIBUTEID_BROWSENAME': 3,
                           'UA_ATTRIBUTEID_DISPLAYNAME': 4, 'UA_ATTRIBUTEID_DESCRIPTION': 5,
                           'UA_ATTRIBUTEID_WRITEMASK': 6, 'UA_ATTRIBUTEID_USERWRITEMASK': 7,
                           'UA_ATTRIBUTEID_ISABSTRACT': 8, 'UA_ATTRIBUTEID_SYMMETRIC': 9,
                           'UA_ATTRIBUTEID_INVERSENAME': 10, 'UA_ATTRIBUTEID_CONTAINSNOLOOPS': 11,
                           'UA_ATTRIBUTEID_EVENTNOTIFIER': 12, 'UA_ATTRIBUTEID_VALUE': 13,
                           'UA_ATTRIBUTEID_DATATYPE': 14, 'UA_ATTRIBUTEID_VALUERANK': 15,
                           'UA_ATTRIBUTEID_ARRAYDIMENSIONS': 16, 'UA_ATTRIBUTEID_ACCESSLEVEL': 17,
                           'UA_ATTRIBUTEID_USERACCESSLEVEL': 18, 'UA_ATTRIBUTEID_MINIMUMSAMPLINGINTERVAL': 19,
                           'UA_ATTRIBUTEID_HISTORIZING': 20, 'UA_ATTRIBUTEID_EXECUTABLE': 21,
                           'UA_ATTRIBUTEID_USEREXECUTABLE': 22, 'UA_ATTRIBUTEID_DATATYPEDEFINITION': 23,
                           'UA_ATTRIBUTEID_ROLEPERMISSIONS': 24, 'UA_ATTRIBUTEID_USERROLEPERMISSIONS': 25,
                           'UA_ATTRIBUTEID_ACCESSRESTRICTIONS': 26, 'UA_ATTRIBUTEID_ACCESSLEVELEX': 27}), (
       'UA_RuleHandling', {'UA_RULEHANDLING_DEFAULT': 0, 'UA_RULEHANDLING_ABORT': 1, 'UA_RULEHANDLING_WARN': 2,
                           'UA_RULEHANDLING_ACCEPT': 3}),
       ('UA_Order', {'UA_ORDER_LESS': -1, 'UA_ORDER_EQ': 0, 'UA_ORDER_MORE': 1}), ('UA_SecureChannelState',
                                                                                   {'UA_SECURECHANNELSTATE_CLOSED': 0,
                                                                                    'UA_SECURECHANNELSTATE_HEL_SENT': 1,
                                                                                    'UA_SECURECHANNELSTATE_HEL_RECEIVED': 2,
                                                                                    'UA_SECURECHANNELSTATE_ACK_SENT': 3,
                                                                                    'UA_SECURECHANNELSTATE_ACK_RECEIVED': 4,
                                                                                    'UA_SECURECHANNELSTATE_OPN_SENT': 5,
                                                                                    'UA_SECURECHANNELSTATE_OPEN': 6,
                                                                                    'UA_SECURECHANNELSTATE_CLOSING': 7}),
       ('UA_SessionState',
        {'UA_SESSIONSTATE_CLOSED': 0, 'UA_SESSIONSTATE_CREATE_REQUESTED': 1, 'UA_SESSIONSTATE_CREATED': 2,
         'UA_SESSIONSTATE_ACTIVATE_REQUESTED': 3, 'UA_SESSIONSTATE_ACTIVATED': 4, 'UA_SESSIONSTATE_CLOSING': 5}),
       ('UA_VariantStorageType', {'UA_VARIANT_DATA': 0, 'UA_VARIANT_DATA_NODELETE': 1}), ('UA_ExtensionObjectEncoding',
                                                                                          {
                                                                                              'UA_EXTENSIONOBJECT_ENCODED_NOBODY': 0,
                                                                                              'UA_EXTENSIONOBJECT_ENCODED_BYTESTRING': 1,
                                                                                              'UA_EXTENSIONOBJECT_ENCODED_XML': 2,
                                                                                              'UA_EXTENSIONOBJECT_DECODED': 3,
                                                                                              'UA_EXTENSIONOBJECT_DECODED_NODELETE': 4}),
       ('UA_DataTypeKind', {'UA_DATATYPEKIND_BOOLEAN': 0, 'UA_DATATYPEKIND_SBYTE': 1, 'UA_DATATYPEKIND_BYTE': 2,
                            'UA_DATATYPEKIND_INT16': 3, 'UA_DATATYPEKIND_UINT16': 4, 'UA_DATATYPEKIND_INT32': 5,
                            'UA_DATATYPEKIND_UINT32': 6, 'UA_DATATYPEKIND_INT64': 7, 'UA_DATATYPEKIND_UINT64': 8,
                            'UA_DATATYPEKIND_FLOAT': 9, 'UA_DATATYPEKIND_DOUBLE': 10, 'UA_DATATYPEKIND_STRING': 11,
                            'UA_DATATYPEKIND_DATETIME': 12, 'UA_DATATYPEKIND_GUID': 13,
                            'UA_DATATYPEKIND_BYTESTRING': 14, 'UA_DATATYPEKIND_XMLELEMENT': 15,
                            'UA_DATATYPEKIND_NODEID': 16, 'UA_DATATYPEKIND_EXPANDEDNODEID': 17,
                            'UA_DATATYPEKIND_STATUSCODE': 18, 'UA_DATATYPEKIND_QUALIFIEDNAME': 19,
                            'UA_DATATYPEKIND_LOCALIZEDTEXT': 20, 'UA_DATATYPEKIND_EXTENSIONOBJECT': 21,
                            'UA_DATATYPEKIND_DATAVALUE': 22, 'UA_DATATYPEKIND_VARIANT': 23,
                            'UA_DATATYPEKIND_DIAGNOSTICINFO': 24, 'UA_DATATYPEKIND_DECIMAL': 25,
                            'UA_DATATYPEKIND_ENUM': 26, 'UA_DATATYPEKIND_STRUCTURE': 27,
                            'UA_DATATYPEKIND_OPTSTRUCT': 28, 'UA_DATATYPEKIND_UNION': 29,
                            'UA_DATATYPEKIND_BITFIELDCLUSTER': 30})]
