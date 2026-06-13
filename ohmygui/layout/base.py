# Base layout class.

from ..widget.base import BaseWidget
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QLayout
from typing import Self
from ..core.context import active_layout

class BaseLayout:
    def __init__(self) -> None:
        self._layout: QLayout # Native layout object
        self.stack: list[BaseWidget] = [] # UI Stack
        if hasattr(active_layout, 'current') and active_layout.current is not None:
            active_layout.current.add_layout(self)
    def add_widget(self, widget: BaseWidget) -> Self:
        """Add a widget to the layout."""
        self.stack.append(widget)
        self._layout.addWidget(widget._widget)
        return self
    def delete_widget(self, widget: BaseWidget) -> Self:
        """Delete a widget from the layout."""
        if widget in self.stack:
            self.stack.remove(widget)
            self._layout.removeWidget(widget._widget)
        else:
            raise ValueError("Widget not found in the layout.")
        return self
    def clear(self) -> Self:
        """Clear the layout."""
        for widget in self.stack:
            self._layout.removeWidget(widget._widget)
        self.stack.clear()
        return self
    def add_layout(self, layout: 'BaseLayout') -> Self:
        """Add a layout to the layout."""
        self._layout.addChildLayout(layout.native)
        return self
    def lock(self) -> Self:
        self._layout.setEnabled(False)
        return self
    def unlock(self) -> Self:
        self._layout.setEnabled(True)
        return self
    @property
    def is_locked(self) -> bool:
        return not self._layout.isEnabled()
    def __len__(self) -> int:
        # len(xxx)
        return len(self.stack)
    def __iter__(self):
        # for x in xxx
        return iter(self.stack)
    def __contains__(self, widget: BaseWidget) -> bool:
        # xx in xxx
        return widget in self.stack
    def __getitem__(self, idx: int) -> BaseWidget:
        # xxx[123]
        return self.stack[idx]
    
    def __enter__(self) -> Self:
        # Set the current layout to active state.
        # Save the layout of the previous layer and restore it upon exit.

        self._prev_layout = getattr(active_layout, 'current', None)
        active_layout.current = self
        return self
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # Restore the previous layout 
        # and clear the activation status.
        active_layout.current = self._prev_layout

        # Auto save to the parent window.
        parent = self._layout.parent()
        if (parent is not None) and (isinstance(parent, QMainWindow)):
            parent.setLayout(self._layout)
            
        return False

    @property
    def native(self) -> QLayout:
        """Get the native layout object."""
        return self._layout
    