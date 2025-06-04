import pygame
from Assets.Character.player import Player
from Assets.Animals.animal_manager import AnimalManager

######################################### Menu #########################################################

class Menu():
    '''
    Base menu class that provides common functionality for all game menus.
    
    Attributes:
        game: Reference to the main game instance
        mid_w, mid_h: Middle coordinates of the display
        run_display: Boolean to control menu display loop
        cursor_rect: Pygame Rect object for menu cursor
        offset: Offset for cursor positioning
        bg_image: Background image for the menu
    '''
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100
        # Load and scale the background image
        self.bg_image = pygame.image.load("Assets/bgs/mainimg.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.game.DISPLAY_W, self.game.DISPLAY_H))

#--------------------------------------------------------------------------------------------------------------------------

    def draw_cursor(self):
        '''
        Draws the cursor (*) at its current position.
        '''
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

#--------------------------------------------------------------------------------------------------------------------------

    def blit_screen(self):
        '''
        Updates the display by blitting the game surface to the window.
        Also updates pygame display and resets key states.
        '''
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

#######################################    Main menu    ###################################################################

class MainMenu(Menu):
    '''
    Main menu of the game with options to start game, view options, credits, or quit.
    
    Attributes:
        state: Current selected menu option
        startx, starty: Coordinates for Start Game option
        optionsx, optionsy: Coordinates for Options option
        creditsx, creditsy: Coordinates for Credits option
        quitx, quity: Coordinates for Quit option
    '''
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Start'
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.quitx, self.quity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

#--------------------------------------------------------------------------------------------------------------------------

    def display_menu(self):
        '''
        Main menu display loop.
        Handles user input and renders menu options.
        '''
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            # Draw the background image instead of filling with black
            self.game.display.blit(self.bg_image, (0, 0))
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.game.draw_text("Quit Game", 20, self.quitx, self.quity + 40)
            self.draw_cursor()
            self.blit_screen()

#--------------------------------------------------------------------------------------------------------------------------

    def move_cursor(self):
        '''
        Handles cursor movement between menu options using UP and DOWN keys.
        Updates cursor position and current state accordingly.
        '''
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity + 40)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity + 40)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

#--------------------------------------------------------------------------------------------------------------------------

    def check_input(self):
        '''
        Handles menu option selection and game state transitions.
        Processes START_KEY to navigate between menus or start the game.
        '''
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                # Reset to level 1 if all levels are completed
                if self.game.last_completed_level >= 3:
                    self.game.last_completed_level = 0
                # Reset game state but keep last completed level
                self.game.level_manager.start_level(1)  # Always start from level 1
                self.game.player = Player(100, 400, self.game.DISPLAY_W, self.game.DISPLAY_H, self.game)
                self.game.animal_manager = AnimalManager(self.game.DISPLAY_W, self.game.DISPLAY_H)
                self.game.timer.reset()
                self.game.timer.start(45)
                self.game.game_over_triggered = False
                self.game.playing = True
                self.game.reset_keys()  # Added key reset after starting game
                self.game.audio_manager.reset_sound_flags()  # Reset sound flags
                self.game.audio_manager.stop_menu_music()  # Stop menu music
                self.game.audio_manager.play_game_start_sound()  # Play game start sound
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Quit':
                pygame.quit()
                exit()
            self.run_display = False

#######################################    Options menu    #################################################################

class OptionsMenu(Menu):
    '''
    Options menu for game settings like volume and controls.
    
    Attributes:
        state: Current selected option
        volx, voly: Coordinates for Volume option
        controlsx, controlsy: Coordinates for Controls option
    '''
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

#--------------------------------------------------------------------------------------------------------------------------

    def display_menu(self):
        '''
        Options menu display loop.
        Renders options menu and handles user input.
        '''
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
        '''
        Handles options menu navigation and selection.
        Processes BACK_KEY to return to main menu and UP/DOWN keys for option selection.
        '''
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.game.audio_manager.play_menu_music()  # Start menu music
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
    '''
    Credits menu displaying game credits and author information.
    '''
    def __init__(self, game):
        super().__init__(game)

#--------------------------------------------------------------------------------------------------------------------------

    def display_menu(self):
        '''
        Credits menu display loop.
        Shows credits information and handles return to main menu.
        '''
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:  # Only backspace returns to main menu
                self.game.curr_menu = self.game.main_menu
                self.game.audio_manager.play_menu_music()  # Start menu music
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by Mikaela Monsma', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()


#######################################    Pause menu    ###############################################################

