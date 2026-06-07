# Advanced widgets

from .base import BaseWidget
from typing import Any, Callable
from PySide6.QtWidgets import (
    QRadioButton, QComboBox, 
    QListWidget, QTableWidget, 
    QTableWidgetItem, QSlider, 
    QProgressBar, QTextEdit, 
    QGraphicsView, QGraphicsScene, 
    QGraphicsEllipseItem, QGraphicsLineItem, 
    QGraphicsRectItem
)
from PySide6.QtGui import QPalette, QColor, QPen, QBrush

class RadioButton(BaseWidget):
    def __init__(self, text: str, fg: str = "#ffffff", bg: str = "#000000"):
        super().__init__()
        self._widget = QRadioButton(text)
        self.set_color(fg, bg)
    
    @property
    def text(self) -> str:
        """Get the text of the radio button."""
        return self._widget.text()
    
    @property
    def fg(self) -> str:
        """Get the foreground color of the radio button."""
        return self._widget.palette().color(QPalette.ColorRole.ButtonText).name()
    
    @property
    def bg(self) -> str:
        """Get the background color of the radio button."""
        return self._widget.palette().color(QPalette.ColorRole.Button).name()

    @property
    def checked(self) -> bool:
        """Get the checked state of the radio button."""
        return self._widget.isChecked()

    def set_text(self, text: str) -> None:
        """Set the display text of the radio button."""
        self._widget.setText(text)

    def set_foreground(self, fg: str) -> None:
        """Set the foreground color of the radio button text."""
        self.set_color(fg, self.bg)

    def set_background(self, bg: str) -> None:
        """Set the background color of the radio button."""
        self.set_color(self.fg, bg) 

    def set_color(self, fg: str, bg: str) -> None:
        """Set both foreground and background colors of the radio button."""
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")

    def set_checked(self, state: bool) -> None:
        """Set the checked state of the radio button."""
        self._widget.setChecked(state)

    def on_click(self, event: Callable[[Any], None]) -> None:
        """Set the callback for when the radio button is clicked."""
        self._widget.clicked.connect(event)

    def set_font(self, font: str) -> None:
        """Set the font family of the radio button text."""
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")


class ComboBox(BaseWidget):
    def __init__(self, fg: str = "#ffffff", bg: str = "#000000"):
        super().__init__()
        self._widget = QComboBox()
        self.set_color(fg, bg)
    
    @property
    def fg(self) -> str:
        """Get the foreground color of the combobox."""
        return self._widget.palette().color(QPalette.ColorRole.ButtonText).name()
    
    @property
    def bg(self) -> str:
        """Get the background color of the combobox."""
        return self._widget.palette().color(QPalette.ColorRole.Button).name()

    @property
    def current_text(self) -> str:
        """Get the currently selected text."""
        return self._widget.currentText()

    @property
    def current_index(self) -> int:
        """Get the currently selected index."""
        return self._widget.currentIndex()

    def add_item(self, text: str) -> None:
        """Add a single item to the combobox."""
        self._widget.addItem(text)

    def add_items(self, items: list[str]) -> None:
        """Add multiple items to the combobox."""
        self._widget.addItems(items)

    def clear_items(self) -> None:
        """Clear all items from the combobox."""
        self._widget.clear()

    def set_current_index(self, index: int) -> None:
        """Set the current selected index."""
        self._widget.setCurrentIndex(index)

    def set_foreground(self, fg: str) -> None:
        """Set the foreground color of the combobox."""
        self.set_color(fg, self.bg)

    def set_background(self, bg: str) -> None:
        """Set the background color of the combobox."""
        self.set_color(self.fg, bg)

    def set_color(self, fg: str, bg: str) -> None:
        """Set both foreground and background colors."""
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")

    def on_selection_change(self, event: Callable[[Any], None]) -> None:
        """Set callback for when selection changes."""
        self._widget.currentIndexChanged.connect(event)

    def set_font(self, font: str) -> None:
        """Set the font family of the combobox text."""
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")


