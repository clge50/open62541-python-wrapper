class UaXxx(UaType):
    def __init__(self, val=ffi.new("UA_Xxx*"), is_pointer=False):
        super().__init__(val=val, c_type="UA_Xxx", is_pointer=is_pointer)
        self._atrA = UaTypeA(val=val.atrA, is_pointer=False)
        self._atrA = UaTypeB(val=val.atrB, is_pointer=True)

    @UaType.value.setter
    def value(self, val):
        self._value[0] = _val(val)
        self._atrA._value[0] = _val(val.atrA)
        self._atrB._value[0] = _val(val.atrB)

    @property
    def atrA(self):
        return self._atrA

    @atrA.setter
    def atrA(self, val):
        self._atrA = val
        self._value.atrA = val.value

    @property
    def atrB(self):
        return self._atrB

    @atrB.setter
    def atrB(self, val):
        self._atrB = val
        self._value.atrB = val.value

    def __str__(self, n=0):
        return ("(UaXxx) :\n" +
                "\t"*(n+1) + "atrA" + self._atrA.__str__(n+1) +
                "\t"*(n+1) + "atrB" + self._atrB.__str__(n+1) + "\n")

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

    @UaType.value.setter
    def value(self, p_val):
        if p_val in self.val_to_string.keys():
            #Vorsicht!!!
            super().__init__(ffi.cast("UA_Zzz", p_val), self._is_pointer)
        else:
            raise OverflowError(f"{val} is not a valid member of this class")

    def __str__(self):
        return f"UaOrder: {self.val_to_string[self._p_value]} ({str(self._p_value)})"

    def str_helper(self, n: int):
        return "\t" * n + str(self)