# Basic Widgets

from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit
from PySide6.QtGui import QPalette
from .base import BaseWidget
from .event import Event
from typing import Callable, Any

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

    def set_text(self, text: str) -> None:
        """Set the text of the label."""
        self._widget.setText(text)

    def set_foreground(self, fg: str) -> None:
        """Set the foreground of the text."""
        self.set_color(fg, self.bg)

    def set_background(self, bg: str) -> None:
        """Set the background of the text."""
        self.set_color(self.fg, bg) 

    def set_color(self, fg: str, bg: str) -> None:
        """Set both the background & foreground"""
        # Set together
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")
    def on_click(self, callback: Event | Callable[[Any], None]) -> None:
        """Set the callback for when the button is clicked."""
        self._widget.clicked.connect(callback)

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
    def set_value(self, value: str) -> None:
        """Set the value of the input."""
        self._widget.setText(value)
    def on_enter(self, callback: Event | Callable[[], None]) -> None:
        """Set the callback for when the input is entered."""
        self._widget.returnPressed.connect(callback)

class PasswordEntry(BaseWidget):
    def __init__(self, default_prompt: str = "Password: ", default_value: str = "") -> None:
        super().__init__()
        self._widget = QLineEdit()
        self._widget.setPlaceholderText(default_prompt)
        self._widget.setText(default_value)
        self._widget.setEchoMode(QLineEdit.EchoMode.Password)
    @property
    def value(self) -> str:
        """Get the value of the input."""
        return self._widget.text()
    def show_password(self) -> None:
        """Show the password."""
        self._widget.setEchoMode(QLineEdit.EchoMode.Normal)
    def on_enter(self, callback: Event | Callable[[], None]) -> None:
        """Set the callback for when the input is entered."""
        self._widget.returnPressed.connect(callback)
    def hide_password(self) -> None:
        """Hide the password."""
        self._widget.setEchoMode(QLineEdit.EchoMode.Password)



