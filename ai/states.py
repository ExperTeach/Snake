from game.directions import Direction
from helper.style import *

class State:
    # Using list comprehensions to initialize state_space
    state_space = [(x, y, direction, danger)
        for x in range(0, int(DISPLAY_WIDTH - BLOCK_SIZE / BLOCK_SIZE) * BLOCK_SIZE, BLOCK_SIZE)
        for y in range(0, int(DISPLAY_HEIGHT - BLOCK_SIZE / BLOCK_SIZE) * BLOCK_SIZE, BLOCK_SIZE)
        for direction in Direction
        for danger in [0, 1]]

    @staticmethod
    def states():
        return State.state_space
