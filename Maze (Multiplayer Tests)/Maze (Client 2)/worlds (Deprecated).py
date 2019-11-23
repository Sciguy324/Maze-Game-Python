from sprite import *


class Tile:
    """Class for animated tiles"""
    interval = 50
    img_index = 0
    colorkey = (200, 50, 200)

    def __init__(self, file):
        img = pygame.image.load(os.path.join(file))
        # Check whether image contains transparency and load accordingly.
        array = pygame.PixelArray(img)
        transparent = False
        x = -1
        for i in array:
            x += 1
            y = -1
            for j in i:
                y += 1
                if j is not None and img.unmap_rgb(j).a < 255:
                    transparent = True
                    break
            if transparent:
                break
        if transparent:
            img.convert_alpha()
        else:
            img.convert()

        self.alpha = bool(transparent)

        # Load individual sub-images from a larger image.
        small_height = img.get_height() // 16
        img = pygame.transform.scale(img, (64, small_height * 64))
        self.img_list = []
        for i in range(small_height):
            if transparent:
                temp_img = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
                temp_img.convert_alpha()
            else:
                temp_img = pygame.Surface((64, 64))
            temp_img.blit(img, (0, 0), (0, 64 * i, 64, 64))
            self.img_list.append(temp_img)

        self.backup_list = tuple(i.copy() for i in self.img_list)
        self.max_imgs = len(self.img_list)
        self.main_img = img

    def draw(self, surface, dest=(0, 0)):
        """Draw an image to a surface."""
        if self.max_imgs > 1:
            surface.blit(self.img_list[int(Tile.img_index % self.max_imgs)], dest)
        else:
            surface.blit(self.img_list[0], dest)

    def draw_norm(self, surface, dest=(0, 0)):
        """Draw an image's backup to a surface."""
        if self.max_imgs > 1:
            surface.blit(self.backup_list[int(Tile.img_index % self.max_imgs)], dest)
        else:
            surface.blit(self.backup_list[0], dest)

    def reset(self):
        """Reset all changes to a tile, restoring it to the backup"""
        self.img_list = list(i.copy() for i in self.backup_list)
    
    @classmethod
    def advance_frame(cls, time_step=1):
        cls.img_index += time_step / cls.interval
        if cls.img_index > 64:
            cls.img_index = 0


# Construction functions for level initialization
def build_id_dict(tiles):
    """Build a dictionary of images paired with their id from the given dictionary"""
    id_list = {}
    for i in list(tiles.items()):
        img = Tile(i[1])
        id_list[i[0]] = img
    return id_list


def build_matrix(width, height):
    """Build a matrix of given width and height"""
    matrix = []
    row = [0] * width
    for i in range(height):
        matrix.append(list(row))
    return matrix


def load_json_level(string):
    data = json.loads(string)
    loading_zones = {}
    for j in data["loading_zones"]:
        loading_zones[tuple(j["zone"])] = [j["target_level"], tuple(j["target_pos"])]

    return Level(data["colliders"],
                 data["tilemap"],
                 data["decomap"],
                 loading_zones,
                 data["lightmap"],
                 data["spawn"],
                 data["name"])


