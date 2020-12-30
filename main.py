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

background_sf = pygame.image.load("sprites/background-day.png").convert()
floor_sf = pygame.image.load("sprites/base.png").convert()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.blit(background_sf, (0,0))
    draw_floor()

    pygame.display.update()
    clock.tick(120)