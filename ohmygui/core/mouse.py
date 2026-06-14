# Mouse position watcher.

from PySide6.QtGui import QCursor
from logging import info, warning, error, critical

def get_mouse_x() -> int:
    """Get the x pos of the mouse."""
    info("get mouse x")
    return QCursor.pos().x()
def get_mouse_y() -> int:
    """Get the y pos of the mouse."""
    info("get mouse y")
    return QCursor.pos().y()
def set_mouse_pos(pos: tuple[int, int]) -> None:
    """Set the position of the mouse."""
    info(f"set mouse pos to {pos}")
    QCursor.pos().setX(pos[0])
    QCursor.pos().setY(pos[1])