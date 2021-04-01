import pygame
from .data import Data

class Game:
    def __init__(self, win):
        self.win = win
        self.data = Data(win)

    def update(self):
        pygame.display.update()
    def gameCycle(self):
        playerArray = self.updatePlayers();
        self.deal();
        gamePhase = 0
        self.update();
        while(gameInProgress == True)
        {
            Data.get_player_bets(gamePhase);  

            if (gamePhase == 0)
            {
                self.data.flop();
                self.update();
            }
            else if(gamePhase == 1)
            {
                self.data.turn();
                self.update();
            }
            else if(gamePhase == 2)
            {
                self.data.river();
                self.update();
            }
            else if(gamePhase == 3)
            {
                self.data.end_game(self);
                gameInProgress = False;
                self.update();
                self.data.reset();
            }
            gamePhase++
        }

    def updatePlayers():
        #check if any players are wating in queue
        #check if any players want to leave
        #return player array
