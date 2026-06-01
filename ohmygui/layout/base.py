# Base layout class.

from ..widget.base import BaseWidget
from PySide6.QtWidgets import QLayout

class BaseLayout:
    def __init__(self) -> None:
        self._layout = QLayout()
        self.stack: list[BaseWidget] = [] # UI Stack

    def add_widget(self, widget: BaseWidget) -> None:
        """Add a widget to the layout."""
        self.stack.append(widget)
        self._layout.addWidget(widget._widget)
    def delete_widget(self, widget: BaseWidget) -> None:
        """Delete a widget from the layout."""
        if widget in self.stack:
            self.stack.remove(widget)
            self._layout.removeWidget(widget._widget)
    def clear(self) -> None:
        """Clear the layout."""
        for widget in self.stack:
            self._layout.removeWidget(widget._widget)
        self.stack.clear()
    def __getitem__(self, idx: int) -> BaseWidget:
        return self.stack[idx]
    @property
    def native(self) -> QLayout:
        """Get the native layout object."""
        return self._layout
    