# +++++++++++++++++ Struct ++++++++++++++++++++
class UaXxx(UaType):
    def __init__(self, val=ffi.new("UA_Xxx*"), is_pointer=False):
        super().__init__(val=val, is_pointer=is_pointer)
        self._atr_a = UaTypeA(val=val.atrA, is_pointer=False)
        self._atr_b = UaTypeB(val=val.atrB, is_pointer=True)

    @UaType._value.setter
    def value(self, val):
        self._value = _val(val)
        self._atr_a._value = _val(val.atrA)
        self._atr_b._value = _val(val.atrB)

    @property
    def atrA(self):
        return self._atrA

    @atrA.setter
    def atrA(self, val):
        self._atr_a = val
        self._value.atr_a = val._value

    @property
    def atrB(self):
        return self._atrB

    @atrB.setter
    def atrB(self, val):
        self._atrB = val
        self._value.atrB = val._value

    def __str__(self, n=0):
        return ("(UaXxx) :\n" +
                "\t"*(n+1) + "atrA" + self._atrA.__str__(n+1) +
                "\t"*(n+1) + "atrB" + self._atrB.__str__(n+1) + "\n")

# +++++++++++++++++ Enum ++++++++++++++++++++
class UaZzz(UaType):
    ATR_A = -1
    ATR_B = 0

    val_to_string = dict([
        (-1, "ATR_A"),
        (0, "ATR_B")])

    def __init__(self, p_val=None, is_pointer=False):
        if p_val is None:
            super().__init__(ffi.new("UA_Zzz*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Zzz", p_val), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        if _val(val) in self.val_to_string.keys():
            self._value = _val(val)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"(UaZzz): {self.val_to_string[self._value]} ({str(self._value)})\n"


# +++++++++++++++++ Primitive ++++++++++++++++++++
class UaBbb(UaType):
    def __init__(self, val=None, is_pointer=False):
        if val is None:
            super().__init__(ffi.new("UA_Bbb*"), is_pointer)
        else:
            super().__init__(ffi.cast("UA_Bbb", _val(val)), is_pointer)

    @UaType._value.setter
    def _value(self, val):
        self._value = ffi.cast("UA_Bbb", _val(val))

    def __str__(self):
        return "(UA_Bbb): " + str(self._val) + "\n"
