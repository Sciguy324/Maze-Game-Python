import pygame
import os
from sys import platform
import matplotlib.pyplot as plt
import time

# Pygame initialization
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

# If the platform is windows, ensure that the system is not stretching the game window to the display.
if platform == "win32":
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    os.environ['SDL_VIDEODRIVER'] = 'directx'
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

# Window settup
win_width = 64 * 16
win_height = 64 * 9
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Maze")
icon = pygame.image.load(os.path.join('assets', 'icon.bmp'))
pygame.display.set_icon(icon)

# Worlds module must be called after the window mode is set, and sprite module depends on worlds module.
from worlds import *
from sprite import *

#missing = pygame.image.load(os.path.join('tiles/missing.png'))
#missing = pygame.transform.scale(missing, (64, 64)).convert()

# Dialog system initialization
Dialog.dialog_init((win_width, win_height), win)


def draw_tilemap(tiles, window, dispx, dispy, litmap, deco=False):
    '''Function to draw tilemap.  Only draws visible area.'''
    if deco:
        id_list = Level.deco_ids
    else:
        id_list = Level.tile_ids
    x_tile = int(abs(dispx / 64))
    y_tile = int(abs(dispy / 64))
    y = y_tile - 1
    for i in tiles[y_tile:y_tile + 10]:
        y += 1
        x = x_tile - 1
        for j in i[x_tile:x_tile + 17]:
            x += 1
            if j in id_list:
                if litmap[y][x]:
                    id_list[j].draw_norm(window, (dispx + x * 64, dispy + y * 64))
                else:
                    id_list[j].draw(window, (dispx + x * 64, dispy + y * 64))
    return window

def stitch_tilemap(lvl, dispx, dispy, deco=False):
    '''Function to stitch tiles together into a single image, as defined by a tilemap matrix.'''
    if deco:
        id_list = Level.deco_ids
        lvl_map = lvl.decomap
    else:
        id_list = Level.tile_ids
        lvl_map = lvl.tilemap
    result = pygame.Surface((lvl.width, lvl.height))
    y = -64
    for i in lvl.tilemap:
        y += 64
        x = -64
        for j in i:
            x += 64
            if j in id_list:
                (id_list[j]).draw(result, (x, y))
    return result

def generate_litmap(lightmap, tilemap):
    '''Generate a reference map for illuminated tiles'''
    row = list(0 for i in range(len(tilemap[0])))
    matrix = list(list(row) for i in range(len(tilemap)))
    rects = []
    for x, y in lightmap:
        for i in range(-1, 2):
            for j in range(-1, 2):
                matrix[max(y + j, 0)][max(x + i, 0)] = 1
        rects.append(pygame.Rect((x - 1) * 64, (y - 1) * 64, 192, 192))
    return matrix, rects

def illuminate(window, lightmap, dispx, dispy, light):
    '''Draw light sources using the lightmap'''
    x_tile = int(abs(dispx / 64))
    y_tile = int(abs(dispy / 64))
    for x, y in lightmap:
        if x in range(x_tile, x_tile + 17) and y in range(y_tile, y_tile + 10):
            window.blit(light, (dispx + (x - 1) * 64, dispy + (y - 1) * 64), special_flags=pygame.BLEND_SUB)

def center_at(userx, usery, world_width, world_height):
    '''Function to center the screen on the player'''
    dispx = max(min(win_width / 2 - userx, 0), win_width - world_width)
    dispy = max(min(win_height / 2 - usery, 0), win_height - world_height)
    return dispx, dispy

def wipe_basic(wipe, screenshot, start):
    '''Function to either wipe or unwipe the screen black, depending on the argument.
    start = 0: wipe
    start = win.get_height(): unwipe
    Requires copy of the screen.'''
    scaled_wipe = pygame.transform.scale(wipe, (win.get_width(), win.get_height() * 2))
    scaled_screenshot = pygame.transform.scale(screenshot, (win.get_width(), win.get_height()))
    i = 0
    while i < win.get_height() * 2:
        t1 = time.perf_counter_ns()
        win.blit(scaled_screenshot, (0, 0))
        win.blit(scaled_wipe, (0, start - i))
        pygame.display.flip()
        time_step = (time.perf_counter_ns() - t1) / 600000
        i += time_step * win.get_height() / win_height

