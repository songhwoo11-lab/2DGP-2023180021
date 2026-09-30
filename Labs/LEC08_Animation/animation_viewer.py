from dataclasses import dataclass
from pathlib import Path

import pico2d


ASSET_PATH = Path(__file__).resolve().with_name("AnimationSheet.png")
SHEET_SIZE = (1800, 1200)
BACKGROUND_COLOR = (89, 145, 194)
ACTION_BANDS = (
	(24, 224),
	(230, 430),
	(420, 620),
	(610, 810),
	(800, 1000),
	(980, 1180),
)
ACTION_NAMES = tuple(f"Action {index}" for index in range(1, len(ACTION_BANDS) + 1))
FRAME_COLUMNS = tuple(576 + index * 190 for index in range(6))
FRAME_WIDTH = 180
FRAME_HEIGHT = 200
ACTION_FRAME_COUNTS = (6, 6, 4, 4, 6, 6)
CANVAS_SIZE = (1280, 720)
FRAME_INTERVAL = 0.12
MAX_VISIBLE_HEIGHT = 179
MIN_VISIBLE_HEIGHT_RATIO = 0.5
FIT_MARGIN_RATIO = 0.9


@dataclass(frozen=True)
class Frame:
	source_x: int
	source_top: int
	source_width: int
	source_height: int


@dataclass(frozen=True)
class Action:
	name: str
	frames: tuple[Frame, ...]


@dataclass
class PlaybackState:
	action_index: int = 0
	frame_index: int = 0
	elapsed: float = 0.0


ACTIONS = tuple(
	Action(
		name=action_name,
		frames=tuple(
			Frame(
				source_x=FRAME_COLUMNS[frame_index],
				source_top=frame_top,
				source_width=FRAME_WIDTH,
				source_height=frame_bottom - frame_top,
			)
			for frame_index in range(frame_count)
		),
	)
	for action_name, (frame_top, frame_bottom), frame_count in zip(
		ACTION_NAMES, ACTION_BANDS, ACTION_FRAME_COUNTS
	)
)


def get_frame_rect(action_index, frame_index):
	if not 0 <= action_index < len(ACTION_BANDS):
		raise IndexError("action index is out of range")
	if not 0 <= frame_index < ACTION_FRAME_COUNTS[action_index]:
		raise IndexError("frame index is out of range")

	frame = ACTIONS[action_index].frames[frame_index]
	return frame.source_x, frame.source_top, frame.source_width, frame.source_height


def calculate_scale(canvas_width, canvas_height):
	if canvas_width <= 0 or canvas_height <= 0:
		raise ValueError("canvas dimensions must be positive")

	target_scale = canvas_height * MIN_VISIBLE_HEIGHT_RATIO / MAX_VISIBLE_HEIGHT
	fit_scale = min(
		canvas_width * FIT_MARGIN_RATIO / FRAME_WIDTH,
		canvas_height * FIT_MARGIN_RATIO / FRAME_HEIGHT,
	)
	return min(target_scale, fit_scale)


def consume_frame_ticks(state, delta_time):
	if delta_time < 0:
		raise ValueError("delta time cannot be negative")

	state.elapsed += delta_time
	frame_ticks = 0
	while state.elapsed + 1e-9 >= FRAME_INTERVAL:
		state.elapsed -= FRAME_INTERVAL
		frame_ticks += 1
	return frame_ticks


def advance_frame(state):
	last_frame_index = len(ACTIONS[state.action_index].frames) - 1
	if state.frame_index >= last_frame_index:
		return False

	state.frame_index += 1
	return True


def advance_to_next_action(state):
	state.action_index = (state.action_index + 1) % len(ACTIONS)
	state.frame_index = 0
	return True


def load_sheet():
	return pico2d.load_image(str(ASSET_PATH))


def draw_frame(sheet, action_index, frame_index, x, y, draw_width, draw_height):
	frame = ACTIONS[action_index].frames[frame_index]
	source_bottom = SHEET_SIZE[1] - frame.source_top - frame.source_height
	sheet.clip_draw(
		frame.source_x,
		source_bottom,
		frame.source_width,
		frame.source_height,
		x,
		y,
		draw_width,
		draw_height,
	)


def draw_background(canvas_width, canvas_height):
	pico2d.draw_rectangle(
		0,
		0,
		canvas_width,
		canvas_height,
		*BACKGROUND_COLOR,
		filled=True,
	)


def open_viewer_canvas():
	pico2d.open_canvas(*CANVAS_SIZE)


def should_close(events):
	return any(event.type == pico2d.SDL_QUIT for event in events)
