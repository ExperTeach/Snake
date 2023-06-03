import pygame
from enum import Enum, auto
import sys
from snake import Snake,RandomSnake,AISnake,AutoSnake,SNAKE_BLOCK,SNAKE_SPEED
from food import Food
from style import WHITE, BLUE, GREEN, RED, DISPLAY_HEIGHT, DISPLAY_WIDTH
pygame.init()

FONT_STYLE = pygame.font.SysFont(None, 50)

class GameState(Enum):
    RUNNING = auto()
    GAME_OVER = auto()
    EXIT = auto()

class SnakeGame:
    def __init__(self, snake, food):
        self.border_thickness = 50  # Choose the thickness of the border
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT + self.border_thickness))  # Increase display height by border_thickness
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.score = 0

        self.reset(snake, food)
        
    def reset(self, snake, food):
        """Reset the game state."""
        self.state = GameState.RUNNING
        self.score = 0
        self.snake = new_snake()
        self.food = new_food()
        
    def draw_border_and_score(self):
        border_and_score_surface = pygame.Surface((DISPLAY_WIDTH, self.border_thickness))  # Create a separate Surface for the border and score
        #border_and_score_surface.fill(BLUE)  # Fill the surface with blue

        # Draw the border
        pygame.draw.rect(border_and_score_surface, WHITE, (0, 0, DISPLAY_WIDTH, self.border_thickness), self.border_thickness)

        # Display the score
        score_text = FONT_STYLE.render(f'Score: {self.score}', True, BLUE)
        border_and_score_surface.blit(score_text, (10, 10))  # Blit the score text onto the border_and_score_surface

        self.display.blit(border_and_score_surface, (0, 0))  # Blit the border_and_score_surface onto the main Surface

    def draw_grid(self):
        grid_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)  # Create a separate Surface

        for x in range(0, DISPLAY_WIDTH, SNAKE_BLOCK):
            pygame.draw.line(grid_surface, WHITE + (30,), (x, 0), (x, DISPLAY_HEIGHT))  # Draw on the separate Surface
        for y in range(0, DISPLAY_HEIGHT, SNAKE_BLOCK):
            pygame.draw.line(grid_surface, WHITE + (30,), (0, y), (DISPLAY_WIDTH, y))  # Draw on the separate Surface

        self.display.blit(grid_surface, (0, 0))  # Blit the grid Surface onto the main Surface


    def display_message(self, msg, color):
        """Display a message on the screen."""
        message_surface = FONT_STYLE.render(msg, True, color)
        message_rect = message_surface.get_rect()
        message_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        self.display.blit(message_surface, message_rect)

    def game_over_screen(self):
        """Display the game over screen and handle user input."""
        self.state = GameState.GAME_OVER
        while self.state == GameState.GAME_OVER:
            self.display.fill(BLUE)
            self.display_message("You Lost! Press C-Play Again or Q-Quit", RED)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.state = GameState.EXIT
                        return
                    if event.key == pygame.K_c:
                        self.reset(self.snake,self.food)
                        return

    def run(self):
        """Main game loop."""
        while self.state != GameState.EXIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.EXIT
                else:
                    self.snake.handle_event(event)

            self.snake.move()
            self.display.fill(BLUE)
            self.draw_grid()
            self.draw_border_and_score()  # Draw the border and score
            self.food.draw(self.display, GREEN, self.border_thickness)

            if self.snake.collision(DISPLAY_WIDTH, DISPLAY_HEIGHT):
                self.game_over_screen()

            self.snake.draw(self.display, WHITE, self.border_thickness)
            pygame.display.update()

            if self.snake.head() == self.food.pos:
                self.snake.eat_food()
                self.score += 1
                self.food.pos = self.food.new_pos()

            self.clock.tick(SNAKE_SPEED)

def new_snake():
    return AutoSnake(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, SNAKE_BLOCK, DISPLAY_WIDTH,DISPLAY_HEIGHT)

def new_food():
    return Food(DISPLAY_WIDTH, DISPLAY_HEIGHT, SNAKE_BLOCK)

if __name__ == "__main__":
    # Initialize Snake
    snake = new_snake()
    food = new_food()
    
    game = SnakeGame(snake,food)
    game.run()