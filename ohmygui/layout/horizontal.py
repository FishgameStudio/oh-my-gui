# Horizontal Layout

from .base import BaseLayout
from PySide6.QtWidgets import QHBoxLayout

class HorizontalLayout(BaseLayout):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QHBoxLayout()
    def add_stretch(self) -> None:
        """Add a stretch to the layout."""
        self._layout.addStretch()
    def add_spacing(self, size: int) -> None:
        """Add spacing to the layout.   """
        self._layout.addSpacing(size)
    def add_margin(self, size: int) -> None:
        """Add margin to the layout."""
        self._layout.setContentsMargins(size, size, size, size)
    def set_common_spacing(self, size: int) -> None:
        """Set the common spacing for the layout."""
        self._layout.setSpacing(size)
    def set_common_margin(self, size: int) -> None:
        """Set the common margin for the layout."""
        self._layout.setContentsMargins(size, size, size, size)
    def set_common_stretch(self, stretch: int) -> None:
        """Set the common stretch for the layout."""
        for i in range(self._layout.count()):
            self._layout.setStretch(i, stretch)