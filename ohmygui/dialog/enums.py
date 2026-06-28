# Standard icons & buttons enumeration.
from typing import TypeAlias


from PySide6.QtWidgets import QMessageBox
from logging import info, warning, error, critical

info(msg=f"Module {__name__} loaded")

Icon: TypeAlias = QMessageBox.Icon
Button: TypeAlias = QMessageBox.StandardButton

