"""
score.py

Moduł odpowiedzialny za obsługę **punktacji** i prezentację wyniku
na ekranie.  Klasa `Score` gromadzi zdobyte punkty, udostępnia
metody ich modyfikacji oraz funkcję `draw`, która renderuje bieżący
rezultat w lewym górnym rogu okna gry.

Zakres odpowiedzialności
---------------------------
* zliczanie punktów zdobytych w czasie jednej sesji,
* zerowanie wyniku przy starcie nowej gry (`reset()`),
* graficzne wyświetlanie liczby punktów (`draw()`).
"""

import pygame

class Score:
    def __init__(self, font_size=30, color=(255, 255, 255)):
        # Inicjalizacja fontu i ustawienie początkowego wyniku
        self.points = 0
        # `None` → wbudowany font Pygame; brak zależności od plików .ttf
        self.font = pygame.font.Font(None, font_size)
        self.color = color

    # Dodawanie punktów
    def add_points(self, amount):
        self.points += amount

    # Zerowanie wyniku
    def reset(self):
        self.points = 0

    # Renderuje tekst z wynikiem i rysuje go w lewym górnym rogu ekranu
    def draw(self, screen, position=(10, 10)):
        score_surface = self.font.render(f"Score: {self.points}", True, self.color)
        screen.blit(score_surface, position)

    # Udostępnienie aktualnego wyniku
    def get_score(self):
        return self.points
        