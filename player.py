"""
player.py

Moduł obsługujący statek gracza - klasę `Player`.

Zawiera logikę:
- sterowania (rotacja, przyspieszanie, hamowanie) z płynną fizyką,
- animacji płomieni silnika zależnej od prędkości (5 dyskretnych rozmiarów),
- zarządzania życiem, tarczą niewrażliwości oraz kolizjami,
- strzelania pociskami, w tym buff "szybkostrzelność" i "spread shot",
- obsługi różnorodnych power-upów oraz komunikacji z "AsteroidField".
"""

import pygame
import audio
from typing import List
from constants import *
from utils import CircleShape, Explosion
from shots import Shot
from asteroidfield import AsteroidField


class Player(CircleShape):
    """Klasa reprezentująca statek gracza.

    Dziedziczy po `CircleShape`, aby korzystać ze wspólnej kolizyjnej
    geometrii (promień, pozycja jako `Vector2`).  Oprócz cech bazowych
    przechowuje również indywidualne parametry ruchu, animację płomienia
    oraz buffy wzmacniające.
    """

    # -------- wstępnie zdefiniowane skale dla płomienia --------
    _FLAME_SCALES = (0.8, 1.0, 1.2, 1.4, 1.6)

    def __init__(self, x: float, y: float, asteroid_field: AsteroidField, lives: int = 3):
        """Inicjalizacja statku.

        Parametry
        ---------
        x, y : float
            Współrzędne startowe.
        asteroid_field : AsteroidField
            Referencja do pola asteroid, aby móc generować wybuchy i buffy.
        lives : int, default 3
            Liczba żyć na start.
        """
        super().__init__(x, y, PLAYER_RADIUS)
        self.asteroid_field = asteroid_field

        # --- zmienne szybkostrzelności -------------
        self.fast_fire_level = 0        # ile stacków
        self.fast_fire_until = 0.0      # wspólny timer

        # ---------------- parametry ruchu ----------------
        self.rotation: float = 0.0      # w stopniach, 0 znaczy „w górę”
        self.speed: float = 0.0         # obecna prędkość (px/s)
        self._ACCEL: float = PLAYER_SPEED * 2  # przyspieszenie (0‑>Vmax w ~0,5 s)

        # --------------- timery gry ----------------
        self.shoot_timer: float = 0.0
        self.invulnerability_timer: float = 0.0
        self.lives: int = lives

        # ---------------- grafika statku ----------------
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect(center=(x, y))

        # ---------------- płomienie ----------------
        sheet = pygame.image.load("assets/thruster_flame_sheet.png").convert_alpha()
        fw, fh = sheet.get_width() // 4, sheet.get_height()

        # --- buffy ---
        self.buff_until: dict[str, float] = {}
        self.spread_level = 0   # ile dodat. par pocisków

    # =============================================================
    # Naprawa artefaktów płomieni (usunięcie białych boxów animacji)                            
    # =============================================================

        # 1) wycinamy bounding‑box dla każdej klatki (usuwa pustą ramkę)
        trimmed_frames: List[pygame.Surface] = []
        for i in range(4):
            raw = sheet.subsurface(pygame.Rect(i * fw, 0, fw, fh))
            bbox = raw.get_bounding_rect(min_alpha=50)
            trimmed = raw.subsurface(bbox).copy()
            trimmed_frames.append(trimmed.convert_alpha())

        # 2) przygotowujemy 5 zestawów rozmiarów – bez skalowania w runtime
        self.flame_frames_by_scale: List[List[pygame.Surface]] = []  # 5 poziomów × 4 klatki
        for s in self._FLAME_SCALES:
            scaled_frames = [
                pygame.transform.scale(f, (int(f.get_width() * s), int(f.get_height() * s))).convert_alpha()
                for f in trimmed_frames
            ]
            self.flame_frames_by_scale.append(scaled_frames)

        # animacyjny stan wewnętrzny płomienia
        self._flame_i = 0
        self._flame_timer = 0.0

    # =============================================================
    #                            UPDATE                            
    # =============================================================
    def update(self, dt: float):
        """Aktualizuj logikę statku.
        Wywoływana co klatkę przez pętlę główną - `dt` (delta time) to odstęp czasu w sekundach.
        """
        if self.spread_level and not self.buff_active(PU_SPREAD):
            self.spread_level = 0
        
        # ---------- strzelanie ----------
        self.shoot_timer -= dt
        if keys[pygame.K_SPACE]:
            self.shoot()

        # ---------- tarcza ----------
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= dt

        keys = pygame.key.get_pressed()

        # ---------- obrót ----------
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        # ---------- akceleracja ----------
        thrust_forward, thrust_back = keys[pygame.K_w], keys[pygame.K_s]
        if thrust_forward:
            self.speed = min(self.speed + self._ACCEL * dt, PLAYER_SPEED)
        elif thrust_back:
            self.speed = max(self.speed - self._ACCEL * dt, -PLAYER_SPEED * 0.5)
        else:
            # pasywne wytracanie prędkości (proporcjonalne)
            decel = self._ACCEL * 1.5 * dt
            if self.speed > 0:
                self.speed = max(0, self.speed - decel)
            elif self.speed < 0:
                self.speed = min(0, self.speed + decel)

        # ---------- ruch & screen‑wrap ----------
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * self.speed * dt
        # wyjście poza ekran po jednej stronie – pojawienie się po przeciwnej
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        self.rect.center = self.position

        # ---------- animacja płomienia ----------
        speed_ratio = abs(self.speed) / PLAYER_SPEED  # 0‑1
        if speed_ratio > 0.05:  # mały próg, by wyłączyć płomień przy znikomej prędkości
            self._flame_timer += dt * (8 + 12 * speed_ratio)
            if self._flame_timer >= 1:
                self._flame_timer, self._flame_i = 0, (self._flame_i + 1) % 4
        else:
            self._flame_timer, self._flame_i = 0, 0


    # =============================================================
    #                             DRAW                            
    # =============================================================
    def draw(self, screen: pygame.Surface):
        """Renderuj statek i płomienie na podanym ekranie Pygame."""
        rotated_ship = pygame.transform.rotate(self.image, -self.rotation)
        ship_rect = rotated_ship.get_rect(center=self.position)

        # --------- płomień ---------
        if abs(self.speed) > 1:     # wyświetlaj tylko przy sensownej prędkości
            speed_ratio = abs(self.speed) / PLAYER_SPEED
            # wybór poziomu skalowania (0‑4)
            scale_idx = min(4, int(speed_ratio * (len(self._FLAME_SCALES) - 1) + 0.5))
            flame_surf = self.flame_frames_by_scale[scale_idx][self._flame_i]
            back_vec = pygame.Vector2(0, 1).rotate(self.rotation)
            # dopasuj pozycję tak, by płomień „wyrastał” zza dyszy
            offset = back_vec * self.radius * 0.9 * self._FLAME_SCALES[scale_idx]
            flame_pos = self.position + offset
            flame_rotated = pygame.transform.rotate(flame_surf, -self.rotation)
            screen.blit(flame_rotated, flame_rotated.get_rect(center=flame_pos))

        # --------- tarcza niewrażliwości ---------
        if self.invulnerability_timer > 0 and int(self.invulnerability_timer * 8) % 2 == 0:
            r = int(self.radius * 1.2)
            shield = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield, (0, 255, 255, 140), (r, r), r, 3)
            screen.blit(shield, shield.get_rect(center=self.position))

        # --------- statek ---------
        screen.blit(rotated_ship, ship_rect.topleft)

    def rotate(self, dt: float):
        self.rotation += PLAYER_TURN_SPEED * dt

    # =============================================================
    #                        GAMEPLAY ACTIONS                      
    # =============================================================
    def shoot(self):
        """Stwórz pociski w aktualnym kierunku - uwzględnia buffy."""
        if self.shoot_timer > 0:
            return
        level = self.buff_active(PU_FAST_FIRE, level=True)
        mult  = FAST_FIRE_MULT ** level if level else 1
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN / mult

        # główny pocisk
        direction = pygame.Vector2(0, -1).rotate(self.rotation)     # ← DODAJ
        shot = Shot(self.position.x, self.position.y, self.rotation)
        shot.velocity = direction * PLAYER_SHOOT_SPEED

        # dodatkowe pociski dla power-upa Spread
        for i in range(self.spread_level):
            angle_offset = SPREAD_ANGLE * (i + 1)
            for sign in (-1, 1):
                dir2 = direction.rotate(sign * angle_offset)
                extra = Shot(self.position.x, self.position.y, self.rotation + sign * angle_offset)
                extra.velocity = dir2 * PLAYER_SHOOT_SPEED

        audio.play_sfx("laser")

    def fire_nova(self):
        for angle in range(0, 360, 360 // 100):
            dir_vec = pygame.Vector2(1, 0).rotate(angle)
            nova_shot = Shot(self.position.x, self.position.y, angle)
            nova_shot.velocity = dir_vec * PLAYER_SHOOT_SPEED
        audio.play_sfx("laser")

    def handle_collision(self, screen, score, exit_screen, restart_game, asteroids, explosions):
        # Obsługa kolizji
        if self.invulnerability_timer > 0:
            return
        self.lives -= 1
        self.invulnerability_timer = 2
        for asteroid in asteroids:
            if self.position.distance_to(asteroid.position) <= 3 * self.radius:
                explosions.add(Explosion(asteroid.position))
                asteroid.kill()
                score.add_points(asteroid.get_points())
        if self.lives <= 0:
            # Jeśli gracz osiągnie 0 żyć - ginie i pojawia się ekran końcowy
            exit_screen(screen, score.get_score())
            restart_game()

    def draw_lives(self, screen: pygame.Surface, fps: float):
        """Rysuje FPS oraz liczbę żyć w prawym górnym rogu, zawsze mieszcząc się w ekranie."""
        text = f"FPS: {int(fps):>3} | LIVES: {self.lives}"
        surf = pygame.font.Font(None, 36).render(text, True, (255, 255, 255))
        # odsuwamy 10 px od prawej krawędzi niezależnie od szerokości napisu
        screen.blit(surf, (SCREEN_WIDTH - surf.get_width() - 10, 10))

    # POWER-UP: Tarcza
    def add_shield(self, extra: float = PU_DURATION[PU_SHIELD]) -> None:
        self.invulnerability_timer += extra

    # ---------------- Power-up API ---------------- #
    def apply_powerup(self, kind: str):
        now = pygame.time.get_ticks() / 1000
        dur = PU_DURATION[kind]

        if kind == PU_FAST_FIRE:
            self.fast_fire_level += 1
            # przedłuż tyle, by KAŻDY stack dotrwał pełen czas
            self.fast_fire_until = max(self.fast_fire_until, now) + dur
            return

        # power-up natychmiastowy
        if kind == PU_NOVA:
            self.fire_nova()
            return
        
        # zapis/odświeżenie timera buffa
        dur = PU_DURATION[kind]
        self.buff_until[kind] = self.buff_until.get(kind, now) + dur

        if kind == PU_SPREAD:
            self.spread_level += 1

        elif kind == PU_SHIELD:
            self.add_shield()

        elif kind == PU_THREAT:
            self.asteroid_field.trigger_threat()

    def buff_active(self, kind: str, *, level: bool=False):
        now = pygame.time.get_ticks() / 1000
        if kind == PU_FAST_FIRE and level:
            return self.fast_fire_level if now < self.fast_fire_until else 0
        return now < self.buff_until.get(kind, 0)
