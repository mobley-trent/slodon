import ctypes
from ctypes import wintypes

# Basic structures
# https://coderslegacy.com/structs-with-python-ctypes/

# Documented here: http://msdn.microsoft.com/en-us/library/windows/desktop/ms646304(v=vs.85).aspx
KEYEVENTF_KEYDOWN = 0x0000  # Technically this constant doesn't exist in the MS documentation. It's the lack of KEYEVENTF_KEYUP that means pressing the key down.
KEYEVENTF_KEYUP = 0x0002


# Event codes to be passed to the mouse_event() win32 function.
# Documented here: http://msdn.microsoft.com/en-us/library/windows/desktop/ms646273(v=vs.85).aspx
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_LEFTCLICK = MOUSEEVENTF_LEFTDOWN + MOUSEEVENTF_LEFTUP
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_RIGHTCLICK = MOUSEEVENTF_RIGHTDOWN + MOUSEEVENTF_RIGHTUP
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_MIDDLECLICK = MOUSEEVENTF_MIDDLEDOWN + MOUSEEVENTF_MIDDLEUP

MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_WHEEL = 0x0800


class MOUSEINPUT(ctypes.Structure):
    """
    https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
    """

    _fields_ = [
        ("dx", ctypes.wintypes.LONG),
        ("dy", ctypes.wintypes.LONG),
        ("mouseData", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]


class KEYBDINPUT(ctypes.Structure):
    """
    https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
    """

    _fields_ = [
        ("wVk", ctypes.wintypes.WORD),
        ("wScan", ctypes.wintypes.WORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    """
    https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-hardwareinput
    """

    _fields_ = [
        ("uMsg", ctypes.wintypes.DWORD),
        ("wParamL", ctypes.wintypes.WORD),
        ("wParamH", ctypes.wintypes.DWORD),
    ]


class INPUT(ctypes.Structure):
    """
    https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
    """

    class _I(ctypes.Union):
        _fields_ = [
            ("mi", MOUSEINPUT),
            ("ki", KEYBDINPUT),
            ("hi", HARDWAREINPUT),
        ]

    _anonymous_ = ("i",)
    _fields_ = [
        ("type", ctypes.wintypes.DWORD),
        ("i", _I),
    ]
