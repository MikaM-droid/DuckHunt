import pygame

######################################### Player #########################################################
#This file contains the Player class, which is the main character of the game.
#It contains the move method, which moves the player across the screen.
#It also contains the draw method, which draws the player on the screen.

class Player():
    def __init__(self, x, y, screen_width, screen_height, game):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game = game
        self.width = 60
        self.height = 60
        self.speed = 5
        self.score = 0
        
        # Load and process the sprite sheet
        try:
            self.sprite_sheet = pygame.image.load("Assets/Character/Images/kitty_1.png").convert_alpha()
            self.frame_width = 32
            self.frame_height = 32
            self.frames_left = []
            self.frames_right = []
            
            # Extract frames for running left (top row)
            for i in range(4):
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
                frame = pygame.transform.scale(frame, (self.width, self.height))
                self.frames_left.append(frame)
            
            # Extract frames for running right (bottom row)
            for i in range(4):
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, self.frame_height, self.frame_width, self.frame_height))
                frame = pygame.transform.scale(frame, (self.width, self.height))
                self.frames_right.append(frame)
            
            self.current_frame = 0
            self.animation_timer = 0
            self.animation_delay = 100
            self.facing_right = True
            self.image = self.frames_right[0]
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))
            self.frames_left = [self.image]
            self.frames_right = [self.image]
            self.current_frame = 0
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Physics properties
        self.jump_power = -20
        self.gravity = 0.8
        self.velocity_y = 0
        self.float_height = self.screen_height - 120
        self.can_jump = True
        self.max_jump_height = 200
        self.initial_jump_y = 0

#--------------------------------------------------------------------------------------------------------------------------

    def move(self, keys):
        is_moving = False
        
        # Horizontal movement
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.facing_right = False
            is_moving = True
        if keys[pygame.K_d]:
            self.x += self.speed
            self.facing_right = True
            is_moving = True
            
        # Keep player within screen bounds
        self.x = max(0, min(self.x, self.screen_width - self.width))
        self.rect.x = self.x
        
        # Update animation
        current_time = pygame.time.get_ticks()
        if is_moving and current_time - self.animation_timer > self.animation_delay:
            self.animation_timer = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames_right)
            self.image = self.frames_right[self.current_frame] if self.facing_right else self.frames_left[self.current_frame]
        elif not is_moving:
            self.image = self.frames_right[0] if self.facing_right else self.frames_left[0]
            self.current_frame = 0

        # Handle jumping
        if keys[pygame.K_w] and self.can_jump:
            self.velocity_y = self.jump_power
            self.can_jump = False
            self.initial_jump_y = self.rect.y
            self.game.audio_manager.play_jump_sound()

        # Apply gravity and update vertical position
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check max jump height
        if not self.can_jump and self.rect.y <= self.initial_jump_y - self.max_jump_height:
            self.velocity_y = 0
            self.rect.y = self.initial_jump_y - self.max_jump_height

        # Ground collision
        if self.rect.bottom > self.float_height:
            self.rect.bottom = self.float_height
            self.velocity_y = 0
            self.can_jump = True

        # Boundary checks
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.screen_width, self.rect.right)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0

#--------------------------------------------------------------------------------------------------------------------------
#Draws the player on the screen

    def draw(self, screen):
        screen.blit(self.image, self.rect)
