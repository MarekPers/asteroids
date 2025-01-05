import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shots import Shot
from score import Score
from exit import exit_screen
from explosion import Explosion


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    background = pygame.image.load("assets/background.png").convert()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Player.containers = (drawable, updatable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    score = Score()

    dt = 0


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                if player.invulnerability_timer <= 0:
                    explosions.add(Explosion(player.position))
                player.handle_collision(screen, score, exit_screen, main, asteroids, explosions)
                break

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    explosions.add(Explosion(asteroid.position))
                    asteroid.split()
                    shot.kill()
                    score.add_points(asteroid.get_points())

        screen.blit(background, (0,0))

        for obj in drawable:
            obj.draw(screen)

        score.draw(screen)
        player.draw_lives(screen)

        explosions.update(dt)
        explosions.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()