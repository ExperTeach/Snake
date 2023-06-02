import pygame
from enum import Enum, auto
import sys
from snake import Snake,SNAKE_BLOCK,SNAKE_SPEED
from food import Food
from style import WHITE, BLUE, GREEN, RED, DISPLAY_HEIGHT, DISPLAY_WIDTH
pygame.init()

FONT_STYLE = pygame.font.SysFont(None, 50)

class GameState(Enum):
    RUNNING = auto()
    GAME_OVER = auto()
    EXIT = auto()

class SnakeGame:
    def __init__(self, snake,food):
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.reset(snake,food)
        
    def reset(self, snake, food):
        """Reset the game state."""
        self.state = GameState.RUNNING
        
        self.snake = snake
        self.food = food

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
                        self.reset()
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
            self.food.draw(self.display, GREEN)

            if self.snake.collision(DISPLAY_WIDTH, DISPLAY_HEIGHT):
                self.game_over_screen()

            self.snake.draw(self.display, WHITE)
            pygame.display.update()

            if self.snake.head() == self.food.pos:
                self.food.pos = self.food.new_pos()
                self.snake.grow()

            self.clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    # Initialize Snake
    snake = Snake(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, SNAKE_BLOCK)
    food = Food(DISPLAY_WIDTH, DISPLAY_HEIGHT, SNAKE_BLOCK)
    
    game = SnakeGame(snake,food)
    game.run()