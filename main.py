import neat
import os
import pygame
from PONG.const import *
from PONG.draw import *
from PONG.solution import game 
from execute import *

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config.txt")

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

#run_neat(config)
#against_ai(config)

pygame.init()

WIND = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

screen_button = 2
current_screen = 1
difficulty = 0

clock = pygame.time.Clock()

while True:
    clock.tick(FPS)
    WIND.fill(WIND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and screen_button - 1 > 1:
        pygame.time.delay(100)
        screen_button -= 1
    elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and screen_button + 1 < 5:
        pygame.time.delay(100)
        screen_button += 1

    if keys[pygame.K_RETURN]:
        if current_screen == 1:
            current_screen = screen_button
            screen_button = 2
            pygame.time.delay(100)
        elif current_screen == 2:
            current_screen = 3
            difficulty = screen_button

    match current_screen:
        case 1:
            draw_main_menu(WIND, screen_button)
        case 2:
            draw_difficulty(WIND, screen_button)
        case 3:
            break;

    pygame.display.update()

if current_screen == 3:
    match difficulty:
        case 0:
            game(WIND)
        case 2:
            with open("easy.pickle", "rb") as file:
                easy = pickle.load(file)

            game(WIND, [easy, None], config)

