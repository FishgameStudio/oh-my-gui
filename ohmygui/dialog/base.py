# Base dialog window.

from PySide6.QtWidgets import QDialog
from typing import Self

class BaseDialog:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self._win = QDialog()
        self._win.setWindowTitle(self.title)
    def show(self) -> Self:
        self._win.exec()
        return self
    def hide(self) -> Self:
        self._win.hide()
        return self
    def close(self) -> Self:
        self._win.close()
        return self
    def set_title(self, title: str) -> Self:
        self.title = title
        self._win.setWindowTitle(self.title)
        return self
    def set_content(self, content: str) -> Self:
        self.content = content
        return self
    def load_stylesheet(self, qss: str) -> Self:
        self._win.setStyleSheet(qss)
        return self
    def lock(self) -> Self:
        self._win.setEnabled(False)
        return self
    def unlock(self) -> Self:
        self._win.setEnabled(True)
        return self
    @property
    def is_locked(self) -> bool:
        return not self._win.isEnabled()
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