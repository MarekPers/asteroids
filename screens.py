"""
screens.py

Moduł odpowiedzialny za **ekrany interfejsu** gry:

• `start_screen`      - ekran tytułowy, wyświetlany przed rozpoczęciem rozgrywki;  
  zatrzymuje się, dopóki gracz nie naciśnie **SPACE** lub **ENTER**.  
• `pause_screen`      - pół-transparentna plansza pauzy; wraca do gry po **ESC**, 
• `game_over_screen`  - podsumowanie wyniku i opcja restartu (**R**) lub wyjścia (**Q**).

Każda funkcja jest *blokująca* - zatrzymuje główną pętlę gry,
dopóki użytkownik nie wybierze jednej z dozwolonych akcji.
"""

import sys
import pygame
from constants import *
import audio


def _blit_center(screen, surf, y):
    # Pomocnicze wyrównanie poziome
    rect = surf.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(surf, rect)


def start_screen(screen):
    """Ekran tytułowy - czeka na SPACE / ENTER."""
    # Przygotowanie zasobów
    clock = pygame.time.Clock()
    background = pygame.image.load("assets/background.png").convert()
    title_f  = pygame.font.Font(None, 120)  # duży, nagłówkowy font
    info_f   = pygame.font.Font(None, 50)   # mniejszy font dla podpowiedzi

    # Główna pętla ekranu tytułowego
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:       # zamknięcie okna
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_RETURN):
                audio.theme()   # zatrzyma intro i puści theme.mp3 w pętli
                return          # ← start gry

        # Rysowanie tła i tekstów
        screen.blit(background, (0, 0))
        _blit_center(screen, title_f.render("ASTEROIDS", True, (255, 255, 255)),
                     SCREEN_HEIGHT // 2 - 80)
        _blit_center(screen, info_f.render("Press SPACE / ENTER to play", True, (255, 255, 255)),
                     SCREEN_HEIGHT // 2 + 20)
        pygame.display.flip()
        clock.tick(60)


def pause_screen(screen):
    """Przyciemnia ekran i czeka na ESC, by wrócić do gry."""
    clock = pygame.time.Clock()
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0)); overlay.set_alpha(150)     # delikatne ściemnienie

    pause_f = pygame.font.Font(None, 100)
    info_f  = pygame.font.Font(None, 50)


    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:       # wyjście z gry
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return          # ← kontynuacja gry

        screen.blit(overlay, (0, 0))
        _blit_center(screen, pause_f.render("PAUSED", True, (255, 255, 255)),
                     SCREEN_HEIGHT // 2 - 40)
        _blit_center(screen, info_f.render("Press ESC to resume", True, (255, 255, 255)),
                     SCREEN_HEIGHT // 2 + 60)
        pygame.display.flip()
        clock.tick(60)


def exit_screen(screen, score_value):
    audio.stop_music()        # zatrzymaj theme
    audio.play_sfx("game_over")
    """GAME OVER - R restart, Q quit."""
    clock = pygame.time.Clock()
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0)); overlay.set_alpha(150)

    big_f  = pygame.font.Font(None, 80)
    small_f = pygame.font.Font(None, 50)

    game_over = big_f.render("GAME OVER", True, (255, 255, 255))
    score_txt = big_f.render(f"Final Score: {score_value}", True, (255, 255, 255))
    opts      = small_f.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    audio.stop_music()
                    pygame.mixer.quit()
                    pygame.quit(); sys.exit()
                if e.key == pygame.K_r:
                    return      # ← restart

        screen.blit(overlay, (0, 0))
        _blit_center(screen, game_over, SCREEN_HEIGHT // 2 - 100)
        _blit_center(screen, score_txt, SCREEN_HEIGHT // 2)
        _blit_center(screen, opts,      SCREEN_HEIGHT // 2 + 100)
        pygame.display.flip()
        clock.tick(60)
