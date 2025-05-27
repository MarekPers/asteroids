"""
powerups.py
===========
Moduł odpowiedzialny za **bonusy (power-upy)** pojawiające się na planszy.
Każdy power-up jest niewielkim obiektem, który przelatuje przez ekran w
linii prostej (z wrap-aroundem, identycznie jak asteroidy) i po
zderzeniu ze statkiem gracza nadaje mu tymczasową zdolność:

• `PU_SHIELD`   - tarcza pozwalająca przetrwać kolizję,
• `PU_FAST_FIRE`- zwiększa szybkostrzelność lasera,
• `PU_SPREAD`   - strzał wachlarzowy (3 pociski naraz),
• `PU_NOVA`     - wysyła falę uderzeniową niszczącą pobliskie obiekty,
• `PU_THREAT`   - negatywny bonus - chwilowy lawinowy atak asteroid.

Klasa `PowerUp` dziedziczy po uproszczonym okrągłym colliderze
`CircleShape`, dzięki czemu do wykrywania kolizji wystarczy porównanie
odległości środków dwóch okręgów (szybkie i wystarczająco dokładne dla
małych sprite'ów).

Kod modułu jest celowo maksymalnie lekki: żadnego zarządzania grupami,
animacji czy dźwięków - cały „żywy” aspekt bonusów (respawn, żywotność,
efekt po zebraniu) obsługują zewnętrzne systemy (`AsteroidField`,
`Player`).
"""

import random, math, pygame
from constants import *
from utils import CircleShape

class PowerUp(CircleShape):
    # Ścieżka do pliku graficznego
    SPRITES = {
        PU_SHIELD:   "assets/powerup/pu_shield.png",
        PU_FAST_FIRE:"assets/powerup/pu_fast_fire.png",
        PU_SPREAD:   "assets/powerup/pu_spread.png",
        PU_NOVA:     "assets/powerup/pu_nova.png",
        PU_THREAT:   "assets/powerup/pu_threat.png",
    }

    # Obiekt przyjmuje:
    # • `pos`      – pozycję startową,
    # • `velocity` – prędkość (kierunek i wartość),
    # • `kind`     – typ bonusu, aby ustalić sprite i działanie.
    def __init__(self, pos: pygame.Vector2, velocity: pygame.Vector2, kind: str):
        # Wywołujemy konstruktor bazowy, aby utworzyć okrągły collider
        super().__init__(pos.x, pos.y, 20)      # <-- poprawne x, y
        # Zachowaj wektor prędkości do przyszłych obliczeń ruchu
        self.velocity = velocity
        self.kind  = kind
        # Ładowanie odpowiedniej grafiki; metoda `convert_alpha()`
        # przyspiesza późniejsze blit‑owanie
        self.image = pygame.image.load(self.SPRITES[kind]).convert_alpha()
        # Obliczamy prostokąt kolizyjny/graficzny z pozycją w środku
        self.rect  = self.image.get_rect(center = self.position)

    # Metoda wywoływana co klatkę z delta‑time (sekundy).
    # Realizuje prosty ruch liniowy i "wrap‑around" – jeśli obiekt
    # wyleci za jedną krawędź ekranu, pojawia się po przeciwnej.
    def update(self, dt: float):
        # Równanie ruchu: p = p0 + v * dt
        self.position += self.velocity * dt
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        # Uaktualniamy środek prostokąta, aby blit był w dobrym miejscu
        self.rect.center = self.position

    # Proste rysowanie – 'blit' spriteʼa w miejscu wyznaczonym przez
    # środek kolidera. Dzięki temu w jednym miejscu ustalamy zarówno
    # fizykę, jak i grafikę obiektu.
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect.topleft)