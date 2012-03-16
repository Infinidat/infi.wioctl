
from infi.exceptools import InfiException
from infi.cwrap import WrappedFunction, IN, IN_OUT
from ctypes import c_void_p, c_ulong
from .errors import WindowsException, InvalidHandle

HANDLE = c_void_p
DWORD = c_ulong
BOOL = c_ulong

def errcheck_invalid_handle():
    from .constants import INVALID_HANDLE_VALUE
    from ctypes import GetLastError
    def errcheck(result, func, args):
        if result == INVALID_HANDLE_VALUE:
            last_error = GetLastError()
            raise InvalidHandle(last_error)
        return result
    return errcheck

def errcheck_bool():
    from ctypes import GetLastError
    from .constants import ERROR_INVALID_HANDLE
    def errcheck(result, func, args):
        if result == 0:
            last_error = GetLastError()
            if last_error == ERROR_INVALID_HANDLE:
                raise InvalidHandle(last_error)
            raise WindowsException(last_error)
        return result
    return errcheck

class CreateFileW(WrappedFunction):
    return_value = HANDLE

    @classmethod
    def get_errcheck(cls):
        return errcheck_invalid_handle()

    @classmethod
    def get_library_name(cls):
        return 'kernel32'

    @classmethod
    def get_parameters(cls):
        return ((c_void_p, IN, "FileName"),
                (DWORD, IN, "DesiredAccess"),
                (DWORD, IN, "SharedMode"),
                (c_void_p, IN, "SecurityAttributes"),
                (DWORD, IN, "CreationDisposition"),
                (DWORD, IN, "FlagsAndAttributes"),
                (HANDLE, IN_OUT, "TemplateFile"))

class DeviceIoControl(WrappedFunction):
    return_value = BOOL

    @classmethod
    def get_errcheck(cls):
        return errcheck_bool()

    @classmethod
    def get_library_name(cls):
        return 'kernel32'

    @classmethod
    def get_parameters(cls):
        return ((HANDLE, IN, "Device"),
                (DWORD, IN, "ControlCode"),
                (c_void_p, IN, "InputBuffer"),
                (DWORD, IN, "InputBufferSize"),
                (c_void_p, IN_OUT, "OutBuffer"),
                (DWORD, IN, "OutBufferSize"),
                (c_void_p, IN_OUT, "BytesReturned"),
                (c_void_p, IN_OUT, "Overldappped"))

class CloseHandle(WrappedFunction):
    return_value = BOOL

    @classmethod
    def get_errcheck(cls):
        return errcheck_bool()

    @classmethod
    def get_library_name(cls):
        return 'kernel32'

    @classmethod
    def get_parameters(cls):
        return ((HANDLE, IN, "Device"),)
