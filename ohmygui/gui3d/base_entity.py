# Base 3D Entity class

from PySide6.Qt3DCore import Qt3DCore as Core
from PySide6.Qt3DExtras import Qt3DExtras as Extras
from PySide6.Qt3DRender import Qt3DRender as Render
from PySide6.QtGui import QVector3D
from logging import info, warning
from .types import xyz, lwh
from typing import Self

class BaseEntity:
    def __init__(self, pos: xyz) -> None:
        info(f"BaseEntity {self} enters __init__")
        
        self._entity = Core.QEntity()
        self._trans = Core.QTransform()
        self._trans.setTranslation(QVector3D(*pos))
        self._entity.addComponent(self._trans)
        info(f"BaseEntity object {self} placed at xyz {pos}")
        info(f"BaseEntity {self} leaves __init__")
    @property
    def xyz(self) -> xyz:
        return (self._trans.translation().x(), self._trans.translation().y(), self._trans.translation().z())
    def set_xyz(self, xyz: xyz) -> Self:
        """Set the X Y Z"""
        info(f"BaseEntity object {self} replaced at xyz {xyz}")
        self._trans.setTranslation(QVector3D(*xyz))
        return self
    @property
    def native(self) -> Core.QEntity:
        return self._entity