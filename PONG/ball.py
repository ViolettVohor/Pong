from PONG.const import *
from random import randint
import pygame

class Ball:
    def __init__(self, x, y, radius, random):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = MAX_VEL
        self.y_vel = self.vel(random) 
        self.random = random

    def vel(self, random):
        if random:
            while True:
                vel = randint(-1 * MAX_VEL, MAX_VEL)
                if vel != 0: return vel
        else:
            return 0

    def draw(self, win):
        pygame.draw.circle(win, BALL_COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = self.vel(self.random) 
