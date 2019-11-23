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


def draw_tilemap(tiles, window, disp, deco=False):
    '''Function to draw tilemap.  Only draws visible area.'''
    x_tile = int(abs(disp[0] / 64))
    y_tile = int(abs(disp[1] / 64))
    y = -64
    for i in tiles[y_tile:y_tile + 10]:
        y += 64
        x = -64
        for j in i[x_tile:x_tile + 17]:
            x += 64
            if deco:
                if j in Level.deco_ids:
                    Level.deco_ids[j].draw(window, (x + disp[0] + x_tile * 64, y + disp[1] + y_tile * 64))
            else:
                if j in Level.tile_ids:
                    Level.tile_ids[j].draw(window, (x + disp[0] + x_tile * 64, y + disp[1] + y_tile * 64))
    return window

def stitch_tilemap(lvl, disp, deco=False):
    '''Function to stitch tiles together into a single image, as defined by a tilemap matrix.'''
    result = pygame.Surface((lvl.width, lvl.height))
    y = -64
    for i in lvl.tilemap:
        y += 64
        x = -64
        for j in i:
            x += 64
            if deco:
                if j in Level.deco_ids:
                    (Level.deco_ids[j]).draw(result, (x, y))
            else:
                if j in Level.tile_ids:
                    (Level.tile_ids[j]).draw(result, (x, y))
    return result

def construct_lightmap(decomap, light):
    '''Construct a light map using the decomap'''
    shade = pygame.Surface((Sprite.focus.level.width, Sprite.focus.level.height))
    shade.fill((100, 100, 100))
    y = -1
    for i in decomap:
        y +=1
        x = -1
        for j in i:
            x += 1
            if j == 1:
                shade.blit(light, (x * 64 - 64, y * 64 - 64))
    shade.convert()
    return shade

def draw_lightmap(window, disp, decomap, tilemap, light):
    '''Draw out the light map using the decomap'''
    for y, i in enumerate(decomap):
        for x, j in enumerate(i):
            if j == 1:
                (Level.tile_ids[decomap[y][x]]).draw_backup(window, (x * 64 + disp[0], y * 64 + disp[1]))
                Level.deco_ids[j].draw_backup(window, (x * 64 + disp[0], y * 64 + disp[1]))
                window.blit(light, (x * 64 - 64 + disp[0], y * 64 - 64 + disp[1]), special_flags=pygame.BLEND_SUB)

def center_at(user, world_width, world_height):
    '''Function to center the screen on the player'''
    dispx = max(min(win_width / 2 - user[0], 0), win_width - world_width)
    dispy = max(min(win_height / 2 - user[1], 0), win_height - world_height)
    return (dispx, dispy)

def wipe_screen(wipe, screenshot):
    '''Function to wipe the screen black.  Requires copy of the screen'''
    scaled_wipe = pygame.transform.scale(wipe, (win.get_width(), win.get_height() * 2))
    scaled_screenshot = pygame.transform.scale(screenshot, (win.get_width(), win.get_height()))
    i = 0
    while i < win.get_height() * 2:
        t1 = time.perf_counter_ns()
        win.blit(scaled_screenshot, (0, 0))
        win.blit(scaled_wipe, (0, win.get_height() - i))
        pygame.display.flip()
        time_step = (time.perf_counter_ns() - t1) / 600000
        i += time_step * win.get_height() / win_height

def unwipe_screen(wipe, screenshot):
    '''Function to unwipe the screen.  Requires a copy of screen without any wiping effect'''
    scaled_wipe = pygame.transform.scale(wipe, (win.get_width(), win.get_height() * 2))
    scaled_screenshot = pygame.transform.scale(screenshot, (win.get_width(), win.get_height()))
    i = 0
    while i < win.get_height() * 2:
        t1 = time.perf_counter_ns()
        win.blit(scaled_screenshot, (0, 0))
        win.blit(scaled_wipe, (0, 0 - i))
        pygame.display.flip()
        time_step = (time.perf_counter_ns() - t1) / 600000
        i += time_step * win.get_height() / win_height

