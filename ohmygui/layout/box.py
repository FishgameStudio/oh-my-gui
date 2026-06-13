# Box superclass.

from PySide6.QtWidgets import QBoxLayout
from .base import BaseLayout
from typing import cast, Self

class BoxLayout(BaseLayout):
    def __init__(self) -> None:
        super().__init__()
        self._box: QBoxLayout = cast(QBoxLayout, self._layout)

    def add_stretch(self, stretch: int = 0) -> Self:
        self._box.addStretch(stretch)
        return self

    def add_spacing(self, size: int) -> Self:
        self._box.addSpacing(size)
        return self

    def set_common_spacing(self, size: int) -> Self:
        self._box.setSpacing(size)
        return self

    def set_common_margin(self, size: int) -> Self:
        self._box.setContentsMargins(size, size, size, size)
        return self

    def set_common_stretch(self, stretch: int) -> Self:
        for i in range(self._box.count()):
            self._box.setStretch(i, stretch)
        return self
