# Base layout class.

from ..widget.base import BaseWidget
from PySide6.QtWidgets import QLayout

class BaseLayout:
    def __init__(self) -> None:
        self._layout: 'QLayout' # Native layout object
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
        else:
            raise ValueError("Widget not found in the layout.")
    def clear(self) -> None:
        """Clear the layout."""
        for widget in self.stack:
            self._layout.removeWidget(widget._widget)
        self.stack.clear()
    def add_layout(self, layout: 'BaseLayout') -> None:
        """Add a layout to the layout."""
        self._layout.addChildLayout(layout.native)
    def lock(self) -> None:
        self._layout.setEnabled(False)
    def unlock(self) -> None:
        self._layout.setEnabled(True)
    @property
    def is_locked(self) -> bool:
        return not self._layout.isEnabled()
    def __len__(self) -> int:
        return len(self.stack)
    def __iter__(self):
        return iter(self.stack)
    def __contains__(self, widget: BaseWidget) -> bool:
        return widget in self.stack
    def __getitem__(self, idx: int) -> BaseWidget:
        return self.stack[idx]
    @property
    def native(self) -> QLayout:
        """Get the native layout object."""
        return self._layout
    