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
        super().__init__(val=val, is_pointer=is_pointer)
        
        if not self._null:
{new_line.join(map(
        lambda attr:
        tab * 3 + f"self._{to_python_ident(attr)} = {to_python_class_name(attribute_to_type[attr][0])}(val=val.{attr}, is_pointer={attribute_to_type[attr][1]})",
        attribute_to_type.keys()))}

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
        tab + f"def {to_python_ident(attr)}(self, val):" + new_line +
        tab * 2 + f"self._{to_python_ident(attr)} = val" + new_line +
        (tab * 2 + f"self._value.{attr} = val._ptr"
         if attribute_to_type[attr][1] else
         tab * 2 + f"self._value.{attr} = val._val"),
        attribute_to_type.keys()))}

    def __str__(self, n=0):
        if self._null:
            return "({to_python_class_name(struct_name)}) : NULL\\n"
        
        return ("({to_python_class_name(struct_name)}) :\\n" +
{new_line.join(map(
        lambda attr:
        tab * 4 + f"{quote}{backslash}t{quote}*(n+1) + {quote}{to_python_ident(attr)}{quote} + self._{to_python_ident(attr)}.__str__(n+1) +",
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

    def _set_value(self, val):
        if _val(val) in self.val_to_string.keys():
            if self._is_pointer:
                self._value = _ptr(val, "{enum_name}")
            else:
                self._value[0] = _val(val)
        else:
            raise OverflowError(f"{l_brace}val{r_brace} is not a valid member of this class")

    def __str__(self, n=0):
        return f"({to_python_class_name(enum_name)
    }): {l_brace}self.val_to_string[self._val]{r_brace} ({l_brace}str(self._val){r_brace})\\n"


"""
    return class_str


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
    "UA_ExampleEnum",
    {
        "attributeNameA": 7,
        "attributeNameB": 13,
        "attributeNameC": 35
    }
)

print(class_from_struct)
print(class_from_enum)






