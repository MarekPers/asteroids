import sys
import pygame
from constants import *

def exit_screen(screen, score_value):
    # Przyciemnienie ekranu
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)  # Ustawienie przezroczystości

    # Wyświetlenie punktacji końcowej
    font = pygame.font.Font(None, 80)
    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    score_text = font.render(f"Final Score: {score_value}", True, (255, 255, 255))

    # Opcje
    options_font = pygame.font.Font(None, 50)
    options_text = options_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

    # Rysowanie
    screen.blit(overlay, (0, 0))
    screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
    screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    screen.blit(options_text, options_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

    pygame.display.flip()

    # Oczekiwanie na akcję gracza
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Wyjście z gry
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:  # Restart gry
                    return
