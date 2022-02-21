from turtle import width
import pygame
import time

WIDTH = 500
HEIGHT = 650

game_active = True
hits = 0
orange_row_contact = True
red_row_contact = True

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
        id = (i * 14) + j
        # block position
        blocks[id].append(pygame.Rect((8 + (j*35)), (133 + (i*13)), 30, 8))
        # height is always 8 and width is always 30

# Load Player and ball
player_surf = pygame.image.load('graphics/player.png').convert()
player_rect = player_surf.get_rect(midbottom=(250, 620))
player_moving_left = False
player_moving_right = False

ball_surf = pygame.image.load('graphics/ball.png').convert()
ball_rect = ball_surf.get_rect(midbottom=(200000, 200000))
ball_velocity = 3
ball_dx = ball_velocity
ball_dy = ball_velocity * (-1)

# Load score
score_surf_1 = game_font.render('000', False, 'White')
score_surf_2 = game_font.render('000', False, 'White')

round_surf_1 = game_font.render('1', False, 'White')
round_surf_2 = game_font.render('1', False, 'White')

score = 0
round = 0

# Background Image
back_img = pygame.image.load('graphics/background.png').convert()

# Player movement
def player_update():
    if game_active:
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
    global ball_dx, ball_dy, game_active, round, hits, ball_velocity

    ball_rect.x += ball_dx
    ball_rect.y += ball_dy

    # Walls collision
    if ball_rect.top <= 20:
        ball_dy = ball_velocity
        pygame.mixer.music.load('sounds/sound_1.mp3')
        pygame.mixer.music.play(0)
    if ball_rect.bottom >= HEIGHT: # lost the round
        ball_rect.midbottom = (WIDTH / 2, 350)
        ball_dy = ball_velocity * (-1)
        round += 1
        if game_active:
            set_round(round)
        pygame.mixer.music.load('sounds/sound_2.mp3')
        pygame.mixer.music.play(0)
        if round > 1:
            time.sleep(3)
            hits = 0
            ball_velocity = 3
    if ball_rect.left <= 0:
        ball_dx = ball_velocity
        pygame.mixer.music.load('sounds/sound_1.mp3')
        pygame.mixer.music.play(0)
    if ball_rect.right >= WIDTH:
        ball_dx = ball_velocity * (-1)
        pygame.mixer.music.load('sounds/sound_1.mp3')
        pygame.mixer.music.play(0)

    # Paddle collision
    if ball_rect.colliderect(player_rect):
        ball_dy = ball_velocity * (-1)
        pygame.mixer.music.load('sounds/sound_1.mp3')
        pygame.mixer.music.play(0)
    
    if block_collision():
        if ball_dy > 0:
            ball_dy = ball_velocity * (-1)
        else:
            ball_dy = ball_velocity


# Ball collision with the blocks
def block_collision():
    global blocks, ball_dx, ball_dy, ball_velocity, score, hits
    for block in blocks:
        # check collision
        if ball_rect.colliderect(block[2]) and block[1]:
            
            pygame.mixer.music.load('sounds/sound_1.mp3')
            pygame.mixer.music.play(0)

            if game_active:
                block[1] = False
                hits += 1

                if hits == 4:
                    set_velocity(0)
                elif hits == 12:
                    set_velocity(1)

                # New score
                if block[0] == '#a60601':
                    score += 7
                    set_velocity(4)
                elif block[0] =='#c98100':
                    score += 5
                    set_velocity(3)
                elif block[0] =='#007e25':
                    score += 3
                elif block[0] =='#c6c811':
                    score += 1
                
                set_score(score)

            if ball_rect.right - ball_velocity < block[2].left:
                ball_dx = ball_velocity * (-1)
            elif ball_rect.left + ball_velocity > block[2].right:
                ball_dx = ball_velocity
            
            if ball_rect.top + ball_velocity > block[2].bottom or ball_rect.bottom - ball_velocity < block[2].top:
                return True

# set score_surf text
def set_score(new_score):
    global score_surf_1

    if new_score < 10:
        score_surf_1 = game_font.render(f'00{new_score}', False, 'White')
    elif new_score < 100:
        score_surf_1 = game_font.render(f'0{new_score}', False, 'White')
    else:
        score_surf_1 = game_font.render(f'{new_score}', False, 'White')

def set_round(new_round):
    global round_surf_2, player_surf, player_rect, game_active
    round_surf_2 = game_font.render(f'{new_round}', False, 'White')

    if new_round == 4:
        player_surf = pygame.image.load('graphics/initial.png').convert()
        player_rect = player_surf.get_rect(midbottom=(250, 620))
        game_active = False

def set_velocity(situation):
    global ball_velocity

    if situation == 0:
        ball_velocity = 3 * 1.3
    elif situation == 2:
        ball_velocity = 3 * 1.5
    elif situation == 3:
        ball_velocity = 3 * 1.7
    else:
        ball_velocity = 3 * 2

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
            block = blocks[(i * 14) + j]
            # if the block isn't broken
            if block[1]:
                pygame.draw.rect(screen, block[0], block[2])

    # Player and ball
    screen.blit(player_surf, player_rect)
    screen.blit(ball_surf, ball_rect)

    player_update()
    ball_update()

    # Score
    screen.blit(round_surf_1, (40, 25))
    screen.blit(round_surf_2, (320, 25))

    screen.blit(score_surf_1, (45, 85))
    screen.blit(score_surf_2, (325, 85))

    pygame.display.update()

    # makes sure that the loop won't run faster than
    # 60 frames per second
    clock.tick(60)