from dialog import *
import random
import json

# # WORLDS MODULE


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


def load_from_string(string):
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
    tile_ids = build_id_dict({1: 'tiles/block.png', 2: 'tiles/stone_table_top.png', 3: 'tiles/stone_table_left.png',
                              4: 'tiles/stone_table_right.png', 5: 'tiles/stone_table_bottom.png',
                              6: 'tiles/stone_wall.png', 7: 'tiles/void.png', 8: 'tiles/wood.png', 9: 'tiles/grass.png',
                              10: 'tiles/corner.png', 11: 'tiles/wall.png', 12: 'tiles/top_left_water.png',
                              13: 'tiles/top_water.png', 14: 'tiles/top_right_water.png', 15: 'tiles/left_water.png',
                              16: 'tiles/water.png', 17: 'tiles/right_water.png', 18: 'tiles/bottom_left_water.png',
                              19: 'tiles/bottom_water.png', 20: 'tiles/bottom_right_water.png', 21: 'tiles/grass3.png',
                              22: 'tiles/grass2.png', 23: 'tiles/pink_wall.png', 24: 'tiles/top_left_path.png',
                              25: 'tiles/top_path.png', 26: 'tiles/top_right_path.png', 27: 'tiles/left_path.png',
                              28: 'tiles/path.png', 29: 'tiles/right_path.png', 30: 'tiles/bottom_left_path.png',
                              31: 'tiles/bottom_path.png', 32: 'tiles/bottom_right_path.png',
                              33: 'tiles/path_corner1.png', 34: 'tiles/path_corner2.png', 35: 'tiles/path_corner3.png',
                              36: 'tiles/path_corner4.png', 37: 'tiles/water_corner1.png',
                              38: 'tiles/water_corner2.png', 39: 'tiles/water_corner3.png',
                              40: 'tiles/water_corner4.png', 41: 'tiles/cliff_top_left.png', 42: 'tiles/cliff_top.png',
                              43: 'tiles/cliff_top_right.png', 44: 'tiles/cliff_face_left.png',
                              45: 'tiles/cliff_center.png', 46: 'tiles/cliff_face_right.png',
                              47: 'tiles/cliff_bottom_left.png', 48: 'tiles/cliff_bottom.png',
                              49: 'tiles/cliff_bottom_right.png', 50: 'tiles/cliff_left.png',
                              51: 'tiles/cliff_back.png', 52: 'tiles/cliff_right.png',
                              53: 'tiles/cliff_left_corner.png', 54: 'tiles/cliff_right_corner.png',
                              55: 'tiles/cliff_stairs_top.png', 56: 'tiles/cliff_stairs.png',
                              57: 'tiles/cliff_stairs_bottom.png', 58: 'tiles/lamp_post_bottom.png',
                              59: 'tiles/table.png', 60: 'tiles/table_left.png', 61: 'tiles/table_center.png',
                              62: 'tiles/table_right.png', 63: 'tiles/table_bottom_left.png',
                              64: 'tiles/table_bottom.png', 65: 'tiles/table_bottom_right.png',
                              66: 'tiles/door_bottom.png', 67: 'tiles/door_top.png', 68: 'tiles/bricks_left.png',
                              69: 'tiles/bricks.png', 70: 'tiles/bricks_right.png', 71: 'tiles/bricks_bottom_left.png',
                              72: 'tiles/bricks_bottom.png', 73: 'tiles/bricks_bottom_right.png',
                              74: 'tiles/window.png', 75: 'tiles/pink_wall_base.png',
                              76: 'tiles/white_green_wall_base_rimmed.png',
                              77: 'tiles/white_green_wall_painting_base.png', 78: 'tiles/drawer.png',
                              79: 'tiles/white_green_wall_base_drawer.png', 80: 'tiles/drawer_legs.png',
                              81: 'tiles/white_green_wall_base_left.png', 82: 'tiles/white_green_wall_base.png',
                              83: 'tiles/white_green_wall_base_right.png', 84: 'tiles/tree_trunk.png',
                              85: 'tiles/water2.png', 86: 'tiles/water_ripple.png', 87: 'tiles/wood_shade.png'})
    deco_ids = build_id_dict({1: 'tiles/lamp_post_top.png', 2: 'tiles/table_top_left.png', 3: 'tiles/table_top.png',
                              4: 'tiles/table_top_right.png', 5: 'tiles/roof_right_bottom.png',
                              6: 'tiles/roof_right_middle1.png', 7: 'tiles/roof_right_middle2.png',
                              8: 'tiles/roof_right_top.png', 9: 'tiles/roof_left_bottom.png',
                              10: 'tiles/roof_left_middle1.png', 11: 'tiles/roof_left_middle2.png',
                              12: 'tiles/roof_left_top.png', 13: 'tiles/roof_top1.png', 14: 'tiles/roof_top2.png',
                              15: 'tiles/top_roof_shadow.png', 16: 'tiles/pink_wall_top.png',
                              17: 'tiles/white_green_wall_top_rimmed.png',
                              18: 'tiles/white_green_wall_painting_top.png', 19: 'tiles/white_green_wall_clock.png',
                              20: 'tiles/lamp.png', 21: 'tiles/white_green_wall_top_left.png',
                              22: 'tiles/white_green_wall_top.png', 23: 'tiles/white_green_wall_top_right.png',
                              24: 'tiles/roof_right_edge.png', 25: 'tiles/roof_left_edge.png',
                              26: 'tiles/tree_top_left.png', 27: 'tiles/tree_top.png', 28: 'tiles/tree_top_right.png',
                              29: 'tiles/tree_mid_left.png', 30: 'tiles/tree_mid.png', 31: 'tiles/tree_mid_right.png'})
    reference_dict = {}

    def __init__(self, colliders, tilemap, decomap, loading_zones, lightmap, default_start=(0, 0), name="Unnamed"):
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
        if name in Level.reference_dict:
            print("WARNING: Multiple levels have the same name '{}'.  Overwriting!".format(name))
        self.name = name
        Level.reference_dict[name] = self

    def __repr__(self):
        return "<Level Object | Name: {}>".format(self.name)

    def jsonify(self):
        loading_zones = []
        for i, j in self.loading_zones.items():
            loading_zones.append({"zone": list(i), "target_level": j[0], "target_pos": j[1]})
        export_dict = {"colliders": self.colliders,
                       "tilemap": self.tilemap,
                       "decomap": self.decomap,
                       "loading_zones": loading_zones,
                       "lightmap": self.lightmap,
                       "spawn": self.default_start,
                       "name": self.name
                       }
        return json.dumps(export_dict)

    @classmethod
    def levels_init(cls):
        found_files = [os.path.join('levels', f) for f in os.listdir('levels/') if
                       os.path.isfile(os.path.join('levels', f)) and os.path.splitext(f)[1] == '.json']
        for i in found_files:
            with open(i) as rf:
                data = json.load(rf)
                loading_zones = {}
                for j in data["loading_zones"]:
                    loading_zones[tuple(j["zone"])] = [j["target_level"], tuple(j["target_pos"])]

                Level(data["colliders"],
                      data["tilemap"],
                      data["decomap"],
                      loading_zones,
                      data["lightmap"],
                      data["spawn"],
                      data["name"])

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
    SignSprite(pygame.Rect(16 * 64, 8 * 64, 64, 32), {'blue_sign': blue_sign}, SignSprite.stand, "demo", "local",
               action='speak', action_args='dialogs/demo_welcome.txt')

    pig_animations = {"front": Animation(
        ('assets/npc/pig/pig_front.png', 'assets/npc/pig/pig_front_walk1.png', 'assets/npc/pig/pig_front_walk2.png'),
        (0, 1, 0, 2)),
                      "back": Animation(('assets/npc/pig/pig_back.png', 'assets/npc/pig/pig_back_walk1.png',
                                         'assets/npc/pig/pig_back_walk2.png'), (0, 1, 0, 2)),
                      "left": Animation(('assets/npc/pig/pig_left.png', 'assets/npc/pig/pig_left_walk1.png',
                                         'assets/npc/pig/pig_left_walk2.png'), (0, 1, 0, 2)),
                      "right": Animation(('assets/npc/pig/pig_right.png', 'assets/npc/pig/pig_right_walk1.png',
                                          'assets/npc/pig/pig_right_walk2.png'), (0, 1, 0, 2))
                      }

    NPCSprite(pygame.Rect(20 * 64, 6 * 64, 64, 32), pig_animations, NPCSprite.wander, "demo", "global", action='speak',
              action_args='dialogs/oink.txt')
    # NPCSprite(pygame.Rect(20 * 64, 8 * 64, 64, 32), pig_images, NPCSprite.always_right, demo, "global", action='speak', action_args='dialogs/oink.txt')

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

    NPCSprite(pygame.Rect(20 * 64, 14 * 64, 64, 32), male_duck_animations, NPCSprite.wander, "demo", "global")

    # Player setup
    player_start = Level.reference_dict[start_level].default_start
    # Player bounding box
    player = pygame.Rect(player_start[0] * 64, player_start[1] * 64, 48, int(112 / 2))
    # Player sprite
    player_animations = {"front": Animation(('assets/player/player_front.png', 'assets/player/player_front_walk1.png',
                                             'assets/player/player_front_walk2.png'), (0, 1, 0, 2)),
                         "back": Animation(('assets/player/player_back.png', 'assets/player/player_back_walk1.png',
                                            'assets/player/player_back_walk2.png'), (0, 1, 0, 2)),
                         "left": Animation(('assets/player/player_left.png', 'assets/player/player_left_walk1.png',
                                            'assets/player/player_left_walk2.png'), (0, 1, 0, 2)),
                         "right": Animation(('assets/player/player_right.png', 'assets/player/player_right_walk1.png',
                                             'assets/player/player_right_walk2.png'), (0, 1, 0, 2))
                         }

    # Default player sprite data
    player_sprite = PlayerSprite(player, player_animations, PlayerSprite.normal, start_level, health=100)

    return player_sprite


