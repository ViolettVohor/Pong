from const import *
from random import randint
import pygame

class Ball:
    def __init__(self, x, y, radius, random_y_vel=False):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = MAX_VEL
        if random_y_vel:
            self.y_vel = self.original_y_vel = randint(-1 * MAX_VEL, MAX_VEL)
        else:
            self.y_vel = self.original_y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, BALL_COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self, random_y_vel=False):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        if random_y_vel:
            self.y_vel = randint(-1 * MAX_VEL, MAX_VEL)
        else:
            self.y_vel = 0
