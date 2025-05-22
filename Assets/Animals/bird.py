import pygame
from .animal import Animal
import os
import random

######################################### Bird #########################################################

class Bird(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, speed=7, points=10)
        try:
            self.image = pygame.image.load("Assets/Animals/bird.png").convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((60, 60))
            self.image.fill((255, 0, 0))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vertical_speed = 4
        self.vertical_direction = random.choice([-1, 1])
        self.initial_y = y
        self.initial_speed = 7
        self.initial_vertical_speed = 4
        self.direction_change_chance = 0.03

#--------------------------------------------------------------------------------------------------------------------------

    def reset_speeds(self):
        self.speed = self.initial_speed
        self.vertical_speed = self.initial_vertical_speed
        self.vertical_direction = random.choice([-1, 1])

#--------------------------------------------------------------------------------------------------------------------------

    def move(self, screen_width, max_height):
        super().move(screen_width, max_height)
        if not self.is_caught:
            self.y += self.vertical_speed * self.vertical_direction
            
            if self.y <= 50:
                self.y = 50
                self.vertical_direction = 1
            elif self.y + self.rect.height >= max_height - 50:
                self.y = max_height - self.rect.height - 50
                self.vertical_direction = -1
            
            if random.random() < self.direction_change_chance:
                self.vertical_direction *= -1
                if random.random() < 0.3:
                    self.direction *= -1
            
            self.rect.y = self.y 