def minor_sprite_setup(start_level):
    """Build all sprites, returning the player sprite"""
    # Player setup
    player_start = Level.reference_dict[start_level].default_start
    # Player bounding box
    player = pygame.Rect(player_start[0] * 64, player_start[1] * 64, 48, int(112 / 2))
    # Player sprite
    player_animations = {"front": Animation(('assets/blue_player/player_front.png', 'assets/blue_player/player_front_walk1.png',
                                             'assets/blue_player/player_front_walk2.png'), (0, 1, 0, 2)),
                         "back": Animation(('assets/blue_player/player_back.png', 'assets/blue_player/player_back_walk1.png',
                                            'assets/blue_player/player_back_walk2.png'), (0, 1, 0, 2)),
                         "left": Animation(('assets/blue_player/player_left.png', 'assets/blue_player/player_left_walk1.png',
                                            'assets/blue_player/player_left_walk2.png'), (0, 1, 0, 2)),
                         "right": Animation(('assets/blue_player/player_right.png', 'assets/blue_player/player_right_walk1.png',
                                             'assets/blue_player/player_right_walk2.png'), (0, 1, 0, 2))
                         }

    # Default player sprite data
    player_sprite = PlayerSprite(player, player_animations, PlayerSprite.normal, start_level, health=100)

    return player_sprite

