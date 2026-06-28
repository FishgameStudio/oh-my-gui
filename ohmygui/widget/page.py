# Page manager.

from ohmygui.layout.base import BaseLayout
from ..layout.base import BaseLayout as _BaseLayout
from typing import Self
from PySide6.QtWidgets import QWidget

class Page:
    """Make group for some widgets."""
    def __init__(self, layout: _BaseLayout) -> None:
        self.page: QWidget = QWidget()
        self.layout: BaseLayout = layout
        self.layout.native.setParent(self.page)
    def set_layout(self, layout: _BaseLayout) -> Self:
        """Bind a layout to set the current binding group"""
        self.layout = layout
        self.layout.native.setParent(self.page)
        return self
    def show(self) -> Self:
        """Show the page"""
        self.page.show()
        return self
    def hide(self) -> Self:
        """Hide the page"""
        self.page.hide()
        return self

class Interface:
    """Manage some pages"""
    def __init__(self, pages: list[Page]) -> None:
        self.pages = pages
        self.active_idx = -1 # Index of current active page, -1=Uninitialized
    @property
    def all_pages(self) -> list[Page]:
        return self.pages
    def _show_active(self) -> Self:
        self.pages[self.active_idx].show()
        return self
    def set_active_page(self, idx: int) -> Self:
        self.active_idx = idx
        self._show_active()
        return self

    
