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

import logging as _logging
log_format = "[%(asctime)s] [%(levelname)s] in [%(funcName)s] : %(message)s"
date_format = "%Y-%m-%d-%H:%M:%S"
_logging.basicConfig(
    level=_logging.DEBUG,
    format=log_format,
    datefmt=date_format
)

__author__  = "Fishgame Studio"
__version__ = "0.5.1"

from . import core
from . import widget
from . import dialog
from . import utils
from . import layout
from . import terminal


__all__ = [
    "core", "widget", "dialog", "utils", "layout", "terminal"
]