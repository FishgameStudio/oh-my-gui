# Box superclass.

from PySide6.QtWidgets import QBoxLayout
from .base import BaseLayout
from typing import cast, Self

class BoxLayout(BaseLayout):
    def __init__(self) -> None:
        super().__init__()
        self._layout: QBoxLayout = cast(QBoxLayout, self._layout) # type: ignore

    def add_stretch(self, stretch: int = 0) -> Self:
        self._layout.addStretch(stretch)
        return self

    def add_spacing(self, size: int) -> Self:
        self._layout.addSpacing(size)
        return self

    def set_common_spacing(self, size: int) -> Self:
        self._layout.setSpacing(size)
        return self

    def set_common_margin(self, size: int) -> Self:
        self._layout.setContentsMargins(size, size, size, size)
        return self

    def set_common_stretch(self, stretch: int) -> Self:
        for i in range(self._layout.count()):
            self._layout.setStretch(i, stretch)
        return self
    @property
    def native(self):
        return self._layout
