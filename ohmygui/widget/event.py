# Main events class for binding button.

from typing import Any, Callable
from logging import info, warning, error, critical

info(f"Module {__name__} loaded")

class Event:
    def __init__(self, func: Callable) -> None:
        self.func = func
    def set_func(self, func: Callable) -> None:
        self.func: Callable[..., Any] = func
    @property
    def get_func(self) -> Callable:
        return self.func
    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)