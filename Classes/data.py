# Auther: Jake Wagner
# Date Started: 3.24.2021
# Date branch made: 3.31.2021

import random
import time
from .card import Card
from .constants import SM_BLIND, BIG_BLIND, PLAYER_NAMES, USER_NAMES, START_STACK, HANDS, SUITS
from .player import Player
from .computer import Computer

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
        self.pot = 0
        self.table_cards = []
        self.player_prev_bets = []
        self.player_hands = []
        self.player_active = []
        self.dealer = 0
        self.gameStatus = True
        self.playerContributions = []
        self.init_players(8)
                
        
    # @description - draws the relevant player board
    # @param - player_num    index of a player
    # @return - None
    def players_draw(self, player_num, front, curr_player):
        other_players = []
        for player in self.players:
            if player.player_num != player_num:
                other_players.append(player)
        self.players[player_num].draw(other_players, front, curr_player)

    # @description - if the hand ended prematurely it returns false
    # @param - None
    # @return - False if the hand ended prematurely
    def get_hand_status(self):
        return self.gameStatus

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
                blind = self.players[self.dealer - 1].blind(SM_BLIND)
                self.player_prev_bets[self.dealer - 1] = blind #if someone raises they would have to call <bet> - <prevbet>
                print(self.players[self.dealer - 1].player_name + " put in " + str(blind) + " as small blind!")
                self.add_to_pot(self.dealer - 1, blind, SM_BLIND, bet_round) #value may not be equal to blind if player has less
                blind = self.players[self.dealer - 2].blind(BIG_BLIND)
                self.player_prev_bets[self.dealer - 2] = blind
                print(self.players[self.dealer - 2].player_name + " put in " + str(blind) + " as big blind!")
                self.add_to_pot(self.dealer - 2, blind, BIG_BLIND, bet_round)
                curr_bet = BIG_BLIND
                curr_player = self.dealer - 3 #Under the gun
                self.players_draw(0, False, curr_player) ###will be need to be changed to be more general
            else:
                curr_bet = 0
                curr_player = self.dealer - 1 #small blind 
            while not done_betting:  #current player and current bet are set
                if curr_player <= -len(self.players):
                    curr_player = 0
                num_active = 0
                for item in self.player_active:
                    if item:
                        num_active += 1
                if num_active >= 2:
                    if self.player_active[curr_player]:
                        self.players_draw(0, False, curr_player) 
                        bet = self.players[curr_player].takeATurn(curr_bet, self.player_prev_bets[curr_player])
                        self.player_prev_bets[curr_player] = bet
                        if bet != -1: # a fold
                            print(self.players[curr_player].player_name + " bet " + str(bet) + "!")
                            self.add_to_pot(curr_player, bet, curr_bet, bet_round)
                            if bet > curr_bet:
                                counter = 0
                                curr_bet = bet
                        else:
                            self.player_active[curr_player] = False
                            self.players[curr_player].playing = False
                    counter += 1
                    if counter == len(self.players): #if it has gone to all players without a raise
                        done_betting = True
                    curr_player -= 1
                else:
                    print("We should be ending the game early")
                    self.gameStatus = False
                    self.end_game()
                    done_betting = True
            for i in range(len(self.player_prev_bets)): #resets player previous bets to zero at the concusion of the round
                self.player_prev_bets[i] = 0

    # @description - resets the data that changes with each hand
    # @param - player_num   Int for player index   
    # @param - amt   Int for amount bet
    # @param - curr_bet Int for amount of current bet
    # @param - bet_round Int for number of betting round (0-3)
    # @return - None
    def add_to_pot(self, player_num, amt, curr_bet, bet_round):
        self.pot += amt
        self.playerContributions[player_num] += amt
        ##self.players[player_num].recievePotValue(self.pot)
    # @description - resets the data that changes with each hand
    # @param - None
    # @return - None
    def reset(self):
        self.deck = list(Card(i) for i in range(52))
        random.shuffle(self.deck)
        for player in self.players:
            player.reset()
        self.dealer -= 1
        if self.dealer < -len(self.players):
            self.dealer = 0
        self.curr_bet = 0
        self.pot = 0
        self.table_cards = []
        self.player_hands = []
        self.player_active = []
        for i in range(len(self.players)):
            self.player_active.append(True)
            self.playerContributions[i] = 0


    # @description - Creates Player objects 
    # @param - num_players   determines how many Player objects will be created
    # @return - None
    def init_players(self, num_players):
        self.players.append(Player(self.win, USER_NAMES[0], 0, START_STACK))
        self.player_active.append(True)
        self.player_prev_bets.append(0)
        self.playerContributions.append(0)
        for i in range(1,num_players):
            self.players.append(Computer(self.win, PLAYER_NAMES[i], i, START_STACK))
            self.player_active.append(True)
            self.player_prev_bets.append(0)
            self.playerContributions.append(0)
            #print(self.players[i].player_name)

        
        '''
        for i in range(num_players):
            self.players.append(Player(self.win, PLAYER_NAMES[i], i, START_STACK))
            self.player_active.append(True)
            self.player_prev_bets.append(0)
        '''


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
            player.receive_board_cards(new_cards, "flop")

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
            player.receive_board_cards(new_card, "turn")

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
            player.receive_board_cards(new_card, "river")

    # @description - awards winning player earnings, resets data
    # @param - None
    # @return - None
    def end_game(self):
        self.award_winnings()
        self.players_draw(0, True, None)
        time.sleep(5)
        ##if player has no money, remove player and replace them
        self.reset()
    
    # @description - gives winner earnings
    # @param - None
    # @return - None
    def award_winnings(self):
        ##player_amt_in = [x,y, z ...]
        playerActiveIndex = []
        for i, active in enumerate(self.player_active):
            if active: 
                playerActiveIndex.append(i)
        ## for i in range(len(self.player_active)): length is a int. for loops in python loop over 'objects' so a range makes it 0-(len-1)
        ##      if self.player_Active[i]:
        ##keep track of if a player has put in less than the other people. Then create a list of all players that have put in at least that much
        # eligiblepot = check all players + that amount to this pot if they put in more than that
        # winner, hand = self.current_winner(list of players eligible for this pot)
        ## minimum_amt = -1
        ## for i in player_active:
        #      if minimum_amt = -1:
        #           minimum_amt = self.player_amt_in[i] //assign to the first amount that a player has put in 
        #       else:
        #          find the lowest minimum 
        # for i, amt in enumerate(self.player_amt_in):
        #      if self.player_active[i]:
        #           elibiglepot += minimum_amt
        #           self.player_amt_in[i] -= minumum_amt
        #       else:
        #           eligibilepot += self.player_amt_in[i] 
        #           self.player_amt_in[i] = 0
        #    
        maxbet = []
        for i in playerActiveIndex:
            betincluded = False
            for bet in maxbet:
                if self.playerContributions[i] == bet:    
                    betincluded = True
            if betincluded == False:
                maxbet.append(self.playerContributions[i])
        maxbet.sort()

        accountedForbet = 0
        adjustedpot = 0
        for bet in maxbet:
            for i in range(len(self.players)):
                if self.playerContributions[i] >= bet:
                    adjustedpot += bet - accountedForbet
                elif self.playerContributions[i] <bet:
                    adjustedpot += self.playerContributions[i] - accountedForbet
            eligiblePlayers = []
            for i in playerActiveIndex:
                if self.playerContributions[i] >= bet:
                    eligiblePlayers.append(i)
            winner, hand = self.current_winner(eligiblePlayers)
            for victor in winner:
                self.players[victor].receive_winnings(adjustedpot//(len(winner)))
            accountedForbet += bet
            adjustedpot = 0

    # @description - determines the hands that each player has, and determines the winner
    # @param - None
    # @return - will return the winning player(s)
    def current_winner(self, activePlayers):
        tiewithwinner = False
        tie = False
        playerWithBestHand = []
        firstactiveplayer = True
        for i in activePlayers:
            hand_num = max(self.check_duplicates(i), self.check_straights_flushes(i))
            if firstactiveplayer == True:
                firstactiveplayer = False
                bestHand = hand_num
                playerWithBestHand.append(i)
            elif hand_num > bestHand:
                tiewithwinner = False   
                bestHand = hand_num
                playerWithBestHand = []
                playerWithBestHand.append(i)
            elif hand_num == bestHand:
                challenger = self.recieveCurrHand(i) 
                currentWinner = self.recieveCurrHand(playerWithBestHand[0])
                for j in range(5):
                    print (str(j) + " " + str(challenger[j]) + " " + str(currentWinner[j])) 
                    if challenger[j] > currentWinner[j]:
                        tiewithwinner = False
                        tie = False 
                        playerWithBestHand = []
                        playerWithBestHand.append(i)
                        break
                    elif challenger[j] < currentWinner[j]:
                        tiewithwinner = False
                        tie = False
                        break
                    elif challenger [j] == currentWinner[j]:
                        tie = True
                if tie:
                    playerWithBestHand.append(i)
                    tiewithwinner = True
                    tie = False

        if tiewithwinner == False:
            return playerWithBestHand, bestHand[0]
        elif tiewithwinner == True:
            print("there were two winners")
            return playerWithBestHand, bestHand[0]
                
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
        
             
    def getPlayerHand(self, player_num):
        hand_num = max(self.check_duplicates(player_num), self.check_straights_flushes(player_num))
        return hand_num

    def recieveCurrHand(self, player_num):
        hand_num = self.getPlayerHand(player_num)
        hand_num = hand_num[0]
        player_cards = self.table_cards + self.player_hands[player_num]
        player_cards_as_int = []


        if hand_num == 5: #flush
            suits = {}
            hand = []
            max_in_suit = 0
            for card in player_cards:
                if card.suit in suits:
                 suits[card.suit] = suits[card.suit] + 1
                 max_in_suit = max(max_in_suit, suits[card.suit])
            for card in player_cards:
                if card.suit == max_in_suit:
                    hand.append(card)
            player_cards = hand



        for card in player_cards:
            player_cards_as_int.append(card.rank)
        player_cards_as_int.sort(reverse = True)

        if hand_num == 0: #highcard
            return player_cards_as_int
        elif hand_num == 1: #pair and 3 distinct cards
            prev = None
            for num in player_cards_as_int:
                if num == prev:
                    pair = num
                    break
                prev = num
            hand = [pair,pair]
            for num in player_cards_as_int:
                if num != pair:
                    hand.append(num)          
            return hand
        elif hand_num == 2: #two pair 1 high card
            prev = None
            pair = None
            pair2 = None
            hand = []
            for num in player_cards_as_int:
                if num == prev and pair == None:
                    pair = num
                    hand = [pair, pair]
                elif num == prev and pair2 == None:
                    pair2 = num
                    hand.append(pair2)
                    hand.append(pair2)
                prev = num
            for num in player_cards_as_int:
                if num != pair or num != pair2:
                    hand.append(num)

            return hand
        elif hand_num == 3: #three of a kind and 2 distinct cards
            prev = None
            for num in player_cards_as_int:
                if num == prev:
                    threeofakind = num
                    break
                prev = num
            hand = [threeofakind,threeofakind,threeofakind]
            for num in player_cards_as_int:
                if num != threeofakind:
                    hand.append(num)          
            return hand
        elif hand_num == 4: #straight no high card
            prev = None
            prev2 = None
            for num in player_cards_as_int:
                if num+1 == prev and num+2 == prev2:
                    straightHighcard = prev2
                    break
                prev2 = prev
                prev = num
            hand = [straightHighcard, straightHighcard-1, straightHighcard-2, straightHighcard-3, straightHighcard-4]
            return hand
        elif hand_num == 5: #flush
            return player_cards_as_int
        elif hand_num == 6: #full house no highcard
            prev = None
            prev2 = None
            for num in player_cards_as_int:
                if num == prev and num == prev2:
                    threeofakind = num
                prev2 = prev
                prev = num
            prev = None
            for num in player_cards_as_int:
                if num == prev and num != threeofakind:
                    pair = num
                prev = num
            hand = [threeofakind,threeofakind,threeofakind,pair,pair]
            return hand
        elif hand_num == 7: #four of a kind 1 high card
            prev = None
            for num in player_cards_as_int:
                if num == prev:
                    fourofakind = num
                    break
                prev = num
            hand = [fourofakind,fourofakind,fourofakind,fourofakind]
            for num in player_cards_as_int:
                if num != fourofakind:
                    hand.append(num)          
            return hand
        elif hand_num == 8: #straight flush no high cards
            prev = None
            prev2 = None
            for num in player_cards_as_int:
                if num+1 == prev and num+2 == prev2:
                    straightHighcard = prev2
                    break
                prev2 = prev
                prev = num
            hand = [straightHighcard, straightHighcard-1, straightHighcard-2, straightHighcard-3, straightHighcard-4]
            return hand
        elif hand_num == 9: #royal flush no high cards
            return player_cards_as_int
    def playAgain(self):
        return True

    
    

