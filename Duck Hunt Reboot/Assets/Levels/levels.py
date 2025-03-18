#class Level

#class Level1:
#class Level2:
#class Level3:

import pygame

class Level():
    def __init__(self, game, bg_image_path):
        self.game = game
        self.background = pygame.image.load(bg_image_path)  # Load the background image
        self.background = pygame.transform.scale(self.background, (game.DISPLAY_W, game.DISPLAY_H))  # Scale it

    def draw(self):
        self.game.display.blit(self.background, (0, 0))  # Draw the background on the screen

class Level1(Level):
    def __init__(self, game):
        super().__init__(game, "level1.png")  # Load the background for Level 1

class Level2(Level):
    def __init__(self, game):
        super().__init__(game, "assets/background2.png")  # Load the background for Level 2

class Level3(Level):
    def __init__(self, game):
        super().__init__(game, "assets/background3.png")  # Load the background for Level 3





#class Level1(Level):



#class Level2(Level):



#class Level3(Level):



