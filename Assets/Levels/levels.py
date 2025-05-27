import pygame
import os
from Assets.Character.player import Player
from Assets.Animals.animal_manager import AnimalManager

################################################## Levels ###########################################################
#Level() is the base class for all levels in the game.
#It contains the draw method, which draws the background on the screen.
#It also contains the update method, which updates the level.

class Level:
    def __init__(self, game, bg_image_path):
        self.game = game
        full_path = os.path.join("Assets", "bgs", bg_image_path)
        self.background = pygame.image.load(full_path)
        self.background = pygame.transform.scale(self.background, (game.DISPLAY_W, game.DISPLAY_H))

    def draw(self):
        self.game.display.blit(self.background, (0, 0))

    def update(self):
        pass

#--------------------------------------------------------------------------------------------------------------------------
# The following classes are the backgrounds for the levels.

class Level1(Level):
    def __init__(self, game):
        super().__init__(game, "level1.png")

#--------------------------------------------------------------------------------------------------------------------------

class Level2(Level):
    def __init__(self, game):
        super().__init__(game, "level2.png")

#--------------------------------------------------------------------------------------------------------------------------

class Level3(Level):
    def __init__(self, game):
        super().__init__(game, "level3.png")

####################################################### Levels Manager#####################################################
# LevelManager() is the manager for the levels in the game. It contains the start_level method, which starts the level.
# It also contains the next_level method, which goes to the next level,
# update method for level updating and draw method for level drawing.

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

#--------------------------------------------------------------------------------------------------------------------------

    def start_level(self, level_number):
        if level_number in self.levels:
            self.current_level_number = level_number
            self.current_level = self.levels[level_number]
            return True
        return False

#--------------------------------------------------------------------------------------------------------------------------

    def next_level(self):
        if self.current_level_number < len(self.levels):
            return self.start_level(self.current_level_number + 1)
        return False

#--------------------------------------------------------------------------------------------------------------------------

    def update(self):
        if self.current_level:
            self.current_level.update()

#--------------------------------------------------------------------------------------------------------------------------

    def draw(self):
        if self.current_level:
            self.current_level.draw()


