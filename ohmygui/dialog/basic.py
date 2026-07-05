# Basic dialog window.

from PySide6.QtGui import QColor


from .base import BaseDialog
from PySide6.QtWidgets import QMessageBox, QFileDialog, QColorDialog
from .enums import Icons, Buttons
from typing import Callable, Self
from logging import info, warning, error, critical

class MessageBox(BaseDialog):
    def __init__(self, title: str, content: str, icon: Icons = Icons.NoIcon, buttons: Buttons = Buttons.Ok) -> None:
        super().__init__(title, content)
        self._win: QMessageBox = QMessageBox()  # pyright: ignore[reportIncompatibleVariableOverride]
        self._win.setWindowTitle(self.title)
        self._win.setText(self.content)
        self._win.setIcon(icon)
        self._win.setStandardButtons(buttons)
    def set_icon(self, icon: QMessageBox.Icon) -> Self:
        """Set the icon of the message box."""
        self._win.setIcon(icon)
        return self
    def set_content(self, content: str) -> Self:
        info(f"Module {__name__} loaded")
        self._win.setText(content)
        return self
    def set_info(self, info: str) -> Self:
        self._win.setInformativeText(info)
        return self
    def set_detail(self, detail: str) -> Self:
        self._win.setDetailedText(detail)
        return self
    def on_click(self, event: Callable[[int], None]):
        """
        Bind callback on button clicked.
        The `int` parameter is the enumerate value of the button.
        """
        event(self._win.question(None, self.title, self.get_content)) # Ask & call

    def set_buttons(self, buttons: Buttons) -> Self:
        """Set the buttons of the message box."""
        self._win.setStandardButtons(buttons)
        return self
class FileChooser(BaseDialog):
    def __init__(self, title: str) -> None:
        super().__init__(title, "")
        self._win: QFileDialog = QFileDialog()    # pyright: ignore[reportIncompatibleVariableOverride]
        self._win.setWindowTitle(self.title)
    def get_selections(self) -> list[str]:
        """Open the file dialog and return the selected file paths."""
        if self._win.exec():
            return self._win.selectedFiles()
        return []
    def set_default_dir(self, dir: str) -> None:
        """Set the default directory when opening."""
        self._win.setDirectory(dir)
class ColorPicker(BaseDialog):
    def __init__(self, title: str, content: str) -> None:
        super().__init__(title, content)
        self._win: QColorDialog = QColorDialog()  # pyright: ignore[reportIncompatibleVariableOverride]
        self._win.setWindowTitle(self.title)
    def get_color(self) -> str:
        """Open the color dialog and return the selected color in hex format."""
        if self._win.exec():
            color: QColor = self._win.selectedColor()
            return color.name()
        return "#000000"

    