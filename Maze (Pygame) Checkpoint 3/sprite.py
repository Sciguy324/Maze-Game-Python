import pygame
import os
import ast
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

# Class for animations
class Animation:

    def __init__():
        pass

# Main class for sprites
class Sprite:
    global_sprites = []
    local_sprites = []
    loaded_locals = []
    focus = None
    
    behavour_args = {}

    def __init__(self, rect, images, behavour, level, scope, action='blank', action_args=None, health=None, max_health=None):
        self.frame = 0
        self.interval = 50
        self.health = health
        self.rect = rect
        self.x = int(rect.x)
        self.y = int(rect.y)
        self.images = dict((v, pygame.image.load(os.path.join(k)).convert_alpha()) for v, k in images.items())
        self.sprite = list(self.images.items())[0][1]
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
    def blit_all(cls, displacement, window):
        '''Blit all sprites that are currently located in the same level as the focus sprite'''
        loaded_sprites = cls.loaded_locals + [i for i in cls.global_sprites if i.level == cls.focus.level]
        
        loaded_sprites.sort(key=lambda kv: kv.rect.center[1])
        for s in loaded_sprites:
            window.blit(s.sprite, (s.x + displacement[0], s.y + displacement[1] - s.rect.height))
            #window.fill((127, 0, 0), s.rect.move(displacement))

    @classmethod
    def reload_loaded_locals(cls):
        '''Recalculate the list of loaded local sprites'''
        cls.loaded_locals = [i for i in cls.local_sprites if i.level == cls.focus.level]


# Subclass for sign sprites
class SignSprite(Sprite):

    def __init__(self, rect, images, behavour, level, scope, action='blank', action_args=None, health=None, max_health=None):
        Sprite.__init__(self, rect, images, behavour, level, "local", action, action_args, None, None)

    def __repr__(self):
        result ='''SignSprite:
                Collision Rectangle: {}
                Images: {}
                Behavour: {}
                Name: {}
                Action: {}
                Action Arguments: {}'''.format(self.rect, list(i for i in self.images), self.behavour, self.name, self.action, self.action_args)
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

    def __init__(self, rect, images, behavour, level, scope, action='blank', action_args=None, health=None, max_health=None):
        Sprite.__init__(self, rect, images, behavour, level, scope, action, action_args, health, max_health)
        self.interval = 25
        self.cycle = 0 
        self.facing = "front"
        self.direction = None
        self.dx = 0
        self.dy = 0

    def __repr__(self):
        result ='''NPCSprite:
                Collision Rectangle: {}
                Images: {}
                Behavour: {}
                Action: {}
                Action Arguments: {}
                Health: {}'''.format(self.rect, list(i for i in self.images), self.behavour, self.action, self.action_args, self.health)
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
        self.cycle += 1.0 * time_step
        if self.cycle <= 80:
            self.movement(tilemap, colliders, time_step)
        else:
            self.frame = 0
        PlayerSprite.update_frame(self)

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
        self.cycle += 1.0 * time_step
        if self.cycle <= 64:
            self.movement(tilemap, colliders, 1.5 * time_step)
        else:
            self.frame = 0
        PlayerSprite.update_frame(self)

    # Behavour of NPC to always move right
    def always_right(self):
        tilemap = self.level.tilemap
        colliders = self.level.colliders
        self.dx = 1
        self.dy = 0
        time_step = Sprite.behavour_args['time_step']
        self.movement(tilemap, colliders, 1.5 * time_step)
        PlayerSprite.update_frame(self)
        
    # Standard NPC movement
    def movement(self, tilemap, colliders, time_step):
        dx, dy = 0, 0
        speed = 1.0 * time_step
        moved = False
        
        if self.dy == -1:
            dy -= speed
            self.facing = "back"
            self.direction = None
            moved = True
            
        if self.dy == 1:
            dy += speed
            self.facing = "front"
            self.direction = None
            moved = True
            
        if self.check_collision(0, dy, tilemap, colliders):
            self.y += dy
        else:
            dy = 0
            self.cycle = 80
            
        if self.dx == -1:
            dx -= speed
            self.direction = "left"
            moved = True
            
        if self.dx == 1:
            dx += speed
            self.direction = "right"
            moved = True
            
        if self.check_collision(dx, 0, tilemap, colliders):
            self.x += dx
        else:
            dx = 0
            self.cycle = 80

        if moved == False or self.frame > self.interval * 4:
            self.frame = 0
        else:
            self.frame += speed * 1.5
            self.rect.move_ip(round(self.x - self.rect.x), round(self.y - self.rect.y))


