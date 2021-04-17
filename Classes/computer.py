from .constants import HANDS, BIG_BLIND
from .player import Player
import random
import time

class Computer(Player):
    
    def takeATurn(self, curr_bet, prev_bet):
        amt_to_stay_in = curr_bet - prev_bet
        c1rank = self.hand[0].rank
        c2rank = self.hand[1].rank
        c1suit = self.hand[0].suit
        c2suit = self.hand[1].suit
        '''
        if len(self.board_cards) == 0: #preflop
            if ( not self.pre_flop_fold(curr_bet, prev_bet)): #not folding preflop
                if c1rank == c2rank: #pocket pair
                    if c1rank == 11 or c1rank == 12 or c1rank == 10:  #pocket queens, kings or aces
                        return self.stack/2
                    else:
                        return curr_bet
                else: 
                    if c1rank > 10 and c2rank > 10: #2 high cards
                        if amt_to_stay_in < self.stack / 8:
                            return amt_to_stay_in
                        else: 
                            return -1
                    else:
                        if (self.bluff()):  #bluff call
                            return amt_to_stay_in
                        else:
                            return -1
            else: 
                return -1
        else: 
            return amt_to_stay_in
        '''
        time.sleep(0.5)
        if random.random() < 0.5:
            return self.bet(curr_bet, prev_bet)
        else:
            return -1
            
                



    def pre_flop_fold(self, curr_bet, prev_bet):
        #returns true if folding
        #false if elsewise

        amt_to_stay_in = curr_bet - prev_bet

        if amt_to_stay_in <= BIG_BLIND:
            return False
        else:
            c1rank = self.hand[0].rank
            c2rank = self.hand[1].rank
            c1suit = self.hand[0].suit
            c2suit = self.hand[1].suit

            if c1rank > 10 and c2rank > 10: #2 high cards
                return False

            if c1rank == c2rank: #pocket pair
                return False
            
            if c2suit == c2suit: #suited
                if c1rank > 8 or c2rank > 8:
                    return False
                else:
                    return True
    '''
    def determineOutcome():
        cutoff = 0.5
        if self.hand_num > self.hand_num_board:
            cutoff = cutoff + 0.1
            if len(self.board_cards) < 4:
                cutoff = cutoff + 0.1
    '''

    def bluff(self):
        if random.random() > 0.8:
            return True
        else:
            return False