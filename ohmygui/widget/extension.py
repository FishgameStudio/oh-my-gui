from .base import BaseWidget
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from typing import Self, Any, Callable
from logging import info as _info
from PySide6.QtWidgets import (
    QSplashScreen, QSpinBox, QDoubleSpinBox, QDial, 
    QTreeWidget, QTreeWidgetItem
)
from PySide6.QtGui import QPalette, QColor

_info(f"Module {__name__} loaded")
# Widgets extension.

class Picture(BaseWidget):
    def __init__(self, path: str) -> None:
        super().__init__()
        self._widget: QPixmap | QSvgWidget = QPixmap(path)
    def load_picture(self, path: str) -> Self:
        self._widget = QPixmap(path) if not path.strip().endswith(".svg") else QSvgWidget(path)
        return self
    @property
    def is_svg(self) -> bool:
        return isinstance(self._widget, QSvgWidget)  

class Video(BaseWidget):
    def __init__(self, path: str) -> None:
        super().__init__()
        self._widget: QVideoWidget = QVideoWidget()
        self.player: QMediaPlayer  = QMediaPlayer()
        self.audio: QAudioOutput   = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self._widget)
    def play(self) -> Self:
        self.player.play()
        return self
    @property
    def audio_output(self) -> QAudioOutput:
        return self.audio
    @property
    def player_object(self) -> QMediaPlayer:
        return self.player
    @property
    def is_playing(self) -> bool:
        return self.player.isPlaying()
    def set_fullscreen(self, option: bool) -> Self:
        self._widget.setFullScreen(option)
        return self
    def set_loop(self, option: bool) -> Self:
        if option:
            self.player.setLoops(QMediaPlayer.Loops.Infinite)
        else:
            self.player.setLoops(QMediaPlayer.Loops.Once)
        return self
    def stop(self) -> Self:
        self.player.stop()
        return self

class SplashScreen(BaseWidget):
    """Wrap QSplashScreen for program startup splash window."""
    def __init__(self, pixmap: QPixmap, fg: str = "#ffffff", bg: str = "#000000"):
        super().__init__()
        _info("Initialize SplashScreen widget")
        self._pix: QPixmap = pixmap
        self._widget: QSplashScreen = QSplashScreen(self._pix)
        self.set_color(fg, bg)
        _info("SplashScreen instance created successfully")

    @property
    def fg(self) -> str:
        """Get foreground text color of splash screen message."""
        color = self._widget.palette().color(QPalette.ColorRole.WindowText)
        return color.name()

    @property
    def bg(self) -> str:
        """Get splash background color (fallback to passed bg)."""
        return self._widget.palette().color(QPalette.ColorRole.Window).name()

    def set_color(self, fg: str, bg: str) -> Self:
        pal = self._widget.palette()
        pal.setColor(QPalette.ColorRole.WindowText, QColor(fg))
        pal.setColor(QPalette.ColorRole.Window, QColor(bg))
        self._widget.setPalette(pal)
        _info(f"SplashScreen set color fg={fg}, bg={bg}")
        return self

    def set_foreground(self, fg: str) -> Self:
        self.set_color(fg, self.bg)
        _info(f"SplashScreen update foreground to {fg}")
        return self

    def set_background(self, bg: str) -> Self:
        self.set_color(self.fg, bg)
        _info(f"SplashScreen update background to {bg}")
        return self

    def show_message(self, msg: str, align: int = 64) -> Self:
        """Show loading text message on splash screen."""
        _info(f"SplashScreen display message: {msg}")
        self._widget.showMessage(msg, align)
        return self

    def finish(self, main_win: Any) -> Self:
        """Close splash after main window ready."""
        _info("SplashScreen finish loading, attach to main window")
        self._widget.finish(main_win._widget)
        return self

    def show(self) -> Self:
        _info("SplashScreen display")
        self._widget.show()
        return self

    def close(self) -> Self:
        _info("SplashScreen close")
        self._widget.close()
        return self

    def set_font(self, font: str) -> Self:
        _info(f"SplashScreen set font family {font}")
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg};")
        return self


