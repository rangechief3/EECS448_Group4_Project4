# Auther: Jake Wagner
# Date Started: 3.24.2021
# Date branch made: 3.31.2021

import random
from .card import Card
from .constants import SM_BLIND, BIG_BLIND, PLAYER_NAMES, START_STACK, HANDS, SUITS
from .player import Player
import time

###TODO
# award_winners()
# pot management
# issue with high cards/determining winner for ALL cards not just the most important
# calculating hand each turn and then sending to player. important for 
class Data:

    #m = re.fullmatch('([2-9]|[ATJQK])[♣♦♠♥]', str(card))
    # @description - SETS the game data, initializing the player classes
    # @param - win    pygame WINDOW passed to players for printing purposes
    # @return - None
    def __init__(self, win):
        self.win = win
        self.deck = list(Card(i) for i in range(52))
        random.shuffle(self.deck)
        self.players = []
        self.pots = []
        self.table_cards = []
        self.player_prev_bets = []
        self.player_hands = []
        self.player_active = []
        self.dealer = 0
        self.init_players(8)
        '''
        self.deal()
        self.get_player_bets(0)
        self.flop()
        self.get_player_bets(1)
        self.turn()
        self.get_player_bets(2)
        self.river()
        self.get_player_bets(3)
        winner, hand, high_card = self.current_winner()
        print(self.players[winner].player_name + " WON with a " + HANDS[hand] + " High Card: " + str(high_card) +  "!\n")
        '''

    # @description - will draw the proper player's board
    # @param - None
    # @return - None
    def players_draw(self): #
        pass

    # @description - gets the player bet for each player, keeping track of pots
    # @param - bet_round    Int for betting round 0 = pre-flop, 1 = after flop, 3 = after river
    # @return - True  if a player takes down the pot  False  if two players remain
    def get_player_bets(self, bet_round):
        # 1) get player_stacks(for keeping track of pots) 2) will take blinds, then go around for bets
        # 3) determine who folds, updating self.player_active 4) if it goes around to original better w/o raise
        # end betting
            player_stacks = []
            for player in self.players:
                player_stacks.append(player.stack)
                
            done_betting = False
            counter = 0
            if bet_round == 0:
                blind = self.players[self.dealer + 1].blind(SM_BLIND)
                self.player_prev_bets[self.dealer + 1] = blind #if someone raises they would have to call <bet> - <prevbet>
                print(self.players[self.dealer + 1].player_name + " put in " + str(blind) + " as small blind!")
                self.add_to_pot(self.dealer + 1, blind, SM_BLIND, bet_round) #value may not be equal to blind if player has less
                blind = self.players[self.dealer + 2].blind(BIG_BLIND)
                self.player_prev_bets[self.dealer + 2] = blind
                print(self.players[self.dealer + 2].player_name + " put in " + str(blind) + " as big blind!")
                self.add_to_pot(self.dealer + 2, blind, BIG_BLIND, bet_round)
                curr_bet = BIG_BLIND
                curr_player = self.dealer + 3 #Under the gun
            else:
                curr_bet = 0
                curr_player = self.dealer + 1 #small blind 
            while not done_betting:  #current player and current bet are set
                if curr_player >= len(self.players):
                    curr_player = 0
                if self.player_active[curr_player]:
                    bet = self.players[curr_player].bet(curr_bet, self.player_prev_bets[curr_player]) #WILL BECOME take_a_turn()
                    self.player_prev_bets[curr_player] = bet
                    if bet != -1: # a fold
                        print(self.players[curr_player].player_name + " bet " + str(bet) + "!")
                        self.add_to_pot(curr_player, bet, curr_bet, bet_round)
                        if bet > curr_bet:
                            counter = 0
                            curr_bet = bet
                    else:
                        self.player_active[curr_player] = False
                counter += 1
                if counter == len(self.players): #if it has gone to all players without a raise
                    done_betting = True
                curr_player += 1
            for i in range(len(self.player_prev_bets)): #resets player previous bets to zero at the concusion of the round
                self.player_prev_bets[i] = 0
            print(self.pots)
            
    # @description - resets the data that changes with each hand
    # @param - player_num   Int for player index   
    # @param - amt   Int for amount bet
    # @param - curr_bet Int for amount of current bet
    # @param - bet_round Int for number of betting round (0-3)
    # @return - None
    def add_to_pot(self, player_num, amt, curr_bet, bet_round):
        #CASES
        #  -no pot
        #  -create side pot
        #  -add to pot
        #TESTING NO SIDE POTS
        if len(self.pots) == 0:
            pot_list = [amt, bet_round, curr_bet, [player_num]] #[total, betting round, current bet, [player1 ... playerk]]
            self.pots.append(pot_list)
        else:
            for pot in self.pots:
                if bet_round > pot[1]:
                    pot[1] = bet_round
                    curr_bet = 0
                if amt > pot[2]:
                    pot[2] = amt
                if player_num not in pot[3]:
                    pot[3].append(player_num)
                pot[0] += amt

    # @description - resets the data that changes with each hand
    # @param - None
    # @return - None
    def reset(self):
        self.deck = list(Card(i) for i in range(52))
        random.shuffle(self.deck)
        self.curr_bet = 0
        self.pots = []
        self.table_cards = []
        self.player_hands = []
        time.sleep(3)

    # @description - Creates Player objects 
    # @param - num_players   determines how many Player objects will be created
    # @return - None
    def init_players(self, num_players):
        for i in range(num_players):
            self.players.append(Player(self.win, PLAYER_NAMES[i], i, START_STACK))
            self.player_active.append(True)
            self.player_prev_bets.append(0)
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
            print(self.players[i].player_name)
            for j in range(2):
                print(self.player_hands[i][j])

    # @description - draws three cards for the board, sending the data to players and storing in self.table_cards
    # @param - None
    # @return - None
    def flop(self):
        self.deck.pop() #burn one card before dealing
        new_cards = []
        print("FLOP!")
        for i in range(3):
            new_cards.append(self.deck.pop())
            print(new_cards[i].str_rank, new_cards[i].str_suit)
        self.table_cards.extend(new_cards)
        
        for player in self.players:
            player.receive_board_cards(new_cards)

    # @description - draws one card(the fourth on the board), and updates the data structures dependent on it
    # @param - None
    # @return - None
    def turn(self):
        self.deck.pop() #burn one card before_dealing
        new_card = []
        new_card.append(self.deck.pop())
        self.table_cards.extend(new_card)
        print("TURN!")
        for card in self.table_cards:
            print(card.str_rank, card.str_suit)

        for player in self.players:
            player.receive_board_cards(new_card)

    # @description - draws one card(the fifth on the board), and updates the data structures dependent on it
    # @param - None
    # @return - None
    def river(self):
        self.deck.pop() #burn one card before_dealing
        new_card = []
        new_card.append(self.deck.pop())
        self.table_cards.extend(new_card)
        print("RIVER")
        for card in self.table_cards:
            print(card.str_rank, card.str_suit)

        for player in self.players:
            player.receive_board_cards(new_card)

    # @description - awards winning player earnings, resets data
    # @param - None
    # @return - None
    def end_hand(self):
        winner, hand, high_card = self.current_winner()
        print(self.players[winner].player_name + " WON with a " + HANDS[hand] + " High Card: " + str(high_card) +  "!\n")
        self.award_winnings(winner)
        self.reset()

    # @description - gives winning player(s) moneey
    # @param - winner index of player that wwon
    # @return - None
    def award_winnings(self, winner):
        ###fix  it to account for differnt pots
        ###bur assume for now only one pot
        #pot = [total, betting round, current bet, player1 ... playerk]
        self.players[winner].receive_winnings(self.pots[0][0])

    # @description - determines the hands that each player has, and determines the winner
    # @param - None
    # @return - will return the winning player(s)
    def current_winner(self):
        best_hand = 0
        best_high_card = 0
        player_winner = 0
        high_card_tiebreaker = 0
        highest_duplicate_hand = 0
        highest_duplicate_card = 0
        highest_specials_hand = 0
        highest_specials_card = 0

        for i in range(len(self.players)):
            highest_duplicate_hand, highest_duplicate_card = self.check_duplicates(i)
            highest_specials_hand, highest_duplicate_card = self.check_straights_flushes(i)
            temp_hand_num = max(highest_duplicate_hand, highest_specials_hand)
            
            if highest_duplicate_hand > highest_specials_card:
                temp_high_card = highest_duplicate_card
            else:
                temp_high_card = highest_specials_card

            if temp_hand_num == best_hand: #i.e. both have a two pair
                if temp_high_card > best_high_card:
                    player_winner = i
            elif temp_hand_num > best_hand:
                player_winner = i
            #update the best hand and high cards    
            best_hand = max(best_hand, temp_hand_num)
            best_high_card = max(best_high_card, temp_high_card)
            print(self.players[i].player_name + " has a " + HANDS[temp_hand_num])
            player_info = []
            for card in self.player_hands[i]:
                player_info.append([card.str_rank + str(card.rank) + card.str_suit])
            for card in self.table_cards:
                player_info.append([card.str_rank + str(card.rank) + card.str_suit])
            print(player_info)
        return player_winner, best_hand, best_high_card

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
    

    # @description - will find straights, flushes, straight flushes, royal flushes
    # @param - player_num   finds the highest card type
    # @return - index of hand in HANDS
    def check_straights_flushes(self, player_num):
        player_cards_temp = self.table_cards + self.player_hands[player_num]
        #1) store all values in a list 2) sort 3) increment values by one, if it successfully incremnets to next value
        # 5 times then it must be a straight
        player_cards = []
        for card in player_cards_temp:
            player_cards.append(card.rank)

        highest_card = 0
        player_cards.sort()
        max_in_a_row = 1
        for i in range(len(player_cards) - 1):
            if (player_cards[i] + 1) == player_cards[i+1]:
                max_in_a_row += 1
                if max_in_a_row == 5:
                    highest_card == player_cards[i+1]
                    break
            else:
                max_in_a_row = 1
        if max_in_a_row == 5 and self.is_flush(player_num):
            r_flush_lst = [10, 11, 12, 13, 14]
            overlap = set(player_cards).intersection(r_flush_lst) #removes any items not in both lists
            r_flush_lst = set(r_flush_lst)

            if r_flush_lst == overlap: 
                
                return 9, highest_card #royal flush
            return 8, highest_card #straight flush
        else:
            if max_in_a_row == 5: #not a flush but a straight
                return 4, highest_card #straight
            elif self.is_flush(player_num):
                for card in player_cards:
                    highest_card =max(highest_card, card)       
                return 5, highest_card #flush'
            else:
                for card in player_cards:
                    highest_card =max(highest_card, card)
                return 0, highest_card #neither straight nor flush
        
    # @description - determines a pair, 2 pair, 3 of kind, 4 of kind, and full house
    # @param - player_num  index of player being checked
    # @return - index of hand in HANDS
    def check_duplicates(self, player_num): #will determine pairs, two pairs, three of a kind, four of a kind, full house
        player_cards = self.table_cards + self.player_hands[player_num]
        ranks = {} #dict with the number of a card as the key, points to the number of those cards
        max_of_a_kind = 1
        highest_card = 0
        pairs = 0
        for card in player_cards:
            if card.rank in ranks:
                if ranks[card.rank] == 1: #if this card has NOT been paired
                    pairs += 1
                ranks[card.rank] = ranks[card.rank] + 1 #denotes number of that kind
                if ranks[card.rank] >= max_of_a_kind:
                    highest_card = max(highest_card, card.rank)
                max_of_a_kind = max(max_of_a_kind, ranks[card.rank])
            else:
                ranks[card.rank] = 1
        if max_of_a_kind == 4:
            return 7, highest_card #four of a kind
        elif max_of_a_kind == 3:
            if pairs >= 2:
                return 6, highest_card #full house
            return 3, highest_card #three of a kind
        elif pairs >= 2:
            return 2, highest_card #two pairs
        elif pairs == 1:
            return 1, highest_card #one pair
        else:
            for card in player_cards:
                highest_card = max(highest_card, card.rank)
            return 0, highest_card #did not find anything
        
             




    
    

