import sys
#sys.path.append('./')
import pygame
from PONG.const import *
from PONG.ball import Ball
from PONG.paddle import Paddle
from PONG.draw import draw_game
import rede
pygame.init()

# Set the window size
WIND = pygame.display.set_mode((WIDTH, HEIGHT))
# Window Title
pygame.display.set_caption("pong")

def game(WIND, genomes=None, config=None, random=False, draw=True, win_score=10):
    run = True
    clock = pygame.time.Clock()

    # x, y, width, height
    left_paddle = Paddle(PADDLE_GAP, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - PADDLE_GAP - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # x, y, radius (the // is being used to obtain a rounded division)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS, random)

    left_score = 0
    right_score = 0

    nets = None
    if genomes != None:
        nets = rede.start_ai(genomes, config)

    while run:
        #draw_hits = True if len(genomes) > 1 else False
        #if draw:
        draw_game(WIND, [left_paddle, right_paddle], ball,
                 left_score, right_score, left_paddle.hits, 
                 right_paddle.hits)
        # Limits the function to only run at 60 times a second, it can run slower
        if genomes == None or genomes[0] != None:
            clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #if len(genomes) > 1:
                quit()
            #else:
             #       run = False
             #       break

        if nets != None:
            game_info = [ball, left_paddle, right_paddle]
            rede.loop_ai(nets, game_info)

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle, genomes)

        handle_collission(ball, left_paddle, right_paddle)

        score = False;
        if ball.x - BALL_RADIUS < 0:
            right_score += 1
            score = True
            pygame.time.delay(200)
        elif ball.x + BALL_RADIUS > WIDTH:
            left_score += 1
            score = True																								
            pygame.time.delay(200)

        if score:
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        run = reset_game([left_paddle, right_paddle], [left_score, right_score], win_score, genomes)
    #if len(genomes) < 1:
    pygame.quit()

def handle_paddle_movement(keys, left_p, right_p, genomes):
    if genomes == None or genomes[0] == None:
        if keys[pygame.K_w] and left_p.y - VEL >= 0:
            left_p.move(up=True)
        elif keys[pygame.K_s] and left_p.y + VEL <= HEIGHT - PADDLE_HEIGHT:
            left_p.move(up=False)

    if genomes == None or genomes[1] == None:
        if keys[pygame.K_UP] and right_p.y - VEL >= 0:
            right_p.move(up=True)
        elif keys[pygame.K_DOWN] and right_p.y + VEL <= HEIGHT - PADDLE_HEIGHT:
            right_p.move(up=False)

def handle_collission(ball, left_p, right_p):
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= HEIGHT:
            ball.y_vel *= -1

    if ball.x_vel > 0:
        if ball.x + ball.radius >= right_p.x and (right_p.y <= ball.y and right_p.y + PADDLE_HEIGHT >= ball.y):
            ball.x_vel *= -1

            # Reduction Factor: Max Distance / Reduction Fator = Max Velocity
            # Reduction Factor = Max Distance / Max Velocity
            
            difference_y = ball.y - (right_p.y + PADDLE_HEIGHT//2)
            reduction_factor = PADDLE_HEIGHT/2 / MAX_VEL
            ball.y_vel = difference_y // reduction_factor
            right_p.hits += 1

    else:
        if ball.x - ball.radius <= PADDLE_GAP + PADDLE_WIDTH and (left_p.y <= ball.y and left_p.y + PADDLE_HEIGHT >= ball.y):
            ball.x_vel *= -1

            # Reduction Factor: Max Distance / Reduction Fator = Max Velocity
            # Reduction Factor = Max Distance / Max Velocity
            
            difference_y = ball.y - (left_p.y + PADDLE_HEIGHT//2)
            reduction_factor = PADDLE_HEIGHT/2 / MAX_VEL
            ball.y_vel = difference_y // reduction_factor
            left_p.hits += 1
            
    ball.move()


def reset_game(paddles, scores, win_score, genomes):
    won = False
    win_text = "Left"
    if scores[0] >= win_score:
        won = True
    elif scores[1] >= win_score:
        won = True
        win_text = "Right"

    run = True 
    if won or paddles[0].hits > 20:
        left_score = 0
        right_score = 0
        won = False
        if genomes == None or genomes[1] == None:
            text = SCORE_FONT.render(win_text + " Player Wins", 1, PURPLE2)
            WIND.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
        elif len(genomes) > 1:
            genomes[0].fitness += paddles[0].hits + left_score
            genomes[1].fitness += paddles[1].hits + right_score
        run = False
        paddles[1].hits = 0
        paddles[1].hits = 0
    return run 
