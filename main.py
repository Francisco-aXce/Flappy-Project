import pygame
import sys
import random


def draw_floor():
    global floor_x_pos
    screen.blit(floor_sf, (floor_x_pos, 450))
    screen.blit(floor_sf, (floor_x_pos+SCREEN_SIZE[0], 450))
    floor_x_pos -= 1
    if floor_x_pos <= -SCREEN_SIZE[0]:
        floor_x_pos = 0


def create_pipe():
    pos = random.choice(pipe_pos)
    buttom_pipe_rect = pipe_sf.get_rect(midtop=(SCREEN_SIZE[0] + 50, pos))
    top_pipe_rect = fpipe_sf.get_rect(midbottom=(SCREEN_SIZE[0] + 50, pos - 150))
    score_rect = pygame.Rect(top_pipe_rect.bottomright[0],top_pipe_rect.bottomright[1], 4, 150)
    score_rects.append(score_rect)
    return buttom_pipe_rect, top_pipe_rect


def draw_pipes():
    for pipe in pipe_list:
        if pipe.bottom > SCREEN_SIZE[1]:
            screen.blit(pipe_sf, pipe.topleft)
        else:
            screen.blit(fpipe_sf, pipe.topleft)


def move_pipes():
    for pipe in pipe_list:
        pipe.centerx -= pipe_speed
    for score_rect in score_rects:
        score_rect.centerx -= pipe_speed


def delete_pipes():
    if len(pipe_list) > 8:
        pipe_list.pop(0)
        pipe_list.pop(1)
    if len(score_rects) > 4:
        score_rects.pop(0)


def check_collisions():
    global game_active, bird_movement, bird_index, score
    for pipe in pipe_list:
        if pipe.colliderect(bird_rect):
            game_active = False
            die_sound.play()
            bird_index = 0
            pipe_list.clear()
            score_rects.clear()
            bird_movement = 0
            bird_rect.centery = 256

    if bird_rect.top <= 0 or bird_rect.bottom >= 450:
        game_active = False
        die_sound.play()
        bird_index = 0
        pipe_list.clear()
        score_rects.clear()
        bird_movement = 0
        bird_rect.centery = 256

    for i in range(len(score_rects)):
        if score_rects[i].colliderect(bird_rect):
            score += 1
            score_sound.play()
            score_rects[i].centery -= 500

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * -3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_rect


def score_display(game_active):
    if game_active:
        score_sf = game_font.render(str(score), True, (255, 255, 255))
        score_rect = score_sf.get_rect(center=(144, 100))
        screen.blit(score_sf, score_rect.topleft)
    else:
        score_sf = game_font.render(
            "Score: " + str(score), True, (255, 255, 255))
        score_rect = score_sf.get_rect(center=(144, 100))
        screen.blit(score_sf, score_rect.topleft)
        high_score_sf = game_font.render(
            "High score: " + str(high_score), True, (255, 255, 255))
        high_score_rect = high_score_sf.get_rect(center=(144, 410))
        screen.blit(high_score_sf, high_score_rect.topleft)


pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
SCREEN_SIZE = (288, 512)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 250)
game_font = pygame.font.Font('04B_19.ttf', 20)

# Variables
floor_x_pos = 0
gravity = 0.15
bird_movement = 0
jump_force = 5.5
pipe_list = []
score_rects = []
pipe_speed = 2
pipe_pos = (200, 300, 400)
game_active = False
score = 0
high_score = 0
bird_index = 0


background_sf = pygame.image.load("sprites/background-day.png").convert()

floor_sf = pygame.image.load("sprites/base.png").convert()

bird_mid_sf = pygame.image.load("sprites/yellowbird-midflap.png").convert_alpha()
bird_up_sf = pygame.image.load("sprites/yellowbird-upflap.png").convert_alpha()
bird_down_sf = pygame.image.load("sprites/yellowbird-downflap.png").convert_alpha()
bird_frames = [bird_mid_sf, bird_up_sf, bird_down_sf]
bird_sf = bird_mid_sf
rotated_bird_sf = bird_sf
bird_rect = bird_sf.get_rect(center=(50, 256))

pipe_sf = pygame.image.load("sprites/pipe-green.png").convert()
fpipe_sf = pygame.transform.flip(pipe_sf, False, True)

message_sf = pygame.image.load("sprites/message.png").convert_alpha()
message_rect = message_sf.get_rect(center = (144, 256))

flap_sound = pygame.mixer.Sound("sounds/sfx_wing.wav")
die_sound = pygame.mixer.Sound("sounds/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sounds/sfx_point.wav")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    game_active = True
                    if score > high_score:
                        high_score = score
                    score = 0
                bird_movement = 0
                bird_movement -= jump_force
                flap_sound.play()
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
            delete_pipes()
        if event.type == BIRDFLAP and game_active:
            if bird_index < len(bird_frames) - 1:
                bird_index += 1
            else:
                bird_index = 0

    # Background
    screen.blit(background_sf, (0, 0))

    # Bird
    if game_active:
        bird_movement += gravity
        bird_rect.centery += round(bird_movement)
        check_collisions()
        screen.blit(rotated_bird_sf, bird_rect.topleft)
    else:
        screen.blit(message_sf, message_rect)
    bird_sf, bird_rect = bird_animation()
    rotated_bird_sf = rotate_bird(bird_sf)

    # Pipes
    if game_active:
        draw_pipes()
        move_pipes()
    
    # Score
    score_display(game_active)

    """ for pipe in pipe_list:
        pygame.draw.rect(screen, (0, 0, 0), pipe)
    pygame.draw.rect(screen, (0, 0, 0), bird_rect)
    for score_rect in score_rects:
        pygame.draw.rect(screen, (0, 255, 0), score_rect) """

    # Floor
    draw_floor()

    pygame.display.update()
    clock.tick(120)