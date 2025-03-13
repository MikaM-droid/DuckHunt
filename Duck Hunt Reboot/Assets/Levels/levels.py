#class Level

#class Level1:
#class Level2:
#class Level3:

import pygame

class Level:
    def __init__(self, game):
        self.game = game
        self.background = pygame.Surface((game.DISPLAY_W, game.DISPLAY_H))
        self.background.fill((50, 168, 82))  # Example: Green background for now

    def draw(self):
        """Draws the level elements onto the game display."""
        self.game.display.blit(self.background, (0, 0))  # Draw background

    def update(self):
        """Updates any logic related to the level (enemies, environment, etc.)."""
        pass  # Implement later when needed

