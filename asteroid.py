'''
asteroid.py

Moduł odpowiedzialny za definicję klasy Asteroid,
która dziedziczy po klasie CircleShape i reprezentuje
pojedynczą asteroidę poruszającą się po ekranie.
Zawiera logikę inicjalizacji grafiki, poruszania się,
dzielenia na mniejsze fragmenty oraz naliczania punktów.
'''

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
from utils import CircleShape
from constants import *
import random


class Asteroid(CircleShape):
    # Klasa Asteroid odpowiada za tworzenie, rysowanie i
    # zarządzanie zachowaniem pojedynczej asteroidy.

    LARGE_ASTEROIDS = ["assets/asteroid/large_asteroid_1.png", "assets/asteroid/large_asteroid_2.png", "assets/asteroid/large_asteroid_3.png"]
    MEDIUM_ASTEROIDS = ["assets/asteroid/medium_asteroid_1.png", "assets/asteroid/medium_asteroid_2.png", "assets/asteroid/medium_asteroid_3.png"]
    SMALL_ASTEROIDS = ["assets/asteroid/small_asteroid_1.png", "assets/asteroid/small_asteroid_2.png", "assets/asteroid/small_asteroid_3.png"]

    def __init__(self, x, y, radius):
        # Konstruktor przyjmuje początkową pozycję i promień,
        # ustala odpowiedni obrazek oraz kierunek ruchu.
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
        # Rysuje asteroidę na przekazanym ekranie w jej aktualnej pozycji.
        screen.blit(self.image, self.rect.topleft)

    def update(self, dt):
        # Aktualizuje pozycję asteroidy i stosuje efekt zawijania ekranu.
        self.position += self.velocity * dt
        # Screen wrapping
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        self.rect.center = self.position

    def split(self):
        # Jeśli asteroida jest wystarczająco duża, rozdziela ją na dwie mniejsze,
        # tworząc nowe obiekty z mniejszym promieniem i odchylonym wektorem prędkości.
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        asteroid_1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        asteroid_2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        asteroid_spread = random.uniform(20, 50)
        asteroid_1.velocity = self.velocity.rotate(asteroid_spread) * 1.2
        asteroid_2.velocity = self.velocity.rotate(-asteroid_spread) * 1.2

    def get_points(self):
        # Zwraca liczbę punktów przyznawanych graczowi za zniszczenie asteroidy
        # w zależności od jej aktualnego rozmiaru.
        if self.radius > ASTEROID_MIN_RADIUS * 2:
            return 25
        elif self.radius > ASTEROID_MIN_RADIUS:
            return 50
        else:
            return 100