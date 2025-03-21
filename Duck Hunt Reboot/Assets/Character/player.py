import pygame

class Player():
    def __init__(self, x, y):
        self.image = pygame.image.load("Duck Hunt Reboot/Assets/Character/cat.png")
        self.image = pygame.transform.scale(self.image, (50, 50)) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.speed = 5  #Horizontal movement speed
        self.jump_power = -12  #Jump velocity
        self.gravity = 0.5  #Gravity strength
        self.velocity_y = 0  #Vertical movement speed
        self.on_ground = True  #Check if the player is on the ground

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False  # Player is in the air

        #Gravity applying
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        #Collision with the ground (temporary ground level at y=500)
        if self.rect.y >= 500:
            self.rect.y = 500
            self.velocity_y = 0
            self.on_ground = True  # Reset jump when touching the ground

    def draw(self, screen):
        screen.blit(self.image, self.rect)
