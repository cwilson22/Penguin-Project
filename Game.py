import pygame
import sys
from pygame import FULLSCREEN
import game_classes
import constants
import pygameMenu
import pygame.font
import json


pygame.init()
pygame.mouse.set_visible(False)

# Initialize constants
CLOCK = pygame.time.Clock()
NUM_TILES = constants.game['num_tiles']
GRID_SIZE = constants.game['grid_size']
GRASS = pygame.image.load('sprites/tiles/tile_grass.png')
DIRT = pygame.image.load('sprites/tiles/tile_dirt.png')
TILE_SIZE = constants.game['tile_size']
ANIMATION_MAX_CT = constants.game['animate_ct']
FPS = constants.game['game_fps']

# Initialize all images and graphics
DIRT_TILES = constants.game['dirt_spots']
SPECIAL_TILES = constants.game['special']
OVERLAY_NUMBERS_X = [constants.game['numberX_locations_top'], constants.game['numberX_locations_bottom']]
OVERLAY_NUMBERS_Y = [constants.game['numberY_location_top'], constants.game['numberY_location_bottom']]
OVERLAY_RESOURCES = [constants.game['overlay1_resources'], constants.game['overlay2_resources']]
OVERLAYS = []
for k in range(12):
    OVERLAYS.append(pygame.image.load('sprites/overlays/overlay_' + str(k) + '.png'))
TILES = []
for k in SPECIAL_TILES.keys():
    TILES.append(pygame.image.load('sprites/tiles/tile_' + str(k) + '.png'))
CONSTRUCTION_MENU = []
for k in range(4):
    CONSTRUCTION_MENU.append(pygame.image.load('text/construct/sprite_' + str(k) + '.png'))
NUMS = []
for k in range(10):
    NUMS.append(pygame.image.load('text/digits/num_' + str(k) + '.png'))

# Initialize player and buildings
PLAYER = game_classes.Penguin()
GAME_OBJECTS = []
RESOURCES = game_classes.ResourceManager()
FISHING = game_classes.Fishing()
with open('savestate.txt', 'r') as f:
    save = json.load(f)
for k in range(len(constants.resources)):
    RESOURCES.resources.append(save[str(k)])
GAME_STATE = 0

