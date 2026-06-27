from logging import info as _info

_info(f"Module {__name__} loaded")
from .conio import ConsoleIO

from sys import modules as _modules
__all__ = [k for k in _modules[__name__].__dict__ if not k.startswith("_")]
