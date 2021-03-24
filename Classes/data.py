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
        self.turn()
        self.river()
        self.current_winner()

    def init_players(self, num_players):
        for i in range(num_players):
            self.players.append(Player(self.win, PLAYER_NAMES[i], i, START_STACK))
            #print(self.players[i].player_name)
    
    def deal(self):
        for i in range(len(self.players)):
            hand = [self.deck.pop() for card in range(2)]
            self.player_hands.append(hand)
            self.players[i].receive_hand(hand)
            print(hand, self.players[i].player_name)
   
    def flop(self):
        self.deck.pop() #burn one card before dealing
        for i in range(3):
            self.table_cards.append(self.deck.pop())
        #print(self.table_cards)
        for player in self.players:
            player.receive_board_cards(self.table_cards)

    def turn(self):
        self.deck.pop() #burn one card before_dealing
        self.table_cards.append(self.deck.pop())
        #print(self.table_cards)
        for player in self.players:
            player.receive_board_cards(self.table_cards)

    def river(self):
        self.deck.pop() #burn one card before_dealing
        self.table_cards.append(self.deck.pop())
        print(self.table_cards)
        print('\n')
        for player in self.players:
            player.receive_board_cards(self.table_cards)

    def current_winner(self):
        for i in range(len(self.players)):
            hand_num = self.check_duplicates(i)
            print(self.players[i].player_name + " has a " + HANDS[hand_num])

    def is_flush(self, player_num): #returns true or false
        player_cards = self.table_cards + self.player_hands[player_num]
        suits = {}
        max_in_suit = 0
        for card in player_cards:
            if card.suit in suits:
                suits[card.suit] = suits[card.suite] + 1
                max_in_suit = max(max_in_suit, suits[card.suit])
            else:
                suits[card.suit] = 1
        if max_in_suit >= 5:
            return True
        return False

    def check_duplicates(self, player_num): #will determine pairs, two pairs, three of a kind, four of a kind, full house
        player_cards = self.table_cards + self.player_hands[player_num]
        ranks = {} #dict with the number of a card as the key, points to the number of those cards
        max_of_a_kind = 1
        pairs = 0
        for card in player_cards:
            if card.rank in ranks:
                if ranks[card.rank] == 1: #if this card has NOT been paired
                    pairs += 1
                ranks[card.rank] = ranks[card.rank] + 1
                max_of_a_kind = max(max_of_a_kind, ranks[card.rank])
            else:
                ranks[card.rank] = 1
        print(ranks)
        print("max of a kind", max_of_a_kind)
        print("pairs", pairs)
        if max_of_a_kind == 4:
            return 7 #four of a kind
        elif max_of_a_kind == 3:
            if pairs >= 2:
                return 6 #full house
            return 3 #three of a kind
        elif pairs >= 2:
            return 2 #two pairs
        elif pairs == 1:
            return 1 #one pair
        else:
            return 0 #did not find anything
        
                    




    
    

