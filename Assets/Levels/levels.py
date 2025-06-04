import pygame
import os
from Assets.Character.player import Player
from Assets.Animals.animal_manager import AnimalManager


################################################## Levels ###########################################################

class Level:
    '''
    Base class for all levels in the game.

    Attributes:
        game (Game): The game instance.
        background (pygame.Surface): The background image.
    '''
    def __init__(self, game, bg_image_path):
        '''
        Initialize the Level class.

        Args:
            game (Game): The game instance.
            bg_image_path (str): The path to the background image.
        '''
        self.game = game
        full_path = os.path.join("Assets", "bgs", bg_image_path)
        self.background = pygame.transform.scale(self.background, (game.DISPLAY_W, game.DISPLAY_H))

#--------------------------------------------------------------------------------------------------------------------------

    def draw(self):
        '''
        Draw the background on the screen.

        Args:
            screen (pygame.Surface): The screen surface.
        '''
        self.game.display.blit(self.background, (0, 0))

#--------------------------------------------------------------------------------------------------------------------------

    def update(self):
        '''
        Update the level.
        '''
        pass

#--------------------------------------------------------------------------------------------------------------------------
# The following classes are the backgrounds for the levels.

class Level1(Level):
    '''
    Level 1 class.

    Attributes:
        game (Game): The game instance.
        background (pygame.Surface): The background image.
    '''
    def __init__(self, game):
        super().__init__(game, "level1.png")

#--------------------------------------------------------------------------------------------------------------------------

class Level2(Level):
    '''
    Level 2 class.

    Attributes:
        game (Game): The game instance.
        background (pygame.Surface): The background image.
    '''
    def __init__(self, game):
        super().__init__(game, "level2.png")

#--------------------------------------------------------------------------------------------------------------------------

class Level3(Level):
    '''
    Level 3 class.

    Attributes:
        game (Game): The game instance.
        background (pygame.Surface): The background image.
    '''
    def __init__(self, game):
        super().__init__(game, "level3.png")

####################################################### Levels Manager#####################################################

class LevelManager:
    '''
    Level manager class.

    Attributes:
        game (Game): The game instance.
        current_level (Level): The current level.
    '''
    def __init__(self, game):
        '''
        Initialize the LevelManager class.

        Args:
            game (Game): The game instance.
        '''
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
        '''
        Start a level.

        Args:
            level_number (int): The level number to start.
        '''
        if level_number in self.levels:
            self.current_level_number = level_number
            self.current_level = self.levels[level_number]
            return True
        return False

#--------------------------------------------------------------------------------------------------------------------------

    def next_level(self):
        '''
        Go to the next level.

        Returns:
            bool: True if the next level exists, False otherwise.
        '''
        if self.current_level_number < len(self.levels):
            return self.start_level(self.current_level_number + 1)
        return False

#--------------------------------------------------------------------------------------------------------------------------

    def update(self):
        '''
        Update the current level. Once the level is updated, the level is drawn.
        '''
        if self.current_level:
            self.current_level.update()

#--------------------------------------------------------------------------------------------------------------------------

    def draw(self):
        '''
        Draw the current level.
        '''
        if self.current_level:
            self.current_level.draw()


