import pygame

class Score:
    def __init__(self, font_size=30, color=(255, 255, 255)):
        self.points = 0
        self.font = pygame.font.Font(None, font_size)
        self.color = color

    def add_points(self, amount):
        self.points += amount

    def reset(self):
        self.points = 0

    def draw(self, screen, position=(10, 10)):
        score_surface = self.font.render(f"Score: {self.points}", True, self.color)
        screen.blit(score_surface, position)
