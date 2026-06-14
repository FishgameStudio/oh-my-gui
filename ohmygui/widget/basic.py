# Basic Widgets

from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit
from PySide6.QtGui import QPalette, QKeyEvent, QFont
from PySide6.QtCore import QObject, QEvent
from .base import BaseWidget
from .event import Event
from typing import Callable, Any, Optional, cast, Self

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

    def set_text(self, text: str) -> Self:
        """Set the text of the label."""
        self._widget.setText(text)
        return self

    def set_foreground(self, fg: str) -> Self:
        """Set the foreground of the text."""
        self.set_color(fg, self.bg)  # Don't cover the foreground
        return self

    def set_background(self, bg: str) -> Self:
        """Set the background of the text."""
        self.set_color(self.fg, bg) 
        return self

    def set_color(self, fg: str, bg: str) -> Self:
        """Set both the background & foreground"""
        # Set together
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")
        return self
    
    def set_font(self, font: str, size: int = 10) -> Self:
        """Set the font of the text."""
        font_ = QFont(font, pointSize=size)
        self._widget.setFont(font_)
        return self


class Button(BaseWidget):
    def __init__(self, text: str, fg: str = "#ffffff", bg: str = "#000000"):
        super().__init__()
        self._widget = QPushButton(text)
        self.set_color(fg, bg)
    
    @property
    def text(self) -> str: return self._widget.text()
    
    @property
    def fg(self) -> str: return self._widget.palette().color(QPalette.ColorRole.ButtonText).name()
    
    @property
    def bg(self) -> str: return self._widget.palette().color(QPalette.ColorRole.Button).name()

    def set_text(self, text: str) -> Self:
        """Set the text of the label."""
        self._widget.setText(text)
        return self

    def set_foreground(self, fg: str) -> Self:
        """Set the foreground of the text."""
        self.set_color(fg, self.bg)
        return self

    def set_background(self, bg: str) -> Self:
        """Set the background of the text."""
        self.set_color(self.fg, bg) 
        return self

    def set_color(self, fg: str, bg: str) -> Self:
        """Set both the background & foreground"""
        # Set together
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")
        return self
    def on_click(self, event: Callable[[Any], None]) -> Self:
        """Set the callback for when the button is clicked."""
        self._widget.clicked.connect(event)
        return self
    def set_font(self, font: str, size: int = 10) -> Self:
        """Set the font of the text."""
        font_ = QFont(font, pointSize=size)
        self._widget.setFont(font_)
        return self

class InputEntry(BaseWidget):
    def __init__(self, default_prompt: str = "", default_value: str = "") -> None:
        super().__init__()
        self._widget = QLineEdit()
        self._widget.setPlaceholderText(default_prompt)
        self._widget.setText(default_value)
    @property
    def value(self) -> str:
        """Get the value of the input."""
        return self._widget.text()
    def set_value(self, value: str) -> Self:
        """Set the value of the input."""
        self._widget.setText(value)
        return self
    def clear_value(self) -> Self:
        """Clear the value of the input."""
        self.set_value("")
        return self
    def on_submit(self, event: Callable[[], None]) -> Self:
        """Set the callback for when the input is entered."""
        self._widget.returnPressed.connect(event)
        return self
    def on_key_press(self, callback: Callable[[str], None]) -> Self:
        """
        Set the callback for when a key pressed.
        The `str` param is for current pressed key.
        """
        class KeyWatcher(QObject):
            def __init__(self, cb: Callable[[str], None], parent: Optional[QObject]):
                super().__init__(parent)
                self.callback = cb
            def eventFilter(self, obj: QObject, e: QEvent) -> bool:
                if e.type() == QEvent.Type.KeyPress:
                    if isinstance(e, QKeyEvent):
                        ke = cast(QKeyEvent, e)
                        key_text = ke.text()
                        if key_text:
                            self.callback(key_text)
                return False

        self._widget.installEventFilter(KeyWatcher(callback, cast(QObject, self)))
        return self
    def set_font(self, font: str, size: int = 10) -> Self:
        """Set the font of the text."""
        font_ = QFont(font, pointSize=size)
        self._widget.setFont(font_)
        return self

class PasswordEntry(BaseWidget):
    def __init__(self, default_prompt: str = "Password: ", default_value: str = "") -> None:
        super().__init__()
        self._widget = QLineEdit()
        self._widget.setPlaceholderText(default_prompt)
        self._widget.setText(default_value)
        self._widget.setEchoMode(QLineEdit.EchoMode.Password) # Hide the password by default
    @property
    def value(self) -> str:
        """Get the value of the input."""
        return self._widget.text()
    def show_password(self) -> Self:
        """Show the password."""
        self._widget.setEchoMode(QLineEdit.EchoMode.Normal)
        return self
    def on_submit(self, event: Callable[[Any], None]) -> Self:
        """Set the callback for when the input is entered."""
        self._widget.returnPressed.connect(event)
        return self
    def set_font(self, font: str, size: int = 10) -> Self:
        """Set the font of the text."""
        font_ = QFont(font, pointSize=size)
        self._widget.setFont(font_)
        return self
    def hide_password(self) -> Self:
        """Hide the password."""
        self._widget.setEchoMode(QLineEdit.EchoMode.Password)
        return self



