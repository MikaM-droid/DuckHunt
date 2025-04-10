#class Level

#class Level1:
#class Level2:
#class Level3:

import pygame
import os

class Level():
    def __init__(self, game, bg_image_path):
        self.game = game
        # Construct the full path to the image in the bgs folder
        full_path = os.path.join("Duck Hunt Reboot", "Assets", "bgs", bg_image_path)
        self.background = pygame.image.load(full_path)  # Load the background image
        self.background = pygame.transform.scale(self.background, (game.DISPLAY_W, game.DISPLAY_H))  # Scale it
        self.completed = False

    def draw(self):
        self.game.display.blit(self.background, (0, 0))  # Draw the background on the screen

    def update(self):
        # Override this method in child classes to add level-specific logic
        pass

class Level1(Level):
    def __init__(self, game):
        super().__init__(game, "level1.png")  # Load the background for Level 1

class Level2(Level):
    def __init__(self, game):
        super().__init__(game, "level2.png")  # Load the background for Level 2

class Level3(Level):
    def __init__(self, game):
        super().__init__(game, "level3.png")  # Load the background for Level 3

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.current_level = None
        self.levels = {
            1: Level1(game),
            2: Level2(game),
            3: Level3(game)
        }
        self.current_level_number = 1

    def start_level(self, level_number):
        if level_number in self.levels:
            self.current_level_number = level_number
            self.current_level = self.levels[level_number]
            return True
        return False

    def next_level(self):
        if self.current_level_number < len(self.levels):
            return self.start_level(self.current_level_number + 1)
        return False

    def update(self):
        if self.current_level:
            self.current_level.update()

    def draw(self):
        if self.current_level:
            self.current_level.draw()





#class Level1(Level):



#class Level2(Level):



#class Level3(Level):



