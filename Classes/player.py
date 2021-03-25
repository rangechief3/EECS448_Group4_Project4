class Player:
    def __init__(self, win, player_name, player_num, start_amt):
        self.win = win
        self.player_name = player_name
        self.player_num = player_num
        self.stack = start_amt

    def receive_hand(self, hand):
        pass

    def receive_board_cards(self, cards): #list of cards. WILL be duplicates
        pass

    def bet(self, curr_bet):
        pass #return 0 for check, curr_bet for call, higher value for raise, -1 for fold
        #reduce player stack by bet amount then return it

    def blind(self, blind_amt): #check if the player has that much, if so, return that much 
        self.stack -= blind_amt #if less, return the max they have
        return blind_amt
