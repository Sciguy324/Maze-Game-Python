from graphics import *
from math import ceil
from levels import *
import datetime

# Window settup
win_height = 64 * 9     # 576
win_width = 64 * 16     # 1024
#light_gray = color_rgb(127, 127, 127)
win = GraphWin("Mazes", win_width, win_height, autoflush=False)
win.setBackground("black")
win.set_icon("assets/rectangle.ico")
large_size = ceil(64 * win.get_screen()[0] / 1024)
#print(large_size)

# Image settup
missing = Image(Point(0, 0), "tiles/missing.png")
missing.img = missing.rescale(64)
large_missing = Image(Point(0, 0), "tiles/missing.png")
large_missing.img = large_missing.rescale(large_size)


def draw_tilemap(map_of_tiles, normal_ids, large_ids, large=False):
    '''Function to draw tilemap'''
    if large:
        tile_dict = large_ids
    else:
        tile_dict = normal_ids
    images = []
    y = -1
    for i in map_of_tiles:
        y += 1
        x = -1
        for j in i:
            x += 1
            if map_of_tiles[y][x] in tile_dict:
                temp_image = tile_dict[map_of_tiles[y][x]].clone()
                temp_image.move(64 * x + 32, 64 * y + 32)
                images.append(temp_image)
    for i in images:
        i.draw(win)
    return images


def check_collision(player, dxdy, map_of_tiles, collision_ids):
    '''Function to check collision'''
    next_player = player.clone()
    next_player.move(dxdy[0], dxdy[1])
    p1 = next_player.p1
    p2 = next_player.p2
    x1, y1, x2, y2 = int(p1.x / 64), int(p1.y / 64), int(p2.x / 64), int(p2.y / 64)
    if (p1.x < 0) or (p1.y < 0) or (p2.x < 0) or (p2.y < 0):
        return False
    try:
        if map_of_tiles[y1][x1] in collision_ids:
            return False
        if map_of_tiles[y2][x1] in collision_ids:
            return False
        if map_of_tiles[y1][x2] in collision_ids:
            return False
        if map_of_tiles[y2][x2] in collision_ids:
            return False
    except IndexError:
        return False
    return True


def center_at_player(player, playerx, playery, images, size, large=False):
    '''Function to shift the screen so the player is in the center'''
    try:
        cx = min(max(playerx - 64 * size[0], 0), size[2] * 64)
        cy = min(max(playery - 64 * size[1], 0), size[3] * 64)
        win.xview_moveto(cx / (64 * len(tilemap[0])))
        win.yview_moveto(cy / (64 * len(tilemap)))
    except:
        pass


def load_level(lvl, lrg):
    '''Function to load a level.
    return tilemap, colliders, normal_tile_ids, large_tile_ids, start, movement_speed'''
    return lvl(lrg)


def main(win, spawn, speed):
    '''Main program'''
    image_map = draw_tilemap(tilemap, normal_tile_ids, large_tile_ids)
    bounds = (16 / 2, 9 / 2, (len(tilemap[0]) - 16 / 2), (len(tilemap) - 9 / 2))
    player = Rectangle(Point(spawn[0], spawn[1]), Point(spawn[0] + 40, spawn[1] + 40))
    player.setFill("red")
    player.setWidth(0)
    player.draw(win)
    image_map += draw_tilemap(decomap, normal_deco_ids, large_deco_ids)
    current_speed = speed
    player_x = player.getCenter().x
    player_y = player.getCenter().y
    win.config(scrollregion=(0, 0, 64 * len(tilemap[0]), 64 * len(tilemap)))
    multiplier = 1

    key_lock = False
    done = False
    while not done:
        try:
            clock = datetime.datetime.now()
            if win.checkKey() == 'Escape':
                win.toggle_fullscreen()
                if win.fullscreen:
                    player.undraw()
                    for i in image_map:
                        i.undraw()
                    image_map = draw_tilemap(tilemap, normal_tile_ids, large_tile_ids, large=True)
                    win.config(scrollregion=(0, 0, 64 * len(tilemap[0]) + large_size  * len(tilemap[0]) / 4, 64 * len(tilemap) + large_size * len(tilemap) / 4))
                    player.draw(win)
                    image_map += draw_tilemap(decomap, normal_deco_ids, large_deco_ids, large=True)
                else:
                    player.undraw()
                    for i in image_map:
                        i.undraw()
                    image_map = draw_tilemap(tilemap, normal_tile_ids, large_tile_ids, large=False)
                    win.config(scrollregion=(0, 0, 64 * len(tilemap[0]), 64 * len(tilemap)))
                    player.draw(win)
                    image_map += draw_tilemap(decomap, normal_deco_ids, large_deco_ids, large=False)
            dx = 0
            dy = 0
            if win.keys['shift_l']:
                move_speed = 0.5 * speed * multiplier
            else:
                move_speed = speed * multiplier
            if win.keys['w']:
                dy -= move_speed
            if win.keys['s']:
                dy += move_speed
            if check_collision(player, (0, dy), tilemap, colliders):
                player_y += dy
                player.move(0, dy)
            if win.keys['a']:
                dx -= move_speed
            if win.keys['d']:
                dx += move_speed
            if check_collision(player, (dx, 0), tilemap, colliders):
                player_x += dx
                player.move(dx, 0)
            center_at_player(player, player_x, player_y, image_map, bounds)
            update(120)
            multiplier = min(20, (datetime.datetime.now() - clock).microseconds / 9000)
        except GraphicsError:
            done = True
    print("Game Closed")

if __name__ == "__main__":
    level = riverside
    start, movement_speed, colliders, tilemap, decomap, normal_tile_ids, large_tile_ids, normal_deco_ids, large_deco_ids = load_level(level, large_size)
    main(win, start, movement_speed)
