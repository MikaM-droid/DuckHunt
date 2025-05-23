import pygame
import random
from .bird import Bird
from .mouse import Mouse

######################################### Animal Manager #########################################################
## This file contains the AnimalManager class, which manages the spawning and updating of animals in the game.

class AnimalManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.animals = []
        self.spawn_delay = 800
        self.last_spawn_time = pygame.time.get_ticks()
        self.ui_height = 100
        self.bird_speed = 7
        self.mouse_speed = 6

#--------------------------------------------------------------------------------------------------------------------------
# Spawn animals at random intervals
# Animals spawn from the left or right side of the screen

    def spawn_animal(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.last_spawn_time = current_time
            spawn_side = random.choice(['left', 'right'])
            x = 0 if spawn_side == 'left' else self.screen_width
            
            if random.random() < 0.4:  # 40% chance for bird
                max_height = self.screen_height - self.ui_height - 100
                y = random.randint(100, max_height)
                bird = Bird(x, y)
                bird.speed = self.bird_speed
                bird.direction = 1 if spawn_side == 'left' else -1
                self.animals.append(bird)
            else:  # 60% chance for mouse
                y = self.screen_height - self.ui_height - 50
                mouse = Mouse(x, y)
                mouse.speed = self.mouse_speed
                mouse.direction = 1 if spawn_side == 'left' else -1
                self.animals.append(mouse)

#--------------------------------------------------------------------------------------------------------------------------
# Update the positions of all animals, animals move across the screen and disappear when they go off screen

    def update(self):
        self.spawn_animal()
        for animal in self.animals:
            animal.move(self.screen_width, self.screen_height - self.ui_height)
        self.animals = [animal for animal in self.animals if not animal.is_caught]

#--------------------------------------------------------------------------------------------------------------------------
# Draw all animals on the screen, animals are drawn on the screen, and their images are updated

    def draw(self, screen):
        for animal in self.animals:
            animal.draw(screen)

#--------------------------------------------------------------------------------------------------------------------------
# Check for collisions with the player, if an animal collides with the player, it is marked as caught and points are awarded

    def check_collisions(self, player_rect):
        total_points = 0
        for animal in self.animals:
            points = animal.check_collision(player_rect)
            total_points += points
        return total_points 