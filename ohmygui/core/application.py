# Main application class.

from sys import argv
from PySide6.QtWidgets import QApplication
from ..widget.event import Event
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from os.path import exists
from os import environ
from typing import Optional, Union, Self
from logging import info, warning, error, critical
from .oms import convert_oms_to_qss as _convert

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Application:
    def __init__(self) -> None:
        info("Application enter __init__")
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        # Enable high API scaling & log debug plugin.
        environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
        environ["QT_DEBUG_PLUGINS"] = "1"

        # Instantiation.
        self._app: Union[QGuiApplication, QApplication] = QApplication(argv)
        self._engine: Optional[QQmlApplicationEngine] = None
        # Call init_widget_mode in default way.
        self._isqml = False
        self.init_widget_mode()

        # Uniform style
        self._app.setStyle("Fusion")
        self._app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        info("Application leave __init__")

    def init_widget_mode(self) -> Self:
        """Initialize with Widget mode(QApplication)."""
        info("Application begin initializing widget mode")
        if not self._isqml: return self
        if self._app is None:
            self._app = QApplication(argv)
        self._isqml = False
        info("Application finish initializing widget mode")
        return self
    def init_qml_mode(self) -> Self:
        """Initialize with QML mode(QGuiApplication)."""
        info("Application begin initializing QML mode")
        if self._isqml: return self
        if self._app is None:
            self._app = QGuiApplication(argv)
        self._isqml = True
        info("Application finish initializing QML mode")
        return self

    def run(self) -> int:
        """Run the application & return error code."""
        info("Application begin running")
        if self._app is None:
            critical("self._app does not initialize QML or widget mode (is None)")
            raise RuntimeError("Please call init_widget_mode() or init_qml_mode() first")
        ec = self._app.exec()
        info(f"Application exit with code {ec}")
        return ec
    def on_quit(self, event: Event) -> None:
        """Set the callback for when the application is quitting."""
        info("bind event on_quit")
        if self._app is not None: 
            self._app.aboutToQuit.connect(event.get_func)
        else:
            critical("self._app does not initialize QML or widget mode (is None)")
            raise RuntimeError("Please call init_widget_mode() or init_qml_mode() first")
        
    def load_style_from(self, path: str) -> Self:
        """Load style sheet from a QSS file."""
        info(f"load QSS from file {path}")
        if not path.endswith(".qss"):
            warning(f"Perhaps not qss file: {path}")
        qss: str
        try:
            with open(path, "r", encoding="utf-8") as f:
                qss = f.read()
            info("QSS has been read")
        except FileNotFoundError as e:
            error(f"QSS file {path} not found")
            raise FileNotFoundError(f"QSS file not found: {e.filename}")
        except PermissionError as e:
            error("QSS file permission denied")
            raise PermissionError(f"QSS file permission denied: {e.filename}")
        if isinstance(self._app, QApplication):
            self._app.setStyleSheet(qss)
        else:
            error("Cannot load stylesheet in QML mode")
        
        return self
    def load_style_string(self, qss: str) -> Self:
        """Load style sheet from a string."""
        if isinstance(self._app, QApplication):
            self._app.setStyleSheet(qss)
        else:
            error("Cannot load stylesheet in QML mode")
        return self
    def load_oms_string(self, oms: str) -> Self:
        """Load a OMS (Oh My Stylesheet) string"""
        self.load_style_string(_convert(oms))
        return self
    def load_oms_from(self, path: str) -> Self:
        """Load a OMS (Oh My Stylesheet) file"""
        if not path.endswith(".oms"):
            warning(f"Perhaps not qss file: {path}")
        oms: str
        try:
            with open(path, "r", encoding="utf-8") as f:
                oms = f.read()
            info("OMS has been read")
        except FileNotFoundError as e:
            error(f"OMS file {path} not found")
            raise FileNotFoundError(f"OMS file not found: {e.filename}")
        except PermissionError as e:
            error("OMS file permission denied")
            raise PermissionError(f"OMS file permission denied: {e.filename}")
        self.load_oms_string(oms)
        return self
    @property
    def is_qml_mode(self) -> bool:
        info("access attribute _isqml")
        return self._isqml

    ###################### QML ######################
    def load_qml_from(self, path: str) -> Self:
        info(f"Application begin loading QML with path {path}")
        if not exists(path):
            error(f"QML file does not exist: {path}")
            raise FileNotFoundError(f"QML file not found: {path}")
        
        # Switch to QML mode
        if not isinstance(self._app, QGuiApplication):
            self.init_qml_mode()
        self._engine = QQmlApplicationEngine()
        self._engine.load(path)
        if self._engine is None or not self._engine.rootObjects():
            error(f"Failed to load from QML: {path}")
            raise RuntimeError("Failed to load QML")
        return self
        

# Alias
App = Application