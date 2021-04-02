import pygame
from .data import Data

class Game:
    def __init__(self, win):
        self.win = win
        self.data = Data(win)

    def update(self):
        pygame.display.update()
        self.data.players_draw()
    
    def gameCycle(self):
        self.data.deal()
        gamePhase = 0
        self.update()
        while(gameInProgress == True)
            self.data.get_player_bets(gamePhase)  
            if (gamePhase == 0):
            
                self.data.flop()

            elif(gamePhase == 1):
                self.data.turn()

            elif(gamePhase == 2):
    
                self.data.river()
            
            elif(gamePhase == 3):

                self.data.end_game(self)
                gameInProgress = False
            
            self.update()
            
            gamePhase += 1

