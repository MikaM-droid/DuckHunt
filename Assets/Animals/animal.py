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
## Reset speeds to initial values

    def move(self, screen_width, max_height):
        if not self.is_caught:
            # Update horizontal position
            self.x += self.speed * self.direction
            
            # Make animal disappear when it goes off screen
            if self.x + self.rect.width < 0 or self.x > screen_width:
                self.is_caught = True
                return
            
            # Update rect position
            self.rect.x = self.x
            self.rect.y = self.y

#--------------------------------------------------------------------------------------------------------------------------
# Draw the animal on the screen

    def draw(self, screen):
        if not self.is_caught:
            screen.blit(self.image, self.rect)

#--------------------------------------------------------------------------------------------------------------------------
# Check for collision with the player

    def check_collision(self, player_rect):
        if not self.is_caught and self.rect.colliderect(player_rect):
            self.is_caught = True
            return self.points
        return 0
