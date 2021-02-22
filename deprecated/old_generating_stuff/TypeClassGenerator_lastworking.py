import xml.etree.ElementTree as ET
import re
import inflection


# attribute_to_type is a dict {"<attributename>": ("<attributename>", <is pointer>)...}
# The use of this class generator is base on two assumptions:
#   1. syntax: the struct name starts with UA_
#   2. semantics: there were already python classes generated for all nested types of the struct
#       -> especially: there are classes for the base types (as stop for the recursion)

# TODO? cannot handle const attributes!!!
# TODO: NodeIds

def generator_primitive(prim_name: str):
    tab = "    "
    new_line = "\n"
    quote = "\""
    backslash = "\\"
    l_brace = "{"
    r_brace = "}"

    class_str = f"""# +++++++++++++++++++ {to_python_class_name(prim_name)} +++++++++++++++++++++++
class {to_python_class_name(prim_name)}(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("{prim_name}*"), is_pointer)
        else:
            super().__init__(ffi.cast("{prim_name}", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = ffi.cast("{prim_name}", _val(val))

    def __str__(self, n=0):
        return "({to_python_class_name(prim_name)}): " + str(self._value) + "\\n"


"""
    return class_str


def generator_struct(struct_name: str, attribute_to_type: dict):
    tab = "    "
    new_line = "\n"
    quote = "\""
    backslash = "\\"

    class_str = f"""# +++++++++++++++++++ {to_python_class_name(struct_name)} +++++++++++++++++++++++
class {to_python_class_name(struct_name)}(UaType):
    def __init__(self, val=ffi.new("{struct_name}*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        
{new_line.join(map(
        lambda attr:
        tab * 2 + f"self._{inflection.underscore(attr)} = {to_python_class_name(attribute_to_type[attr][0])}(val=val.{attr}, is_pointer={attribute_to_type[attr][1]})",
        attribute_to_type.keys()))}

    @UaType._value.setter
    def _value(self, val):
        self.__value[0] = _val(val)
{new_line.join(map(
        lambda attr:
        tab * 2 + f"self._{inflection.underscore(attr)}.__value[0] = _val(val.{attr})",
        attribute_to_type.keys()))}
    
{(new_line * 2).join(map(
        lambda attr:
        tab + f"@property" + new_line +
        tab + f"def {inflection.underscore(attr)}(self):" + new_line +
        tab * 2 + f"return self._{inflection.underscore(attr)}",
        attribute_to_type.keys()))}
    
{(new_line * 2).join(map(
        lambda attr:
        tab + f"@{inflection.underscore(attr)}.setter" + new_line +
        tab + f"def {inflection.underscore(attr)}(self, val):" + new_line +
        tab * 2 + f"self._{inflection.underscore(attr)} = val" + new_line +
        tab * 2 + f"self._value.{attr} = val._value",
        attribute_to_type.keys()))}

    def __str__(self, n=0):
        return ("({to_python_class_name(struct_name)}) :\\n" +
{new_line.join(map(
        lambda attr:
        tab*4 + f"{quote}{backslash}t{quote}*(n+1) + {quote}{inflection.underscore(attr)}{quote} + self._{inflection.underscore(attr)}.__str__(n+1) +",
        attribute_to_type.keys()))} "\\n")


"""
    return class_str


def generator_enum(enum_name: str, ident_to_val: dict):
    tab = "    "
    new_line = "\n"
    quote = "\""
    l_brace = "{"
    r_brace = "}"

    class_str = f"""# +++++++++++++++++++ {to_python_class_name(enum_name)} +++++++++++++++++++++++
class {to_python_class_name(enum_name)}(UaType):
{new_line.join(map(
        lambda attr:
        f"{tab}{attr} = {ident_to_val[attr]}",
        ident_to_val.keys()))}

    val_to_string = dict([
{("," + new_line).join(map(
        lambda attr:
        f"{tab * 2}({ident_to_val[attr]}, {quote}{attr}{quote})",
        ident_to_val.keys()))}])

    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("{enum_name}*"), is_pointer)
        else:
            super().__init__(ffi.cast("{enum_name}", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self.__value[0] = _val(val)
        else:
            raise OverflowError(f"{l_brace}val{r_brace} is not a valid member of this class")

    def __str__(self, n=0):
        return f"({to_python_class_name(enum_name)
    }): {l_brace}self.val_to_string[self._value]{r_brace} ({l_brace}str(self._value){r_brace})\\n"


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


def defs_from_h(file_name: str):
    f = open(file_name, "r")
    ffi_defs = f.read()
    f.close()

    res = re.findall(r"typedef enum \{\n((.*,\n)*.*\n)(.*?;\n)",
                     ffi_defs)
    res = map(lambda x: (get_type_name(x[2]),
                         get_attr_to_val(x[0])),
              res)

    enum_list = list(res)

    res = re.findall(r"typedef struct \{\n((.*;\n)*?)(\}.*?;\n)",
                     ffi_defs)
    res = map(lambda x: (get_type_name(x[2]),
                         get_attr_to_type(x[0])),
              res)

    struct_list = list(res)

    return struct_list, enum_list


def generate_defs(file_name: str):
    struct_list, enum_list = defs_from_h(file_name)

    type_classes = """
# -------------------------------------------------------------
# --------------------------- Enums ---------------------------
# -------------------------------------------------------------

"""
    type_classes += "".join(map(lambda pair: generator_enum(pair[0], pair[1]), enum_list))

    type_classes += """
# -------------------------------------------------------------
# -------------------------- Structs --------------------------
# -------------------------------------------------------------
    
"""
    type_classes += "".join(map(lambda pair: generator_struct(pair[0], pair[1]), struct_list))

    handle = open(f"{file_name}.py", "w")
    handle.write(type_classes)
    handle.close()


def generate_defs_primitive(prim_list):
    type_classes = "".join(map(lambda type_name: generator_primitive(type_name), prim_list))

    handle = open("types_primitive.py", "w")
    handle.write(type_classes)
    handle.close()


generate_defs("types_generated")
generate_defs("common_edited")
generate_defs("types_struct_enum")
generate_defs_primitive(["UA_Boolean",
                         "UA_SByte",
                         "UA_Byte",
                         "UA_Int16",
                         "UA_UInt16",
                         "UA_Int32",
                         "UA_UInt32",
                         "UA_Int64",
                         "UA_UInt64",
                         "UA_Float",
                         "UA_Double",
                         "UA_StatusCode",
                         "UA_DateTime"])

# remember: UA_ExtensionObject
