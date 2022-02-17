from turtle import width
import pygame

WIDTH = 500
HEIGHT = 650

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Breakout - LPC2022')

# framerate
clock = pygame.time.Clock()

# Game font
game_font = pygame.font.Font('font/Pixeltype.ttf', 80)

# Load Blocks
blocks = []

for i in range(28): blocks.append(["#a60601", True])
for i in range(28): blocks.append(["#c98100", True])
for i in range(28): blocks.append(["#007e25", True])
for i in range(28): blocks.append(["#c6c811", True])

# Load Player and ball
player_surf = pygame.image.load('graphics/player.png').convert()
player_rect = player_surf.get_rect(midbottom = (250, 620))
player_moving_left = False
player_moving_right = False

ball_surf = pygame.image.load('graphics/ball.png').convert()
ball_rect = ball_surf.get_rect(midbottom = (WIDTH/2, 580))

# Load score
score_surf = game_font.render('000', False, 'White')
round_surf = game_font.render('1', False, 'White')

# Background Image
back_img = pygame.image.load('graphics/background.png').convert()

# Player movement
def player_update():
    if player_moving_right:
        player_rect.x += 7
    if player_moving_left:
        player_rect.x -= 7
    
    if player_rect.left <= 0:
        player_rect.left = 0
    if player_rect.right >= WIDTH:
        player_rect.right = WIDTH

# Game loop
while True:
    # Check player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # desinitialize pygame
            pygame.quit()
            # close de program
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_moving_right = True
            if event.key == pygame.K_LEFT:
                player_moving_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_moving_right = False
            if event.key == pygame.K_LEFT:
                player_moving_left = False
    
    # Load background
    screen.blit(back_img, (0, 0))

    # rows
    for i in range(8):
        # collumns
        for j in range(14):
            block = blocks[(i*14) + j]
            # if the block isn't broken
            if block[1]:
                pygame.draw.line(screen, block[0], (8 + (j*35), 133 + (i*13)), (38 + (j*35), 133 + (i*13)), 8)
    
    # Score
    screen.blit(round_surf, (40, 25))
    screen.blit(round_surf, (320, 25))

    screen.blit(score_surf, (45, 85))
    screen.blit(score_surf, (325, 85))
    
    # Player and ball
    screen.blit(player_surf, player_rect)
    screen.blit(ball_surf, ball_rect)

    player_update()
    
    pygame.display.update()

    # makes sure that the loop won't run faster than
    # 60 frames per second
    clock.tick(60)