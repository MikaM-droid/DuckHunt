import pygame
from menu import MainMenu, OptionsMenu, CreditsMenu, PauseMenu, GameOverMenu, LevelTransitionMenu, VictoryMenu
from Assets.Character.player import Player
from Assets.Levels.levels import LevelManager
from timer import GameTimer
from useri import UI
from Assets.Animals.animal_manager import AnimalManager
from Assets.Audio.audio_manager import AudioManager

#--------------------------------------------------------------------------------------------------------------------------
#The main setup.

class Game():
    def __init__(self):
        pygame.init() # Initialize pygame, must be done before using pg 
        self.running, self.playing = True, False # Running is true, playing is false
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False # Keybinds
        self.DISPLAY_W, self.DISPLAY_H = 1000, 600 # Display width and height
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H)) # Creating a surface where the graphics can be drawn
        self.window = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H)) # Creates the actual game window
        self.font_name = pygame.font.get_default_font() # Font name
        #self.font_name = 'Testtest.ttf'
        self.BLACK, self.WHITE = (0,0,0), (255,255,255) # Colors
        self.main_menu = MainMenu(self) # Main menu
        self.options = OptionsMenu(self) # Options menu
        self.credits = CreditsMenu(self) # Credits menu
        self.pause_menu = PauseMenu(self) # Pause menu
        self.game_over_menu = GameOverMenu(self) # Game over menu
        self.level_transition_menu = LevelTransitionMenu(self) # Level transition menu
        self.victory_menu = VictoryMenu(self) # Victory menu
        self.curr_menu = self.main_menu # Current menu
        self.player = Player(100, 400, self.DISPLAY_W, self.DISPLAY_H, self) # Player
        self.level_manager = LevelManager(self) # Level manager
        self.paused = False # Paused
        self.timer = GameTimer()  # Initialize the timer
        self.ui = UI(self.DISPLAY_W, self.DISPLAY_H) # UI
        self.animal_manager = AnimalManager(self.DISPLAY_W, self.DISPLAY_H) # Animal manager
        self.audio_manager = AudioManager()  # Initialize the audio manager
        self.audio_manager.play_menu_music()  # Start playing menu music
        self.last_completed_level = 0  # Track the last completed level

#--------------------------------------------------------------------------------------------------------------------------
#Main game loop :)

    def game_loop(self):
        self.level_manager.start_level(self.last_completed_level + 1) # Start from the next level after last completed
        self.timer.start(45) # Start with 45 seconds
        self.game_over_triggered = False # Flag to check if game over has been triggered
        clock = pygame.time.Clock() # Create a clock object for frame rate control
        FPS = 60 # Set the desired frame rate

        while self.playing:
            clock.tick(FPS) # Control the frame rate
            self.check_events() # Checking the user input so it can act accordingly (key input)
            
            if self.BACK_KEY: # Pause the game when backspace is pressed
                self.paused = True
                self.timer.pause()  
                self.pause_menu.display_menu()
                self.paused = False
                self.timer.resume()  
                self.reset_keys()
                continue
                
            if not self.paused:
                # Clears the screen each frame
                self.display.fill(self.BLACK)      
                
                # Reset sound flags if needed
                self.audio_manager.reset_sound_flags()
                
                # Update and draw the current level
                self.level_manager.update()        
                self.level_manager.draw()
                
                # Update and draw the player
                self.player.move(pygame.key.get_pressed())     
                self.player.draw(self.display)
                
                # Update and draw animals
                self.animal_manager.update()
                self.animal_manager.draw(self.display)
                
                # Check for collisions and update score
                points = self.animal_manager.check_collisions(self.player.rect)
                self.player.score += points
                
                # Get required score based on level
                required_score = 100 if self.level_manager.current_level_number == 1 else (125 if self.level_manager.current_level_number == 2 else 150)
                
                # Check for level progression
                if self.player.score >= required_score:
                    if self.level_manager.current_level_number == 3:
                        # Show victory screen
                        self.timer.pause() # Pause the timer
                        self.audio_manager.play_win_sound()  # Play win sound
                        self.last_completed_level = 3  # Update last completed level
                        self.victory_menu.display_menu() # Display the victory menu
                        if not self.playing:  # If playing is False, break the loop
                            break
                        continue
                    else:
                        # Show level transition screen
                        self.timer.pause() # Pause the timer
                        self.audio_manager.play_win_sound()  # Play win sound for level completion
                        self.last_completed_level = self.level_manager.current_level_number  # Update last completed level
                        self.level_transition_menu.display_menu() # Display the level transition menu
                        if not self.playing:  # If playing is False, break the loop
                            break
                        continue
                
                # Update and draw UI
                self.ui.update(self.timer.get_formatted_time(), self.player.score, required_score)
                self.ui.draw(self.display)

                if self.timer.get_time_remaining() <= 0 and not self.game_over_triggered:
                    self.game_over_triggered = True
                    self.timer.pause()
                    self.audio_manager.play_game_over_sound()  # Play game over sound
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
        font = pygame.font.Font(self.font_name, size) # Font
        text_surface = font.render(text, True, self.WHITE) # Render the text
        text_rect = text_surface.get_rect() # Get the rect of the text
        text_rect.center = (x, y) # Center the text
        self.display.blit(text_surface, text_rect) # Blit the text onto the screen

