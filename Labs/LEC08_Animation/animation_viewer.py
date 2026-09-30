from dataclasses import dataclass
from pathlib import Path
import time

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
ACTION_NAMES = ("Repulsion", "Roll", "Slide", "Squat", "Throw2", "Work2")
FRAME_COLUMNS = tuple(576 + index * 190 for index in range(6))
FRAME_WIDTH = 180
FRAME_HEIGHT = 200
ACTION_FRAME_COUNTS = (6, 6, 4, 4, 6, 6)
CANVAS_SIZE = (1280, 720)
FRAME_INTERVAL = 0.12
ACTION_REPETITIONS = 5
ACTION_REST_DURATION = 1.0
MAX_VISIBLE_HEIGHT = 179
MIN_VISIBLE_HEIGHT_RATIO = 0.5
FIT_MARGIN_RATIO = 0.9
STATUS_FONT_PATH = Path("C:/Windows/Fonts/malgun.ttf")
STATUS_FONT_SIZE = 24


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
	repetition_count: int = 0
	rest_elapsed: float = 0.0
	resting: bool = False
	paused: bool = False


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
	state.elapsed = 0.0
	state.repetition_count = 0
	state.rest_elapsed = 0.0
	state.resting = False
	return True


def update_playback(state, delta_time):
	if delta_time < 0:
		raise ValueError("delta time cannot be negative")
	if state.paused:
		return

	if state.resting:
		time_to_next_action = ACTION_REST_DURATION - state.rest_elapsed
		if delta_time < time_to_next_action:
			state.rest_elapsed += delta_time
			return
		delta_time -= time_to_next_action
		advance_to_next_action(state)

	for _ in range(consume_frame_ticks(state, delta_time)):
		if not advance_frame(state):
			state.repetition_count += 1
			if state.repetition_count < ACTION_REPETITIONS:
				state.frame_index = 0
			else:
				state.resting = True
				state.rest_elapsed = 0.0
				state.elapsed = 0.0
				break


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


def draw_current_frame(sheet, state, canvas_width, canvas_height):
	scale = calculate_scale(canvas_width, canvas_height)
	draw_width = round(FRAME_WIDTH * scale)
	draw_height = round(FRAME_HEIGHT * scale)
	draw_frame(
		sheet,
		state.action_index,
		state.frame_index,
		round(canvas_width / 2),
		round(canvas_height / 2),
		draw_width,
		draw_height,
	)


def load_status_font():
	return pico2d.load_font(str(STATUS_FONT_PATH), STATUS_FONT_SIZE)


def draw_status(font, state, canvas_width, canvas_height):
	action_number = state.action_index + 1
	repetition = min(state.repetition_count + 1, ACTION_REPETITIONS)
	phase = "1초 휴식" if state.resting else f"{repetition}/{ACTION_REPETITIONS}"
	status = f"액션 {action_number} / {len(ACTIONS)} · {ACTIONS[state.action_index].name} · {phase}"
	font.draw(24, canvas_height - 30, status, color=(255, 255, 255))


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


def reset_playback(state):
	state.action_index = 0
	state.frame_index = 0
	state.elapsed = 0.0
	state.repetition_count = 0
	state.rest_elapsed = 0.0
	state.resting = False
	state.paused = False


def handle_events(events, state):
	for event in events:
		if event.type == pico2d.SDL_QUIT:
			return True
		if event.type != pico2d.SDL_KEYDOWN:
			continue

		key = event.key.keysym.sym
		if key == pico2d.SDLK_ESCAPE:
			return True
		if key == pico2d.SDLK_SPACE:
			state.paused = not state.paused
		elif key == pico2d.SDLK_r:
			reset_playback(state)

	return False


def run_viewer():
	open_viewer_canvas()
	try:
		sheet = load_sheet()
		font = load_status_font()
		state = PlaybackState()
		previous_time = time.perf_counter()
		running = True

		while running:
			events = pico2d.get_events()
			running = not handle_events(events, state)
			current_time = time.perf_counter()
			update_playback(state, current_time - previous_time)
			previous_time = current_time

			pico2d.clear_canvas()
			draw_background(*CANVAS_SIZE)
			draw_current_frame(sheet, state, *CANVAS_SIZE)
			draw_status(font, state, *CANVAS_SIZE)
			pico2d.update_canvas()
			pico2d.delay(0.01)
	finally:
		pico2d.close_canvas()


if __name__ == "__main__":
	run_viewer()
