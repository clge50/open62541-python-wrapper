def _ptr(val, c_type=""):
    if c_type == "":
        c_type = str(val).split("'")[1]

    try:
        return ffi.cast(c_type + "*", ffi.addressof(val))
    except TypeError:
        return val


def _val(val):
    if _is_ptr(val):
        return val[0]
    else:
        return val


def _is_ptr(val):
    try:
        ffi.addressof(val)
    except TypeError:
        return False

    return True


class UaType:
    # _value should always be a pointer, so if it has to be dereferenced call .value (for getter)
    def __init__(self, val, c_type="", is_pointer=False):
        val = ptr(val, c_type)
        self._value = val
        self._is_pointer = is_pointer

    @property
    def value(self):
        return self._value[0]

    def __str__(self, n=0):
        return str(self._value[0])
