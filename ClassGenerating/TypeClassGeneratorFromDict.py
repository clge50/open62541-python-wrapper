import xml.etree.ElementTree as ET
import re
import inflection


# attribute_to_type is a dict {"<attributename>": ("<attributename>", <is pointer>)...}
# The use of this class generator is base on two assumptions:
#   1. syntax: the struct name starts with UA_
#   2. semantics: there were already python classes generated for all nested types of the struct
#       -> especially: there are classes for the base types (as stop for the recursion)

def generator_struct(struct_name: str, attribute_to_type: dict):
    tab = "    "
    new_line = "\n"
    quote = "\""
    backslash = "\\"

    class_str = f"""# +++++++++++++++++++ {to_python_class_name(struct_name)} +++++++++++++++++++++++
class {to_python_class_name(struct_name)}(UaType):
    def __init__(self, val=ffi.new("{struct_name}*"), is_pointer=False):
        if type(val) is Void:
            val = ffi.cast("{struct_name}*", val._ptr)
        super().__init__(val=val, is_pointer=is_pointer)

        if not self._null:
{new_line.join(map(
        lambda attr:
        tab * 3 + f"self._{to_python_ident(attr)} = {to_python_class_name(attribute_to_type[attr][0])}(val=val.{attr}, is_pointer={attribute_to_type[attr][1]})",
        attribute_to_type.keys()))}

    def _update(self):
        self.__init__(self._ptr)

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
    else:
        return inflection.underscore(open62541_name)


# !!!! Please save your dicts here, so if the generator functions change we can generate the classes again. !!!!

# Example
# typedef struct {
#     UA_ExampleTypeA *attributeNameA;
#     UA_ExampleTypeB attributeNameB;
#     UA_ExampleTypeC attributeNameC;
# } UA_ExampleStruct;

class_from_struct = generator_struct(
    "UA_ExampleStruct",
    {
        "attributeNameA": ("UA_ExampleTypeA", True),
        "attributeNameB": ("UA_ExampleTypeB", False),
        "attributeNameC": ("UA_ExampleTypeC", False),
    }
)

# Example
# typedef enum {
#     attributeNameA = 7,
#     attributeNameB = 13,
#     attributeNameC = 35
# } UA_ExampleEnum;

class_from_enum = generator_enum(
    "UA_LogCategory",
    {
        "UA_LOGCATEGORY_NETWORK": 0,
        "UA_LOGCATEGORY_SECURECHANNEL": 1,
        "UA_LOGCATEGORY_SESSION": 2,
        "UA_LOGCATEGORY_SERVER": 3,
        "UA_LOGCATEGORY_CLIENT": 4,
        "UA_LOGCATEGORY_USERLAND": 5,
        "UA_LOGCATEGORY_SECURITYPOLICY": 6
    }
)
class_from_enum += generator_enum(
    "UA_LogLevel",
    {
        "UA_LOGLEVEL_TRACE": 0,
        "UA_LOGLEVEL_DEBUG": 1,
        "UA_LOGLEVEL_INFO": 2,
        "UA_LOGLEVEL_WARNING": 3,
        "UA_LOGLEVEL_ERROR": 4,
        "UA_LOGLEVEL_FATAL": 5
    }
)

# print(class_from_struct)
print(class_from_enum)
