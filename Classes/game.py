import pygame

class Game:
    def __init__(self, win):
        self.win = win

    def update(self):
        pygame.display.update()