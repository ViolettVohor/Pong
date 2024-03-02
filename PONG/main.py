sys.path.append('../NEAT/')

from solution import PongGame
from const import *
from NEAT.neat.py import move_ai
import pygame

def main(ai=False, net1=None, net2=None):
    # Window Title
    pygame.display.set_caption("Pong")
    pygame.init()

    run = True
    clock = pygame.time.Clock()
    game = PongGame()

    while run:
        game.draw()
        # Limits the function to only run at 60 times a second, it can run slower
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()

        if ai:
            if net1 != None:
                move_ai(net1, game.ball, game.left_paddle)
            elif net2 != None:
                move_ai(net2, game.ball, game.right_paddle)

        game.handle_paddle_movement(keys)

        game.handle_collission()

        score = False;
        if game.ball.x - BALL_RADIUS < 0:
            game.right_score += 1
            score = True
            pygame.time.delay(200)
        elif game.ball.x + BALL_RADIUS > WIDTH:
            game.left_score += 1
            score = True																								
            pygame.time.delay(200)

        if score:
            game.ball.reset(True)
            game.left_paddle.reset()
            game.right_paddle.reset()

        won = False
        if game.left_score >= WINNING_SCORE:
            won = True
            win_text = "Left"
        elif game.right_score >= WINNING_SCORE:
            won = True
            win_text = "Right"
        
        if won:
            text = SCORE_FONT.render(win_text + " Player Wins", 1, PURPLE2)
            WIND.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            game.left_score = 0
            game.right_score = 0
            won = False

    pygame.quit()

# It only runs the function if the file 
# is executed and not imported
if __name__ == '__main__':
    main()
