from logging import info, warning, error, critical

info(f"Module {__name__} loaded")
from .conio import *
__all__ = ["conio"]