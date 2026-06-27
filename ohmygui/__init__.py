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
_current_folder = _dirname(__file__)
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
    def format(self, record):
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
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[_logging.StreamHandler(_stdout)]
)
_root_handler = _logging.getLogger().handlers[0]
from typing import cast as _cast
_root_handler.setFormatter(_ColorFormatter(_cast(_logging.Formatter, _root_handler.formatter)._fmt))


__author__  = "Fishgame Studio"
__version__ = "1.2.1"

from . import core
from . import widget
from . import dialog
from . import utils
from . import layout
from . import terminal
from . import oml


from sys import modules as _modules
__all__ = [k for k in _modules[__name__].__dict__ if not k.startswith("_")]
from logging import warning as _warning, info as _info


# Check version & auto upgrade

from os import environ as _environ
from sys import stdout as _stdout
if "OMGUI_NO_AUTO_UPGRADE" not in _environ:
    try:
        latest_ok = utils.is_latest_version()
    except Exception as err:
        _warning(f"Remote version check failed, skip upgrade prompt. Error: {err}")
    else:
        if not latest_ok:
            _info("New version of oh-my-gui detected.")
            if _stdout is not None and getattr(_stdout, "isatty", lambda: False)():
                user_choice = input("Upgrade to latest version? (y/n): ").strip().lower()
                if user_choice == "y":
                    success = utils.upgrade_ohmygui()
                    if success:
                        _info("Upgrade complete, restart application to take effect.")
            _info("Set environment variable OMGUI_NO_AUTO_UPGRADE=1 to turn off upgrade reminder.")
