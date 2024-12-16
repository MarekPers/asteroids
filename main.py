import pygame
from constants import *


def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    running = True
    color = (0, 0, 0)
    while running:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
        screen.fill(color)
        pygame.display.flip()
        dt = clock.tick(60)/1000


if __name__ == "__main__":
    main()