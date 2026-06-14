from typing import Final
from logging import info, warning, error, critical

info(f"Module {__name__} loaded")
from ..dialog.enums import Icon as i, Button as b

# Color constants
WHITE: Final = "#ffffff"
BLACK: Final = "#000000"
GRAY: Final = "#808080"
RED: Final = "#ff0000"
ORANGE: Final = "#ffa500"
YELLOW: Final = "#ffff00"
GREEN: Final = "#00ff00"
CYAN: Final = "#00ffff"
BLUE: Final = "#0000ff"
PURPLE: Final = "#800080"
PINK: Final = "#ffc0cb"
LIGHT_GRAY: Final = "#d3d3d3"
LIGHT_RED: Final = "#ff7f7f"
LIGHT_ORANGE: Final = "#ffb347"
LIGHT_YELLOW: Final = "#ffffe0"
LIGHT_GREEN: Final = "#90ee90"
LIGHT_CYAN: Final = "#e0ffff"
LIGHT_BLUE: Final = "#add8e6"
LIGHT_PURPLE: Final = "#dda0dd"
LIGHT_PINK: Final = "#ffb6c1"
DARK_GRAY: Final = "#494949"
DARK_RED: Final = "#8b0000"
DARK_ORANGE: Final = "#ff8c00"
DARK_YELLOW: Final = "#9b870c"
DARK_GREEN: Final = "#006400"
DARK_CYAN: Final = "#008b8b"
DARK_BLUE: Final = "#00008b"
DARK_PURPLE: Final = "#4b0082"
DARK_PINK: Final = "#ff1493"

# Message box style constants

ASSERTION: Final = (
    "Assertion Failed",
    "Assertion failed",
    i.Critical,
    b.Ignore | b.Abort | b.Retry
)

ERROR: Final = (
    "Error",
    "Error!",
    i.Critical,
    b.Ok
)

WARNING: Final = (
    "Warning",
    "Warning!",
    i.Warning,
    b.Ok
)

SAVE_FILE: Final = (
    "Unsaved modifications",
    "Do you want to save changes to the file?",
    i.Question,
    b.Yes | b.No | b.Cancel
)

CANT_OPEN_FILE: Final = (
    "Cannot Open File",
    "The file could not be opened or does not exist.",
    i.Critical,
    b.Ok
)

FILE_NOT_FOUND: Final = (
    "File Not Found",
    "The selected file path is invalid.",
    i.Critical,
    b.Ok
)

OVERWRITE_FILE: Final = (
    "Overwrite File",
    "This file already exists. Overwrite?",
    i.Question,
    b.Yes | b.No
)

INFO: Final = (
    "Information",
    "Operation completed successfully.",
    i.Information,
    b.Ok
)

CONFIRM_EXIT: Final = (
    "Exit Confirmation",
    "Are you sure you want to exit?",
    i.Question,
    b.Yes | b.No
)

PERMISSION_DENIED: Final = (
    "Permission Denied",
    "You don't have permission to access this file.",
    i.Critical,
    b.Ok
)
