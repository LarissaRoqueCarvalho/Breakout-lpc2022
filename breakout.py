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

# rows
for i in range(8):
    # collumns
    for j in range(14):
        id = (i*14) + j
        # block position
        blocks[id].append(8 + (j*35)) # x position
        blocks[id].append(133 + (i*13)) # y position
        # height is always 8 and width is always 30

# Load Player and ball
player_surf = pygame.image.load('graphics/player.png').convert()
player_rect = player_surf.get_rect(midbottom = (250, 620))
player_moving_left = False
player_moving_right = False

ball_surf = pygame.image.load('graphics/ball.png').convert()
ball_rect = ball_surf.get_rect(midbottom = (WIDTH/2, 580))
ball_velocity = 3
ball_dx = ball_velocity
ball_dy = ball_velocity * (-1)

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
    
    # Walls collision
    if player_rect.left <= 0:
        player_rect.left = 0
    if player_rect.right >= WIDTH:
        player_rect.right = WIDTH

# Ball movement
def ball_update():
    global ball_dx
    global ball_dy

    ball_rect.x += ball_dx
    ball_rect.y += ball_dy

    # Walls collision
    if ball_rect.top <= 20:
        ball_dy = ball_velocity
    if ball_rect.bottom >= HEIGHT:
        ball_dy = ball_velocity * (-1)
    if ball_rect.left <= 0:
        ball_dx = ball_velocity
    if ball_rect.right >= WIDTH:
        ball_dx = ball_velocity * (-1)
    
    # Paddle collision
    if ball_rect.colliderect(player_rect):
        ball_dy = ball_velocity * (-1)
    
    # Collision with a block
    if block_collision():
        ball_dy = ball_velocity

# Ball collision with the blocks
def block_collision():
    global blocks
    for i in range(len(blocks)):
        # check collision
        if ball_rect.colliderect(pygame.Rect((blocks[i][2], blocks[i][3]), (30, 8))) and blocks[i][1]:
            blocks[i][1] = False
            return True

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
    ball_update()
    
    pygame.display.update()

    # makes sure that the loop won't run faster than
    # 60 frames per second
    clock.tick(60)