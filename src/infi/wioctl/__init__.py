
from contextlib import contextmanager
from . import constants, structures, api
import ctypes

@contextmanager
def open_handle(device_path):
    from constants import FILE_SHARE_READ, FILE_SHARE_WRITE, OPEN_EXISTING
    handle = None
    try:
        handle = api.CreateFileW(ctypes.create_unicode_buffer(device_path),
                             0, FILE_SHARE_READ | FILE_SHARE_WRITE,
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
    def __init__(self, device_path):
        super(DeviceIoControl, self).__init__()
        self.device_path = device_path

    @contextmanager
    def open_handle(self):
        with open_handle(self.device_path) as handle:
            yield handle

    def ioctl(self, control_code, in_buffer, in_buffer_size, out_buffer, out_buffer_size):
        with self.open_handle(self.device_path) as handle:
            return ioctl(control_code, in_buffer, in_buffer_size, out_buffer, out_buffer_size)