def play_level(start_level):
    '''Play a level, requires starting position of player and map of level'''
    global win
    global step_list
    # Internal window
    win2 = pygame.Surface((win_width, win_height))
    Dialog.internal_window = win2
    full = False

    # Setup all sprites
    player_sprite = sprite_setup(start_level)
    Sprite.focus = player_sprite
    
    # Misc.
    dispx, dispy = center_at(Sprite.focus.rect.x, Sprite.focus.rect.y, Sprite.focus.level.width, Sprite.focus.level.height)
    time_step = 1
    clock = pygame.time.Clock()
    time_taken = 0

    # Nightime-shading setup
    light_area = pygame.image.load(os.path.join('assets/light.png')).convert_alpha()
    light = pygame.Surface((192, 192))
    light.fill((100, 100, 100))
    light.blit(light_area, (0, 0))
    light.convert()
    litmap, lit_rects = generate_litmap(Sprite.focus.level.lightmap, Sprite.focus.level.tilemap)
    night = False
    
    # Screen wipe setup
    wipe_up = pygame.image.load(os.path.join('assets/wipe_up.png')).convert_alpha()
    wipe_down = pygame.image.load(os.path.join('assets/wipe_down.png')).convert_alpha()
    Sprite.behavour_args["screen_wipe"] = True
    
    # Main loop
    done = False
    while not done:
        time_start = time.perf_counter_ns()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    return
                elif event.key == pygame.K_F11:
                    full = not(full)
                    if full:
                        win = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        win = pygame.display.set_mode((win_width, win_height))
                elif event.key == pygame.K_f:
                    print(1000 / time_taken, "fps. Fullscreen:", full, "Night:", night)
                elif event.key == pygame.K_z:
                    night = True
                elif event.key == pygame.K_x:
                    night = False
                elif event.key == pygame.K_n:
                    Level.darken_imgs(100)
                    Sprite.darken_all(100)
                elif event.key == pygame.K_m:
                    Level.reset_imgs()
                    Sprite.reset_imgs()

        # Get keyboard input for sprite arguments
        keys = pygame.key.get_pressed()

        # Update internal window.
        Sprite.behavour_args['keys'] = keys
        Sprite.behavour_args['time_step'] = time_step
        Sprite.behave_all()

        # Wipe the screen if the player changed zone.
        if Sprite.behavour_args['screen_wipe']:
            wipe_basic(wipe_up, win2, win.get_height())
            Sprite.reload_loaded_locals()
            litmap, lit_rects = generate_litmap(Sprite.focus.level.lightmap, Sprite.focus.level.tilemap)
            #world_image = stitch_tilemap(Sprite.focus.level, dispx, dispy)
            #world_image.convert()

        dispx, dispy = center_at(Sprite.focus.x, Sprite.focus.y, Sprite.focus.level.width, Sprite.focus.level.height)
        win2 = draw_tilemap(Sprite.focus.level.tilemap, win2, dispx, dispy, litmap) # 6-7 ms
        #win2.blit(world_image, dispx, dispy, area=pygame.Rect(0, 0, win_width, win_height).move_ip(dispx, dispy))
        if night:
            Sprite.blit_all_night(dispx, dispy, win2, litmap, lit_rects)
            win2 = draw_tilemap(Sprite.focus.level.decomap, win2, dispx, dispy, litmap, deco=True)
            illuminate(win2, Sprite.focus.level.lightmap, dispx, dispy, light)            
        else:
            Sprite.blit_all(dispx, dispy, win2)
            win2 = draw_tilemap(Sprite.focus.level.decomap, win2, dispx, dispy, litmap, deco=True)
        
        # Transfer internal window to displayed window and update screen.
        pygame.transform.scale(win2, (win.get_width(), win.get_height()), win) # 2-3 ms

        if Sprite.behavour_args['screen_wipe']:
            wipe_basic(wipe_down, win2, 0)
            Sprite.behavour_args['screen_wipe'] = False
        pygame.display.flip()
        #step_list.append((time.perf_counter_ns() - time_start2) / 1000000)
        #timer.tick()
        if keys[pygame.K_v]:
            time_step = min(clock.tick(60) / 10, 2.5)
        else:
            time_taken = time.perf_counter_ns() - time_start
            time_taken_ms = time_taken / 1000000
            time_step = min(time_taken_ms / 9, 12)

        Tile.advance_frame(time_step)
        step_list.append(time_step)

step_list = []

if __name__ == "__main__":
    print("Debug Controls:")
    print("\t-z: Night")
    print("\t-x: Day")
    print("\t-f: Print framerate")
    print("\t-v: Hold for old time-step calculation")
    print("\t-Backspace: Stop game")
    print("\nTodo:")
    print("\t-Animate more tiles")
    print("\t-Add more to sprite system")
    print("\t\t-Add more behaviours")
    print("\t-Transfer sprite drawing responcibilty to Animation class")
    print("\t\t-This will be important for clipped sprite lighting")
    play_level(demo)

pygame.quit()

if len(step_list) > 0:
    step_list.pop(0)
    print("Average Value:", sum(step_list) / len(step_list))
    graph = plt.figure()
    graph.suptitle('Timestep Each Tick')
    plt.plot(step_list, label="Timestep")
    plt.legend()
    plt.show()
