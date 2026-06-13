from .box import BoxLayout
from PySide6.QtWidgets import QVBoxLayout
from typing import Self, cast


class VerticalLayout(BoxLayout):
    def __init__(self) -> None:
        super().__init__()
    @property
    def _box(self):
        return cast(QVBoxLayout, self._box)
    def add_stretch(self, stretch: int = 0) -> Self:
        """Add a stretch to the layout."""
        self._box.addStretch()
        return self
    def add_spacing(self, size: int) -> Self:
        """Add spacing to the layout.   """
        self._box.addSpacing(size)
        return self
    def add_margin(self, size: int) -> Self:
        """Add margin to the layout."""
        self._box.setContentsMargins(size, size, size, size)
        return self
    def set_common_spacing(self, size: int) -> Self:
        """Set the common spacing for the layout."""
        self._box.setSpacing(size)
        return self
    def set_common_margin(self, size: int) -> Self:
        """Set the common margin for the layout."""
        self._box.setContentsMargins(size, size, size, size)
        return self
    def set_common_stretch(self, stretch: int) -> Self:
        """Set the common stretch for the layout."""
        for i in range(self._box.count()):
            self._box.setStretch(i, stretch)
        return self
