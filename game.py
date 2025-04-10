import pygame
from menu import *
from Assets.Character.player import Player
from Assets.Levels.levels import LevelManager
from timer import GameTimer

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
        self.curr_menu = self.main_menu
        self.player = Player(100, 500, self.DISPLAY_W, self.DISPLAY_H)
        self.level_manager = LevelManager(self)
        self.paused = False
        self.timer = GameTimer()  # Initialize the timer

#--------------------------------------------------------------------------------------------------------------------------
#Main game loop :)

    def game_loop(self):
        self.level_manager.start_level(1)  # Start with level 1
        self.timer.start()  # Start the timer when the game starts
        while self.playing:
            self.check_events() # Checking the user input so it can act accordingly (key input)
            
            if self.BACK_KEY:  # Pause the game when backspace is pressed
                self.paused = True
                self.timer.pause()  # Pause the timer
                self.pause_menu.display_menu()
                self.paused = False
                self.timer.resume()  # Resume the timer
                self.reset_keys()
                continue
                
            if not self.paused:
                self.display.fill(self.BLACK) # Clears the screen each frame
                
                # Update and draw the current level
                self.level_manager.update()
                self.level_manager.draw()
                
                # Update and draw the player
                self.player.move(pygame.key.get_pressed())
                self.player.draw(self.display)
                
                # Draw the timer
                self.draw_text(self.timer.get_formatted_time(), 20, self.DISPLAY_W - 100, 30)
                
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

