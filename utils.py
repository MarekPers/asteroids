import pygame
import audio
import random

# ------------------------------------------------------------
#  Klasa bazowa dla sprite'ów o kolistym kształcie
#  (proste sprawdzanie kolizji na podstawie sumy promieni).
# ------------------------------------------------------------
class CircleShape(pygame.sprite.Sprite):
    """
    Sprite reprezentujący okrągły obiekt w przestrzeni 2D.
    Dostarcza wspólną obsługę pozycji, prędkości, promienia i kolizji
    dla asteroid, pocisków, statku gracza czy UFO.
    """
    def __init__(self, x, y, radius):
        # ten atrybut pozwala klasom potomnym wskazać grupy sprite'ów
        # (poprzez zmienną klasową `containers`), do których obiekt ma
        # zostać automatycznie dodany podczas inicjalizacji.
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def collides_with(self, obj2):
        distance = self.position.distance_to(obj2.position)
        return distance <= (self.radius + obj2.radius)
        # zwraca True lub False

    def draw(self, screen):
        # metoda powinna zostać nadpisana w klasie dziedziczącej
        pass

    def update(self, dt):
        # metoda powinna zostać nadpisana w klasie dziedziczącej
        pass


class Explosion(pygame.sprite.Sprite):
    """
    Animowany sprite wybuchu, który po odtworzeniu wszystkich klatek
    usuwa się automatycznie z grup sprite'ów i odtwarza efekt dźwiękowy.
    """
    def __init__(self, position):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/explosion_sprite_sheet_fixed.png").convert_alpha()
        self.frames = []
        frame_width, frame_height = 128, 128
        for i in range(6):  # 6 klatek animacji
            frame = self.spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

        self.current_frame = 0
        self.position = position
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)
        self.animation_speed = 0.1  # odstęp czasu między klatkami (sekundy)
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                audio.play_sfx("explosion")
                self.kill()  # Usunięcie obiektu po zakończeniu animacji
            else:
                self.image = self.frames[self.current_frame]

    
def random_velocity(min_speed: float, max_speed: float) -> pygame.Vector2:
    """ Zwraca wektor `pygame.Vector2` o losowym kierunku i prędkości z podanego zakresu. """
    angle  = random.uniform(0, 360)
    speed  = random.uniform(min_speed, max_speed)
    return pygame.Vector2(speed, 0).rotate(angle)


def random_outside_position(margin: int = 50) -> pygame.Vector2:
    """
    Losuje punkt znajdujący się poza granicami ekranu o podanym marginesie.

    margin : int, opcjonalny
        Liczba pikseli określająca odległość od krawędzi (domyślnie 50).
    """
    screen = pygame.display.get_surface().get_rect()
    side   = random.choice(("top", "bottom", "left", "right"))

    if side == "top":
        x, y = random.uniform(0, screen.width), -margin
    elif side == "bottom":
        x, y = random.uniform(0, screen.width), screen.height + margin
    elif side == "left":
        x, y = -margin, random.uniform(0, screen.height)
    else:  # right
        x, y = screen.width + margin, random.uniform(0, screen.height)

    return pygame.Vector2(x, y)