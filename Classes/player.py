import random 
from data import *
from constants import *
from button import *
import time
from card import Card
import gc
import pygame
import sys

FPS = 60

class Player:
    def __init__(self, player_name, player_num, start_amt): #remove the windows as a parameter
        self.player_name = player_name
        self.player_num = player_num
        self.stack = start_amt
        self.deck_img = Card(5)
        self.hand = []
        self.board_cards = []
        self.buttons = []
        self.curr_hand = None
        self.playing = True
        self.hand_num = 0
        self.high_card = 0
        self.init_buttons()
        self.chip_pos = self.get_chip_pos()
        self.card_pos = self.get_card_pos(self.player_num)
        self.font = pygame.font.SysFont('Arial', SMALL_CARD_FONT_SIZE)

    # If needing to print out a player object, will return name and player number. To use in main: print(player)
    def __str__(self):
        return "Player Name: " + self.player_name + " --- " + "Player Number: " + str(self.player_num)

    def receive_winnings(self, amt):
        self.stack += amt

    def receive_top_hand_and_card(self, hand_num, high_card): #both int
        self.hand_num = hand_num
        self.high_card = high_card

    # @return - How much the player is paying for the blind (Not sure if the self.stack is suppose to be manipulated)
    def blind(self, blind_amt):  
        ###same as in bet, determine if the player has that much money left
        ###if it doesn't then return the maxium amt it cant(subtracting so that self.stack = 0) and the data class will handle
        copy_stack = self.stack
        copy_stack -= blind_amt
        # ? return the amount player added to blind ?
        '''
        if copy_stack < 0:
            print(str(self.stack) + ' - ' + str(blind_amt) + " = " + str(copy_stack))
            new_blind_amt = self.stack
            self.stack = 0
            return new_blind_amt
        else:
        '''
        self.stack -= blind_amt
        return blind_amt

    # @description - Gets a list of (number, suit), converts into Card object, stores Card objects into the self.hand list
    # @param - A list of cards that will be the objects hand
    # @return - nothing
    def receive_hand(self, hand):
        for card in hand:
            self.hand.append(card)
    
    # @description - changes relevant cards to be null 
    # @param - None
    # @return - None
    def reset(self):
        self.board_cards = []
        self.hand = []
        self.hand_num = 0
        self.playing = True
        self.high_card = 0


    # @description - Gets a list of (number, suit), converts into Card object, stores Card objects into the self.hand list
    # @param - A list of numbers that will be the board cards
    # @return - nothing
    def receive_board_cards(self, cards, str):  
        for card in cards:
            self.board_cards.append(card)

    # @description - Adds money to the current players stack of money
    # @param - money that will be added to current players stack of money
    # @return - nothing
    def receive_money(self, money):
        self.stack += money

    # @description - Current player has folded. Players hand is empty
    # @param - nothing
    # @return - nothing
    def fold(self):
        self.playing = False
        self.hand = []

    #def takeATurn(self, curr_bet, prev_bet):
    #    time.sleep(0.5)
    #    return self.bet(curr_bet, prev_bet)

    def get_x_y(self, pos):
        x = pos[0]
        y= pos[1]
        return x,y 

    def draw_current_player_turn_indicator(self, x, y, win):
        border_thickness = 3
        width = border_thickness* 2 + CARD_WIDTH * 2 + GAP
        height = border_thickness* 2 + CARD_HEIGHT
        #card.draw(self.win, self.card_pos[0] + i*CARD_WIDTH + i*GAP, self.card_pos[1], front)
        pygame.draw.rect(win, (0, 255, 0), (x, y, width, height), border_thickness)

    def takeATurn(self, cur_bet, prev_bet, win):
        clock = pygame.time.Clock()
        running = True
        x,y = -1, -1
        while running:
            clock.tick(FPS)
            self.draw_current_player_turn_indicator(self.card_pos[0] - 3, self.card_pos[1] - 3, win)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x,y = self.get_x_y(pos)
            ## (Check, Call, Raise, Fold)
            if x != -1 and y != -1:
                for i,button in enumerate(self.buttons):
                    if (button.x <= x < (button.x + button.width)) and (button.y < y < (button.y + button.height)):
                        if button.clickable:

                            if i == 0: #check
                                if (cur_bet - prev_bet) == 0:
                                    return 0
                            elif i == 1: #call
                                self.update_stack(cur_bet-prev_bet)
                                return cur_bet - prev_bet
                            elif i == 2: #raise
                                self.update_stack(cur_bet * 2 - prev_bet)
                                return cur_bet * 2
                            elif i == 3: #fold
                                self.playing = False
                                return -1
            else:
                pass #waiting for input
            pygame.display.update()


    # @description - Draws each card from current players hand
    # @param - front True if drawing front false if back
    # @return - nothing
    def draw_cards(self, win, front ):
        if self.playing:
            for i, card in enumerate(self.hand):
                card.draw(win, self.card_pos[0] + i*CARD_WIDTH + i*GAP, self.card_pos[1], front)

    def draw_player_name(self, win, x, y, name):
        win.blit(self.font.render(name, True, BLACK), (x - (TOKEN_FONT_SIZE // 2) + OFFSET, y - (TOKEN_FONT_SIZE // 2)))

    # @description - Draws the board cards
    # @param - nothing
    # @return - nothing
    def draw_board_cards(self, win):
        for i, card in enumerate(self.board_cards):
            card.draw(win, 560 + 5 *(i+1) + OFFSET + i* CARD_WIDTH, 365 + 15 // 2, True)

    # @description - Draws the user interface
    # @param - other_players -- > list of players other than the current player
    # @return - nothing
    def draw(self, win, other_players, front, curr_player): 
        self.draw_board(win)
        self.draw_chips(win) 
        self.draw_board_cards(win)
        self.draw_cards(win,True)
        self.draw_player_name(win,self.chip_pos[0] - 3* len(self.player_name), self.chip_pos[1] + 50, self.player_name)
        self.draw_buttons(win)
        self.draw_deck(win)
        self.draw_opponents(win,other_players, front)
        if curr_player != None:
            if curr_player != 0:
                curr_player = 8 + curr_player
            pos = self.get_card_pos(curr_player)
            self.draw_current_player_turn_indicator(win,pos[0] - 3, pos[1] - 3)
        pygame.display.update()

    # @description - draws the deck
    # @param - None
    # @return - nothing
    def draw_deck(self, win): 
        self.deck_img.draw_deck(win)

    # @description - Draws all the other players cards
    # @param - nothing
    # @return - nothing
    def draw_opponents(self, win,other_players, front):
        for player in other_players:
            if player.playing:
                player.draw_cards(win,front) #boolean for which side to draw            
            player.draw_chips(win)
            sign = 1
            if player.chip_pos[1] < HEIGHT//2:
                sign = -1
            str_length = len(player.player_name)
            player.draw_player_name(win,player.chip_pos[0]-3 * str_length , player.chip_pos[1] - 50* sign, player.player_name)

    def draw_board(self, win):
        win.fill(BACKGROUND_COLOR)
        board = pygame.draw.circle(win, BOARD_COLOR, (WIDTH // 2 + OFFSET, HEIGHT // 2), BOARD_RADIUS)
        inner_circle = pygame.draw.circle(win, WHITE, (WIDTH // 2 + OFFSET, HEIGHT // 2), INNER_BORDER_RADIUS, width=1)

    def draw_chips(self, win):
        pygame.draw.circle(win, WHITE, (self.chip_pos[0] + OFFSET, self.chip_pos[1]), CHIP_SIZE)
        win.blit(self.font.render(str(self.stack), True, BLACK), (self.chip_pos[0] - (TOKEN_FONT_SIZE // 2) + OFFSET, self.chip_pos[1] - (TOKEN_FONT_SIZE // 2)))

    def init_buttons(self):
        self.buttons.append(Button( 30, HEIGHT - INFO_BOX_HEIGHT + 17, f'Check') )
        self.buttons.append(Button( 30, HEIGHT - INFO_BOX_HEIGHT + 17 * 2 + 40 * 1, f'Call'))
        self.buttons.append(Button( 30, HEIGHT - INFO_BOX_HEIGHT + 17 * 3 + 40 * 2, f'Raise'))
        self.buttons.append(Button( 30, HEIGHT - INFO_BOX_HEIGHT + 17 * 4 + 40 * 3, f'Fold'))
        self.buttons.append(Button( 60, HEIGHT - INFO_BOX_HEIGHT + 17 * 4 + 40 * 3, f'Confirm Raise'))
    
    def draw_buttons(self, win):
        pygame.draw.rect(win, BOARD_CARDS_BOX_COLOR, (25, HEIGHT - INFO_BOX_HEIGHT, 115, INFO_BOX_HEIGHT - 50))
        for button in self.buttons:
            button.draw(win)

    def get_chip_pos(self):
        if self.player_num == 0:
            return (437.5, 400)
        elif self.player_num == 1:
            return (525, 575)
        elif self.player_num == 2:
            return (700, 662.5)
        elif self.player_num == 3:
            return (875, 575)
        elif self.player_num == 4:
            return (962.5, 400)
        elif self.player_num == 5:
            return (875, 225)
        elif self.player_num == 6:
            return (700, 137.5)
        elif self.player_num == 7:
            return (525, 225)
        else:
            return "Error in get_chip_pos()"

    def get_card_pos(self, player_num):
        if player_num == 0:
            return (475 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif player_num == 1:
            return (582 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif player_num == 2:
            return (850 - CARD_WIDTH, 775 - CARD_WIDTH - 30)
        elif player_num == 3:
            return (1117 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif player_num == 4:
            return (1225 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif player_num == 5:
            return (1112 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        elif player_num == 6:
            return (850 - CARD_WIDTH, 25 - (CARD_WIDTH // 2) + 10)
        elif player_num == 7:
            return (582 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        else:
            return "Error in get_card_pos()"

    def update_stack(self, amt):
        self.stack -= amt

    def bet(self, curr_bet, prev_bet):
        if curr_bet == 0:
            self.stack -= (10 - prev_bet)
            return 10 - prev_bet
        self.stack -= (curr_bet - prev_bet)
        return curr_bet - prev_bet
        # return 0 for check, curr_bet for call, higher value for raise, -1 for fold
        # reduce player stack by bet amount then return it
    
    def playAgainQuery(self, win):
        buttonyes = Button(win, 30, HEIGHT - INFO_BOX_HEIGHT + 17, f'yes')
        buttonyes.draw()
        buttonno = Button(win, 30, HEIGHT - INFO_BOX_HEIGHT + 17, f'no')
        buttonno.draw()


        
             