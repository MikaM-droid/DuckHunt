import pygame

######################################### Player #########################################################
#This file contains the Player class, which is the main character of the game.
#It contains the move method, which moves the player across the screen.
#It also contains the draw method, which draws the player on the screen.

class Player():
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 60
        self.height = 60
        self.speed = 5
        self.score = 0
        
        # Load and process the sprite sheet
        try:
            self.sprite_sheet = pygame.image.load("Assets/Character/Images/kitty_1.png").convert_alpha()
            self.frame_width = 32  # Each frame is 32x32
            self.frame_height = 32
            self.frames_left = []  # Top row - running left
            self.frames_right = []  # Bottom row - running right
            
            # Extract frames for running left (top row)
            for i in range(4):  # Assuming 4 frames per row
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
            self.animation_delay = 100  # milliseconds between frame changes
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
        
        self.jump_power = -20                                          #Jump velocity
        self.gravity = 0.8                                            #Gravity strength
        self.velocity_y = 0                                           #Vertical movement speed
        self.float_height = self.screen_height - 120                   # Position above UI bar
        self.can_jump = True                                          # Flag to control jumping
        self.max_jump_height = 200                                    # Maximum jump height
        self.initial_jump_y = 0                                       # Starting Y position of jump

#--------------------------------------------------------------------------------------------------------------------------

    def move(self, keys):
        is_moving = False
        
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.facing_right = False
            is_moving = True
        if keys[pygame.K_d]:
            self.x += self.speed
            self.facing_right = True
            is_moving = True
            
        # Keep player within screen bounds
        if self.x < 0:
            self.x = 0
        elif self.x > self.screen_width - self.width:
            self.x = self.screen_width - self.width
            
        self.rect.x = self.x
        
        # Update animation only when moving
        if is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > self.animation_delay:
                self.animation_timer = current_time
                self.current_frame = (self.current_frame + 1) % len(self.frames_right)
                self.image = self.frames_right[self.current_frame] if self.facing_right else self.frames_left[self.current_frame]
        else:
            # Reset to first frame when not moving
            self.image = self.frames_right[0] if self.facing_right else self.frames_left[0]
            self.current_frame = 0

        # Handle jumping
        if keys[pygame.K_w] and self.can_jump:
            self.velocity_y = self.jump_power
            self.can_jump = False
            self.initial_jump_y = self.rect.y

        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check if we've reached max jump height
        if not self.can_jump and self.rect.y <= self.initial_jump_y - self.max_jump_height:
            self.velocity_y = 0
            self.rect.y = self.initial_jump_y - self.max_jump_height

        # Keep character floating at desired height
        if self.rect.bottom > self.float_height:
            self.rect.bottom = self.float_height
            self.velocity_y = 0
            self.can_jump = True  # Reset jump ability when touching the ground

        # Boundary checks------------- Makes sure the player doesn't go out of bounds
        # Left boundary
        if self.rect.left < 0:
            self.rect.left = 0
        # Right boundary
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        # Top boundary
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0

#--------------------------------------------------------------------------------------------------------------------------
#Draws the player on the screen

    def draw(self, screen):
        screen.blit(self.image, self.rect)
