
from contextlib import contextmanager
from . import constants, structures, api
import ctypes

@contextmanager
def open_handle(device_path, read_only=True):
    from constants import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
    from constants import FILE_SHARE_READ, FILE_SHARE_WRITE, OPEN_EXISTING
    handle = None
    try:
        handle = api.CreateFileW(ctypes.create_unicode_buffer(device_path),
                             GENERIC_READ if read_only else GENERIC_READ | GENERIC_WRITE,
                             FILE_SHARE_READ if read_only else FILE_SHARE_READ | FILE_SHARE_WRITE,
                             0, OPEN_EXISTING, 0, 0)
        yield handle
    finally:
        if handle is not None:
            api.CloseHandle(handle)

def ioctl(handle, control_code, in_buffer, in_buffer_size, out_buffer, out_buffer_size):
    bytes_returned = ctypes.c_ulong()
    api.DeviceIoControl(handle, control_code, in_buffer, in_buffer_size, out_buffer, out_buffer_size,
                        ctypes.byref(bytes_returned), 0)
    return bytes_returned.value

class DeviceIoControl(object):
    def __init__(self, device_path, read_only=True):
        super(DeviceIoControl, self).__init__()
        self.device_path = device_path
        self._read_only

    @contextmanager
    def open_handle(self):
        with open_handle(self.device_path, self._read_only) as handle:
            yield handle

    def ioctl(self, control_code, in_buffer, in_buffer_size, out_buffer, out_buffer_size):
        with self.open_handle() as handle:
            return ioctl(handle, control_code, in_buffer, in_buffer_size, out_buffer, out_buffer_size)

