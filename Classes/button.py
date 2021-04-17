import pygame

BUTTON_HEIGHT = 50
BUTTON_WIDTH = 100

class Button:
    def __init__(self, x , y, text):
        self.x = x
        self.y = y 
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        self.text = text
        self.border_width = 5
        self.box_color = (255, 255, 255)
        self.hidden = False
        self.clickable = True

    def draw(self, win):
        if(self.hidden == False):
            pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.width, self.height), 0, 7)
            pygame.draw.rect(win, self.box_color, (self.x + self.border_width, self.y + self.border_width, self.width - 2*self.border_width, self.height - 2*self.border_width), 0, 3)
            font = pygame.font.SysFont('Arial',20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, ((self.x + self.width//2) - text.get_width()//2, (self.y + self.height//2) - text.get_height()//2))
