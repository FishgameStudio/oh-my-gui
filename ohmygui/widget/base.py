# Base widget class

from PySide6.QtWidgets import QWidget
from typing import Annotated

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
    @property
    def get_size(self) -> Size_Type:
        """Get the size."""
        return (self.width, self.height)
    @property
    def native(self):
        """Native escape port."""
        return self._widget