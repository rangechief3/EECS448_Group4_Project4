class Player:
    def __init__(self, win, player_name, player_num, start_amt):
        self.win = win
        self.player_name = player_name
        self.player_num = player_num
        self.start_amt = start_amt

    def receive_hand(self, hand):
        pass

    def receive_board_cards(self, cards): #list of cards. WILL be duplicates
        pass
