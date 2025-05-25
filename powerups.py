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

    def __init__(self, pos, velocity, kind):
        super().__init__(pos, velocity, radius=20)
        self.kind = kind
        self.image = pygame.image.load(self.SPRITES[kind]).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        super().update(dt)
        # delikatne podkręcanie wizualne
        self.rotate(60 * dt)