class IntegerEntry(BaseWidget):
    """Wrapped QSpinBox integer input box."""
    def __init__(
        self,
        min_val: int = 0,
        max_val: int = 9999,
        default: int = 0,
        fg: str = "#ffffff",
        bg: str = "#000000"
    ) -> None:
        super().__init__()
        _info("Initialize IntegerEntry (QSpinBox)")
        self._widget: QSpinBox = QSpinBox()
        self._widget.setRange(min_val, max_val)
        self._widget.setValue(default)
        self.set_color(fg, bg)
        _info(f"IntegerEntry range [{min_val}, {max_val}], default={default}")

    @property
    def fg(self) -> str:
        return self._widget.palette().color(QPalette.ColorRole.Text).name()

    @property
    def bg(self) -> str:
        return self._widget.palette().color(QPalette.ColorRole.Base).name()

    @property
    def value(self) -> int:
        return self._widget.value()

    @property
    def min_value(self) -> int:
        return self._widget.minimum()

    @property
    def max_value(self) -> int:
        return self._widget.maximum()

    def set_range(self, min_val: int, max_val: int) -> Self:
        _info(f"IntegerEntry update range min={min_val}, max={max_val}")
        self._widget.setRange(min_val, max_val)
        return self

    def set_value(self, val: int) -> Self:
        _info(f"IntegerEntry set value {val}")
        self._widget.setValue(val)
        return self

    def set_step(self, step: int) -> Self:
        _info(f"IntegerEntry single step set to {step}")
        self._widget.setSingleStep(step)
        return self

    def set_foreground(self, fg: str) -> Self:
        self.set_color(fg, self.bg)
        _info(f"IntegerEntry foreground color {fg}")
        return self

    def set_background(self, bg: str) -> Self:
        self.set_color(self.fg, bg)
        _info(f"IntegerEntry background color {bg}")
        return self

    def set_color(self, fg: str, bg: str) -> Self:
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")
        _info(f"IntegerEntry set color fg={fg}, bg={bg}")
        return self

    def on_value_change(self, event: Callable[[int], None]) -> Self:
        _info("IntegerEntry bind valueChanged callback")
        self._widget.valueChanged.connect(event)
        return self

    def set_font(self, font: str) -> Self:
        _info(f"IntegerEntry font family {font}")
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")
        return self


class DoubleEntry(BaseWidget):
    """Wrapped QDoubleSpinBox floating point input box."""
    def __init__(
        self,
        min_val: float = 0.0,
        max_val: float = 9999.0,
        default: float = 0.0,
        decimals: int = 2,
        fg: str = "#ffffff",
        bg: str = "#000000"
    ) -> None:
        super().__init__()
        _info("Initialize DoubleEntry (QDoubleSpinBox)")
        self._widget: QDoubleSpinBox = QDoubleSpinBox()
        self._widget.setDecimals(decimals)
        self._widget.setRange(min_val, max_val)
        self._widget.setValue(default)
        self.set_color(fg, bg)
        _info(f"DoubleEntry range [{min_val}, {max_val}], decimals={decimals}, default={default}")

    @property
    def fg(self) -> str:
        return self._widget.palette().color(QPalette.ColorRole.Text).name()

    @property
    def bg(self) -> str:
        return self._widget.palette().color(QPalette.ColorRole.Base).name()

    @property
    def value(self) -> float:
        return self._widget.value()

    @property
    def min_value(self) -> float:
        return self._widget.minimum()

    @property
    def max_value(self) -> float:
        return self._widget.maximum()

    @property
    def decimals(self) -> int:
        return self._widget.decimals()

    def set_range(self, min_val: float, max_val: float) -> Self:
        _info(f"DoubleEntry update range min={min_val}, max={max_val}")
        self._widget.setRange(min_val, max_val)
        return self

    def set_value(self, val: float) -> Self:
        _info(f"DoubleEntry set value {val}")
        self._widget.setValue(val)
        return self

    def set_decimals(self, digits: int) -> Self:
        _info(f"DoubleEntry decimal digits set to {digits}")
        self._widget.setDecimals(digits)
        return self

    def set_step(self, step: float) -> Self:
        _info(f"DoubleEntry single step set to {step}")
        self._widget.setSingleStep(step)
        return self

    def set_foreground(self, fg: str) -> Self:
        self.set_color(fg, self.bg)
        _info(f"DoubleEntry foreground color {fg}")
        return self

    def set_background(self, bg: str) -> Self:
        self.set_color(self.fg, bg)
        _info(f"DoubleEntry background color {bg}")
        return self

    def set_color(self, fg: str, bg: str) -> Self:
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")
        _info(f"DoubleEntry set color fg={fg}, bg={bg}")
        return self

    def on_value_change(self, event: Callable[[float], None]) -> Self:
        _info("DoubleEntry bind valueChanged callback")
        self._widget.valueChanged.connect(event)
        return self

    def set_font(self, font: str) -> Self:
        _info(f"DoubleEntry font family {font}")
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")
        return self


