# Author: Jake Wagner
# Date Started: 3/22/2021

import pygame
from Classes.constants import WIDTH, HEIGHT, PLAYER_NAMES
from Classes.game import Game
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texas Hold 'em")
pygame.init()

# @pre - None
# @param - None
# @description - Runs game loop, using the Game class to direct all of the other classes
def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game.gameCycle()
    '''
    while running:
        game.gameCycle()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()

    pygame.quit()
    '''

main()
