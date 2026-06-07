# Form layout class.

from .base import BaseLayout
from PySide6.QtWidgets import QFormLayout
from ..widget.base import BaseWidget
from typing import cast

class FormLayout(BaseLayout):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QFormLayout()

    def add_margin(self, size: int) -> None:
        """Add margin to the layout."""
        self._layout.setContentsMargins(size, size, size, size)

    def set_common_spacing(self, size: int) -> None:
        """Set the common spacing for the layout."""
        self._layout.setSpacing(size)

    def set_common_margin(self, size: int) -> None:
        """Set the common margin for the layout."""
        self._layout.setContentsMargins(size, size, size, size)

    def add_widget(self, widget: BaseWidget, label: str = "") -> None:
        """Add a label<->widget pair to the form layout."""
        self.stack.append(widget)
        cast(QFormLayout, self._layout).addRow(label, widget._widget)