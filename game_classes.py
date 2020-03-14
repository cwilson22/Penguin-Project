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
        self.x_offset = constants.penguin['center_px_x_offset']
        self.y_offset = constants.penguin['center_px_y_offset']
        self.x_spd = 0
        self.y_spd = 0
        self.key_up = False
        self.key_down = False
        self.key_left = False
        self.key_right = False
        self.facing_up = False
        self.facing_left = False
        self.sprite_frame = 0
        self.animation_count = 0

    def move(self):
        if self.key_left:
            self.x_spd -= 0.4
        if self.key_right:
            self.x_spd += 0.4
        if self.key_up:
            self.y_spd -= 0.32
        if self.key_down:
            self.y_spd += 0.32
        if ((self.x_spd < 0 and self. x + 5 > 0) and self.key_left) or ((self.x_spd > 0 and self.x + 15 < constants.game['grid_size'][0]) and self.key_right):
            self.x += self.x_spd
        if (self.y_spd < 0 and self.y > 5 and self.key_up) or (self.y_spd > 0 and self.y + 15 < constants.game['grid_size'][1] - 5 and self.key_down):
            self.y += self.y_spd
        self.x_spd *= 0.76
        self.y_spd *= 0.76
        self.animation_count += 1
        if self.animation_count > 4:
            self.animation_count = 0
            self.sprite_frame = (self.sprite_frame + 1) % self.num_sprites

    def calculate_tile(self):
        return (self.x + self.x_offset) // constants.game['tile_size'] + constants.game['num_tiles'][0] \
               * ((self.y + self.y_offset) // constants.game['tile_size'])

    def stop(self):
        self.x_spd = 0
        self.y_spd = 0
        self.key_right = False
        self.key_left = False
        self.key_down = False
        self.key_up = False


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
        self.operation1 = True
        self.num_product1 = 0
        self.num_product2 = 0
        self.fuel1 = 0
        self.fuel2 = 0
        self.fuel1_type = constants.factories[name]['fuel1_type']
        self.fuel2_type = constants.factories[name]['fuel2_type']
        self.fuel1_ipo = constants.factories[name]['fuel1_ipo']
        self.fuel2_ipo = constants.factories[name]['fuel2_ipo']
        self.level = 1
        self.numY_offset = constants.factories[name]['numY_offset']
        self.num1_offset = constants.factories[name]['num1_offset']
        self.num2_offset = constants.factories[name]['num2_offset']
        self.num3_offset = constants.factories[name]['num3_offset']
        self.on = False
        self.animation_rate = constants.factories[name]['animation_rate']
        self.sprite_frame = 0
        self.num_sprites = len(self.on_sprites)

    def produce(self):
        if self.operation1 and self.fuel1 >= self.fuel1_ipo:
            self.fuel1 -= self.fuel1_ipo
            self.num_product1 += 1
        elif self.fuel2 >= self.fuel1_ipo:
            self.fuel2 -= self.fuel2_ipo
            self.num_product2 += 1

    def upgrade(self, amount):
        self.level += amount

    def switch_operation(self):
        self.operation1 = not self.operation1

    def flip_switch(self):
        self.on = not self.on
        self.sprite_frame = 0

    def animate(self, animation_count):
        if self.on:
            self.sprite_frame = (animation_count // self.animation_rate) % self.num_sprites


class ResourceManager:
    def __init__(self):
        self.resources = []
        self.can_build = []
        for fact in constants.factories.values():
            self.can_build.append(fact['grid_pos'])

    def increase(self, resource, amount):
        self.resources[resource] += amount

    def decrease(self, resource, amount):
        self.resources[resource] -= amount

    def save(self):
        pass