class ListWidget(BaseWidget):
    def __init__(self, fg: str = "#ffffff", bg: str = "#000000"):
        super().__init__()
        self._widget = QListWidget()
        self.set_color(fg, bg)
    
    @property
    def fg(self) -> str:
        """Get the foreground color of the list widget."""
        return self._widget.palette().color(QPalette.ColorRole.ButtonText).name()
    
    @property
    def bg(self) -> str:
        """Get the background color of the list widget."""
        return self._widget.palette().color(QPalette.ColorRole.Button).name()

    @property
    def current_text(self) -> str:
        """Get the text of the currently selected item."""
        item = self._widget.currentItem()
        return item.text() if item else ""

    @property
    def current_index(self) -> int:
        """Get the index of the currently selected item."""
        return self._widget.currentRow()

    def add_item(self, text: str) -> None:
        """Add a single item to the list widget."""
        self._widget.addItem(text)

    def add_items(self, items: list[str]) -> None:
        """Add multiple items to the list widget."""
        self._widget.addItems(items)

    def clear_items(self) -> None:
        """Clear all items from the list widget."""
        self._widget.clear()

    def remove_current_item(self) -> None:
        """Remove the currently selected item from the list."""
        self._widget.takeItem(self.current_index)

    def set_current_index(self, index: int) -> None:
        """Set the currently selected item by index."""
        self._widget.setCurrentRow(index)

    def set_foreground(self, fg: str) -> None:
        """Set the foreground color of the list widget."""
        self.set_color(fg, self.bg)

    def set_background(self, bg: str) -> None:
        """Set the background color of the list widget."""
        self.set_color(self.fg, bg)

    def set_color(self, fg: str, bg: str) -> None:
        """Set both foreground and background colors."""
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")

    def on_selection_change(self, event: Callable[[Any], None]) -> None:
        """Set callback for when the selected item changes."""
        self._widget.currentItemChanged.connect(event)

    def set_font(self, font: str) -> None:
        """Set the font family of the list items."""
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")

class Table(BaseWidget):
    def __init__(self, rows: int = 0, cols: int = 0, fg: str = "#ffffff", bg: str = "#000000"):
        super().__init__()
        self._widget = QTableWidget(rows, cols)
        self.set_color(fg, bg)

    @property
    def fg(self) -> str:
        """Get the foreground color of the table."""
        return self._widget.palette().color(QPalette.ColorRole.ButtonText).name()

    @property
    def bg(self) -> str:
        """Get the background color of the table."""
        return self._widget.palette().color(QPalette.ColorRole.Button).name()

    @property
    def row_count(self) -> int:
        """Get the total number of rows in the table."""
        return self._widget.rowCount()

    @property
    def col_count(self) -> int:
        """Get the total number of columns in the table."""
        return self._widget.columnCount()

    @property
    def current_row(self) -> int:
        """Get the index of the currently selected row."""
        return self._widget.currentRow()

    @property
    def current_col(self) -> int:
        """Get the index of the currently selected column."""
        return self._widget.currentColumn()

    def set_headers(self, headers: list[str]) -> None:
        """Set horizontal header labels for the table."""
        self._widget.setHorizontalHeaderLabels(headers)

    def set_item(self, row: int, col: int, text: str) -> None:
        """Set text content at a specific row and column."""
        self._widget.setItem(row, col, QTableWidgetItem(text))

    def get_item(self, row: int, col: int) -> str:
        """Get text content from a specific row and column."""
        item = self._widget.item(row, col)
        return item.text() if item else ""

    def add_row(self) -> None:
        """Add a new empty row to the table."""
        self._widget.insertRow(self.row_count)

    def remove_row(self, row: int) -> None:
        """Remove a row at the specified index."""
        self._widget.removeRow(row)

    def clear(self) -> None:
        """Clear all content in the table."""
        self._widget.clearContents()

    def clear_all(self) -> None:
        """Clear all content and headers in the table."""
        self._widget.clear()

    def set_row_count(self, rows: int) -> None:
        """Set the total number of rows in the table."""
        self._widget.setRowCount(rows)

    def set_col_count(self, cols: int) -> None:
        """Set the total number of columns in the table."""
        self._widget.setColumnCount(cols)

    def set_foreground(self, fg: str) -> None:
        """Set the foreground color of the table."""
        self.set_color(fg, self.bg)

    def set_background(self, bg: str) -> None:
        """Set the background color of the table."""
        self.set_color(self.fg, bg)

    def set_color(self, fg: str, bg: str) -> None:
        """Set both foreground and background colors."""
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")

    def on_cell_click(self, event: Callable[[Any], None]) -> None:
        """Set callback for when a table cell is clicked."""
        self._widget.cellClicked.connect(event)

    def set_font(self, font: str) -> None:
        """Set the font family of the table text."""
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")


