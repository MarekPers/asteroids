# score.py - zarządzanie wynikiem gracza
import pygame

class Score:
    def __init__(self, font_size=30, color=(255, 255, 255)):
        # Inicjalizacja fontu i ustawienie początkowego wyniku
        self.points = 0
        self.font = pygame.font.Font(None, font_size)
        self.color = color

    def add_points(self, amount):
        self.points += amount

    def reset(self):
        self.points = 0

    # Renderuje tekst z wynikiem i rysuje go w lewym górnym rogu ekranu
    def draw(self, screen, position=(10, 10)):
        score_surface = self.font.render(f"Score: {self.points}", True, self.color)
        screen.blit(score_surface, position)

    def get_score(self):
        return self.points
        