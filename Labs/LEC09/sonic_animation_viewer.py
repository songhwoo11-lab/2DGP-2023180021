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


ANIMATIONS: tuple[Animation, ...] = (
    Animation(
        "대기·자세 전환",
        (
            Frame(1, 39, 29, 39),
            Frame(31, 40, 26, 38),
            Frame(58, 39, 28, 39),
            Frame(86, 40, 30, 38),
            Frame(118, 40, 30, 38),
            Frame(150, 40, 30, 38),
            Frame(182, 40, 29, 38),
            Frame(211, 39, 29, 38),
            Frame(240, 39, 29, 38),
            Frame(270, 45, 24, 32),
            Frame(302, 51, 29, 26),
        ),
        moves=False,
    ),
    Animation(
        "달리기",
        (
            Frame(8, 80, 26, 37),
            Frame(37, 80, 27, 37),
            Frame(65, 80, 31, 38),
            Frame(97, 80, 37, 37),
            Frame(135, 80, 32, 35),
            Frame(170, 79, 32, 38),
            Frame(206, 79, 26, 38),
            Frame(238, 80, 24, 37),
            Frame(263, 80, 30, 37),
            Frame(295, 80, 36, 37),
            Frame(334, 80, 32, 36),
            Frame(370, 79, 29, 38),
        ),
        moves=True,
    ),
    Animation(
        "점프·비행",
        (
            Frame(1, 124, 33, 40),
            Frame(39, 124, 35, 39),
            Frame(89, 125, 35, 38),
            Frame(130, 121, 34, 42),
            Frame(181, 122, 34, 41),
            Frame(228, 122, 33, 40),
        ),
        moves=True,
    ),
    Animation(
        "구르기 전환",
        (
            Frame(1, 169, 29, 30),
            Frame(35, 167, 29, 31),
            Frame(67, 169, 30, 29),
            Frame(98, 169, 31, 29),
            Frame(131, 168, 29, 30),
            Frame(162, 168, 29, 31),
            Frame(193, 170, 30, 29),
            Frame(230, 170, 31, 29),
        ),
        moves=False,
    ),
    Animation(
        "구르기",
        (
            Frame(1, 206, 30, 27),
            Frame(36, 206, 29, 27),
            Frame(70, 206, 29, 27),
            Frame(105, 206, 29, 27),
            Frame(139, 206, 29, 27),
            Frame(174, 206, 29, 27),
        ),
        moves=True,
    ),
    Animation(
        "대시",
        (
            Frame(1, 239, 29, 35),
            Frame(36, 239, 30, 35),
            Frame(74, 239, 31, 35),
            Frame(111, 238, 31, 36),
            Frame(149, 239, 30, 35),
            Frame(186, 238, 31, 36),
        ),
        moves=True,
    ),
    Animation(
        "스핀 대시",
        (
            Frame(1, 283, 29, 35),
            Frame(36, 283, 30, 35),
            Frame(72, 286, 39, 31),
            Frame(123, 285, 39, 32),
            Frame(172, 286, 39, 31),
            Frame(218, 285, 38, 32),
        ),
        moves=True,
    ),
    Animation(
        "방향 전환",
        (
            Frame(1, 326, 24, 45),
            Frame(31, 327, 29, 44),
            Frame(65, 327, 20, 44),
            Frame(90, 327, 25, 43),
            Frame(119, 327, 25, 43),
            Frame(149, 327, 20, 44),
        ),
        moves=False,
    ),
    Animation(
        "공중 자세",
        (
            Frame(184, 341, 40, 28),
            Frame(232, 341, 39, 27),
        ),
        moves=True,
    ),
    Animation(
        "달리기 자세",
        (
            Frame(1, 379, 27, 38),
            Frame(31, 379, 31, 36),
            Frame(64, 379, 31, 36),
            Frame(99, 377, 33, 38),
            Frame(136, 379, 32, 36),
            Frame(176, 379, 33, 36),
            Frame(217, 379, 33, 36),
            Frame(254, 378, 33, 36),
        ),
        moves=True,
    ),
    Animation(
        "피격·반응",
        (
            Frame(1, 429, 39, 40),
            Frame(49, 426, 34, 43),
            Frame(96, 427, 23, 39),
            Frame(125, 427, 23, 39),
        ),
        moves=False,
    ),
)


def handle_events() -> bool:
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def main() -> None:
    if not SPRITE_PATH.is_file():
        raise FileNotFoundError(f"Sprite sheet not found: {SPRITE_PATH}")

    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        while handle_events():
            delay(0.01)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
