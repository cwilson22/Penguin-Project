import pygame
import sys
from pygame import FULLSCREEN


class Factory:
    def __init__(self, x, y, num_sprites, name):
        self.sprites = []
        for i in range(num_sprites):
            self.sprites.append(pygame.image.load('sprites/' + name + '/sprite_' + str(i) + '.png'))
        self.x = x
        self.y = y
        self.num_product = 0

    def produce(self):
        self.num_product += 1


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
        self.animation_count += 1  # abs(self.x_dir) + abs(self.y_dir)
        if self.animation_count > 3:
            self.animation_count = 0
            self.sprite_frame = (self.sprite_frame + 1) % self.num_sprites


clock = pygame.time.Clock()
GRASS = pygame.image.load('sprites/grass.png')
PLAYER = Penguin(0, 0, 4)
GRID_SIZE = (160, 128)
WHEAT = Factory(90, 90, 1, "wheat_factory")
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
game_surface = pygame.Surface(GRID_SIZE)
screen_width = screen.get_width()
screen_height = screen.get_height()
smallest_side = min(4*screen_width/5, screen_height)
screen_surface = pygame.Surface((5*smallest_side//4, smallest_side))


def blit_screen(game_height):
    for x in range(0, game_height[0], 32):
        for y in range(0, game_height[1], 32):
            game_surface.blit(GRASS, (x, y))

    game_surface.blit(WHEAT.sprites[0], (WHEAT.x, WHEAT.y))

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

    pygame.transform.scale(game_surface, (5*smallest_side//4, smallest_side), screen_surface)

    screen.blit(screen_surface, ((screen_width - 5*smallest_side/4) // 2, (screen_height - smallest_side) // 2))
    pygame.display.flip()


if __name__ == '__main__':
    blit_screen(GRID_SIZE)
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    PLAYER.y_dir -= 1
                elif event.key == pygame.K_s:
                    PLAYER.y_dir += 1
                elif event.key == pygame.K_a:
                    PLAYER.x_dir -= 1
                elif event.key == pygame.K_d:
                    PLAYER.x_dir += 1
        PLAYER.move()
        blit_screen(GRID_SIZE)
        clock.tick(10)
