import constants
import pygame


class Penguin:
    def __init__(self):
        self.front_sprites = []
        self.left_sprites = []
        self.back_sprites = []
        self.still_front_sprites = []
        self.still_back_sprites = []
        self.num_sprites = constants.penguin['num_sprites']
        for i in range(self.num_sprites):
            self.front_sprites.append(pygame.image.load('sprites/penguin_front_walk/sprite_' + str(i) + '.png'))
            self.left_sprites.append(pygame.image.load('sprites/penguin_left_walk/sprite_' + str(i) + '.png'))
            self.back_sprites.append(pygame.image.load('sprites/penguin_back_walk/sprite_' + str(i) + '.png'))
            self.still_front_sprites.append(pygame.image.load('sprites/penguin_front_still/sprite_' + str(i) + '.png'))
            self.still_back_sprites.append(pygame.image.load('sprites/penguin_back_still/sprite_' + str(i) + '.png'))
        self.x = constants.penguin['start_x']
        self.y = constants.penguin['start_y']
        self.x_dir = 0
        self.y_dir = 0
        self.facing_up = False
        self.facing_left = False
        self.sprite_frame = 0
        self.animation_count = 0

    def move(self):
        self.x += self.x_dir
        self.y += self.y_dir
        self.animation_count += 1
        if self.animation_count > 3:
            self.animation_count = 0
            self.sprite_frame = (self.sprite_frame + 1) % self.num_sprites


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
        self.building_num = constants.factories[name]['bldg_num']
        self.num_product = 0
        self.fuel1 = 0
        self.fuel2 = 0
        self.fuel1_type = constants.factories[name]['fuel1_type']
        self.fuel2_type = constants.factories[name]['fuel2_type']
        self.level = 0
        self.on = False
        self.animation_rate = constants.factories[name]['animation_rate']
        self.sprite_frame = 0
        self.num_sprites = len(self.on_sprites)

    def produce(self):
        self.num_product += 1

    def upgrade(self, amount):
        self.level += amount

    def flip_switch(self):
        self.on = not self.on
        self.sprite_frame = 0

    def animate(self, animation_count):
        if self.on:
            self.sprite_frame = (animation_count // self.animation_rate) % self.num_sprites
