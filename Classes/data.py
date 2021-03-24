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
    # @description - SETS the game data, initializing the player classes
    # @param - win    pygame WINDOW passed to players for printing purposes
    # @return - None
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

    # @description - resets the data that changes with each hand
    # @param - None
    # @return - None
    def reset(self):
        self.deck = list(Card)
        random.shuffle(self.deck)
        self.curr_bet = BIG_BLIND
        self.pots = []
        self.table_cards = []
        self.player_hands = []

    '''
    def test_flush(self): #used to set values of player cards rather than random
        #['♣','♦','♠','♥']
        self.player_hands.append([Card('K♥'), Card('2♥')]) #royal flush
        self.player_hands.append([Card('8♥'), Card('9♥')]) #straight flush
        self.player_hands.append([Card('7♦'), Card('7♥')]) #four of a kind
        self.player_hands.append([Card('J♣'), Card('J♦')]) #full house
        self.player_hands.append([Card('2♥'), Card('4♥')]) #flush
        self.player_hands.append([Card('8♦'), Card('9♣')]) #straight
        self.player_hands.append([Card('7♦'), Card('6♣')]) #3 of a kind
        self.player_hands.append([Card('T♠'), Card('3♣')]) #2 pair
        self.table_cards.append(Card('7♣'))
        self.table_cards.append(Card('7♠'))
        self.table_cards.append(Card('Q♥'))
        self.table_cards.append(Card('J♥'))
        self.table_cards.append(Card('T♥'))
        for i in range(len(self.player_hands)):
            print(self.player_hands[i], self.players[i].player_name)
        self.current_winner()
    '''

    # @description - Creates Player objects 
    # @param - num_players   determines how many Player objects will be created
    # @return - None
    def init_players(self, num_players):
        for i in range(num_players):
            self.players.append(Player(self.win, PLAYER_NAMES[i], i, START_STACK))
            #print(self.players[i].player_name)

    # @description - gives each player two cards, sending data to player and storing in self.player_hands
    # @param - None
    # @return - None
    def deal(self):
        print("ROUND STARTING\n")
        for i in range(len(self.players)):
            hand = [self.deck.pop() for card in range(2)]
            self.player_hands.append(hand)
            self.players[i].receive_hand(hand)
            print(hand, self.players[i].player_name)

    # @description - draws three cards for the board, sending the data to players and storing in self.table_cards
    # @param - None
    # @return - None
    def flop(self):
        self.deck.pop() #burn one card before dealing
        for i in range(3):
            self.table_cards.append(self.deck.pop())
        #print(self.table_cards)
        for player in self.players:
            player.receive_board_cards(self.table_cards)

    # @description - draws one card(the fourth on the board), and updates the data structures dependent on it
    # @param - None
    # @return - None
    def turn(self):
        self.deck.pop() #burn one card before_dealing
        self.table_cards.append(self.deck.pop())
        #print(self.table_cards)
        for player in self.players:
            player.receive_board_cards(self.table_cards)

    # @description - draws one card(the fifth on the board), and updates the data structures dependent on it
    # @param - None
    # @return - None
    def river(self):
        self.deck.pop() #burn one card before_dealing
        self.table_cards.append(self.deck.pop())
        print(self.table_cards)
        print('\n')
        for player in self.players:
            player.receive_board_cards(self.table_cards)

    # @description - determines the hands that each player has, and determines the winner
    # @param - None
    # @return - will return the winning player(s)
    def current_winner(self):
        for i in range(len(self.players)):
            hand_num = max(self.check_duplicates(i), self.check_straights_flushes(i))
            print(self.players[i].player_name + " has a " + HANDS[hand_num])

    # @description - determines if a player's hand is a flush
    # @param - player_num   index of player being checked
    # @return - True  if five cards of a suit exist 
    def is_flush(self, player_num): #returns true or false
        player_cards = self.table_cards + self.player_hands[player_num]
        suits = {}
        max_in_suit = 0
        for card in player_cards:
            if card.suit in suits:
                suits[card.suit] = suits[card.suit] + 1
                max_in_suit = max(max_in_suit, suits[card.suit])
            else:
                suits[card.suit] = 1
        if max_in_suit >= 5:
            return True
        return False
    
    # @description - converts card_rank to an integer for straight comparisons
    # @param - card_rank   string 2-9 or T-A
    # @return - list of num_id. Needs to be a list because A can be high or low
    def conv_rank_to_int(self, card_rank):
        card_rank = str(card_rank)
        m = re.fullmatch('[2-9]', card_rank)
        if m != None: #2-9
            num_id = [int(card_rank)]
        else:
            if card_rank == 'T':
                num_id = [10]
            elif card_rank == 'J':
                num_id = [11]
            elif card_rank == 'Q':
                num_id = [12]
            elif card_rank == 'K':
                num_id = [13]
            elif card_rank == 'A':
                num_id = [1,14]
        return num_id

    # @description - will find straights, flushes, straight flushes, royal flushes
    # @param - player_num   finds the highest card type
    # @return - index of hand in HANDS
    def check_straights_flushes(self, player_num):
        player_cards = self.table_cards + self.player_hands[player_num]
        #1) store all values in a list 2) sort 3) increment values by one, if it successfully incremnets to next value
        # 5 times then it must be a straight 
        player_cards_as_int = []
        for card in player_cards:
            rank_ints = self.conv_rank_to_int(card.rank)
            for num in rank_ints:
                player_cards_as_int.append(num)
        player_cards_as_int.sort()

        max_in_a_row = 1
        for i in range(len(player_cards_as_int) - 1):
            if (player_cards_as_int[i] + 1) == player_cards_as_int[i+1]:
                max_in_a_row += 1
                if max_in_a_row == 5:
                    break
            else:
                max_in_a_row = 1
        if max_in_a_row == 5 and self.is_flush(player_num):
            r_flush_lst = [10, 11, 12, 13, 14]
            overlap = set(player_cards_as_int).intersection(r_flush_lst) #removes any items not in both lists
            r_flush_lst = set(r_flush_lst)

            if r_flush_lst == overlap: 
                return 9 #royal flush
            return 8 #straight flush
        else:
            if max_in_a_row == 5: #not a flush but a straight
                return 4 #straight
            elif self.is_flush(player_num):
                return 5 #flush'
            else:
                return 0 #neither straight nor flush
        

    # @description - determines a pair, 2 pair, 3 of kind, 4 of kind, and full house
    # @param - player_num  index of player being checked
    # @return - index of hand in HANDS
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
        
                    




    
    

