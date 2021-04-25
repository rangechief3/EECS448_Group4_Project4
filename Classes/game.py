import pygame
from .data import Data
import time
from . constants import *

pygame.font.init()

class Game:
    def __init__(self, win, Test):
        self.win = win
        self.data = Data(win, Test)
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
                pygame.display.update()
                if self.data.players[0].player_name != "Player One":
                    font = pygame.font.SysFont('Arial',60)
                    self.win.fill((0, 0, 0))                      
                    text = font.render("YOU LOST!!!", 1, (250, 0, 0))
                    self.win.blit(text,(WIDTH//2 - text.get_width() //2, HEIGHT//2 - text.get_height() //2))
                    pygame.display.update()
                    print("you lost, exiting game")
                    time.sleep(3)
                    return False
                gameInProgress = False

            
            gamePhase += 1
        self.hand_num += 1
        return True

    def update_game_status(self):
        self.data.gameStatus = True


    def testCycle(self):
        print("\n(1)testing if a pair beat a highcard: ")
        if self.data.pairBeatsHighCard():
            print("passed \n")
        else:
            print("failed \n")
        print("(2)testing if a 2 players have the same hand: ")
        if self.data.samehandtest():
            print("passed \n")
        else:
            print("failed \n")
        print("(3)testing if: split pots work")
        if self.data.splitpottest():
            print("passed \n")
        else:
            print("failed \n")
        print("(4)testing if: game can pick best hand when given pair and straight")
        if self.data.determinebesthandtest():
            print("passed \n")
        else:
            print("failed \n")
        print("(5)testing if: game can determine three of a kind correctly")
        if self.data.testthreeofakind():
            print("passed \n")
        else:
            print("failed \n")
        print("(6)testing if: game can determine a flush")
        if self.data.testflush():
            print("passed \n")
        else:
            print("failed \n")
        print("(7)testing if: Dealing gives the player 2 new cards")
        if self.data.testdealing():
            print("passed \n")
        else:
            print("failed \n")
        print("(8)testing if: reset correctly resets")
        if self.data.testreset():
            print("passed \n")
        else:
            print("failed \n")
           
        self.data.players[0].run_test()
        

