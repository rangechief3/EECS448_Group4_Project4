# Author: 
# Date added: 3.31.2021

from .constants import SUITS

class Card:
    def __init__(self, card_num):
        self.rank = card_num % 13 # (0-12) 2 => 0 A => 12
        self.get_rank_string()
        self.suit = card_num % 4 
        self.str_suit = SUITS[card_num % 4]
        self.card_num = card_num 

    def get_rank_string(self):
        if (0 <= self.rank and self.rank <= 7):
            new_rank = self.rank + 2
            self.str_rank = str(new_rank)
        else:
            if self.rank == 8:
                self.str_rank = 'T'
            if self.rank == 9:
                self.str_rank = 'J'
            if self.rank == 10:
                self.str_rank = 'Q'
            if self.rank == 11:
                self.str_rank = 'K'
            if self.rank == 12:
                self.str_rank = 'A'