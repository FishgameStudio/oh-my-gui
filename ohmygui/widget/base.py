# Base widget class

from PySide6.QtWidgets import QWidget
from typing import Annotated, Callable, cast
from PySide6.QtCore import QObject, QEvent


Size_Type = tuple[int, int]

class BaseWidget:
    def __init__(self):
        self._widget = QWidget() # Store Qt native widget. 
    def show(self) -> None: self._widget.show()
    def hide(self) -> None: self._widget.hide()
    @property 
    def x_pos(self) -> int: return self._widget.x()
    @property 
    def y_pos(self) -> int: return self._widget.y()
    @property 
    def width(self) -> int: return self._widget.width()
    @property 
    def height(self) -> int: return self._widget.height()

    def set_pos(self, x: int, y: int, w: int | None = None, h: int | None = None) -> None:
        """Set the position.""" 
        self._widget.setGeometry(
            x, y, w if w != None else self.width, 
            h if h != None else self.height
        )
    def set_size(self, size: Size_Type) -> None:
        """Set the size."""
        self.set_pos(self.x_pos, self.y_pos, *size)
    def set_transparency(self, val: Annotated[float, "0.0 ~ 1.0"]) -> None:
        """
        Set the transparency(Not opacity!) of the widget.
        0.0 -> Transparent
        1.0 -> Opaque
        """
        if val > 1 or val < 0:
            raise ValueError("Value must between 1 and 0")
        self._widget.setWindowOpacity(1.0 - val)
    def on_hover(self, enter: Callable[[], None], leave: Callable[[], None] | None = None, move: Callable[[], None] | None = None) -> None:
        """Set the callback when the mouse hovers on it."""
        class HoverWatcher(QObject):
            def __init__(self, e_cb, l_cb, m_cb, parent):
                super().__init__(parent)
                self.enter = e_cb
                self.leave = l_cb
                self.move = m_cb

            def eventFilter(self, obj: QObject, evt: QEvent):
                if evt.type() == QEvent.Type.HoverEnter and self.enter is not None:
                    self.enter()
                elif evt.type() == QEvent.Type.HoverLeave and self.leave is not None:
                    self.leave()
                elif evt.type() == QEvent.Type.HoverMove and self.move is not None:
                    self.move()
                return False
        self._widget.installEventFilter(HoverWatcher(enter, leave, move, cast(QObject,self)))
    @property
    def get_size(self) -> Size_Type:
        """Get the size."""
        return (self.width, self.height)
    @property
    def native(self):
        """Native escape port."""
        return self._widget