# Author: Jake Wagner
# Date Started: 3/22/2021

import pygame
import random
import time
from Classes.constants import WIDTH, HEIGHT, PLAYER_NAMES, BOARD_COLOR, BACKGROUND_COLOR, BROWN, YELLOW
from Classes.game import Game
from Classes.menuButton import MenuButton
from Classes.backgroundObj import backgroundObject
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texas Hold 'em")
pygame.init()

PAD_LEFT = WIDTH//6 #margin left and right
PAD_TOP = HEIGHT//3 #margin top and bot
BTN_NUM = 5
SPACE = 15
BTN_HEIGHT = PAD_TOP
BTN_WIDTH = ((WIDTH - PAD_LEFT * 2) - ((BTN_NUM-1)*SPACE))/ BTN_NUM
buttons = []
background_objects = []

# @pre - None
# @param - None
# @description - Runs game loop, using the Game class to direct all of the other classes
def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    while running:
        running = game.gameCycle()
        game.update_game_status()
    pygame.quit()

def init_buttons():
    buttons.append(MenuButton(PAD_LEFT, PAD_TOP, BTN_WIDTH, BTN_HEIGHT, (255, 0, 0), 'red', "Start Game"))
    buttons.append(MenuButton(PAD_LEFT + BTN_WIDTH + SPACE, PAD_TOP, BTN_WIDTH, BTN_HEIGHT, (0, 0, 0), 'black', "Leave Game"))
    buttons.append(MenuButton(PAD_LEFT + BTN_WIDTH*2 + SPACE*2, PAD_TOP, BTN_WIDTH, BTN_HEIGHT, (0, 0, 0), 'red', "A"))
    buttons.append(MenuButton(PAD_LEFT + BTN_WIDTH*3 + SPACE*3, PAD_TOP, BTN_WIDTH, BTN_HEIGHT, (0, 0, 0), 'black', "K"))
    buttons.append(MenuButton(PAD_LEFT + BTN_WIDTH*4 + SPACE*4, PAD_TOP, BTN_WIDTH, BTN_HEIGHT, (0, 0, 0), 'red', "Q"))

init_buttons()

def init_background_objects():
    for i in range(WIDTH//2):
        if random.random() > 0.8:
            background_objects.append(backgroundObject())

init_background_objects()

def draw_buttons():
    for btn in buttons:
        btn.draw(WIN)

def add_background_objects():
    for i in range(50):
        background_objects.append(backgroundObject())

def update_background():
    
    add_background_objects()
    for obj in background_objects:
        obj.draw(WIN)
        delete = obj.update()
        if delete:
            background_objects.remove(obj)

def display_menu():
    WIN.fill(BACKGROUND_COLOR)
    pygame.draw.rect(WIN, BOARD_COLOR, (0, 0, WIDTH, HEIGHT), border_radius = 150) #felt color
    update_background()
    pygame.draw.rect(WIN, BROWN, (0, 0 , WIDTH, HEIGHT), 50, 150)
    for i in range(5):
        pygame.draw.rect(WIN, YELLOW, (PAD_LEFT + i *BTN_WIDTH + i*SPACE, PAD_TOP, BTN_WIDTH, BTN_HEIGHT), width = 10)
    

    draw_buttons()

    

def get_x_y(pos):
    return pos[0], pos[1]

def menu():
    running = True
    clock = pygame.time.Clock()
    
    while running:
        display_menu()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x,y = get_x_y(pos)
                    for i, btn in enumerate(buttons):
                        if (x > btn.x and x < (btn.x +btn.width)) and (y > btn.y and y < (btn.y + btn.height)):
                            if i == 0:
                                running = False
                            elif i == 1:
                                pygame.quit()
        pygame.display.update()
    main()
menu()




    
