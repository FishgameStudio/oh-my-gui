import logging

from .base import BaseWidget
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from typing import Self

logging.info(f"Module {__name__} loaded")
# Widgets extension.

from .base import BaseWidget
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from typing import Self

class Picture(BaseWidget):
    def __init__(self, path: str):
        super().__init__()
        self._widget: QPixmap | QSvgWidget = QPixmap(path)
    def load_picture(self, path: str) -> Self:
        self._widget = QPixmap(path) if not path.strip().endswith(".svg") else QSvgWidget(path)
        return self
    @property
    def is_svg(self) -> bool:
        return isinstance(self._widget, QSvgWidget)  

class Video(BaseWidget):
    def __init__(self, path):
        super().__init__()
        self._widget = QVideoWidget()
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self._widget)
    def play(self) -> Self:
        self.player.play()
        return self
    @property
    def audio_output(self):
        return self.audio
    @property
    def player_object(self):
        return self.player
    @property
    def is_playing(self) -> bool:
        return self.player.isPlaying()
    def set_fullscreen(self, option: bool) -> Self:
        self._widget.setFullScreen(option)
        return self
    def set_loop(self, option: bool) -> Self:
        if option:
            self.player.setLoops(QMediaPlayer.Loops.Infinite)
        else:
            self.player.setLoops(QMediaPlayer.Loops.Once)
        return self
    def stop(self) -> Self:
        self.player.stop()
        return self
    