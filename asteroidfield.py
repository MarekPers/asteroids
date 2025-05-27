"""
asteroidfield.py

Zarządza "ruchem ulicznym" asteroid pojawiających się na planszy.
Klasa `AsteroidField` pełni rolę prostego _factory_ - w określonych
odstępach czasu tworzy i umieszcza w grze obiekty klasy `Asteroid`.

Główne zadania modułu:
- wyznaczanie pozycji i kierunku startowego dla każdej nowej asteroidy,
- regulowanie częstotliwości pojawiania się (z uwzględnieniem power-upów),
- obsługa efektu **Threat** (tymczasowe zwiększenie natężenia spawnu).
"""

import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    """
    Kontener sprite'ów Pygame odpowiedzialny za generowanie kolejnych asteroid.
    
    Parametry składowe:
    --------------------
    spawn_timer : float
        Licznik odmierzający czas do kolejnego spawnu.
    spawn_mult : float
        Mnożnik przyspieszający lub spowalniający generowanie (np. po aktywacji power-upa).
    _threat_timer : float
        Pozostały czas działania efektu Threat.
    """
    edges = [
        # Każdy wpis opisuje jedną krawędź ekranu:
        # [
        #   <wektor kierunku lotu pierwotnego>,
        #   <funkcja generująca losową pozycję startową na danej krawędzi>
        # ]
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        # Inicjalizacja pól wewnętrznych
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer   = 0.0
        self.spawn_mult    = 1.0      # 1 → normalnie
        self._threat_timer = 0.0

    def trigger_threat(self, duration: float = PU_DURATION[PU_THREAT]) -> None:
        # Aktywuje lub przedłuża działanie power‑up'a Threat zwiększającego liczbę asteroid.
        self.spawn_mult   = ASTEROID_SPAWN_BOOST
        self._threat_timer += duration

    def spawn(self, radius, position, velocity):
        # Pomocnicza metoda tworząca nową asteroidę i ustawiająca jej prędkość.
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        """
        Wywoływana co klatkę - zlicza upływ czasu,
        a gdy zajdzie potrzeba generuje kolejną asteroidę.

        Parametr
        --------
        dt (delta time) : float
            Czas (w sekundach) jaki minął od ostatniego wywołania.
        """
        self.spawn_timer += dt * self.spawn_mult
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
        if self._threat_timer > 0:
            self._threat_timer -= dt
            if self._threat_timer <= 0:
                self.spawn_mult = 1.0