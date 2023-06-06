import pygame
import matplotlib.pyplot as plt
from helper.model_parser import ModelParser
from enum import Enum, auto
from game.food import Food
from game.score_board import ScoreBoard
from helper.constants import *
from snakes.aisnake import AISnake
from snakes.autosnake import AutoSnake
from snakes.randomsnake import RandomSnake
from snakes.snake import Snake

class GameState(Enum):
    RUNNING = auto()
    GAME_OVER = auto()
    EXIT = auto()

class SnakeGame:
    def __init__(self, snake, food, gamestyle):
        self.gamestyle = gamestyle
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
        self.tries_step = 1
        self.max_tries_range = 10
        self.max_scores_range = 10 
        plt.rcParams['backend'] = "Qt5Agg"
        
        # Start with an empty plot window:
        self.show_evaluation()
        
        self.reset(snake, food)
        
    def reset(self, snake, food):
        """Reset the game state."""
        self.state = GameState.RUNNING
        self.score = 0
        self.snake = snake.reset(start_x,start_y,BLOCK_SIZE)
        self.food = new_food()

    def draw_grid(self):
        # Create a separate Surface:
        grid_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                                      pygame.SRCALPHA)
        grid_color = WHITE + (30,) # Added alpha channel
        
        # Vertical grid-lines:
        for x in range(0, DISPLAY_WIDTH, BLOCK_SIZE):
            # Draw on the separate Surface
            pygame.draw.line(grid_surface, 
                             grid_color, 
                             (x, 0), 
                             (x, DISPLAY_HEIGHT))
        
        # Horizontal grid-lines:
        for y in range(0, DISPLAY_HEIGHT, BLOCK_SIZE):
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
        
        # Clear the plot so the line color stays the same:
        plt.clf()
        plt.title("Score Evaluation")
        
        # Set ticks of the axes (might need adaptive range fitting...)
        if len(self.scores) > self.max_tries_range:
            self.max_tries_range *= 2
            self.tries_step *= 2
        plt.xticks(range(0, len(self.scores), self.tries_step))
        plt.yticks(range(max(self.scores) + 1)) 
        
        # Plot the scores as a line:
        plt.plot(self.scores)
        
        # Set labelnames:
        plt.xlabel("number of tries")
        plt.ylabel("score")
        
        # Draw and show the plot:
        plt.draw()
        plt.show(block=False) # ensures to not block the game
        plt.pause(.1)
        
    def game_over_screen(self):
        """Display the game over screen and handle user input."""
        self.state = GameState.GAME_OVER

            
        # Show the evaluation of continous playing:
        self.show_evaluation()
            
        # Store Q-Table:
        if self.gamestyle == "ai-snake":
            with open('ai/model/q_table.json', 'w') as file:
                ModelParser.store_q_table(file,AISnake.q_table)

            AISnake.epsilon *= 0.95
            self.epsilon = max(AISnake.epsilon, 0.01)
            self.reset(self.snake,self.food)
            print("Epsilon is: ",self.epsilon)
        while self.state == GameState.GAME_OVER:

            # Restart on AI
            if self.gamestyle == "snake-ai" \
                or self.gamestyle == "auto-snake" \
                or self.gamestyle == "random-snake":
                return
            
            # Game Over Mode
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
                    
    def verify_movement(self,current_state,action,new_state):
        if self.gamestyle == "ai-snake":
            if self.snake.collision(DISPLAY_WIDTH,DISPLAY_HEIGHT):
                reward = -500
                AISnake.update_q_table(AISnake.q_table, current_state, action, reward, current_state, AISnake.alpha, AISnake.gamma)
                self.game_over_screen()
            elif self.snake.head() == self.food.pos:
                self.snake.eat_food()
                self.score += 1
                reward = 500
                self.food.pos = self.food.new_pos()
                AISnake.update_q_table(AISnake.q_table, current_state, action, reward, new_state, AISnake.alpha, AISnake.gamma)
            else:
                reward = -10
                AISnake.update_q_table(AISnake.q_table, current_state, action, reward, new_state, AISnake.alpha, AISnake.gamma)
        else:
            if self.snake.collision(DISPLAY_WIDTH,DISPLAY_HEIGHT):
                self.game_over_screen()
            elif self.snake.head() == self.food.pos:
                self.snake.eat_food()
                self.score += 1
                self.food.pos = self.food.new_pos()

    def run(self):
        """Main game loop."""
        while self.state != GameState.EXIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.EXIT
                else:
                    self.snake.handle_event(event)
                    
            current_state, action, new_state = self.snake.move()
            self.verify_movement(current_state, action, new_state)
            
            # Inefficient drawing!!!
            self.display.fill(BLUE)
            self.score_board.draw_border_and_score(self.score)  # Draw the border and score
            self.draw_grid()
            self.food.draw(self.display, GREEN, SCORE_BOARD_HEIGHT)
            self.snake.draw(self.display, WHITE, SCORE_BOARD_HEIGHT)
            pygame.display.update()
            
            self.clock.tick(GAME_SPEED_AI) if self.gamestyle == "ai-snake" else self.clock.tick(GAME_SPEED)


def new_snake(gamestyle):
    # return AutoSnake(start_x, start_y, SNAKE_BLOCK, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    start_x, start_y, BLOCK_SIZE
    if gamestyle=="snake":
        return Snake(start_x,start_y,BLOCK_SIZE)
    elif gamestyle=="auto-snake":
        return AutoSnake(start_x,start_y,BLOCK_SIZE,DISPLAY_WIDTH,DISPLAY_HEIGHT)
    elif gamestyle=="random-snake":
        return RandomSnake(start_x,start_y,BLOCK_SIZE)
    elif gamestyle == "ai-snake":
        return AISnake(start_x, start_y, BLOCK_SIZE)
    else:
        raise 

def new_food():
    return Food(DISPLAY_WIDTH, DISPLAY_HEIGHT)

def main(gamestyle):
    pygame.init()
    
    # Initialize Snake     
    snake = new_snake(gamestyle)   
    food = new_food()
    
    # Initialize game and run:
    game = SnakeGame(snake, food,gamestyle)
    game.run()
