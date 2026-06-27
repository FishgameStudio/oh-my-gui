# Base widget class

from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QGraphicsEffect
from typing import Annotated, Callable, cast, Self
from PySide6.QtCore import QObject, QEvent
from PySide6.QtGui import QKeyEvent, QColor
from logging import info, warning, error, critical

info(f"Module {__name__} loaded")

Size_Type = tuple[int, int]

class _HoverWatcher(QObject):
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

class BaseWidget:
    def __init__(self):
        info("BaseWidget enter __init__")
        self._widget = QWidget() # Store Qt native widget. 
        self._key_callbacks: list[Callable[[int], None]] = []
        self._init_key_event_handler()
    
    def show(self) -> Self: self._widget.show(); return self
    def hide(self) -> Self: self._widget.hide(); return self
    @property 
    def x_pos(self) -> int: return self._widget.x()
    @property 
    def y_pos(self) -> int: return self._widget.y()
    @property 
    def width(self) -> int: return self._widget.width()
    @property 
    def height(self) -> int: return self._widget.height()

    def set_pos(self, x: int, y: int, w: int | None = None, h: int | None = None) -> Self:
        """Set the position.""" 
        self._widget.setGeometry(
            x, y, w if w != None else self.width, 
            h if h != None else self.height
        )
        return self
    def set_size(self, size: Size_Type) -> Self:
        """Set the size."""
        self.set_pos(self.x_pos, self.y_pos, *size)
        return self
    def set_transparency(self, val: Annotated[float, "0.0 ~ 1.0"]) -> Self:
        """
        Set the transparency(Not opacity!) of the widget.\n
        0.0 -> Transparent\n
        1.0 -> Opaque
        """
        if val > 1 or val < 0:
            warning(f"value not bewteen 0 and 1 (was {val})")
            raise ValueError("Value must between 0 and 1")
        self._widget.setWindowOpacity(1.0 - val)
        return self
    def on_hover(self, enter: Callable[[], None], leave: Callable[[], None] | None = None, move: Callable[[], None] | None = None) -> Self:
        """Set the callback when the mouse hovers on it."""
        
        self._widget.installEventFilter(_HoverWatcher(enter, leave, move, cast(QObject,self)))
        return self
    def load_stylesheet(self, qss: str) -> Self:
        self._widget.setStyleSheet(qss)
        return self
    def load_omstylesheet(self, oms: str) -> Self:
        """Load a OMS (Oh My Stylesheet) string"""
        from ..core import convert_oms_to_qss as _convert
        self.load_stylesheet(_convert(oms))
        return self
    def lock(self) -> Self:
        self._widget.setEnabled(False)
        return self
    def unlock(self) -> Self:
        self._widget.setEnabled(True)
        return self
    
    def set_rounded_corner(self, radius: int) -> Self:
        """Set the rounded corner radius of the widget."""
        self._widget.setStyleSheet(f"QWidget {{ border-radius: {radius}px; }}")
        return self
    def _init_key_event_handler(self):
        """Unified hijacking button event, executed only once, all bindings go here"""
        original_key_press = self._widget.keyPressEvent

        def wrapped(evt: QKeyEvent):
            key_text = evt.text()
            key_ascii = ord(key_text) if key_text else evt.key()

            for callback in self._key_callbacks:
                try:
                    callback(key_ascii)
                except Exception as e:
                    error(f"error when calling callback '{callback}' with exception {e} ")
                    raise RuntimeError(f"Error when executing callback: {e}")
            original_key_press(evt)

        self._widget.keyPressEvent = wrapped

    def on_any_keypressed(self, callback: Callable[[int], None]) -> Self:
        """
        Bind event when pressed any key.\n
        The int param is the ASCII code of the current-pressed key.
        """
        self._key_callbacks.append(callback)
        return self

    def on_keypress(self, ascii: int, callback: Callable[[], None]) -> Self:
        """Bind event when a specified key (ASCII code) pressed."""
        def _key_filter(current_key: int):
            if current_key == ascii:
                callback()

        self._key_callbacks.append(_key_filter)
        return self
    def set_shadow(self, blur_radius: int = 10, x_offset: int = 0, y_offset: int = 3, color: str = "#00000080") -> Self:
        """
        Add shadow effects.\n
        :param blur_radius: Blur radius, the larger the radius, the softer the shadow
        :param x_offset: horizontal offset: positive to the right, negative to the left
        :param y_offset: Vertical offset: positive downward, negative upward
        :param color: Shadow color, supports hexadecimal `#RRGGBBAA` with transparency
        """
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(blur_radius)
        shadow_effect.setXOffset(x_offset)
        shadow_effect.setYOffset(y_offset)
        shadow_effect.setColor(QColor(color))
        
        self._widget.setGraphicsEffect(shadow_effect)
        return self
    def remove_shadow(self) -> Self:
        self._widget.setGraphicsEffect(cast(QGraphicsEffect, None))
        return self

    @property
    def is_locked(self) -> bool:
        return not self._widget.isEnabled()
    @property
    def get_size(self) -> Size_Type:
        """Get the size."""
        return (self.width, self.height)
    @property
    def native(self):
        """Native escape port."""
        return self._widget