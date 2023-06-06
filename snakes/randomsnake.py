from snakes.snake import Snake
from game.directions import Direction
import random

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
        
        return None,None,None