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
            # Load and process the sprite sheet
            self.sprite_sheet = pygame.image.load("Assets/Animals/Images/walking.png").convert_alpha()
            self.frame_width = 16  # 16x16 pixel frames
            self.frame_height = 16
            self.frames = []
            
            # Extract frames from the sprite sheet (4 frames)
            for i in range(4):
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
                frame = pygame.transform.scale(frame, (40, 40))  # Scale up to 40x40
                self.frames.append(frame)
            
            self.current_frame = 0
            self.animation_timer = 0
            self.animation_delay = 100  # milliseconds between frame changes
            self.image = self.frames[0]
        except (pygame.error, FileNotFoundError):
            # Create a fallback colored rectangle if image loading fails
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 255, 0))  # Green rectangle as fallback
            self.frames = [self.image]
            self.current_frame = 0
        
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
            
            # Update animation
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > self.animation_delay:
                self.animation_timer = current_time
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                # Flip the image based on direction
                if self.direction < 0:
                    self.image = pygame.transform.flip(self.image, True, False) 