# Subclass for player sprite
class PlayerSprite(Sprite):
    
    def __init__(self, rect, images, behavour, level, health=None, max_health=None):
        Sprite.__init__(self, rect, images, behavour, level, "global", health=health, max_health=max_health)
        self.facing = "front"
        self.direction = None

    def __repr__(self):
        return '''PlayerSprite:
                Collision Rectangle: {}
                Images: {}
                Health: {}
                Level: <{}>'''.format(self.rect, list(i for i in self.images), self.health, str(self.level))

    # Execute the behavour of the player sprite
    def behave(self):
        self.behavour(self)

    # Determine which frame should be shown
    def update_frame(self):
        if self.facing == "front":
            if self.direction == "left":
                if 0 <= self.frame < self.interval:
                    self.sprite = self.images["left"]
                elif self.interval <= self.frame < self.interval * 2:
                    self.sprite = self.images["left_walk1"]
                elif self.interval * 2 <= self.frame < self.interval * 3:
                    self.sprite = self.images["left"]
                else:
                    self.sprite = self.images["left_walk2"]
            elif self.direction == "right":
                if 0 <= self.frame < self.interval:
                    self.sprite = self.images["right"]
                elif self.interval <= self.frame < self.interval * 2:
                    self.sprite = self.images["right_walk1"]
                elif self.interval * 2 <= self.frame < self.interval * 3:
                    self.sprite = self.images["right"]
                else:
                    self.sprite = self.images["right_walk2"]
            else:
                if 0 <= self.frame < self.interval:
                    self.sprite = self.images["front"]
                elif self.interval <= self.frame < self.interval * 2:
                    self.sprite = self.images["front_walk1"]
                elif self.interval * 2 <= self.frame < self.interval * 3:
                    self.sprite = self.images["front"]
                else:
                    self.sprite = self.images["front_walk2"]
        else:
            if self.direction == "left":
                if 0 <= self.frame < self.interval:
                    self.sprite = self.images["left"]
                elif self.interval <= self.frame < self.interval * 2:
                    self.sprite = self.images["left_walk1"]
                elif self.interval * 2 <= self.frame < self.interval * 3:
                    self.sprite = self.images["left"]
                else:
                    self.sprite = self.images["left_walk2"]
            elif self.direction == "right":
                if 0 <= self.frame < self.interval:
                    self.sprite = self.images["right"]
                elif self.interval <= self.frame < self.interval * 2:
                    self.sprite = self.images["right_walk1"]
                elif self.interval * 2 <= self.frame < self.interval * 3:
                    self.sprite = self.images["right"]
                else:
                    self.sprite = self.images["right_walk2"]
            else:
                if 0 <= self.frame < self.interval:
                    self.sprite = self.images["back"]
                elif self.interval <= self.frame < self.interval * 2:
                    self.sprite = self.images["back_walk1"]
                elif self.interval * 2 <= self.frame < self.interval * 3:
                    self.sprite = self.images["back"]
                else:
                    self.sprite = self.images["back_walk2"]

    # Player sprite movement
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
            self.facing = "back"
            self.direction = None
            player_moved = True
            
        if keys[pygame.K_s]:
            dy += speed
            self.facing = "front"
            self.direction = None
            player_moved = True
            
        if self.check_collision(0, dy, tilemap, colliders):
            self.y += dy
            
        if keys[pygame.K_a]:
            dx -= speed
            self.direction = "left"
            player_moved = True
            
        if keys[pygame.K_d]:
            dx += speed
            self.direction = "right"
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

        if player_moved == False or self.frame > self.interval * 4:
            self.frame = 0
        else:
            self.frame += speed / 2
            self.rect.move_ip(round(self.x - self.rect.x), round(self.y - self.rect.y))
        self.update_frame()

    # Regular player behavour
    def normal(self):
        keys = Sprite.behavour_args['keys']
        time_step = Sprite.behavour_args['time_step']
        tilemap = self.level.tilemap
        colliders = self.level.colliders
        self.movement((keys, time_step, tilemap, colliders))
