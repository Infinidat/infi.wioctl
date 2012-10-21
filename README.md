Overview
========

An easy-to-use facade for doing IOCTLs on Windows.

Usage
-----

Here's an example on how to use this module:

```python
from infi.wioctl.constants import IOCTL_SCSI_GET_ADDRESS, ERROR_ACCESS_DENIED
from infi.wioctl import DeviceIoControl
from infi.wioctl.errors import Windows
from ctypes import c_buffer
from logging import getLogger

logger = getLogger(__name__)
out_buffer_size = 40
out_buffer = c_buffer('\x00'*out_buffer_size, out_buffer_size)
device = DeviceIoControl(r"\\.\PHYSICALDRIVE0")
try:
    _ = device.ioctl(IOCTL_SCSI_GET_ADDRESS, 0, 0, out_buffer, out_buffer_size)
except WindowsException, exception:
    logger.exception("IOCTL failed")
    raise
```

Checking out the code
=====================

This project uses buildout and infi-projector, and git to generate setup.py and __version__.py.
In order to generate these, first get infi-projector:

    easy_install infi.projector

    and then run in the project directory:

        projector devenv build
