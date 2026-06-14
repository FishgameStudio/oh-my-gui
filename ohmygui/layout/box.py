# Box superclass.

from PySide6.QtWidgets import QBoxLayout
from .base import BaseLayout
from typing import cast, Self
from logging import info, warning, error, critical

info(f"Module {__name__} loaded")

class BoxLayout(BaseLayout):
    def __init__(self) -> None:
        super().__init__()
        self._layout: QBoxLayout | None = None # type: ignore

    def add_stretch(self, stretch: int = 0) -> Self:
        self._layout.addStretch(stretch) # type: ignore
        return self

    def add_spacing(self, size: int) -> Self:
        self._layout.addSpacing(size) # type: ignore
        return self

    def set_common_spacing(self, size: int) -> Self:
        self._layout.setSpacing(size) # type: ignore
        return self

    def set_common_margin(self, size: int) -> Self:
        self._layout.setContentsMargins(size, size, size, size) # type: ignore
        return self

    def set_common_stretch(self, stretch: int) -> Self:
        for i in range(self._layout.count()):  # type: ignore
            self._layout.setStretch(i, stretch)  # type: ignore
        return self
    @property
    def native(self):  # type: ignore
        return self._layout
