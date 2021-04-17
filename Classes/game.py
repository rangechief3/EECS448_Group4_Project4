import pygame
from .data import Data
import time

class Game:
    def __init__(self, win):
        self.win = win
        self.data = Data(win)
        self.hand_num = 0

    def update(self):
        self.data.players_draw(0, False, None) #index of player to be drawn
        pygame.display.update()
        time.sleep(2)
     
    def gameCycle(self):
        self.data.deal()
        gamePhase = 0
        self.update() #should draw cards now
        gameInProgress = True
        while(gameInProgress):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            
            self.data.get_player_bets(gamePhase)  
            self.update() #should draw cards
            run_normally = self.data.get_hand_status()
            print(gamePhase, run_normally)
            if not run_normally:
                print("We are leaving the game call, hopefully BEFORE the next card is drawn")
                self.hand_num += 1
                return True
            if (gamePhase == 0):
                self.data.flop()

            elif(gamePhase == 1):
                self.data.turn()

            elif(gamePhase == 2):
                self.data.river()
            
            elif(gamePhase == 3):
                self.update()
                self.data.end_game()
                gameInProgress = False

            
            gamePhase += 1
        self.hand_num += 1
        return True

    def update_game_status(self):
        self.data.gameStatus = True
        
        

