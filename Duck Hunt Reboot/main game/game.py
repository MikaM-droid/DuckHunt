import pygame
from menu import MainMenu

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
        self.curr_menu = MainMenu(self)

#--------------------------------------------------------------------------------------------------------------------------
#Main game loop :)

    def game_loop(self):
        while self.playing:
            self.check_events() # Checking the user input so it can act accordingly (key input)
            if self.START_KEY:
                 self.playing= False
            self.display.fill(self.BLACK) # Clears the screen each frame
            self.draw_text('Thanks for playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update() # Update the screen to show changes
            self.reset_keys()

#--------------------------------------------------------------------------------------------------------------------------

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

    def draw_text(self, text, size, x,y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

#--------------------------------------------------------------------------------------------------------------------------

