import pygame
from const import *
from paddle import Paddle
from ball import Ball

class PongGame:
    def __init__(self):
        # Set the window size
        self.WIND = pygame.display.set_mode((WIDTH, HEIGHT))
        # x, y, width, height
        self.left_paddle = Paddle(PADDLE_GAP, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.right_paddle = Paddle(WIDTH - PADDLE_GAP - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

        # x, y, radius (the // is being used to obtain a rounded division)
        self.ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS, True)

        self.left_score = 0
        self.right_score = 0

    def draw(self):
        self.WIND.fill(WIND_COLOR)

        left_score_text = SCORE_FONT.render(f"{self.left_score}", 1, PURPLE2) 
        right_score_text = SCORE_FONT.render(f"{self.right_score}", 1, PURPLE2) 
        
        self.WIND.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()/2, 30))
        self.WIND.blit(right_score_text, (3 * WIDTH//4 - left_score_text.get_width()/2, 30))

        # initial gap, height of window, amount of rectangles on the line
        for i in range(HEIGHT//LINE_AMOUNT//4, HEIGHT, HEIGHT//LINE_AMOUNT):
            pygame.draw.rect(self.WIND, LINE_COLOR, (WIDTH//2 - LINE_WIDTH//2, i, LINE_WIDTH, HEIGHT//LINE_AMOUNT//2))

        self.left_paddle.draw(self.WIND)
        self.right_paddle.draw(self.WIND)

        self.ball.draw(self.WIND)

        pygame.display.update()

    def handle_paddle_movement(self, keys):
        if keys[pygame.K_w] and self.left_paddle.y - VEL >= 0:
            self.left_paddle.move(up=True)
        elif keys[pygame.K_s] and self.left_paddle.y + VEL <= HEIGHT - PADDLE_HEIGHT:
            self.left_paddle.move(up=False)

        if keys[pygame.K_UP] and self.right_paddle.y - VEL >= 0:
            self.right_paddle.move(up=True)
        elif keys[pygame.K_DOWN] and self.right_paddle.y + VEL <= HEIGHT - PADDLE_HEIGHT:
            self.right_paddle.move(up=False)

    def handle_collission(self):
        if self.ball.y - self.ball.radius <= 0 or self.ball.y + self.ball.radius >= HEIGHT:
                self.ball.y_vel *= -1

        if self.ball.x_vel > 0:
            if self.ball.x + self.ball.radius >= self.right_paddle.x and (self.right_paddle.y <= self.ball.y and self.right_paddle.y + PADDLE_HEIGHT >= self.ball.y):
                self.ball.x_vel *= -1

                # Reduction Factor: Max Distance / Reduction Fator = Max Velocity
                # Reduction Factor = Max Distance / Max Velocity
                
                difference_y = self.ball.y - (self.right_paddle.y + PADDLE_HEIGHT//2)
                reduction_factor = PADDLE_HEIGHT/2 / MAX_VEL
                self.ball.y_vel = difference_y // reduction_factor

        else:
            if self.ball.x - self.ball.radius <= PADDLE_GAP + PADDLE_WIDTH and (self.left_paddle.y <= self.ball.y and self.left_paddle.y + PADDLE_HEIGHT >= self.ball.y):
                self.ball.x_vel *= -1

                # Reduction Factor: Max Distance / Reduction Fator = Max Velocity
                # Reduction Factor = Max Distance / Max Velocity
                
                difference_y = self.ball.y - (self.left_paddle.y + PADDLE_HEIGHT//2)
                reduction_factor = PADDLE_HEIGHT/2 / MAX_VEL
                self.ball.y_vel = difference_y // reduction_factor
                
        self.ball.move()

