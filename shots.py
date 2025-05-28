import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SHOT_RADIUS, PLAYER_SHOOT_SPEED
from utils import CircleShape


class Shot(CircleShape):
    SPRITE_PATH = "assets/laser.png"

    # wczytujemy i buforujemy surową grafikę tylko raz
    _base_image: pygame.Surface | None = None

    def __init__(self, x: float, y: float, rotation: float):
        super().__init__(x, y, SHOT_RADIUS)
        self.rotation = rotation  # zachowujemy, by nie trzeba było liczyć kąta przy rysowaniu

        # base image lazy‑load
        if Shot._base_image is None:
            Shot._base_image = pygame.image.load(self.SPRITE_PATH).convert_alpha()

        # dopasuj wielkość pocisku do promienia
        w = int(self.radius * 4)
        h = int(self.radius * 1.4)
        self.image_original = pygame.transform.smoothscale(Shot._base_image, (w, h))
        # obracamy do kierunku lotu
        self.image = pygame.transform.rotate(self.image_original, -self.rotation)
        self.rect = self.image.get_rect(center=self.position)

    # ------------------------------------------------------------
    def update(self, dt: float):
        self.position += self.velocity * dt
        self.rect.center = self.position
        # usuń pocisk, jeśli opuści ekran (brak wrap‑around)
        if (
            self.position.x < -self.radius
            or self.position.x > SCREEN_WIDTH + self.radius
            or self.position.y < -self.radius
            or self.position.y > SCREEN_HEIGHT + self.radius
        ):
            self.kill()

    # ------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect.topleft)