class PauseMenu(Menu):
    '''
    Pause menu that appears during gameplay.
    
    Attributes:
        state: Current selected option
        resumex, resumey: Coordinates for Resume option
        mainmenux, mainmenuy: Coordinates for Main Menu option
    '''
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Resume'
        self.resumex, self.resumey = self.mid_w, self.mid_h + 30
        self.mainmenux, self.mainmenuy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)

#--------------------------------------------------------------------------------------------------------------------------

    def display_menu(self):
        '''
        Pause menu display loop.
        Shows pause options and handles user input.
        '''
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

#--------------------------------------------------------------------------------------------------------------------------

    def move_cursor(self):
        '''
        Handles cursor movement between pause menu options.
        Updates cursor position and current state based on UP/DOWN key input.
        '''
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

#--------------------------------------------------------------------------------------------------------------------------

    def check_input(self):
        '''
        Handles pause menu option selection.
        Processes START_KEY to resume game or return to main menu.
        '''
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Resume':
                self.game.playing = True
                self.run_display = False
            elif self.state == 'Main Menu':
                self.game.playing = False
                self.game.player.score = 0  # Reset the score
                self.game.curr_menu = self.game.main_menu
                self.game.audio_manager.play_menu_music()  # Start menu music
                self.run_display = False

#######################################    Game over menu    ###############################################################

class GameOverMenu(Menu):
    '''
    Game over menu displayed when player loses.
    
    Attributes:
        state: Current selected option
        playagainx, playagainy: Coordinates for Play Again option
        mainmenux, mainmenuy: Coordinates for Main Menu option
    '''
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Play Again'
        self.playagainx, self.playagainy = self.mid_w, self.mid_h + 30
        self.mainmenux, self.mainmenuy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.playagainx + self.offset, self.playagainy)

#--------------------------------------------------------------------------------------------------------------------------

    def display_menu(self):
        '''
        Game over menu display loop.
        Shows game over options and handles user input.
        '''
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Game Over', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Play Again", 20, self.playagainx, self.playagainy)
            self.game.draw_text("Main Menu", 20, self.mainmenux, self.mainmenuy)
            self.draw_cursor()
            self.blit_screen()

#--------------------------------------------------------------------------------------------------------------------------

    def move_cursor(self):
        '''
        Handles cursor movement between game over menu options.
        Updates cursor position and current state based on UP/DOWN key input.
        '''
        if self.game.DOWN_KEY:
            if self.state == 'Play Again':
                self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Main Menu'
            elif self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.playagainx + self.offset, self.playagainy)
                self.state = 'Play Again'
        elif self.game.UP_KEY:
            if self.state == 'Play Again':
                self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Main Menu'
            elif self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.playagainx + self.offset, self.playagainy)
                self.state = 'Play Again'

#--------------------------------------------------------------------------------------------------------------------------

    def check_input(self):
        '''
        Handles game over menu option selection.
        Processes START_KEY to restart game or return to main menu.
        '''
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Play Again':
                # Always start from level 1 when clicking Play Again
                self.game.level_manager.start_level(1)
                self.game.player = Player(100, 400, self.game.DISPLAY_W, self.game.DISPLAY_H, self.game)
                self.game.animal_manager = AnimalManager(self.game.DISPLAY_W, self.game.DISPLAY_H)
                self.game.timer.reset()
                self.game.timer.start(45)
                self.game.game_over_triggered = False
                self.game.playing = True
                # Don't reset sound flags here - let the audio manager handle it!!
                self.run_display = False
                return  # Add return to prevent further execution
            elif self.state == 'Main Menu':
                self.game.playing = False
                self.game.player.score = 0  # Reset the score
                self.game.last_completed_level = 0  # Reset last completed level
                self.game.curr_menu = self.game.main_menu
                self.game.audio_manager.play_menu_music()  # Start menu music
                self.run_display = False

#######################################    Level Transition Menu    ###############################################################

class LevelTransitionMenu(Menu):
    '''
    Menu displayed between levels.
    
    Attributes:
        state: Current selected option
        nextlevelx, nextlevely: Coordinates for Next Level option
        mainmenux, mainmenuy: Coordinates for Main Menu option
    '''
    def __init__(self, game):
        '''
        Initializes the LevelTransitionMenu.
        '''
        Menu.__init__(self, game)
        self.state = 'Next Level'
        self.nextlevelx, self.nextlevely = self.mid_w, self.mid_h + 30
        self.mainmenux, self.mainmenuy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.nextlevelx + self.offset, self.nextlevely)