class Slider(BaseWidget):
    def __init__(self, min_val: int = 0, max_val: int = 100, fg: str = "#ffffff", bg: str = "#000000"):
        super().__init__()
        self._widget = QSlider()
        self._widget.setRange(min_val, max_val)
        self.set_color(fg, bg)

    @property
    def fg(self) -> str:
        """Get the foreground color of the slider."""
        return self._widget.palette().color(QPalette.ColorRole.ButtonText).name()

    @property
    def bg(self) -> str:
        """Get the background color of the slider."""
        return self._widget.palette().color(QPalette.ColorRole.Button).name()

    @property
    def value(self) -> int:
        """Get current value of the slider."""
        return self._widget.value()

    @property
    def min_value(self) -> int:
        """Get minimum value of the slider."""
        return self._widget.minimum()

    @property
    def max_value(self) -> int:
        """Get maximum value of the slider."""
        return self._widget.maximum()

    def set_value(self, val: int) -> None:
        """Set current value of the slider."""
        self._widget.setValue(val)

    def set_range(self, min_val: int, max_val: int) -> None:
        """Set value range for the slider."""
        self._widget.setRange(min_val, max_val)

    def set_single_step(self, step: int) -> None:
        """Set single step increment."""
        self._widget.setSingleStep(step)

    def set_page_step(self, step: int) -> None:
        """Set page step increment."""
        self._widget.setPageStep(step)

    def set_foreground(self, fg: str) -> None:
        """Set the foreground color of the slider."""
        self.set_color(fg, self.bg)

    def set_background(self, bg: str) -> None:
        """Set the background color of the slider."""
        self.set_color(self.fg, bg)

    def set_color(self, fg: str, bg: str) -> None:
        """Set both foreground and background colors."""
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")

    def on_value_change(self, event: Callable[[Any], None]) -> None:
        """Set callback for value changed event."""
        self._widget.valueChanged.connect(event)

    def set_font(self, font: str) -> None:
        """Set the font family of the slider."""
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")


class Progress(BaseWidget):
    def __init__(self, fg: str = "#ffffff", bg: str = "#000000"):
        super().__init__()
        self._widget = QProgressBar()
        self.set_color(fg, bg)
    
    @property
    def fg(self) -> str:
        """Get the foreground color of the progress bar."""
        return self._widget.palette().color(QPalette.ColorRole.ButtonText).name()
    
    @property
    def bg(self) -> str:
        """Get the background color of the progress bar."""
        return self._widget.palette().color(QPalette.ColorRole.Button).name()

    @property
    def value(self) -> int:
        """Get the current value of the progress bar."""
        return self._widget.value()

    @property
    def maximum(self) -> int:
        """Get the maximum value of the progress bar."""
        return self._widget.maximum()

    @property
    def minimum(self) -> int:
        """Get the minimum value of the progress bar."""
        return self._widget.minimum()

    def set_value(self, value: int) -> None:
        """Set the current progress value."""
        self._widget.setValue(value)

    def set_range(self, min_val: int, max_val: int) -> None:
        """Set the minimum and maximum range."""
        self._widget.setMinimum(min_val)
        self._widget.setMaximum(max_val)

    def reset(self) -> None:
        """Reset the progress bar to zero."""
        self._widget.reset()

    def set_foreground(self, fg: str) -> None:
        """Set the foreground color of the progress bar."""
        self.set_color(fg, self.bg)

    def set_background(self, bg: str) -> None:
        """Set the background color of the progress bar."""
        self.set_color(self.fg, bg)

    def set_color(self, fg: str, bg: str) -> None:
        """Set both foreground and background colors."""
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")

    def on_value_change(self, event: Callable[[Any], None]) -> None:
        """Set callback for progress value changed."""
        self._widget.valueChanged.connect(event)

    def set_font(self, font: str) -> None:
        """Set the font family of the progress text."""
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")

