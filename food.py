import pygame
import random

class Food:
    def __init__(self, x_range, y_range, block_size):
        self.x_range = x_range
        self.y_range = y_range
        self.block_size = block_size
        self.pos = self.new_pos()

    def new_pos(self):
        food_x = round(random.randrange(0, self.x_range - self.block_size) / 10.0) * 10.0
        food_y = round(random.randrange(0, self.y_range - self.block_size) / 10.0) * 10.0
        return [food_x, food_y]

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, [self.pos[0], self.pos[1], self.block_size, self.block_size])