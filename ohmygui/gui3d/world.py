# World - Manage the blocks.

from typing import Callable, Any, Self
from .block import CubeBlock
from .types import xyz_int

def singleton(cls) -> Callable[..., Any]:
    instances: dict[Any, Any] = {}
    def get_instance(*args, **kwargs) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class World:
    def __init__(self, blocks: list[list[list[CubeBlock | None]]]) -> None:
        # NOTE: list[list[list[CubeBlock]]] => z,y,z
        # `None` means no block at the pos.
        self.blocks = blocks
    def __getitem__(self, xyz: xyz_int) -> CubeBlock | None:
        return self.blocks[xyz[0]][xyz[1]][xyz[2]]
    def __setitem__(self, xyz: xyz_int, block: CubeBlock) -> CubeBlock | None:
        origin = self[xyz]
        self.blocks[xyz[0]][xyz[1]][xyz[2]] = block
        return origin
    def __delitem__(self, xyz) -> CubeBlock | None:
        origin = self[xyz]
        self.blocks[xyz[0]][xyz[1]][xyz[2]] = None
        return origin
