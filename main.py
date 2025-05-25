import pygame
import audio
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shots import Shot
from score import Score
from screens import exit_screen, start_screen, pause_screen
from utils import Explosion
from ufo import UFO


def main():
    pygame.init()
    audio.intro()         #  <<< startowa muzyczka
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    background = pygame.image.load("assets/background.png").convert()

    # === Start screen ===
    start_screen(screen)

    # === Sprite groups ===
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    ufos = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    # === Containers binding ===
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    UFO.containers = (ufos, updatable, drawable)
    asteroid_field = AsteroidField()

    Player.containers = (drawable, updatable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    score = Score()

    # === Timers ===
    dt = 0
    fps = 0
    ufo_spawn_timer = random.uniform(UFO_MIN_SPAWN_TIME, UFO_MAX_SPAWN_TIME)

    while True:
        # -------------- events --------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_screen(screen)

        # -------------- logic --------------
        # update timers
        ufo_spawn_timer -= dt
        if ufo_spawn_timer <= 0:
            # spawn new UFO
            direction = random.choice([-1, 1])
            y = random.uniform(50, SCREEN_HEIGHT - 50)
            if direction == 1:
                x = -UFO_RADIUS
                velocity = pygame.Vector2(UFO_SPEED, 0)
            else:
                x = SCREEN_WIDTH + UFO_RADIUS
                velocity = pygame.Vector2(-UFO_SPEED, 0)
            ufo = UFO(x, y)
            ufo.velocity = velocity
            ufo_spawn_timer = random.uniform(UFO_MIN_SPAWN_TIME, UFO_MAX_SPAWN_TIME)

        # update all objects
        for obj in updatable:
            obj.update(dt)

        # -------------- collisions --------------
        # player vs asteroids
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                if player.invulnerability_timer <= 0:
                    explosions.add(Explosion(player.position))
                player.handle_collision(screen, score, exit_screen, main, asteroids, explosions)
                break

        # player vs UFO
        for ufo in ufos:
            if ufo.collides_with(player):
                if player.invulnerability_timer <= 0:
                    explosions.add(Explosion(player.position))
                player.handle_collision(screen, score, exit_screen, main, asteroids, explosions)
                ufo.kill()
                break
      
        # asteroid vs shots
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    explosions.add(Explosion(asteroid.position))
                    asteroid.split()
                    shot.kill()
                    score.add_points(asteroid.get_points())

        # UFO vs shots
        for ufo in ufos:
            for shot in shots:
                if ufo.collides_with(shot):
                    explosions.add(Explosion(ufo.position))
                    shot.kill()
                    ufo.kill()
                    score.add_points(ufo.get_points())

        # -------------- drawing --------------
        screen.blit(background, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        score.draw(screen)
        player.draw_lives(screen, fps)

        explosions.update(dt)
        explosions.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000
        fps = clock.get_fps()


if __name__ == "__main__":
    main()
