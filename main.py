# Author: Jake Wagner
# Date Started: 3/22/2021


import pygame
from Classes.constants import WIDTH, HEIGHT, PLAYER_NAMES
from Classes.game import Game
#from Classes.data import Data
from Classes.player import Player

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texas Hold 'em")
pygame.init()

# ! not meant for actual game, just helps and clarifies how the methods work in player.py
player = Player(WIN, "Umar", 1, 1000)
print(player)
player.receive_hand([(1, 'H'), (2, 'H')])
player.receive_board_cards([(3, 'K'), (4, 'K'), (5, 'K')])
print("Current stack: " + str(player.stack))
player.receive_money(10)
print("New player stack: " + str(player.stack))
player.draw_card()
player.draw_board()
other_players = []
for i in range(len(PLAYER_NAMES)):
    other_players.append(Player(WIN, PLAYER_NAMES[i], i, 1000))
    other_players[i].receive_hand([(i, 'J'), (i, 'K')])
player.draw_opponents(other_players)

# Copy and pasted the output of code on to terminal for lines 17-31. Or can just compile the code
# Player Name: Umar --- Player Number: 1
# Recieving cards for Umar
# 	Card number: 1 Card suit: H
# 	Card number: 2 Card suit: H
# Receiving board cards
# 	Card number: 3 Card suit: K
# 	Card number: 4 Card suit: K
# 	Card number: 5 Card suit: K
# Current stack: 1000
# New player stack: 1010
# Drew card on board 1 H
# Drew card on board 2 H
# Drew card on board 3 K
# Drew card on board 4 K
# Drew card on board 5 K
# Recieving cards for Daniel Negreanu
# 	Card number: 0 Card suit: J
# 	Card number: 0 Card suit: K
# Recieving cards for Bryn Kenney
# 	Card number: 1 Card suit: J
# 	Card number: 1 Card suit: K
# Recieving cards for Phil Ivey
# 	Card number: 2 Card suit: J
# 	Card number: 2 Card suit: K
# Recieving cards for Justin Bonomo
# 	Card number: 3 Card suit: J
# 	Card number: 3 Card suit: K
# Recieving cards for Erik Seidel
# 	Card number: 4 Card suit: J
# 	Card number: 4 Card suit: K
# Recieving cards for Dan Smith
# 	Card number: 5 Card suit: J
# 	Card number: 5 Card suit: K
# Recieving cards for Stephen Chidwick
# 	Card number: 6 Card suit: J
# 	Card number: 6 Card suit: K
# Recieving cards for Tom Dwan
# 	Card number: 7 Card suit: J
# 	Card number: 7 Card suit: K
# Drew card on board 0 J
# Drew card on board 0 K
# Drew card on board 1 J
# Drew card on board 1 K
# Drew card on board 2 J
# Drew card on board 2 K
# Drew card on board 3 J
# Drew card on board 3 K
# Drew card on board 4 J
# Drew card on board 4 K
# Drew card on board 5 J
# Drew card on board 5 K
# Drew card on board 6 J
# Drew card on board 6 K
# Drew card on board 7 J
# Drew card on board 7 K

# @pre - None
# @param - None
# @description - Runs game loop, using the Game class to direct all of the other classes
def main():
    running = True
    clock = pygame.time.Clock()

    game = Game(WIN)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()

    pygame.quit()


main()
