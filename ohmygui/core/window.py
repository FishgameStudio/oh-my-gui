# Main window class

from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import QSize, QObject
from PySide6.QtGui import QCloseEvent
from ..widget.base import BaseWidget
from ..layout.base import BaseLayout
from ..widget.event import Event
from typing import Callable, Any

Size_Type = tuple[int, int]

class Window:
    def __init__(self, title: str = "", size: Size_Type = (800, 500)) -> None:
        self._win = QMainWindow()
        self._win.setWindowTitle(title)
        self._win.resize(*size)
        self.central = QWidget() # Central Widget for binding UI.
        self._win.setCentralWidget(self.central)
        self.stack: list[BaseWidget] = [] # UI Stack

    @property
    def x(self) -> int: return self._win.x()
    @property
    def y(self) -> int: return self._win.y()
    @property
    def w(self) -> int: return self._win.width()
    @property
    def h(self) -> int: return self._win.height()

    def set_size(self, size: Size_Type) -> None:
        """Set the size of the window."""
        self._win.resize(*size)

    def set_position(self, x: int, y: int) -> None:
        """Set the position of the window on the screen."""
        self._win.setGeometry(x, y, self.w, self.h)

    @property
    def get_size(self) -> Size_Type:
        """Returns the window size."""
        return (self.w, self.h)

    def fix_size(self) -> None:
        """Fix the size."""
        self._win.setFixedSize(self.w, self.h)

    def unfix_size(self) -> None:
        """Unfix the size."""
        # Unlock the size scope.
        self._win.setMinimumSize(0, 0)
        self._win.setMaximumSize(QSize(16777215, 16777215))

    def bind_widget(self, widget: BaseWidget, dir: Size_Type) -> None:
        """Bind a widget to the window."""
        # All the widgets are on the central widget.
        
        self.stack.append(widget)
        widget._widget.setParent(self.central)
        widget.set_pos(*dir)
        widget.show()
    def set_parent(self, parent: 'Window') -> None:
        self._win.setParent(parent.native)
    @property
    def parent(self) -> QObject | None:
        return self._win.parent()
    @property
    def children(self) -> list[QObject]:
        return self._win.children()

    @property
    def top_widgets(self) -> QWidget:
        """Returns the top window & widgets."""
        return self._win.topLevelWidget()

    def set_layout(self, layout: BaseLayout) -> None:
        """Set a layout on the window's central widget."""
        self.central.setLayout(layout.native)
    def load_style_from(self, path: str) -> None:
        """Load style sheet from a QSS file."""
        qss: str
        try:
            with open(path, "r", encoding="utf-8") as f:
                qss = f.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"QSS file not found: {e.filename}")
        self._win.setStyleSheet(qss)
    def load_style_string(self, qss: str) -> None:
        """Load style sheet from a string."""
        self._win.setStyleSheet(qss)
    @property
    def export_QSS(self) -> str:
        """Export the current QStyleSheet."""
        return self._win.styleSheet()
    
    def relative_bind(self): ...
    def set_snap_layout(self): ...
    def on_resize(self): ...


    def show(self) -> None:
        """Show the window."""
        self._win.show()

    def hide(self) -> None:
        """Hide the window."""
        self._win.hide()
    def close(self) -> None:
        """Close the window."""
        self._win.close()
    def on_close(self, event: Callable[[Any], None]) -> None:
        """Set the callback for when the window is closed."""
        self._win.closeEvent = event
    def set_bg(self, color: str) -> None:
        """Set the background color of the window."""
        self._win.setStyleSheet(f"background-color: {color};")

    @property
    def bg_color(self) -> str:
        """Get the background color of the window."""
        return self._win.palette().color(self._win.backgroundRole()).name()
    @property
    def top_widget(self) -> BaseWidget:
        return self.stack[-1]

    def __getitem__(self, idx: int):
        return self.stack[idx]

    @property
    def native(self):
        """Native escape port: Get the underlying PySide6 control"""
        return self._win