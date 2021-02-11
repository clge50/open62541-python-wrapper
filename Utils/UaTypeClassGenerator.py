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


def to_python_class_name(open62541_name: str):
    if open62541_name[0:3] == "UA_":
        open62541_name.replace("UA_", "Ua")
        return open62541_name
    else:
        raise Exception("invalid class identifier passed.")
