import pygame
from network import Network
from button import Button
from constants import WIDTH, HEIGHT
import pickle
pygame.font.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


def main():
    running = True
    clock = pygame.time.Clock()
    n = Network()
    try:
        player = n.get_player_object()
        print("You are a player object", player.player_num)
    except:
        print("Could not connect")
        running = False

    while running:
        clock.tick(60)
        try:
            data = n.send("get")
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



