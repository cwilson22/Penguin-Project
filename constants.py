game = {'grid_size': (192, 128), 'num_tiles': (6, 4), 'tile_size': 32, 'animate_ct': 6, 'game_fps': 15}

penguin = {'start_x': 15, 'start_y': 15, 'center_px_x_offset': 9, 'center_px_y_offset': 10, 'num_sprites': 4}

resources = ['0wheat', '1silk', '2metal', '3sand', '4oil', '5line', '6nets', '7cereal', '8plastic', '9lures',
             '10shiners', '11blennies', '12guppies', '13angels', '14jellies', '15blue_orbs', '16pink_orbs',
             '17green_orbs', '18yellow_orbs', '19purple_orbs']

construct_menu = {'offset_x': 108, 'offset2': 64, 'offset4': 71, 'offset13': 78, 'offset14': 85,
                  'resources': [2, 4, 13, 14]}

factories = {
    'cereal_factory': dict(max_product=999, build_cost1=130, build_cost2=100, cost_type1=8, cost_type2=10,
                           num_on_sprites=4, num_off_sprites=1, x_coord=20, y_coord=20, fuel1_type=2,
                           fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30, production_rate=3, grid_pos=6,
                           animation_rate=2,
                           bldg_num=1),
    'fishing_hut': dict(max_product=999, build_cost1=130, build_cost2=100, cost_type1=10, cost_type2=10,
                        num_on_sprites=4, num_off_sprites=1, x_coord=20, y_coord=20, fuel1_type=2,
                        fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30, production_rate=3, grid_pos=6,
                        animation_rate=2,
                        bldg_num=2),
    'net_weaver': dict(max_product=999, build_cost1=130, build_cost2=100, cost_type1=1, cost_type2=1,
                       num_on_sprites=4, num_off_sprites=1, x_coord=20, y_coord=20, fuel1_type=2,
                       fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30, production_rate=3, grid_pos=6,
                       animation_rate=2,
                       bldg_num=3),
    'auto_producer': dict(max_product=999, build_cost1=100, build_cost2=100, cost_type1=2, cost_type2=13,
                          num_on_sprites=4, num_off_sprites=1, x_coord=20, y_coord=20, fuel1_type=12,
                          fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30, production_rate=3, grid_pos=2,
                          animation_rate=2,
                          bldg_num=4),
    'lure_maker': dict(max_product=999, build_cost1=130, build_cost2=100, cost_type1=12, cost_type2=1,
                       num_on_sprites=4, num_off_sprites=1, x_coord=20, y_coord=20, fuel1_type=12,
                       fuel2_type=10, fuel1_ipo=30, fuel2_ipo=30, production_rate=3, grid_pos=6,
                       animation_rate=2,
                       bldg_num=5),
    'auto_miner': dict(max_product=999, build_cost1=130, build_cost2=100, cost_type1=13, cost_type2=14,
                       num_on_sprites=4, num_off_sprites=1, x_coord=20, y_coord=20, fuel1_type=12,
                       fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30, production_rate=3, grid_pos=6,
                       animation_rate=2,
                       bldg_num=6),
    'glassblower': dict(max_product=999, build_cost1=130, build_cost2=100, cost_type1=10, cost_type2=1,
                        num_on_sprites=4, num_off_sprites=1, x_coord=20, y_coord=20, fuel1_type=1,
                        fuel2_type=1, fuel1_ipo=30, fuel2_ipo=30, production_rate=3, grid_pos=6,
                        animation_rate=2,
                        bldg_num=7),
}
