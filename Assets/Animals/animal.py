import pygame
import random

######################################### Animal #########################################################
#This file contains the Animal class, which is the base class for all animals in the game.
#It contains the move method, which moves the animal across the screen.
#It also contains the check_collision method, which checks if the animal has collided with the player.

class Animal:
    def __init__(self, x, y, speed, points):
        self.x = x
        self.y = y
        self.speed = speed
        self.points = points
        self.rect = None
        self.direction = 1  # 1 for right, -1 for left
        self.is_caught = False

#--------------------------------------------------------------------------------------------------------------------------

    def move(self, screen_width, max_height):
        if not self.is_caught:
            # Update horizontal position
            self.x += self.speed * self.direction
            
            # Keep within screen bounds
            if self.x <= 0:
                self.x = 0
                self.direction = 1
            elif self.x + self.rect.width >= screen_width:
                self.x = screen_width - self.rect.width
                self.direction = -1
            
            # Update rect position
            self.rect.x = self.x
            self.rect.y = self.y

#--------------------------------------------------------------------------------------------------------------------------

    def draw(self, screen):
        if not self.is_caught:
            screen.blit(self.image, self.rect)

#--------------------------------------------------------------------------------------------------------------------------

    def check_collision(self, player_rect):
        if not self.is_caught and self.rect.colliderect(player_rect):
            self.is_caught = True
            return self.points
        return 0
