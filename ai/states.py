from game.directions import Direction
from helper.constants import *

class State:
    @staticmethod
    def states():
        # Using list comprehensions to initialize state_space
        state_space = [(x, y, direction, danger)
            for x in range(0, DISPLAY_WIDTH + 1, BLOCK_SIZE)
            for y in range(0, DISPLAY_HEIGHT + 1, BLOCK_SIZE)
            for direction in Direction
            for danger in [0, 1]]
        return state_space


if __name__ == "__main__":
    State.states()