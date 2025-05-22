import pygame
from .animal import Animal
import os
import random

######################################### Mouse #########################################################
#This file contains the Mouse class, which is a child of the Animal class.

class Mouse(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, speed=3, points=5)
        try:
            self.image = pygame.image.load("Assets/Animals/Images/mouse.png").convert_alpha()
        except (pygame.error, FileNotFoundError):
            # Create a fallback colored rectangle if image loading fails
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 255, 0))  # Green rectangle as fallback
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.y = y
        self.rect.y = y
        self.vertical_speed = 2
        self.vertical_direction = 1
        self.direction_change_chance = 0.05
        self.vertical_change_chance = 0.03

    def move(self, screen_width, max_height):
        if not self.is_caught:
            # Update horizontal position
            self.x += self.speed * self.direction
            
            # Update vertical position
            self.y += self.vertical_speed * self.vertical_direction
            
            # Random direction changes
            if random.random() < self.direction_change_chance:
                self.direction *= -1
            
            if random.random() < self.vertical_change_chance:
                self.vertical_direction *= -1
            
            # Keep within vertical bounds
            if self.y <= max_height - 100:  # Don't go too high
                self.y = max_height - 100
                self.vertical_direction = 1
            elif self.y >= max_height - 50:  # Don't go too low
                self.y = max_height - 50
                self.vertical_direction = -1
            
            # Make mouse disappear when it goes off screen horizontally
            if self.x + self.rect.width < 0 or self.x > screen_width:
                self.is_caught = True
                return
            
            # Update rect position
            self.rect.x = self.x
            self.rect.y = self.y 