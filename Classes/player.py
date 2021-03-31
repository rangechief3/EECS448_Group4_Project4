from . data import *
from . constants import *
import time
from . card import Card


class Player:
    def __init__(self, win, player_name, player_num, start_amt):
        self.win = win
        self.player_name = player_name
        self.player_num = player_num
        self.stack = start_amt
        self.hand = []
        self.board_cards = []
        self.buttons = None
        self.curr_hand = None       # Idk what this is
        self.playing = True

    # If needing to print out a player object, will return name and player number. To use in main: print(player)
    def __str__(self):
        return "Player Name: " + self.player_name + " --- " + "Player Number: " + str(self.player_num)


    def blind(self, blind_amt):  
        ###same as in bet, determine if the player has that much money left
        ###if it doesn't then return the maxium amt it cant(subtracting so that self.stack = 0) and the data class will handle
        self.stack -= blind_amt  # if less, return the max they have
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
        print(f'Recieving cards for {self.player_name}')
        for card, tuple in enumerate(hand):
            card_number = tuple[0]
            card_suit = tuple[1]
            self.hand.append(Card(card_number, card_suit))
            print("\t" + str(self.hand[i]))
            i += 1

    # @description - Gets a list of (number, suit), converts into Card object, stores Card objects into the self.hand list
    # @param - A list of numbers that will be the board cards
    # @return - nothing
    def receive_board_cards(self, cards):  # list of cards. WILL be duplicates
        ###Same thing as above, it will come in as Card objects that can be accessed with Card.rank and card.suit
        ###Can Not just use append. Check if the card already exists in self.board_cards before using append
        ### the entire board will be sent each time so there will be duplicates
        i = 0
        print(f"Receiving board cards")
        for card, tuple in enumerate(cards):
            card_number = tuple[0]
            card_suit = tuple[1]
            self.board_cards.append(Card(card_number, card_suit))
            print("\t" + str(self.board_cards[i]))
            i += 1

    # @description - Adds money to the current players stack of money
    # @param - money that will be added to current players stack of money
    # @return - nothing
    def receive_money(self, money):
        self.stack += money

    # @description - Draws each card from current players hand
    # @param - nothing
    # @return - nothing
    def draw_cards(self):
        # each card is an object from card class
        self.hand[0].draw()
        self.hand[1].draw()

    # @description - Draws the board cards
    # @param - nothing
    # @return - nothing
    def draw_board_cards(self):
        for i in range(len(self.board_cards)):
            self.board_cards[i].draw()

    # @description - Draws all the other players cards
    # @param - nothing
    # @return - nothing
    def draw_opponents(self, other_players):
        for player in other_players:
            player.draw_cards()

    # @description - Current player has folded. Players hand is empty
    # @param - nothing
    # @return - nothing
    def fold(self):
        self.playing = False
        self.hand = []

    def take_turn(self, cur_bet, prev_bet):
        # Might need some help with this method. Played poker like 5 times but have no clue how to play.
        ###This will be an input loop similar to what happens in main. We will await input from the user in terms of buttons

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
        pass

    def bet(self, curr_bet, prev_bet):
        ### This was for testing for me, so change this to be based on user input 
        ### self.take_turn() 
        ### keep track of what they do. If they end up calling fold() then return -1, if they bet the same as the current bet, then 
        ### return curr_bet - prev_bet
        ### if they raise, then return the value they raised, etc
        if curr_bet == 0:
            self.stack -= (10 + prev_bet)
            return 10 - prev_bet
        self.stack -= (curr_bet + prev_bet)
        return curr_bet - prev_bet
        # return 0 for check, curr_bet for call, higher value for raise, -1 for fold
        # reduce player stack by bet amount then return it


        ###Add drawing of the board and player symbols, etc. 