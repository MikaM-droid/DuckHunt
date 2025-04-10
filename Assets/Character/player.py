import pygame

class Player():
    def __init__(self, x, y, screen_width, screen_height):
        self.image = pygame.image.load("Assets/Character/cat.png")
        self.image = pygame.transform.scale(self.image, (100, 100)) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 3  #Horizontal movement speed
        self.jump_power = -12  #Jump velocity
        self.gravity = 0.5  #Gravity strength
        self.velocity_y = 0  #Vertical movement speed
        self.on_ground = True  #Check if the player is on the ground

    def move(self, keys):
        # Store the previous position
        prev_x = self.rect.x
        prev_y = self.rect.y

        # Handle horizontal movement
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        # Handle jumping
        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False  # Player is in the air

        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

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
        # Bottom boundary (ground)
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
            self.velocity_y = 0
            self.on_ground = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
