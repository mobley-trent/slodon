# https://www.win7dll.info/user32_dll.html
from ctypes import windll as w

# This project
from slodon.slodonix.systems.windows.keyboard_map import full_map as key_map
from slodon.slodonix.systems.windows.utils import *
from slodon.slodonix.systems.windows.structures import *
from . import *


__all__ = ["Display", "get_os", "DisplayContext"]

INPUT_KEYBOARD = 1

class Screen:
    """
    Represent a screen in a display on windows, it contains information about the screen.
    """

    pass


class _Interact:
    """ """

    def __init__(self) -> None:
        """ """

    def key_up(self, key: str) -> None:
        """
        key release
        ### Arguments
            - key (str): The key(FROM UTILS.KEY_NAMES) to release
        ### Returns
            - None
        """

    # noinspection PyMethodMayBeStatic
    def key_down(self, key: str) -> None:
        """
        https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-keybd_event
        Key press without release
        ### Arguments
          - key (str): The key(FROM UTILS.KEY_NAMES) to press down
        ### Returns
          - None
        """
        if key_map[key] is None:  # the key is not valid
            return

        needsShift = isShiftCharacter(key)

        mods, vkCode = divmod(key_map[key], 0x100)
        for apply_mod, vk_mod in [(mods & 4, 0x12), (mods & 2, 0x11),
                                  (mods & 1 or needsShift, 0x10)]:
            if apply_mod:
                w.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYDOWN, 0)
        w.user32.keybd_event(vkCode, 0, KEYEVENTF_KEYDOWN, 0)
        for apply_mod, vk_mod in [(mods & 1 or needsShift, 0x10), (mods & 2, 0x11),
                                  (mods & 4, 0x12)]:
            if apply_mod:
                w.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYUP, 0)

    def position(self) -> Position:
        """
        x-y position of the mouse
        ### Arguments
          - key (str): Return back the mouse position
        ### Returns
          - Position object
        """

    def screen(self):
        """ """
        pass

    def moveto(self):
        """
        x-y position of the mouse
        ### Arguments
         - key (str): Return back the mouse position
        ### Returns
         - None
        """

    def mouse_down(self):
        """ """
        pass

    def mouse_up(self):
        """ """
        pass

    def click(self):
        """ """
        pass

    def mouse_is_swapped(self):
        """ """
        pass

    def send_mouse_event(self):
        """ """
        pass

    def scrool(self):
        """ """
        pass

    def hscrool(self):
        """ """
        pass


class _Info:
    """
    Returns back information about the display
    """

    def get_top_window(self):
        pass


class Display:
    """
    Represents a basic display, which is the starting point.
    Acts as a context manager.
    """

    def __init__(self):
        self.interact = _Interact()
        self.info = _Info()


class DisplayContext(Display):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def get_os() -> str:
    """
    Return back the currently used operating system.
    """
    return "Windows"
