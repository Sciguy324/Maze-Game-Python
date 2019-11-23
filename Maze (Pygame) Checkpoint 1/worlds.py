import pygame
import os
from sprite import *

def build_id_list(tiles):
    id_list = {}
    for i in list(tiles.items()):
        img = pygame.image.load(os.path.join(i[1]))
        img = pygame.transform.scale(img, (64, 64)).convert_alpha()
        id_list[i[0]] = img
    return id_list


def build_matrix(width, height):
    row = []
    matrix = []
    for i in range(0, width):
        row.append(0)
    for i in range(0, height):
        matrix.append(row)
    return matrix


def test():
    block = pygame.image.load(os.path.join('tiles/block.png'))
    block = pygame.transform.scale(block, (64, 64)).convert()
    t_ids = {1: block}
    d_ids = {}
    colliders = [1]

    tilemap = [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
               [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
               [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
               [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0],
               [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    decomap = build_matrix(len(tilemap[0]), len(tilemap))

    start = (0, 0)

    loading_zones = {}
    
    return t_ids, tilemap, d_ids, decomap, colliders, loading_zones

def city():
    # Image setup
    tile_dict = {1: 'tiles/stone_wall.png', 2: 'tiles/wood.png', 3: 'tiles/stone_table_left.png', 4: 'tiles/stone_table_right.png', 5: 'tiles/stone_table_top.png', 6: 'tiles/stone_table_bottom.png'}
    t_ids = build_id_list(tile_dict)
    d_ids = {}

    # Identify all tiles that warrant collision
    colliders = [1, 3, 4, 5, 6]

    # Define tilemap
    city_tilemap = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
                    [1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2],
                    [1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2],
                    [1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2],
                    [1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2],
                    [1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2],
                    [1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2],
                    [1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 3, 4, 2, 1, 2, 1, 2, 1, 2],
                    [1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2],
                    [1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2],
                    [1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2],
                    [1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2],
                    [1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2],
                    [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
                    [1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
                    [1, 2, 5, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                    [1, 2, 6, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5, 2, 1],
                    [1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 6, 2, 6, 2, 6, 2, 6, 2, 6, 2, 6, 2, 1],
                    [1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                    [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    # Define decoration layer map.  In this case, it is blank so the function 'build_matrix' is used.
    city_decomap = build_matrix(len(city_tilemap[0]), len(city_tilemap))

    # Starting position of player
    start = (0, 320)

    # Regions that will cause the current level to end and a new one to start.
    loading_zones = {}
    
    return t_ids, city_tilemap, d_ids, city_decomap, colliders, loading_zones


def house():
    tile_dict = {8: 'tiles/wood.png', 9: 'tiles/grass.png', 10: 'tiles/corner.png', 11: 'tiles/wall.png', 12: 'tiles/grass2.png', 13: 'tiles/grass3.png'}
    t_ids = build_id_list(tile_dict)
    d_ids = {}

    colliders = [10, 11]

    world_tilemap = [[9, 13, 9, 9, 9, 9, 9, 9, 9, 9, 13, 13, 9, 9, 13, 9],
                     [9, 13, 9, 9, 10, 11, 11, 11, 11, 11, 11, 11, 10, 9, 12, 13],
                     [9, 13, 12, 9, 10, 8, 8, 8, 8, 8, 8, 8, 10, 9, 9, 13],
                     [13, 9, 9, 9, 10, 8, 8, 8, 8, 8, 8, 8, 10, 13, 13, 9],
                     [13, 9, 13, 9, 10, 8, 8, 8, 8, 8, 8, 8, 10, 9, 9, 9],
                     [9, 13, 9, 9, 10, 8, 8, 8, 8, 8, 8, 8, 10, 9, 9, 9],
                     [9, 13, 13, 13, 11, 11, 11, 11, 8, 11, 11, 11, 11, 9, 13, 9],
                     [9, 9, 12, 13, 9, 9, 9, 9, 9, 9, 9, 12, 9, 9, 9, 12],
                     [9, 9, 9, 9, 13, 13, 9, 12, 13, 9, 13, 9, 9, 9, 9, 9]]

    world_decomap = build_matrix(len(world_tilemap[0]), len(world_tilemap))

    start = (0, 320)

    loading_zones = {}
    
    return t_ids, world_tilemap, d_ids, world_decomap, colliders, loading_zones


def town():
    tile_dict = {2: 'tiles/stone_table_top.png', 3: 'tiles/stone_table_left.png', 5: 'tiles/stone_table_bottom.png', 8: 'tiles/wood.png', 9: 'tiles/grass.png', 10: 'tiles/corner.png', 11: 'tiles/wall.png', 12: 'tiles/top_left_water.png', 13: 'tiles/top_water.png', 14: 'tiles/top_right_water.png', 15: 'tiles/left_water.png', 17: 'tiles/right_water.png', 18: 'tiles/bottom_left_water.png', 19: 'tiles/bottom_water.png', 20: 'tiles/bottom_right_water.png', 21: 'tiles/grass3.png', 22: 'tiles/grass2.png', 23: 'tiles/pink_wall.png', 24:'tiles/top_left_path.png', 25: 'tiles/top_path.png', 26: 'tiles/top_right_path.png', 27: 'tiles/left_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 31: 'tiles/bottom_path.png', 32: 'tiles/bottom_right_path.png', 33: 'tiles/path_corner1.png', 34: 'tiles/path_corner2.png', 35: 'tiles/path_corner3.png', 36: 'tiles/path_corner4.png', 37: 'tiles/water_corner1.png', 38: 'tiles/water_corner2.png', 39: 'tiles/water_corner3.png', 40: 'tiles/water_corner4.png'}
    t_ids = build_id_list(tile_dict)
    d_ids = {}

    colliders = [2, 3, 5, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 23, 37, 38, 39, 40]

    town_tilemap = [[9, 9, 9, 9, 22, 9, 9, 9, 9, 22, 12, 13, 13, 14, 22, 9, 9, 9, 9, 10, 23, 23, 23, 23, 23, 23, 23, 10],
                    [9, 9, 10, 23, 23, 23, 23, 23, 10, 9, 15, 39, 40, 17, 24, 25, 25, 25, 25, 11, 8, 8, 8, 8, 8, 8, 8, 10],
                    [22, 9, 10, 8, 8, 8, 8, 8, 10, 21, 15, 17, 15, 17, 27, 28, 28, 28, 28, 8, 8, 8, 8, 8, 8, 8, 8, 10],
                    [9, 9, 10, 8, 8, 8, 8, 2, 10, 21, 15, 17, 15, 17, 27, 34, 31, 31, 31, 10, 8, 8, 8, 8, 8, 8, 8, 10],
                    [9, 9, 10, 8, 8, 8, 8, 5, 10, 9, 15, 38, 37, 17, 27, 29, 10, 23, 23, 23, 8, 8, 8, 8, 8, 8, 8, 10],
                    [9, 9, 11, 11, 11, 8, 11, 11, 11, 22, 18, 19, 19, 20, 27, 29, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
                    [9, 22, 9, 9, 27, 28, 29, 9, 22, 9, 21, 21, 21, 22, 27, 29, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
                    [25, 25, 25, 25, 36, 28, 33, 25, 25, 25, 25, 25, 25, 25, 36, 29, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
                    [28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 29, 11, 11, 11, 11, 8, 11, 11, 11, 11, 11, 11, 11],
                    [31, 31, 35, 28, 34, 31, 31, 31, 31, 31, 31, 35, 28, 28, 28, 33, 25, 25, 25, 36, 28, 33, 25, 25, 25, 25, 25, 25],
                    [9, 9, 27, 28, 29, 9, 9, 22, 9, 21, 22, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 34, 31, 35, 28, 34, 31],
                    [22, 9, 27, 28, 29, 9, 9, 21, 21, 21, 21, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 29, 10, 23, 8, 23, 10],
                    [10, 23, 23, 8, 23, 23, 23, 23, 23, 10, 21, 27, 28, 28, 34, 31, 31, 31, 31, 31, 31, 31, 32, 10, 8, 8, 8, 10],
                    [10, 8, 8, 8, 8, 8, 8, 8, 8, 10, 21, 27, 28, 28, 29, 22, 10, 23, 23, 23, 23, 23, 23, 23, 8, 8, 8, 10],
                    [10, 8, 8, 8, 8, 8, 8, 8, 8, 10, 22, 27, 28, 28, 29, 21, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
                    [10, 8, 8, 8, 8, 8, 8, 8, 8, 11, 25, 36, 28, 28, 33, 25, 11, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
                    [10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 28, 28, 28, 28, 28, 28, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
                    [10, 8, 8, 8, 8, 8, 8, 8, 8, 10, 31, 31, 31, 31, 31, 31, 10, 8, 8, 8, 8, 8, 3, 2, 2, 2, 2, 10],
                    [10, 8, 8, 8, 8, 8, 8, 8, 8, 10, 9, 22, 9, 9, 22, 9, 10, 8, 8, 8, 8, 8, 3, 22, 22, 22, 22, 10],
                    [10, 8, 8, 8, 8, 8, 8, 8, 8, 10, 9, 9, 9, 21, 22, 9, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
                    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 9, 22, 22, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 9, 9, 9, 9]]

    town_decomap = build_matrix(len(town_tilemap[0]), len(town_tilemap))


    start = (0, 320)

    loading_zones = {}
    
    return t_ids, town_tilemap, d_ids, town_decomap, colliders, loading_zones


def riverside():
    tile_dict = {8: 'tiles/wood.png', 9: 'tiles/grass.png', 10: 'tiles/corner.png', 11: 'tiles/wall.png', 12: 'tiles/top_left_water.png', 13: 'tiles/top_water.png', 14: 'tiles/top_right_water.png', 15: 'tiles/left_water.png', 16: 'tiles/water.png', 17: 'tiles/right_water.png', 18: 'tiles/bottom_left_water.png', 19: 'tiles/bottom_water.png', 20: 'tiles/bottom_right_water.png', 21: 'tiles/grass3.png', 22: 'tiles/grass2.png', 23: 'tiles/pink_wall.png', 24: 'tiles/top_left_path.png', 25: 'tiles/top_path.png', 26: 'tiles/top_right_path.png', 27: 'tiles/left_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 30: 'tiles/bottom_left_path.png', 31: 'tiles/bottom_path.png', 32: 'tiles/bottom_right_path.png', 33: 'tiles/path_corner1.png', 35: 'tiles/path_corner3.png', 36: 'tiles/path_corner4.png', 37: 'tiles/water_corner1.png', 38: 'tiles/water_corner2.png', 39: 'tiles/water_corner3.png', 40: 'tiles/water_corner4.png'}
    t_ids = build_id_list(tile_dict)
    d_ids = {}

    colliders = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 37, 38, 39, 40]

    riverside_tilemap = [[9, 9, 21, 9, 9, 9, 9, 12, 13, 13, 14, 9, 9, 9, 9, 22, 21, 9, 9, 9, 9, 22, 9, 21, 9, 9, 21, 9, 9, 22, 9, 9],
                         [21, 9, 9, 9, 22, 9, 12, 37, 16, 16, 38, 14, 9, 9, 9, 9, 9, 9, 9, 10, 23, 23, 23, 23, 23, 10, 23, 23, 23, 23, 10],
                         [9, 21, 9, 9, 9, 12, 37, 16, 16, 16, 16, 38, 14, 9, 24, 25, 25, 25, 26, 10, 8, 8, 8, 8, 8, 10, 8, 8, 8, 8, 10],
                         [9, 9, 9, 21, 9, 15, 16, 16, 16, 16, 16, 16, 17, 9, 30, 31, 35, 28, 29, 10, 8, 8, 8, 8, 8, 10, 8, 8, 8, 8, 10],
                         [9, 9, 9, 21, 9, 18, 40, 16, 16, 16, 16, 16, 17, 21, 21, 21, 27, 28, 29, 10, 8, 8, 8, 8, 8, 10, 8, 8, 8, 8, 10],
                         [9, 22, 9, 21, 21, 9, 15, 16, 16, 16, 16, 39, 20, 9, 9, 9, 27, 28, 29, 11, 11, 11, 10, 23, 8, 23, 23, 8, 23, 23, 10],
                         [9, 9, 9, 9, 21, 9, 18, 40, 16, 16, 39, 20, 9, 9, 9, 9, 27, 28, 29, 9, 9, 9, 10, 8, 8, 8, 8, 8, 8, 8, 10],
                         [21, 21, 21, 21, 21, 9, 9, 18, 19, 19, 20, 9, 9, 21, 21, 9, 27, 28, 29, 9, 22, 9, 10, 8, 8, 8, 8, 8, 8, 8, 10],
                         [9, 9, 21, 21, 21, 9, 9, 9, 9, 9, 9, 9, 9, 9, 21, 9, 27, 28, 29, 21, 21, 9, 11, 11, 8, 8, 11, 11, 11, 11, 11],
                         [9, 9, 9, 9, 21, 21, 21, 21, 21, 21, 21, 21, 9, 9, 21, 21, 27, 28, 29, 9, 21, 9, 9, 27, 28, 28, 29, 9, 9, 21, 9],
                         [13, 14, 9, 9, 21, 9, 9, 9, 9, 9, 9, 21, 9, 22, 9, 9, 27, 28, 33, 25, 25, 25, 25, 36, 28, 28, 29, 9, 21, 21, 21],
                         [16, 38, 14, 9, 9, 9, 21, 21, 22, 9, 9, 21, 21, 9, 9, 9, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28, 29, 9, 21, 22, 9],
                         [16, 16, 38, 14, 9, 9, 9, 9, 9, 9, 9, 9, 21, 9, 9, 9, 30, 31, 31, 31, 31, 31, 31, 31, 31, 31, 32, 9, 9, 12, 13],
                         [16, 16, 16, 38, 13, 13, 13, 13, 13, 13, 14, 9, 9, 21, 9, 9, 9, 9, 9, 9, 9, 12, 13, 13, 13, 13, 13, 13, 13, 37, 16],
                         [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 38, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 37, 16, 16, 16, 16, 16, 16, 16, 16, 16],
                         [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
                         [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
                         [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]]

    riverside_decomap = build_matrix(len(riverside_tilemap[0]), len(riverside_tilemap))

    start = (0, 320)

    loading_zones = {}
    
    return t_ids, riverside_tilemap, d_ids, riverside_decomap, colliders, loading_zones


def mountain():
    tile_dict = {9: 'tiles/grass.png', 24: 'tiles/top_left_path.png', 27: 'tiles/left_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 32: 'tiles/bottom_right_path.png', 34: 'tiles/path_corner2.png', 36: 'tiles/path_corner4.png', 41: 'tiles/cliff.png', 42: 'tiles/cliff_top_left.png', 43: 'tiles/cliff_top.png', 44: 'tiles/cliff_top_right.png', 47: 'tiles/cliff_right.png', 48: 'tiles/cliff_bottom_left.png', 49: 'tiles/cliff_bottom.png', 50: 'tiles/cliff_bottom_right.png', 51: 'tiles/lamp_post_bottom.png', 52: 'tiles/tree_bottom.png'}
    deco_dict = {1: 'tiles/lamp_post_top.png', 2: 'tiles/tree_top.png'}
    t_ids = build_id_list(tile_dict)
    d_ids = build_id_list(deco_dict)

    colliders = [41, 42, 43, 44, 47, 48, 49, 50, 51, 52]

    tilemap = [[9, 9, 9, 9, 9, 9, 9, 9, 9, 47, 9, 9, 9, 9, 9, 24],
               [9, 9, 52, 9, 9, 9, 52, 9, 9, 47, 9, 9, 9, 52, 24, 36],
               [9, 9, 9, 9, 52, 9, 9, 9, 43, 44, 9, 9, 51, 24, 36, 28],
               [42, 43, 9, 9, 9, 9, 9, 44, 41, 41, 9, 9, 24, 36, 28, 34],
               [41, 41, 42, 43, 43, 43, 44, 41, 49, 50, 9, 24, 36, 28, 34, 32],
               [48, 49, 41, 41, 41, 41, 41, 50, 9, 9, 24, 36, 28, 34, 32, 9],
               [9, 9, 48, 49, 49, 49, 50, 9, 9, 9, 27, 28, 34, 32, 9, 9],
               [9, 9, 9, 9, 9, 9, 9, 9, 52, 9, 27, 28, 29, 9, 9, 9],
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

    start = (0, 7)

    loading_zones = {}

    return t_ids, tilemap, d_ids, decomap, colliders, loading_zones


def demo():
    tile_dict = {9: 'tiles/grass.png', 12: 'tiles/top_left_water.png', 13: 'tiles/top_water.png', 14: 'tiles/top_right_water.png', 16: 'tiles/water.png', 21: 'tiles/grass3.png', 22: 'tiles/grass2.png', 24: 'tiles/top_left_path.png', 25: 'tiles/top_path.png', 26: 'tiles/top_right_path.png', 27: 'tiles/left_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 30: 'tiles/bottom_left_path.png', 31: 'tiles/bottom_path.png', 32: 'tiles/bottom_right_path.png', 33: 'tiles/path_corner1.png', 34: 'tiles/path_corner2.png', 35: 'tiles/path_corner3.png', 36: 'tiles/path_corner4.png', 37: 'tiles/water_corner1.png', 38: 'tiles/water_corner2.png', 41: 'tiles/cliff_top_left.png', 42: 'tiles/cliff_top.png', 43: 'tiles/cliff_top_right.png', 44: 'tiles/cliff_face_left.png', 45: 'tiles/cliff_center.png', 46: 'tiles/cliff_face_right.png', 47: 'tiles/cliff_bottom_left.png', 48: 'tiles/cliff_bottom.png', 49: 'tiles/cliff_bottom_right.png', 50: 'tiles/cliff_left.png', 52: 'tiles/cliff_right.png', 53: 'tiles/cliff_left_corner.png', 54: 'tiles/cliff_right_corner.png', 58: 'tiles/lamp_post_bottom.png', 67: 'tiles/door_bottom.png', 68: 'tiles/door_top.png', 69: 'tiles/bricks_left.png', 70: 'tiles/bricks.png', 71: 'tiles/bricks_right.png', 72: 'tiles/bricks_bottom_left.png', 73: 'tiles/bricks_bottom.png', 74: 'tiles/bricks_bottom_right.png', 75: 'tiles/window.png', 85: 'tiles/tree_trunk_left.png', 86: 'tiles/tree_trunk_right.png'}
    deco_dict = {1: 'tiles/lamp_post_top.png', 6: 'tiles/roof_right_bottom.png', 7: 'tiles/roof_right_middle1.png', 9: 'tiles/roof_right_top.png', 10: 'tiles/roof_left_bottom.png', 11: 'tiles/roof_left_middle1.png', 13: 'tiles/roof_left_top.png', 14: 'tiles/roof_top1.png', 15: 'tiles/roof_top2.png', 16: 'tiles/top_roof_shadow.png', 25: 'tiles/tree_top_left.png', 26: 'tiles/tree_top_right.png', 27: 'tiles/tree_mid_left.png', 28: 'tiles/tree_mid_right.png'}
    t_ids = build_id_list(tile_dict)
    d_ids = build_id_list(deco_dict)

    colliders = [12, 13, 14, 16, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 58, 69, 70, 71, 72, 73, 74, 75, 85, 86]

    tilemap = [[9, 9, 50, 9, 9, 9, 22, 9, 52, 9, 24, 25, 25, 25, 25, 25, 25, 25, 25, 25, 26, 21, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
               [9, 9, 41, 53, 85, 86, 9, 54, 43, 9, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28, 29, 21, 21, 9, 9, 9, 9, 9, 9, 21, 21, 22],
               [9, 9, 47, 41, 42, 42, 42, 43, 49, 21, 30, 31, 31, 31, 31, 31, 31, 31, 35, 28, 29, 9, 21, 9, 21, 69, 70, 70, 70, 71, 21, 21],
               [41, 53, 9, 47, 48, 48, 48, 49, 9, 9, 9, 85, 86, 9, 54, 42, 43, 9, 27, 28, 29, 21, 22, 9, 9, 69, 70, 70, 70, 71, 9, 9],
               [44, 41, 53, 9, 9, 21, 9, 9, 9, 54, 42, 42, 42, 42, 43, 45, 46, 9, 27, 28, 29, 9, 21, 21, 9, 69, 75, 68, 75, 71, 9, 9],
               [44, 44, 41, 53, 21, 9, 85, 86, 54, 43, 45, 45, 45, 45, 46, 45, 46, 9, 27, 28, 33, 26, 9, 9, 9, 72, 73, 67, 73, 74, 9, 21],
               [47, 44, 44, 41, 42, 42, 42, 42, 43, 46, 45, 45, 45, 45, 46, 48, 49, 9, 27, 28, 28, 29, 21, 21, 9, 58, 27, 28, 29, 58, 21, 21],
               [9, 47, 44, 44, 45, 45, 45, 45, 46, 46, 48, 48, 48, 48, 49, 9, 21, 21, 27, 28, 28, 33, 25, 25, 25, 25, 36, 28, 33, 25, 25, 25],
               [9, 9, 47, 44, 45, 45, 45, 45, 46, 49, 21, 9, 21, 21, 21, 22, 24, 25, 36, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
               [9, 9, 9, 47, 48, 48, 48, 48, 49, 9, 24, 25, 25, 25, 25, 25, 36, 28, 28, 28, 28, 28, 34, 31, 31, 31, 31, 31, 31, 31, 31, 31],
               [13, 14, 9, 9, 21, 9, 9, 21, 21, 21, 27, 28, 28, 28, 28, 28, 28, 28, 34, 31, 31, 31, 32, 22, 9, 9, 9, 9, 9, 12, 13, 13],
               [16, 38, 13, 13, 13, 13, 14, 9, 9, 21, 30, 31, 31, 31, 31, 31, 31, 31, 32, 9, 9, 21, 21, 9, 85, 86, 9, 12, 13, 37, 16, 16],
               [16, 16, 16, 16, 16, 16, 38, 13, 13, 14, 21, 85, 86, 21, 21, 85, 86, 9, 12, 13, 13, 13, 13, 13, 13, 13, 13, 37, 16, 16, 16, 16],
               [16, 16, 16, 16, 16, 16, 16, 16, 16, 38, 13, 13, 13, 13, 13, 13, 13, 13, 37, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]]

    decomap = [[0, 0, 0, 0, 27, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 15, 9, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 11, 14, 7, 9, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 27, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 10, 16, 6, 7, 0, 0],
               [0, 0, 0, 0, 0, 0, 25, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 27, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 26, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 26, 0, 0, 25, 26, 0, 0, 0, 0, 0, 0, 0, 27, 28, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 27, 28, 0, 0, 27, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    loading_zones = {(31, 8): [demo2, (1, 8)], (27, 5): [demo_house, (8, 7)], (27, 4): [demo_house, (8, 7)], (31, 7): [demo2, (1, 7)], (31, 9): [demo2, (1, 9)]}

    SignSprite(pygame.Rect(16 * 64, 8 * 64, 64, 32), {'blue_sign': 'assets/sign/blue_sign.png'}, SignSprite.stand, action='speak', action_args='dialogs/demo_welcome.txt', level='demo')
    pig_images = {"front": 'assets/npc/pig_front.png',
                  "front_walk1": 'assets/npc/pig_front_walk1.png',
                  "front_walk2": 'assets/npc/pig_front_walk2.png',
                  "back": 'assets/npc/pig_back.png',
                  "back_walk1": 'assets/npc/pig_back_walk1.png',
                  "back_walk2": 'assets/npc/pig_back_walk2.png',
                  "left": 'assets/npc/pig_left.png',
                  "left_walk1": 'assets/npc/pig_left_walk1.png',
                  "left_walk2": 'assets/npc/pig_left_walk2.png',
                  "right": 'assets/npc/pig_right.png',
                  "right_walk1": 'assets/npc/pig_right_walk1.png',
                  "right_walk2": 'assets/npc/pig_right_walk2.png'
                  }

    for name in Sprite.persists:
        if Sprite.persists[name]['level'] == 'demo':
            Sprite(None, None, None, name, level='demo')
            
    if not 'pig' in Sprite.persists:
        NPCSprite(pygame.Rect(20 * 64, 6 * 64, 64, 32), pig_images, NPCSprite.wander, name='pig', action='speak', action_args='dialogs/oink.txt', level='demo')
    
    return t_ids, tilemap, d_ids, decomap, colliders, loading_zones


def demo_house():
    tile_dict = {7: 'tiles/void.png', 8: 'tiles/wood.png', 10: 'tiles/corner.png', 60: 'tiles/table.png', 64: 'tiles/table_bottom_left.png', 66: 'tiles/table_bottom_right.png', 77: 'tiles/white_green_wall_base_rimmed.png', 78: 'tiles/white_green_wall_painting_base.png', 80: 'tiles/white_green_wall_base_drawer.png', 81: 'tiles/drawer_legs.png', 82: 'tiles/white_green_wall_base_left.png', 83: 'tiles/white_green_wall_base.png', 84: 'tiles/white_green_wall_base_right.png'}
    deco_dict = {3: 'tiles/table_top_left.png', 5: 'tiles/table_top_right.png', 17: 'tiles/white_green_wall_top_rimmed.png', 18: 'tiles/white_green_wall_painting_top.png', 19: 'tiles/white_green_wall_clock.png', 20: 'tiles/lamp.png', 21: 'tiles/white_green_wall_top_left.png', 22: 'tiles/white_green_wall_top.png', 23: 'tiles/white_green_wall_top_right.png'}
    t_ids = build_id_list(tile_dict)
    d_ids = build_id_list(deco_dict)

    colliders = [10, 60, 64, 66, 77, 78, 80, 82, 83, 84]

    tilemap = [[10, 7, 7, 7, 7, 7, 10, 7, 7, 10, 7, 7, 7, 7, 7, 7, 10],
               [10, 82, 83, 83, 83, 84, 10, 7, 7, 10, 82, 78, 83, 83, 80, 84, 10],
               [10, 8, 8, 8, 8, 8, 10, 7, 7, 10, 8, 8, 8, 8, 81, 8, 10],
               [10, 8, 8, 8, 8, 8, 10, 7, 7, 10, 8, 8, 64, 66, 8, 8, 10],
               [10, 82, 84, 8, 82, 83, 83, 83, 84, 10, 8, 8, 8, 8, 8, 8, 10],
               [10, 8, 8, 8, 8, 8, 8, 8, 8, 10, 7, 8, 7, 7, 8, 7, 10],
               [10, 8, 60, 8, 8, 8, 8, 8, 8, 82, 84, 8, 82, 84, 8, 77, 10],
               [10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
               [10, 10, 10, 10, 10, 10, 10, 10, 8, 10, 10, 10, 10, 10, 10, 10, 10]]

    decomap = [[0, 21, 22, 22, 22, 23, 0, 0, 0, 0, 21, 18, 22, 22, 19, 23, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 0, 0, 0],
               [0, 21, 23, 0, 21, 22, 22, 22, 23, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 23, 0, 21, 23, 0, 17, 0],
               [0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    loading_zones = {(8, 8): [demo, (27, 6)]}

    return t_ids, tilemap, d_ids, decomap, colliders, loading_zones


def demo2():
    tile_dict = {9: 'tiles/grass.png', 12: 'tiles/top_left_water.png', 15: 'tiles/left_water.png', 16: 'tiles/water.png', 18: 'tiles/bottom_left_water.png', 22: 'tiles/grass2.png', 25: 'tiles/top_path.png', 26: 'tiles/top_right_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 31: 'tiles/bottom_path.png', 32: 'tiles/bottom_right_path.png', 37: 'tiles/water_corner1.png', 40: 'tiles/water_corner4.png', 58: 'tiles/lamp_post_bottom.png', 85: 'tiles/tree_trunk_left.png', 86: 'tiles/tree_trunk_right.png'}
    deco_dict = {1: 'tiles/lamp_post_top.png', 25: 'tiles/tree_top_left.png', 26: 'tiles/tree_top_right.png', 27: 'tiles/tree_mid_left.png', 28: 'tiles/tree_mid_right.png'}
    t_ids = build_id_list(tile_dict)
    d_ids = build_id_list(deco_dict)

    colliders = [12, 15, 16, 18, 37, 40, 58, 85, 86]

    tilemap = [[9, 9, 9, 9, 9, 9, 18, 40, 16, 16, 16, 16, 16, 16, 16, 16],
               [9, 22, 9, 9, 9, 9, 9, 18, 40, 16, 16, 16, 16, 16, 16, 16],
               [85, 86, 9, 9, 9, 9, 9, 9, 15, 16, 16, 16, 16, 16, 16, 16],
               [9, 9, 9, 22, 9, 85, 86, 9, 15, 16, 16, 16, 16, 16, 16, 16],
               [9, 9, 9, 9, 9, 9, 9, 9, 15, 16, 16, 16, 16, 16, 16, 16],
               [9, 22, 9, 9, 9, 9, 9, 12, 37, 16, 16, 16, 16, 16, 16, 16],
               [9, 9, 58, 9, 22, 9, 12, 37, 16, 16, 16, 16, 16, 16, 16, 16],
               [25, 25, 25, 25, 26, 9, 18, 40, 16, 16, 16, 16, 16, 16, 16, 16],
               [28, 28, 28, 28, 29, 9, 9, 15, 16, 16, 16, 16, 16, 16, 16, 16],
               [31, 31, 31, 31, 32, 9, 9, 15, 16, 16, 16, 16, 16, 16, 16, 16],
               [9, 9, 9, 9, 9, 9, 12, 37, 16, 16, 16, 16, 16, 16, 16, 16],
               [9, 22, 9, 9, 9, 9, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [9, 9, 9, 9, 22, 9, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [9, 85, 86, 9, 9, 9, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [9, 9, 9, 9, 9, 12, 37, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [9, 9, 9, 9, 9, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [9, 9, 9, 9, 9, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
               [22, 9, 85, 86, 9, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]]

    decomap = [[25, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [27, 28, 0, 0, 0, 25, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 27, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 25, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 27, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 25, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 27, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    loading_zones = {(0, 8): [demo, (30, 8)], (0, 7): [demo, (30, 7)], (0, 9): [demo, (30, 9)]}

    return t_ids, tilemap, d_ids, decomap, colliders, loading_zones


def lala():
    tile_dict = {2: 'tiles/stone_table_top.png', 3: 'tiles/stone_table_left.png', 4: 'tiles/stone_table_right.png', 5: 'tiles/stone_table_bottom.png', 8: 'tiles/wood.png', 9: 'tiles/grass.png', 10: 'tiles/corner.png', 11: 'tiles/wall.png', 12: 'tiles/top_left_water.png', 13: 'tiles/top_water.png', 14: 'tiles/top_right_water.png', 15: 'tiles/left_water.png', 16: 'tiles/water.png', 17: 'tiles/right_water.png', 18: 'tiles/bottom_left_water.png', 19: 'tiles/bottom_water.png', 20: 'tiles/bottom_right_water.png', 21: 'tiles/grass3.png', 22: 'tiles/grass2.png', 23: 'tiles/pink_wall.png', 24: 'tiles/top_left_path.png', 25: 'tiles/top_path.png', 27: 'tiles/left_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 30: 'tiles/bottom_left_path.png', 31: 'tiles/bottom_path.png', 32: 'tiles/bottom_right_path.png', 33: 'tiles/path_corner1.png', 34: 'tiles/path_corner2.png', 35: 'tiles/path_corner3.png', 36: 'tiles/path_corner4.png', 37: 'tiles/water_corner1.png', 39: 'tiles/water_corner3.png', 41: 'tiles/cliff.png', 42: 'tiles/cliff_top_left.png', 43: 'tiles/cliff_top.png', 44: 'tiles/cliff_top_right.png', 47: 'tiles/cliff_right.png', 48: 'tiles/cliff_bottom_left.png', 49: 'tiles/cliff_bottom.png', 50: 'tiles/cliff_bottom_right.png', 51: 'tiles/lamp_post_bottom.png', 52: 'tiles/tree_bottom.png'}
    deco_dict = {1: 'tiles/lamp_post_top.png', 2: 'tiles/tree_top.png'}
    t_ids = build_id_list(tile_dict)
    d_ids = build_id_list(deco_dict)

    colliders = [2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 37, 39, 41, 43, 44, 47, 48, 49, 50, 51, 52]

    tilemap = [[10, 23, 23, 23, 23, 10, 9, 9, 9, 22, 22, 9, 9, 9, 9, 9, 21, 21, 21, 21, 21, 21, 21, 21, 21, 10, 23, 23, 23, 23, 23, 23, 23, 23, 23, 10],
               [10, 2, 8, 8, 8, 10, 9, 22, 52, 9, 21, 24, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 11, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
               [10, 5, 8, 8, 8, 10, 9, 9, 9, 9, 21, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
               [10, 8, 8, 8, 8, 10, 22, 21, 9, 9, 22, 27, 28, 34, 31, 31, 31, 35, 28, 34, 31, 31, 31, 31, 31, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
               [10, 8, 8, 8, 8, 23, 23, 23, 23, 23, 10, 27, 28, 29, 9, 9, 22, 27, 28, 29, 21, 21, 21, 21, 21, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
               [10, 8, 8, 8, 8, 8, 8, 8, 3, 4, 10, 27, 28, 29, 21, 21, 21, 27, 28, 29, 21, 21, 21, 21, 21, 10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
               [10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10, 27, 28, 29, 22, 47, 21, 27, 28, 29, 21, 21, 22, 21, 21, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
               [10, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10, 27, 28, 29, 9, 47, 21, 27, 28, 29, 51, 21, 21, 21, 21, 21, 9, 21, 21, 21, 21, 21, 22, 21, 21, 21],
               [11, 11, 11, 11, 8, 8, 11, 11, 11, 11, 11, 27, 28, 29, 9, 47, 21, 27, 28, 29, 21, 21, 21, 21, 21, 22, 9, 9, 9, 9, 9, 9, 9, 21, 21, 22],
               [21, 9, 9, 27, 28, 28, 29, 9, 9, 9, 9, 27, 28, 29, 9, 47, 21, 27, 28, 29, 21, 21, 10, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 10],
               [21, 9, 51, 27, 28, 28, 33, 25, 25, 25, 25, 36, 28, 29, 9, 47, 21, 27, 28, 33, 25, 25, 11, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
               [21, 9, 9, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28, 29, 9, 47, 21, 27, 28, 28, 28, 28, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
               [42, 43, 21, 30, 31, 31, 31, 31, 31, 31, 31, 31, 31, 32, 43, 44, 21, 30, 31, 31, 31, 31, 10, 3, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 10],
               [41, 41, 42, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 44, 41, 41, 21, 21, 21, 21, 21, 21, 11, 11, 11, 11, 11, 11, 11, 10, 8, 8, 8, 8, 8, 10],
               [41, 41, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 50, 41, 41, 21, 22, 21, 21, 22, 21, 9, 9, 9, 22, 9, 9, 9, 10, 8, 8, 8, 8, 2, 10],
               [41, 41, 21, 9, 21, 22, 21, 21, 21, 21, 21, 21, 21, 21, 41, 41, 21, 21, 21, 21, 21, 12, 13, 13, 13, 13, 13, 14, 9, 10, 8, 8, 8, 8, 5, 10],
               [41, 41, 42, 9, 9, 21, 21, 21, 52, 21, 22, 9, 9, 44, 41, 41, 21, 21, 21, 21, 21, 15, 16, 16, 16, 16, 16, 17, 9, 10, 8, 8, 8, 8, 8, 10],
               [48, 49, 41, 42, 43, 43, 43, 43, 43, 43, 43, 43, 44, 41, 49, 50, 21, 22, 21, 12, 13, 37, 16, 16, 16, 16, 16, 17, 21, 11, 11, 11, 11, 11, 11, 11],
               [21, 21, 48, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 50, 9, 21, 21, 21, 21, 15, 16, 16, 16, 16, 16, 16, 39, 20, 9, 9, 9, 9, 9, 22, 9, 9],
               [22, 21, 21, 48, 49, 49, 49, 49, 49, 49, 49, 49, 50, 21, 22, 21, 12, 13, 13, 37, 16, 16, 16, 16, 16, 39, 20, 9, 9, 9, 9, 22, 9, 9, 9, 9],
               [21, 21, 21, 22, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 15, 16, 16, 16, 16, 16, 16, 16, 39, 20, 21, 21, 21, 21, 22, 21, 52, 21, 21, 22],
               [21, 52, 21, 21, 21, 21, 21, 21, 21, 22, 21, 21, 21, 21, 21, 21, 18, 19, 19, 19, 19, 19, 19, 19, 20, 21, 21, 22, 21, 21, 21, 21, 21, 22, 21, 21]]

    decomap = [[0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
               [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    loading_zones = {}

    start = (3, 3)

    return t_ids, tilemap, d_ids, decomap, colliders, loading_zones