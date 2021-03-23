# Auther: Jake Wagner
# Date Started:

import poker
from .constants import BIG_BLIND

class Data:
    def __init__(self, win):
        self.win = win
        self.deck = list(Card)
        self.curr_bet = BIG_BLIND
        self.pots = []
        self.table_cards = []
        self.player_hands = []
        self.dealer = 0
        self.init_players()