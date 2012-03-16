
from infi.exceptools import chain, InfiException
from infi.pyutils.decorators import wraps

class IoctlException(InfiException):
    pass

class WindowsException(IoctlException):
    def __init__(self, errno):
        from ctypes import FormatError
        self.winerror = errno
        self.strerror = FormatError(errno)

    def __repr__(self):
        return "%s, %s" % (self.winerror, self.strerror)

    def __str__(self):
        return self.__repr__()

class InvalidHandle(WindowsException):
    pass

