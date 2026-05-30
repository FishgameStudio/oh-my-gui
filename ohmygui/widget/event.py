# Main events class for binding button.

from typing import Callable
from base import BaseWidget

class Event:
    def __init__(self, func: Callable):
        self.func = func
    def set_func(self, func: Callable):
        self.func = func
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)