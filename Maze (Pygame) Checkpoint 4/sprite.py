import pygame
import os
from dialog import *
import random

# Functions for actions
def blank(args):
    '''Default interaction that does absolutely nothing'''

def speak(args):
    '''Basic interaction that causes text to appear'''
    text_box = TextDialog("assets/dialog_box.png")
    text_box.display_dialog(args)

action_lookup = {'blank': blank, 'speak': speak}

# Class for variables that keep track of whether they've been changed
class Tracker:

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

# Class for animations
class Animation:

    def __init__(self, images, sequence):
        self.tick = 0
        self.prev_tick = 0
        self.frame_list = tuple(pygame.image.load(os.path.join(images[i])).convert_alpha() for i in sequence)
        self.backup_list = tuple(i.copy() for i in self.frame_list)
        self.rect_list = tuple(i.get_rect() for i in self.frame_list)
        self.frame_count = len(self.frame_list) - 1
        self.frame = self.frame_list[0]
        self.rect = self.rect_list[0]
        self.interval = 50

    def update(self, time_step):
        '''Update the animation frame'''
        self.tick += time_step / self.interval
        if int(self.tick) != int(self.prev_tick):
            if int(self.tick) > self.frame_count:
                self.tick = 0
            self.frame = self.frame_list[int(self.tick)]
            self.rect = self.rect_list[int(self.tick)]
        self.prev_tick = float(self.tick)

    def draw(self, window, dest):
        '''Draw current frame to window'''
        window.blit(self.frame, dest)

    def draw_norm(self, window, dest):
        '''Draw current backup frame to window'''
        window.blit(self.backup_list[int(self.tick)], dest)

    def draw_clipped(self, window, disp, disp_reg, litmap_rects):
        '''Draw current backup frame with only area outside a light
        source darkened'''
        # First get a list of rectangles that intersect the source
        # Then copy this part of the current backup frame onto the current frame
        img_rect = self.rect.move(1, 1)
        img = self.frame.copy()
        window.blit(img, (disp_reg))
        for i in img_rect.collidelistall(litmap_rects):
            dark_rect = img_rect.clip(litmap_rects[i])
            dark_rect.move_ip(-1, -1)
            if dark_rect.size != (0, 0):
                #window.fill((255, 0, 0), dark_rect.move(disp))
                window.blit(self.backup_list[int(self.tick)], dest=dark_rect.move(disp), area=dark_rect.move(self.rect.topleft[0] * -1, self.rect.topleft[1] * -1))

    def reset(self):
        '''Reset the animation frame to base'''
        if self.tick != 0:
            self.tick = 0
            self.prev_tick = 0
            self.frame = self.frame_list[0]
            self.rect = self.rect_list[0]

    def darken(self, amount):
        '''Darken the image by an amount'''
        for i in self.frame_list:
            shade = pygame.Surface((i.get_width(), i.get_height()))
            shade.fill((amount, amount, amount))
            i.blit(shade, (0, 0), special_flags=pygame.BLEND_SUB)
        self.frame = self.frame_list[int(self.tick)]
    
    def undo(self):
        '''Reset all changes to the animation images'''
        self.frame_list = tuple(i.copy() for i in self.backup_list)
        self.frame = self.frame_list[int(self.tick)]

# Subclass for static animations
class Static(Animation):

    def __init__(self, image):
        self.frame = pygame.image.load(os.path.join(image)).convert_alpha()
        self.backup = self.frame.copy()
        self.rect = self.frame.get_rect()

    def update(self):
        '''Handles any calls for frame updates.  Helps with
        standardization, but otherwise does nothing'''
        pass

    def draw(self, window, dest):
        '''Standard drawing function'''
        window.blit(self.frame, dest)

    def draw_norm(self, window, dest):
        '''Draw backup image'''
        window.blit(self.backup, dest)

    def draw_clipped(self, window, source, litmap_rects):
        '''Draw current backup frame with only area outside a light
        source darkened'''
        img_rect = self.rect.move(1, 1)
        img = self.frame.copy()
        window.blit(img, (disp_reg))
        for i in img_rect.collidelistall(litmap_rects):
            dark_rect = img_rect.clip(litmap_rects[i])
            dark_rect.move_ip(-1, -1)
            if dark_rect.size != (0, 0):
                #window.fill((255, 0, 0), dark_rect.move(disp))
                window.blit(self.backup_list, dest=dark_rect.move(disp), area=dark_rect.move(self.rect.topleft[0] * -1, self.rect.topleft[1] * -1))

    def darken(self, amount):
        '''Darken the image by an amount'''
        shade = pygame.Surface((self.frame.get_width(), self.frame.get_height()))
        shade.fill((amount, amount, amount))
        self.frame.blit(shade, (0, 0), special_flags=pygame.BLEND_SUB)

    def undo(self):
        '''Reset all changes to the animation image'''
        self.frame = self.backup.copy()

