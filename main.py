import pygame

from objects import Game, GameMenu
from SETTINGS import (GAME_NAME, WIDTH, HEIGHT)


# Sound presets: frequency, size, channels, buffer
pygame.mixer.pre_init(44100, -16, 2, 512)

pygame.init()
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()


if __name__ == "__main__":
    game = Game(canvas, clock)
    menu = GameMenu(canvas, game)
    menu.call()
