import pygame
from .data import Data
import time

class Game:
    def __init__(self, win):
        self.win = win
        self.data = Data(win)

    def update(self):
        pygame.display.update()
        self.data.players_draw(0) #index of player to be drawn
        time.sleep(2)
     
    def gameCycle(self):
        self.data.deal()
        gamePhase = 0
        self.update() #should draw cards now
        gameInProgress = True
        while(gameInProgress):
            self.data.get_player_bets(gamePhase)  
            if (gamePhase == 0):
                self.data.flop()

            elif(gamePhase == 1):
                self.data.turn()

            elif(gamePhase == 2):
                self.data.river()
            
            elif(gamePhase == 3):
                self.data.end_game()
                gameInProgress = False
            
            self.update() #should draw cards
            gamePhase += 1