# Main class for sprites
class Sprite:
    global_sprites = []
    local_sprites = []
    loaded_locals = []
    focus = None
    
    behavour_args = {}

    def __init__(self, rect, animation_dict, behavour, level, scope, action='blank', action_args=None, health=None, max_health=None):
        self.health = health
        self.rect = rect
        self.x = int(rect.x)
        self.y = int(rect.y)
        if len(animation_dict) == 1:
            self.animation = list(animation_dict.items())[0][1]
        else:
            self.animation_dict = animation_dict
            self.animation = list(animation_dict.items())[0][1]
        self.freeze = False
        self.behavour = behavour
        self.level = level
        self.scope = scope
        self.action = action_lookup[action]
        self.action_args = action_args
        if scope == "global":
            Sprite.global_sprites.append(self)
        elif scope == "local":
            Sprite.global_sprites.append(self)
        else:
            print("An error occured while loading a sprite:\n'{}' is an invalid scope".format(scope))

    def __repr__(self):
        '''Override in subclass'''
        pass

    def __str__(self):
        return self.__repr__()

    def check_collision(self, dx, dy, tilemap, collider_ids):
        '''Function to check if a sprite rectange has collided with something'''
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
            if Sprite.check_sprites_collide(self, dx, dy) != None:
                return False
            return True
        except IndexError:
            return False

    def behave(self):
        '''Function to execute the behavour of sprites.  Override in subclass'''
        pass

    def check_load_zone(self):
        '''Check if the sprite is in a loading zone, and if so, send the sprite to the relevant level.
        Return False if nothing happens, return True if successfull.'''
        x, y = self.rect.center
        x = int(x / 64)
        y = int(y / 64)
        if (x, y) in self.level.loading_zones:
            zone = self.level.loading_zones[(x, y)]
            self.level = zone[0]()
            self.x = zone[1][0] * 64
            self.y = zone[1][1] * 64
            self.rect.x = zone[1][0] * 64
            self.rect.y = zone[1][1] * 64
            return True
        else:
            return False

    def check_lit_tile(self, litmap):
        '''Check if the sprite is partially or fully on tiles that are illuminated.
        -Return 0 if sprite is NOT touching a lit tile.
        -Return 1-3 if the sprite is PARTIALLY touching a lit tile.
        -Return 4 if the sprite is ONLY touching lit tiles.
        -Return 0 if an IndexError occurs (entity is out of bounds).
        '''
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
    def freeze(cls, state):
        '''Set the freeze state of all sprites'''
        for s in cls.global_sprites + cls.loaded_locals:
            s.freeze = state

    @classmethod
    def check_sprites_collide(cls, entity, dx, dy):
        '''Function to check if a sprite has collided with another sprite, and if so, return that sprite'''
        entity_rect = entity.rect.copy()
        sprite_list = cls.local_sprites + [i for i in cls.global_sprites if i.level == entity.level]
        other_rects = list(s.rect for s in sprite_list if s.rect != entity_rect)
        index = entity_rect.move(dx, dy).collidelist(other_rects)
        if index == -1:
            return None
        return other_rects[index]

    @classmethod
    def behave_all(cls):
        '''Function to execute the behavour of all sprites'''
        for s in cls.global_sprites + cls.loaded_locals:
            s.behave()
        for s in cls.global_sprites:
            if s.check_load_zone() and type(s) == PlayerSprite:
                Sprite.behavour_args["screen_wipe"] = True

    @classmethod
    def blit_all(cls, dispx, dispy, window):
        '''Blit all sprites that are currently located in the same level as the focus sprite.
        Does not handle light levels'''
        loaded_sprites = cls.loaded_locals + [i for i in cls.global_sprites if i.level == cls.focus.level]
        
        loaded_sprites.sort(key=lambda kv: kv.rect.center[1])
        for s in loaded_sprites:
            s.animation.draw(window, (s.x + dispx, s.y + dispy - s.rect.height))
            #window.blit(s.animation.frame, (s.x + dispx, s.y + dispy - s.rect.height))
            #window.fill((127, 0, 0), s.rect.move(dispx, dispy))

    @classmethod
    def blit_all_night(cls, dispx, dispy, window, litmap, lit_rects):
        '''Blit all sprites that are currently located in the same level as the focus sprite.
        Designed for handling light levels'''
        loaded_sprites = cls.loaded_locals + [i for i in cls.global_sprites if i.level == cls.focus.level]
        
        loaded_sprites.sort(key=lambda kv: kv.rect.center[1])
        for s in loaded_sprites:
            s.animation.rect.bottomleft = (s.x, s.y + s.rect.height)
            disp_reg = (s.x + dispx, s.y + dispy - s.rect.height)
            lit_tiles = s.check_lit_tile(litmap)
            # Player is not touching any lit tiles, draw normally.
            if not lit_tiles:
                s.animation.draw(window, disp_reg)
            # Player is only touching lit tiles, draw illuminated backup.
            elif lit_tiles == 4:
                s.animation.draw_norm(window, disp_reg)
            # Player is partially touching lit tiles, 
            else:
                s.animation.draw_clipped(window, (dispx, dispy), disp_reg, lit_rects)
    
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
        '''Recalculate the list of loaded local sprites'''
        cls.loaded_locals = [i for i in cls.local_sprites if i.level == cls.focus.level]


