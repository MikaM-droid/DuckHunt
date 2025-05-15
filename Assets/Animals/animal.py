import pygame
import random

class Animal:
    def __init__(self, x, y, speed, points):
        self.x = x
        self.y = y
        self.speed = speed
        self.points = points
        self.rect = None
        self.direction = 1  # 1 for right, -1 for left
        self.is_caught = False

    def move(self, screen_width):
        if not self.is_caught:
            self.x += self.speed * self.direction
            # Reverse direction if hitting screen edges
            if self.x <= 0 or self.x + self.rect.width >= screen_width:
                self.direction *= -1
                self.x = max(0, min(self.x, screen_width - self.rect.width))

    def draw(self, screen):
        if not self.is_caught:
            screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        if not self.is_caught and self.rect.colliderect(player_rect):
            self.is_caught = True
            return self.points
        return 0
