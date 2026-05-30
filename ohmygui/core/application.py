# Main application class.

from PySide6.QtWidgets import QApplication

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance()

@singleton
class Application:
    def __init__(self) -> None:
        self._app = QApplication()
    def run(self) -> int:
        """Run the application & return error code."""
        return self._app.exec()

App = Application