# # SPRITE MODULE


# Functions for actions
def blank(args):
    """Default interaction that does absolutely nothing"""
    pass


def speak(args):
    """Basic interaction that causes text to appear"""
    text_box = TextDialog("assets/dialog_box.png")
    text_box.display_dialog(args)


action_lookup = {'blank': blank, 'speak': speak}


class Tracker:
    """Class for variables that keep track of whether they've been changed"""

    def __init__(self, value):
        self.value = value
        self.changed = False

    def set(self, new_value):
        if self.value != new_value:
            self.changed = True
            self.value = new_value

    def querry(self):
        if self.changed:
            self.changed = False
            return True


class Animation:
    """Class for animations"""

    def __init__(self, images, sequence):
        self.tick = 0
        self.prev_tick = 0
        self.image_tuple = images
        self.image_sequence = sequence
        self.frame_list = tuple(pygame.image.load(os.path.join(images[i])).convert_alpha() for i in sequence)
        self.backup_list = tuple(i.copy() for i in self.frame_list)
        self.rect_list = tuple(i.get_rect() for i in self.frame_list)
        self.frame_count = len(self.frame_list) - 1
        self.frame = self.frame_list[0]
        self.rect = self.rect_list[0]
        self.interval = 25
        self.running = False

    def update(self, time_step):
        """Update the animation frame"""
        self.running = True
        self.tick += time_step / self.interval
        if int(self.tick) != int(self.prev_tick):
            if int(self.tick) > self.frame_count:
                self.tick = 0
            self.frame = self.frame_list[int(self.tick)]
            self.rect = self.rect_list[int(self.tick)]
        self.prev_tick = float(self.tick)

    def draw(self, window, dest):
        """Draw current frame to window"""
        window.blit(self.frame, dest)

    def draw_norm(self, window, dest):
        """Draw current backup frame to window"""
        window.blit(self.backup_list[int(self.tick)], dest)

    def draw_clipped(self, window, dispx, dispy, disp_reg, litmap_rects):
        """Draw current backup frame with only area outside a light
        source darkened"""
        # First get a list of rectangles that intersect the source
        # Then copy this part of the current backup frame onto the current frame
        img_rect = self.rect.move(1, 1)
        img = self.frame.copy()
        window.blit(img, disp_reg)
        for i in img_rect.collidelistall(litmap_rects):
            dark_rect = img_rect.clip(litmap_rects[i])
            if dark_rect.size != (0, 0):
                dark_rect.move_ip(-1, -1)
                # window.fill((255, 0, 0), dark_rect.move(disp))
                window.blit(self.backup_list[int(self.tick)], dest=dark_rect.move(dispx, dispy), area=dark_rect.move(self.rect.topleft[0] * -1, self.rect.topleft[1] * -1))

    def reset(self):
        """Reset the animation frame to base"""
        self.running = False
        if self.tick != 0:
            self.tick = 0
            self.prev_tick = 0
            self.frame = self.frame_list[0]
            self.rect = self.rect_list[0]

    def darken(self, amount):
        """Darken the image by an amount"""
        for i in self.frame_list:
            shade = pygame.Surface((i.get_width(), i.get_height()))
            shade.fill((amount, amount, amount))
            i.blit(shade, (0, 0), special_flags=pygame.BLEND_SUB)
        self.frame = self.frame_list[int(self.tick)]
    
    def undo(self):
        """Reset all changes to the animation images"""
        self.frame_list = tuple(i.copy() for i in self.backup_list)
        self.frame = self.frame_list[int(self.tick)]


