import pygame
from .data import Data

class Game:
    def __init__(self, win):
        self.win = win
        self.data = Data(win)

    def update(self):
        pygame.display.update()