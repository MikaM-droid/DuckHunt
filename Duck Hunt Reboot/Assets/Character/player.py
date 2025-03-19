import pygame

class Player():
    def __init__(self, x, y):
        self.image = pygame.image.load("Duck Hunt Reboot/Assets/Character/cat.png")  # Load player sprite
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5  # Movement speed

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

