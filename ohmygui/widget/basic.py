# Basic Widgets

from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QPalette

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
    @property
    def native(self):
        """Native escape port."""
        return self._widget

class Text(BaseWidget):
    """Label text."""
    def __init__(self, text: str = "", fg: str = "#000000", bg: str = "#ffffff"):
        super().__init__()
        self._widget = QLabel(text)
        self._widget.setAutoFillBackground(True)
        self.set_color(fg, bg)
        
    @property
    def text(self) -> str: return self._widget.text()
    
    @property
    def fg(self) -> str: return self._widget.palette().color(QPalette.ColorRole.WindowText).name()
    
    @property
    def bg(self) -> str: return self._widget.palette().color(QPalette.ColorRole.Window).name()

    def set_text(self, text: str) -> None:
        """Set the text of the label."""
        self._widget.setText(text)

    def set_foreground(self, fg: str) -> None:
        """Set the foreground of the text."""
        self.set_color(fg, self.bg)  # Don't cover the foreground

    def set_background(self, bg: str) -> None:
        """Set the background of the text."""
        self.set_color(self.fg, bg) 

    def set_color(self, fg: str, bg: str) -> None:
        """Set both the background & foreground"""
        # Set together
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")