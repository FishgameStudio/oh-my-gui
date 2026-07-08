# A Basic cube block class.


from .base_entity import BaseEntity
from typing import Self
from .types import xyz, lwh
from PySide6.Qt3DCore import Qt3DCore as Core
from PySide6.QtGui import QVector3D
from PySide6.Qt3DExtras import Qt3DExtras as Extras
from PySide6.Qt3DRender import Qt3DRender as Core
from PySide6.Qt3DLogic import Qt3DLogic as Logic

SIDE_LENGTH = 2

class CubeBlock(BaseEntity):
    def __init__(self, pos: xyz, side_len: float = SIDE_LENGTH, color_rgb: str = "") -> None:
        """
        The param `size` is for the length, width and height (in meters).   
        """
        super().__init__(pos)
        ### Set Mesh ###
        self._mesh = Extras.QCuboidMesh()
        self._mesh.setXExtent(side_len)
        self._mesh.setYExtent(side_len)
        self._mesh.setZExtent(side_len)
        ### Set Color ###
        self._mat = Extras.QPhongMaterial()
        self._mat.setDiffuse(color_rgb)

        self._entity.addComponent(self._mesh)
        self._entity.addComponent(self._mat)

    @property
    def size(self) -> float:
        """The size of the block."""
        return SIDE_LENGTH * SIDE_LENGTH * SIDE_LENGTH
