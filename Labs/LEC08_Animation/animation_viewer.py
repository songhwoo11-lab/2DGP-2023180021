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
ACTION_FRAME_COUNTS = (6, 6, 4, 4, 6, 6)


def get_frame_rect(action_index, frame_index):
	if not 0 <= action_index < len(ACTION_BANDS):
		raise IndexError("action index is out of range")
	if not 0 <= frame_index < ACTION_FRAME_COUNTS[action_index]:
		raise IndexError("frame index is out of range")

	frame_top, frame_bottom = ACTION_BANDS[action_index]
	return (
		FRAME_COLUMNS[frame_index],
		frame_top,
		FRAME_WIDTH,
		frame_bottom - frame_top,
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
