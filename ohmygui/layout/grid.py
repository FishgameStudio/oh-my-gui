# Grid Layout.

from .base import BaseLayout
from PySide6.QtWidgets import QGridLayout
from ..widget.base import BaseWidget

class GridLayout(BaseLayout):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QGridLayout()
    def add_margin(self, size: int) -> None:
        """Add margin to the layout."""
        self._layout.setContentsMargins(size, size, size, size)
    def set_common_spacing(self, size: int) -> None:
        """Set the common spacing for the layout."""
        self._layout.setSpacing(size)
    def set_common_margin(self, size: int) -> None:
        """Set the common margin for the layout."""
        self._layout.setContentsMargins(size, size, size, size)
    def add_widget(self, widget: BaseWidget, row: int = 0, column: int = 0, row_span: int = 1, column_span: int = 1) -> None:
        """Add a widget to the layout."""
        self.stack.append(widget)
        self._layout.addWidget(widget._widget, row, column, row_span, column_span)
    