class Static(Animation):
    """Subclass for static animations"""

    def __init__(self, image):
        self.frame = pygame.image.load(os.path.join(image)).convert_alpha()
        self.backup = self.frame.copy()
        self.rect = self.frame.get_rect()
        self.running = False

    def update(self, timestep):
        """Handles any calls for frame updates.  Helps with
        standardization, but otherwise does nothing"""
        pass

    def draw(self, window, dest):
        """Standard drawing function"""
        window.blit(self.frame, dest)

    def draw_norm(self, window, dest):
        """Draw backup image"""
        window.blit(self.backup, dest)

    def draw_clipped(self, window, dispx, dispy, disp_reg, litmap_rects):
        """Draw current backup frame with only area outside a light
        source darkened"""
        img_rect = self.rect.move(1, 1)
        img = self.frame.copy()
        window.blit(img, (disp_reg))
        for i in img_rect.collidelistall(litmap_rects):
            dark_rect = img_rect.clip(litmap_rects[i])
            if dark_rect.size != (0, 0):
                dark_rect.move_ip(-1, -1)
                #window.fill((255, 0, 0), dark_rect.move(disp))
                window.blit(self.backup_list, dest=dark_rect.move(dispx, dispy), area=dark_rect.move(self.rect.topleft[0] * -1, self.rect.topleft[1] * -1))

    def darken(self, amount):
        """Darken the image by an amount"""
        shade = pygame.Surface((self.frame.get_width(), self.frame.get_height()))
        shade.fill((amount, amount, amount))
        self.frame.blit(shade, (0, 0), special_flags=pygame.BLEND_SUB)

    def undo(self):
        """Reset all changes to the animation image"""
        self.frame = self.backup.copy()


