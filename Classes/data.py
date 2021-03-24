# Auther: Jake Wagner
# Date Started:

import random
import re
#from pokercards import cards
from poker import Card
from .constants import BIG_BLIND, PLAYER_NAMES, START_STACK
from .player import Player

class Data:

    SUITS = ['♣','♦','♠','♥']
    HANDS = ['High Card', 'Pair', 'Two Pair', 'Three of a kind', 
             'Straight', 'Flush', 'Full House', 'Four of a kind',
             'Straight Flush', 'Royal Flush']

    #m = re.fullmatch('([2-9]|[ATJQK])[♣♦♠♥]', str(card))
    def __init__(self, win):
        self.win = win
        self.deck = list(Card)
        random.shuffle(self.deck)
        self.curr_bet = BIG_BLIND
        self.players = []
        self.pots = []
        self.table_cards = []
        self.player_hands = []
        self.dealer = 0
        self.init_players(8)
        self.deal()
        self.flop()

    def init_players(self, num_players):
        for i in range(num_players):
            self.players.append(Player(self.win, PLAYER_NAMES[i], i, START_STACK))
            print(self.players[i].player_name)
    
    def deal(self):
        for i in range(len(self.players)):
            hand = [self.deck.pop() for card in range(2)]
            self.player_hands.append(hand)
            self.players[i].receive_hand(hand)
   
    def flop(self):
        self.deck.pop() #burn one card before dealing
        for i in range(3):
            self.table_cards.append(self.deck.pop())
        print(self.table_cards)
        for player in self.players:
            player.receive_board_cards(self.table_cards)
    

    
    

