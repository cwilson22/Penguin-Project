game = {'grid_size': (192, 128), 'num_tiles': (6, 4), 'tile_size': 32, 'animate_ct': 6, 'game_fps': 18,
        'dirt_spots': [1, 2, 3, 4, 5, 11, 17, 19, 20, 21, 22, 23],
        'special': {0: 0, 6: 1, 7: 2, 12: 3, 13: 4, 18: 5},
        'numberX_locations_top': [21, 54, 84, 115, 148, 180], 'numberY_location_top': 1,
        'numberX_locations_bottom': [19, 52, 83, 117, 150, 182], 'numberY_location_bottom': 122,
        'overlay1_resources': [10, 11, 12, 13, 14, 20], 'overlay2_resources': [0, 1, 3, 2, 4, 8]}

penguin = {'start_x': 85, 'start_y': 55, 'center_px_x_offset': 9, 'center_px_y_offset': 10, 'num_sprites': 4}

resources = ['0wheat', '1silk', '2metal', '3sand', '4oil', '5line', '6nets', '7cereal', '8plastic', '9lures',
             '10shiners', '11blennies', '12guppies', '13angels', '14jellies', '15blue_orbs', '16pink_orbs',
             '17green_orbs', '18yellow_orbs', '19purple_orbs', '20trophies']

construct_menu = {'offset_x': 108, 'offset1': 64, 'offset2': 71, 'offset3': 78, 'offset4': 85,
                  'resources': [2, 4, 13, 14]}

factories = {
    'cereal_factory': dict(name='cereal_factory', bldg_num=1,
                           build_cost1=100, build_cost2=100, build_cost3=0, build_cost4=0,
                           num_on_sprites=4, num_off_sprites=1, animation_rate=2,
                           x_coord=2, y_coord=34, grid_pos=3,
                           fuel1_type=0, fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30,
                           numY_offset=18, num1_offset=13, num2_offset=17, num3_offset=21,
                           product1=7, product2=8, product3=-1,
                           upgrade_mult=1.05, upgrade_cost1=10, upgrade_cost2=10, upgrade_type1=3, upgrade_type2=4,
                           ops_per_tick_add=0.5,
                           build_next=['net_weaver']
                           ),
    'fishing_hut': dict(name='fishing_hut', bldg_num=2,
                        build_cost1=100, build_cost2=100, build_cost3=100, build_cost4=0,
                        num_on_sprites=1, num_off_sprites=1, animation_rate=2,
                        x_coord=20, y_coord=20, grid_pos=0,
                        fuel1_type=2, fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30,
                        numY_offset=18, num1_offset=13, num2_offset=17, num3_offset=21,
                        product1=-1, product2=-1, product3=-1,
                        upgrade_mult=1.05,
                        ops_per_tick_add=0.5,
                        build_next=[]
                        ),
    'net_weaver': dict(name='net_weaver', bldg_num=3,
                       build_cost1=100, build_cost2=100, build_cost3=0, build_cost4=100,
                       num_on_sprites=1, num_off_sprites=1, animation_rate=2,
                       x_coord=20, y_coord=20, grid_pos=11,
                       fuel1_type=2, fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30,
                       numY_offset=18, num1_offset=13, num2_offset=17, num3_offset=21,
                       product1=5, product2=6, product3=-1,
                       upgrade_mult=1.05,
                       ops_per_tick_add=0.4,
                       build_next=[]
                       ),
    'auto_producer': dict(name='auto_producer', bldg_num=4,
                          build_cost1=100, build_cost2=100, build_cost3=100, build_cost4=100,
                          num_on_sprites=1, num_off_sprites=1, animation_rate=2,
                          x_coord=36, y_coord=5, grid_pos=1,
                          fuel1_type=12, fuel2_type=1, fuel1_ipo=2, fuel2_ipo=30,
                          numY_offset=18, num1_offset=13, num2_offset=17, num3_offset=21,
                          product1=0, product2=1, product3=-1,
                          upgrade_mult=1.05, upgrade_cost1=10, upgrade_cost2=10, upgrade_type1=3, upgrade_type2=4,
                          ops_per_tick_add=0.2,
                          build_next=['cereal_factory', 'auto_miner']
                          ),
    'lure_maker': dict(name='lure_maker', bldg_num=5,
                       build_cost1=130, build_cost2=100, build_cost3=12, build_cost4=1,
                       num_on_sprites=1, num_off_sprites=1, animation_rate=2,
                       x_coord=20, y_coord=20, grid_pos=20,
                       fuel1_type=12, fuel2_type=10, fuel1_ipo=30, fuel2_ipo=30,
                       numY_offset=18, num1_offset=13, num2_offset=17, num3_offset=21,
                       product1=9, product2=-1, product3=-1,
                       upgrade_mult=1.05,
                       ops_per_tick_add=0.5,
                       build_next=[]
                       ),
    'auto_miner': dict(name='auto_miner', bldg_num=6,
                       build_cost1=130, build_cost2=100, build_cost3=13, build_cost4=14,
                       num_on_sprites=1, num_off_sprites=1, animation_rate=2,
                       x_coord=20, y_coord=20, grid_pos=4,
                       fuel1_type=12, fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30,
                       numY_offset=18, num1_offset=13, num2_offset=17, num3_offset=21,
                       product1=3, product2=2, product3=4,
                       upgrade_mult=1.05,
                       ops_per_tick_add=0.5,
                       build_next=['glassblower', 'lure_maker']
                       ),
    'glassblower': dict(name='glassblower', bldg_num=7,
                        build_cost1=130, build_cost2=100, build_cost3=10, build_cost4=1,
                        num_on_sprites=1, num_off_sprites=1, animation_rate=2,
                        x_coord=20, y_coord=20, grid_pos=22,
                        fuel1_type=1, fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30,
                        numY_offset=18, num1_offset=13, num2_offset=17, num3_offset=21,
                        upgrade_mult=1.05,
                        ops_per_tick_add=0.5,
                        build_next=[]
                        ),
}

fishing = dict(
    shiner_chance=30, blenny_chance=30, guppy_chance=30, angel_chance=5, jelly_chance=5,

)
