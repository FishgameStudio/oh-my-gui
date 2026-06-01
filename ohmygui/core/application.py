# Main application class.

from sys import argv
from PySide6.QtWidgets import QApplication
from ..widget.event import Event

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
        self._app = QApplication(argv)
    def run(self) -> int:
        """Run the application & return error code."""
        return self._app.exec()
    def on_quit(self, event: Event) -> None:
        """Set the callback for when the application is quitting."""
        self._app.aboutToQuit.connect(event.get_func)

# Alias
App = Application