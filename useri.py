import pygame

#---------------------------------------------------------------------------------------------------------------------------

class UI:
    def __init__(self, screen_width, screen_height, font_path=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ui_height = 100  # UI bar height

        # Load font
        if font_path:
            self.font = pygame.font.Font(font_path, 24)
        else:
            self.font = pygame.font.SysFont("Arial", 24)

        # Timer and score tracking
        self.timer = "0:00"
        self.score = 0
        self.needed_score = 60  # Total score needed to complete the level

        # Progress bar settings
        self.bar_width = 300  # Width of the progress bar
        self.bar_height = 30
        self.bar_x = self.screen_width - self.bar_width - 20  # Position on the right side
        self.bar_y = self.screen_height - self.ui_height + 35

#---------------------------------------------------------------------------------------------------------------------------

    def update(self, timer, score, needed_score):
        self.timer = timer
        self.score = score
        self.needed_score = needed_score

#---------------------------------------------------------------------------------------------------------------------------

    def draw(self, screen):
        # Draw UI background
        ui_rect = pygame.Rect(0, self.screen_height - self.ui_height, self.screen_width, self.ui_height)
        pygame.draw.rect(screen, (30, 30, 30), ui_rect)  # Dark background

        # Draw timer on the left
        timer_text = self.font.render(f"Time: {self.timer}", True, (255, 255, 255))
        screen.blit(timer_text, (20, self.screen_height - self.ui_height + 35))

        # Draw score text with more space before the progress bar
        score_text = self.font.render(f"Score: {self.score}/{self.needed_score}", True, (255, 255, 255))
        screen.blit(score_text, (self.bar_x - 200, self.screen_height - self.ui_height + 35))

        # Draw progress bar background
        pygame.draw.rect(screen, (80, 80, 80), (self.bar_x, self.bar_y, self.bar_width, self.bar_height), border_radius=10)

        # Calculate filled width
        progress_ratio = min(max(self.score / self.needed_score, 0), 1)
        filled_width = int(self.bar_width * progress_ratio)

        # Draw progress bar fill
        pygame.draw.rect(screen, (0, 200, 0), (self.bar_x, self.bar_y, filled_width, self.bar_height), border_radius=10)