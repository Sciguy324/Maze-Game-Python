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

# Main class for sprites
class Sprite:
    instances = []
    behavour_args = {}
    persists = {}

    def __init__(self, rect, images, behavour, name=None, action='blank', action_args=None, level='test', health=None, max_health=None):
        self.frame = 0
        self.interval = 20
        self.health = health
        if name:
            if name in Sprite.persists:
                if Sprite.persists[name]['level'] != level:     # Abort construction if persistent is not in the level being loaded4
                    return
                sprite_type = Sprite.persists[name]['type']
                r = ast.literal_eval(Sprite.persists[name]['rect'])
                s_rect = pygame.Rect(r)
                s_imgs = ast.literal_eval(Sprite.persists[name]['images'])
                s_behave = Sprite.persists[name]['behavour']
                s_action = Sprite.persists[name]['action']
                s_action_args = Sprite.persists[name]['action_args']
                s_health = Sprite.persists[name]['health']
                s_max_health = Sprite.persists[name]['max_health']
                if sprite_type == 'SignSprite':
                    full_sprite = SignSprite(s_rect, s_imgs, s_behave, action=s_action, action_args=s_action_args, level=level, health=s_health, max_health=s_max_health)
                elif sprite_type == 'NPCSprite':
                    full_sprite = NPCSprite(s_rect, s_imgs, s_behave, action=s_action, action_args=s_action_args, level=level, health=s_health, max_health=s_max_health)
                full_sprite.name = name
                if not full_sprite in Sprite.instances:
                    Sprite.instances.append(full_sprite)
                return
        self.rect = rect
        self.images = dict((v, pygame.image.load(os.path.join(k)).convert_alpha()) for v, k in images.items())
        self.sprite = list(self.images.items())[0][1]
        self.freeze = False
        self.behavour = behavour
        self.action = action_lookup[action]
        self.action_args = action_args
        if name:
            self.name = name
            Sprite.persists[name] = {'images': str(images),
                                     'rect': str(rect.topleft + rect.size),
                                     'level': level,
                                     'behavour': behavour,
                                     'action': action,
                                     'action_args': action_args,
                                     'health': health,
                                     'max_health': max_health}
        Sprite.instances.append(self)

    def __repr__(self):
        '''Override in subclass'''
        pass

    def __str__(self):
        Sprite.__repr__(self)

    def check_collision(rect, dx, dy, tilemap, collider_ids):
        '''Function to check if a sprite rectange has collided with something'''
        try:
            new_rect = rect.move(dx, dy)
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
            if Sprite.check_sprites_collide(rect, dx, dy) != None:
                return False
            return True
        except IndexError:
            return False

    def behave(self):
        '''Function to execute the behavour of sprites.  Override in subclass'''
        pass
        
    #def movement(self, args):
    #    '''Function to control how the sprite moves.  Override in subclasses'''
    #    pass

    @classmethod
    def freeze(cls, state):
        '''Set the freeze state of all sprites'''
        for instance in cls.instances:
            instance.freeze = state

    @classmethod
    def check_sprites_collide(cls, entity, dx, dy):
        '''Function to check if a sprite has collided with another sprite, and if so, return that sprite'''
        other_rects = list(instance.rect for instance in cls.instances if instance.rect != entity)
        index = entity.move(dx, dy).collidelist(other_rects)
        if index == -1:
            return None
        return other_rects[index]
        
    @classmethod
    def behave_all(cls):
        '''Function to execute the behavour of all sprites'''
        for instance in cls.instances:
            instance.behave()

    @classmethod
    def blit_all(cls, displacement, window):
        cls.instances.sort(key=lambda kv: kv.rect.center[1])
        for instance in cls.instances:
            window.blit(instance.sprite, (instance.rect.x + displacement[0], instance.rect.y + displacement[1] - instance.rect.height))
            #window.fill((127, 0, 0), instance.rect.move(displacement))
    
    @classmethod
    def clear(cls):
        '''Delete sprite instances'''
        cls.instances = []


