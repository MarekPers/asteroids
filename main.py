import pygame
from constants import *
from time import sleep


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    running = True
    color = (0, 0, 0)
    while running:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
        screen.fill(color)
        pygame.display.flip()
        sleep(1)


if __name__ == "__main__":
    main()