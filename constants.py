from enum import Enum

VERSION = '0.0.2'

# How many pieces are needed to be in a row to win
NUM_IN_A_ROW = 5

# 15 * 15 board
BOARD_SIZE = 15
CENTER_POINT = 7, 7

# Board size in pixels
BOARD_WIDTH_PIXELS = 640
BOARD_HEIGHT_PIXELS = BOARD_WIDTH_PIXELS + 40
PIECE_RADIUS_PIXELS = 15

# Point to Point distance in pixels
P2P_PIXELS = BOARD_WIDTH_PIXELS / (BOARD_SIZE + 1)


class VersusMode(Enum):
    PvP = 1
    PvA = 2  # Player black vs AI white
    AvP = 3  # AI black vs player white
