# Very basic version of card class. Just used to test player.py

class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit

    def __str__(self):
        return "Card number: " + str(self.num) + " Card suit: " + str(self.suit)

    def draw(self):
        print(f"Drew card on board {self.num} {self.suit}")
