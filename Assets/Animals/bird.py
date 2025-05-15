import pygame
from .animal import Animal
import os

class Bird(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, speed=4, points=10)
        try:
            self.image = pygame.image.load("Assets/Animals/bird.png").convert_alpha()
        except (pygame.error, FileNotFoundError):
            # Create a fallback colored rectangle if image loading fails
            self.image = pygame.Surface((60, 60))
            self.image.fill((255, 0, 0))  # Red rectangle as fallback
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vertical_speed = 2
        self.vertical_direction = 1
        self.vertical_range = 100  # How far up and down the bird will fly
        self.initial_y = y

    def move(self, screen_width):
        super().move(screen_width)
        if not self.is_caught:
            self.y += self.vertical_speed * self.vertical_direction # Adding vertical movement
            if abs(self.y - self.initial_y) > self.vertical_range:
                self.vertical_direction *= -1
            self.rect.y = self.y 