from infi.instruct import SLInt64, ULInt64, ULInt32, ULInt16, ULInt8, Field, FixedSizeArray, FixedSizeString
from infi.instruct import Struct

def is_64bit():
    import sys
    return sys.maxsize > 2 ** 32

POINTER = ULInt64 if is_64bit() else ULInt32
WORD = ULInt16
DWORD = ULInt32
BYTE = ULInt8
ULONG = DWORD
UCHAR = BYTE
BOOLEAN = BYTE
ULONG64 = ULInt64
WCHAR = ULInt16

class LARGE_INTEGER(Struct):
    _fields_ = [SLInt64("QuadPart"), ] if is_64bit() else [DWORD("LowPart"), DWORD("HighPart")]

class GUID(Struct):
    _fields_ = [DWORD("Data1"), WORD("Data2"), WORD("Data3"), FixedSizeArray("Data4", 8, BYTE)]

    def __eq__(self, other):
        if not isinstance(other, GUID):
            return False
        return all(getattr(self, 'Data%d' % i) == getattr(other, 'Data%d' % i) for i in range(1, 5))
