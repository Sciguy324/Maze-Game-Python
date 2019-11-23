import pygame
import os
from worlds import *
from sys import platform
from sprite import *

# If the platform is windows, ensure that the system is not stretching the game window to the display.
if platform == "win32":
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    os.environ['SDL_VIDEODRIVER'] = 'directx'

# Pygame initialization
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

# Window settup
win_width = 64 * 16
win_height = 64 * 9
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Maze")
icon = pygame.image.load(os.path.join('assets', 'icon.bmp'))
pygame.display.set_icon(icon)

missing = pygame.image.load(os.path.join('tiles/missing.png'))
missing = pygame.transform.scale(missing, (64, 64)).convert()

# Dialog system initialization
Dialog.dialog_init((win_width, win_height), win)


def draw_tilemap(tiles, ids, window, disp, deco=False):
    '''Function to draw tilemap.  Only draws visible area.'''
    x_tile = int(abs(disp[0] / 64))
    y_tile = int(abs(disp[1] / 64))
    y = -64
    for i in tiles[y_tile:y_tile + 10]:
        y += 64
        x = -64
        for j in i[x_tile:x_tile + 17]:
            x += 64
            if j in ids:
                window.blit(ids[j], (x + disp[0] + x_tile * 64, y + disp[1] + y_tile * 64))
                if deco:
                    pass
    return window

def illuminate(window, disp, light, sources):
    '''Function to draw tilemap'''
    for i in sources:
        window.blit(light, (i[0] * 64 + disp[0] - 64, i[1] * 64 + disp[1] - 64))
    return window

def center_at(user, world_width, world_height):
    '''Function to center the screen on the player'''
    dispx = max(min(win_width / 2 - user.x, 0), win_width - world_width)
    dispy = max(min(win_height / 2 - user.y, 0), win_height - world_height)
    return (dispx, dispy)

def check_zone(user, loading_zones):
    '''Function to check if a rectangle is inside a loading zone'''
    x, y = user.rect.center
    x = int(x / 64)
    y = int(y / 64)
    if (x, y) in loading_zones:
        return loading_zones[(x, y)]
    return None

def wipe_screen(wipe, screenshot):
    '''Function to wipe the screen black.  Requires copy of the screen'''
    temp_clock = pygame.time.Clock()
    scaled_wipe = pygame.transform.scale(wipe, (win.get_width(), win.get_height() * 2))
    scaled_screenshot = pygame.transform.scale(screenshot, (win.get_width(), win.get_height()))
    i = 0
    while i < win.get_height() * 2:
        win.blit(scaled_screenshot, (0, 0))
        win.blit(scaled_wipe, (0, win.get_height() - i))
        pygame.display.flip()
        time_step = min(temp_clock.tick() / 10, 10) * 24
        i += time_step

def unwipe_screen(wipe, screenshot):
    '''Function to unwipe the screen.  Requires a copy of screen without any wiping effect'''
    temp_clock = pygame.time.Clock()
    scaled_wipe = pygame.transform.scale(wipe, (win.get_width(), win.get_height() * 2))
    scaled_screenshot = pygame.transform.scale(screenshot, (win.get_width(), win.get_height()))
    i = 0
    while i < win.get_height() * 2:
        win.blit(scaled_screenshot, (0, 0))
        win.blit(scaled_wipe, (0, 0 - i))
        pygame.display.flip()
        time_step = min(temp_clock.tick() / 10, 10) * 24
        i += time_step


