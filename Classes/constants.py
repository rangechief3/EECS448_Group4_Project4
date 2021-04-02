import pygame

WIDTH = 800
HEIGHT = 500

#Poker values
START_STACK = 1000
SM_BLIND = 5
BIG_BLIND = 10

PLAYER_NAMES = ["Daniel Negreanu", "Bryn Kenney", "Phil Ivey", "Justin Bonomo",
                "Erik Seidel", "Dan Smith", "Stephen Chidwick", "Tom Dwan"]
SUITS = ['♣','♦','♠','♥']
HANDS = ['High Card', 'Pair', 'Two Pair', 'Three of a kind', 
        'Straight', 'Flush', 'Full House', 'Four of a kind',
        'Straight Flush', 'Royal Flush']

HEART = pygame.transform.scale(pygame.image.load('Pictures/Card_heart.png'), (36,28))
DIAMOND = pygame.transform.scale(pygame.image.load('Pictures/Card_diamond.png'), (36,28))
CLUB = pygame.transform.scale(pygame.image.load('Pictures/Card_club.png'), (36,28))
SPADE = pygame.transform.scale(pygame.image.load('Pictures/Card_spade.png'), (36,28))
BACK = pygame.transform.scale(pygame.image.load('Pictures/Card_back.jpg'), (100,150))