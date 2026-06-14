# Sleep module for GUI.

import threading
import time
from logging import info, warning, error, critical

info(f"Module {__name__} loaded")

def sleep(second: float) -> None:
    """Sleep for seconds (NON-BLOCKING)"""
    thread = threading.Thread(target=time.sleep, args=(second,), daemon=True)
    thread.start()

def sleep_ms(millisecond: int) -> None:
    """Sleep for milliseconds (NON-BLOCKING)"""
    thread = threading.Thread(target=time.sleep, args=(millisecond / 1000,), daemon=True)
    thread.start()
