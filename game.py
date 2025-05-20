import pygame
from menu import *
from Assets.Character.player import Player
from Assets.Levels.levels import LevelManager
from timer import GameTimer
from useri import UI
from Assets.Animals.animal_manager import AnimalManager

#--------------------------------------------------------------------------------------------------------------------------
#The main setup.

class Game():
    def __init__(self):
        pygame.init() # Initialize pygame, must be done before using pg 
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1000, 600
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H)) # Creating a surface where the graphics can be drawn
        self.window = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H)) # Creates the actual game window
        self.font_name = pygame.font.get_default_font()
        #self.font_name = 'Testtest.ttf'
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.pause_menu = PauseMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.level_transition_menu = LevelTransitionMenu(self)
        self.victory_menu = VictoryMenu(self)
        self.curr_menu = self.main_menu
        self.player = Player(100, 400, self.DISPLAY_W, self.DISPLAY_H)
        self.level_manager = LevelManager(self)
        self.paused = False
        self.timer = GameTimer()  # Initialize the timer
        self.ui = UI(self.DISPLAY_W, self.DISPLAY_H)
        self.animal_manager = AnimalManager(self.DISPLAY_W, self.DISPLAY_H)

#--------------------------------------------------------------------------------------------------------------------------
#Main game loop :)

    def game_loop(self):
        self.level_manager.start_level(1)           # Start with level 1
        self.timer.start(45)                        # Start with 45 seconds instead of 60
        self.game_over_triggered = False            # Flag to check if game over has been triggered
        clock = pygame.time.Clock()                 # Create a clock object for frame rate control
        FPS = 60                                   # Set the desired frame rate

        while self.playing:
            clock.tick(FPS)                         # Control the frame rate
            self.check_events()                     # Checking the user input so it can act accordingly (key input)
            
            if self.BACK_KEY:                       # Pause the game when backspace is pressed
                self.paused = True
                self.timer.pause()  
                self.pause_menu.display_menu()
                self.paused = False
                self.timer.resume()  
                self.reset_keys()
                continue
                
            if not self.paused:
                self.display.fill(self.BLACK)       # Clears the screen each frame
                
                self.level_manager.update()         # Update and draw the current level
                self.level_manager.draw()
                
                self.player.move(pygame.key.get_pressed())      # Update and draw the player
                self.player.draw(self.display)
                
                # Update and draw animals
                self.animal_manager.update()
                self.animal_manager.draw(self.display)
                
                # Check for collisions and update score
                points = self.animal_manager.check_collisions(self.player.rect)
                self.player.score += points
                
                # Get required score based on level
                required_score = 150 if self.level_manager.current_level_number < 3 else 200
                
                # Check for level progression
                if self.player.score >= required_score:
                    if self.level_manager.current_level_number == 3:
                        # Show victory screen
                        self.timer.pause()
                        self.victory_menu.display_menu()
                        if not self.playing:  # If playing is False, break the loop
                            break
                        continue
                    else:
                        # Show level transition screen
                        self.timer.pause()
                        self.level_transition_menu.display_menu()
                        if not self.playing:  # If playing is False, break the loop
                            break
                        # Reset game state before advancing to next level
                        self.player = Player(100, 400, self.DISPLAY_W, self.DISPLAY_H)
                        self.animal_manager = AnimalManager(self.DISPLAY_W, self.DISPLAY_H)
                        self.level_manager.next_level()
                        self.timer.reset()
                        # Set time based on level
                        if self.level_manager.current_level_number == 3:
                            self.timer.start(30)  # 30 seconds for level 3
                        else:
                            self.timer.start(40)  # 40 seconds for other levels
                        self.game_over_triggered = False
                        self.paused = False  # Ensure game is not paused after level transition
                        continue
                
                # Update and draw UI
                self.ui.update(self.timer.get_formatted_time(), self.player.score, required_score)
                self.ui.draw(self.display)

                if self.timer.get_time_remaining() <= 0 and not self.game_over_triggered:
                    self.game_over_triggered = True
                    self.timer.pause()
                    self.game_over_menu.display_menu()
                    if not self.playing:  # If playing is False, break the loop
                        break
                    continue  # Otherwise continue the game loop
                
                self.window.blit(self.display, (0,0))
                pygame.display.update() # Update the screen to show changes
                self.reset_keys()
        
        self.timer.reset()  # Reset the timer when the game loop ends

#--------------------------------------------------------------------------------------------------------------------------
#Set up for the keybinds

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            elif event.type == pygame.KEYDOWN:  # Only check event.key when it's a KEYDOWN event
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_UP:
                    self.UP_KEY = True
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

#--------------------------------------------------------------------------------------------------------------------------
#Draws the text onto the screen

    def draw_text(self, text, size, x,y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

#--------------------------------------------------------------------------------------------------------------------------

