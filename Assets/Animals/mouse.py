import pygame
from .animal import Animal
import os

class Mouse(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, speed=3, points=5)
        try:
            self.image = pygame.image.load("Assets/Animals/mouse.png").convert_alpha()
        except (pygame.error, FileNotFoundError):
            # Create a fallback colored rectangle if image loading fails
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 255, 0))  # Green rectangle as fallback
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.y = y
        self.rect.y = y 