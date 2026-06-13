# Grid Layout.

from .base import BaseLayout
from PySide6.QtWidgets import QGridLayout
from ..widget.base import BaseWidget
from typing import Self

class GridLayout(BaseLayout):
    def __init__(self) -> None:
        super().__init__()
        self._grid: QGridLayout = QGridLayout()
    def add_margin(self, size: int) -> Self:
        """Add margin to the layout."""
        self._grid.setContentsMargins(size, size, size, size)
        return self
    def set_common_spacing(self, size: int) -> Self:
        """Set the common spacing for the layout."""
        self._grid.setSpacing(size)
        return self
    def set_common_margin(self, size: int) -> Self:
        """Set the common margin for the layout."""
        self._grid.setContentsMargins(size, size, size, size)
        return self
    def add_widget(self, widget: BaseWidget, row: int = 0, column: int = 0, row_span: int = 1, column_span: int = 1) -> Self:
        """Add a widget to the layout."""
        self.stack.append(widget)
        self._grid.addWidget(widget._widget, row, column, row_span, column_span)
        return self
    