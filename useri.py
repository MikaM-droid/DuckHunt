import pygame

############################################## Game UI ###################################################

class UI:
    """
    Game UI class that handles the display of the timer, score, and progress bar.
    
    Attributes:
        screen_width: Width of the screen
        screen_height: Height of the screen
        ui_height: Height of the UI
    """
    def __init__(self, screen_width, screen_height, font_path=None):
        '''
        Initialize the UI class.
        
        Args:
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
            font_path (str, optional): The path to the font file. Defaults to None.
        '''
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ui_height = 100

        # Load font
        if font_path:
            self.font = pygame.font.Font(font_path, 24)
        else:
            self.font = pygame.font.SysFont("Arial", 24)

        # Timer and score tracking
        self.timer = "0:00"
        self.score = 0 # Score of the player
        self.needed_score = 100 # Default score needed for level 1

        # Progress bar settings
        self.bar_width = 300  # Width and height of the progress bar
        self.bar_height = 30    
        self.bar_x = self.screen_width - self.bar_width - 20  # Position on the right side of the screen
        self.bar_y = self.screen_height - self.ui_height + 35 # Position on the bottom of the screen

#---------------------------------------------------------------------------------------------------------------------------
# Update the UI with new values

    def update(self, timer, score, needed_score):
        """
        Update the UI with new values.
        
        Args:
            timer (str): The timer value.
            score (int): The score value.
            needed_score (int): The needed score value.
        """	
        self.timer = timer
        self.score = score
        self.needed_score = needed_score

#---------------------------------------------------------------------------------------------------------------------------
# Draw the UI elements on the screen

    def draw(self, screen):
        """
        Draw the UI elements on the screen.
        
        Args:
            screen (pygame.Surface): The screen surface.
        """
        # Draw UI background
        ui_rect = pygame.Rect(0, self.screen_height - self.ui_height, self.screen_width, self.ui_height)
        pygame.draw.rect(screen, (30, 30, 30), ui_rect)  # Dark background

        # Draw timer on the left
        timer_text = self.font.render(f"Time: {self.timer}", True, (255, 255, 255))
        screen.blit(timer_text, (20, self.screen_height - self.ui_height + 35))

        # Draw score text with space before the progress bar to avoid overlap
        score_text = self.font.render(f"Score: {self.score}/{self.needed_score}", True, (255, 255, 255))
        screen.blit(score_text, (self.bar_x - 200, self.screen_height - self.ui_height + 35))

        # Draw progress bar background 
        pygame.draw.rect(screen, (80, 80, 80), (self.bar_x, self.bar_y, self.bar_width, self.bar_height), border_radius=10)

        # Calculate filled width
        progress_ratio = min(max(self.score / self.needed_score, 0), 1)
        filled_width = int(self.bar_width * progress_ratio)

        # Draw progress bar fill
        pygame.draw.rect(screen, (0, 200, 0), (self.bar_x, self.bar_y, filled_width, self.bar_height), border_radius=10)