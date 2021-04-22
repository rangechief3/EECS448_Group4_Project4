import pygame
from .constants import *

class MenuButton:
    def __init__(self, x, y, width, height, color, suit_colors, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.suit_colors = suit_colors
        self.text = text
        self.get_decorator_images()

    def get_decorator_images(self):
        if self.suit_colors == "red":
            self.images = [MENU_DMD, MENU_HRT]
            self.font_color = (255, 0, 0)
            self.font_shadow = (0, 0, 0)
        else:
            self.images = [MENU_CLUB, MENU_SPD]
            self.font_color = (0, 0, 0)
            self.font_shadow = (255, 0, 0)
    
    def draw(self, win):
        PADDING = 5
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(win, (255, 255, 255), (self.x + PADDING, self.y+ PADDING, self.width-PADDING * 2, self.height-PADDING * 2), border_radius=10)
        font = pygame.font.SysFont('Arial',33)
        text = font.render(self.text, 1, self.font_color)
        win.blit(text, ((self.x + self.width//2) - text.get_width()//2, (self.y + self.height//2) - text.get_height()//2))
        #text = font.render(self.text, 1, self.font_shadow)
        TEXT_OFFSET = 1
        #win.blit(text, ((self.x + self.width//2 + TEXT_OFFSET) - text.get_width()//2, (self.y + self.height//2 + TEXT_OFFSET) - text.get_height()//2))
        self.draw_decorators(win)

    def draw_decorators(self, win):
        img_width = self.images[0].get_width()
        img_height = self.images[0].get_height()
        
        win.blit(self.images[0], ((self.x +img_width //2, self.y + img_height // 2)))
        win.blit(self.images[0], (((self.x + self.width -img_width) - img_width //2, (self.y + self.height-img_height) - img_height // 2)))
        win.blit(self.images[1], ((self.x + img_width //2, (self.y + self.height - img_height) - img_height //2)))
        win.blit(self.images[1], (((self.x + self.width - img_width) - img_width //2, self.y + img_height //2)))