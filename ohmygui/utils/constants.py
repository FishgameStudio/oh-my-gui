from typing import Final as _Final
from logging import info as _info

_info(f"Module {__name__} loaded")
from ..dialog.enums import Icons as _i, Buttons as _b

# Color constants
WHITE: _Final = "#ffffff"
BLACK: _Final = "#000000"
GRAY: _Final = "#808080"
RED: _Final = "#ff0000"
ORANGE: _Final = "#ffa500"
YELLOW: _Final = "#ffff00"
GREEN: _Final = "#00ff00"
CYAN: _Final = "#00ffff"
BLUE: _Final = "#0000ff"
PURPLE: _Final = "#800080"
PINK: _Final = "#ffc0cb"
LIGHT_GRAY: _Final = "#d3d3d3"
LIGHT_RED: _Final = "#ff7f7f"
LIGHT_ORANGE: _Final = "#ffb347"
LIGHT_YELLOW: _Final = "#ffffe0"
LIGHT_GREEN: _Final = "#90ee90"
LIGHT_CYAN: _Final = "#e0ffff"
LIGHT_BLUE: _Final = "#add8e6"
LIGHT_PURPLE: _Final = "#dda0dd"
LIGHT_PINK: _Final = "#ffb6c1"
DARK_GRAY: _Final = "#494949"
DARK_RED: _Final = "#8b0000"
DARK_ORANGE: _Final = "#ff8c00"
DARK_YELLOW: _Final = "#9b870c"
DARK_GREEN: _Final = "#006400"
DARK_CYAN: _Final = "#008b8b"
DARK_BLUE: _Final = "#00008b"
DARK_PURPLE: _Final = "#4b0082"
DARK_PINK: _Final = "#ff1493"

# Message box style constants

ASSERTION: _Final = (
    "Assertion Failed",
    "Assertion failed",
    _i.Critical,
    _b.Ignore | _b.Abort | _b.Retry
)

ERROR: _Final = (
    "Error",
    "Error!",
    _i.Critical,
    _b.Ok
)

WARNING: _Final = (
    "Warning",
    "Warning!",
    _i.Warning,
    _b.Ok
)

SAVE_FILE: _Final = (
    "Unsaved modifications",
    "Do you want to save changes to the file?",
    _i.Question,
    _b.Yes | _b.No | _b.Cancel
)

CANT_OPEN_FILE: _Final = (
    "Cannot Open File",
    "The file could not be opened or does not exist.",
    _i.Critical,
    _b.Ok
)

FILE_NOT_FOUND: _Final = (
    "File Not Found",
    "The selected file path is invalid.",
    _i.Critical,
    _b.Ok
)

OVERWRITE_FILE: _Final = (
    "Overwrite File",
    "This file already exists. Overwrite?",
    _i.Question,
    _b.Yes | _b.No
)

INFO: _Final = (
    "Information",
    "Operation completed successfully.",
    _i.Information,
    _b.Ok
)

CONFIRM_EXIT: _Final = (
    "Exit Confirmation",
    "Are you sure you want to exit?",
    _i.Question,
    _b.Yes | _b.No
)

PERMISSION_DENIED: _Final = (
    "Permission Denied",
    "You don't have permission to access this file.",
    _i.Critical,
    _b.Ok
)
