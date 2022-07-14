import pygame, sys
from settings import *
from player import Player

# Basic setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

# Groups
all_sprites = pygame.sprite.Group()

# Sprites
player = Player((600,400),all_sprites)

# Game loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Delta time
    dt = clock.tick() / 1000

    # draw a bg
    display_surface.fill('black')

    # Update
    all_sprites.update(dt)

    # Draw
    all_sprites.draw(display_surface)

    # Update the display_surface -> drawing the frame
    pygame.display.update()