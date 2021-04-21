import random
import pygame
import math
from .constants import WIDTH, HEIGHT,BACKGROUND_OBJECTS

class backgroundObject:
    def __init__(self):
        self.x = self.get_random(WIDTH)
        self.y = 0
        self.vel = self.get_random(3) + 1
        self.acc = self.get_random(2) + 1
        self.img = random.choice(BACKGROUND_OBJECTS)

    def get_random(self, max):
        return math.floor(random.random() * max)
    
    def draw(self, win):
        win.blit(self.img, (self.x + self.img.get_width()//2, self.y))
    
    def update(self):
        self.y += self.vel
        self.vel += self.acc
        if (self.y >= HEIGHT):
            return True #if returning true(delete), then remove item 
        return False
