import pygame
import math
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, UFO_RADIUS
from utils import CircleShape

class UFO(CircleShape):
    """Rzadko pojawiający się statek, który przelatuje w poprzek ekranu.
    Można go zestrzelić dla dodatkowych punktów.
    """
    def __init__(self, x, y, radius=UFO_RADIUS):
        super().__init__(x, y, radius)

        self.image = pygame.image.load("assets/ufo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 1.3))

        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        # Ruch w poziomie
        self.position += self.velocity * dt

        # Prosty sinusoidalny dryf w pionie
        self.position.y += math.sin(pygame.time.get_ticks() * 0.002) * 0.3

        # Po opuszczeniu ekranu – usuń obiekt
        if self.position.x < -self.radius or self.position.x > SCREEN_WIDTH + self.radius:
            self.kill()

        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def get_points(self):
        return 200
