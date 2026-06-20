# Main window class

from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import QSize, QObject
from PySide6.QtGui import QResizeEvent, QCloseEvent, QAction
from ..widget.base import BaseWidget
from ..layout.base import BaseLayout
from typing import Callable, Any, Annotated, Self
from typing_extensions import deprecated as _deprecated
from logging import info, warning, error, critical
from ..widget.page import Interface as _Interface
from weakref import finalize as _finalize


Size_Type = tuple[int, int]
Dir = Size_Type
RelDir = tuple[Annotated[float, "0.0 ~ 1.0"], Annotated[float, "0.0 ~ 1.0"]]

class Window:
    def __init__(self, title: str = "", size: Size_Type = (800, 500)) -> None:
        info("Window enter __init__")
        self._win = QMainWindow()
        self._win.setWindowTitle(title)
        self._win.resize(*size)
        self.central = QWidget() # Central Widget for binding UI.
        self._win.setCentralWidget(self.central)
        self.menubar = self._win.menuBar()
        self._menus = []
        self.stack: list[tuple[bool, BaseWidget]] = [] # is_relative_binded & UI Stack
        # caches of Relative positions
        self._rel_cache: dict[BaseWidget, RelDir] = {}
        self._interface: _Interface | None = None
        # destructor
        self._dtor = _finalize(self, self.__destruct__)
        info("Window exit __init__")

    @property
    def x(self) -> int: return self._win.x()
    @property
    def y(self) -> int: return self._win.y()
    @property
    def w(self) -> int: return self._win.width()
    @property
    def h(self) -> int: return self._win.height()

    def set_size(self, size: Size_Type) -> Self:
        """Set the size of the window."""
        info(f"set Window size as {size}")
        self._win.resize(*size)
        return self

    def set_position(self, pos: Dir) -> Self:
        """Set the position of the window on the screen."""
        info(f"set pos as {pos}")
        self._win.setGeometry(*pos, self.w, self.h)
        return self

    @property
    def size(self) -> Size_Type:
        """Returns the window size."""
        return (self.w, self.h)

    def fix_size(self) -> Self:
        """Fix the size."""
        info("Window size fixed")
        self._win.setFixedSize(self.w, self.h)
        return self

    def unfix_size(self) -> Self:
        """Unfix the size."""
        info("Window size unfixed")
        # Unlock the size scope.
        self._win.setMinimumSize(0, 0)
        self._win.setMaximumSize(QSize(16777215, 16777215))
        return self

    def bind_widget(self, widget: BaseWidget, dir: Dir) -> Self:
        """Bind a widget to the window."""
        info(f"bind widget {widget}")
        # All the widgets are on the central widget.
        
        self.stack.append((False, widget))
        widget._widget.setParent(self.central)
        widget.set_pos(*dir)
        widget.show()
        return self

    def relative_bind(self, widget: BaseWidget, reldir: RelDir) -> Self: 
        """Bind widgets by relative position."""
        info(f"bind widget {widget} in relative")
        self.stack.append((True, widget))
        widget._widget.setParent(self.central)
        # store relative pos
        self._rel_cache[widget] = reldir
        
        # Parent window w/h
        pw = self._win.width()
        ph = self._win.height()
        # The w/h of itself
        w = widget.native.width()
        h = widget.native.height()
        # Calc absolute position
        x = (pw * reldir[0]) - (w * 0.5)
        y = (ph * reldir[1]) - (h * 0.5)

        widget.set_pos(int(x), int(y))
        widget.show()
        return self
    def set_parent(self, parent: 'Window') -> Self:
        info(f"Window parent set as {parent}")
        self._win.setParent(parent.native)
        return self
    @property
    def parent(self) -> QObject | None:
        return self._win.parent()
    @property
    def children(self) -> list[QObject]:
        return self._win.children()
    
    @property
    @_deprecated("`top_widgets` is deprecated. Use toplevel_widget instead.")
    def top_widgets(self) -> Self: ...

    @property
    def toplevel_widget(self) -> QWidget:
        """Returns the top window & widgets."""
        return self._win.topLevelWidget()

    def set_layout(self, layout: BaseLayout) -> Self:
        """Set a layout on the window's central widget."""
        info(f"set layout as {layout}")
        self.central.setLayout(layout.native)
        # Clear interface
        self._interface = None
        return self
    def set_interface(self, interface: _Interface) -> Self:
        """Set self._interface"""
        info(f"set interface as {interface}")
        self._interface = interface
        # Detach layout
        self.central.setLayout(None) # type: ignore
        return self
    def load_style_from(self, path: str) -> Self:
        """Load style sheet from a QSS file."""
        info(f"load QSS from file {path}")
        qss: str
        try:
            with open(path, "r", encoding="utf-8") as f:
                qss = f.read()
            info("QSS has been read")
        except FileNotFoundError as e:
            error(f"QSS file {path} not found")
            raise FileNotFoundError(f"QSS file not found: {e.filename}")
        self._win.setStyleSheet(qss)
        return self
    def load_style_string(self, qss: str) -> Self:
        """Load style sheet from a string."""
        self._win.setStyleSheet(qss)
        return self
    @property
    def export_QSS(self) -> str:
        """Export the current QStyleSheet."""
        return self._win.styleSheet()
    
    def _update_relpos(self) -> None:
        """Update positions of relative-binded widgets."""
        def _get_relwidgets() -> list[BaseWidget]:
            res: list[BaseWidget] = []
            for tuple_ in self.stack:
                if tuple_[0]:
                    res.append(tuple_[1])
            return res
        relwidgets = _get_relwidgets()
        for widget in relwidgets:
            # Read relpos from cache
            relx, rely = self._rel_cache[widget]
            pw = self.native.width()
            ph = self.native.height()
            ww = widget.native.width()
            wh = widget.native.height()

            x = pw * relx - ww / 2
            y = ph * rely - wh / 2
            widget.set_pos(int(x), int(y))
        
    def on_resize(self, callback: Callable[[int, int], None]) -> Self: 
        """
        Bind callback when resizing window.
        The `int, int` params are the width & height of the window.
        """
        original_event = self._win.resizeEvent
        # Wrap the event.
        def wrapped(event: QResizeEvent) -> None:
            # Execute origin event
            original_event(event)
            # Update relative-binded widget while resizing. 
            self._update_relpos()
            callback(self.w, self.h)
        self._win.resizeEvent = wrapped
        return self

    def show(self) -> Self:
        """Show the window."""
        self._win.show()
        return self

    def hide(self) -> Self:
        """Hide the window."""
        self._win.hide()
        return self
    def close(self) -> Self:
        """Close the window."""
        self._win.close()
        return self
    def on_close(self, event: Callable[[Any], None]) -> Self:
        """Set the callback for when the window is closed."""
        original = self._win.closeEvent
        def wrapped(evt: QCloseEvent):
            event(None)
            original(evt)
        self._win.closeEvent = wrapped
        return self
    def set_bg(self, color: str) -> Self:
        """Set the background color of the window."""
        self._win.setStyleSheet(f"background-color: {color};")
        return self
    
    def add_menu(
            self, name: str, shortcut: str, 
            actions: list[tuple[str, Callable] | None]
        ) -> Self:
        """
        Add a top menu.

        `None` in actions means a separator. 
        `tuple[str, Callable]` is the name and the callback.
        """
        menu = self.menubar.addMenu(f"{name}(&{shortcut})")
        for action in actions:
            if action is not None:
                a = QAction(action[0], self._win)
                a.triggered.connect(action[1])
                menu.addAction(a)
            else:
                menu.addSeparator()
        self._menus.append(menu)    
        return self

    def destroy(self) -> Self:
        """Destory this window."""
        self._win.destroy()
        return self
    
    @property
    def menus(self) -> list:
        return self._menus
        
    @property
    def bg_color(self) -> str:
        """Get the background color of the window."""
        return self._win.palette().color(self._win.backgroundRole()).name()
    @property
    def top_widget(self) -> BaseWidget:
        return self.stack[-1][1]

    def __getitem__(self, idx: int):
        return self.stack[idx][1]

    @property
    def native(self):
        """Native escape port: Get the underlying PySide6 control"""
        return self._win
    
    def __destruct__(self) -> None:
        self._interface = None
        self._win.setLayout(None) # type: ignore
        self._rel_cache.clear()
        self._menus.clear()
        self.stack.clear()
        self._win.deleteLater()
