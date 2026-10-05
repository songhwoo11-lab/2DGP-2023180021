"""Sequential animation viewer for the Sonic sprite sheet."""

from dataclasses import dataclass
from pathlib import Path
import os

from pico2d import *


BASE_DIR = Path(__file__).resolve().parent
SPRITE_PATH = BASE_DIR / "sonic-sprite.png"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCALE = 4
FRAME_INTERVAL = 0.1
REPEAT_COUNT = 5
PAUSE_DURATION = 1.0


@dataclass(frozen=True)
class Frame:
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class Animation:
    name: str
    frames: tuple[Frame, ...]
    moves: bool


ANIMATIONS: tuple[Animation, ...] = ()
