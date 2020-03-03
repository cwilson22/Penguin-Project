import pygame
import sys
from pygame import FULLSCREEN
import game_classes
import constants
import pygameMenu
import pygame.font


pygame.init()

# Initialize constants
GRID_SIZE = constants.game['grid_size']
CLOCK = pygame.time.Clock()
GRASS = pygame.image.load('sprites/tiles/tile_dirt.png')
NUM_TILES = constants.game['num_tiles']
TILE_SIZE = constants.game['tile_size']
ANIMATION_MAX_CT = constants.game['animate_ct']
TILES = []
for k in range(1, 6):
    TILES.append(pygame.image.load('sprites/tiles/tile_' + str(k) + '.png'))

# Initialize player and starting buildings
PLAYER = game_classes.Penguin()
WHEAT = game_classes.Factory('cereal_factory')

# Set up screen surfaces
SCREEN = pygame.display.set_mode((0, 0), FULLSCREEN)
GAME_SURFACE = pygame.Surface(GRID_SIZE)
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()
SMALLEST_SIDE = min(NUM_TILES[1] * SCREEN_WIDTH / NUM_TILES[0], SCREEN_HEIGHT)
SCREEN_SURFACE = pygame.Surface((NUM_TILES[0] * SMALLEST_SIDE // NUM_TILES[1], SMALLEST_SIDE))
GAME_OBJECTS = [WHEAT]


def blit_screen(game_size, animation_timer):
    for x in range(0, game_size[0], TILE_SIZE):
        for y in range(0, game_size[1], TILE_SIZE):
            GAME_SURFACE.blit(GRASS, (x, y))
    for i in range(5):
        GAME_SURFACE.blit(TILES[i], (32 * i, 0))

    for game_object in GAME_OBJECTS:
        game_object.animate(animation_timer)
        if game_object.on:
            GAME_SURFACE.blit(game_object.on_sprites[game_object.sprite_frame], (game_object.x, game_object.y))
        else:
            GAME_SURFACE.blit(game_object.off_sprites[game_object.sprite_frame], (game_object.x, game_object.y))

    if PLAYER.y_dir == 0 and PLAYER.x_dir == 0:
        if PLAYER.facing_up:
            GAME_SURFACE.blit(PLAYER.still_back_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
        else:
            GAME_SURFACE.blit(PLAYER.still_front_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
    elif PLAYER.y_dir < 0:
        GAME_SURFACE.blit(PLAYER.back_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
    elif PLAYER.x_dir < 0:
        GAME_SURFACE.blit(PLAYER.left_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
    else:
        GAME_SURFACE.blit(PLAYER.front_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))

    pygame.transform.scale(GAME_SURFACE, (NUM_TILES[0] * SMALLEST_SIDE // NUM_TILES[1], SMALLEST_SIDE), SCREEN_SURFACE)

    SCREEN.blit(SCREEN_SURFACE, ((SCREEN_WIDTH - NUM_TILES[0] * SMALLEST_SIDE / NUM_TILES[1]) // 2,
                                 (SCREEN_HEIGHT - SMALLEST_SIDE) // 2))
    pygame.display.flip()


def bg_pass():
    pass


def main():
    animation_frame = 0
    blit_screen(GRID_SIZE, 0)
    simple_menu = pygameMenu.TextMenu(SCREEN, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
                                      font=pygameMenu.font.FONT_8BIT, font_color=(255, 255, 255), enabled=False,
                                      font_size=20, title='Test', bgfun=bg_pass, menu_alpha=100,
                                      onclose=pygameMenu.events.CLOSE, option_shadow=False, menu_color=(0, 0, 0),
                                      menu_width=600, menu_height=600)
    simple_menu.set_fps(15)
    simple_menu.add_option('Close', pygameMenu.events.CLOSE)
    simple_menu.add_option('Exit', pygameMenu.events.EXIT)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    PLAYER.facing_up = True
                    PLAYER.facing_left = False
                    PLAYER.y_dir += 1
                if event.key == pygame.K_s:
                    PLAYER.facing_up = False
                    PLAYER.facing_left = False
                    PLAYER.y_dir -= 1
                if event.key == pygame.K_a:
                    PLAYER.facing_left = True
                    PLAYER.facing_up = False
                    PLAYER.x_dir += 1
                if event.key == pygame.K_d:
                    PLAYER.facing_left = False
                    PLAYER.facing_up = False
                    PLAYER.x_dir -= 1
                if event.key == pygame.K_SPACE:
                    for ob in GAME_OBJECTS:
                        if PLAYER.x // 32 + 5 * (PLAYER.y // 32) == ob.grid_pos:
                            ob.flip_switch()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    simple_menu.enable()
                    PLAYER.x_dir = 0
                    PLAYER.y_dir = 0
                if event.key == pygame.K_w:
                    PLAYER.y_dir -= 1
                elif event.key == pygame.K_s:
                    PLAYER.y_dir += 1
                elif event.key == pygame.K_a:
                    PLAYER.x_dir -= 1
                elif event.key == pygame.K_d:
                    PLAYER.x_dir += 1

        PLAYER.move()
        blit_screen(GRID_SIZE, animation_frame)
        simple_menu.mainloop()
        animation_frame += 1
        if animation_frame > ANIMATION_MAX_CT:
            animation_frame = 0
        CLOCK.tick(15)


if __name__ == '__main__':
    main()
