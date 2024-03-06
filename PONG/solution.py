import sys
#sys.path.append('./')
import pygame
from PONG.const import *
from PONG.ball import Ball
from PONG.paddle import Paddle
import rede
pygame.init()

# Set the window size
WIND = pygame.display.set_mode((WIDTH, HEIGHT))
# Window Title
pygame.display.set_caption("Pong")

def main(genomes=None, config=None, random=False, draw=True):
    run = True
    clock = pygame.time.Clock()

    # x, y, width, height
    left_paddle = Paddle(PADDLE_GAP, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - PADDLE_GAP - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # x, y, radius (the // is being used to obtain a rounded division)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS, random)

    left_score = 0
    right_score = 0

    if genomes != None:
        nets = rede.start_ai(genomes, config)

    while run:
        draw_hits = True if len(genomes) > 1 else False
        if draw:
            draw(WIND, [left_paddle, right_paddle], ball,
                 left_score, right_score, left_paddle.hits, 
                 right_paddle.hits, draw_hits)
        # Limits the function to only run at 60 times a second, it can run slower
        if genomes == None:
            clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if len(genomes) > 1:
                    quit()
                else:
                    run = False
                    break

        if nets != None:
            game_info = [ball, left_paddle, right_paddle]
            rede.loop_ai(nets, game_info, config)

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

        won = False
        win_score = WINNING_SCORE if genomes == None else 2
        if left_score >= win_score:
            won = True
            win_text = "Left"
        elif right_score >= win_score:
            won = True
            win_text = "Right"
        
        if won or left_paddle.hits > 20:
            left_score = 0
            right_score = 0
            won = False
            if genomes == None:
                text = SCORE_FONT.render(win_text + " Player Wins", 1, PURPLE2)
                WIND.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
                pygame.display.update()
                pygame.time.delay(3000)
            elif len(genomes) > 1:
                genomes[0].fitness += left_paddle.hits + left_score
                genomes[1].fitness += right_paddle.hits + right_score
                run = False
            left_paddle.hits = 0
            right_paddle.hits = 0

    if len(genomes) < 1:
        pygame.quit()

def draw(wind, paddles, ball, left_score, right_score, left_hits, right_hits, draw_hits):
    wind.fill(WIND_COLOR)

    if not draw_hits:
        left_score_text = SCORE_FONT.render(f"{left_score}", 1, PURPLE2) 
        right_score_text = SCORE_FONT.render(f"{right_score}", 1, PURPLE2) 
        
        wind.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()/2, 30))
        wind.blit(right_score_text, (3 * WIDTH//4 - right_score_text.get_width()/2, 30))
    else:
        hits = SCORE_FONT.render(f"{right_hits + left_hits}", 1, PURPLE2) 
        wind.blit(hits, (WIDTH//2 - hits.get_width()/2, 30))

    # initial gap, height of window, amount of rectangles on the line
    for i in range(HEIGHT//LINE_AMOUNT//4, HEIGHT, HEIGHT//LINE_AMOUNT):
        pygame.draw.rect(wind, LINE_COLOR, (WIDTH//2 - LINE_WIDTH//2, i, LINE_WIDTH, HEIGHT//LINE_AMOUNT//2))

    for paddle in paddles:
        paddle.draw(wind)

    ball.draw(wind)

    pygame.display.update()

def handle_paddle_movement(keys, left_p, right_p, genomes):
    if genomes[0] == None:
        if keys[pygame.K_w] and left_p.y - VEL >= 0:
            left_p.move(up=True)
        elif keys[pygame.K_s] and left_p.y + VEL <= HEIGHT - PADDLE_HEIGHT:
            left_p.move(up=False)

    if genomes[1] == None:
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

# It only runs the function if the file 
# is executed and not imported
if __name__ == '__main__':
    main()
