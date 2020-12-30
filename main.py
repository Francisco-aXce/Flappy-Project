import pygame, sys

def draw_floor():
    global floor_x_pos
    screen.blit(floor_sf, (floor_x_pos,450))
    screen.blit(floor_sf, (floor_x_pos+SCREEN_SIZE[0],450))
    floor_x_pos -= 1
    if floor_x_pos <= -SCREEN_SIZE[0]:
        floor_x_pos = 0

pygame.init()
SCREEN_SIZE = (288,512)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Variables
floor_x_pos = 0
gravity = 0.15
bird_movement = 0
jump_force = 5.5

background_sf = pygame.image.load("sprites/background-day.png").convert()
floor_sf = pygame.image.load("sprites/base.png").convert()
bird_sf = pygame.image.load("sprites/yellowbird-midflap.png").convert()
bird_rect = bird_sf.get_rect(center = (50, 256))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= jump_force

    bird_movement += gravity
    bird_rect.centery += round(bird_movement)
    
    screen.blit(background_sf, (0,0))
    screen.blit(bird_sf, bird_rect.center)
    draw_floor()

    pygame.display.update()
    clock.tick(120)