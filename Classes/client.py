import pygame
from network import Network
from button import Button
from constants import *
from card import Card
from player import Player
import time
import pickle
pygame.font.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
deck_img = Card(5)
font = pygame.font.SysFont('Arial', SMALL_CARD_FONT_SIZE)

def main():
    running = True
    clock = pygame.time.Clock()
    n = Network()
    print("Created the network")
    
    player_num = int(n.get_player_number())
    print("You are a player object with name: ", player_num)
    player = Player(USER_NAMES[player_num], player_num, START_STACK)
    player.draw_board(win)
    pygame.display.update()
    while running:
        clock.tick(60)
        try:
            data = n.send("get")
            print("sending...")
        except:
            running = False
            print("Couldn't get game")
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()   
    #draw, #receive_hand, #receive_winnings, #receive_board_cards, #receive_pot_value
    #self, win, other_players, front, curr_player): 
    #other_players = draw_parameters[0]
    #front = draw_parameters[1]
    #curr_player = draw_parameters[2]
    #player.draw(win, other_players,)

main()



