# 3D Window.

from PySide6.QtCore import QSize, QObject, QRect as _QRect, Qt as _Qt
from PySide6.QtGui import QResizeEvent, QCloseEvent, QPixmap, QVector3D
from typing import Callable, Any, Annotated, Self, TypeAlias
from logging import info, error
from enum import Enum as _Enum
from PySide6.Qt3DCore import Qt3DCore as Core
from PySide6.Qt3DExtras import Qt3DExtras as Extras
from PySide6.Qt3DRender import Qt3DRender as Render
from .base_entity import BaseEntity
from .types import xyz, lwh
from weakref import finalize


Size_Type: TypeAlias = tuple[int, int]
Direction: TypeAlias = Size_Type

LinearSpeed: TypeAlias = Annotated[float, "0.1 ~ 20"]

class WinSize(_Enum):
    Maximum       = 0
    Minimum       = 1
    Regular       = 2
    Left          = 3
    Right         = 4
    Top           = 5
    Bottom        = 6

class Window3D:
    def __init__(self, title: str = "", size: Size_Type = (1000, 800), /, *, light_pos: xyz = (0, 0, 0), light_color: str = "#ffffff") -> None:
        info("Window3D enter __init__")
        self._win: Extras.Qt3DWindow = Extras.Qt3DWindow()
        self._win.setTitle(title)
        self._win.resize(*size)
        self._root = Core.QEntity()
        # Critical: bind the scene root so Qt3D actually renders entities.
        self._win.setRootEntity(self._root)

        self._cam = self._win.camera()
        # Create controller after the window is shown (input wiring depends on window lifecycle).
        self._cam_ctrl: Extras.QOrbitCameraController | None = None
        self._entities: list[BaseEntity] = []

        # Set the world light.
        self._light_entity = Core.QEntity()
        self._light = Render.QDirectionalLight()
        self._light.setWorldDirection(QVector3D(*light_pos))
        self._light.setColor(light_color)
        self._light_entity.addComponent(self._light)

        self._dtor = finalize(self, self.__destruct__)
        info("Window3D exit __init__")

    @property
    def root_entity(self) -> Core.QEntity:
        return self._root
    @property
    def camera(self) -> Render.QCamera:
        return self._cam
    @property
    def camera_pos(self) -> xyz:
        vector = self._cam.position()
        return (vector.x(), vector.y(), vector.z())
    @property
    def camera_facing(self) -> xyz:
        vc = self._cam.viewCenter()
        return (vc.x(), vc.y(), vc.z())
    @property
    def light(self) -> Render.QDirectionalLight:
        return self._light
    
    
    @property
    def x(self) -> int: return self._win.x()
    @property
    def y(self) -> int: return self._win.y()
    @property
    def w(self) -> int: return self._win.width()
    @property
    def h(self) -> int: return self._win.height()

    def set_size(self, size: Size_Type) -> Self:
        """Set the size of the window."""
        info(f"set Window size as {size}")
        self._win.resize(*size)
        return self

    def set_position(self, pos: Direction) -> Self:
        """Set the position of the window on the screen."""
        info(f"set pos as {pos}")
        self._win.setGeometry(*pos, self.w, self.h)
        return self
    
    def set_icon(self, ico_path: str) -> Self:
        """Set the icon of the window."""
        try:
            self._win.setIcon(QPixmap(ico_path))
        except FileNotFoundError:
            error(f"Icon file not found: {ico_path}")
        except PermissionError:
            error(f"Icon file permission denied: {ico_path}")
        except Exception as e:
            error(f"Except when setting window icon: {e}")
        return self
    @property
    def size(self) -> Size_Type:
        """Returns the window size."""
        return (self.w, self.h)

    def set_camera_pos(self, pos: xyz) -> Self:
        self._cam.setPosition(QVector3D(*pos))
        return self
    def set_camera_facing(self, pos: xyz) -> Self:
        self._cam.setViewCenter(QVector3D(*pos))
        return self

    def fix_size(self) -> Self:
        """Fix the size."""
        info("Window size fixed")
        self._win.setMinimumSize(QSize(*self.size))
        self._win.setMaximumSize(QSize(*self.size))
        return self

    def unfix_size(self) -> Self:
        """Unfix the size."""
        info("Window size unfixed")
        # Unlock the size scope.
        self._win.setMinimumSize(QSize(0, 0))
        self._win.setMaximumSize(QSize(16777215, 16777215))
        return self
    def set_parent(self, parent: 'Window3D') -> Self:
        info(f"Window parent set as {parent}")
        self._win.setParent(parent.native)
        return self
    @property
    def parent(self) -> QObject | None:
        return self._win.parent()
    @property
    def children(self) -> list[QObject]:
        return self._win.children()
        
    def on_resize(self, callback: Callable[[int, int], None]) -> Self: 
        """
        Bind callback when resizing window.
        The `int, int` params are the width & height of the window.
        """
        original_event: Callable[[QResizeEvent], None] = self._win.resizeEvent
        # Wrap the event.
        def wrapped(event: QResizeEvent) -> None:
            # Execute origin event
            original_event(event)
            callback(self.w, self.h)
        self._win.resizeEvent = wrapped
        return self

    def set_camera_linear_speed(self, speed: LinearSpeed) -> Self:
        # Controller may not be created until show()
        if self._cam_ctrl is None:
            self.show()
        assert self._cam_ctrl is not None
        self._cam_ctrl.setLinearSpeed(speed)
        return self

    def set_camera_look_speed(self, speed: float = 180) -> Self:
        if self._cam_ctrl is None:
            self.show()
        assert self._cam_ctrl is not None
        self._cam_ctrl.setLookSpeed(speed)
        return self

    def set_light_pos(self, pos: xyz) -> Self:
        """Set the position where the light facing to."""
        self._light.setWorldDirection(QVector3D(*pos))
        return self
    @property
    def light_pos(self) -> xyz:
        v = self._light.worldDirection()
        return (v.x(), v.y(), v.z())
    
    def set_light_color(self, color: str) -> Self:
        """Set the color of the light"""
        self._light.setColor(color)
        return self
    @property
    def light_color(self) -> str:
        color = self._light.color()
        return f"#{color.red()}{color.green()}{color.blue()}"

    def show(self) -> Self:
        """Show the window."""
        self._win.show()
        # (Re)create controller after the window is visible to ensure input events are wired.
        if self._cam_ctrl is None:
            self._cam_ctrl = Extras.QOrbitCameraController(self._cam)
            self._cam_ctrl.setParent(self._root)
        return self

    def hide(self) -> Self:
        """Hide the window."""
        self._win.hide()
        return self
    
    def add_entities(self, entities: list[BaseEntity]) -> Self:
        """Add some entities."""
        self._entities += entities
        for entity in entities:
            entity.native.setParent(self._root)
        return self

    def close(self) -> Self:
        """Close the window."""
        self._win.close()
        return self
    def on_close(self, event: Callable[[Any], None]) -> Self:
        """Set the callback for when the window is closed."""
        original: Callable[[QCloseEvent], None] = self._win.closeEvent
        def wrapped(evt: QCloseEvent) -> None:
            event(None)
            original(evt)
        self._win.closeEvent = wrapped
        return self

    def destroy(self) -> Self:
        """Destory this window."""
        self._win.destroy()
        return self
    
    def set_frameless(self, option: bool) -> Self:
        """Set the window frameless."""
        self._win.setFlags(_Qt.WindowType.FramelessWindowHint)
        return self
    def snap(self, layout: WinSize) -> Self:
        """Set snaping mode"""
        screen_rect = self._win.screen().availableGeometry()
        target_rect: _QRect = _QRect()
        match layout:
            case WinSize.Maximum:
                target_rect = _QRect(
                    screen_rect.left(),
                    screen_rect.top(),
                    screen_rect.width(), 
                    screen_rect.height()
                )
            case WinSize.Minimum:
                target_rect = _QRect(
                    0, 0, 0, 0
                )
            case WinSize.Left:
                half_w: int = screen_rect.width() // 2
                target_rect = _QRect(
                    screen_rect.left(),
                    screen_rect.top(),
                    half_w,
                    screen_rect.height()
                )
            case WinSize.Right:
                half_w = screen_rect.width() // 2
                target_rect = _QRect(
                    half_w, 
                    screen_rect.top(),
                    half_w,
                    screen_rect.height()
                )
            case WinSize.Top:
                half_h = screen_rect.height() // 2
                target_rect = _QRect(
                    screen_rect.left(),  
                    screen_rect.top(),
                    screen_rect.width(),
                    half_h
                )
            case WinSize.Bottom:
                half_h = screen_rect.height() // 2
                target_rect = _QRect(
                    screen_rect.left(),  
                    half_h,
                    screen_rect.width(),
                    half_h
                )
        self._win.setGeometry(target_rect)
        return self

    @property
    def native(self) -> Extras.Qt3DWindow:
        """Native escape port: Get the underlying PySide6 control"""
        return self._win
    
    def __destruct__(self) -> None:
        self._entities.clear()
    