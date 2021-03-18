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
    UA_TYPE = UA_TYPES.{prim_name.replace("UA_", "").upper()}
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("{prim_name}*"), is_pointer)
        else:
            if type(val) is list:
                super().__init__(ffi.new("{prim_name}[]", val), True)
            elif is_pointer:
                super().__init__(val, is_pointer)
            else:
                super().__init__(ffi.new("{prim_name}*", _val(val)), is_pointer)

    @property
    def value(self):
        return int(self._val)

    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "{prim_name}")
        else:
            self._value[0] = ffi.cast("{prim_name}", _val(val))

    def __str__(self, n=0):
        return "({to_python_class_name(prim_name)}): " + str(self._val) + "\\n"

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


"""
    return class_str


def generator_struct(struct_name: str, attribute_to_type: dict):
    tab = "    "
    new_line = "\n"
    quote = "\""
    backslash = "\\"

    class_str = f"""# +++++++++++++++++++ {to_python_class_name(struct_name)} +++++++++++++++++++++++
class {to_python_class_name(struct_name)}(UaType):
    _UA_TYPE = _UA_TYPES._{struct_name.replace("UA_", "").upper()}
    
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            val = ffi.new("{struct_name}*")
        if isinstance(val, UaType):
            val = ffi.cast("{struct_name}*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
{new_line.join(map(
        lambda attr:
        tab * 3 + f"self._{to_python_ident(attr)} = {to_python_class_name(attribute_to_type[attr][0])}(val=val.{attr}, is_pointer={attribute_to_type[attr][1]})",
        attribute_to_type.keys()))}

    def _update(self):
        self.__init__(val=self._ptr)
    
    def _set_value(self, val):
        if self._is_pointer:
            self._value = _ptr(val, "{struct_name}")
        else:
            self._value[0] = _val(val)

        if not _is_null(val):
{new_line.join(map(
        lambda attr:
        tab * 3 + f"self._{to_python_ident(attr)}._value = val.{attr}"
        if attribute_to_type[attr][1] else
        tab * 3 + f"self._{to_python_ident(attr)}._value[0] = _val(val.{attr})",
        attribute_to_type.keys()))}

{(new_line * 2).join(map(
        lambda attr:
        tab + f"@property" + new_line +
        tab + f"def {to_python_ident(attr)}(self):" + new_line +
        tab * 2 + f"if self._null:" + new_line +
        tab * 3 + f"return None" + new_line +
        tab * 2 + f"else:" + new_line +
        tab * 3 + f"return self._{to_python_ident(attr)}",
        attribute_to_type.keys()))}

{(new_line * 2).join(map(
        lambda attr:
        tab + f"@{to_python_ident(attr)}.setter" + new_line +
        tab + f"def {to_python_ident(attr)}(self, val: {to_python_class_name(attribute_to_type[attr][0])}):" + new_line +
        tab * 2 + f"self._{to_python_ident(attr)} = val" + new_line +
        (tab * 2 + f"self._value.{attr} = val._ptr"
         if attribute_to_type[attr][1] else
         tab * 2 + f"self._value.{attr} = val._val"),
        attribute_to_type.keys()))}

    def __str__(self, n=0):
        if self._null:
            return "({to_python_class_name(struct_name)}) : NULL\\n"
        
        return ("({to_python_class_name(struct_name)}) :\\n"
{new_line.join(map(
        lambda attr:
        tab * 4 + "+ " + f"{quote}{backslash}t{quote}*(n+1) + {quote}{to_python_ident(attr)}{quote} + self._{to_python_ident(attr)}.__str__(n+1)",
        attribute_to_type.keys()))})


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
    _UA_TYPE = _UA_TYPES._{enum_name.replace("UA_", "").upper()}
    
    val_to_string = dict([
{("," + new_line).join(map(
        lambda attr:
        f"{tab * 2}({ident_to_val[attr]}, {quote}{attr}{quote})",
        ident_to_val.keys()))}])

    def __init__(self, val: Union[int, Void] = None, is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("{enum_name}*", val._ptr)
        if val is None:
            super().__init__(ffi.new("{enum_name}*"), is_pointer)
        else:
            super().__init__(ffi.cast("{enum_name}", _val(val)), is_pointer)

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "{enum_name}")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{l_brace}val{r_brace} is not a valid member of this class")
    
{new_line.join(map(
        lambda attr:
        f"{tab}@staticmethod" +
        f"{new_line}{tab}def {strip_enum_ident(attr)}():" +
        f"{new_line}{tab}{tab}return {to_python_class_name(enum_name)}({ident_to_val[attr]}){new_line}",
        ident_to_val.keys()))}
    def __str__(self, n=0):
        return f"({to_python_class_name(enum_name)
    }): {l_brace}self.val_to_string[self._val]{r_brace} ({l_brace}str(self._val){r_brace})\\n"


"""
    return class_str


def strip_enum_ident(attr: str):
    return "_".join(attr.split("_")[2:])


def to_python_ident(attr: str):
    if attr == "value":
        return "data_value"
    return inflection.underscore(attr)


def to_python_class_name(open62541_name: str):
    if open62541_name[0:3] == "UA_":
        return open62541_name.replace("UA_", "Ua")
    elif "size_t" in open62541_name:
        print(open62541_name)
        return "SizeT"
    elif "char" in open62541_name:
        print(open62541_name)
        return "CString"
    elif "void" in open62541_name:
        print(open62541_name)
        return "Void"
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
generate_defs("server_config")
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
