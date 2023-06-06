import pygame

import random
from game.directions import Direction


   


class Snake:
    def __init__(self, start_x, start_y, block_size):
        self.body = [[start_x, start_y]]
        self.block_size = block_size
        self.direction = Direction.NONE  # initial direction
        
    def reset(self, start_x,start_y,block_size):
        self.body = [[start_x, start_y]]
        self.block_size = block_size
        self.direction = Direction.NONE  # initial direction
        return self
    
    def head(self):
        return self.body[0]
    
    def eat_food(self):
        #self.grow()
        pass

    def grow(self):
        #self.body.append(self.head())
        pass
        
    #def handle_event(self, event):
    #    if event.type == pygame.KEYDOWN:
    #        if event.key == pygame.K_UP:
    #            self.direction = Direction.UP
    #        elif event.key == pygame.K_DOWN:
    #            self.direction = Direction.DOWN
    #        elif event.key == pygame.K_LEFT:
    #            self.direction = Direction.LEFT
    #        elif event.key == pygame.K_RIGHT:
    #            self.direction = Direction.RIGHT

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == Direction.UP:
            head_y -= self.block_size
        elif self.direction == Direction.DOWN:
            head_y += self.block_size
        elif self.direction == Direction.LEFT:
            head_x -= self.block_size
        elif self.direction == Direction.RIGHT:
            head_x += self.block_size

        self.body.insert(0, [head_x, head_y])  # add new position to the head of the snake
        self.body.pop()  # remove the tail of the snake
        
    def is_out_of_bounds(self, width, height):
        head_x, head_y = self.head()
        if head_x >= width or head_x < 0 or head_y >= height or head_y < 0:
            return True
        return False

    def draw(self, surface, color, border_thickness):
        for x, y in self.body:
            pygame.draw.rect(surface, color, [x, y + border_thickness, self.block_size, self.block_size])  # Shift y-coordinate by border_thickness

    def self_collision(self):
        return self.head() in self.body[1:]
    
    def collision(self,width,height):
        return self.self_collision() or self.is_out_of_bounds(width,height)
    

class RandomSnake(Snake):        
    def __init__(self, x, y, block_size):
        self.body = [[x, y]]
        self.block_size = block_size
        self.direction = Direction.LEFT  # initial direction
    
    def check_potential_collision(self, position:list):
        return position in self.body[:-1]
    
    def move(self):
        potential_collision = True
        while potential_collision:
            self.direction = random.choice(list(Direction))
            head_x, head_y = self.body[0]
            new_head_x = head_x
            new_head_y = head_y
            if self.direction == Direction.UP:
                new_head_y = head_y - self.block_size
            elif self.direction == Direction.DOWN:
                new_head_y = head_y + self.block_size
            elif self.direction == Direction.LEFT:
                new_head_x = head_x - self.block_size
            elif self.direction == Direction.RIGHT:
                new_head_x = head_x + self.block_size
            potential_collision = self.check_potential_collision([new_head_x,new_head_y])

        self.body.insert(0, [new_head_x, new_head_y])  # add new position to the head of the snake
        self.body.pop()  # remove the tail of the snake