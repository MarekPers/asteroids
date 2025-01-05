import pygame
from circleshape import CircleShape
from constants import *
import random


class Asteroid(CircleShape):
    LARGE_ASTEROIDS = ["assets/large_asteroid_1.png", "assets/large_asteroid_2.png"]
    MEDIUM_ASTEROIDS = ["assets/medium_asteroid_1.png", "assets/medium_asteroid_2.png"]
    SMALL_ASTEROIDS = ["assets/small_asteroid_1.png", "assets/small_asteroid_2.png"]

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
        if self.radius > ASTEROID_MIN_RADIUS * 2:
            image_path = random.choice(self.LARGE_ASTEROIDS)
        elif self.radius > ASTEROID_MIN_RADIUS:
            image_path = random.choice(self.MEDIUM_ASTEROIDS)
        else:
            image_path = random.choice(self.SMALL_ASTEROIDS)

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        asteroid_1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        asteroid_2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        asteroid_spread = random.uniform(20, 50)
        asteroid_1.velocity = self.velocity.rotate(asteroid_spread) * 1.2
        asteroid_2.velocity = self.velocity.rotate(-asteroid_spread) * 1.2

    def get_points(self):
        if self.radius > ASTEROID_MIN_RADIUS * 2:
            return 25
        elif self.radius > ASTEROID_MIN_RADIUS:
            return 50
        else:
            return 100