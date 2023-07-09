# https://www.win7dll.info/user32_dll.html
from ctypes import windll as w, c_long
import ctypes

# This project
from slodon.slodonix.systems.windows.keyboard_map import full_map as key_map
from slodon.slodonix.systems.windows.utils import *
from slodon.slodonix.systems.windows.structures import POSITION, SIZE
from slodon.slodonix.systems.windows.constants import *

__all__ = [
    "Display",
    "get_os",
    "DisplayContext",
    "MOUSEEVENTF_LEFTCLICK",
    "MOUSEEVENTF_MIDDLECLICK" "MOUSEEVENTF_RIGHTCLICK",
]
ev = MOUSEEVENTF_LEFTDOWN
ev_up = MOUSEEVENTF_LEFTUP


class Screen:
    """
    Represent a screen in a display on windows, it contains information about the screen.
    """

    pass


class _Interact:
    """ """

    def __init__(self) -> None:
        pass

    # noinspection PyMethodMayBeStatic
    def key_up(self, key: str) -> None:
        """
        - https://learn.microsoft.com/en-us/windows/win32/inputdev/wm-keyup#parameters
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L295-L332

        ### Arguments
            - key (str): The key(FROM UTILS.KEY_NAMES) to release
        ### Returns
            - None
        """

        if key_map[key] is None:
            return

        needs_shift = is_shift_character(key)

        mods, vk_code = divmod(key_map[key], 0x100)

        for apply_mod, vk_mod in [
            (mods & 4, 0x12),
            (mods & 2, 0x11),
            (mods & 1 or needs_shift, 0x10),
        ]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                ctypes.windll.user32.keybd_event(vk_mod, 0, 0, 0)  #

        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)

        for apply_mod, vk_mod in [
            (mods & 1 or needs_shift, 0x10),
            (mods & 2, 0x11),
            (mods & 4, 0x12),
        ]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                ctypes.windll.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYUP, 0)  #

    # Todo: redefine this by using the latest SendInput function
    # noinspection PyMethodMayBeStatic
    def key_down(self, key: str, with_release=False) -> None:
        """
        - https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L250-L292
        Key press without release | with release
        ### Arguments
          - key (str): The key(FROM UTILS.KEY_NAMES) to press down
          - with_release (bool): Whether to release the key after press down
        ### Returns
          - None
        """

        if key_map[key] is None:  # the key is not valid
            return

        needs_shift = is_shift_character(key)

        # https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
        mods, vk_code = divmod(key_map[key], 0x100)

        for apply_mod, vk_mod in [
            (mods & 4, 0x12),
            (mods & 2, 0x11),
            (mods & 1 or needs_shift, 0x10),
        ]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                ctypes.windll.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYDOWN, 0)  #

        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYDOWN, 0)
        for apply_mod, vk_mod in [
            (mods & 1 or needs_shift, 0x10),
            (mods & 2, 0x11),
            (mods & 4, 0x12),
        ]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                ctypes.windll.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYUP, 0)  #

        if with_release:
            self.key_up(key)

    # noinspection PyMethodMayBeStatic
    def moveto(self, x: int, y: int):
        """
        x-y position of the mouse
        ### Arguments
         - key (str): Return back the mouse position
        ### Returns
         - None
        """
        w.user32.SetCursorPos(x, y)

    # noinspection PyMethodMayBeStatic
    def mouse_down(self, x, y, button, with_release=False):
        """
        - https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L375-L401

        ### Arguments
          - x (int): The x position of the mouse
          - y (int): The y position of the mouse
          - button (str): The button to press down
        ### Returns
          - None
        """
        global ev
        if button not in (LEFT, MIDDLE, RIGHT):
            raise ValueError(
                'button arg to _click() must be one of "left", "middle", or "right", not %s'
                % button
            )

        if button == LEFT:
            ev = MOUSEEVENTF_LEFTDOWN
        elif button == MIDDLE:
            ev = MOUSEEVENTF_MIDDLEDOWN
        elif button == RIGHT:
            ev = MOUSEEVENTF_RIGHTDOWN

        try:
            send_mouse_event(ev, x, y, instance=_Info())  # instance for the size
        except (PermissionError, OSError):
            # TODO: We need to figure out how to prevent these errors,
            #  see https://github.com/asweigart/pyautogui/issues/60
            pass
        if with_release:
            self.mouse_up(x, y, button)

    # noinspection PyMethodMayBeStatic
    def mouse_up(self, x, y, button):
        """
        - https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L404-L429
        Args:
            x (int): The x position of the mouse event.
            y (int): The y position of the mouse event.
            button (str): The mouse button, either 'left', 'middle', or 'right'
        Returns:
          None
        """
        global ev_up
        if button not in (LEFT, MIDDLE, RIGHT):
            raise ValueError(
                'button arg to _click() must be one of "left", "middle", or "right", not %s'
                % button
            )

        if button == LEFT:
            ev_up = MOUSEEVENTF_LEFTUP
        elif button == MIDDLE:
            ev_up = MOUSEEVENTF_MIDDLEUP
        elif button == RIGHT:
            ev_up = MOUSEEVENTF_RIGHTUP

        try:
            send_mouse_event(ev_up, x, y, instance=_Info())
        except (
            PermissionError,
            OSError,
        ):  # TODO: We need to figure out how to prevent these errors,
            # see https://github.com/asweigart/pyautogui/issues/60
            pass

    def click(self, x, y, button):
        """
        - https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L432
        Sends the mouse click event to Windows.
        Args:
            x (int): The x position of the mouse event.
            y (int): The y position of the mouse event.
            button (str): The mouse button, either 'LEFT',
            'RIGHT' or 'MIDDLE'
        Returns:
            None
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
        - https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L461
        Checks if the meanings of the left and right
        mouse buttons are swapped
        """
        return ctypes.windll.user32.GetSystemMetrics(23) != 0

    def send_mouse_event(self, ev, x, y, dwData=0):
        """
        - https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L466
        Helper function that makes the call to the mouse_event
        win32 function.
        Args:
            ev (int): The win32 code for the mouse event. Use one of
            the MOUSEEVENTF_* constants for this argument.
            x (int): The x position of the mouse event.
            y (int): The y position of the mouse event.
            dwData (int): The argument for mouse_event()'s dwData
            parameter. Only used by mouse scrolling.
        Returns:
            None.
        """
        assert (x is not None) and (y is not None), "x and y cannot be set to None"
        # TODO: ARG! For some reason, SendInput isn't working for mouse events. I'm switching to using the older mouse_event win32 function.
        # mouseStruct = MOUSEINPUT()
        # mouseStruct.dx = x
        # mouseStruct.dy = y
        # mouseStruct.mouseData = ev
        # mouseStruct.time = 0
        # mouseStruct.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0)) # according to https://stackoverflow.com/questions/13564851/generate-keyboard-events I can just set this. I don't really care about this value.
        # inputStruct = INPUT()
        # inputStruct.mi = mouseStruct
        # inputStruct.type = INPUT_MOUSE
        # ctypes.windll.user32.SendInput(1, ctypes.pointer(inputStruct), ctypes.sizeof(inputStruct))

        # TODO Note: We need to handle additional buttons, which I believe is documented here:
        # https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event

        width, height = _Info.size()
        convertedX = 65536 * x // width + 1
        convertedY = 65536 * y // height + 1
        w.user32.mouse_event(ev, c_long(convertedX), c_long(convertedY), dwData, 0)

    def scroll(self, clicks, x=None, y=None):
        """
        - https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L507
        Send the mouse vertical scroll event to Windows by calling
        the mouse_event() win32 function.
        Args:
            clicks (int): The amount of scrolling to do. A positive value
            is the mouse wheel moving forward (scrolling up), a negative value
            is backwards (down).
            x (int): The x position of the mouse event.
            y (int): The y position of the mouse event.
        Returns:
            None
        """
        startx, starty = _Info.position()
        width, height = _Info.size()

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
        - https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L544
        Send the mouse horizontal scroll event to Windows by calling
        the mouse_event() win32 function.
        Args:
            clicks (int): The amount of scrolling to do. A positive value is
            the mouse wheel moving right, a negative value is moving left.
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

    # noinspection PyMethodMayBeStatic
    def position(self) -> Position:
        """
        x-y position of the mouse
        ### Returns
          - Position object with the x and y coordinates
        """

        pos = POSITION()

        w.user32.GetCursorPos(
            ctypes.byref(pos)
        )  # fill up the pointer with the information

        return Position(pos.x, pos.y)  # access it from the pointer

    # noinspection PyMethodMayBeStatic
    def size(self) -> SIZE:
        """
        - https://learn.microsoft.com/en-us/windows/win32/api/windef/ns-windef-size(?)
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L348-L354
        """
        return SIZE(
            ctypes.windll.user32.GetSystemMetrics(0),
            ctypes.windll.user32.GetSystemMetrics(1),
        )


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