class TextEdit(BaseWidget):
    def __init__(self, fg: str = "#ffffff", bg: str = "#000000"):
        super().__init__()
        self._widget = QTextEdit()
        self.set_color(fg, bg)
    
    @property
    def fg(self) -> str:
        """Get the foreground color of the text edit."""
        return self._widget.palette().color(QPalette.ColorRole.ButtonText).name()
    
    @property
    def bg(self) -> str:
        """Get the background color of the text edit."""
        return self._widget.palette().color(QPalette.ColorRole.Button).name()

    @property
    def text(self) -> str:
        """Get plain text content from the text edit."""
        return self._widget.toPlainText()

    def set_text(self, text: str) -> None:
        """Set plain text content of the text edit."""
        self._widget.setPlainText(text)

    def append(self, text: str) -> None:
        """Append text to the end of the text edit."""
        self._widget.append(text)

    def clear(self) -> None:
        """Clear all text content."""
        self._widget.clear()

    def set_foreground(self, fg: str) -> None:
        """Set the foreground color of the text."""
        self.set_color(fg, self.bg)

    def set_background(self, bg: str) -> None:
        """Set the background color of the text edit."""
        self.set_color(self.fg, bg)

    def set_color(self, fg: str, bg: str) -> None:
        """Set both foreground and background colors."""
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")

    def set_font(self, font: str) -> None:
        """Set the font family of the text."""
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")

class Canvas(BaseWidget):
    def __init__(self, fg: str = "#ffffff", bg: str = "#222222"):
        super().__init__()
        self._widget = QGraphicsView()
        self._scene = QGraphicsScene()
        self._widget.setScene(self._scene)
        self.set_color(fg, bg)

        self.pen = QPen(QColor(fg))
        self.brush = QBrush(QColor(fg))

    @property
    def fg(self) -> str:
        """Get the foreground color of the canvas."""
        return self.pen.color().name()

    @property
    def bg(self) -> str:
        """Get the background color of the canvas."""
        color = self._widget.backgroundBrush().color()
        return color.name() if color.isValid() else "#000000"

    def set_foreground(self, fg: str) -> None:
        """Set the foreground drawing color."""
        self.pen.setColor(QColor(fg))
        self.brush.setColor(QColor(fg))

    def set_background(self, bg: str) -> None:
        """Set the canvas background color."""
        self._widget.setBackgroundBrush(QBrush(QColor(bg)))

    def set_color(self, fg: str, bg: str) -> None:
        """Set both drawing color and background color."""
        self.set_foreground(fg)
        self.set_background(bg)

    def make_dot(self, x: float, y: float, size: float = 4) -> None:
        """Draw a dot at the given (x, y) position."""
        dot = QGraphicsEllipseItem(x - size/2, y - size/2, size, size)
        dot.setPen(self.pen)
        dot.setBrush(self.brush)
        self._scene.addItem(dot)

    def make_line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """Draw a line from (x1,y1) to (x2,y2)."""
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(self.pen)
        self._scene.addItem(line)

    def make_rect(self, x: float, y: float, w: float, h: float) -> None:
        """Draw a rectangle with top-left (x,y), width w, height h."""
        rect = QGraphicsRectItem(x, y, w, h)
        rect.setPen(self.pen)
        self._scene.addItem(rect)

    def make_circle(self, x: float, y: float, radius: float) -> None:
        """Draw a circle centered at (x,y) with given radius."""
        circle = QGraphicsEllipseItem(x - radius, y - radius, radius*2, radius*2)
        circle.setPen(self.pen)
        self._scene.addItem(circle)

    def clear(self) -> None:
        """Clear all drawings from the canvas."""
        self._scene.clear()

    def set_font(self, font: str) -> None:
        """Set font for text items (reserved for future use)."""
        pass