# Main application class.

from sys import argv
import sys
from PySide6.QtWidgets import QApplication
from ..widget.event import Event
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from os.path import exists
from os import environ
from typing import Any, Callable, Self, TypeAlias, Never
from logging import info, warning, error, critical
from .oms import convert_oms_to_qss as _convert
from ..oml import convert_oml_to_qml as _convert_oml

def singleton(cls) -> Callable[..., Any]:
    instances: dict[Any, Any] = {}
    def get_instance(*args, **kwargs) -> Any:
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
        self._app: QGuiApplication | QApplication = QApplication(argv)
        self._engine: QQmlApplicationEngine | None = None
        # Call init_widget_mode in default way.
        self._isqml: bool = False
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
        ec: int = self._app.exec()
        info(f"Application exit with code {ec}")
        return ec
    def run_quit(self) -> Never:
        """Run the application & return error code."""
        info("Application begin running")
        if self._app is None:
            critical("self._app does not initialize QML or widget mode (is None)")
            raise RuntimeError("Please call init_widget_mode() or init_qml_mode() first")
        ec: int = self._app.exec()
        info(f"Application exit with code {ec}")
        sys.exit(ec)
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
        try:
            with open(path, "r", encoding="utf-8") as f:
                qss: str = f.read()
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
        try:
            with open(path, "r", encoding="utf-8") as f:
                oms: str = f.read()
            info("OMS has been read")
        except FileNotFoundError as e:
            error(f"OMS file {path} not found")
            raise FileNotFoundError(f"OMS file not found: {e.filename}")
        except PermissionError as e:
            error("OMS file permission denied")
            raise PermissionError(f"OMS file permission denied: {e.filename}")
        self.load_oms_string(oms)
        return self
    def load_oml_from(self, path: str) -> Self:
        """Load an OML file."""
        if not path.endswith(".oml"):
            warning(f"Perhaps not OML file: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                oml: str = f.read()
            info("OML has been read")
        except FileNotFoundError as e:
            error(f"OML file {path} not found")
            raise FileNotFoundError(f"OML file not found: {e.filename}")
        except PermissionError as e:
            error("OML file permission denied")
            raise PermissionError(f"OML file permission denied: {e.filename}")
        self.load_qml_string(_convert_oml(oml))
        return self
    def load_oml_string(self, oml: str) -> Self:
        """Load an OML string."""
        self.load_qml_string(_convert_oml(oml))
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
    def load_qml_string(self, qml: str) -> Self:
        """Load a string of QML."""
        info(f"Application begin loading QML string {qml[0:30]}...")
        self._engine = QQmlApplicationEngine()
        comp: QQmlComponent = QQmlComponent(self._engine)
        comp.setData(qml.encode("utf-8"), "")
        info(f"Start compiling QQmlComponent object {comp}")
        # Wait for async compiling of component
        def on_ready() -> None:
            if comp.status() == QQmlComponent.Status.Ready:
                comp.create()
            else:
                # Print compiling errors.
                for e in comp.errors():
                    error(e.toString())

        comp.statusChanged.connect(on_ready)
        return self
      

# Alias
App: TypeAlias = Application # pyright: ignore