# Subclass for sign sprites
class SignSprite(Sprite):

    def __init__(self, rect, images, behavour, name=None, action='blank', action_args=None, level='test', health=None, max_health=None):
        Sprite.__init__(self, rect, images, behavour, name, action, action_args, level, None, None)
        if name:
            Sprite.persists[name]['type'] = 'SignSprite'

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

    def __init__(self, rect, images, behavour, name=None, action='blank', action_args=None, level='test', health=None, max_health=None):
        Sprite.__init__(self, rect, images, behavour, name, action, action_args, level, health, max_health)
        self.interval = 10
        self.cycle = 0 
        self.facing = "front"
        self.direction = None
        self.dx = 0
        self.dy = 0
        if name:
            Sprite.persists[name]['type'] = 'NPCSprite'

    def __repr__(self):
        result ='''NPCSprite:
                Collision Rectangle: {}
                Images: {}
                Behavour: {}
                Name: {}
                Action: {}
                Action Arguments: {}
                Health: {}'''.format(self.rect, list(i for i in self.images), self.behavour, self.name, self.action, self.action_args, self.health)
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
        tilemap = Sprite.behavour_args['tilemap']
        collisions = Sprite.behavour_args['collisions']
        if self.cycle > 384:
            self.cycle = 0
            self.dx = random.randint(-1, 1)
            self.dy = random.randint(-1, 1)
            if not Sprite.check_collision(self.rect, self.dx * 64, self.dy * 64, tilemap, collisions):
                self.dx, self.dy = 0, 0
                self.cycle = 385
        time_step = Sprite.behavour_args['time_step']
        self.cycle += 1.0 * time_step
        if self.cycle <= 80:
            self.movement(tilemap, collisions, time_step)
        else:
            self.frame = 0
        PlayerSprite.update_frame(self)

    # Behavour of NPC to panic aimlessly
    def panic(self):
        tilemap = Sprite.behavour_args['tilemap']
        collisions = Sprite.behavour_args['collisions']
        if self.cycle > 64:
            self.cycle = 0
            self.dx, self.dy = 0, 0
            while self.dx == 0 and self.dy == 0:
                self.dx = random.randint(-1, 1)
                self.dy = random.randint(-1, 1)
            if not Sprite.check_collision(self.rect, self.dx, self.dy, tilemap, collisions):
                self.dx, self.dy = 0, 0
                self.cycle = 65
        time_step = Sprite.behavour_args['time_step']
        self.cycle += 1.0 * time_step
        if self.cycle <= 64:
            self.movement(tilemap, collisions, 1.5 * time_step)
        else:
            self.frame = 0
        PlayerSprite.update_frame(self)

    # Standard NPC movement
    def movement(self, tilemap, collisions, time_step):
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
            
        if Sprite.check_collision(self.rect, 0, dy, tilemap, collisions):
            self.rect.move_ip(0, dy)
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
            
        if Sprite.check_collision(self.rect, dx, 0, tilemap, collisions):
            self.rect.move_ip(dx, 0)
        else:
            dx = 0
            self.cycle = 80

        if moved == False or self.frame > self.interval * 4:
            self.frame = 0
        else:
            self.frame += round(speed / 7) + 1


# Subclass for player sprite
class PlayerSprite(Sprite):
    
    def __init__(self, rect, images, behavour, name=None, health=None, max_health=None):
        Sprite.__init__(self, rect, images, behavour, None, health=health, max_health=max_health)
        self.facing = "front"
        self.direction = None

    def __repr__(self):
        return '''PlayerSprite:
                Collision Rectangle: {}
                Images: {}
                Health: {}'''.format(self.rect, list(i for i in self.images), self.health)

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
        collisions = args[3]
        dx = 0
        dy = 0
        player_moved = False
        
        if keys[pygame.K_LSHIFT]:
            speed = time_step * 1.5
        else:
            speed = 3 * time_step
            
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
            
        if Sprite.check_collision(self.rect, 0, dy, tilemap, collisions):
            self.rect.move_ip(0, dy)
            
        if keys[pygame.K_a]:
            dx -= speed
            self.direction = "left"
            player_moved = True
            
        if keys[pygame.K_d]:
            dx += speed
            self.direction = "right"
            player_moved = True
            
        if Sprite.check_collision(self.rect, dx, 0, tilemap, collisions):
            self.rect.move_ip(dx, 0)

        if player_moved == False or self.frame > self.interval * 4:
            self.frame = 0
        else:
            self.frame += round(speed / 7) + 1
        self.update_frame()

        # Trigger call for interact
        if keys[pygame.K_SPACE]:
            for instance in Sprite.instances:
                if type(instance) != PlayerSprite:
                    if self.rect.inflate(16, 16).colliderect(instance.rect):
                        instance.action(instance.action_args)
                        break

    # Regular player behavour
    def normal(self):
        keys = Sprite.behavour_args['keys']
        time_step = Sprite.behavour_args['time_step']
        tilemap = Sprite.behavour_args['tilemap']
        collisions = Sprite.behavour_args['collisions']
        self.movement((keys, time_step, tilemap, collisions))
