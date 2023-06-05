import pygame
#import pygame_widgets.button as pw_button
import matplotlib.pyplot as plt
from enum import Enum, auto
from snake import (
    Snake,
    RandomSnake,
    AISnake,
    AutoSnake,
    SNAKE_BLOCK,
    SNAKE_SPEED,
)
from food import Food
from style import *


class GameState(Enum):
    RUNNING = auto()
    GAME_OVER = auto()
    EXIT = auto()


class ScoreBoard:
    def __init__(self, width, height, display: pygame.Surface, 
                 font_style: pygame.font.Font) -> None:
        self.width = width
        self.height = height
        self.font_style = font_style
        self.display = display
        
        # Create a separate Surface for the border and score:
        self.surface = pygame.Surface((self.width, self.height))
        
        # TODO: Buttons for leaderboard, options and quit:
        # self.button = pw_button.Button(self.surface, 
        #                                DISPLAY_WIDTH / 2, 0, 
        #                                200, self.height,
        #                                text='Leaderboard',
        #                                fontSize=50, margin=20,
        #                                inactiveColour=(255, 0, 0),
        #                                pressedColour=(0, 255, 0), radius=5,
        #                                onClick=lambda: print('Click'))
    
    def draw_border_and_score(self, score):
        # Draw the border
        rect = (0, 0, self.width, self.height)
        pygame.draw.rect(self.surface, WHITE, rect, self.height)

        # Display the score
        score_text = self.font_style.render(f'Score: {score}', True, BLUE)
        
        # events = pygame.event.get()
        # self.button.listen(events)
        # self.button.draw()
        
        # Blit the score text onto the border_and_score_surface
        self.surface.blit(score_text, (10, 10))

        # Blit the border_and_score_surface onto the main Surface
        self.display.blit(self.surface, (0, 0))


class SnakeGame:
    def __init__(self, snake, food):
        # Increase display height by Score board height:
        disp_size = (DISPLAY_WIDTH, DISPLAY_HEIGHT + SCORE_BOARD_HEIGHT) 
        self.display = pygame.display.set_mode(disp_size)
        
        pygame.display.set_caption('Snake Game')
        
        self.clock = pygame.time.Clock()
        self.score = 0
        
        # Set Fontstyle:
        self.font_style = pygame.font.SysFont(None, 50)
        
        # Initialize Score Board:
        self.score_board =  ScoreBoard(DISPLAY_WIDTH, SCORE_BOARD_HEIGHT, 
                                       self.display, self.font_style)

        # Scores:
        self.scores = []
        
        # Start with an empty plot window:
        self.show_evaluation()
        
        self.reset(snake, food)
        
    def reset(self, snake, food):
        """Reset the game state."""
        self.state = GameState.RUNNING
        self.score = 0
        self.snake = new_snake()
        self.food = new_food()

    def draw_grid(self):
        # Create a separate Surface:
        grid_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                      pygame.SRCALPHA)
        grid_color = WHITE + (30,) # Added alpha channel
        
        # Vertical grid-lines:
        for x in range(0, DISPLAY_WIDTH, SNAKE_BLOCK):
            # Draw on the separate Surface
            pygame.draw.line(grid_surface, 
                             grid_color, 
                             (x, 0), 
                             (x, DISPLAY_HEIGHT))
        
        # Horizontal grid-lines:
        for y in range(0, DISPLAY_HEIGHT, SNAKE_BLOCK):
            pygame.draw.line(grid_surface, 
                             grid_color, 
                             (0, y), 
                             (DISPLAY_WIDTH, y))

        # Blit the grid Surface onto the main Surface
        self.display.blit(grid_surface, (0, SCORE_BOARD_HEIGHT))


    def display_message(self, msg, color):
        """Display a message on the screen."""
        message_surface = self.font_style.render(msg, True, color)
        message_rect = message_surface.get_rect()
        message_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        self.display.blit(message_surface, message_rect)

    def show_evaluation(self):
        self.scores.append(self.score)
        # print(self.scores)
        
        # Clear the plot so the line color stays the same:
        plt.clf()
        plt.title("Score Evaluation")
        
        # Set ticks of the axes (might need adaptive range fitting...)
        plt.xticks(range(len(self.scores)))
        plt.yticks(range(max(self.scores) + 1))
        
        # Plot the scores as a line:
        plt.plot(self.scores)
        
        # Set labelnames:
        plt.xlabel("number of tries")
        plt.ylabel("score")
        
        # Draw and show the plot:
        plt.draw()
        plt.show(block=False) # ensures to not block the game
    
    def game_over_screen(self):
        """Display the game over screen and handle user input."""
        self.state = GameState.GAME_OVER
        
        # Show the evaluation of continous playing:
        self.show_evaluation()
        
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
            
            # TODO: Inefficient drawing!!!
            self.display.fill(BLUE)
            
            # Draw the border and score
            self.score_board.draw_border_and_score(self.score)
            self.draw_grid()
            self.food.draw(self.display, GREEN, SCORE_BOARD_HEIGHT)

            if self.snake.collision(DISPLAY_WIDTH, DISPLAY_HEIGHT):
                self.game_over_screen()

            self.snake.draw(self.display, WHITE, SCORE_BOARD_HEIGHT)
            pygame.display.update()

            if self.snake.head() == self.food.pos:
                self.snake.eat_food()
                self.score += 1
                self.food.pos = self.food.new_pos()

            self.clock.tick(SNAKE_SPEED)


def new_snake():
    start_x = DISPLAY_WIDTH / 2
    start_y = DISPLAY_HEIGHT / 2
    # return AutoSnake(start_x, start_y, SNAKE_BLOCK, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    return Snake(start_x, start_y, SNAKE_BLOCK)


def new_food():
    return Food(DISPLAY_WIDTH, DISPLAY_HEIGHT, SNAKE_BLOCK)


def main():
    pygame.init()
    
    # Initialize Snake
    snake = new_snake()
    food = new_food()
    
    # Initialize game and run:
    game = SnakeGame(snake, food)
    game.run()


if __name__ == "__main__":
    main()
