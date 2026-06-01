# Base dialog window.

from PySide6.QtWidgets import QDialog

class BaseDialog:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self._win = QDialog()
        self._win.setWindowTitle(self.title)
    def show(self) -> None:
        self._win.exec_()
    def hide(self) -> None:
        self._win.hide()
    def close(self) -> None:
        self._win.close()
    def set_title(self, title: str) -> None:
        self.title = title
        self._win.setWindowTitle(self.title)
    def set_content(self, content: str) -> None:
        self.content = content
    @property
    def get_title(self) -> str:
        return self.title
    @property
    def get_content(self) -> str:
        return self.content
    @property
    def native(self) -> QDialog:
        """Native escape interface."""
        return self._win