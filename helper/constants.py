from enum import Enum,auto

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

SCORE_BOARD_HEIGHT = 50
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

BLOCK_SIZE = 40
GAME_SPEED = 15
GAME_SPEED_AI = 500

start_x = int((DISPLAY_WIDTH / 2 ) / BLOCK_SIZE ) * BLOCK_SIZE
start_y = int((DISPLAY_HEIGHT / 2 ) / BLOCK_SIZE ) * BLOCK_SIZE

    