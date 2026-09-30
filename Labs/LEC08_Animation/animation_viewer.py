from pathlib import Path


ASSET_PATH = Path(__file__).resolve().with_name("AnimationSheet.png")
SHEET_SIZE = (1800, 1200)
BACKGROUND_COLOR = (89, 145, 194)
ACTION_BANDS = (
	(24, 230),
	(240, 420),
	(420, 610),
	(610, 800),
	(800, 990),
	(980, 1180),
)
ACTION_NAMES = tuple(f"Action {index}" for index in range(1, len(ACTION_BANDS) + 1))
