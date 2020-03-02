import pygame
import sys
from pygame import FULLSCREEN
import constants
import pygameMenu
import pygame.font


class Factory:
    def __init__(self, name):
        self.off_sprites = []
        self.on_sprites = []
        for i in range(constants.factories[name]['num_off_sprites']):
            self.off_sprites.append(pygame.image.load('sprites/' + name + '/off/sprite_' + str(i) + '.png'))
        for j in range(constants.factories[name]['num_on_sprites']):
            self.on_sprites.append(pygame.image.load('sprites/' + name + '/on/sprite_' + str(j) + '.png'))
        self.x = constants.factories[name]['x_coord']
        self.y = constants.factories[name]['y_coord']
        self.grid_pos = constants.factories[name]['grid_pos']
        self.num_product = 0
        self.fuel1 = 0
        self.fuel2 = 0
        self.on = False
        self.sprite_frame = 0
        self.num_sprites = len(self.on_sprites)

    def produce(self):
        self.num_product += 1

    def flip_switch(self):
        self.on = not self.on
        self.sprite_frame = 0

    def animate(self, animation_count):
        if self.on:
            self.sprite_frame = animation_count % self.num_sprites


class Penguin:
    def __init__(self, x, y, num_sprites):
        self.front_sprites = []
        self.left_sprites = []
        self.back_sprites = []
        self.still_front_sprites = []
        self.still_back_sprites = []
        for i in range(num_sprites):
            self.front_sprites.append(pygame.image.load('sprites/penguin_front_walk/sprite_' + str(i) + '.png'))
            self.left_sprites.append(pygame.image.load('sprites/penguin_left_walk/sprite_' + str(i) + '.png'))
            self.back_sprites.append(pygame.image.load('sprites/penguin_back_walk/sprite_' + str(i) + '.png'))
            self.still_front_sprites.append(pygame.image.load('sprites/penguin_front_still/sprite_' + str(i) + '.png'))
            self.still_back_sprites.append(pygame.image.load('sprites/penguin_back_still/sprite_' + str(i) + '.png'))
        self.x = x
        self.y = y
        self.x_dir = 0
        self.y_dir = 0
        self.facing_up = False
        self.facing_left = False
        self.sprite_frame = 0
        self.animation_count = 0
        self.num_sprites = num_sprites

    def move(self):
        self.x += self.x_dir
        self.y += self.y_dir
        self.animation_count += 1
        if self.animation_count > 3:
            self.animation_count = 0
            self.sprite_frame = (self.sprite_frame + 1) % self.num_sprites


def bg_pass():
    pass


pygame.init()
GAME_STATE = 0
clock = pygame.time.Clock()
GRASS = pygame.image.load('sprites/tiles/tile_dirt.png')
TILES = []
for i in range(1, 6):
    TILES.append(pygame.image.load('sprites/tiles/tile_' + str(i) + '.png'))
PLAYER = Penguin(0, 0, 4)
GRID_SIZE = (160, 128)

WHEAT = Factory("cereal_factory")
WHEAT.flip_switch()

screen = pygame.display.set_mode((0, 0), FULLSCREEN)
game_surface = pygame.Surface(GRID_SIZE)
screen_width = screen.get_width()
screen_height = screen.get_height()
smallest_side = min(4 * screen_width / 5, screen_height)
screen_surface = pygame.Surface((5 * smallest_side // 4, smallest_side))
OBJECTS = [WHEAT]


def blit_screen(game_height, animation_timer):
    for x in range(0, game_height[0], 32):
        for y in range(0, game_height[1], 32):
            game_surface.blit(GRASS, (x, y))
    for i in range(1, 6):
        game_surface.blit(TILES[i-1], (32*(i-1), 0))

    for game_object in OBJECTS:
        game_object.animate(animation_timer)
        if game_object.on:
            game_surface.blit(game_object.on_sprites[game_object.sprite_frame], (game_object.x, game_object.y))
        else:
            game_surface.blit(game_object.off_sprites[game_object.sprite_frame], (game_object.x, game_object.y))

    if PLAYER.y_dir == 0 and PLAYER.x_dir == 0:
        if PLAYER.facing_up:
            game_surface.blit(PLAYER.still_back_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
        else:
            game_surface.blit(PLAYER.still_front_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
    elif PLAYER.y_dir < 0:
        game_surface.blit(PLAYER.back_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
    elif PLAYER.x_dir < 0:
        game_surface.blit(PLAYER.left_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
    else:
        game_surface.blit(PLAYER.front_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))

    pygame.transform.scale(game_surface, (5 * smallest_side // 4, smallest_side), screen_surface)

    screen.blit(screen_surface, ((screen_width - 5 * smallest_side / 4) // 2, (screen_height - smallest_side) // 2))
    pygame.display.flip()


def main():
    animation_frame = 0
    blit_screen(GRID_SIZE, 0)
    simple_menu = pygameMenu.TextMenu(screen, window_width=screen_width, window_height=screen_height,
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
                    for ob in OBJECTS:
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
        if animation_frame > 3:
            animation_frame = 0
        clock.tick(15)


if __name__ == '__main__':
    main()
