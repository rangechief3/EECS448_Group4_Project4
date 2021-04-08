import random 
from . data import *
from . constants import *
from . button import *
import time
from . card import Card
import gc
import pygame
import sys

class Player:
    def __init__(self, win, player_name, player_num, start_amt):
        self.win = win
        self.player_name = player_name
        self.player_num = player_num
        self.stack = start_amt
        self.hand = []
        self.board_cards = []
        self.buttons = []
        self.curr_hand = None
        self.playing = True
        self.hand_num = 0
        self.high_card = 0
        self.chip_pos = self.get_chip_pos()
        self.card_pos = self.get_card_pos()
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
        ###With that poker module, the cards are actually already in a built-in class(maybe it would have been easier to just implement with numbers idk)
        ### but it will come in a Card object. To get the rank and suit, they can be accessed with card.suit and card.rank
        ###  these will return strings for the rank(2-9 or T,J,Q,K,A) and suit. The suits are special characters. I have these in the constants in data.py
        ### and have added them to this branch
        i = 0
        for card in hand:
            #if i % 2 == 0:
            #print("[player.py] " + self.player_name + " receiving cards:")
            self.hand.append(card)
            #print(f'\t [player.py] Added to hand: {self.hand[i]}')
            i += 1

    # @description - Gets a list of (number, suit), converts into Card object, stores Card objects into the self.hand list
    # @param - A list of numbers that will be the board cards
    # @return - nothing
    def receive_board_cards(self, cards, str):  # list of cards. WILL be duplicates
        ###Same thing as above, it will come in as Card objects that can be accessed with Card.rank and card.suit
        ###Can Not just use append. Check if the card already exists in self.board_cards before using append
        ### the entire board will be sent each time so there will be duplicates
        #print(f'[player.py] {self.player_name} has access to the board cards:')
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

    def take_turn(self, cur_bet, prev_bet):
        # Might need some help with this method. Played poker like 5 times but have no clue how to play.
        ###This will be an input loop similar to what happens in main. We will await input from the user in terms of buttons

        for button in self.buttons:
            if button == button.clickable:
                pass
            else:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pass
        ### for btn in self.btns:
        ###     btn.activate will make it appear, otherwise it will be hidden
        ### while not input:
        ###
        ###     for event in pygame.event.get():
        ###         if event.type == pygame.MOUSEBUTTONDONW
        ###             check if it hit a button in self.btns - these will include FOLD, CALL, CHECK, RAISE, CONFIRM or
        ###                                                     something that can do those functions. The reason for confirm
        ###                                                     would be so that a person could click raise several times
        ###             if it should do something, FOLD, CALL, CHECK, etc then do it
        ###             and end the loop
        ###
        ###ACTUALLY, JUST GET RID OF BET() AND JUST DO TAKE_TURN

        ###Add drawing of the board and player symbols, etc.

    # @description - Draws each card from current players hand
    # @param - front True if drawing front false if back
    # @return - nothing
    def draw_cards(self, front):
        # each card is an object from card class
        #print(f'[player.py] Drawing cards on screen for player {self.player_name}')
        self.hand[0].draw(self.win, self.card_pos[0], self.card_pos[1], front)
        self.hand[1].draw(self.win, self.card_pos[0] + CARD_WIDTH + GAP, self.card_pos[1], front)
        pass
        # print(f'[player.py] Drawing {self.player_name} 1st card on screen: {self.hand[0].draw(self.win, 800, 800)}')
        # print(f'[player.py] Drawing {self.player_name} 2nd card on screen: {self.hand[1].draw(self.win, 500, 500)}')
        # Running into errors using Card.draw(), will fix tom

    # @description - Draws the board cards
    # @param - nothing
    # @return - nothing
    def draw_board_cards(self):
        #print(f'[player.py] Drawing board cards on screen for player {self.player_name}')
        for i, card in enumerate(self.board_cards):
            #def draw(self, win, topX, topY, front):
            card.draw(self.win, 560 + 5 *(i+1) + OFFSET + i* CARD_WIDTH, 365 + 15 // 2, True)
        '''
        board_card_box = pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (560 + OFFSET, 365, BOARD_CARD_BOX_X, BOARD_CARD_BOX_Y))
        board_card_1 = self.board_cards[0][0].draw(self.win, 560 + 5 * 1 + OFFSET, 365 + 15 // 2)
        board_card_2 = self.board_cards[0][1].draw(self.win, 560 + 5 * 2 + 1 * CARD_WIDTH + OFFSET, 365 + 15 // 2)
        board_card_3 = self.board_cards[0][2].draw(self.win, 560 + 5 * 3 + 2 * CARD_WIDTH + OFFSET, 365 + 15 // 2)
        try:
            board_card_4 =self.board_cards[0][3].draw(self.win, 560 + 5 * 4 + 3 * CARD_WIDTH + OFFSET, 365 + 15 // 2)
        except:
            print('[player.py] There are current only 3 board cards. Drawing 2 blank cards')
            board_card_4 = pygame.draw.rect(self.win, WHITE, (560 + 5 * 4 + 3 * CARD_WIDTH + OFFSET, 365 + 15 // 2, CARD_WIDTH, CARD_HEIGHT))
        try:
            board_card_5 =self.board_cards[0][4].draw(self.win, 560 + 5 * 5 + 4 * CARD_WIDTH + OFFSET, 365 + 15 // 2)
        except:
            print('[player.py] There are current only 4 board cards. Drawing 1 blank cards')
            board_card_5 = pygame.draw.rect(self.win, WHITE, (560 + 5 * 5 + 4 * CARD_WIDTH + OFFSET, 365 + 15 // 2, CARD_WIDTH, CARD_HEIGHT))
        '''

    # @description - Draws the user interface
    # @param - other_players -- > list of players other than the current player
    # @return - nothing
    def draw(self, other_players, front): 
        self.draw_board()
        self.draw_chips() 
        self.draw_board_cards()
        self.draw_cards(True)
        self.button_area()
        self.draw_opponents(other_players, front)
        pygame.display.update()

    # @description - Draws all the other players cards
    # @param - nothing
    # @return - nothing
    def draw_opponents(self, other_players, front):
        #print(f'[player.py] Drawing card/hands of other players')
        for player in other_players:
            player.draw_cards(front) #boolean for which side to draw            
            player.draw_chips()
        # Running into errors using Card.draw(), will fix tom

    def draw_board(self):
        self.win.fill(BACKGROUND_COLOR)
        board = pygame.draw.circle(self.win, BOARD_COLOR, (WIDTH // 2 + OFFSET, HEIGHT // 2), BOARD_RADIUS)
        inner_circle = pygame.draw.circle(self.win, WHITE, (WIDTH // 2 + OFFSET, HEIGHT // 2), INNER_BORDER_RADIUS, width=1)
              # Won't need if for loop works
        

    def draw_chips(self):
        pygame.draw.circle(self.win, WHITE, (self.chip_pos[0] + OFFSET, self.chip_pos[1]), CHIP_SIZE)
        self.win.blit(self.font.render(str(self.stack), True, BLACK), (self.chip_pos[0] - (TOKEN_FONT_SIZE // 2) + OFFSET, self.chip_pos[1] - (TOKEN_FONT_SIZE // 2)))
        #print(f'[player.py] Chip coordinates for {self.player_name}: {self.chip_pos}')

    def info(self):
        pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (25, 25, INFO_BOX_WIDTH, INFO_BOX_HEIGHT))
        self.hand[0].draw_big(self.win, 35, 35)
        self.hand[1].draw_big(self.win, 35 + MAG_CARD_WIDTH + 15, 35)
        self.win.blit(self.font.render(f'{self.player_name} Stack = {self.stack}', True, BLACK), (25, 15 + MAG_CARD_HEIGHT + 30))
        self.win.blit(self.font.render(f'Idk what other info', True, BLACK), (25, 15 + MAG_CARD_HEIGHT + 30 + TOKEN_FONT_SIZE))

    def button_area(self):
        pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (25, HEIGHT - INFO_BOX_HEIGHT, 115, INFO_BOX_HEIGHT - 50))
        button1 = Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17, f'Check')
        button1.draw()
        button2 = Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17 * 2 + 40 * 1, f'Call')
        button2.draw()
        button3 = Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17 * 3 + 40 * 2, f'Raise')
        button3.draw()
        button4 = Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17 * 4 + 40 * 3, f'Fold')
        button4.draw()

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

    def get_card_pos(self):
        if self.player_num == 0:
            return (475 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif self.player_num == 1:
            return (582 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif self.player_num == 2:
            return (850 - CARD_WIDTH, 775 - CARD_WIDTH - 30)
        elif self.player_num == 3:
            return (1117 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif self.player_num == 4:
            return (1225 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif self.player_num == 5:
            return (1112 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        elif self.player_num == 6:
            return (850 - CARD_WIDTH, 25 - (CARD_WIDTH // 2) + 10)
        elif self.player_num == 7:
            return (582 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        else:
            return "Error in get_card_pos()"

    def takeATurn(self, curr_bet, prev_bet):
        time.sleep(0.5)
        return self.bet(curr_bet, prev_bet)

    def bet(self, curr_bet, prev_bet):
        ### This was for testing for me, so change this to be based on user input
        ### self.take_turn()
        ### keep track of what they do. If they end up calling fold() then return -1, if they bet the same as the current bet, then
        ### return curr_bet - prev_bet
        ### if they raise, then return the value they raised, etc
        if curr_bet == 0:
            self.stack -= (10 - prev_bet)
            return 10 - prev_bet
        self.stack -= (curr_bet - prev_bet)
        return curr_bet - prev_bet
        # return 0 for check, curr_bet for call, higher value for raise, -1 for fold
        # reduce player stack by bet amount then return it
    
    '''
        def bet(self, curr_bet, prev_bet):
        if curr_bet == 0:
            bet = int(random.random() * 100)
            self.stack -= bet
            return bet
        elif curr_bet > (self.stack + prev_bet):
            bet = self.stack
            self.stack = 0
            return bet
        else:
            bet = curr_bet - prev_bet
            self.stack -= bet
            return bet
        #return 0 for check, curr_bet for call, higher value for raise, -1 for fold
        #reduce player stack by bet amount then return it
    '''

        
             