def play_level(start, tilemap, decomap, loading_zones, full, data):
    '''Play a level, requires starting position of player and map of level'''
    global win
    # Internal window
    win2 = pygame.Surface((win_width, win_height))
    Dialog.internal_window = win2
    # Player bounding box
    player = pygame.Rect(start[0] * 64, start[1] * 64, 48, int(112/2))
    # Player sprites
    player_images = {"front": 'assets/player/player_front.png',
                     "front_walk1": 'assets/player/player_front_walk1.png',
                     "front_walk2": 'assets/player/player_front_walk2.png',
                     "back": 'assets/player/player_back.png',
                     "back_walk1": 'assets/player/player_back_walk1.png',
                     "back_walk2": 'assets/player/player_back_walk2.png',
                     "left": 'assets/player/player_left.png',
                     "left_walk1": 'assets/player/player_left_walk1.png',
                     "left_walk2": 'assets/player/player_left_walk2.png',
                     "right": 'assets/player/player_right.png',
                     "right_walk1": 'assets/player/player_right_walk1.png',
                     "right_walk2": 'assets/player/player_right_walk2.png'
                     }
    # Default player sprite data
    player_sprite = PlayerSprite(player, player_images, PlayerSprite.normal, health=data['health'])

    Sprite.behavour_args = {'tilemap': tilemap,
                            'collisions': collisions
                            }
    
    # Misc.
    world_width = 64 * len(tilemap[1])
    world_height = 64 * len(tilemap)
    displacement = center_at(player, world_width, world_height)
    time_step = 1
    clock = pygame.time.Clock()

    timer = pygame.time.Clock()     # For measuring how long various lines are taking to run.
    time_taken = 0                  # For recording the above

    # Nightime-shading setup
    shade = pygame.Surface((win_width, win_height))
    shade.set_alpha(128)
    shade.fill((0, 0, 27))
    # Light source setup
    light = pygame.image.load(os.path.join('assets/light.png')).convert_alpha()
    # Screen wipe setup
    wipe_up = pygame.image.load(os.path.join('assets/wipe_up.png')).convert_alpha()
    wipe_down = pygame.image.load(os.path.join('assets/wipe_down.png')).convert_alpha()
    first_time = True   # Allows screen un-wipe to trigger once.
    # Light sources setup
    night = False
    light_sources = []
    y = -1
    for i in decomap:
        y +=1
        x = -1
        for j in i:
            x += 1
            if j == 1:
                light_sources.append((x, y))

    # Main loop
    done = False
    while not done:
        timer.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, None, None, full, data
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    return True, None, None, full, data
                elif event.key == pygame.K_F11:
                    full = not(full)
                    if full:
                        win = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        win = pygame.display.set_mode((win_width, win_height))
                elif event.key == pygame.K_f:
                    try:
                        print(1000 / time_taken, "fps. Fullscreen:", full, "Night:", night)
                        #print(timer.get_fps(), "fps. Fullscreen:", full, "Night:", night)
                        #print(time_taken, "ms. Fullscreen:", full, "Night:", night)
                    except ZeroDivisionError:
                        print("Failed to compute")
                elif event.key == pygame.K_z:
                    night = True
                elif event.key == pygame.K_x:
                    night = False

        # Player movement via keyboard input
        keys = pygame.key.get_pressed()

        # Update internal window.
        Sprite.behavour_args['keys'] = keys
        Sprite.behavour_args['time_step'] = time_step
        Sprite.behave_all()
        
        displacement = center_at(player, world_width, world_height)        
        win2 = draw_tilemap(tilemap, tile_ids, win2, displacement) # 6-7 ms       
        Sprite.blit_all(displacement, win2)
        win2 = draw_tilemap(decomap, deco_ids, win2, displacement, deco=True) # 0-1 ms

        if night:   # 3-4 ms, 5-6 ms if light sources are present
            win2.blit(shade, (0, 0)) # 3-4 ms
            win2 = illuminate(win2, displacement, light, light_sources) # 0 ms, 1 ms if light sources are present

        # Transfer internal window to displayed window and update screen.
        pygame.transform.scale(win2, (win.get_width(), win.get_height()), win) # 2-3 ms

        if first_time:
            first_time = False
            unwipe_screen(wipe_down, win2)

        pygame.display.flip() # 1-2 ms

        time_step = min(clock.tick_busy_loop(60) / 10, 2.5)

        # Check player position for loading zone.
        # If loading zone is found, end this level so the next can be loaded.
        current_zone = check_zone(player_sprite, loading_zones)
        if current_zone:
            wipe_screen(wipe_up, win2)
            data['health'] = player_sprite.health
            return False, current_zone[0], current_zone[1], full, data
        time_taken = timer.tick()
        

if __name__ == "__main__":
        print("Debug Controls:")
        print("\t-z: Night")
        print("\t-x: Day")
        print("\t-f: Print framerate")
        print("\t-Backspace: Stop game")
        print("\nTodo:")
        print("\t-Drastically rework sprite and level systems")
        print("\t-Animated tiles")
        print("\t-Expansion of sprite system")
        print("\t\t-Add more behaviours")
        print("\t\t-Combat system")
        # Starting level and position
        level = demo
        start = (12, 10)
        game_stop = False
        fullscreen = False
        data = {'health': 100}
        while not game_stop:
            Sprite.clear()
            tile_ids, tilemap, deco_ids, decomap, collisions, loading_zones, = level()
            game_stop, level, start, fullscreen, data = play_level(start, tilemap, decomap, loading_zones, fullscreen, data)
            
            # Update persistant sprites upon level end.
            for i in Sprite.instances:
                try:
                    Sprite.persists[i.name]['rect'] = str(i.rect.topleft + i.rect.size)
                    Sprite.persists[i.name]['level'] = self.level
                    Sprite.persists[i.name]['behavour'] = self.behavour
                    Sprite.persists[i.name]['action'] = self.action.__name__
                    Sprite.persists[i.name]['action_args'] = self.action_args
                    Sprite.persists[i.name]['health'] = self.health
                    Sprite.persists[i.name]['max_health'] = self.max_health
                except:
                    pass

pygame.quit()
