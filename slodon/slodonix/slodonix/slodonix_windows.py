# https://www.win7dll.info/user32_dll.html
import ctypes
from ctypes import windll as w, c_long
from ctypes import wintypes, byref
from typing import Tuple

# This project
from slodon.slodonix.systems.windows.keyboard_map import full_map as key_map
from slodon.slodonix.systems.windows.utils import *
from slodon.slodonix.systems.windows.structures import *
from slodon.slodonix.slodonix import *


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
        if key_map[key] is None:  # the key is not valid
            return

        needsShift = isShiftCharacter(key)

        mods, vkCode = divmod(key_map[key], 0x100)
        for apply_mod, vk_mod in [
            (mods & 4, 0x12),
            (mods & 2, 0x11),
            (mods & 1 or needsShift, 0x10),
        ]:
            if apply_mod:
                w.user32.keybd_event(vk_mod, 0, 0, 0)
        w.user32.keybd_event(vkCode, 0, KEYEVENTF_KEYUP, 0)
        for apply_mod, vk_mod in [
            (mods & 1 or needsShift, 0x10),
            (mods & 2, 0x11),
            (mods & 4, 0x12),
        ]:
            if apply_mod:
                w.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYUP, 0)

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
        for apply_mod, vk_mod in [
            (mods & 4, 0x12),
            (mods & 2, 0x11),
            (mods & 1 or needsShift, 0x10),
        ]:
            if apply_mod:
                w.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYDOWN, 0)
        w.user32.keybd_event(vkCode, 0, KEYEVENTF_KEYDOWN, 0)
        for apply_mod, vk_mod in [
            (mods & 1 or needsShift, 0x10),
            (mods & 2, 0x11),
            (mods & 4, 0x12),
        ]:
            if apply_mod:
                w.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYUP, 0)

    def position(self) -> tuple[c_long, c_long]:
        """
        x-y position of the mouse
        ### Arguments
          - key (str): Return back the mouse position
        ### Returns
          - Position object
        """
        cursor = ctypes.wintypes.POINT()
        w.user32.GetCursorPos(byref(cursor))
        return cursor.x, cursor.y

    def screen(self):
        """ """
        pass

    def size(self) -> Tuple:
        """
        Returns the width and height of the screen as a two integer tuple.
        """
        return w.user32.GetSystemMetrics(0), w.user32.GetSystemMetrics(1)

    def moveto(self, x, y) -> None:
        """
        x-y position of the mouse
        ### Arguments
         - x (int): The x position of the mouse event.
         - y (int): The y position of the mouse event.
        ### Returns
         - None
        """
        w.user32.SetCursorPos(x, y)

    def mouse_down(self, x, y, button):
        """
        Send the mouse_down event to Windows
        ### Arguments
         - x (int): The x position of the mouse event.
         - y (int): The y position of the mouse event.
         - button (str): The mouse button, either 'LEFT',
           'RIGHT' or 'MIDDLE'.
        ### Returns
         - None
        """
        if button not in (LEFT, MIDDLE, RIGHT):
            raise ValueError(
                'button arg to _click() must be one of "left", "middle", or "right", not %s'
                % button
            )

        if button == LEFT:
            EV = MOUSEEVENTF_LEFTDOWN
        elif button == MIDDLE:
            EV = MOUSEEVENTF_MIDDLEDOWN
        elif button == RIGHT:
            EV = MOUSEEVENTF_RIGHTDOWN

        try:
            self.send_mouse_event(EV, x, y)
        except (PermissionError, OSError):
            pass

    def mouse_up(self, x, y, button):
        """
        Send the mouse up event to Windows
        ### Arguments
         - x (int): The x position of the mouse event.
         - y (int): The y position of the mouse event.
         - button (str): The mouse button, either 'LEFT',
           'RIGHT' or 'MIDDLE'.
        ### Returns
         - None
        """
        if button not in (LEFT, MIDDLE, RIGHT):
            raise ValueError(
                'button arg to _click() must be one of "left", "middle", or "right", not %s'
                % button
            )

        if button == LEFT:
            EV = MOUSEEVENTF_LEFTUP
        elif button == MIDDLE:
            EV = MOUSEEVENTF_MIDDLEUP
        elif button == RIGHT:
            EV = MOUSEEVENTF_RIGHTUP

        try:
            self.send_mouse_event(EV, x, y)
        except (PermissionError, OSError):
            pass

    def click(self, x, y, button):
        """
        Send the mouse click event to Windows
        ### Arguments
         - x (int): The x position of the mouse event.
         - y (int): The y position of the mouse event.
         - button (str): The mouse button, either 'LEFT',
           'RIGHT' or 'MIDDLE'.
        ### Returns
         - None
        """
        if button not in (LEFT, MIDDLE, RIGHT):
            raise ValueError(
                'button arg to _click() must be one of "left", "middle", or "right", not %s'
                % button
            )

        if button == LEFT:
            EV = MOUSEEVENTF_LEFTCLICK
        elif button == MIDDLE:
            EV = MOUSEEVENTF_MIDDLECLICK
        elif button == RIGHT:
            EV = MOUSEEVENTF_RIGHTCLICK

        try:
            self.send_mouse_event(EV, x, y)
        except (PermissionError, OSError):
            pass

    def mouse_is_swapped(self):
        """
        Checks if the meanings of the left and
        right mouse buttons are swapped.
        """
        return w.user32.GetSystemMetrics(23) != 0

    def send_mouse_event(self, ev, x, y, dwData=0):
        """
        Helper function that makes the call to mouse_event() function
        in win32
        Args:
            ev (int): The win32 code for the mouse event.
            x (int): The x position of the mouse event.
            y (int): The y position of the mouse event.
            dwData (int): The argument for mouse_event()'s dwData
                parameter. Only used by mouse scrolling.

        Returns:
            None
        """
        assert (x is not None) and (y is not None), "x and y cannot be set to None"

        width, height = self.size()
        convertedX = 65536 * x // width + 1
        convertedY = 65536 * y // height + 1
        w.user32.mouse_event(ev, c_long(convertedX), c_long(convertedY), dwData, 0)

    def scroll(self, clicks, x=None, y=None):
        """
        Send the mouse vertical scroll event to Windows
        Args:
            clicks (int): The amount of scrolling to do. A positive
                value is the mouse wheel scrolling up, a negative value
                is scrolling down
            x (int): The x position of the mouse event.
            y (int): The y position of the mouse event.

        Returns:
             None
        """
        startx, starty = self.position()
        width, height = self.size()

        if x is None:
            x = startx
        else:
            if x < 0:
                x = 0
            elif x >= width:
                x = width - 1
        if y is None:
            y = starty
        else:
            if y < 0:
                y = 0
            elif y >= height:
                y = height - 1

        try:
            self.send_mouse_event(MOUSEEVENTF_WHEEL, x, y, dwData=clicks)
        except (PermissionError, OSError):
            pass

    def hscroll(self, clicks, x, y):
        """
        Send the mouse horizontal scroll event to Windows
        Args:
            clicks (int): The amount of scrolling to do. A positive
                value is the mouse wheel moving right, a negative value
                is moving left.
            x (int): The x position of the mouse event.
            y (int): The y position of the mouse event.

        Returns:
             None
        """
        return self.scroll(clicks, x, y)


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
