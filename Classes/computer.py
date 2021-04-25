from .constants import HANDS, BIG_BLIND
from .player import Player
import math
import random
import time

class Computer(Player):
    
    def update_stack(self, amt):
        amt = math.floor(min(self.stack, amt))
        self.stack -= amt
        return amt

    def takeATurn(self, curr_bet, prev_bet):
        time.sleep(0.4)
        amt_to_stay_in = curr_bet - prev_bet
        c1rank = self.hand[0].rank
        c2rank = self.hand[1].rank
        c1suit = self.hand[0].suit
        c2suit = self.hand[1].suit
        if len(self.board_cards) == 0: #preflop
            if ( not self.pre_flop_fold(curr_bet, prev_bet)): #not folding preflop
                if c1rank == c2rank: #pocket pair
                    if c1rank == 11 or c1rank == 12 or c1rank == 10 or c1rank == 9 or c1rank ==4 or c1rank == 5 or c1rank == 6 or c1rank == 7 or c1rank == 8:  #pocket queens, kings or aces
                        amt_to_go = self.stack

                        if(self.bluff()):
                            amt = self.update_stack(math.floor(self.stack / 4))
                            return amt
                        else:
                            self.active = -1
                            return -1
                    else:
                        amt = self.update_stack(amt_to_stay_in)
                        return amt 
                else: 
                    if c1rank > 10 and c2rank > 10: #2 high cards
                        if amt_to_stay_in < self.stack / 8:
                            amt = self.update_stack(amt_to_stay_in * 2)
                            return amt
                        else: 
                            self.active = False
                            return -1
                    else:
                        if (self.bluff()):  #bluff call
                            amt = self.update_stack(amt_to_stay_in)
                            return amt 
                        else:
                            self.active = False
                            return -1 #fold
            else: 
                self.active = False
                return -1
        else:
            if len(self.board_cards) == 3: #flop
                if (self.bluff()):
                    amt_to_go = min(self.stack, math.floor(amt_to_stay_in * 2.25))
                    amt = self.update_stack(amt_to_go)
                    return amt
                else:
                    if self.hand_num == 0:
                        if amt_to_stay_in > self.stack / 10:
                            self.active = False
                            return -1
                        else:
                            amt = self.update_stack(amt_to_stay_in)
                            return amt #check
                    if self.hand_num == 1:
                        if(self.bluff()):
                            amt = self.update_stack(amt_to_stay_in * 2)
                            return amt 
                        else: 
                            if amt_to_stay_in > 0:
                                self.active = False
                                amt = self.update_stack(amt_to_stay_in)
                                return amt
                            else:
                                return 0 
                    if self.hand_num == 2:
                        if(self.bluff()):
                            amt_to_go = self.stack
                            amt = self.update_stack(self.stack)
                            return amt
                        else:
                            if amt_to_stay_in > self.stack / 10:
                                amt = self.update_stack(self.stack / 10)
                                return amt
                            else: 
                                amt = self.update_stack(math.floor(amt_to_stay_in * 1.5))
                                return amt
                    if self.hand_num == 3:
                        if(self.bluff()):
                            amt = self.update_stack(self.stack / 10)
                            return amt
                        else:
                            if amt_to_stay_in > self.stack / 10:
                                amt = self.update_stack(amt_to_stay_in)
                                return amt 
                            else:
                                amt = self.update_stack(math.floor(amt_to_stay_in * 1.5))
                                return amt
                    if self.hand_num == 4:
                        if(self.bluff()):
                            amt = self.update_stack(self.stack / 10)
                            return amt
                        else:
                            if amt_to_stay_in > self.stack / 10:
                                amt = self.update_stack(amt_to_stay_in)
                                return amt
                            else:
                                return 0
                    if self.hand_num > 4:
                        amt = self.update_stack(amt_to_stay_in)
                        return amt
            
            if len(self.board_cards) == 4: #turn

                if(self.bluff()):
                            amt = self.update_stack(self.stack / 10)
                            return amt
                if self.hand_num == 0:
                    if amt_to_stay_in > self.stack / 5:
                        self.active = False
                        return -1
                    else:
                        amt = self.update_stack(amt_to_stay_in)
                        return amt
                if self.hand_num == 1:
                    if(self.bluff()):
                        amt = self.update_stack(amt_to_stay_in * 2)
                        return amt
                    else:
                        if amt_to_stay_in > self.stack / 10:
                            if random.random() > .7:
                                amt = self.update_stack(amt_to_stay_in)
                                return amt
                            else:
                                self.active = False
                                return -1
                        else:
                            amt = self.update_stack(amt_to_stay_in)
                            return amt
                if self.hand_num == 2:
                    if(self.bluff()):
                        amt = self.update_stack(amt_to_stay_in * 2)
                        return amt
                    else:
                        if amt_to_stay_in > 0:
                            amt = self.update_stack(self.stack / 10)
                            return amt
                        else:
                            return 0
                if self.hand_num == 3:
                    if(self.bluff()):
                        amt = self.update_stack(math.floor(amt_to_stay_in * 2.5))
                        return amt
                    else:
                        if amt_to_stay_in > self.stack / 10:
                            amt = self.update_stack(amt_to_stay_in )
                            return amt
                        else:
                            amt = self.update_stack(amt_to_stay_in)
                            return amt
                if self.hand_num == 4:
                    if(self.bluff()):
                        if amt_to_stay_in > 0:
                            amt = self.update_stack(self.stack / 10)
                            return amt
                        else:
                            return 0
                    else:
                        if amt_to_stay_in > 0:
                            amt = self.update_stack(amt_to_stay_in * 2)
                            return amt
                        else:
                            amt = self.update_stack(math.floor(amt_to_stay_in * 1.5))
                            return amt
                if self.hand_num == 5:
                    if(self.bluff()):
                        amt_to_go = self.stack
                        amt = self.update_stack(self.stack)
                        return amt
                    else:
                        if amt_to_stay_in > self.stack / 10:
                            amt = self.update_stack(amt_to_stay_in * 2)
                            return amt2
                        else:
                            amt = self.update_stack(amt_to_stay_in)
                            return amt
                if self.hand_num > 5:
                    if(self.bluff()):
                        amt_to_go = self.stack
                        amt = self.update_stack(self.stack)
                        return amt
                    else:
                        amt = self.update_stack(amt_to_stay_in)
                        return amt
            if len(self.board_cards) == 5:
                if self.hand_num == 0:
                    if(self.bluff()):
                        amt_to_go = self.stack
                        amt = self.update_stack(self.stack / 10)
                        return amt
                    else:
                        if amt_to_stay_in > 0:
                            self.active = False
                            return -1
                        else:
                            return 0

                if self.hand_num == 1:
                    if(bluff()):
                        amt = self.update_stack(amt_to_stay_in * 2)
                        return amt
                    else:
                        if amt_to_stay_in > self.stack / 10:
                            if random.random() > 0.6:
                                amt = self.update_stack(amt_to_stay_in)
                                return amt
                            else:
                                self.active = False
                                return -1
                        else:
                            amt = self.update_stack(amt_to_stay_in)
                            return amt
                if self.hand_num == 2: 
                    if(bluff()):
                        amt = self.update_stack(self.stack)
                        return amt
                    else:
                        if amt_to_stay_in > 0:
                            amt = self.update_stack(self.stack / 10 )
                            return amt
                        else:
                            return 0
                if self.hand_num == 3:
                    if(bluff()):
                        amt = self.update_stack(amt_to_stay_in * 2)
                        return amt
                    else:
                        if amt_to_stay_in > 0:
                            amt = self.update_stack(amt_to_stay_in)
                            return amt
                        else: 
                            return 0
                if self.hand_num == 4:
                    if(bluff()):
                        amt_to_go = self.stack
                        amt = self.update_stack(self.stack)
                        return amt
                    else:
                        if amt_to_stay_in > 0:
                            amt = self.update_stack(amt_to_stay_in)
                            return amt
                        else: 
                            amt = self.update_stack(amt_to_stay_in * 3)
                            return amt
                if self.hand_num == 5:
                    if(bluff()):
                        amt_to_go = self.stack
                        amt = self.update_stack(self.stack)
                        return amt
                    else:
                        if amt_to_stay_in > self.stack / 10: 
                            amt = self.update_stack(amt_to_stay_in * 3)
                            return amt
                        else:
                            amt = self.update_stack(amt_to_stay_in * 2)
                            return amt
                if self.hand_num > 5:
                    if(bluff()):
                        if amt_to_stay_in > self.stack / 10:
                            amt = self.update_stack(amt_to_stay_in)
                            return amt
                        else:
                            amt = self.update_stack(amt_to_stay_in)
                            return amt
                    else:
                        amt_to_go = self.stack
                        amt = self.update_stack(self.stack)
                        return amt
                        
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

            if c1rank == 7 and c2rank == 2:
                return False  #2 7 perma call
                
            if c2rank == 7 and c1rank == 2:
                return False


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
        if random.random() > 0.5: #Altered to make less folds
            return True
        else:
            return False
