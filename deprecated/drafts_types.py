class UaBoolean:
    def __init__(self, val: bool):
        self._value = ffi.cast("UA_Boolean", val)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val.isInstance(bool):
            self._value = ffi.cast("UA_Boolean", val)
        else:
            # TODO: improve type handling?
            self._value = val


class UaType:
    def __init__(self, val):
        self._value = val
        self._dict = UaType.to_dict(val)

    @property
    def value(self):
        return self._value

    # return list of attrinbutes

    # instead of setter, set specific attributes

    @dict.setter
    def dict(self, dictionary):
        try:
            ...
        except LookupError:
            raise AttributeError("the ") from LookupError

    # setter which keeps value and dict consistent

    # new functions (provided by open62541 or via ffi) as static functions invoking the constructor?

    @staticmethod
    def to_dict(val):
        # convert open62541-struct to a dict where the key is the name of the attribute in open62541
        # and the value is
        #   if an attribute is not a base type: A recursively constructed UaType
        #   if an attribute is a base type several options:
        #       1. either provide particular classes for those
        #       2. or use a class like UaBaseType (or UaType) where dict is a primitive python variable
        #       3. or dict has as value not a UaType but a primitive python type

        # where xxx is another UaType
        dictionary = {"attribute_name": "xxx"}
        return dictionary



# Every type is subtype of uaType, autogenereate other type classes as subclass of this
class UaType:
    def __init__(self, val):
        self._value = val

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class UaXxxxx(UaType):
    def __init__(self, val):
        super().__init__(val)
        self._attribute1 = <type of val.attribute1, UA_ to Ua>(val.attribute1)
        self._attributeN = <type of val.attributeN, UA_ to Ua>(val.attribute1)

    def __init__(self):
        super().__init__(ffi.new(<type ofval.attribute1>*))
        self._attribute1 = None
        self._attributeN = None

    @property
    def attribute1(self):
        return self._attribute1

    @property
    def attributeN(self):
        return self._attributeN

    @attribute1.setter
    def attribute1(self, val):
        self._attribute1 = val
        self._value.attribute1 = val.value

    @attributeN.setter
    def attributeN(self, val):
        self._attributeN = val
        self._value.attributeN = val.value

    def __str__(self):
        "UaXxxxx:"+
        self._attribute1.str_helper(1) + ...

    def str_helper(self, n: int):
        "\t"*n + "UaXxxxx:\n" + self._attribute1.str_helper(n+1) + ...


# from enum
class UaXxxxx(UaType):
    attr1 = x1
    ...
    attrN = xN

    val_to_string = dict([
        (x1, "attr1"),
        ...,
        (xN, "attrN")])

    def __init__(self, val=None):
    if val is None:
        super().__init__(ffi.new("UA_Xxxxx*"))
        self._p_value = None
    else:
        super().__init__(val)
        self._p_value = val[0]

    @property
    def p_value(self):
        return self._p_value

    @p_value.setter
    def p_value(self, val):
        if min(x1...xN) <= val <= max(x1...xN)
            self._p_value = val
            self._value = ffi.new("UA_Xxxxx*", val)
        else:
            raise OverflowError(f"{val} is not in range min(x1...xN) .. max(x1...xN)")


    def __str__(self):
        return f"UaXxxxx: {val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)