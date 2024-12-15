# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from time import sleep

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    # running = True
    color = (0, 0, 0)
    while running:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               return
        screen.fill(color)
        pygame.display.flip()
        sleep(1)


if __name__ == "__main__":
    main()