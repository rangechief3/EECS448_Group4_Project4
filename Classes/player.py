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

    def bet(self, curr_bet, prev_bet):
        if curr_bet == 0:
            self.stack -= (10 + prev_bet)
            return 10 - prev_bet
        self.stack -= (curr_bet + prev_bet)
        return curr_bet - prev_bet
        # return 0 for check, curr_bet for call, higher value for raise, -1 for fold
        # reduce player stack by bet amount then return it

    def blind(self, blind_amt):  # check if the player has that much, if so, return that much
        self.stack -= blind_amt  # if less, return the max they have
        return blind_amt

    # @description - Gets a list of (number, suit), converts into Card object, stores Card objects into the self.hand list
    # @param - A list of cards that will be the objects hand
    # @return - nothing
    def receive_hand(self, hand):
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
    def draw_card(self):
        # each card is an object from card class
        self.hand[0].draw()
        self.hand[1].draw()

    # @description - Draws the board cards
    # @param - nothing
    # @return - nothing
    def draw_board(self):
        for card in range(len(self.board_cards)):
            self.board_cards[card].draw()

    # @description - Draws all the other players cards
    # @param - nothing
    # @return - nothing
    def draw_opponents(self, other_players):
        for player in other_players:
            player.draw_card()

    # @description - Current player has folded. Players hand is empty
    # @param - nothing
    # @return - nothing
    def fold(self):
        self.playing = False
        self.hand = []

    def take_turn(self, cur_bet):
        # Might need some help with this method. Played poker like 5 times but have no clue how to play.
        pass
