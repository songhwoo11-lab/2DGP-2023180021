"""Sequential animation viewer for the Sonic sprite sheet."""

from dataclasses import dataclass
from pathlib import Path
import os

from pico2d import *


BASE_DIR = Path(__file__).resolve().parent
SPRITE_PATH = BASE_DIR / "sonic-sprite.png"
FONT_PATH = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / "malgun.ttf"
SHEET_WIDTH = 399
SHEET_HEIGHT = 525
MIN_SCREEN_WIDTH = 600
MIN_SCREEN_HEIGHT = 800
SCALE = 4
FRAME_INTERVAL = 0.1
MOVE_SPEED = 200.0
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


@dataclass
class PlaybackState:
    animation_index: int = 0
    frame_index: int = 0
    frame_elapsed: float = 0.0
    completed_repeats: int = 0
    pause_remaining: float = 0.0
    position_x: float = 0.0


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


def validate_animation_data() -> None:
    if not ANIMATIONS:
        raise ValueError("At least one animation must be registered.")

    names = [animation.name for animation in ANIMATIONS]
    if len(names) != len(set(names)):
        raise ValueError("Animation names must be unique.")

    for animation in ANIMATIONS:
        if not animation.frames:
            raise ValueError(f"Animation has no frames: {animation.name}")
        for frame in animation.frames:
            if frame.width <= 0 or frame.height <= 0:
                raise ValueError(f"Invalid frame size in {animation.name}: {frame}")
            if (
                frame.x < 0
                or frame.y < 0
                or frame.x + frame.width > SHEET_WIDTH
                or frame.y + frame.height > SHEET_HEIGHT
            ):
                raise ValueError(f"Frame is outside the sprite sheet: {frame}")


def calculate_canvas_size() -> tuple[int, int]:
    max_frame_width = max(
        frame.width for animation in ANIMATIONS for frame in animation.frames
    )
    max_frame_height = max(
        frame.height for animation in ANIMATIONS for frame in animation.frames
    )
    max_name_length = max(len(animation.name) for animation in ANIMATIONS)

    required_width = max(
        MIN_SCREEN_WIDTH,
        max_frame_width * SCALE + 48,
        max_name_length * 24 + 48,
    )
    required_height = max(
        MIN_SCREEN_HEIGHT,
        max_frame_height * SCALE + 48 + 40,
    )
    ratio_unit = max((required_width + 2) // 3, (required_height + 3) // 4)
    return ratio_unit * 3, ratio_unit * 4


def handle_events() -> bool:
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def draw_frame(
    sprite_sheet: Image, frame: Frame, center_x: float, center_y: float, scale: int = 1
) -> None:
    sprite_sheet.clip_draw(
        frame.x,
        SHEET_HEIGHT - frame.y - frame.height,
        frame.width,
        frame.height,
        center_x,
        center_y,
        frame.width * scale,
        frame.height * scale,
    )


def draw_current_frame(
    sprite_sheet: Image,
    animation: Animation,
    state: PlaybackState,
    screen_width: int,
    screen_height: int,
) -> None:
    center_x = state.position_x if animation.moves else screen_width / 2
    draw_frame(
        sprite_sheet,
        animation.frames[state.frame_index],
        center_x,
        screen_height / 2,
        scale=SCALE,
    )


def start_animation(
    state: PlaybackState, animation_index: int, screen_width: int
) -> None:
    animation = ANIMATIONS[animation_index]
    state.animation_index = animation_index
    state.frame_index = 0
    state.frame_elapsed = 0.0
    state.completed_repeats = 0
    state.pause_remaining = 0.0
    if animation.moves:
        widest_frame = max(frame.width for frame in animation.frames) * SCALE
        state.position_x = -widest_frame / 2
    else:
        state.position_x = screen_width / 2


def update_frame(
    state: PlaybackState, delta_time: float, screen_width: int
) -> None:
    if state.pause_remaining > 0.0:
        state.pause_remaining = max(0.0, state.pause_remaining - delta_time)
        if state.pause_remaining == 0.0:
            next_index = (state.animation_index + 1) % len(ANIMATIONS)
            start_animation(state, next_index, screen_width)
        return

    animation = ANIMATIONS[state.animation_index]
    state.frame_elapsed += delta_time
    while state.frame_elapsed >= FRAME_INTERVAL:
        state.frame_elapsed -= FRAME_INTERVAL
        state.frame_index += 1
        if state.frame_index == len(animation.frames):
            state.completed_repeats += 1
            if state.completed_repeats == REPEAT_COUNT:
                state.frame_index -= 1
                state.pause_remaining = PAUSE_DURATION
                state.frame_elapsed = 0.0
                break
            state.frame_index = 0


def update_position(
    state: PlaybackState,
    animation: Animation,
    delta_time: float,
    screen_width: int,
) -> None:
    if animation.moves and state.pause_remaining == 0.0:
        state.position_x += MOVE_SPEED * delta_time
        half_width = max(frame.width for frame in animation.frames) * SCALE / 2
        right_edge = screen_width + half_width
        if state.position_x > right_edge:
            travel = screen_width + half_width * 2
            overflow = (state.position_x - right_edge) % travel
            state.position_x = -half_width + overflow


def main() -> None:
    if not SPRITE_PATH.is_file():
        raise FileNotFoundError(f"Sprite sheet not found: {SPRITE_PATH}")
    if not FONT_PATH.is_file():
        raise FileNotFoundError(f"Korean font not found: {FONT_PATH}")
    validate_animation_data()

    screen_width, screen_height = calculate_canvas_size()
    open_canvas(screen_width, screen_height)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        font = None
        try:
            font = load_font(str(FONT_PATH), 20)
            playback = PlaybackState()
            start_animation(playback, 0, screen_width)
            previous_time = get_time()
            while handle_events():
                current_time = get_time()
                delta_time = current_time - previous_time
                previous_time = current_time
                update_frame(playback, delta_time, screen_width)
                animation = ANIMATIONS[playback.animation_index]
                update_position(playback, animation, delta_time, screen_width)

                clear_canvas()
                draw_current_frame(
                    sprite_sheet,
                    animation,
                    playback,
                    screen_width,
                    screen_height,
                )
                font.draw(20, screen_height - 32, animation.name, (255, 255, 255))
                update_canvas()
                delay(0.01)
        finally:
            font = None
            sprite_sheet = None
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
