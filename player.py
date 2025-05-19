import pygame
from constants import *
from utils import CircleShape
from shots import Shot
from utils import Explosion

class Player(CircleShape):
    def __init__(self, x, y, lives=3):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.lives = lives
        self.invulnerability_timer = 0

        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect(center=(x, y))

    def handle_collision(self, screen, score, exit_screen, restart_game, asteroids, explosions):
        if self.invulnerability_timer > 0:
            return  # Nie tracimy życia i nie generujemy eksplozji
        self.lives -= 1
        self.invulnerability_timer = 2
        # Eliminacja asteroid w promieniu 3x długości statku i dodanie eksplozji
        for asteroid in asteroids:
            if self.position.distance_to(asteroid.position) <= 3 * self.radius:
                explosions.add(Explosion(asteroid.position))
                asteroid.kill()
                score.add_points(asteroid.get_points())
        if self.lives <= 0:
            exit_screen(screen, score.get_score())
            restart_game()

    def draw(self, screen):
        if self.invulnerability_timer > 0:
            # Miganie co klatkę
            if int(self.invulnerability_timer * 10) % 2 == 0:
                # Błękitna obwódka
                pygame.draw.circle(screen, (0, 255, 255), self.rect.center, self.radius + 5, width=3)
            # Miganie postaci
            rotated_image = pygame.transform.rotate(self.image, -self.rotation)
            new_rect = rotated_image.get_rect(center=self.position)
            screen.blit(rotated_image, new_rect.topleft)
        else:
            # Standardowe rysowanie
            rotated_image = pygame.transform.rotate(self.image, -self.rotation)
            new_rect = rotated_image.get_rect(center=self.position)
            screen.blit(rotated_image, new_rect.topleft)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        self.rect.center = self.position

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def draw_lives(self, screen):
        font = pygame.font.Font(None, 36)
        lives_text = f"LIVES: {self.lives}"
        text_surface = font.render(lives_text, True, (255, 255, 255))
        screen.blit(text_surface, (SCREEN_WIDTH - 150, 10))