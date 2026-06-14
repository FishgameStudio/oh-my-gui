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
        self._app: Union[QGuiApplication, QApplication] = QApplication(argv)
        self._engine: Optional[QQmlApplicationEngine] = None
        # Call init_widget_mode in default way.
        self._isqml = False
        self.init_widget_mode()

        # Uniform style & enable 
        self._app.setStyle("Fusion")
        environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
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
            raise RuntimeError("Please call init_widget_mode() or init_qml_mode() first")
    
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