LIGHTSIZE = 192
NIGHTCOLOR = [0, 0, 0, 200]

def CreateLight():
    gradient = pygame.Surface([LIGHTSIZE, LIGHTSIZE], 0, 8)
    gradient.set_palette([[x, x, x] for x in range(256)])
    a = NIGHTCOLOR[3]
    gradient.fill((a, a, a))
    r = int(round(LIGHTSIZE/2))
    for i in range(r):
        c = (a * (r-i))/r
        pygame.draw.circle(gradient, [c, c, c], [r, r], r-i)
        c -= 1
    return gradient

def CreateNight():
    pic = pygame.Surface((win_width, win_height), pygame.SRCALPHA, 32).convert_alpha()
    pic.fill(NIGHTCOLOR)
    return pic

def CreateAlpha():
    pic = pygame.Surface((win_width, win_height), 0, 8)
    pic.set_palette([[x, x, x] for x in range(256)])
    a = NIGHTCOLOR[3]
    pic.fill([a, a, a])
    return pic

def RefreshNight(night, alpha, light, x, y):
    a = NIGHTCOLOR[3]
    alpha.fill([a, a, a])
    r = LIGHTSIZE/2
    alpha.blit(light, [x-r, y-r])
    pygame.surfarray.pixels_alpha(night)[:, :] = pygame.surfarray.pixels2d(alpha)
    
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
    displacement = center_at(Sprite.focus.rect, Sprite.focus.level.width, Sprite.focus.level.height)
    time_step = 1
    clock = pygame.time.Clock()
    time_taken = 0

    # Nightime-shading setup
    #light_area = pygame.image.load(os.path.join('assets/light.png')).convert_alpha()
    #light = pygame.Surface((192, 192))
    #light.fill((100, 100, 100))
    #light.blit(light_area, (0, 0))
    #light.convert()
    #shade = construct_lightmap(Sprite.focus.level.decomap, light)
    night = False
    
    # Screen wipe setup
    wipe_up = pygame.image.load(os.path.join('assets/wipe_up.png')).convert_alpha()
    wipe_down = pygame.image.load(os.path.join('assets/wipe_down.png')).convert_alpha()
    Sprite.behavour_args["screen_wipe"] = True

    x, y = 400, 300
    circle = CreateLight()
    night = CreateNight()
    alpha = CreateAlpha()
    
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
                    #print(1000 / time_taken, "fps. Fullscreen:", full, "Night:", night)
                    print(time_taken_ms, "ms. Fullscreen:", full, "Night:", night)
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

        #time_start2 = time.perf_counter_ns()
        # Wipe the screen if the player changed zone.
        if Sprite.behavour_args['screen_wipe']:
            wipe_screen(wipe_up, win2)
            Sprite.reload_loaded_locals()
            #shade = construct_lightmap(Sprite.focus.level.decomap, light)
            #world_image = stitch_tilemap(Sprite.focus.level, displacement)
            #world_image.convert()

        displacement = center_at((Sprite.focus.x, Sprite.focus.y), Sprite.focus.level.width, Sprite.focus.level.height)
        win2 = draw_tilemap(Sprite.focus.level.tilemap, win2, displacement) # 6-7 ms
        #win2.blit(world_image, displacement, area=pygame.Rect(0, 0, win_width, win_height).move_ip(displacement[0], displacement[1]))
        Sprite.blit_all(displacement, win2)
        win2 = draw_tilemap(Sprite.focus.level.decomap, win2, displacement, deco=True) # 0-1 ms

        if night:
            RefreshNight(night, alpha, circle, x, y)
            win2.blit(night, (0, 0))
##        if night: draw_lightmap(win2, displacement, Sprite.focus.level.decomap, Sprite.focus.level.tilemap, light)
        
        # Transfer internal window to displayed window and update screen.
        pygame.transform.scale(win2, (win.get_width(), win.get_height()), win) # 2-3 ms

        if Sprite.behavour_args['screen_wipe']:
            unwipe_screen(wipe_down, win2)
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
