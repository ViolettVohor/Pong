from PONG.const import *
import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.hits = 0

    def draw(self, wind):
        pygame.draw.rect(wind, PADDLE_COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= VEL
        else:
            self.y += VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
