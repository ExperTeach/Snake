import pygame
import random

class Food:
    def __init__(self, x_range, y_range, block_size):
        self.x_range = x_range
        self.y_range = y_range
        self.block_size = block_size
        self.pos = self.new_pos()

    def new_pos(self):
        x_number_of_blocks = (self.x_range - self.block_size) / self.block_size
        y_number_of_blocks = (self.x_range - self.block_size) / self.block_size
        food_x = round(random.randrange(0,x_number_of_blocks) )* self.block_size
        food_y = round(random.randrange(0,y_number_of_blocks) )* self.block_size
        return [food_x, food_y]

    def draw(self, surface, color, border_thickness):
        pygame.draw.rect(surface, color, [self.pos[0], self.pos[1] + border_thickness, self.block_size, self.block_size])  # Shift y-coordinate by border_thickness