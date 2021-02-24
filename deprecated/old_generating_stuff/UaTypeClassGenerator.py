# The use of this class generator is base on two assumptions:
#   1. syntax: the struct name starts with UA_
#   2. semantics: there were already python classes generated for all nested types of the struct
#       -> especially: there are classes for the base types (as stop for the recursion)

def ua_struct_class_generator(structname: str, attribute_to_type: dict):
    class_str = f""" 
    
    
    # The class {to_python_class_name(structname)} represents the open62541 type {structname}.
    # It's attribute val holds a ffi POINTER(!) on a {structname}.
    # The other attributes are the Python equivalents to the attributes of the c struct.
    
    """
    class_str += """class """ + to_python_class_name(structname) + f"""(UaType):
        def __init__(self, val=ffi.new({structname}*)):
            super().__init__(val)\n"""

    for attribute, typename in attribute_to_type.items():
        class_str += f"\t\tself._{attribute} = {to_python_class_name(typename)}(val.{attribute})\n"
    class_str += "\t\n"

    for attribute, typename in attribute_to_type.items():
        class_str += f"""
            @property
            def {attribute}(self):
                return self._{attribute}
            
            @{attribute}.setter
            def {attribute}(self, val):
                self._{attribute} = val
                self._value.{attribute} = val.value
            """

    class_str += (f"""
        def __str__(self):
            return ("{to_python_class_name(structname)}:\\n" + """ +
                  " +".join(map(lambda s: f"\n\t\t\tself._{s}.str_helper(1)", attribute_to_type.values())) +
                  ")\n\t\n")

    class_str += (f"""
            def str_helper(self, n: int):
                return ("\\t"*n + "{to_python_class_name(structname)}:\\n" + """ +
                  " +".join(map(lambda s: f"\n\t\t\tself._{s}.str_helper(n+1)", attribute_to_type.values())) +
                  ")\n\t\n")


def ua_enum_class_generator(enumname: str, ident_to_val: dict):
    tab = "\t"
    newline = "\n"
    class_str = f""" 


    # The class {to_python_class_name(enumname)} represents the open62541 enum {enumname}.
    # It's attribute val holds a ffi POINTER(!) on a variable with type {enumname}.
    # So a member of this class represents a variable with type {enumname}
    # The static attributes are the Python equivalents to the members of the enum.

    """
    class_str += f"""class {to_python_class_name(enumname)}(UaType):
    {newline.join(map(lambda ident: f"{tab}{ident} = {ident_to_val[ident]}", ident_to_val.keys()))}
        
        val_to_string = dict([
    {f",{newline}".join(map(lambda ident: f"{tab}{tab}({ident_to_val[ident]}, {ident})", ident_to_val.keys()))}])
       
        def __init__(self, val=None):
            if val is None:
                super().__init__(ffi.new("{enumname}*"))
                self._p_value = None
            else:
                super().__init__(val)
                self._p_value = val[0]

        @property
        def p_value(self):
            return self._p_value
    
        @p_value.setter
        def p_value(self, val):
            if val in val_to_string.keys()
                self._p_value = val
                self._value = ffi.new("{enumname}*", val)
            else:
                raise OverflowError(f"{{val}} is not a valid member of this class")
    
        def __str__(self):
            return f"{to_python_class_name(enumname)}: {{val_to_string[self._p_value]}} ({{str(self._p_value)}})"
    
        def str_helper(self, n: int):
            return "\\t" * n + str(self)"""

    return class_str


def to_python_class_name(open62541_name: str):
    if open62541_name[0:3] == "UA_":
        return open62541_name.replace("UA_", "Ua")
    else:
        raise Exception("invalid class identifier passed.")


print(ua_enum_class_generator("UA_xxx", {"a": 1, "b": 2, "c": 3}))