# Set up screen surfaces
SCREEN = pygame.display.set_mode((0, 0), FULLSCREEN)
GAME_SURFACE = pygame.Surface(GRID_SIZE)
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()
SMALLEST_SIDE = min(NUM_TILES[1] * SCREEN_WIDTH / NUM_TILES[0], SCREEN_HEIGHT)
SCREEN_SURFACE = pygame.Surface((NUM_TILES[0] * SMALLEST_SIDE // NUM_TILES[1], SMALLEST_SIDE))


def calc_xy(grid_pos):
    return TILE_SIZE * (grid_pos % 6), TILE_SIZE * (grid_pos // 6)


def blit_levels():
    for ob in GAME_OBJECTS:
        ct = 3
        x = ob.level
        while x > 0:
            if ct == 3:
                GAME_SURFACE.blit(NUMS[x % 10], (ob.x + ob.num3_offset, ob.y + ob.numY_offset))
            elif ct == 2:
                GAME_SURFACE.blit(NUMS[x % 10], (ob.x + ob.num2_offset, ob.y + ob.numY_offset))
            elif ct == 1:
                GAME_SURFACE.blit(NUMS[x % 10], (ob.x + ob.num1_offset, ob.y + ob.numY_offset))
            x = x // 10
            ct -= 1


def blit_overlay():
    for t in range(len(OVERLAY_RESOURCES)):
        for s in range(len(OVERLAY_RESOURCES[t])):
            GAME_SURFACE.blit(OVERLAYS[s + 6*t], (TILE_SIZE * s, t * 96))
            ct = 0
            x = int(RESOURCES.resources[OVERLAY_RESOURCES[t][s]])
            if x == 0:
                GAME_SURFACE.blit(NUMS[0], (OVERLAY_NUMBERS_X[t][s], OVERLAY_NUMBERS_Y[t]))
            else:
                while x > 0:
                    GAME_SURFACE.blit(NUMS[x % 10], (OVERLAY_NUMBERS_X[t][s] - (4*ct), OVERLAY_NUMBERS_Y[t]))
                    x = x // 10
                    ct += 1


def blit_screen(animation_timer):
    for x in range(NUM_TILES[0]):
        for y in range(NUM_TILES[1]):
            if 6 * y + x in DIRT_TILES:
                GAME_SURFACE.blit(DIRT, (TILE_SIZE * x, TILE_SIZE * y))
            elif 6 * y + x in SPECIAL_TILES.keys():
                GAME_SURFACE.blit(TILES[SPECIAL_TILES[6 * y + x]], (TILE_SIZE * x, TILE_SIZE * y))
            else:
                GAME_SURFACE.blit(GRASS, (TILE_SIZE * x, TILE_SIZE * y))

    for game_object in GAME_OBJECTS:
        game_object.animate(animation_timer)
        if game_object.on:
            GAME_SURFACE.blit(game_object.on_sprites[game_object.sprite_frame], (game_object.x, game_object.y))
        else:
            GAME_SURFACE.blit(game_object.off_sprites[game_object.sprite_frame], (game_object.x, game_object.y))

    for to_build in RESOURCES.can_build:
        GAME_SURFACE.blit(RESOURCES.sign, (calc_xy(to_build)[0] + 2, calc_xy(to_build)[1] + 22))

    blit_levels()

    if not PLAYER.key_up and not PLAYER.key_down and not PLAYER.key_left and not PLAYER.key_right:
        if PLAYER.facing_up:
            GAME_SURFACE.blit(PLAYER.still_back_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
        else:
            GAME_SURFACE.blit(PLAYER.still_front_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
    elif PLAYER.y_spd < -0.65:
        GAME_SURFACE.blit(PLAYER.back_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
    elif PLAYER.x_spd < 0:
        GAME_SURFACE.blit(PLAYER.left_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))
    else:
        GAME_SURFACE.blit(PLAYER.front_sprites[PLAYER.sprite_frame], (PLAYER.x, PLAYER.y))

    blit_overlay()

    pygame.transform.scale(GAME_SURFACE, (NUM_TILES[0] * SMALLEST_SIDE // NUM_TILES[1], SMALLEST_SIDE), SCREEN_SURFACE)

    SCREEN.blit(SCREEN_SURFACE, ((SCREEN_WIDTH - NUM_TILES[0] * SMALLEST_SIDE / NUM_TILES[1]) // 2,
                                 (SCREEN_HEIGHT - SMALLEST_SIDE) // 2))
    pygame.display.flip()


def blit_construction_menu():
    for x in range(2):
        for y in range(2):
            GAME_SURFACE.blit(CONSTRUCTION_MENU[x+2*y], (2*TILE_SIZE + x*TILE_SIZE, TILE_SIZE + y*TILE_SIZE))

    for fact in constants.factories.values():
        if PLAYER.calculate_tile() == fact['grid_pos']:
            GAME_SURFACE.blit(pygame.image.load('text/construct/numbers/' + str(fact['build_cost1']) + '.png'),
                              (constants.construct_menu['offset_x'], constants.construct_menu['offset1']))
            GAME_SURFACE.blit(pygame.image.load('text/construct/numbers/' + str(fact['build_cost2']) + '.png'),
                              (constants.construct_menu['offset_x'], constants.construct_menu['offset2']))
            GAME_SURFACE.blit(pygame.image.load('text/construct/numbers/' + str(fact['build_cost3']) + '.png'),
                              (constants.construct_menu['offset_x'], constants.construct_menu['offset3']))
            GAME_SURFACE.blit(pygame.image.load('text/construct/numbers/' + str(fact['build_cost4']) + '.png'),
                              (constants.construct_menu['offset_x'], constants.construct_menu['offset4']))
            break

    pygame.transform.scale(GAME_SURFACE, (NUM_TILES[0] * SMALLEST_SIDE // NUM_TILES[1], SMALLEST_SIDE), SCREEN_SURFACE)

    SCREEN.blit(SCREEN_SURFACE, ((SCREEN_WIDTH - NUM_TILES[0] * SMALLEST_SIDE / NUM_TILES[1]) // 2,
                                 (SCREEN_HEIGHT - SMALLEST_SIDE) // 2))
    pygame.display.flip()


def transfer_product():
    for ob in GAME_OBJECTS:
        if ob.product1 > 0:
            RESOURCES.resources[ob.product1_type] += ob.product1
            ob.product1 = 0
        if ob.product2 > 0:
            RESOURCES.resources[ob.product2_type] += ob.product2
            ob.product2 = 0


def bg_pass():
    pass


def main():
    global GAME_STATE
    animation_frame = 0
    blit_screen(0)
    simple_menu = pygameMenu.TextMenu(SCREEN, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
                                      font=pygameMenu.font.FONT_8BIT, font_color=(255, 255, 255), enabled=False,
                                      font_size=20, title='Exit', bgfun=bg_pass, menu_alpha=100,
                                      onclose=pygameMenu.events.CLOSE, option_shadow=False, menu_color=(0, 0, 0),
                                      menu_width=300, menu_height=300)
    simple_menu.set_fps(FPS)
    simple_menu.add_option('Close Menu', pygameMenu.events.CLOSE)
    simple_menu.add_option('Exit Game', pygameMenu.events.EXIT)

    while 1:
        if GAME_STATE == 0:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        PLAYER.facing_up = True
                        PLAYER.facing_left = False
                        PLAYER.key_up = False
                    if event.key == pygame.K_s:
                        PLAYER.facing_up = False
                        PLAYER.facing_left = False
                        PLAYER.key_down = False
                    if event.key == pygame.K_a:
                        PLAYER.facing_left = True
                        PLAYER.facing_up = False
                        PLAYER.key_left = False
                    if event.key == pygame.K_d:
                        PLAYER.facing_left = False
                        PLAYER.facing_up = False
                        PLAYER.key_right = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        PLAYER.key_up = True
                    elif event.key == pygame.K_s:
                        PLAYER.key_down = True
                    elif event.key == pygame.K_a:
                        PLAYER.key_left = True
                    elif event.key == pygame.K_d:
                        PLAYER.key_right = True
                    if event.key == pygame.K_q:
                        simple_menu.enable()
                        PLAYER.stop()
                    if event.key == pygame.K_z:
                        for ob in GAME_OBJECTS:
                            if PLAYER.calculate_tile() == ob.grid_pos:
                                ob.flip_switch()
                    if event.key == pygame.K_e:
                        if PLAYER.calculate_tile() in RESOURCES.unbuilt:
                            GAME_STATE = 1
                            PLAYER.stop()
                    if event.key == pygame.K_SPACE:
                        if PLAYER.calculate_tile() == 12:
                            fish = FISHING.catch()
                            if fish == 6:
                                RESOURCES.resources[20] += 1
                            else:
                                RESOURCES.resources[fish + 9] += FISHING.catch_quantity
                        else:
                            for ob in GAME_OBJECTS:
                                if PLAYER.calculate_tile() == ob.grid_pos:
                                    if ob.operation == 1:
                                        RESOURCES.resources[ob.product1] += 1
                                    elif ob.operation == 2:
                                        RESOURCES.resources[ob.product2] += 1
                                    elif ob.operation == 3:
                                        RESOURCES.resources[ob.product3] += 1
                    if event.key == pygame.K_f:
                        for ob in GAME_OBJECTS:
                            if PLAYER.calculate_tile() == ob.grid_pos:
                                ob.switch_operation()
                    if event.key == pygame.K_1:
                        for ob in GAME_OBJECTS:
                            if PLAYER.calculate_tile() == ob.grid_pos:
                                if RESOURCES.resources[ob.upgrade_type1] >= ob.upgrade_cost1 and \
                                        RESOURCES.resources[ob.upgrade_type2] >= ob.upgrade_cost2:
                                    RESOURCES.resources[ob.upgrade_type1] -= ob.upgrade_cost1
                                    RESOURCES.resources[ob.upgrade_type2] -= ob.upgrade_cost2
                                    ob.upgrade(1)
                    if event.key == pygame.K_v:
                        for ob in GAME_OBJECTS:
                            if PLAYER.calculate_tile() == ob.grid_pos:
                                if RESOURCES.resources[ob.fuel1_type] >= 50:
                                    ob.fuel1 += 50
                                    RESOURCES.resources[ob.fuel1_type] -= 50

            PLAYER.move()
            blit_screen(animation_frame)
            simple_menu.mainloop()
            for ob in GAME_OBJECTS:
                ob.produce()
            transfer_product()
            animation_frame += 1
            if animation_frame > ANIMATION_MAX_CT:
                animation_frame = 0
            if GAME_STATE == 1:
                blit_construction_menu()

        elif GAME_STATE == 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        GAME_STATE = 0
                    if event.key == pygame.K_SPACE:
                        for fact in constants.factories.values():
                            if PLAYER.calculate_tile() == fact['grid_pos']:
                                build1 = constants.construct_menu['resources'][0]
                                build2 = constants.construct_menu['resources'][1]
                                build3 = constants.construct_menu['resources'][2]
                                build4 = constants.construct_menu['resources'][3]
                                cost1 = fact['build_cost1']
                                cost2 = fact['build_cost2']
                                cost3 = fact['build_cost3']
                                cost4 = fact['build_cost4']
                                if RESOURCES.resources[build1] >= cost1 and RESOURCES.resources[build2] >= cost2 and \
                                        RESOURCES.resources[build3] >= cost3 and RESOURCES.resources[build4] >= cost4:
                                    RESOURCES.resources[build1] -= cost1
                                    RESOURCES.resources[build2] -= cost2
                                    RESOURCES.resources[build3] -= cost3
                                    RESOURCES.resources[build4] -= cost4
                                    GAME_OBJECTS.append(game_classes.Factory(fact['name']))
                                    RESOURCES.unbuilt.remove(fact['grid_pos'])
                                    RESOURCES.can_build.remove(fact['grid_pos'])
                                    for nex in fact['build_next']:
                                        RESOURCES.can_build.append(constants.factories[nex]['grid_pos'])
                                break
                        GAME_STATE = 0
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
