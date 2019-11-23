from graphics import *


def build_id_lists(ids, large_size):
    normal_tile_ids = {}
    large_tile_ids = {}
    for i in list(ids.items()):
        norm_img = Image(Point(0, 0), i[1])
        norm_img.img = norm_img.rescale(64)
        large_img = Image(Point(0, 0), i[1])
        large_img.img = large_img.rescale(large_size)
        normal_tile_ids[i[0]] = norm_img
        large_tile_ids[i[0]] = large_img
    return normal_tile_ids, large_tile_ids


def build_matrix(width, height):
    row = []
    matrix = []
    for i in range(0, width):
        row.append(0)
    for i in range(0, height):
        matrix.append(row)
    return matrix


# return tilemap, colliders, normal_tile_ids, large_tile_ids, start, movement_speed

def test(large_size):
    # Worldmap that tells 'draw_tilemap' what to render and where
    tilemap = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
               [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
               [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0],
               [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
               [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # Worldmap that tells 'draw_tilemap' how to render the decoration layer.
    # In this case, the 'build_matrix' function is used to create a blank decomap.
    decomap = build_matrix(len(tilemap[0]), len(tilemap))
    
    # Setup tile images for both regular and fullscreen.
    # To handle broken ids in the tilemap, the 'missing' tile has been omitted from these dictionaries and placed in the root script.
    tile_dict = {1: 'tiles/block.png'}
    deco_dict = {}
    normal_tile_ids, large_tile_ids = build_id_lists(tile_dict, large_size)
    normal_deco_ids, large_deco_ids = build_id_lists(deco_dict, large_size)

    # List of blocks that will be solid
    colliders = [1]

    # Basic player setup
    start = (0, 0)
    movement_speed = 3
    
    return start, movement_speed, colliders, tilemap, decomap, normal_tile_ids, large_tile_ids, normal_deco_ids, large_deco_ids

def house(large_size):
    tilemap = [[16, 16, 16, 16, 16, 39, 20, 9, 22, 9, 9, 9, 21, 21, 21, 21],
               [16, 16, 16, 16, 16, 17, 9, 9, 9, 10, 11, 11, 11, 11, 10, 9],
               [16, 16, 16, 16, 16, 20, 21, 21, 9, 10, 8, 8, 8, 8, 10, 9],
               [16, 39, 19, 19, 20, 9, 21, 21, 9, 10, 8, 8, 8, 8, 10, 21],
               [19, 20, 24, 25, 26, 9, 9, 21, 9, 11, 11, 11, 8, 11, 11, 9],
               [9, 9, 27, 28, 33, 25, 25, 25, 25, 25, 25, 36, 28, 29, 9, 9],
               [21, 21, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 29, 9, 9],
               [9, 9, 30, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 32, 9, 22],
               [21, 9, 9, 9, 9, 9, 9, 9, 21, 21, 9, 9, 9, 9, 9, 9],
               [21, 9, 9, 9, 9, 9, 9, 9, 21, 21, 9, 9, 9, 9, 9, 9]]

    decomap = build_matrix(len(tilemap[0]), len(tilemap))

    tile_dict = {8: 'tiles/wood.png', 9: 'tiles/grass.png', 10: 'tiles/corner.png', 11: 'tiles/wall.png', 16: 'tiles/water.png', 17: 'tiles/right_water.png', 19: 'tiles/bottom_water.png', 20: 'tiles/bottom_right_water.png', 21: 'tiles/grass3.png', 22: 'tiles/grass2.png', 24: 'tiles/top_left_path.png', 25: 'tiles/top_path.png', 26: 'tiles/top_right_path.png', 27: 'tiles/left_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 30: 'tiles/bottom_left_path.png', 31: 'tiles/bottom_path.png', 32: 'tiles/bottom_right_path.png', 33: 'tiles/path_corner1.png', 36: 'tiles/path_corner4.png', 39: 'tiles/water_corner3.png'}
    deco_dict = {}
    normal_tile_ids, large_tile_ids = build_id_lists(tile_dict, large_size)
    normal_deco_ids, large_deco_ids = build_id_lists(deco_dict, large_size)

    colliders = [10, 11, 16, 17, 19, 20, 39]

    start = (64 * 0, 64 * 8)
    movement_speed = 4

    return start, movement_speed, colliders, tilemap, decomap, normal_tile_ids, large_tile_ids, normal_deco_ids, large_deco_ids

def riverside(large_size):
    tilemap = [[9, 9, 21, 9, 9, 9, 9, 12, 13, 13, 14, 9, 9, 9, 9, 22, 21, 9, 9, 9, 9, 22, 9, 21, 9, 9, 21, 9, 9, 22, 9, 9],
               [21, 9, 9, 9, 22, 9, 12, 37, 16, 16, 38, 14, 9, 9, 9, 9, 9, 9, 9, 10, 23, 23, 23, 23, 23, 10, 23, 23, 23, 23, 10, 9],
               [9, 21, 9, 9, 9, 12, 37, 16, 16, 16, 16, 38, 14, 9, 24, 25, 25, 25, 26, 10, 8, 8, 8, 8, 8, 10, 8, 8, 8, 8, 10, 9],
               [9, 9, 9, 21, 9, 15, 16, 16, 16, 16, 16, 16, 17, 9, 30, 31, 35, 28, 29, 10, 8, 8, 8, 8, 8, 10, 8, 8, 8, 8, 10, 9],
               [9, 9, 9, 21, 9, 18, 40, 16, 16, 16, 16, 16, 17, 21, 21, 21, 27, 28, 29, 10, 8, 8, 8, 8, 8, 10, 8, 8, 8, 8, 10, 9],
               [9, 22, 9, 21, 21, 9, 15, 16, 16, 16, 16, 39, 20, 9, 9, 9, 27, 28, 29, 11, 11, 11, 10, 23, 8, 23, 23, 8, 23, 23, 10, 9],
               [9, 9, 9, 9, 21, 9, 18, 40, 16, 16, 39, 20, 9, 9, 9, 9, 27, 28, 29, 9, 9, 9, 10, 8, 8, 8, 8, 8, 8, 8, 10, 9],
               [21, 21, 21, 21, 21, 9, 9, 18, 19, 19, 20, 9, 9, 21, 21, 9, 27, 28, 29, 9, 22, 9, 10, 8, 8, 8, 8, 8, 8, 8, 10, 9],
               [9, 9, 21, 21, 21, 9, 9, 9, 9, 9, 9, 9, 9, 9, 21, 9, 27, 28, 29, 21, 21, 9, 11, 11, 8, 8, 11, 11, 11, 11, 11, 9],
               [9, 9, 9, 9, 21, 21, 21, 21, 21, 21, 21, 21, 9, 9, 21, 21, 27, 28, 29, 9, 21, 9, 9, 27, 28, 28, 29, 9, 9, 21, 9, 9],
               [13, 14, 9, 9, 21, 9, 9, 9, 9, 9, 9, 21, 9, 22, 9, 9, 27, 28, 33, 25, 25, 25, 25, 36, 28, 28, 29, 9, 21, 21, 21, 9],
               [16, 38, 14, 9, 9, 9, 21, 21, 22, 9, 9, 21, 21, 9, 9, 9, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28, 29, 9, 21, 22, 9, 9],
               [16, 16, 38, 14, 9, 9, 9, 9, 9, 9, 9, 9, 21, 9, 9, 9, 30, 31, 31, 31, 31, 31, 31, 31, 31, 31, 32, 9, 9, 12, 13, 13],
               [16, 16, 16, 38, 13, 13, 13, 13, 13, 13, 14, 9, 9, 21, 9, 9, 9, 9, 9, 9, 9, 12, 13, 13, 13, 13, 13, 13, 13, 37, 16, 16],
               [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 38, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 37, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]]

    decomap = build_matrix(len(tilemap[0]), len(tilemap))
    
    tile_dict = {8: 'tiles/wood.png', 9: 'tiles/grass.png', 10: 'tiles/corner.png', 11: 'tiles/wall.png', 12: 'tiles/top_left_water.png', 13: 'tiles/top_water.png', 14: 'tiles/top_right_water.png', 15: 'tiles/left_water.png', 16: 'tiles/water.png', 17: 'tiles/right_water.png', 18: 'tiles/bottom_left_water.png', 19: 'tiles/bottom_water.png', 20: 'tiles/bottom_right_water.png', 21: 'tiles/grass3.png', 22: 'tiles/grass2.png', 23: 'tiles/pink_wall.png', 24: 'tiles/top_left_path.png', 25: 'tiles/top_path.png', 26: 'tiles/top_right_path.png', 27: 'tiles/left_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 30: 'tiles/bottom_left_path.png', 31: 'tiles/bottom_path.png', 32: 'tiles/bottom_right_path.png', 33: 'tiles/path_corner1.png', 35: 'tiles/path_corner3.png', 36: 'tiles/path_corner4.png', 37: 'tiles/water_corner1.png', 38: 'tiles/water_corner2.png', 39: 'tiles/water_corner3.png', 40: 'tiles/water_corner4.png'}
    deco_dict = {}
    normal_tile_ids, large_tile_ids = build_id_lists(tile_dict, large_size)
    normal_deco_ids, large_deco_ids = build_id_lists(deco_dict, large_size)

    colliders = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 37, 38, 39, 40]
    
    start = (64 * 0, 64 * 8)
    movement_speed = 4

    return start, movement_speed, colliders, tilemap, decomap, normal_tile_ids, large_tile_ids, normal_deco_ids, large_deco_ids


def mountain(large_size):
    tilemap = [[9, 9, 9, 9, 9, 9, 9, 9, 9, 47, 9, 9, 9, 9, 9, 24],
               [9, 9, 52, 9, 9, 9, 52, 9, 9, 47, 9, 9, 9, 52, 24, 36],
               [9, 9, 9, 9, 52, 9, 9, 9, 43, 44, 9, 9, 51, 24, 36, 28],
               [42, 43, 9, 9, 9, 9, 9, 44, 41, 41, 9, 9, 24, 36, 28, 34],
               [41, 41, 42, 43, 43, 43, 44, 41, 41, 41, 9, 24, 36, 28, 34, 32],
               [41, 41, 41, 41, 41, 41, 41, 41, 49, 50, 24, 36, 28, 34, 32, 9],
               [48, 49, 41, 41, 41, 41, 41, 50, 9, 9, 27, 28, 34, 32, 9, 9],
               [9, 9, 48, 49, 49, 49, 50, 9, 52, 9, 27, 28, 29, 9, 9, 9],
               [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 27, 28, 29, 9, 52, 9]]

    decomap = [[0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
               [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    tile_dict = {9: 'tiles/grass.png', 24: 'tiles/top_left_path.png', 27: 'tiles/left_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 32: 'tiles/bottom_right_path.png', 34: 'tiles/path_corner2.png', 36: 'tiles/path_corner4.png', 41: 'tiles/cliff.png', 42: 'tiles/cliff_top_left.png', 43: 'tiles/cliff_top.png', 44: 'tiles/cliff_top_right.png', 47: 'tiles/cliff_right.png', 48: 'tiles/cliff_bottom_left.png', 49: 'tiles/cliff_bottom.png', 50: 'tiles/cliff_bottom_right.png', 51: 'tiles/lamp_post_bottom.png', 52: 'tiles/tree_bottom.png'}
    deco_dict = {1: 'tiles/lamp_post_top.png', 2: 'tiles/tree_top.png'}
    normal_tile_ids, large_tile_ids = build_id_lists(tile_dict, large_size)
    normal_deco_ids, large_deco_ids = build_id_lists(deco_dict, large_size)

    colliders = [41, 42, 43, 44, 47, 48, 49, 50, 51, 52]

    start = (64 * 0, 64 * 8)
    movement_speed = 4

    return start, movement_speed, colliders, tilemap, decomap, normal_tile_ids, large_tile_ids, normal_deco_ids, large_deco_ids
