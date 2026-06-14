# Horizontal Layout

from .box import BoxLayout
from PySide6.QtWidgets import QHBoxLayout
from typing import Self, cast
from logging import info, warning, error, critical

info(f"Module {__name__} loaded")

class HorizentalLayout(BoxLayout):
    def __init__(self) -> None:
        super().__init__()
        self._layout: QHBoxLayout = QHBoxLayout() # type: ignore

    def add_stretch(self, stretch: int = 0) -> Self:
        """Add a stretch to the layout."""
        self._layout.addStretch()
        return self
    def add_spacing(self, size: int) -> Self:
        """Add spacing to the layout.   """
        self._layout.addSpacing(size)
        return self
    def add_margin(self, size: int) -> Self:
        """Add margin to the layout."""
        self._layout.setContentsMargins(size, size, size, size)
        return self
    def set_common_spacing(self, size: int) -> Self:
        """Set the common spacing for the layout."""
        self._layout.setSpacing(size)
        return self
    def set_common_margin(self, size: int) -> Self:
        """Set the common margin for the layout."""
        self._layout.setContentsMargins(size, size, size, size)
        return self
    def set_common_stretch(self, stretch: int) -> Self:
        """Set the common stretch for the layout."""
        for i in range(self._layout.count()):
            self._layout.setStretch(i, stretch)
        return self
        