# Subclass for sign sprites
class SignSprite(Sprite):

    def __init__(self, rect, animation_dict, behavour, level, scope, action='blank', action_args=None, health=None, max_health=None):
        Sprite.__init__(self, rect, animation_dict, behavour, level, "local", action, action_args, None, None)

    def __repr__(self):
        result ='''SignSprite:
                Collision Rectangle: {}
                Behavour: {}
                Name: {}
                Action: {}
                Action Arguments: {}'''.format(self.rect, self.behavour, self.name, self.action, self.action_args)
        try:
            result += '\nInhabited Level: {}'.format(self.level)
        except:
            pass
        return result

    # Execute the behavour of the sign sprite
    def behave(self):
        self.behavour(self)

    # Normal standing behavour
    def stand(self):
        pass


# Subclass for NPC sprites
class NPCSprite(Sprite):

    def __init__(self, rect, animation_dict, behavour, level, scope, action='blank', action_args=None, health=None, max_health=None):
        Sprite.__init__(self, rect, animation_dict, behavour, level, scope, action, action_args, health, max_health)
        self.interval = 25
        self.cycle = 0 
        self.facing = Tracker("front")
        self.direction = Tracker(None)
        self.dx = 0
        self.dy = 0

    def __repr__(self):
        result ='''NPCSprite:
                Collision Rectangle: {}
                Behavour: {}
                Action: {}
                Action Arguments: {}
                Health: {}'''.format(self.rect, self.behavour, self.action, self.action_args, self.health)
        try:
            result += '\nInhabited Level: {}'.format(self.level)
        except:
            pass
        return result

    # Execute behavour of the NPC sprite
    def behave(self):
        self.behavour(self)

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
        time_step = Sprite.behavour_args['time_step']
        self.cycle += time_step
        if self.cycle <= 80:
            self.movement(tilemap, colliders, time_step)
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
        time_step = Sprite.behavour_args['time_step']
        self.cycle += time_step
        if self.cycle <= 64:
            self.movement(tilemap, colliders, 1.5 * time_step)
        else:
            self.animation.reset()

    # Behavour of NPC to always move right
    def always_right(self):
        tilemap = self.level.tilemap
        colliders = self.level.colliders
        self.dx = 1
        self.dy = 0
        time_step = Sprite.behavour_args['time_step']
        self.movement(tilemap, colliders, 1.5 * time_step)
        
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

        if moved == False:
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
    
    def __init__(self, rect, animation_dict, behavour, level, health=None, max_health=None):
        Sprite.__init__(self, rect, animation_dict, behavour, level, "global", health=health, max_health=max_health)
        self.facing = Tracker("front")
        self.direction = Tracker(None)

    def __repr__(self):
        return '''PlayerSprite:
                Collision Rectangle: {}
                Health: {}
                Level: <{}>'''.format(self.rect, self.health, str(self.level))

    # Execute the behavour of the player sprite
    def behave(self):
        self.behavour(self)

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
        
        if keys[pygame.K_LSHIFT]:
            speed = time_step * 1.25
        else:
            speed = 2.25 * time_step
            
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

        if player_moved == False:
            self.animation.reset()
        else:
            if self.direction.querry() or self.facing.querry():
                if self.direction.value:
                    self.animation = self.animation_dict[self.direction.value]
                else:
                    self.animation = self.animation_dict[self.facing.value]

            self.animation.update(speed / 2)
            self.rect.move_ip(round(self.x - self.rect.x), round(self.y - self.rect.y))

    # Regular player behavour
    def normal(self):
        keys = Sprite.behavour_args['keys']
        time_step = Sprite.behavour_args['time_step']
        tilemap = self.level.tilemap
        colliders = self.level.colliders
        self.movement((keys, time_step, tilemap, colliders))
