import pygame, sys, random

def draw_floor():
    global floor_x_pos
    screen.blit(floor_sf, (floor_x_pos,450))
    screen.blit(floor_sf, (floor_x_pos+SCREEN_SIZE[0],450))
    floor_x_pos -= 1
    if floor_x_pos <= -SCREEN_SIZE[0]:
        floor_x_pos = 0


def create_pipe():
    pos = random.choice(pipe_pos)
    buttom_pipe_rect = pipe_sf.get_rect(midtop = (SCREEN_SIZE[0] + 50, pos))
    top_pipe_rect = fpipe_sf.get_rect(midbottom = (SCREEN_SIZE[0] + 50, pos - 150))
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


def delete_pipes():
    if len(pipe_list) > 8:
        pipe_list.pop(0)
        pipe_list.pop(1)


def check_collisions():
    for pipe in pipe_list:
        if pipe.colliderect(bird_rect):
            print("Collision")
    
    if bird_rect.top <= 0 or bird_rect.bottom >= 450:
        print("Limit")

pygame.init()
SCREEN_SIZE = (288,512)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Variables
floor_x_pos = 0
gravity = 0.15
bird_movement = 0
jump_force = 5.5
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_speed = 2
pipe_pos = (200, 300, 400)

background_sf = pygame.image.load("sprites/background-day.png").convert()

floor_sf = pygame.image.load("sprites/base.png").convert()

bird_sf = pygame.image.load("sprites/yellowbird-midflap.png").convert()
bird_rect = bird_sf.get_rect(center = (50, 256))

pipe_sf = pygame.image.load("sprites/pipe-green.png")
fpipe_sf = pygame.transform.flip(pipe_sf, False, True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= jump_force
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            delete_pipes()


    # Background
    screen.blit(background_sf, (0,0))

    # Bird
    bird_movement += gravity
    bird_rect.centery += round(bird_movement)
    screen.blit(bird_sf, bird_rect.center)
    check_collisions()

    # Pipes
    draw_pipes()
    move_pipes()
    for pipe in pipe_list:
        pygame.draw.rect(screen, (0,0,0), pipe)

    # Floor
    draw_floor()

    pygame.display.update()
    clock.tick(120)