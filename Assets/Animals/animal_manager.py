import pygame
import random
from .bird import Bird
from .mouse import Mouse

class AnimalManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.animals = []
        self.spawn_timer = 0
        self.spawn_delay = 2000  # Spawn new animal every 2 seconds
        self.last_spawn_time = pygame.time.get_ticks()

    def spawn_animal(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.last_spawn_time = current_time
            if random.random() < 0.3:                               # 30% chance for bird
                y = random.randint(100, self.screen_height - 200)  # Random height for birds
                self.animals.append(Bird(0, y))
            else:                                                  # 70% chance for mouse
                y = self.screen_height - 100                       # Ground level for mice
                self.animals.append(Mouse(0, y))

    def update(self):
        self.spawn_animal()
        for animal in self.animals:
            animal.move(self.screen_width)                         # Remove caught animals
        self.animals = [animal for animal in self.animals if not animal.is_caught]

    def draw(self, screen):
        for animal in self.animals:
            animal.draw(screen)

    def check_collisions(self, player_rect):
        total_points = 0
        for animal in self.animals:
            points = animal.check_collision(player_rect)
            total_points += points
        return total_points 