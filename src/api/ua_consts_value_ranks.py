from ua_types_primitive import UaInt32

class UaValueRanks:
    SCALAR_OR_ONE_DIMENSION = UaInt32(-3)
    ANY = UaInt32(-2)
    SCALAR = UaInt32(-1)
    ONE_OR_MORE_DIMENSIONS = UaInt32(0)
    ONE_DIMENSION = UaInt32(1)
    TWO_DIMENSIONS = UaInt32(2)
    THREE_DIMENSIONS = UaInt32(3)