class Sprite:
    """Main class for sprites"""

    sprite_dict = {}
    global_sprites = []
    local_sprites = []

    loaded_locals = []
    focus = None
    id_counter = 0
    
    behavior_args = {}

    def __init__(self, rect, animation_dict, behavior, level, scope, action='blank', action_args=None, health=None, max_health=None):
        self.health = health
        self.max_health = max_health
        self.rect = rect
        self.x = int(rect.x)
        self.y = int(rect.y)
        self.collision_time = 0
        self.animation_dict = animation_dict
        self.animation = list(animation_dict.items())[0][1]
        self.freeze = False
        self.behavior = behavior
        self.level = Level.reference_dict[level]
        self.scope = scope
        self.action = action_lookup[action]
        self.action_args = action_args
        self.speed_mult = 1
        self.entity_id = Sprite.id_counter
        self.facing = Tracker(None)
        self.direction = Tracker(None)
        Sprite.id_counter += 1
        if scope == "global":
            Sprite.global_sprites.append(self)
        elif scope == "local":
            Sprite.local_sprites.append(self)
        else:
            print("An error occurred while loading a sprite:\n'{}' is an invalid scope".format(scope))

        # Additional data for asking server about levels
        self.inquiring = False
        self.inquire_of = ""
        Sprite.sprite_dict[self.entity_id] = self

    def __repr__(self):
        """Override in subclass"""
        pass

    def __str__(self):
        return self.__repr__()

    def jsonify(self):
        """Converts a sprite into a json representation of itself, override in subclass"""
        pass

    def check_collision(self, dx, dy, tilemap, collider_ids):
        """Function to check if a sprite rectangle has collided with something"""
        try:
            dx, dy = round(1.5 * dx), round(1.5 * dy)
            new_rect = self.rect.move(dx, dy)
            x1 = int(new_rect.x / 64)
            y1 = int(new_rect.y / 64)
            x2 = int((new_rect.x + new_rect.width) / 64)
            y2 = int((new_rect.y + new_rect.height) / 64)
            if (new_rect.x < 0) or (new_rect.y < 0) or (x2 < 0) or (y2 < 0):
                return False
            if tilemap[y1][x1] in collider_ids:
                return False
            if tilemap[y2][x1] in collider_ids:
                return False
            if tilemap[y1][x2] in collider_ids:
                return False
            if tilemap[y2][x2] in collider_ids:
                return False
            if self.collision_time < 180 and Sprite.check_sprites_collide(self, dx, dy) is not None:
                self.collision_time += Sprite.behavior_args["time_step"]
                return False
            if self.collision_time > 0:
                self.collision_time -= Sprite.behavior_args["time_step"] / 2
            return True
        except IndexError:
            return False

    def behave(self):
        """Function to execute the behavior of sprites.  Override in subclass"""
        pass

    def check_load_zone(self):
        """Check if the sprite is in a loading zone, and if so, send the sprite to the relevant level.
        Return False if nothing happens, return True if successful."""
        x, y = self.rect.center
        x = int(x / 64)
        y = int(y / 64)
        if (x, y) in self.level.loading_zones:
            zone = self.level.loading_zones[(x, y)]
            self.inquire_of = zone[0]
            self.x = zone[1][0] * 64
            self.y = zone[1][1] * 64
            self.rect.x = zone[1][0] * 64
            self.rect.y = zone[1][1] * 64
            return True
        else:
            return False

    def check_lit_tile(self, litmap):
        """Check if the sprite is partially or fully on tiles that are illuminated.
        -Return 0 if sprite is NOT touching a lit tile.
        -Return 1-3 if the sprite is PARTIALLY touching a lit tile.
        -Return 4 if the sprite is ONLY touching lit tiles.
        -Return 0 if an IndexError occurs (entity is out of bounds).
        """
        try:
            r = self.animation.rect
            c = 0
            for x in (r.left, r.right):
                for y in (r.bottom, r.top):
                    if litmap[y // 64][x // 64]: c += 1
            return c
        except IndexError:
            return 0

    @classmethod
    def delete_sprite(cls, entity_id):
        """Removed a sprite from the sprite dictionary"""
        for i, j in enumerate(Sprite.global_sprites):
            if entity_id == j.entity_id:
                Sprite.global_sprites.pop(i)
                break
        for i, j in cls.sprite_dict.items():
            if entity_id == i:
                del cls.sprite_dict[i]
                break

    @classmethod
    def add_sprite(cls, json_dict):
        """Registers a new sprite sent from the server"""

        if json_dict["type"] == "SignSprite":
            new = SignSprite(pygame.Rect(json_dict["entity_data"]["rect"]),
                             dict((i, Static(j)) for i, j in json_dict["entity_data"]["animation"].items()),
                             behavior_lookup[json_dict["entity_data"]["behavior"]],
                             json_dict["entity_data"]["level"],
                             json_dict["entity_data"]["scope"],
                             json_dict["entity_data"]["action"],
                             json_dict["entity_data"]["action_args"]
                             )
            del cls.sprite_dict[new.entity_id]
            new.entity_id = json_dict["id"]
            cls.sprite_dict[new.entity_id] = new
            print("Entity ID:", new.entity_id)
            print("After attempting to add SignSprite:", cls.sprite_dict)
        elif json_dict["type"] == "NPCSprite":
            new = NPCSprite(pygame.Rect(json_dict["entity_data"]["rect"]),
                            dict((i, Animation(j[0], j[1])) for i, j in json_dict["entity_data"]["animation_dict"].items()),
                            GuestSprite.normal,
                            json_dict["entity_data"]["level"],
                            json_dict["entity_data"]["scope"],
                            json_dict["entity_data"]["action"],
                            json_dict["entity_data"]["action_args"],
                            json_dict["entity_data"]["health"],
                            json_dict["entity_data"]["max_health"]
                            )
            del cls.sprite_dict[new.entity_id]
            new.entity_id = json_dict["id"]
            cls.sprite_dict[new.entity_id] = new
        elif json_dict["type"] == "GuestSprite" or json_dict["type"] == "PlayerSprite":
            new = GuestSprite(json_dict["id"],
                              pygame.Rect(json_dict["entity_data"]["rect"]),
                              dict((i, Animation(j[0], j[1])) for i, j in json_dict["entity_data"]["animation_dict"].items()),
                              json_dict["entity_data"]["level"]
                              )
            del cls.sprite_dict[new.entity_id]
            new.entity_id = json_dict["id"]
            cls.sprite_dict[new.entity_id] = new
        else:
            print("Error: '{}' is not a valid sprite type".format(json_dict["type"]))

    @classmethod
    def freeze(cls, state):
        """Set the freeze state of all sprites"""
        for s in cls.global_sprites + cls.loaded_locals:
            s.freeze = state

    @classmethod
    def check_sprites_collide(cls, entity, dx, dy):
        """Function to check if a sprite has collided with another sprite, and if so, return that sprite"""
        entity_rect = entity.rect.copy()
        sprite_list = cls.local_sprites + [i for i in cls.global_sprites if i.level == entity.level]
        other_rects = list(s.rect for s in sprite_list if s.rect != entity_rect)
        index = entity_rect.move(dx, dy).collidelist(other_rects)
        if index == -1:
            return None
        return other_rects[index]

    @classmethod
    def behave_all(cls):
        """Function to execute the behavior of all sprites"""
        for s in cls.global_sprites + cls.loaded_locals:
            s.behave()
        for s in cls.global_sprites:
            if s.check_load_zone() and type(s) == PlayerSprite:
                s.inquiring = True
                Sprite.behavior_args["screen_wipe"] = True

    @classmethod
    def blit_all(cls, dispx, dispy, window):
        """Blit all sprites that are currently located in the same level as the focus sprite.
        Does not handle light levels"""
        loaded_sprites = cls.loaded_locals + [i for i in cls.global_sprites if i.level.name == cls.focus.level.name]
        
        loaded_sprites.sort(key=lambda kv: kv.rect.center[1])
        for s in loaded_sprites:
            s.animation.draw(window, (s.x + dispx, s.y + dispy - s.rect.height))
            # window.fill((127, 0, 0), s.rect.move((dispx, dispy)))

    @classmethod
    def blit_all_night(cls, dispx, dispy, window, litmap, lit_rects):
        """Blit all sprites that are currently located in the same level as the focus sprite.
        Designed for handling light levels"""
        loaded_sprites = cls.loaded_locals + [i for i in cls.global_sprites if i.level.name == cls.focus.level.name]
        
        loaded_sprites.sort(key=lambda kv: kv.rect.center[1])
        for s in loaded_sprites:
            s.animation.rect.bottomleft = s.rect.bottomleft
            disp_reg = (s.x + dispx, s.y + dispy - s.rect.height)
            lit_tiles = s.check_lit_tile(litmap)
            # Player is not touching any lit tiles, draw normally.
            if not lit_tiles:
                s.animation.draw(window, disp_reg)
            # Player is only touching lit tiles, draw illuminated backup.
            elif lit_tiles == 4:
                s.animation.draw_norm(window, disp_reg)
            # Player is partially touching lit tiles, draw clipped.
            else:
                s.animation.draw_clipped(window, dispx, dispy, disp_reg, lit_rects)
    
    @classmethod
    def darken_all(cls, amount=100):
        for i in cls.local_sprites + cls.global_sprites:
            try:
                for j, k in i.animation_dict.items():
                    k.darken(amount)
            except AttributeError:
                i.animation.darken(amount)

    @classmethod
    def reset_imgs(cls):
        for i in cls.local_sprites + cls.global_sprites:
            try:
                for j, k in i.animation_dict.items():
                    k.undo()
            except AttributeError:
                i.animation.undo()

    @classmethod
    def reload_loaded_locals(cls):
        """Recalculate the list of loaded local sprites"""
        cls.loaded_locals = [i for i in cls.local_sprites if i.level == cls.focus.level]


# Subclass for sign sprites
class SignSprite(Sprite):

    def __init__(self, rect, animation_dict, behavior, level, scope, action='blank', action_args=None):
        Sprite.__init__(self, rect, animation_dict, behavior, level, "local", action, action_args, None, None)

    def __repr__(self):
        result = """<SignSprite | ID: {}, Rect: {}, Behavior: {}, Action: {}, Action Args: {}, Level: {}""".format(
            self.entity_id, self.rect, self.behavior, self.action, self.action_args, self.level)
        return result

    def jsonify(self):
        """Converts the sprite into a JSON representation of itself"""
        result = {"id": self.entity_id, "type": "SignSprite", "entity_data": {
            "rect": [self.rect.x, self.rect.y, self.rect.w, self.rect.h],
            "animation_dict": dict((i, j.image_tuple)
                                   for i, j in self.animation_dict.items()),
            "behavior": dict((j, i) for i, j in behavior_lookup.items())[self.behavior],
            "level": self.level.name,
            "scope": "local",
            "action": dict((j, i) for i, j in action_lookup.items())[self.action],
            "action_args": self.action_args,
            "health": None,
            "max_health": None
        }
                  }
        return json.dumps(result)

    # Execute the behavior of the sign sprite
    def behave(self):
        self.behavior(self)

    # Normal standing behavior
    def stand(self):
        pass


# Subclass for NPC sprites
class NPCSprite(Sprite):

    def __init__(self, rect, animation_dict, behavior, level, scope, action='blank', action_args=None, health=None, max_health=None):
        Sprite.__init__(self, rect, animation_dict, behavior, level, scope, action, action_args, health, max_health)
        self.interval = 25
        self.cycle = 0 
        self.facing = Tracker("front")
        self.direction = Tracker(None)
        self.dx = 0
        self.dy = 0

    def __repr__(self):
        result = """<NPCSprite | Rect: {}, Behavior: {}, Action: {}, Action Args: {}, Health: {}, Level: {}>""".format(
            self.rect, self.behavior, self.action, self.action_args, self.health, self.level)
        return result

    def jsonify(self):
        """Converts the sprite into a JSON representation of itself"""
        result = {"id": self.entity_id, "type": "NPCSprite", "entity_data": {
            "rect": [self.rect.x, self.rect.y, self.rect.w, self.rect.h],
            "animation_dict": dict((i, [j.image_tuple, j.image_sequence])
                                   for i, j in self.animation_dict.items()),
            "behavior": dict((j, i) for i, j in behavior_lookup.items())[self.behavior],
            "level": self.level.name,
            "scope": self.scope,
            "action": dict((j, i) for i, j in action_lookup.items())[self.action],
            "action_args": self.action_args,
            "health": None,
            "max_health": None
        }
                  }
        return json.dumps(result)

    # Execute behavior of the NPC sprite
    def behave(self):
        self.behavior(self)

    # Behavour of NPC to stand in place
    def stand(self):
        pass

    # Behavour of NPC to wander aimlessly around the map
    def wander(self):
        tilemap = self.level.tilemap
        colliders = self.level.colliders
        if self.cycle > 384:
            self.cycle = 0
            self.dx = random.randint(-1, 1)
            self.dy = random.randint(-1, 1)
            if not self.check_collision(self.dx * 64, self.dy * 64, tilemap, colliders):
                self.dx, self.dy = 0, 0
                self.cycle = 385
        time_step = Sprite.behavior_args['time_step']
        self.cycle += time_step
        if self.cycle <= 80:
            self.movement(tilemap, colliders, time_step)
            self.speed_mult = 1
        else:
            if self.cycle <= 100:
                self.animation.reset()

    # Behavour of NPC to panic aimlessly
    def panic(self):
        tilemap = self.level.tilemap
        colliders = self.level.colliders
        if self.cycle > 64:
            self.cycle = 0
            self.dx, self.dy = 0, 0
            while self.dx == 0 and self.dy == 0:
                self.dx = random.randint(-1, 1)
                self.dy = random.randint(-1, 1)
            if not self.check_collision(self.dx, self.dy, tilemap, colliders):
                self.dx, self.dy = 0, 0
                self.cycle = 65
        time_step = Sprite.behavior_args['time_step']
        self.cycle += time_step
        if self.cycle <= 64:
            self.movement(tilemap, colliders, 1.5 * time_step)
            self.speed_mult = 1.5
        else:
            self.animation.reset()

    # Behavour of NPC to always move right
    def always_right(self):
        tilemap = self.level.tilemap
        colliders = self.level.colliders
        self.dx = 1
        self.dy = 0
        time_step = Sprite.behavior_args['time_step']
        self.movement(tilemap, colliders, 1.5 * time_step)
        self.speed_mult = 1.5
        
    # Standard NPC movement
    def movement(self, tilemap, colliders, time_step):
        dx, dy = 0, 0
        speed = 1.0 * time_step
        moved = False
        
        if self.dy == -1:
            dy -= speed
            self.facing.set("back")
            self.direction.set(None)
            moved = True
            
        if self.dy == 1:
            dy += speed
            self.facing.set("front")
            self.direction.set(None)
            moved = True
            
        if self.check_collision(0, dy, tilemap, colliders):
            self.y += dy
        else:
            dy = 0
            self.cycle = 80
            
        if self.dx == -1:
            dx -= speed
            self.direction.set("left") 
            moved = True
            
        if self.dx == 1:
            dx += speed
            self.direction.set("right") 
            moved = True
            
        if self.check_collision(dx, 0, tilemap, colliders):
            self.x += dx
        else:
            dx = 0
            self.cycle = 80

        if not moved:
            self.animation.reset()
        else:
            if self.direction.querry() or self.facing.querry():
                if self.direction.value:
                    self.animation = self.animation_dict[self.direction.value]
                else:
                    self.animation = self.animation_dict[self.facing.value]
                
            self.animation.update(speed * 1.5)
            self.rect.move_ip(round(self.x - self.rect.x), round(self.y - self.rect.y))


# Subclass for player sprite
class PlayerSprite(Sprite):
    
    def __init__(self, rect, animation_dict, behavior, level, health=None, max_health=None):
        Sprite.__init__(self, rect, animation_dict, behavior, level, "global", health=health, max_health=max_health)
        self.facing = Tracker("front")
        self.direction = Tracker(None)

    def __repr__(self):
        return """<PlayerSprite | Rect: {}, Health: {}, Level: {}>""".format(self.rect, self.health, str(self.level))

    def jsonify(self):
        """Converts the sprite into a JSON representation of itself"""
        result = {"id": self.entity_id, "type": "PlayerSprite", "entity_data": {
            "rect": [self.rect.x, self.rect.y, self.rect.w, self.rect.h],
            "animation_dict": dict((i, [j.image_tuple, j.image_sequence])
                                   for i, j in self.animation_dict.items()),
            "behavior": dict((j, i) for i, j in behavior_lookup.items())[self.behavior],
            "level": self.level.name,
            "scope": "global",
            "health": None,
            "max_health": None
        }
                  }
        return json.dumps(result)

    def jsonify2(self):
        """Converts necessary information about this sprite into a json format"""
        data = {"id": self.entity_id,
                "x": self.x,
                "y": self.y,
                "facing": self.facing.value,
                "direction": self.direction.value,
                "animated": self.animation.running,
                "speed": self.speed_mult,
                "level": self.level.name
                }
        return json.dumps(data)

    # Execute the behavior of the player sprite
    def behave(self):
        self.behavior(self)

    # Standard player sprite movement
    def movement(self, args):
        if self.freeze:
            return
        
        keys = args[0]
        time_step = args[1]
        tilemap = args[2]
        colliders = args[3]
        dx = 0
        dy = 0
        player_moved = False
        self.speed_mult = 1.25
        
        if keys[pygame.K_LSHIFT]:
            speed = time_step * 1.25
        else:
            speed = 2.25 * time_step
            self.speed_mult += 1

        if keys[pygame.K_w]:
            dy -= speed
            self.facing.set("back")
            self.direction.set(None)
            player_moved = True
            
        if keys[pygame.K_s]:
            dy += speed
            self.facing.set("front")
            self.direction.set(None)
            player_moved = True
            
        if self.check_collision(0, dy, tilemap, colliders):
            self.y += dy
            
        if keys[pygame.K_a]:
            dx -= speed
            self.direction.set("left")
            player_moved = True
            
        if keys[pygame.K_d]:
            dx += speed
            self.direction.set("right")
            player_moved = True
            
        if self.check_collision(dx, 0, tilemap, colliders):
            self.x += dx

        # Trigger call for interact
        if keys[pygame.K_SPACE]:
            loaded_globals = [i for i in Sprite.global_sprites if i.level == self.level]
            for s in (loaded_globals + Sprite.loaded_locals):
                if type(s) != PlayerSprite:
                    if self.rect.inflate(16, 16).colliderect(s.rect):
                        s.action(s.action_args)
                        break

        if player_moved is False:
            self.animation.reset()
        else:
            if self.direction.querry() or self.facing.querry():
                if self.direction.value:
                    self.animation = self.animation_dict[self.direction.value]
                else:
                    self.animation = self.animation_dict[self.facing.value]

            self.animation.update(speed / 2)
            self.rect.move_ip(round(self.x - self.rect.x), round(self.y - self.rect.y))

    # Regular player behavior
    def normal(self):
        keys = Sprite.behavior_args['keys']
        time_step = Sprite.behavior_args['time_step']
        tilemap = self.level.tilemap
        colliders = self.level.colliders
        self.movement((keys, time_step, tilemap, colliders))


class GuestSprite(Sprite):
    """Class for sprites that represent multiplayer players"""

    def __init__(self, entity_id, rect, animation_dict, level, health=None, max_health=None):
        Sprite.__init__(self, rect, animation_dict, GuestSprite.normal, level, "global", health=health, max_health=max_health)
        self.facing = Tracker("front")
        self.direction = Tracker(None)
        self.entity_id = entity_id

    def __repr__(self):
        return """<GuestSprite | ID: {}, Rect: {}, Health: {}, Level: {}>""".format(
            self.entity_id, self.rect, self.health, str(self.level))

    def jsonify(self):
        """Converts the sprite into a JSON representation of itself"""
        result = {"id": self.entity_id, "type": "GuestSprite", "entity_data": {
            "rect": [self.rect.x, self.rect.y, self.rect.w, self.rect.h],
            "animation_dict": dict((i, [j.image_tuple, j.image_sequence])
                                   for i, j in self.animation_dict.items()),
            "behavior": dict((j, i) for i, j in behavior_lookup.items())[self.behavior],
            "level": self.level.name,
            "scope": "global",
            "health": None,
            "max_health": None
        }
                  }
        return json.dumps(result)

    def behave(self):
        self.behavior(self)

    def normal(self):
        """Regular guest sprite behavior, typically used for syncing internal sprite data"""
        self.rect.x = self.x
        self.rect.y = self.y
        if self.animation.running:
            if self.direction.querry() or self.facing.querry():
                if self.direction.value:
                    self.animation = self.animation_dict[self.direction.value]
                else:
                    self.animation = self.animation_dict[self.facing.value]

            self.animation.update(self.speed_mult * Sprite.behavior_args["time_step"] / 2)

        else:
            self.animation.reset()


behavior_lookup = {"SignSprite.stand": SignSprite.stand,
                   "NPCSprite.wander": NPCSprite.wander,
                   "NPCSprite.panic": NPCSprite.panic,
                   "NPCSprite.always_right": NPCSprite.always_right,
                   "PlayerSprite.normal": PlayerSprite.normal,
                   "GuestSprite.normal": GuestSprite.normal
                   }
