# MIT License

# Copyright (c) 2026 Fishgame Studio

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sys import path as _sys_path, stdout as _stdout
from os.path import dirname as _dirname

_current_folder: str = _dirname(__file__)
if _current_folder not in _sys_path:
    _sys_path.insert(0, _current_folder)

import logging as _logging
class _Color:
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"
class _ColorFormatter(_logging.Formatter):
    def format(self, record: LogRecord) -> str:
        if record.levelno == _logging.DEBUG:
            c = _Color.BLUE
        elif record.levelno == _logging.INFO:
            c = _Color.GREEN
        elif record.levelno == _logging.WARNING:
            c = _Color.YELLOW
        else:
            c = _Color.RED
        s = super().format(record)
        return f"{c}{s}{_Color.RESET}"
_logging.basicConfig(
    level=_logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] in [%(module)s, %(funcName)s] : %(message)s",
    datefmt="%Y-%m-%d-%H:%M:%S",
    handlers=[_logging.StreamHandler(_stdout)]
)
_root_handler: Handler = _logging.getLogger().handlers[0]
from typing import cast as _cast
_root_handler.setFormatter(_ColorFormatter(_cast(_logging.Formatter, _root_handler.formatter)._fmt))


__author__  = "Fishgame Studio"
__version__ = "1.2.6"

from .core import *
from .widget import *
from .dialog import *
from .utils import *
from .layout import *
from .terminal import *
from .oml import *

__all__ = [
     "BaseWidget",
    "Text",
    "Button",
    "InputEntry",
    "PasswordEntry",
    "Event",
    "RadioButton",
    "ComboBox",
    "ListWidget",
    "Table",
    "Slider",
    "Progress",
    "TextEdit",
    "Canvas",
    "DoubleEntry",
    "IntegerEntry",
    "Video",
    "Picture",
    "Tree",
    "Dial",
    "SplashScreen",
    "Page",
    "Interface",
    "WHITE",
    "BLACK",
    "GRAY",
    "RED",
    "ORANGE",
    "YELLOW",
    "GREEN",
    "CYAN",
    "BLUE",
    "PURPLE",
    "PINK",
    "LIGHT_GRAY",
    "LIGHT_RED",
    "LIGHT_ORANGE",
    "LIGHT_YELLOW",
    "LIGHT_GREEN",
    "LIGHT_CYAN",
    "LIGHT_BLUE",
    "LIGHT_PURPLE",
    "LIGHT_PINK",
    "DARK_GRAY",
    "DARK_RED",
    "DARK_ORANGE",
    "DARK_YELLOW",
    "DARK_GREEN",
    "DARK_CYAN",
    "DARK_BLUE",
    "DARK_PURPLE",
    "DARK_PINK",
    "ASSERTION",
    "ERROR",
    "WARNING",
    "SAVE_FILE",
    "CANT_OPEN_FILE",
    "FILE_NOT_FOUND",
    "OVERWRITE_FILE",
    "INFO",
    "CONFIRM_EXIT",
    "PERMISSION_DENIED",
    "play_audio",
    "get_environment_variable",
    "set_clip",
    "get_clip",
    "get_user_root_dir",
    "send_system_notification",
    "PKG_NAME",
    "PYPI_API_URL",
    "REQUEST_TIMEOUT",
    "get_latest_ver",
    "get_local_version",
    "compare_ver",
    "is_latest_version",
    "upgrade_ohmygui",
    "sleep",
    "sleep_ms",
    'ConsoleIO',
    "CONSTANTS",
    "COMPONENT_MAP",
    "OML_KEYWORDS",
    "UNIT_LIST",
    "convert_oml_to_qml",
    "ErrorLimitExceededError",
    "BaseLayout",
    "BoxLayout",
    "VerticalLayout",
    "HorizontalLayout",
    "GridLayout",
    "FormLayout",
    'BaseDialog', 
    'MessageBox', 
    'FileChooser', 
    'ColorPicker', 
    'Icons', 
    "Buttons", 
    "Application",
    "App",
    "Window",
    "WinSize",
    "get_mouse_x",
    "get_mouse_y",
    "set_mouse_pos",
    "bind",
    "QssString",
    "OP",
    "CONSTANTS",
    "WIDGET",
    "UNIT_LIST",
    "convert_oms_to_qss",
    "ErrorLimitExceededError",
]


from logging import Handler, LogRecord, warning as _warning, info as _info


# Check version & auto upgrade

from os import environ as _environ
if "OMGUI_NO_AUTO_UPGRADE" not in _environ:
    try:
        latest_ok: bool = utils.is_latest_version()
    except Exception as err:
        _warning(f"Remote version check failed, skip upgrade prompt. Error: {err}")
    else:
        if not latest_ok:
            _info("New version of oh-my-gui detected.")
            if _stdout is not None and getattr(_stdout, "isatty", lambda: False)():
                user_choice: str = input("Upgrade to latest version? (y/n): ").strip().lower()
                if user_choice == "y":
                    success: bool = utils.upgrade_ohmygui()
                    if success:
                        _info("Upgrade complete, restart application to take effect.")
            _info("Set environment variable OMGUI_NO_AUTO_UPGRADE=1 to turn off upgrade reminder.")

# Delete other symbols
del _sys_path, _stdout, _dirname, _cast, _root_handler, _warning, _info, _environ, _current_folder
