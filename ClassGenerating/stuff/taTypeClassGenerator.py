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
    def __init__(self, val=ffi.new("{struct_name}*, is_pointer=False")):
        super().__init__(val, is_pointer)\n"""

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
    def __str__(self):
        return ("{to_python_class_name(struct_name)}:\\n" + """ +
                  " +".join(map(lambda s: f"\n{tab*4}self._{s}.str_helper(1)",
                                map(lambda s: inflection.underscore(s), attribute_to_type.keys()))) +
                  f")\n{tab}")

    class_str += (f"""
    def str_helper(self, n: int):
        return ("\\t"*n + "{to_python_class_name(struct_name)}:\\n" + """ +
                  " +".join(map(lambda s: f"\n{tab * 4}self._{s}.str_helper(n+1)",
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

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("{enum_name}*"), is_pointer)
            self._p_value = None
        else:
            super().__init__(val, is_pointer)
            self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        if val in self.val_to_string.keys():
            self._p_value = val
            super().__init__(ffi.new("{enum_name}*", val), self._is_pointer)
        else:
            raise OverflowError(f"{{val}} is not a valid member of this class")

    def __str__(self):
        return f"{to_python_class_name(enum_name)}: {{self.val_to_string[self._p_value]}} ({{str(self._p_value)}})"

    def str_helper(self, n: int):
        return "\\t" * n + str(self)


"""
    return class_str


def to_python_class_name(open62541_name: str):
    if open62541_name[0:3] == "UA_":
        return open62541_name.replace("UA_", "Ua")
    elif "size_t" in open62541_name:
        print(open62541_name)
        return "SizeT"
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
    
    
typedef struct {
    UA_UInt16 memberTypeIndex;
    UA_Byte   padding;
    UA_Boolean namespaceZero;
    UA_Boolean isArray;
    UA_Boolean isOptional;
    char *memberName;
} UA_DataTypeMember;



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
    return struct_list


struct_list = defs_from_h()
print(struct_list)

print(ua_struct_class_generator(struct_list[0][0], struct_list[0][1]))

