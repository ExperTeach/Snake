import pygame
from helper.style import *

class ScoreBoard:
    def __init__(self, width, height, display: pygame.Surface, 
                 font_style: pygame.font.Font) -> None:
        self.width = width
        self.height = height
        self.font_style = font_style
        self.display = display
        
        # Create a separate Surface for the border and score:
        self.surface = pygame.Surface((self.width, self.height))
    
    def draw_border_and_score(self, score):
        # Draw the border
        rect = (0, 0, self.width, self.height)
        pygame.draw.rect(self.surface, WHITE, rect, self.height)

        # Display the score
        score_text = self.font_style.render(f'Score: {score}', True, BLUE)
        
        # Blit the score text onto the border_and_score_surface
        self.surface.blit(score_text, (10, 10))

        # Blit the border_and_score_surface onto the main Surface
        self.display.blit(self.surface, (0, 0))