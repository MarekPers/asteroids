# powerups.py
import random, math, pygame
from constants import *
from utils import CircleShape

class PowerUp(CircleShape):
    """Latający obiekt do zebrania."""

    SPRITES = {
        PU_SHIELD:   "assets/powerup/pu_shield.png",
        PU_FAST_FIRE:"assets/powerup/pu_fast_fire.png",
        PU_SPREAD:   "assets/powerup/pu_spread.png",
        PU_NOVA:     "assets/powerup/pu_nova.png",
        PU_THREAT:   "assets/powerup/pu_threat.png",
    }

    def __init__(self, pos: pygame.Vector2, velocity: pygame.Vector2, kind: str):
        super().__init__(pos.x, pos.y, 20)      # <-- poprawne x, y
        self.velocity = velocity                # <-- zapisz prędkość!
        self.kind  = kind
        self.image = pygame.image.load(self.SPRITES[kind]).convert_alpha()
        self.rect  = self.image.get_rect(center = self.position)

    def update(self, dt: float):
        # proste przemieszczenie + wrap-around (jak w asteroidach)
        self.position += self.velocity * dt
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        self.rect.center = self.position

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect.topleft)