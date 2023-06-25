# Constants for the mouse button names:
LEFT = "left"
MIDDLE = "middle"
RIGHT = "right"


def isShiftCharacter(character):
    """
    Returns True if the ``character`` is a keyboard key that would require the shift key to be held down, such as
    uppercase letters or the symbols on the keyboard's number row.
    """
    # NOTE TODO - This will be different for non-qwerty keyboards.
    return character.isupper() or character in set('~!@#$%^&*()_+{}|:"<>?')
