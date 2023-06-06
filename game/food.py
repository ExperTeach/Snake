import pygame
import random
from helper.style import BLOCK_SIZE

class Food:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range
        self.pos = self.new_pos()

    def new_pos(self):
        food_x = round(random.randrange(0, self.x_range - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(0, self.y_range - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        return [food_x, food_y]

    def draw(self, surface, color, border_thickness):
        pygame.draw.rect(surface, color, [self.pos[0], self.pos[1] + border_thickness, BLOCK_SIZE, BLOCK_SIZE])  # Shift y-coordinate by border_thickness