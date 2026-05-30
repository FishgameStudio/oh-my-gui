# Base widget class

from PySide6.QtWidgets import QWidget

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
    def set_size(self, width: int, height: int) -> None:
        """Set the size."""
        self.set_pos(self.x_pos, self.y_pos, width, height)
    @property
    def native(self):
        """Native escape port."""
        return self._widget