class Dial(BaseWidget):
    """Wrapped QDial circular rotary dial control."""
    def __init__(
        self,
        min_val: int = 0,
        max_val: int = 100,
        default: int = 0,
        fg: str = "#ffffff",
        bg: str = "#000000"
    ) -> None:
        super().__init__()
        _info("Initialize Dial rotary controller")
        self._widget: QDial = QDial()
        self._widget.setRange(min_val, max_val)
        self._widget.setValue(default)
        self.set_color(fg, bg)
        _info(f"Dial range [{min_val}, {max_val}], initial value={default}")

    @property
    def fg(self) -> str:
        return self._widget.palette().color(QPalette.ColorRole.Text).name()

    @property
    def bg(self) -> str:
        return self._widget.palette().color(QPalette.ColorRole.Base).name()

    @property
    def value(self) -> int:
        return self._widget.value()

    @property
    def min_value(self) -> int:
        return self._widget.minimum()

    @property
    def max_value(self) -> int:
        return self._widget.maximum()

    def set_range(self, min_val: int, max_val: int) -> Self:
        _info(f"Dial update range min={min_val}, max={max_val}")
        self._widget.setRange(min_val, max_val)
        return self

    def set_value(self, val: int) -> Self:
        _info(f"Dial set rotation value {val}")
        self._widget.setValue(val)
        return self

    def set_step(self, step: int) -> Self:
        _info(f"Dial single step increment {step}")
        self._widget.setSingleStep(step)
        return self

    def show_ticks(self, enable: bool = True) -> Self:
        _info(f"Dial tick marks visible={enable}")
        self._widget.setNotchesVisible(enable)
        return self

    def set_foreground(self, fg: str) -> Self:
        self.set_color(fg, self.bg)
        _info(f"Dial foreground color {fg}")
        return self

    def set_background(self, bg: str) -> Self:
        self.set_color(self.fg, bg)
        _info(f"Dial background color {bg}")
        return self

    def set_color(self, fg: str, bg: str) -> Self:
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")
        _info(f"Dial set color fg={fg}, bg={bg}")
        return self

    def on_value_change(self, event: Callable[[int], None]) -> Self:
        _info("Dial bind valueChanged rotation callback")
        self._widget.valueChanged.connect(event)
        return self

    def set_font(self, font: str) -> Self:
        _info(f"Dial font family {font}")
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")
        return self
    
class Tree(BaseWidget):
    def __init__(self, fg: str = "#ffffff", bg: str = "#000000") -> None:
        super().__init__()
        _info("Initialize TreeWidget component")
        self._widget: QTreeWidget = QTreeWidget()
        self._widget.setColumnCount(1)
        self.set_color(fg, bg)
        _info("TreeWidget instance created, single column enabled by default")

    @property
    def fg(self) -> str:
        """Get tree item foreground text color."""
        return self._widget.palette().color(QPalette.ColorRole.Text).name()

    @property
    def bg(self) -> str:
        """Get tree view background color."""
        return self._widget.palette().color(QPalette.ColorRole.Base).name()

    @property
    def current_text(self) -> str:
        """Get text of currently selected tree item (first column)."""
        item: QTreeWidgetItem = self._widget.currentItem()
        return item.text(0) if item else ""

    @property
    def current_item(self) -> QTreeWidgetItem | None:
        """Get raw selected QTreeWidgetItem object."""
        return self._widget.currentItem()

    def set_column_count(self, count: int) -> Self:
        """Set number of tree columns."""
        _info(f"TreeWidget set column count = {count}")
        self._widget.setColumnCount(count)
        return self

    def set_header_labels(self, labels: list[str]) -> Self:
        """Set horizontal header text for each column."""
        _info(f"TreeWidget set header labels: {labels}")
        self._widget.setHeaderLabels(labels)
        return self

    def add_root_item(self, text: str) -> Self:
        """Add top-level root tree node."""
        _info(f"TreeWidget add root item: {text}")
        item = QTreeWidgetItem([text])
        self._widget.addTopLevelItem(item)
        return self

    def add_child_item(self, parent_item: QTreeWidgetItem, text: str) -> Self:
        """Add child node under specified parent item."""
        _info(f"TreeWidget add child item '{text}' to parent node")
        child = QTreeWidgetItem([text])
        parent_item.addChild(child)
        return self

    def clear_all(self) -> Self:
        """Remove all tree items completely."""
        _info("TreeWidget clear all nodes")
        self._widget.clear()
        return self

    def expand_all(self) -> Self:
        """Expand every collapsible tree node."""
        _info("TreeWidget expand all items")
        self._widget.expandAll()
        return self

    def collapse_all(self) -> Self:
        """Collapse every tree node."""
        _info("TreeWidget collapse all items")
        self._widget.collapseAll()
        return self

    def set_foreground(self, fg: str) -> Self:
        """Override item text color."""
        self.set_color(fg, self.bg)
        _info(f"TreeWidget update foreground color {fg}")
        return self

    def set_background(self, bg: str) -> Self:
        """Override tree background color."""
        self.set_color(self.fg, bg)
        _info(f"TreeWidget update background color {bg}")
        return self

    def set_color(self, fg: str, bg: str) -> Self:
        """Set both foreground text and background color."""
        self._widget.setStyleSheet(f"color: {fg}; background-color: {bg};")
        _info(f"TreeWidget set color fg={fg}, bg={bg}")
        return self

    def on_item_click(self, event: Callable[[QTreeWidgetItem, int], None]) -> Self:
        """Bind callback for single click on tree item, passes (item, column)."""
        _info("TreeWidget bind itemClicked event callback")
        self._widget.itemClicked.connect(event)
        return self

    def on_item_double_click(self, event: Callable[[QTreeWidgetItem, int], None]) -> Self:
        """Bind callback for double click on tree item."""
        _info("TreeWidget bind itemDoubleClicked event callback")
        self._widget.itemDoubleClicked.connect(event)
        return self

    def set_font(self, font: str) -> Self:
        """Set global font family for all tree items."""
        _info(f"TreeWidget set font family = {font}")
        self._widget.setStyleSheet(f"font-family: {font}; color: {self.fg}; background-color: {self.bg};")
        return self
    

    