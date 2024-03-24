import pygame
from PONG.const import *

pygame.init()

def draw_main_menu(wind, main_button):
    title = SCORE_FONT.render("PONG", 1, PURPLE2)
    play1 = SCORE_FONT.render("1 Player", 1, PURPLE2)
    play2 = SCORE_FONT.render("2 Players", 1, PURPLE2)
    train = SCORE_FONT.render("Train", 1, PURPLE2)

    wind.blit(title, (WIDTH//2 - title.get_width()/2, HEIGHT//8))

    button1 = SCREEN_BUTTON
    button2 = SCREEN_BUTTON
    button3 = SCREEN_BUTTON
    match main_button:
        case 2:
            button1 = SEL_SCREEN_BUTTON
        case 3:
            button2 = SEL_SCREEN_BUTTON
        case 4:
            button3 = SEL_SCREEN_BUTTON

    pygame.draw.rect(wind, button1, (WIDTH*3//8, HEIGHT*2//8 + HEIGHT//16, WIDTH//4, HEIGHT//8)) 
    wind.blit(play1, (WIDTH//2 - play1.get_width()/2, HEIGHT*3//8 - play1.get_height()/2))

    pygame.draw.rect(wind, button2, (WIDTH*3//8, HEIGHT*4//8 + HEIGHT//16, WIDTH//4, HEIGHT//8)) 
    wind.blit(play2, (WIDTH//2 - play2.get_width()/2, HEIGHT*5//8 - play2.get_height()/2))

    pygame.draw.rect(wind, button3, (WIDTH*3//8, HEIGHT*6//8 + HEIGHT//16, WIDTH//4, HEIGHT//8)) 
    wind.blit(train, (WIDTH//2 - train.get_width()/2, HEIGHT*7//8 - train.get_height()/2))

def draw_difficulty(wind, diff_button):
    title = SCORE_FONT.render("Difficulty", 1, PURPLE2)
    diff1 = SCORE_FONT.render("Easy", 1, PURPLE2)          # Fitness 50
    diff2 = SCORE_FONT.render("Normal", 1, PURPLE2)        # Fitness 100
    diff3 = SCORE_FONT.render("Hard", 1, PURPLE2)          # Fitness 200

    wind.blit(title, (WIDTH//2 - title.get_width()/2, HEIGHT//8))

    button1 = SCREEN_BUTTON
    button2 = SCREEN_BUTTON
    button3 = SCREEN_BUTTON
    match diff_button:
        case 2:
            button1 = SEL_SCREEN_BUTTON
        case 3:
            button2 = SEL_SCREEN_BUTTON
        case 4:
            button3 = SEL_SCREEN_BUTTON

    pygame.draw.rect(wind, button1, (WIDTH*3//8, HEIGHT*2//8 + HEIGHT//16, WIDTH//4, HEIGHT//8)) 
    wind.blit(diff1, (WIDTH//2 - diff1.get_width()/2, HEIGHT*3//8 - diff1.get_height()/2))

    pygame.draw.rect(wind, button2, (WIDTH*3//8, HEIGHT*4//8 + HEIGHT//16, WIDTH//4, HEIGHT//8)) 
    wind.blit(diff2, (WIDTH//2 - diff2.get_width()/2, HEIGHT*5//8 - diff2.get_height()/2))

    pygame.draw.rect(wind, button3, (WIDTH*3//8, HEIGHT*6//8 + HEIGHT//16, WIDTH//4, HEIGHT//8)) 
    wind.blit(diff3, (WIDTH//2 - diff3.get_width()/2, HEIGHT*7//8 - diff3.get_height()/2))

def draw_game(wind, paddles, ball, left_score, right_score, left_hits, right_hits, draw_hits=False, draw_score=True):
    wind.fill(WIND_COLOR)
    
    if draw_score:
        left_score_text = SCORE_FONT.render(f"{left_score}", 1, PURPLE2) 
        right_score_text = SCORE_FONT.render(f"{right_score}", 1, PURPLE2) 
        
        wind.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()/2, 30))
        wind.blit(right_score_text, (3 * WIDTH//4 - right_score_text.get_width()/2, 30))

    if draw_hits:
        hits = SCORE_FONT.render(f"{right_hits + left_hits}", 1, PURPLE2) 
        wind.blit(hits, (WIDTH//2 - hits.get_width()/2, 30))

    # initial gap, height of window, amount of rectangles on the line
    for i in range(HEIGHT//LINE_AMOUNT//4, HEIGHT, HEIGHT//LINE_AMOUNT):
        pygame.draw.rect(wind, LINE_COLOR, (WIDTH//2 - LINE_WIDTH//2, i, LINE_WIDTH, HEIGHT//LINE_AMOUNT//2))

    for paddle in paddles:
        paddle.draw(wind)

    ball.draw(wind)

    pygame.display.update()
