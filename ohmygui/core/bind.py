# Decorator for binding events.

from typing import Callable as _Callable, Any as _Any
from logging import info

def bind(register_method: _Callable[[_Callable[..., _Any]], _Any]):
    """
    Decorator for register function in register methods.

    Example::

        win = Window()
        @core.bind(win.on_close)
        def close(e) -> None: # bind for close event.
            ... 
    """
    def decorator(target_func: _Callable[..., _Any]) -> _Callable[..., _Any]:
        register_method(target_func)
        info(f"bind callback function {target_func} to register method {register_method}")
        return target_func
    return decorator

