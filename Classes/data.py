# Auther: Jake Wagner
# Date Started:

import random
import re
#from pokercards import cards
from poker import Card
from .constants import BIG_BLIND, PLAYER_NAMES, START_STACK, HANDS, SUITS
from .player import Player

class Data:

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
            print(hand)
   
    def flop(self):
        self.deck.pop() #burn one card before dealing
        for i in range(3):
            self.table_cards.append(self.deck.pop())
        print(self.table_cards)
        for player in self.players:
            player.receive_board_cards(self.table_cards)
    
    
    def check_duplicates(self, player_num): #will determine pairs, two pairs, three of a kind, four of a kind, full house
        player_cards = self.table_cards + self.player_cards[player_num]
        ranks = {} #dict with the number of a card as the key, points to the number of those cards
        max_of_kind = 0
        pairs = 0
        for card in player_cards:
            if card[0] in ranks:
                if ranks[card[0]] == 1: #if there has already been at least a pair
                    pairs += 1
                ranks[card[0]] += 1
                max_of_kind = max(max_of_kind, ranks[card[0]])
            ranks[card[0]] = 1
        if max_of_a_kind == 4:
            return 7 #four of a kind
        elif max_of_a_kind == 3:
            if pairs == 2:
                return 6 #full house
            return 3 #three of a kind
        elif pairs == 2:
            return 2 #two pairs
        elif pairs == 0:
            return 1 #one pair
        else:
            return 0 #did not find anything
        
                    




    
    

