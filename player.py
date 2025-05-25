import pygame
from typing import List
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
)
from utils import CircleShape, Explosion
from shots import Shot


class Player(CircleShape):
    """Sterowanie statkiem z płynną akceleracją
    i płomieniem silnika o **dyskretnych poziomach wielkości** (bez skalowania w locie),
    co eliminuje artefakt prostokątnej ramki przy przezroczystym tle.

    Redukcja artefaktów płomieni napisana z użyciem GPT o3 od OpenAI.

    Dodatkowo: migająca tarcza niewrażliwości."""

    # -------- wstępnie zdefiniowane skale dla płomienia --------
    _FLAME_SCALES = (0.8, 1.0, 1.2, 1.4, 1.6)

    def __init__(self, x: float, y: float, lives: int = 3):
        super().__init__(x, y, PLAYER_RADIUS)

        # ---------------- parametry ruchu ----------------
        self.rotation: float = 0.0
        self.speed: float = 0.0  # px/s
        self._ACCEL: float = PLAYER_SPEED * 2  # przyspieszenie (0‑>Vmax w ~0,5 s)

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

        # ---------------- GPT o3 START ----------------
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

        self._flame_i = 0
        self._flame_timer = 0.0

        # ---------------- GPT o3 END ----------------

    # =============================================================
    #                            UPDATE                            
    # =============================================================
    def update(self, dt: float):
        self.shoot_timer -= dt
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
            decel = self._ACCEL * 1.5 * dt
            if self.speed > 0:
                self.speed = max(0, self.speed - decel)
            elif self.speed < 0:
                self.speed = min(0, self.speed + decel)

        # ---------- ruch & screen‑wrap ----------
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * self.speed * dt
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

        # ---------- strzelanie ----------
        if keys[pygame.K_SPACE]:
            self.shoot()

    # =============================================================
    #                             DRAW                            
    # =============================================================
    def draw(self, screen: pygame.Surface):
        rotated_ship = pygame.transform.rotate(self.image, -self.rotation)
        ship_rect = rotated_ship.get_rect(center=self.position)

        # --------- płomień - GPT o3 ---------
        if abs(self.speed) > 1:
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

    # =============================================================
    #                           HELPERS                           
    # =============================================================
    def rotate(self, dt: float):
        self.rotation += PLAYER_TURN_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y, self.rotation)
        shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def handle_collision(self, screen, score, exit_screen, restart_game, asteroids, explosions):
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
            exit_screen(screen, score.get_score())
            restart_game()

    def draw_lives(self, screen: pygame.Surface, fps: float):
        """Rysuje FPS oraz liczbę żyć w prawym górnym rogu, zawsze mieszcząc się w ekranie."""
        text = f"FPS: {int(fps):>3} | LIVES: {self.lives}"
        surf = pygame.font.Font(None, 36).render(text, True, (255, 255, 255))
        # odsuwamy 10 px od prawej krawędzi niezależnie od szerokości napisu
        screen.blit(surf, (SCREEN_WIDTH - surf.get_width() - 10, 10))
