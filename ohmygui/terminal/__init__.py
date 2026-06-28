from logging import info as _info

_info(f"Module {__name__} loaded")
from .conio import ConsoleIO

__all__ = ['ConsoleIO']

del _info