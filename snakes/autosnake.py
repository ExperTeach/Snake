from snakes.snake import *

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