class Level:
    """Class for levels"""
    tile_ids = build_id_dict({1: 'tiles/block.png', 2: 'tiles/stone_table_top.png', 3: 'tiles/stone_table_left.png', 4: 'tiles/stone_table_right.png', 5: 'tiles/stone_table_bottom.png', 6: 'tiles/stone_wall.png', 7: 'tiles/void.png', 8: 'tiles/wood.png', 9: 'tiles/grass.png', 10: 'tiles/corner.png', 11: 'tiles/wall.png', 12: 'tiles/top_left_water.png', 13: 'tiles/top_water.png', 14: 'tiles/top_right_water.png', 15: 'tiles/left_water.png', 16: 'tiles/water.png', 17: 'tiles/right_water.png', 18: 'tiles/bottom_left_water.png', 19: 'tiles/bottom_water.png', 20: 'tiles/bottom_right_water.png', 21: 'tiles/grass3.png', 22: 'tiles/grass2.png', 23: 'tiles/pink_wall.png', 24: 'tiles/top_left_path.png', 25: 'tiles/top_path.png', 26: 'tiles/top_right_path.png', 27: 'tiles/left_path.png', 28: 'tiles/path.png', 29: 'tiles/right_path.png', 30: 'tiles/bottom_left_path.png', 31: 'tiles/bottom_path.png', 32: 'tiles/bottom_right_path.png', 33: 'tiles/path_corner1.png', 34: 'tiles/path_corner2.png', 35: 'tiles/path_corner3.png', 36: 'tiles/path_corner4.png', 37: 'tiles/water_corner1.png', 38: 'tiles/water_corner2.png', 39: 'tiles/water_corner3.png', 40: 'tiles/water_corner4.png', 41: 'tiles/cliff_top_left.png', 42: 'tiles/cliff_top.png', 43: 'tiles/cliff_top_right.png', 44: 'tiles/cliff_face_left.png', 45: 'tiles/cliff_center.png', 46: 'tiles/cliff_face_right.png', 47: 'tiles/cliff_bottom_left.png', 48: 'tiles/cliff_bottom.png', 49: 'tiles/cliff_bottom_right.png', 50: 'tiles/cliff_left.png', 51: 'tiles/cliff_back.png', 52: 'tiles/cliff_right.png', 53: 'tiles/cliff_left_corner.png', 54: 'tiles/cliff_right_corner.png', 55: 'tiles/cliff_stairs_top.png', 56: 'tiles/cliff_stairs.png', 57: 'tiles/cliff_stairs_bottom.png', 58: 'tiles/lamp_post_bottom.png', 59: 'tiles/table.png', 60: 'tiles/table_left.png', 61: 'tiles/table_center.png', 62: 'tiles/table_right.png', 63: 'tiles/table_bottom_left.png', 64: 'tiles/table_bottom.png', 65: 'tiles/table_bottom_right.png', 66: 'tiles/door_bottom.png', 67: 'tiles/door_top.png', 68: 'tiles/bricks_left.png', 69: 'tiles/bricks.png', 70: 'tiles/bricks_right.png', 71: 'tiles/bricks_bottom_left.png', 72: 'tiles/bricks_bottom.png', 73: 'tiles/bricks_bottom_right.png', 74: 'tiles/window.png', 75: 'tiles/pink_wall_base.png', 76: 'tiles/white_green_wall_base_rimmed.png', 77: 'tiles/white_green_wall_painting_base.png', 78: 'tiles/drawer.png', 79: 'tiles/white_green_wall_base_drawer.png', 80: 'tiles/drawer_legs.png', 81: 'tiles/white_green_wall_base_left.png', 82: 'tiles/white_green_wall_base.png', 83: 'tiles/white_green_wall_base_right.png', 84: 'tiles/tree_trunk.png', 85: 'tiles/water2.png', 86: 'tiles/water_ripple.png', 87: 'tiles/wood_shade.png'})
    deco_ids = build_id_dict({1: 'tiles/lamp_post_top.png', 2: 'tiles/table_top_left.png', 3: 'tiles/table_top.png', 4: 'tiles/table_top_right.png', 5: 'tiles/roof_right_bottom.png', 6: 'tiles/roof_right_middle1.png', 7: 'tiles/roof_right_middle2.png', 8: 'tiles/roof_right_top.png', 9: 'tiles/roof_left_bottom.png', 10: 'tiles/roof_left_middle1.png', 11: 'tiles/roof_left_middle2.png', 12: 'tiles/roof_left_top.png', 13: 'tiles/roof_top1.png', 14: 'tiles/roof_top2.png', 15: 'tiles/top_roof_shadow.png', 16: 'tiles/pink_wall_top.png', 17: 'tiles/white_green_wall_top_rimmed.png', 18: 'tiles/white_green_wall_painting_top.png', 19: 'tiles/white_green_wall_clock.png', 20: 'tiles/lamp.png', 21: 'tiles/white_green_wall_top_left.png', 22: 'tiles/white_green_wall_top.png', 23: 'tiles/white_green_wall_top_right.png', 24: 'tiles/roof_right_edge.png', 25: 'tiles/roof_left_edge.png', 26: 'tiles/tree_top_left.png', 27: 'tiles/tree_top.png', 28: 'tiles/tree_top_right.png', 29: 'tiles/tree_mid_left.png', 30: 'tiles/tree_mid.png', 31: 'tiles/tree_mid_right.png'})
    
    def __init__(self, colliders, tilemap, decomap, loading_zones, lightmap=[], default_start=(0, 0), name="Unnamed"):
        self.colliders = colliders
        self.tilemap = tilemap
        self.lightmap = lightmap
        self.width = 64 * len(tilemap[1])
        self.height = 64 * len(tilemap)
        if decomap is None:
            self.decomap = build_matrix(len(tilemap[0]), len(tilemap))
        else:
            self.decomap = decomap
        self.loading_zones = loading_zones
        self.default_start = default_start
        self.name = name

    def __repr__(self):
        return "<Level Object | Name: {}>".format(self.name)

    @classmethod
    def darken_imgs(cls, amount=100):
        """Darken all tiles and decos"""
        shade = pygame.Surface((64, 64)).convert_alpha()
        shade.fill((amount, amount, amount, 100))
        for i, j in Level.tile_ids.items():
            for k in j.img_list:
                k.blit(shade, (0, 0), special_flags=pygame.BLEND_SUB)

        for i, j in Level.deco_ids.items():
            for k in j.img_list:
                k.blit(shade, (0, 0), special_flags=pygame.BLEND_SUB)

    @classmethod
    def reset_imgs(cls):
        """Reset changes to all tiles and decos"""
        for i, j in cls.tile_ids.items():
            j.reset()
        for i, j in cls.deco_ids.items():
            j.reset()


