import constants
import pygame
import random


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
        if ((self.x_spd < 0 and self. x + 5 > 0) and self.key_left) or \
                ((self.x_spd > 0 and self.x + 15 < constants.game['grid_size'][0]) and self.key_right):
            self.x += self.x_spd
        if (self.y_spd < 0 and self.y > 0 and self.key_up) or \
                (self.y_spd > 0 and self.y + 15 < constants.game['grid_size'][1] and self.key_down):
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
        # Basic/positional data
        self.x = constants.factories[name]['x_coord']
        self.y = constants.factories[name]['y_coord']
        self.grid_pos = constants.factories[name]['grid_pos']
        self.building_num = constants.factories[name]['bldg_num']
        self.special = constants.factories[name]['special']

        # Fuel/product resource quantities and data
        self.product = 0
        self.fuel1 = 0
        self.fuel2 = 0
        self.product_type = constants.factories[name]['product']
        self.fuel1_type = constants.factories[name]['fuel1_type']
        self.fuel2_type = constants.factories[name]['fuel2_type']
        self.fuel1_ipo = constants.factories[name]['fuel1_ipo']
        self.fuel2_ipo = constants.factories[name]['fuel2_ipo']

        # Upgrade information, production operation info, and production multipliers
        self.ops_per_tick = 1
        self.opt_add = constants.factories[name]['ops_per_tick_add']
        self.upgrade_multiplier = constants.factories[name]['upgrade_mult']
        self.upgrade_type1 = constants.factories[name]['upgrade_type1']
        self.upgrade_type2 = constants.factories[name]['upgrade_type2']
        self.upgrade_cost1 = constants.factories[name]['upgrade_cost1']
        self.upgrade_cost2 = constants.factories[name]['upgrade_cost2']
        self.level = 1

        # Pixel offsets for level displayed on building
        self.numY_offset = constants.factories[name]['numY_offset']
        self.num1_offset = constants.factories[name]['num1_offset']
        self.num2_offset = constants.factories[name]['num2_offset']
        self.num3_offset = constants.factories[name]['num3_offset']

        # Animation data
        self.off_sprites = []
        self.on_sprites = []
        for i in range(constants.factories[name]['num_off_sprites']):
            self.off_sprites.append(pygame.image.load('sprites/' + name + '/off/sprite_' + str(i) + '.png'))
        for j in range(constants.factories[name]['num_on_sprites']):
            self.on_sprites.append(pygame.image.load('sprites/' + name + '/on/sprite_' + str(j) + '.png'))
        self.on = False
        self.animation_rate = constants.factories[name]['animation_rate']
        self.sprite_frame = 0
        self.num_sprites = len(self.on_sprites)

    def produce(self):
        if self.level >= 1:
            if self.fuel2_type == -1:
                if self.fuel1 >= self.fuel1_ipo * self.ops_per_tick:
                    self.fuel1 -= self.fuel1_ipo * self.ops_per_tick
                    self.product += self.ops_per_tick
                    self.on = True
                else:
                    self.on = False
                    self.sprite_frame = 0
            elif self.fuel1 >= self.fuel1_ipo * self.ops_per_tick and self.fuel2 >= self.fuel1_ipo * self.ops_per_tick:
                self.fuel1 -= self.fuel1_ipo * self.ops_per_tick
                self.fuel2 -= self.fuel2_ipo * self.ops_per_tick
                self.product += self.ops_per_tick
                self.on = True
            else:
                self.on = False
                self.sprite_frame = 0

    def upgrade(self, amount):
        self.ops_per_tick += self.opt_add * amount
        self.level += amount
        self.upgrade_cost1 *= pow(self.upgrade_multiplier, amount)
        self.upgrade_cost2 *= pow(self.upgrade_multiplier, amount)

    def flip_switch(self):
        self.on = not self.on
        self.sprite_frame = 0

    def animate(self, animation_count):
        if self.on:
            self.sprite_frame = (animation_count // self.animation_rate) % self.num_sprites


class ResourceManager:
    def __init__(self):
        self.resources = []
        self.unbuilt = []
        for fact in constants.factories.values():
            self.unbuilt.append(fact['grid_pos'])
        self.can_build = []
        self.can_build.append(constants.factories['wheat_farm']['grid_pos'])
        self.sign = pygame.image.load('sprites/tiles/for_sale_sign.png')

    def increase(self, resource, amount):
        self.resources[resource] += amount

    def decrease(self, resource, amount):
        self.resources[resource] -= amount

    def save(self):
        pass


class Fishing:
    def __init__(self):
        self.shiner_chance = constants.fishing['shiner_chance']
        self.blenny_chance = constants.fishing['blenny_chance']
        self.guppy_chance = constants.fishing['guppy_chance']
        self.angel_chance = constants.fishing['angel_chance']
        self.jelly_chance = constants.fishing['jelly_chance']
        self.trophy_chance = 0.0

        self.catch_quantity = 1
        self.cereal_mult = 1
        self.lure_mult = 1
        self.line_mult = 1

    def catch(self, with_rod):
        x = random.random()*100
        if x < self.shiner_chance:
            return 1
        elif x < self.shiner_chance + self.blenny_chance:
            return 2
        elif x < self.shiner_chance + self.blenny_chance + self.guppy_chance:
            return 3
        elif x < self.shiner_chance + self.blenny_chance + self.guppy_chance + self.angel_chance:
            return 4
        elif x < self.shiner_chance + self.blenny_chance + self.guppy_chance + self.angel_chance + self.jelly_chance:
            return 5
        else:
            if with_rod:
                return 6
            return 5

    def increase_odds(self, fish, amt):
        if fish == 1:
            self.shiner_chance += amt
            self.blenny_chance -= amt * 5 / 12
            self.guppy_chance -= amt * 5 / 12
            self.angel_chance -= amt / 12
            self.jelly_chance -= amt / 12
        elif fish == 2:
            self.shiner_chance -= amt * 5 / 12
            self.blenny_chance += amt
            self.guppy_chance -= amt * 5 / 12
            self.angel_chance -= amt / 12
            self.jelly_chance -= amt / 12
        elif fish == 3:
            self.shiner_chance -= amt * 5 / 12
            self.blenny_chance -= amt * 5 / 12
            self.guppy_chance += amt
            self.angel_chance -= amt / 12
            self.jelly_chance -= amt / 12
        elif fish == 4:
            self.shiner_chance -= amt * 5 / 16
            self.blenny_chance -= amt * 5 / 16
            self.guppy_chance -= amt * 5 / 16
            self.angel_chance += amt
            self.jelly_chance -= amt / 16
        elif fish == 5:
            self.shiner_chance -= amt * 5 / 16
            self.blenny_chance -= amt * 5 / 16
            self.guppy_chance -= amt * 5 / 16
            self.angel_chance -= amt / 16
            self.jelly_chance += amt
        elif fish == 6:
            self.shiner_chance -= amt / 5
            self.blenny_chance -= amt / 5
            self.guppy_chance -= amt / 5
            self.angel_chance -= amt / 5
            self.jelly_chance -= amt / 5
            self.trophy_chance += amt

    def check_negative(self):
        if self.shiner_chance < 0:
            self.increase_odds(1, abs(self.shiner_chance))
        if self.blenny_chance < 0:
            self.increase_odds(2, abs(self.blenny_chance))
        if self.guppy_chance < 0:
            self.increase_odds(3, abs(self.guppy_chance))
        if self.angel_chance < 0:
            self.increase_odds(4, abs(self.angel_chance))
        if self.jelly_chance < 0:
            self.increase_odds(5, abs(self.jelly_chance))
