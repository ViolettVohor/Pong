import pygame
pygame.init()
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
PURPLE2 = (150, 0, 244)

# Score
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 10

# Window Related
WIDTH, HEIGHT = 700, 500
WIND_COLOR = BLACK
FPS = 60

# Paddle Related
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_COLOR = WHITE
PADDLE_GAP = 10
VEL = 6

# Line Related
LINE_WIDTH, LINE_AMOUNT = 2, 10
LINE_COLOR = PURPLE
LINE_SPACE = 30

# Ball Related
MAX_VEL = 5
BALL_RADIUS = 6
BALL_COLOR = WHITE