def sprite_setup(start_level):
    """Build all sprites, returning the player sprite"""
    blue_sign = Static('assets/sign/blue_sign.png')
    SignSprite(pygame.Rect(16 * 64, 8 * 64, 64, 32), {'blue_sign': blue_sign}, SignSprite.stand, demo, "local", action='speak', action_args='dialogs/demo_welcome.txt')

    pig_animations = {"front": Animation(('assets/npc/pig/pig_front.png', 'assets/npc/pig/pig_front_walk1.png', 'assets/npc/pig/pig_front_walk2.png'), (0, 1, 0, 2)),
                      "back": Animation(('assets/npc/pig/pig_back.png', 'assets/npc/pig/pig_back_walk1.png', 'assets/npc/pig/pig_back_walk2.png'), (0, 1, 0, 2)),
                      "left": Animation(('assets/npc/pig/pig_left.png', 'assets/npc/pig/pig_left_walk1.png', 'assets/npc/pig/pig_left_walk2.png'), (0, 1, 0, 2)),
                      "right":  Animation(('assets/npc/pig/pig_right.png', 'assets/npc/pig/pig_right_walk1.png', 'assets/npc/pig/pig_right_walk2.png'), (0, 1, 0, 2))
                      }
    
    NPCSprite(pygame.Rect(20 * 64, 6 * 64, 64, 32), pig_animations, NPCSprite.wander, demo, "global", action='speak', action_args='dialogs/oink.txt')
    #NPCSprite(pygame.Rect(20 * 64, 8 * 64, 64, 32), pig_images, NPCSprite.always_right, demo, "global", action='speak', action_args='dialogs/oink.txt')

    male_duck_animations = {"front": Animation(('assets/npc/male_duck/male_duck_front.png',), (0,)),
                            "back": Animation(('assets/npc/male_duck/male_duck_back.png',), (0,)),
                            "left": Animation(('assets/npc/male_duck/male_duck_left.png',), (0,)),
                            "right": Animation(('assets/npc/male_duck/male_duck_right.png',), (0,))
                            }

    female_duck_animations = {"front": Animation(('assets/npc/female_duck/female_duck_front.png',), (0,)),
                              "back": Animation(('assets/npc/female_duck/female_duck_back.png',), (0,)),
                              "left": Animation(('assets/npc/female_duck/female_duck_left.png',), (0,)),
                              "right": Animation(('assets/npc/female_duck/female_duck_right.png',), (0,))
                              }

    duckling_animations = {"front": Animation(('assets/npc/duckling/duckling_front.png',), (0,)),
                           "back": Animation(('assets/npc/duckling/duckling_back.png',), (0,)),
                           "left": Animation(('assets/npc/duckling/duckling_left.png',), (0,)),
                           "right": Animation(('assets/npc/duckling/duckling_right.png',), (0,))
                           }

    NPCSprite(pygame.Rect(20 * 64, 14 * 64, 64, 32), male_duck_animations, NPCSprite.wander, demo, "global")
    
    # Player setup
    player_start = start_level.default_start
    # Player bounding box
    player = pygame.Rect(player_start[0] * 64, player_start[1] * 64, 48, int(112/2))
    # Player sprite
    player_animations = {"front": Animation(('assets/player/player_front.png', 'assets/player/player_front_walk1.png', 'assets/player/player_front_walk2.png'), (0, 1, 0, 2)),
                         "back": Animation(('assets/player/player_back.png', 'assets/player/player_back_walk1.png', 'assets/player/player_back_walk2.png'), (0, 1, 0, 2)),
                         "left": Animation(('assets/player/player_left.png', 'assets/player/player_left_walk1.png', 'assets/player/player_left_walk2.png'), (0, 1, 0, 2)),
                         "right": Animation(('assets/player/player_right.png', 'assets/player/player_right_walk1.png', 'assets/player/player_right_walk2.png'), (0, 1, 0, 2))
                         }

    # Default player sprite data
    player_sprite = PlayerSprite(player, player_animations, PlayerSprite.normal, start_level, health=100)

    return player_sprite
