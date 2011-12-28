from infi.instruct import ULInt64, ULInt32, ULInt16, ULInt8, Field, FixedSizeArray, FixedSizeString
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
PARTITION_STYLE = ULInt32

class LARGE_INTEGER(Struct):
    _fields_ = [ULInt64("QuadPart"), ] if is_64bit() else [DWORD("LowPart"), DWORD("HighPart")]

class GUID(Struct):
    _fields_ = [DWORD("Data1"), WORD("Data2"), WORD("Data3"), FixedSizeArray("Data4", 8, BYTE)]

