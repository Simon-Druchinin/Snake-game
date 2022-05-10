import os


# Cells
CELL_SIZE = 40
CELL_AMOUNT = 20

# Widow size
WIDTH = HEIGHT = CELL_SIZE * CELL_AMOUNT

# Colors
GREEN = (175,215,70)
GRASS_COLOR = (167,209,61)
TEXT_COLOR = (56, 74, 12) # Gray

GAME_NAME = "Питон"

# Pathes to data
DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_SCORE_JSON_PATH = f"{DIR}/data/player_score.json"