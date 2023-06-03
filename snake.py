import pygame
from enum import Enum,auto

SNAKE_BLOCK = 10
SNAKE_SPEED = 25

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()

class Snake:
    def __init__(self, x, y, block_size):
        self.body = [[x, y]]
        self.block_size = block_size
        self.direction = Direction.NONE  # initial direction

    def head(self):
        return self.body[-1]

    def grow(self):
        self.body.append(list(self.head()))
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                self.direction = Direction.DOWN
            elif event.key == pygame.K_LEFT:
                self.direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                self.direction = Direction.RIGHT

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

    def draw(self, surface, color):
        for x, y in self.body:
            pygame.draw.rect(surface, color, [x, y, self.block_size, self.block_size])
    
    def self_collision(self):
        return self.head() in self.body[:-1]
    
    def collision(self,width,height):
        return self.self_collision() or self.is_out_of_bounds(width,height)
    
class RandomSnake(Snake):
    
    def move(self):
        return super().move()
    

class AISnake(Snake):
    
    def move(self):
        return super().move()