import pygame
import os
from sys import platform
import matplotlib.pyplot as plt
import time
from networks import *
import threading

# # PRE-INITIALIZATION:

# Pygame initialization
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

# If the platform is windows, ensure that the system is not stretching the game window to the display.
if platform == "win32":
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    os.environ['SDL_VIDEODRIVER'] = 'directx'

# missing = pygame.image.load(os.path.join('tiles/missing.png'))
# missing = pygame.transform.scale(missing, (64, 64)).convert()


def setup_light():
    light_area = pygame.image.load(os.path.join('assets/light.png')).convert_alpha()
    light = pygame.Surface((192, 192))
    light.fill((100, 100, 100))
    light.blit(light_area, (0, 0))
    light.convert()
    return light


def center_at(userx, usery, world_width, world_height):
    """Function to center the screen on a sprite"""
    dispx = max(min(1024 / 2 - userx, 0), 1024 - world_width)
    dispy = max(min(576 / 2 - usery, 0), 576 - world_height)
    return dispx, dispy


class Game:
    """Overarching class for Maze"""

    # General class variable setup
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h
    win_width = 64 * 16
    win_height = 64 * 9
    win = pygame.display.set_mode((win_width, win_height))
    ext_width = win.get_width()
    ext_height = win.get_height()
    focus = None
    light = None
    player = None

    def __init__(self, start_level):
        # Display window setup
        pygame.display.set_caption("Maze (Client)")
        icon = pygame.image.load(os.path.join('assets', 'icon.bmp'))
        pygame.display.set_icon(icon)

        # Dialog system initialization
        Dialog.dialog_init((Game.win_width, Game.win_height), Game.win)

        # Internal window and module setup
        self.win2 = pygame.Surface((Game.win_width, Game.win_height))
        Dialog.internal_window = self.win2
        self.full = False
        self.night = False

        # Client connection initialization
        self.net = Network()
        time.sleep(0.1)

        # Download maps
        self.download_basic_levels()
        time.sleep(0.1)
        self.inquire_level(start_level)

        # Setup all sprites
        player_sprite = minor_sprite_setup(start_level)
        player_sprite.entity_id = self.net.id
        Game.player = player_sprite
        Sprite.focus = player_sprite
        Game.focus = player_sprite

        # Early rendering
        Game.light = setup_light()
        self.generate_litmap(player_sprite)

        # Finish client connection setup
        time.sleep(0.1)
        self.download_sprites()
        time.sleep(0.1)
        self.net.send("pst" + self.player.jsonify2())
        send_thread = threading.Thread(target=Game.send_thread, args=(self,))
        send_thread.daemon = True
        send_thread.start()

    def draw_tilemap(self, dispx, dispy, deco=False):
        """Function to draw tilemap.  Only draws visible area."""
        if deco:
            draw_map = self.focus.level.decomap
            id_list = Level.deco_ids
        else:
            draw_map = self.focus.level.tilemap
            id_list = Level.tile_ids
        window = self.win2
        litmap = self.litmap
        x_tile = int(abs(dispx / 64))
        y_tile = int(abs(dispy / 64))
        y = y_tile - 1
        for i in draw_map[y_tile:y_tile + 10]:
            y += 1
            x = x_tile - 1
            for j in i[x_tile:x_tile + 17]:
                x += 1
                if j in id_list:
                    if litmap[y][x]:
                        id_list[j].draw_norm(window, (dispx + x * 64, dispy + y * 64))
                    else:
                        id_list[j].draw(window, (dispx + x * 64, dispy + y * 64))

    def stitch_tilemap(self, deco=False):
        """Function to stitch tiles together into a single image, as defined by a tilemap matrix."""
        if deco:
            id_list = Level.deco_ids
            lvl_map = self.focus.level.decomap
        else:
            id_list = Level.tile_ids
            lvl_map = self.focus.level.tilemap
        result = pygame.Surface((self.focus.level.width, self.focus.level.height))
        y = -64
        for i in lvl_map:
            y += 64
            x = -64
            for j in i:
                x += 64
                if j in id_list:
                    id_list.draw(result, (x, y))
        return result

    def generate_litmap(self, focus):
        """Generate a reference map for illuminated tiles"""
        focus_level = focus.level
        row = [0] * (focus_level.width // 64)
        matrix = [list(row) for i in range(focus_level.height // 64)]
        rects = []
        for x, y in focus_level.lightmap:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    matrix[max(y + j, 0)][max(x + i, 0)] = 1
            rects.append(pygame.Rect((x - 1) * 64, (y - 1) * 64, 192, 192))
        self.litmap, self.lit_rects = list(matrix), list(rects)

    def illuminate(self, dispx, dispy):
        """Draw light sources using the lightmap"""
        window = self.win2
        light = Game.light
        x_tile = int(abs(dispx / 64))
        y_tile = int(abs(dispy / 64))
        for x, y in self.focus.level.lightmap:
            if x in range(x_tile, x_tile + 17) and y in range(y_tile, y_tile + 10):
                window.blit(light, (dispx + (x - 1) * 64, dispy + (y - 1) * 64), special_flags=pygame.BLEND_SUB)

    def wipe_effect(self):
        """Function that wipes the screen black, and then unwipes it again"""
        wipe_up = pygame.image.load(os.path.join('assets/wipe_up.png')).convert_alpha()
        self.wipe_basic(wipe_up, self.win2.copy(), Game.ext_height)
        self.generate_litmap(self.focus)
        while self.focus.inquiring:
            pass
        self.render()
        wipe_down = pygame.image.load(os.path.join('assets/wipe_down.png')).convert_alpha()
        self.wipe_basic(wipe_down, self.win2.copy(), 0)

    def wipe_basic(self, wipe, screenshot, start):
        """Generic function to wipe/unwipe the screen black."""
        scaled_wipe = pygame.transform.scale(wipe, (Game.ext_width, Game.ext_height * 2))
        scaled_screenshot = pygame.transform.scale(screenshot, (Game.ext_width, Game.ext_height))
        i = 0
        while i < Game.ext_height * 2:
            t1 = time.perf_counter_ns()
            Game.win.blit(scaled_screenshot, (0, 0))
            Game.win.blit(scaled_wipe, (0, start - i))
            pygame.display.flip()
            time_step = (time.perf_counter_ns() - t1) / 600000
            i += time_step * Game.ext_height / Game.win_height

    def render(self):
        """Standard rendering function"""
        win2 = self.win2
        focus = self.focus
        # Wipe the screen if the player changed zone.
        
        if Sprite.behavior_args['screen_wipe']:
            Sprite.behavior_args['screen_wipe'] = False
            self.wipe_effect()
            Sprite.reload_loaded_locals()
            self.generate_litmap(focus)
            # world_image = stitch_tilemap(Sprite.focus.level, dispx, dispy)
            # world_image.convert()

        dispx, dispy = center_at(focus.x, focus.y, focus.level.width, focus.level.height)
        self.draw_tilemap(dispx, dispy)  # 6-7 ms
        # win2.blit(world_image, dispx, dispy, area=pygame.Rect(0, 0, win_width, win_height).move_ip(dispx, dispy))
        if self.night:
            Sprite.blit_all_night(dispx, dispy, win2, self.litmap, self.lit_rects)
            self.draw_tilemap(dispx, dispy, deco=True)
            self.illuminate(dispx, dispy)
        else:
            Sprite.blit_all(dispx, dispy, win2)
            self.draw_tilemap(dispx, dispy, deco=True)
        
        # Transfer internal window to displayed window and update screen.
        pygame.transform.scale(win2, (Game.ext_width, Game.ext_height), Game.win)  # 2-3 ms

    def send_thread(self):
        """Thread that handles sending player sprite information"""
        formatted_response = ""
        while True:
            focus = self.focus
            # If the focus sprite is attempting to join another map, first run that request
            if focus.inquiring:
                focus.level = self.inquire_level(focus.inquire_of)
                focus.inquiring = False
                time.sleep(0.1)

            # Standard sprite data updating
            response = self.net.send("set" + self.player.jsonify2())
            if response:
                # Check for override
                # Server has ordered refresh of client's guest dictionaries.
                if response[:3] == "rel":
                    self.download_sprites()
                # Server reports the addition of a new sprite
                elif response[:3] == "add":
                    print(response[3:], "joined the server!")
                    GuestSprite.add_sprite(int(response[3:]))
                # Server reports the removal of an existing sprite
                elif response[:3] == "del":
                    print(response[-1], "left the server!")
                    Sprite.delete_sprite(int(response[-1]))
                # Server has sprite data to inform the client about
                elif response[:3] == "upd":
                    try:
                        entity_count = int(response[3:])
                        for i in range(entity_count):
                            response = self.net.send("next")
                            formatted_response = json.loads(response)
                            s = Sprite.sprite_dict[formatted_response["id"]]
                            s.x = formatted_response["x"]
                            s.y = formatted_response["y"]
                            s.facing.set(formatted_response["facing"])
                            s.direction.set(formatted_response["direction"])
                            s.animation.running = formatted_response["animated"]
                            s.speed_mult = formatted_response["speed"]
                            s.level = Level.reference_dict[formatted_response["level"]]
                    except Exception as e:
                        print("Failed to parse sprite data, was:\n", formatted_response)
                        print("Registered sprites was:\n", Sprite.sprite_dict)
                        raise e
            else:
                print("Read Error")
            # time.sleep(0.01)

    def inquire_level(self, level):
        """Ask server for JSON level data"""
        print("Downloading level:", level)
        package_count = int(self.net.send("lvl" + level))
        time.sleep(0.1)
        data = ""
        for i in range(package_count):
            data += self.net.send("next")
        print(data)
        return load_from_string(data)

    def download_basic_levels(self):
        """Ask server about what levels currently exist, and set up the bare minimum"""
        print("Downloading basic level instances")
        level_count = int(self.net.send("blv"))
        time.sleep(0.1)
        data = []
        for i in range(level_count):
            data.append(self.net.send("next"))
        for i in data:
            Level([], build_matrix(16, 9), build_matrix(16, 9), [], [], (0, 0), i)

    def download_sprites(self):
        print("Downloading sprites")
        for i, j in list(Sprite.sprite_dict.items()):
            if i != self.player.entity_id:
                Sprite.delete_sprite(i)
        entity_count = int(self.net.send("spr"))
        for i in range(entity_count):
            package_count = int(self.net.send("next"))
            if package_count == 1:
                data = self.net.send("next")
            else:
                data = ""
                for j in range(package_count):
                    data += self.net.send("next")
            Sprite.add_sprite(json.loads(data))
        time.sleep(0.1)
        print("Finished downloading sprites")

    def play(self):
        """Play a level, requires starting position of player and map of level"""
        # Misc.
        time_step = 1
        time_taken = 0
        Sprite.behavior_args["screen_wipe"] = True        
        
        # Main loop
        done = False
        while not done:
            time_start = time.perf_counter_ns()

            # # CLIENT INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        return
                    elif event.key == pygame.K_F11:
                        self.full = not self.full
                        if self.full:
                            Game.win = pygame.display.set_mode((Game.screen_width, Game.screen_height),
                                                               pygame.FULLSCREEN | pygame.DOUBLEBUF)
                            Game.ext_width = int(Game.screen_width)
                            Game.ext_height = int(Game.screen_height)
                        else:
                            Game.win = pygame.display.set_mode((Game.win_width, Game.win_height))
                            Game.ext_width = int(Game.win_width)
                            Game.ext_height = int(Game.win_height)
                    elif event.key == pygame.K_f:
                        print(1000 / time_taken, "fps. Fullscreen:", self.full, "Night:", self.night)
                    elif event.key == pygame.K_z:
                        self.night = True
                        Level.darken_imgs(100)
                        Sprite.darken_all(100)
                    elif event.key == pygame.K_x:
                        self.night = False
                        Level.reset_imgs()
                        Sprite.reset_imgs()
                    elif event.key == pygame.K_c:
                        for i, j in Sprite.sprite_dict.items():
                            print(i, ">", j)
    
            # # SERVER FUNCTIONS (BUT NOT QUITE, CURRENTLY)
            # Update entities
            Sprite.behavior_args['keys'] = pygame.key.get_pressed()
            Sprite.behavior_args['time_step'] = time_step
            Sprite.behave_all()

            # # CLIENT FUNCTIONS
            self.render()
            pygame.display.flip()

            # # UNIVERSAL (SERVER + CLIENT) FUNCTIONS
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
    print("\t-Backspace: Stop game")
    print("\nTodo:")
    print("\t-Add more to sprite system")
    print("\t\t-Add more behaviours")
    print("\t-Debug lighting engine")
    print("\t-Complete major overhaul No. 3 billion")
    print("\t-Make Static class more consistent")
    # Worlds module must be called after the window mode is set, and sprite module depends on worlds module.
    from sprite import *

    # Run game
    maze = Game("demo")
    maze.play()

pygame.quit()

if len(step_list) > 0:
    step_list.pop(0)
    print("Average Value:", sum(step_list) / len(step_list))
    graph = plt.figure()
    graph.suptitle('Timestep Each Tick')
    plt.plot(step_list, label="Timestep")
    plt.legend()
    plt.show()
