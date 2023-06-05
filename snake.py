import pygame
from enum import Enum,auto
import random

SNAKE_BLOCK = 40
SNAKE_SPEED = 15

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
        return self.body[0]
    
    def eat_food(self):
        self.grow()

    def grow(self):
        self.body.append(self.head())
        
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
        
        
class AutoSnake(Snake):
    def __init__(self, x, y, block_size, width, height):
        super().__init__(x, y, block_size)
        self.direction = Direction.RIGHT  # initial direction for auto-move
        self.width = width
        self.height = height
        self.visited = set()  # Set to store visited positions
        self.visited.add((x, y))  # Add initial position to visited set
        self.food_found = False 
        self.start_position = x,y

    def spiral_move(self):
        # Define the spiral direction order
        direction_order = {
            Direction.UP: [Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN],
            Direction.RIGHT: [Direction.DOWN, Direction.RIGHT, Direction.UP, Direction.LEFT],
            Direction.DOWN: [Direction.LEFT, Direction.DOWN, Direction.RIGHT, Direction.UP],
            Direction.LEFT: [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT],
        }

        for next_direction in direction_order[self.direction]:
            next_head = list(self.head())
            if next_direction == Direction.UP:
                next_head[1] -= self.block_size
            elif next_direction == Direction.DOWN:
                next_head[1] += self.block_size
            elif next_direction == Direction.LEFT:
                next_head[0] -= self.block_size
            elif next_direction == Direction.RIGHT:
                next_head[0] += self.block_size

            # Check if the next position is valid and not visited
            if (tuple(next_head) not in self.visited and 
                    next_head not in self.body and 
                    0 <= next_head[0] < self.width and 
                    0 <= next_head[1] < self.height):
                self.direction = next_direction
                break

        super().move()
        self.visited.add(tuple(self.head()))  # Add new head position to visited set

    def eat_food(self):
         super().eat_food()
         self.food_found = True
         self.visited = set()
         
    def move_towards_target(self):
        head_x, head_y = self.head()
        target_x, target_y = self.start_position
        if head_x < target_x:
            self.direction = Direction.RIGHT
        elif head_x > target_x:
            self.direction = Direction.LEFT
        elif head_y < target_y:
            self.direction = Direction.DOWN
        elif head_y > target_y:
            self.direction = Direction.UP
        else:
            self.food_found = False
            
        super().move()

    def move(self):
        if not self.food_found:
            self.spiral_move()  # Calls the spiral move method
        else:
            self.move_towards_target()
            
            
class AISnake(Snake):
    def move(self):
        return super().move()
