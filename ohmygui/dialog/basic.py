# Basic dialog window.

from .base import BaseDialog
from PySide6.QtWidgets import QMessageBox, QFileDialog, QColorDialog
from .enums import Icon, Button
from typing import Callable

class MessageBox(BaseDialog):
    def __init__(self, title: str, content: str, icon: Icon = Icon.NoIcon, buttons: Button = Button.Ok) -> None:
        super().__init__(title, content)
        self._win = QMessageBox()
        self._win.setWindowTitle(self.title)
        self._win.setText(self.content)
        self._win.setIcon(icon)
        self._win.setStandardButtons(buttons)
    def set_icon(self, icon: QMessageBox.Icon) -> None:
        """Set the icon of the message box."""
        self._win.setIcon(icon)
    def set_content(self, content: str) -> None:
        return self._win.setText(content)
    def set_info(self, info: str) -> None:
        return self._win.setInformativeText(info)
    def set_detail(self, detail: str) -> None:
        return self._win.setDetailedText(detail)
    def on_click(self, event: Callable[[int], None]):
        """
        Bind callback on button clicked.
        The `int` parameter is the enumerate value of the button.
        """
        event(self._win.question(None, self.title, self.get_content)) # Ask & call

    def set_buttons(self, buttons: Button) -> None:
        """Set the buttons of the message box."""
        self._win.setStandardButtons(buttons)
class FileChooser(BaseDialog):
    def __init__(self, title: str, content: str) -> None:
        super().__init__(title, content)
        self._win = QFileDialog()
        self._win.setWindowTitle(self.title)
    def get_selections(self) -> list[str]:
        """Open the file dialog and return the selected file paths."""
        if self._win.exec():
            return self._win.selectedFiles()
        return []
class ColorPicker(BaseDialog):
    def __init__(self, title: str, content: str) -> None:
        super().__init__(title, content)
        self._win = QColorDialog()
        self._win.setWindowTitle(self.title)
    def get_color(self) -> str:
        """Open the color dialog and return the selected color in hex format."""
        if self._win.exec():
            color = self._win.selectedColor()
            return color.name()
        return "#000000"

    