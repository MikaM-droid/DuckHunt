import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

#--------------------------------------------------------------------------------------------------------------------------

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

#--------------------------------------------------------------------------------------------------------------------------

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

#######################################    Main menu    ###################################################################

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

#--------------------------------------------------------------------------------------------------------------------------
# Draws text for the main menu

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

#--------------------------------------------------------------------------------------------------------------------------
#Scrolling through the menu with the up and down keys

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

#--------------------------------------------------------------------------------------------------------------------------
#Directs to the other page when clicked on enter

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.game.reset_keys()  # Added key reset after starting game
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

#######################################    Options menu    #################################################################

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

#--------------------------------------------------------------------------------------------------------------------------

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()  # <-- Make sure to call this
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Volume', 15, self.volx, self.voly)
            self.game.draw_text('Controls', 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

#--------------------------------------------------------------------------------------------------------------------------

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY:  # Separate UP and DOWN checks
            if self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
        elif self.game.START_KEY:
            # TODO: Create a control and volume menu. 
            pass

#######################################    Credits menu    ###############################################################

class CreditsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:  # Only backspace returns to main menu
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by Mikaela Monsma', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()

class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Resume'
        self.resumex, self.resumey = self.mid_w, self.mid_h + 30
        self.mainmenux, self.mainmenuy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Paused', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Resume", 20, self.resumex, self.resumey)
            self.game.draw_text("Main Menu", 20, self.mainmenux, self.mainmenuy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Resume':
                self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Main Menu'
            elif self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
                self.state = 'Resume'
        elif self.game.UP_KEY:
            if self.state == 'Resume':
                self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Main Menu'
            elif self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
                self.state = 'Resume'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Resume':
                self.game.playing = True
                self.run_display = False
            elif self.state == 'Main Menu':
                self.game.playing = False
                self.game.curr_menu = self.game.main_menu
                self.run_display = False