from .constants import HANDS
import random 
'''
        self.win = win
        self.player_name = player_name
        self.player_num = player_num
        self.stack = start_amt
        self.hand = []
        self.board_cards = []
        self.buttons = []
        self.hand_num = 0 #your hand + board cards
        self.high_card = 0
        
'''

class Computer(Player):
    # @return int value for the bet, must be greater than or equal to curr_bet or -1
    def takeATurn(self, curr_bet, prev_bet):
        if len(self.board_cards) == 0:
            if ( not self.pre_flop_fold(curr_bet, prev_bet)):
            if (!pre_flop_folding()) {

            }
            if pre_flop_folding() == False:
                stay in 
            else:
                fold
                if curr_bet == 0:
                    len(self.board_cards)

                else:

                    if self.hand_num > 5:
                        return self.stack
                    if curr_bet > SMALL_BLIND * 10 and self.hand_num < 2:
                        outcome = determineOutcome()
                        if outcome == 2:
                            multiplier = 2
                            if random.random() > 0.8:
                                mutiplier = 4
                            elif random.random > 0.5:
                                multiplier = 3
                            self.stack -= curr_bet * multiplier - prev_bet
                            return curr_bet * multiplier
            else:
                return -1
                

    def determineOutcome():
        cutoff = 0.5
        if self.hand_num > self.hand_num_board:
            cutoff += 0.1
            if len(self.board_cards) < 4):
                cutoff += 0.1
        ##add a few more comparisons that make sense
        if random.random() < cutoff: #0 - fold 1 - call 2 - raise
            return 2
        elif random.random() < .95:
            return 0
    
    def pre_flop_fold(self, curr_bet, prev_bet):
        #return True if folding 
        #return False if staying in
        
        #use self.hand to determine hand strength
        amt_to_stay_in = curr_bet - prev_bet

        if amt_to_stay_in <= SMALL_BLIND:
            return False #staying in 
        else:
            self.hand = [Card1, Card2]
            c1rank = self.hand[0].rank
            c2rank = self.hand[1].rank
            c1suit = self.hand[0].suit
            c2suit = self.hand[1].suit
            Card = rank, suit
            card.rank = #0-12
            card.suit = #0-3
            if self.hand[0].rank == self.hand[1].rank: #pocket pair
                return False
            if self.hand[0].suit == self.hand[1].suit: #suited
                if c1rank > 6 or c2rank > 6:
                    return False
                else:
                    return True


