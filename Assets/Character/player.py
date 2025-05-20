import pygame

class Player():
    def __init__(self, x, y, screen_width, screen_height):
        self.image = pygame.image.load("Assets/Character/cat.png")
        self.image = pygame.transform.scale(self.image, (100, 100)) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.score = 0                                                 # Player's score
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 5                                                 #Horizontal movement speed
        self.jump_power = -20                                          #Jump velocity
        self.gravity = 0.8                                            #Gravity strength
        self.velocity_y = 0                                           #Vertical movement speed
        self.float_height = self.screen_height - 120                   # Position above UI bar
        self.can_jump = True                                          # Flag to control jumping
        self.max_jump_height = 200                                    # Maximum jump height
        self.initial_jump_y = 0                                       # Starting Y position of jump

    def move(self, keys):
        # Handle horizontal movement
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

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

        # Boundary checks
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)
