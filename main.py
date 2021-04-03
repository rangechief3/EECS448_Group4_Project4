# Author: Jake Wagner
# Date Started: 3/22/2021



import pygame
from Classes.constants import WIDTH, HEIGHT, PLAYER_NAMES
from Classes.game import Game
from Classes.data import Data


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texas Hold 'em")
pygame.init()

# ! not meant for actual game, just helps and clarifies how the methods work in player.py
data = Data(WIN)
print('\t')
player1 = data.players[1]
player1.draw_board()
player1.draw_cards()
player1.info()


# @pre - None
# @param - None
# @description - Runs game loop, using the Game class to direct all of the other classes
def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while running:
        game.gameCycle()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()

    pygame.quit()


main()
