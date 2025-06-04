import pygame
from .animal import Animal
import os
import random

######################################### Bird #########################################################

class Bird(Animal):
    '''
    Bird class.

    Attributes:
        x (int): The x coordinate of the bird.
        y (int): The y coordinate of the bird.
        speed (int): The speed of the bird.
        points (int): The points of the bird.
    '''
    def __init__(self, x, y):
        '''
        Initialize the Bird class.

        Args:
            x (int): The x coordinate of the bird.
            y (int): The y coordinate of the bird.
        '''
        super().__init__(x, y, speed=7, points=10)
        # Load and process the sprite sheet
        try:
            self.sprite_sheet = pygame.image.load("Assets/Animals/Images/BirdFly.png").convert_alpha()
            self.frame_width = self.sprite_sheet.get_width() // 8  # 8 frames in the sprite sheet
            self.frame_height = self.sprite_sheet.get_height()
            self.frames = []
            
            # Extract individual frames from the sprite sheet
            for i in range(8):
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
                frame = pygame.transform.scale(frame, (60, 60))  # Scale the frame
                self.frames.append(frame)
            
            self.current_frame = 0
            self.animation_timer = 0
            self.animation_delay = 100  # milliseconds between frame changes
            self.image = self.frames[0]
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((60, 60))
            self.image.fill((255, 0, 0))
            self.frames = [self.image]
            self.current_frame = 0
        
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
        '''
        Reset the speeds to initial values.
        '''
        self.speed = self.initial_speed
        self.vertical_speed = self.initial_vertical_speed
        self.vertical_direction = random.choice([-1, 1])

#--------------------------------------------------------------------------------------------------------------------------
# Move the bird, the bird moves up and down, and changes direction randomly

    def move(self, screen_width, max_height):
        '''
        Move the bird.

        Args:
            screen_width (int): The width of the screen.
            max_height (int): The height of the screen.
        '''
        super().move(screen_width, max_height)
        if not self.is_caught:
            self.y += self.vertical_speed * self.vertical_direction
            
            # Check for boundaries
            if self.y <= 50:
                self.y = 50
                self.vertical_direction = 1
            elif self.y + self.rect.height >= max_height - 50:
                self.y = max_height - self.rect.height - 50
                self.vertical_direction = -1
            
            # Randomly change direction
            if random.random() < self.direction_change_chance:
                self.vertical_direction *= -1
                if random.random() < 0.3:
                    self.direction *= -1
            
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