#--------------------------------------------------------------------------------------------------------------------------

    def display_menu(self):
        '''
        Level transition menu display loop.
        Shows level completion and handles user input.
        '''
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(f'Level {self.game.level_manager.current_level_number} Complete!', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Next Level", 20, self.nextlevelx, self.nextlevely)
            self.game.draw_text("Main Menu", 20, self.mainmenux, self.mainmenuy)
            self.draw_cursor()
            self.blit_screen()

#--------------------------------------------------------------------------------------------------------------------------

    def move_cursor(self):
        '''
        Handles cursor movement between level transition menu options.
        Updates cursor position and current state based on UP/DOWN key input.
        '''
        if self.game.DOWN_KEY:
            if self.state == 'Next Level':
                self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Main Menu'
            elif self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.nextlevelx + self.offset, self.nextlevely)
                self.state = 'Next Level'
        elif self.game.UP_KEY:
            if self.state == 'Next Level':
                self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Main Menu'
            elif self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.nextlevelx + self.offset, self.nextlevely)
                self.state = 'Next Level'

#--------------------------------------------------------------------------------------------------------------------------

    def check_input(self):
        '''
        Handles level transition menu option selection.
        Processes START_KEY to advance to next level or return to main menu.
        '''
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Next Level':
                # Reset game state before advancing to next level
                self.game.player = Player(100, 400, self.game.DISPLAY_W, self.game.DISPLAY_H, self.game)
                self.game.animal_manager = AnimalManager(self.game.DISPLAY_W, self.game.DISPLAY_H)
                self.game.level_manager.next_level()
                self.game.timer.reset()
                self.game.timer.start(45)  # Standard 45 seconds for all levels
                self.game.game_over_triggered = False
                self.game.paused = False  # Ensure game is not paused after level transition
                self.game.playing = True
                self.run_display = False
            elif self.state == 'Main Menu':
                self.game.playing = False
                self.game.curr_menu = self.game.main_menu
                self.game.audio_manager.play_menu_music()  # Start menu music
                self.run_display = False

#######################################    Victory Menu    ###############################################################

class VictoryMenu(Menu):
    '''
    Victory menu displayed when player completes all levels.
    
    Attributes:
        state: Current selected option
        playagainx, playagainy: Coordinates for Play Again option
        mainmenux, mainmenuy: Coordinates for Main Menu option
    '''
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Play Again'
        self.playagainx, self.playagainy = self.mid_w, self.mid_h + 30
        self.mainmenux, self.mainmenuy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.playagainx + self.offset, self.playagainy)

#--------------------------------------------------------------------------------------------------------------------------

    def display_menu(self):
        '''
        Victory menu display loop.
        Shows victory message and handles user input.
        '''
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Victory!', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Play Again", 20, self.playagainx, self.playagainy)
            self.game.draw_text("Main Menu", 20, self.mainmenux, self.mainmenuy)
            self.draw_cursor()
            self.blit_screen()

#--------------------------------------------------------------------------------------------------------------------------

    def move_cursor(self):
        '''
        Handles cursor movement between victory menu options.
        Updates cursor position and current state based on UP/DOWN key input.
        '''
        if self.game.DOWN_KEY:
            if self.state == 'Play Again':
                self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Main Menu'
            elif self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.playagainx + self.offset, self.playagainy)
                self.state = 'Play Again'
        elif self.game.UP_KEY:
            if self.state == 'Play Again':
                self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Main Menu'
            elif self.state == 'Main Menu':
                self.cursor_rect.midtop = (self.playagainx + self.offset, self.playagainy)
                self.state = 'Play Again'

#--------------------------------------------------------------------------------------------------------------------------

    def check_input(self):
        '''
        Handles victory menu option selection.
        Processes START_KEY to restart game or return to main menu.
        '''
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Play Again':
                # Reset to level 1 if all levels are completed
                if self.game.last_completed_level >= 3:
                    self.game.last_completed_level = 0
                # Reset game state but keep last completed level
                self.game.level_manager.start_level(self.game.last_completed_level + 1)
                self.game.player = Player(100, 400, self.game.DISPLAY_W, self.game.DISPLAY_H, self.game)
                self.game.animal_manager = AnimalManager(self.game.DISPLAY_W, self.game.DISPLAY_H)
                self.game.timer.reset()
                self.game.timer.start(45)
                self.game.game_over_triggered = False
                self.game.playing = True
                # Don't reset sound flags here - let the audio manager handle it
                self.run_display = False
                return
            elif self.state == 'Main Menu':
                self.game.playing = False
                self.game.curr_menu = self.game.main_menu
                self.game.audio_manager.play_menu_music()  # Start menu music
                self.run_display = False