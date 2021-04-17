# Author: Mitch Reeves
# Date added: 3.31.2021

import pygame
from constants import SUITS, HEART, DIAMOND, CLUB, SPADE, BACK, CARD_HEIGHT, CARD_WIDTH, OFFSET

CARDW = 100
CARDH = 150
OUTLINEBUFF = 3
NUMBUFF = 10
DECKBUFF = 4

class Card:
    def __init__(self, card_num):
        self.rank = card_num % 13 # (0-12) 2 => 0 A => 12
        self.get_rank_string()
        self.suit = card_num % 4 
        self.str_suit = SUITS[card_num % 4] #club, diam, spade, heart
        self.card_num = card_num
        
        if(self.card_num % 4 == 0 ): # Assign suit picture
            self.suit_pic = CLUB
            self.color = (0,0,0)
        elif(self.card_num % 4 == 1):
            self.suit_pic = DIAMOND
            self.color = (255,0,0)
        elif(self.card_num % 4 == 2):
            self.suit_pic = SPADE
            self.color = (0,0,0)
        else:
            self.suit_pic = HEART
            self.color = (255,0,0)

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

    def draw(self, win, topX, topY, front):
        #win.fill((255,255,255)) ############GET RID OF THIS
        if(front == True):
            pygame.draw.rect(win, (0,0,0), (topX, topY, CARD_WIDTH, CARD_HEIGHT), 7,7)
            pygame.draw.rect(win, (255,255,255), (topX + OUTLINEBUFF, topY + OUTLINEBUFF, CARD_WIDTH - 2*OUTLINEBUFF, CARD_HEIGHT - 2*OUTLINEBUFF), 0, 3)
            win.blit(self.suit_pic, ((topX + CARD_WIDTH//2) - self.suit_pic.get_width()//2, (topY + CARD_HEIGHT//2) - self.suit_pic.get_height()//2))
            font = pygame.font.SysFont('Arial',25)
            text = font.render(self.str_rank, 1, self.color)
            win.blit(text, (topX + NUMBUFF, topY + NUMBUFF))
            win.blit(text, (topX + CARD_WIDTH - 2*NUMBUFF, topY + CARD_HEIGHT - 4*NUMBUFF))
        elif(front == False):
            win.blit(BACK, (topX,topY))

    def draw_deck(self, win):
        initial_x = 560 + 5 *(3) + OFFSET + 2* CARD_WIDTH
        initial_y = 365 + 15 // 2 - CARD_HEIGHT - 5
        win.blit(BACK, (initial_x,initial_y)) #I dont know where exactly to put the deck so im picking a random value
        win.blit(BACK, (initial_x + DECKBUFF,initial_y))
        win.blit(BACK, (initial_x + 2*DECKBUFF,initial_y))
        win.blit(BACK, (initial_x + 3*DECKBUFF,initial_y))
        win.blit(BACK, (initial_x + 4*DECKBUFF,initial_y))

    def __str__(self):
        return "{0}  {1}".format(self.str_rank, self.str_suit)

'''
class Card:
    def __init__(self, card_num):
        # '♣','♦','♠','♥'
        self.rank = card_num % 13  # (0-12) 2 => 0 A => 12
        self.get_rank_string()
        self.suit = card_num % 4
        self.str_suit = SUITS[card_num % 4]  # club, diam, spade, heart
        self.card_num = card_num
        self.font_reg = pygame.font.SysFont('Arial', SMALL_CARD_FONT_SIZE)
        self.font_big = pygame.font.SysFont('Arial', BIG_CARD_FONT_SIZE)

        if (self.card_num % 4 == 0):  # Assign suit picture
            self.suit_pic = '♣'
            self.color = (0, 0, 0)
        elif (self.card_num % 4 == 1):
            self.suit_pic = '♦'
            self.color = (255, 0, 0)
        elif (self.card_num % 4 == 2):
            self.suit_pic = '♠'
            self.color = (0, 0, 0)
        else:
            self.suit_pic = '♥'
            self.color = (255, 0, 0)

        self.rank_str = self.str_rank

    def get_rank_string(self):
        if 0 <= self.rank and self.rank <= 7:
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

    # def draw(self, win, topX, topY):
    #     win.fill((255,255,255)) ############GET RID OF THIS
    #     pygame.draw.rect(win, (0,0,0), (topX, topY, CARDW, CARDH), 7, 7)
    #     pygame.draw.rect(win, (255,255,255), (topX + OUTLINEBUFF, topY + OUTLINEBUFF, CARDW - 2*OUTLINEBUFF, CARDH - 2*OUTLINEBUFF), 3, 3)
    #     win.blit(self.suit_pic, ((topX + CARDW//2) - self.suit_pic.get_width()//2, (topY + CARDH//2) - self.suit_pic.get_height()//2))
    #     font = pygame.font.SysFont('Arial',25)
    #     text = font.render(self.rank_str, 1, self.color)
    #     win.blit(text, (topX + NUMBUFF, topY + NUMBUFF))
    #     win.blit(text, (topX + CARDW - 2*NUMBUFF, topY + CARDH - 4*NUMBUFF))

    def draw(self, win, topX, topY):
        #win.fill((255, 255, 255))  ############GET RID OF THIS
        pygame.draw.rect(win, WHITE, (topX, topY, CARD_WIDTH, CARD_HEIGHT))
        win.blit(self.font_reg.render(f'{self.suit_pic}', True, BLACK), (topX + 5, topY))
        win.blit(self.font_reg.render(f'{self.str_rank}', True, BLACK), (topX + 17, topY + 30))

    def draw_big(self, win, topX, topY):
        pygame.draw.rect(win, WHITE, (topX, topY, MAG_CARD_WIDTH, MAG_CARD_HEIGHT))
        win.blit(self.font_big.render(f'{self.suit_pic}', True, BLACK), (topX + 5, topY))
        win.blit(self.font_big.render(f'{self.str_rank}', True, BLACK), (topX + 40, topY + 70))

'''