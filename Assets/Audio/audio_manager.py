import pygame

########################################### Audio Manager ###############################################

class AudioManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load music
        self.menu_music = "Assets/Audio/Music/roa-music-walk-around(chosic.com).mp3"
        
        # Load sound effects
        self.win_sound = pygame.mixer.Sound("Assets/Audio/Sound effects/8-bit-video-game-win-level-sound-version-1-145827.mp3")
        self.jump_sound = pygame.mixer.Sound("Assets/Audio/Sound effects/cartoon-jump-6462.mp3")
        self.game_over_sound = pygame.mixer.Sound("Assets/Audio/Sound effects/game-over-arcade-6435.mp3")
        self.game_start_sound = pygame.mixer.Sound("Assets/Audio/Sound effects/game-start-317318.mp3")
        
        # Set volume for all sounds (0.0 to 1.0)
        self.win_sound.set_volume(0.5)
        self.jump_sound.set_volume(0.5)
        self.game_over_sound.set_volume(0.5)
        self.game_start_sound.set_volume(0.5)
        
        # Flag to track if game over sound has been played to prevent it from playing multiple times
        self.game_over_played = False
        self.win_sound_played = False
        self.current_sound = None

#----------------------------------------------------------------------------------------------------------
#Play the menu music
    
    def play_menu_music(self):
        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely, so it plays the music over and over again

#----------------------------------------------------------------------------------------------------------
#Stop the menu music

    def stop_menu_music(self):
        pygame.mixer.music.stop()

#----------------------------------------------------------------------------------------------------------
#Play the win sound

    def play_win_sound(self):
        if not self.win_sound_played:
            self.win_sound.play()
            self.win_sound_played = True
            self.current_sound = self.win_sound

#----------------------------------------------------------------------------------------------------------
#Play the jump sound

    def play_jump_sound(self):
        self.jump_sound.play()

#----------------------------------------------------------------------------------------------------------
#Play the game over sound

    def play_game_over_sound(self):
        if not self.game_over_played:
            self.game_over_sound.play()
            self.game_over_played = True
            self.current_sound = self.game_over_sound

#----------------------------------------------------------------------------------------------------------
#Play the game start sound

    def play_game_start_sound(self):
        self.game_start_sound.play()

#----------------------------------------------------------------------------------------------------------
#Reset the sound flags

    def reset_sound_flags(self):
        # Only reset flags if the current sound has finished playing
        if self.current_sound and not self.current_sound.get_num_channels():
            self.game_over_played = False
            self.win_sound_played = False
            self.current_sound = None 