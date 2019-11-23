from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from ast import *
from shutil import copy2
from os import path
import json

def build_matrix(width, height):
    row = []
    matrix = []
    for i in range(0, width):
        row.append(0)
    for i in range(0, height):
        matrix.append(row)
    return matrix


def add_row(matrix):
    new_row = []
    for i in range(0, len(matrix[0])):
        new_row.append(0)
    return matrix + [new_row]


def add_column(matrix):
    clone = list(matrix)
    build = []
    for i in clone:
        row = list(i)
        row += [0]
        build += [row]
    return build


def delete_row(matrix):
    del matrix[len(matrix) - 1]
    return matrix


def delete_column(matrix):
    del matrix[0][0]
    return matrix


class Dialog(Toplevel):

    def __init__(self, parent, title=None, text="", args=None):

        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.iconbitmap('assets/hammer.ico')
        self.parent = parent
        self.result = None
        body = Frame(self)
        self.initial_focus = self.body(body, text, args)
        body.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)


    def body(self, master, txt, args=None):
        '''Override this function'''
        pass


    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()


    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()


    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()


    def validate(self):
        '''Override this function'''
        pass

    def apply(self):
        '''Override this function'''
        pass


class EnterNumber(Dialog):

    def body(self, master, txt, args=None):
        Label(master, text=txt).grid(row=0)
        self.entry = Entry(master)
        self.entry.grid(row=0, column=1)
        return self.entry

    def validate(self):
        try:
            self.result = int(self.entry.get())
            return 1
        except ValueError:
            showwarning(
                "Invalid Input",
                "Please enter a number."
                )
            return 0

    def apply(self):
        self.result = int(self.entry.get())

class Enter2Numbers(Dialog):

    def body(self, master, txt, args=None):
        Label(master, text=txt).grid(row=0)
        self.entry_x = Entry(master)
        self.entry_y = Entry(master)
        self.entry_x.grid(row=0, column=1)
        self.entry_y.grid(row=0, column=2)
        return self.entry_x

    def validate(self):
        try:
            self.result = (int(self.entry_x.get()), int(self.entry_y.get()))
            return 1
        except ValueError:
            showwarning(
                "Invalid Input",
                "Please enter a number."
                )
            return 0

    def apply(self):
        self.result = (int(self.entry_x.get()), int(self.entry_y.get()))

class EnterText(Dialog):

    def body(self, master, txt, args=None):
        Label(master, text=txt).grid(row=0)
        self.entry = Entry(master)
        self.entry.grid(row=0, column=1)
        return self.entry

    def validate(self):
        try:
            self.result = str(self.entry.get())
            return 1
        except ValueError:
            showwarning(
                "Invalid Input",
                "Please enter a number."
                )
            return 0

    def apply(self):
        self.result = str(self.entry.get())


class EditLoadDestination(Dialog):

    def body(self, master, txt=None, args=None):
        Label(master, text="Tile X: ").grid(row=0, column=0)
        Label(master, text="Tile Y: ").grid(row=0, column=2)
        Label(master, text="Level : ").grid(row=1, column=0)
        self.entry_x = Entry(master)
        self.entry_y = Entry(master)
        self.entry_level = Entry(master)
        self.entry_x.grid(row=0, column=1)
        self.entry_y.grid(row=0, column=3)
        self.entry_level.grid(row=1, column=1)
        if args:
            self.entry_x.insert(0, args[1][0])
            self.entry_y.insert(0, args[1][1])
            self.entry_level.insert(0, args[0])

    def validate(self):
        try:
            self.result = [str(self.entry_level.get()), (int(self.entry_x.get()), int(self.entry_y.get()))]
            return 1
        except ValueError:
            showwarning(
                "Invalid Input",
                "Please enter coordinates and a level to load."
                )
            return 0

    def apply(self):
        self.result = [str(self.entry_level.get()), (int(self.entry_x.get()), int(self.entry_y.get()))]


class EditTileIds(Dialog):

    def body(self, master, txt, args=None):

        self.vbar = Scrollbar(master)
        self.vbar.grid(row = 0, column=1, sticky=N+S)
        self.canvas = Canvas(master, height=256)
        self.canvas.grid(row=0, column=0)
        self.canvas.grid_propagate(False)
        self.vbar.config(command=self.canvas.yview)
        self.vbar.activate("slider")
        
        y = 0
        self.entry_list = []
        for i in list(App.tile_ids.items()):
            y += 1
            label = Label(self.canvas, text=i[0])
            self.entry_list.append(Entry(self.canvas))
            self.entry_list[len(self.entry_list) - 1].insert(0, str(i[1]))
            self.canvas.create_window(80, 20 * y + 20, window=label)
            self.canvas.create_window(256, 20 * y + 20, window=self.entry_list[len(self.entry_list) - 1])

        self.canvas.config(scrollregion=self.canvas.bbox("all"), yscrollcommand=self.vbar.set)            

    def validate(self):
        try:
            out = {}
            index = -1
            for i in self.entry_list:
                index += 1
                image = list(App.tile_ids.items())[index][0]
                out[image] = int(i.get())
            self.result = out
            return 1
        except ValueError:
            showwarning("Invalid Input", "Image IDs must be an integer.")
            return 0        

    def apply(self):
        out = {}
        index = -1
        for i in self.entry_list:
            index += 1
            image = list(App.tile_ids.items())[index][0]
            out[image] = int(i.get())
        self.result = out


class EditDecoIds(Dialog):

    def body(self, master, txt, args=None):

        self.vbar = Scrollbar(master)
        self.vbar.grid(row = 0, column=1, sticky=N+S)
        self.canvas = Canvas(master, height=256)
        self.canvas.grid(row=0, column=0)
        self.canvas.grid_propagate(False)
        self.vbar.config(command=self.canvas.yview)
        self.vbar.activate("slider")
        
        y = 0
        self.entry_list = []
        for i in list(App.deco_ids.items()):
            y += 1
            label = Label(self.canvas, text=i[0])
            self.entry_list.append(Entry(self.canvas))
            self.entry_list[len(self.entry_list) - 1].insert(0, str(i[1]))
            self.canvas.create_window(80, 20 * y + 20, window=label)
            self.canvas.create_window(256, 20 * y + 20, window=self.entry_list[len(self.entry_list) - 1])

        self.canvas.config(scrollregion=self.canvas.bbox("all"), yscrollcommand=self.vbar.set)
            

    def validate(self):
        try:
            out = {}
            index = -1
            for i in self.entry_list:
                index += 1
                image = list(App.deco_ids.items())[index][0]
                out[image] = int(i.get())
            self.result = out
            return 1
        except ValueError:
            showwarning("Invalid Input", "Decoration IDs must be an integer.")
            return 0
        

    def apply(self):
        out = {}
        index = -1
        for i in self.entry_list:
            index += 1
            image = list(App.deco_ids.items())[index][0]
            out[image] = int(i.get())
        self.result = out


class EditColliderList(Dialog):

    def body(self, master, txt, args=None):

        #print("In:", args)
        self.vbar = Scrollbar(master)
        self.vbar.grid(row = 0, column=1, sticky=N+S)
        self.canvas = Canvas(master, height=256, width=72)
        self.canvas.grid(row=0, column=0)
        self.canvas.grid_propagate(False)
        self.vbar.config(command=self.canvas.yview)
        self.vbar.activate("slider")
        
        y = 0
        self.button_list = []
        self.value_list = []
        tile_list = list(App.tile_ids.items())
        del tile_list[0]
        for i in tile_list:
            y += 1
            #label = Label(self.canvas, text=i[0])
            self.value_list.append(IntVar(master))
            self.button_list.append(Checkbutton(self.canvas, variable=self.value_list[y-1], onvalue=i[1], offvalue=0, image=App.translate_f2tk[i[0]], indicatoron=False, highlightthickness=3, bg='gray'))
            #print("Checking index", y-1)
            if y-1 in args:
                self.value_list[y-1].set(i[1])
                #print("Found {} with ID {}, given value {}".format(i[0], y-1, i[1]))
            self.canvas.create_window(0, 80 * y + 20, window=self.button_list[len(self.button_list) - 1])

        self.canvas.config(scrollregion=self.canvas.bbox("all"), yscrollcommand=self.vbar.set)
            

    def validate(self):
        try:
            out = []
            tile_list = list(App.tile_ids.items())
            del tile_list[0]
            for i in self.value_list:
                #print("The image {} with ID {} was found in the list".format(tile_list[i.get()][0], i.get()))
                t_id = tile_list[i.get()][1]
                if t_id != 0:
                    out.append(t_id)
            self.result = list(out)
            return 1
        except ValueError:
            showwarning("Invalid Input", "Decoration IDs must be an integer.")
            return 0
        

    def apply(self):
        out = []
        tile_list = list(App.tile_ids.items())
        del tile_list[0]
        for i in self.value_list:
            t_id = tile_list[i.get()][1]
            if t_id != 0:
                out.append(t_id)
        self.result = list(out)


class EditCatagories(Dialog):

    def body(self, master, txt, args=None):

        self.selected_group = StringVar(master)
        self.selected_group.set("All")
        self.group_dict = args

        def new_group():
            new_name = EnterText(master, title="New Group", text="Enter New Group Name:").result
            if new_name == None:
                return
            self.group_dict[new_name] = []
            rebuild_selection()

        def switch_group(event, something, var_mode):
            # Build list of tiles in this group
            tile_out = []
            tile_list = list(App.tile_ids.items())
            del tile_list[0]
            for i in self.tile_value_list:
                t_id = tile_list[i.get()][0]
                # If the current value was not previously (here defaulting to missing.png), don't include that in the output
                if t_id != 'tiles/missing.png':
                    tile_out.append(t_id)

            # Build list of decos in this group
            deco_out = []
            deco_list = list(App.deco_ids.items())
            del deco_list[0]
            for i in self.deco_value_list:
                d_id = deco_list[i.get()][0]
                # If the current value was not previously (here defaulting to missing.png), don't include that in the output
                if d_id != 'tiles/box.png':
                    deco_out.append(d_id)
            
            self.group_dict[self.current_group] = tile_out + deco_out
            self.current_group = self.selected_group.get()
            rebuild_selection()
                
        self.selected_group.trace('w', switch_group)

        def build_selection():
            self.current_group = self.selected_group.get()
            options = list(i[0] for i in self.group_dict.items())
            self.groups_menu = OptionMenu(master, self.selected_group, *options).grid(row=0, column=0)
            self.new_group_button = Button(master, text="New Group", command=new_group)
            self.new_group_button.grid(row=0, column=1)
            
            self.tile_vbar = Scrollbar(master)
            self.tile_vbar.grid(row=1, column=2, sticky=N+S)
            self.tile_canvas = Canvas(master, height=256, width=72)
            self.tile_canvas.grid(row=1, column=0)
            self.tile_canvas.grid_propagate(False)
            self.tile_vbar.config(command=self.tile_canvas.yview)
            self.tile_vbar.activate("slider")

            self.deco_vbar = Scrollbar(master)
            self.deco_vbar.grid(row=1, column=3, sticky=N+S)
            self.deco_canvas = Canvas(master, height=256, width=72)
            self.deco_canvas.grid(row=1, column=1)
            self.deco_canvas.grid_propagate(False)
            self.deco_vbar.config(command=self.deco_canvas.yview)
            self.deco_vbar.activate("slider")
            
            # Tile selection panel
            y = 0
            self.tile_button_list = []
            self.tile_value_list = []
            tile_list = list(App.tile_ids.items())
            del tile_list[0]
            for i in tile_list:
                y += 1
                self.tile_value_list.append(IntVar(master))
                self.tile_button_list.append(Checkbutton(self.tile_canvas, variable=self.tile_value_list[y-1], onvalue=i[1], offvalue=0, image=App.translate_f2tk[i[0]], indicatoron=False, highlightthickness=3, bg='gray'))
                # This code determines if a button is already set, and configures it accordingly
                if i[0] in self.group_dict[self.selected_group.get()]:
                    self.tile_value_list[y-1].set(i[1])
                self.tile_canvas.create_window(0, 80 * y + 20, window=self.tile_button_list[len(self.tile_button_list) - 1])

            self.tile_canvas.config(scrollregion=self.tile_canvas.bbox("all"), yscrollcommand=self.tile_vbar.set)

            # Deco selection panel
            y = 0
            self.deco_button_list = []
            self.deco_value_list = []
            deco_list = list(App.deco_ids.items())
            del deco_list[0]
            for i in deco_list:
                y += 1
                self.deco_value_list.append(IntVar(master))
                self.deco_button_list.append(Checkbutton(self.deco_canvas, variable=self.deco_value_list[y-1], onvalue=i[1], offvalue=0, image=App.translate_f2tk[i[0]], indicatoron=False, highlightthickness=3, bg='gray'))
                # This code determines if a button is already set, and configures it accordingly
                if i[0] in self.group_dict[self.selected_group.get()]:
                    self.deco_value_list[y-1].set(i[1])
                self.deco_canvas.create_window(0, 80 * y + 20, window=self.deco_button_list[len(self.deco_button_list) - 1])

            self.deco_canvas.config(scrollregion=self.deco_canvas.bbox("all"), yscrollcommand=self.deco_vbar.set)

        def rebuild_selection():
            self.tile_canvas.destroy()
            self.deco_canvas.destroy()
            self.tile_vbar.destroy()
            self.deco_vbar.destroy()
            build_selection()

        build_selection()

    def validate(self):
        try:
            # Build list of tiles in this group
            tile_out = []
            tile_list = list(App.tile_ids.items())
            del tile_list[0]
            for i in self.tile_value_list:
                t_id = tile_list[i.get()][0]
                # If the current value was not previously (here defaulting to missing.png), don't include that in the output
                if t_id != 'tiles/missing.png':
                    tile_out.append(t_id)

            # Build list of decos in this group
            deco_out = []
            deco_list = list(App.deco_ids.items())
            del deco_list[0]
            for i in self.deco_value_list:
                d_id = deco_list[i.get()][0]
                # If the current value was not previously (here defaulting to missing.png), don't include that in the output
                if d_id != 'tiles/box.png':
                    deco_out.append(d_id)
            
            self.group_dict[self.current_group] = tile_out + deco_out
            self.result = self.group_dict
            return 1
        except ValueError:
            showwarning("An unknown error occured")
            return 0
        

    def apply(self):
        # Build list of tiles in this group
        tile_out = []
        tile_list = list(App.tile_ids.items())
        del tile_list[0]
        for i in self.tile_value_list:
            t_id = tile_list[i.get()][0]
            # If the current value was not previously (here defaulting to missing.png), don't include that in the output
            if t_id != 'tiles/missing.png':
                tile_out.append(t_id)

        # Build list of decos in this group
        deco_out = []
        deco_list = list(App.deco_ids.items())
        del deco_list[0]
        for i in self.deco_value_list:
            d_id = deco_list[i.get()][0]
            # If the current value was not previously (here defaulting to missing.png), don't include that in the output
            if d_id != 'tiles/box.png':
                deco_out.append(d_id)
        
        self.group_dict[self.current_group] = tile_out + deco_out
        self.result = self.group_dict


class App:

    tiles = []
    decos = []
    translate_tk2f = {0: 0}
    translate_f2tk = {0: 0}
    load_tiles = {}
    try:
        with open('assets/image_config.config', 'r') as rf:
            tile_ids = literal_eval(rf.readline())
            deco_ids = literal_eval(rf.readline())
            groups = literal_eval(rf.readline())
    except FileNotFoundError:
        with open('assets/image_config.config', 'w') as wf:
            wf.write('{0: 0, "tiles/missing.png": 0, "tiles/block.png": 1}')
            wf.write('{0: 0, "tiles/box.png": 0}')
            wf.write('{"All": ["tiles/missing.png", "tiles/block.png"]}')
            tile_ids = {0: 0, "tiles/missing.png": 0, "tiles/block.png": 1}
            deco_ids = {0: 0, "tiles/box.png": 0}
            groups = {"All": ["tiles/missing.png", "tiles/block.png"]}

    def __init__(self, master):

        master.title("Worldbuilder")
        master.iconbitmap('assets/hammer.ico')
        master.state('zoomed')
        frame = Frame(master)
        frame.pack(fill=NONE, expand=0)
        saved = IntVar(master)          # 0: Not saved, 1: Saved
        saved.set(1)
        selected_image = IntVar(master) # Currently selected base-layer tile
        selected_deco = IntVar(master)  # Currently selected decoration tile
        selected_load = IntVar(master)  # Currently selected loading zone tile
        selected_light = IntVar(master) # Currently selected lightmap tile
        cursor_mode = IntVar(master)    # 0: Regular mode, 1: Pan mode, 2: Busy mode
        cursor_mode.set(0)
        view_mode = IntVar(master)      # 0: View ground layer, 1: View decoration layer, 2: View loading zones
        force_grid = IntVar(master)     # 0: Do not force grid, 1: Force grid
        catagories = StringVar(master)
        self.tilemap = build_matrix(16, 9)
        self.decomap = build_matrix(16, 9)
        self.directory = "no_file"
        self.colliders = []
        self.loading_zones = {}
        self.light_sources = []
        self.default_start = (0, 0)
        self.copied_load_settings = None

        # Frame setup + coordinate indicator setup
        self.menu_frame = Frame(frame)
        self.menu_frame.pack(side=TOP, anchor=N+W)
        self.coords_label = Label(frame, text="¯\_(ツ)_/¯")
        self.coords_label.pack(side=BOTTOM, anchor=W)
        self.map_frame = Frame(frame, bd=2, relief=SUNKEN, bg="WHITE", width=64*16, height=64*9)
        self.map_frame.pack(padx=10, pady=10, side=LEFT, anchor=CENTER, expand=0)
        self.tile_frame = Frame(frame, bd=2, relief=SUNKEN)
        self.tile_frame.pack(padx=5, pady=5, side=RIGHT, anchor=E, expand=0)

        # Additional Options Panel
        self.pointer = PhotoImage(file="assets/pointer_cursor.png")
        self.mover = PhotoImage(file="assets/movement_cursor.png")
        self.forcegrid = PhotoImage(file="assets/grid.png")
        self.menu_selection = Radiobutton(self.menu_frame, image=self.pointer, variable=cursor_mode, value=0, indicatoron=0)
        self.menu_selection.grid(row=0, column=0)
        self.menu_selection = Radiobutton(self.menu_frame, image=self.mover, variable=cursor_mode, value=1, indicatoron=0)
        self.menu_selection.grid(row=0, column=1)
        self.menu_selection = Checkbutton(self.menu_frame, image=self.forcegrid, variable=force_grid, indicatoron=0, offvalue=0, onvalue=1)
        self.menu_selection.grid(row=0, column=2)
    
        self.menu_spacing = Frame(self.menu_frame, width=80, height=40, bd=2)
        self.menu_spacing.grid(row=0, column=3)

        # Layer control panel initialization
        self.ground = PhotoImage(file="assets/ground.png")
        self.decoration = PhotoImage(file="assets/decoration.png")
        self.loadzone = PhotoImage(file="assets/loading_zone.png")
        self.lightmap = PhotoImage(file="assets/lightbulb.png")
        self.view_selection = Radiobutton(self.menu_frame, image=self.ground, variable=view_mode, value=0, indicatoron=0)
        self.view_selection.grid(row=0, column=4)
        self.view_selection = Radiobutton(self.menu_frame, image=self.decoration, variable=view_mode, value=1, indicatoron=0)
        self.view_selection.grid(row=0, column=5)
        self.view_selection = Radiobutton(self.menu_frame, image=self.loadzone, variable=view_mode, value=2, indicatoron=0)
        self.view_selection.grid(row=0, column=6)
        self.view_selection = Radiobutton(self.menu_frame, image=self.lightmap, variable=view_mode, value=3, indicatoron=0)
        self.view_selection.grid(row=0, column=7)

        self.menu_spacing2 = Frame(self.menu_frame, width=80, height=40, bd=2)
        self.menu_spacing2.grid(row=0, column=8)

        # Category panel initialization
        options = list(i[0] for i in App.groups.items())
        catagories.set(options[0])
        self.groups_menu = OptionMenu(self.menu_frame, catagories, *options)
        self.groups_menu.grid(row=0, column=9)

        # Changed palette group action
        def set_group(event, something, var_mode):
            redraw_panels()

        catagories.trace('w', set_group)

        # Selected image action
        def set_cursor_icon(event, something, var_mode):
            if cursor_mode.get() == 0:
                self.map_canvas.config(cursor="")
            elif cursor_mode.get() == 1:
                self.map_canvas.config(cursor="fleur")
            elif cursor_mode.get() == 2:
                self.map_canvas.config(cursor="wait")
            else:
                pass

        cursor_mode.trace('w', set_cursor_icon)

        # Selected mode action
        def set_view_mode(event, something, var_mode):
            if view_mode.get() == 0:
                
                self.deco_canvas.grid_remove()
                self.deco_vbar.grid_remove()
                self.load_canvas.grid_remove()
                self.load_vbar.grid_remove()
                self.light_canvas.grid_remove()
                self.light_vbar.grid_remove()
                self.tile_canvas.grid(row=0, column=0, sticky=N+S+E+W)
                self.img_vbar.grid(row=0, column=1, sticky=N+S)
            elif view_mode.get() == 1:
                self.tile_canvas.grid_remove()
                self.img_vbar.grid_remove()
                self.load_canvas.grid_remove()
                self.load_vbar.grid_remove()
                self.light_canvas.grid_remove()
                self.light_vbar.grid_remove()
                self.deco_canvas.grid(row=0, column=0, sticky=N+S+E+W)
                self.deco_vbar.grid(row=0, column=1, sticky=N+S)
            elif view_mode.get() == 2:
                self.deco_canvas.grid_remove()
                self.deco_vbar.grid_remove()
                self.tile_canvas.grid_remove()
                self.img_vbar.grid_remove()
                self.light_canvas.grid_remove()
                self.light_vbar.grid_remove()
                self.load_canvas.grid(row=0, column=0, sticky=N+S+E+W)
                self.load_vbar.grid(row=0, column=1, sticky=N+S)
            else:
                self.deco_canvas.grid_remove()
                self.deco_vbar.grid_remove()
                self.tile_canvas.grid_remove()
                self.img_vbar.grid_remove()
                self.load_canvas.grid_remove()
                self.load_vbar.grid_remove()
                self.light_canvas.grid(row=0, column=0, sticky=N+S+E+W)
                self.light_vbar.grid(row=0, column=1, sticky=N+S)
            redraw_map_canvas()

        view_mode.trace('w', set_view_mode)

        # Toggled force grid action
        def toggle_grid(event, something, var_mode):
            redraw_map_canvas()

        force_grid.trace('w', toggle_grid)


        # Change heading in accordance to whether or not the file is saved
        def save_update(event, something, var_mode):
            if saved.get() == 1:
                master.title("Worldbuilder")
            else:
                master.title("*Worldbuilder*")

        saved.trace('w', save_update)

        
        def img_setup():
            '''Function to set up images for tile/deco panels'''
            App.translate_tk2f = {0: 0}
            App.translate_f2tk = {0: 0}
            App.tiles = []
            App.decos = []
            App.load_tiles = {}
            for tile in list(App.tile_ids.items()):
                if tile[0] != 0:
                    img = PhotoImage(file=tile[0]).zoom(64).subsample(16)
                    App.tiles.append(img)
                    App.translate_tk2f[img] = tile[0]
                    App.translate_f2tk[tile[0]] = img
            for deco in list(App.deco_ids.items()):
                if deco[0] != 0:
                    img = PhotoImage(file=deco[0]).zoom(64).subsample(16)
                    App.decos.append(img)
                    App.translate_tk2f[img] = deco[0]
                    App.translate_f2tk[deco[0]] = img
            index = -1
            for load in ["assets/inactive_zone.png", "assets/reserved_zone.png", "assets/active_zone.png"]:
                index += 1
                App.load_tiles[index] = PhotoImage(file=load).zoom(64).subsample(16)
                
        
        def tile_panel_setup():
            self.tile_canvas = Canvas(self.tile_frame, width=72*3, height=72*8, bd=0)
            self.tile_canvas.grid(row=0, column=0, sticky=N+S+E+W)
            self.tile_canvas.grid_propagate(False)
            self.img_vbar = Scrollbar(self.tile_frame)
            self.img_vbar.config(command=self.tile_canvas.yview)
            self.img_vbar.grid(row=0, column=1, sticky=N+S)
            self.img_vbar.activate("slider")
            self.tile_x = -1
            self.tile_y = 0
            index = -1
            for tile in App.tiles:
                index += 1
                if App.translate_tk2f[tile] in App.groups[catagories.get()]:
                    self.tile_x += 1
                    if self.tile_x > 2:
                        self.tile_x = 0
                        self.tile_y += 1
                    radiobutton = Radiobutton(self.tile_canvas, image=tile, variable=selected_image, value=index, indicatoron=0)
                    self.tile_canvas.create_window(self.tile_x * 72 + 36, self.tile_y * 72 + 36, window=radiobutton)
            self.tile_canvas.config(scrollregion=self.tile_canvas.bbox("all"), yscrollcommand=self.img_vbar.set)

        def deco_panel_setup():
            '''Function to set up deco panel'''
            self.deco_canvas = Canvas(self.tile_frame, width=72*3, height=72*8, bd=0)
            self.deco_canvas.grid_propagate(False)
            self.deco_vbar = Scrollbar(self.tile_frame)
            self.deco_vbar.config(command=self.deco_canvas.yview)
            self.deco_vbar.activate("slider")
            self.deco_x = -1
            self.deco_y = 0
            index = -1
            for deco in App.decos:
                self.deco_x += 1
                index += 1
                if self.deco_x > 2:
                    self.deco_x = 0
                    self.deco_y += 1
                radiobutton = Radiobutton(self.deco_canvas, image=deco, variable=selected_deco, value=index, indicatoron=0)
                self.deco_canvas.create_window(self.deco_x * 72 + 36, self.deco_y * 72 + 36, window=radiobutton)
            self.deco_canvas.config(scrollregion=self.deco_canvas.bbox("all"), yscrollcommand=self.deco_vbar.set)

        def load_panel_setup():
            '''Function to set up loading zone panel'''
            self.load_canvas = Canvas(self.tile_frame, width=72*3, height=72*8, bd=0)
            self.load_canvas.grid_propagate(False)
            self.load_vbar = Scrollbar(self.tile_frame)
            self.load_vbar.config(command=self.load_canvas.yview)
            self.load_vbar.activate("slider")
            self.load_x = -1
            self.load_y = 0
            index = -1
            options = ["assets/delete_zone.png", "assets/new_zone.png", "assets/set_zone_destination.png", "assets/copy_zone_settings.png", "assets/paste_zone_settings.png"]
            self.load_imgs = []
            for i in options:
                self.load_imgs.append(PhotoImage(file=i).zoom(64).subsample(16))
            for img in self.load_imgs:
                self.load_x += 1
                index += 1
                if self.load_x > 2:
                    self.load_x = 0
                    self.load_y += 1
                radiobutton = Radiobutton(self.load_canvas, image=img, variable=selected_load, value=index, indicatoron=0)
                self.load_canvas.create_window(self.load_x * 72 + 36, self.load_y * 72 + 36, window=radiobutton)
            self.load_canvas.config(scrollregion=self.load_canvas.bbox("all"), yscrollcommand=self.load_vbar.set)

        def light_panel_setup():
            '''Function to set up loading zone panel'''
            self.light_canvas = Canvas(self.tile_frame, width=72*3, height=72*8, bd=0)
            self.light_canvas.grid_propagate(False)
            self.light_vbar = Scrollbar(self.tile_frame)
            self.light_vbar.config(command=self.light_canvas.yview)
            self.light_vbar.activate("slider")
            self.light_x = -1
            self.light_y = 0
            index = -1
            options = ["assets/delete_light.png", "assets/3x3_light_source.png"]
            self.light_imgs = []
            for i in options:
                self.light_imgs.append(PhotoImage(file=i).zoom(64).subsample(16))
            for img in self.light_imgs:
                self.light_x += 1
                index += 1
                if self.light_x > 2:
                    self.light_x = 0
                    self.light_y += 1
                radiobutton = Radiobutton(self.light_canvas, image=img, variable=selected_light, value=index, indicatoron=0)
                self.light_canvas.create_window(self.light_x * 72 + 36, self.light_y * 72 + 36, window=radiobutton)
            self.light_canvas.config(scrollregion=self.light_canvas.bbox("all"), yscrollcommand=self.light_vbar.set)

        def redraw_panels():
            '''Redraw tile/deco panels if needed'''
            original_cursor = cursor_mode.get()
            cursor_mode.set(2)
            master.update()
            self.tile_canvas.destroy()
            self.deco_canvas.destroy()
            self.load_canvas.destroy()
            self.light_canvas.destroy()
            img_setup()
            tile_panel_setup()
            deco_panel_setup()
            load_panel_setup()
            light_panel_setup()
            redraw_map_canvas()
            cursor_mode.set(original_cursor)

        # Actually set up tile and deco panels
        img_setup()
        tile_panel_setup()
        deco_panel_setup()
        load_panel_setup()
        light_panel_setup()
        
        
        # Tilemap window setup
        def draw_map(matrix):
            y = -1
            for i in matrix:
                y += 1
                x = -1
                for j in i:
                    x += 1
                    if matrix[y][x] != 0:
                        try:
                            self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=App.translate_f2tk[matrix[y][x]])
                        except KeyError:
                            self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=App.translate_f2tk['tiles/missing.png'])
                            print("An error occured while loading tilemap, \"{}\" was not found".format(matrix[y][x]))
                        
        
        def draw_grid():
            new_height = 64 * len(self.tilemap)
            new_width = 64 * len(self.tilemap[0])
            self.map_canvas.config(scrollregion=(0, 0, new_width, new_height))
            for i in range(0, new_height + 1):
                self.map_canvas.create_line(0, 64 * i, new_width, 64 * i)
            for j in range(0, new_width + 1):
                self.map_canvas.create_line(64 * j, 0, 64 * j, new_height)

        
        def redraw_map_canvas():
            self.map_canvas.delete("all")
            if force_grid.get() == 0:
                draw_grid()
            draw_map(self.tilemap)
            draw_map(self.decomap)
            if view_mode.get() == 2:
                for i in list(self.loading_zones.items()):
                    if i[1] != []:
                        self.map_canvas.create_image((32 + 64 * i[0][0], 32 + 64 * i[0][1]), image=App.load_tiles[2])
                    else:
                        self.map_canvas.create_image((32 + 64 * i[0][0], 32 + 64 * i[0][1]), image=App.load_tiles[0])
            elif view_mode.get() == 3:
                for i, j in self.light_sources:
                    self.map_canvas.create_image((32 + 64 * i, 32 + 64 * j), image=self.light_imgs[1])
            if force_grid.get() == 1:
                draw_grid()

        
        self.start = None
        def mark_start(event):
            '''Marks starting position of mouse for canvas dragging'''
            self.start = (event.x, event.y)
            callback(event)
            
        def callback(event):
            saved.set(0)
            if cursor_mode.get() == 0:
                # Canvas painting mode
                try:
                    dx = self.map_canvas.xview()[0] * len(self.tilemap[0])
                    dy = self.map_canvas.yview()[0] * len(self.tilemap)
                    x = max(int(dx + event.x / 64), 0)
                    y = max(int(dy + event.y / 64), 0)
                    # Regular base-layer tile mode
                    if view_mode.get() == 0:
                        map_of_tiles = list(self.tilemap)
                        self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=App.tiles[selected_image.get()])
                        row = list(map_of_tiles[y])
                        row[x] = App.translate_tk2f[App.tiles[selected_image.get()]]
                        map_of_tiles[y] = row
                    # Decoration layer mode
                    elif view_mode.get() == 1:
                        map_of_tiles = list(self.decomap)
                        row = list(map_of_tiles[y])
                        self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=App.decos[selected_deco.get()])
                        if selected_deco.get() != 0:
                            row[x] = App.translate_tk2f[App.decos[selected_deco.get()]]
                        else:
                            row[x] = 0
                        map_of_tiles[y] = row
                    # Loading zone mode
                    elif view_mode.get() == 2:
                        # Delete loading zone
                        if selected_load.get() == 0:
                            self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=self.load_imgs[0])
                            try:
                                del self.loading_zones[(x, y)]
                            except:
                                pass
                        # Add loading zone
                        elif selected_load.get() == 1:
                            self.loading_zones[(x, y)] = []
                            self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=self.load_imgs[1])
                        # Configure loading zone
                        elif selected_load.get() == 2:
                            self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=self.load_imgs[2])
                            if (x, y) in self.loading_zones:
                                new_loading_zone = EditLoadDestination(master, title="Edit Destination", args=self.loading_zones[(x, y)]).result
                                if new_loading_zone != None:
                                    self.loading_zones[(x, y)] = new_loading_zone
                            redraw_map_canvas()
                        # Copy loading zone settings
                        elif selected_load.get() == 3:
                            self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=self.load_imgs[3])
                            if (x, y) in self.loading_zones:
                                self.copied_load_settings = self.loading_zones[(x, y)]
                        # Paste loading zone settings
                        elif selected_load.get() == 4:
                            self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=self.load_imgs[4])
                            if (x, y) in self.loading_zones and self.copied_load_settings != None:
                                self.loading_zones[(x, y)] = self.copied_load_settings
                        else:
                            print("Unknown instruction")
                    # Lightmap mode
                    else:
                        # Delete light source
                        if selected_light.get() == 0:
                            try:
                                self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=self.light_imgs[0])
                                self.light_sources.remove((x, y))
                            except ValueError:
                                pass
                        # Add basic 3x3 light source
                        if selected_light.get() == 1:
                            if not (x, y) in self.light_sources:
                                self.light_sources.append((x, y))
                                self.map_canvas.create_image((32 + 64 * x, 32 + 64 * y), image=self.light_imgs[1])
                    
                except IndexError:
                    return
                if view_mode.get() == 0:
                    self.tilemap = map_of_tiles
                elif view_mode.get() == 1:
                    self.decomap = map_of_tiles
                else:
                    pass
                
            elif cursor_mode.get() == 1:
                # Canvas dragging mode
                if self.start != None:
                    self.map_canvas.scan_mark(self.start[0], self.start[1])
                    self.start = None
                self.map_canvas.scan_dragto(event.x, event.y, gain=1)

            else:
                # Do nothing, usually to lock-out input while canvas is reloading.
                pass


        def redraw(event):
            redraw_map_canvas()


        def set_coords_label(event):
            dx = self.map_canvas.xview()[0] * len(self.tilemap[0])
            dy = self.map_canvas.yview()[0] * len(self.tilemap)
            x = int(dx + event.x / 64)
            y = int(dy + event.y / 64)
            self.coords_label.config(text="x: {},    y: {}".format(x, y))
                        

        self.map_canvas = Canvas(self.map_frame, width=64*16, height=64*9, bg="WHITE", bd=0)
        self.map_canvas.grid(row=0, column=0)
        self.map_vbar = Scrollbar(self.map_frame)
        self.map_vbar.config(command=self.map_canvas.yview)
        self.map_vbar.grid(row=0, column=1, sticky=N+S)
        self.map_vbar.activate("slider")
        self.map_hbar = Scrollbar(self.map_frame, orient=HORIZONTAL)
        self.map_hbar.config(command=self.map_canvas.xview)
        self.map_hbar.grid(row=1, column=0, sticky=E+W)
        self.map_hbar.activate("slider")
        self.map_canvas.config(scrollregion=(0, 0, 64*16, 64*9), xscrollcommand=self.map_hbar.set, yscrollcommand=self.map_vbar.set)
        for i in range(0, 9 + 1):
            self.map_canvas.create_line(0, 64 * i, 64 * 16, 64 * i)
        for j in range(0, 16 + 1):
            self.map_canvas.create_line(64 * j, 0, 64 * j, 64 * 9)
        self.map_canvas.bind("<Button-1>", callback)
        self.map_canvas.bind("<ButtonPress-1>", mark_start)
        self.map_canvas.bind("<ButtonRelease-1>", redraw)
        self.map_canvas.bind("<B1-Motion>", callback)
        self.map_canvas.bind("<Motion>", set_coords_label)

        
        # Menu bar function setup
        def open_file():
            f = askopenfilename(filetypes=[("Tilemap", "*.tilemap")], defaultextension=[("Tilemap", "*.tilemap")])
            if f is '':
                return
            current_tilemap = self.tilemap
            current_decomap = self.decomap
            current_directory = self.directory
            current_colliders = self.colliders
            current_loading_zones = self.loading_zones
            #try:
            with open(f) as rf:
                new_tilemap = literal_eval(rf.readline())
                print("Found {} by {} tilemap".format(len(new_tilemap), len(new_tilemap[0])))
                self.tilemap = new_tilemap
                new_decomap = literal_eval(rf.readline())
                print("Found {} by {} decomap".format(len(new_decomap), len(new_decomap[0])))
                self.decomap = new_decomap
                new_colliders = literal_eval(rf.readline())
                print("Found collision list:", new_colliders)
                self.colliders = new_colliders
                new_loading_zones = literal_eval(rf.readline())
                print("Found loading zone dictionary:", new_loading_zones)
                self.loading_zones = new_loading_zones
                new_light_sources = literal_eval(rf.readline())
                print("Found light source list:", new_light_sources)
                self.light_sources = new_light_sources
                new_default_start = literal_eval(rf.readline())
                print("Found default spawn:", new_default_start)
                self.default_start = new_default_start
                redraw_map_canvas()
                self.directory = f
                saved.set(1)
##            except:
##                showwarning("File Error", "Error: Could not open file.")
##                self.tilemap = current_tilemap
##                self.decomap = current_decomap
##                self.directory = current_directory
##                self.colliders = current_colliders
##                self.loading_zones = current_loading_zones
##                redraw_map_canvas()
##                saved.set(0)
        

        def save_file():
            #print(list(len(i) for i in self.tilemap))
            if self.directory == "no_file":
                save_file_as()
            else:
                f = open(self.directory, "w")
                data_to_save = str(self.tilemap)
                data_to_save += "\n"
                data_to_save += str(self.decomap)
                data_to_save += "\n"
                data_to_save += str(self.colliders)
                data_to_save += "\n"
                data_to_save += str(self.loading_zones)
                data_to_save += "\n"
                data_to_save += str(self.light_sources)
                data_to_save += "\n"
                data_to_save += str(self.default_start)
                f.write(data_to_save)
                f.close()
                saved.set(1)
                

        def save_file_as():
            f = asksaveasfile(mode="w", filetypes=[("Tilemap", "*.tilemap")], defaultextension=[("Tilemap", "*.tilemap")])
            if f is None:
                return
            data_to_save = str(self.tilemap)
            data_to_save += "\n"
            data_to_save += str(self.decomap)
            data_to_save += "\n"
            data_to_save += str(self.colliders)
            data_to_save += "\n"
            data_to_save += str(self.loading_zones)
            data_to_save += "\n"
            data_to_save += str(self.light_sources)
            data_to_save += "\n"
            data_to_save += str(self.default_start)
            self.directory = f.name
            f.write(data_to_save)
            f.close()
            saved.set(1)

        def new():
            if saved.get() == 0:
                action = askyesnocancel("Worldbuilder", "Progress is unsaved.  Would you like to save first?", icon='warning')
                if action == False:
                    pass
                elif action == True:
                    save_file()
                    return
                else:
                    return
            self.tilemap = build_matrix(16, 9)
            self.decomap = build_matrix(16, 9)
            self.directory = "no_file"
            self.colliders = []
            self.loading_zones = {}
            self.copied_load_settings = None
            redraw_map_canvas()
                


        def tilemap2string(tilemap, ids, spacing):
            translated_map = []
            used_list = []
            rev_ids = dict((v,k) for k,v in ids.items())
            for i in range(len(tilemap)):
                translated_map.append([ids.get(item, item) for item in tilemap[i]])
            for i in translated_map:
                for j in i:
                    if not j in used_list:
                        used_list.append(j)
            used_list.sort()
            used = dict((item, rev_ids[item]) for item in used_list)
            string_version = "["
            for i in range(len(tilemap) - 1):
                string_version += str(translated_map[i]) + ",\n" + " " * (spacing + 1)
            string_version += str(translated_map[:-1]) + "]"
            return string_version, used

        
        def export_file():
            f = asksaveasfile(mode='w', filetypes=[('JSON File', '*.json')], defaultextension=[('JSON File', '*.json')])
            if f is None:
                return
            try:
                export_dict = {}

                # Translate the tilemap and decomap to numerical ID's
                translated_tilemap = []
                for i in self.tilemap:
                    translated_tilemap.append([App.tile_ids.get(item, item) for item in i])

                translated_decomap = []
                for i in self.decomap:
                    translated_decomap.append([App.deco_ids.get(item, item) for item in i])
                        
                # Export only colliders that are being used
                used_colliders = []
                for i in translated_tilemap:
                    for j in i:
                        if j in self.colliders:
                            used_colliders.append(j)
                            
                export_dict["colliders"] = used_colliders

                # Export tilemap and decomap
                export_dict["tilemap"] = translated_tilemap
                export_dict["decomap"] = translated_decomap

                # Export loading zones
                export_dict["loading_zones"] = []
                for i, j in self.loading_zones.items():
                    export_dict["loading_zones"].append({"zone": i,
                                                         "target_level": j[0],
                                                         "target_pos": j[1]
                                                         })

                # Export lightmap, default spawn, and level name
                export_dict["lightmap"] = self.light_sources
                export_dict["spawn"] = self.default_start
                export_dict["name"] = path.splitext(path.basename(f.name))[0]

                # Save dictionary as .json file
                json.dump(export_dict, f)
                
                
            except KeyError:
                showwarning("Export Error", "One of the exported images has not been assigned an ID.")
            f.close()


        def add_rows():
            number = EnterNumber(master, title="Add Rows", text="Add Rows").result
            if number is None or number < 0:
                return            
            for i in range(number):
                self.tilemap = add_row(self.tilemap)
                self.decomap = add_row(self.decomap)
            redraw_map_canvas()
            

        def add_columns():
            number = EnterNumber(master, title="Add Column", text="Add Column").result
            if number is None or number < 0:
                return
            for i in range(number):
                self.tilemap = add_column(self.tilemap)
                self.decomap = add_column(self.decomap)
            redraw_map_canvas()


        def delete_rows():
            number = EnterNumber(master, title="Delete Column", text="Delete Column").result
            if number is None:
                return            
            if len(self.tilemap) - number >= 9:
                for i in range(number):
                    self.tilemap = delete_row(self.tilemap)
                    self.decomap = delete_row(self.decomap)
                redraw_map_canvas()
            else:
                showwarning("Invalid Size", "Tilemaps cannot have a height smaller than 9 tiles.")


        def delete_columns():
            number = EnterNumber(master, title="Delete Column", text="Delete Column").result
            if number is None:
                return            
            if len(self.tilemap[0]) - number >= 16:
                for i in range(0, number):
                    self.tilemap = delete_column(self.tilemap)
                    self.decomap = delete_column(self.decomap)
                redraw_map_canvas()
            else:
                showwarning("Invalid Size", "Tilemaps cannot have a width smaller than 16 tiles.")

        def edit_default_pos():
            new_pos = Enter2Numbers(master, title="Default Spawn Position", text="(x, y)").result
            if new_pos is None:
                return
            if not(0 <= new_pos[0] <= len(self.tilemap[0])) or not(0 <= new_pos[1] <= len(self.tilemap)):
                showwarning("Invalid Position", "Spawn position must be on the map")
            else:
                self.default_start = new_pos

        def check_config():
            tile_ids_copy = dict(list(self.tile_ids.items())[1:])
            ids = list(i[1] for i in tile_ids_copy.items())
            dupes = [value for index, value in enumerate(ids) if value in ids[:index]]
            if dupes != []:
                showwarning("Tile Id List Error", 'Duplicate id(s) were found in the tile id list:\n{}\n\nPlease edit the list using "Manage Tile Ids" and check again for errors using "Check ID List"'.format(dupes))
            deco_ids_copy = dict(list(self.deco_ids.items())[1:])
            ids = list(i[1] for i in deco_ids_copy.items())
            dupes = [value for index, value in enumerate(ids) if value in ids[:index]]
            if dupes != []:
                showwarning("Decoration Id List Error", 'Duplicate id(s) were found in the decoration id list:\n{}\n\nPlease edit the list using "Manage Decoration Ids" and check again for errors using "Check ID List"'.format(dupes))
        

        def import_image():
            f = askopenfilename(defaultextension=".png")
            if f is '':
                return
            name = "tiles/" + path.basename(f)
            if path.isfile(name):
                print("Image is a duplicate")
                copy2(f, "tiles")
                redraw_panels()
                return
            try:
                copy2(f, "tiles")
            except:
                print("An error occured while loading image.  Is the image a duplicate?")
            img = PhotoImage(file=name).zoom(64).subsample(16)
            App.translate_tk2f[img] = name
            App.translate_f2tk[name] = img
            if view_mode.get() == 0:
                App.tiles.append(img)
                self.tile_x += 1
                if self.tile_x > 2:
                    self.tile_x = 0
                    self.tile_y += 1
                radiobutton = Radiobutton(self.tile_canvas, image=img, variable=selected_image, value=len(App.tiles)-1, indicatoron=0)
                self.tile_canvas.create_window(self.tile_x * 72 + 36, self.tile_y * 72 + 36, window=radiobutton)
                self.tile_canvas.config(scrollregion=self.tile_canvas.bbox("all"))
                App.tile_ids[name] = len(App.tile_ids) - 1
                with open("assets/image_config.config", 'w') as rf:
                    rf.write(str(App.tile_ids))
                    rf.write("\n")
                    rf.write(str(App.deco_ids))
                    rf.write("\n")
                    rf.write(str(App.groups))
            else:
                App.decos.append(img)
                self.deco_x += 1
                if self.deco_x > 2:
                    self.deco_x = 0
                    self.deco_y += 1
                radiobutton = Radiobutton(self.deco_canvas, image=img, variable=selected_deco, value=len(App.decos)-1, indicatoron=0)
                self.deco_canvas.create_window(self.deco_x * 72 + 36, self.deco_y * 72 + 36, window=radiobutton)
                self.deco_canvas.config(scrollregion=self.deco_canvas.bbox("all"))
                App.deco_ids[name] = len(App.deco_ids) - 1
                with open("assets/image_config.config", 'w') as rf:
                    rf.write(str(App.tile_ids))
                    rf.write("\n")
                    rf.write(str(App.deco_ids))
                    rf.write("\n")
                    rf.write(str(App.groups))
            App.groups["All"].append(name)
            check_config()


        
        # Catch window quiting when file is unsaved in order to prevent CATASTROPHE
        def catch_quit():
            if saved.get() == 0:
                action = askyesnocancel("Worldbuilder", "Progress is unsaved.  Would you like to save first?", icon='warning')
                if action == False:
                    root.destroy()
                elif action == True:
                    save_file()
                else:
                    pass
            else:
                root.destroy()
        
        master.protocol('WM_DELETE_WINDOW', catch_quit)


        def edit_tile_ids():
            new_ids = EditTileIds(master, title="Edit Image IDs").result
            if new_ids != None:
                App.tile_ids = new_ids
                with open("assets/image_config.config", 'w') as wf:
                    wf.write(str(App.tile_ids))
                    wf.write("\n")
                    wf.write(str(App.deco_ids))
                    wf.write("\n")
                    wf.write(str(App.groups))

        def edit_deco_ids():
            new_ids = EditDecoIds(master, title="Edit Decoration IDs").result
            if new_ids != None:
                App.deco_ids = new_ids
                with open("assets/image_config.config", 'w') as wf:
                    wf.write(str(App.tile_ids))
                    wf.write("\n")
                    wf.write(str(App.deco_ids))
                    wf.write("\n")
                    wf.write(str(App.groups))

        def edit_colliders():
            new_list = EditColliderList(master, title="Edit Collider List", args=self.colliders).result
            if new_list != None:
                self.colliders = new_list

        def edit_groups():
            new_groups = EditCatagories(master, title="Edit Tile Catagories", args=App.groups).result
            if new_groups == None:
                return
            for i in new_groups:
                new_groups[i].insert(0, "tiles/missing.png")
            App.groups = new_groups
            with open("assets/image_config.config", 'w') as wf:
                wf.write(str(App.tile_ids) + "\n" + str(App.deco_ids) + "\n" + str(App.groups))
            options = list(i[0] for i in App.groups.items())
            catagories.set(options[0])
            self.groups_menu = OptionMenu(self.menu_frame, catagories, *options)
            self.groups_menu.grid(row=0, column=8)
            redraw_panels()

        def copy_tile_dict():
            temp_dict = dict((j, i) for i, j in App.tile_ids.items() if j != 0)
            #print(temp_dict)
            root.clipboard_clear()
            #root.clipboard_append('i can has clipboardz?')
            root.clipboard_append(str(temp_dict))

        def copy_deco_dict():
            temp_dict = dict((j, i) for i, j in App.deco_ids.items() if j != 0)
            #print(temp_dict)
            root.clipboard_clear()
            #root.clipboard_append('i can has clipboardz?')
            root.clipboard_append(str(temp_dict))

        def about():
            showwarning("Error", "This feature is not yet available.")

        
        # Menubar setup
        self.menubar = Menu(master)
        # File menubar
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open                    Ctrl+O", command=open_file)
        self.filemenu.add_command(label="Save                      Ctrl+S", command=save_file)
        self.filemenu.add_command(label="Save As", command=save_file_as)
        self.filemenu.add_command(label="New                       Ctrl+N", command=new)
        self.filemenu.add_command(label="Export Tilemap    Ctrl+E", command=export_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Copy Tile Dictionary to Clipboard", command=copy_tile_dict)
        self.filemenu.add_command(label="Copy Deco Dictionary to Clipboard", command=copy_deco_dict)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=master.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        # Edit menubar
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Add Rows", command=add_rows)
        self.editmenu.add_command(label="Add Columns", command=add_columns)
        self.editmenu.add_command(label="Delete Rows", command=delete_rows)
        self.editmenu.add_command(label="Delete Columns", command=delete_columns)
        self.editmenu.add_command(label="Default Spawn Position", command=edit_default_pos)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        # Palette menubar
        self.palettemenu = Menu(self.menubar, tearoff=0)
        self.palettemenu.add_command(label="Import Image      Ctrl+I", command=import_image)
        self.palettemenu.add_command(label="Manage Tile Ids", command=edit_tile_ids)
        self.palettemenu.add_command(label="Manage Decoration Ids", command=edit_deco_ids)
        self.palettemenu.add_command(label="Manage Colliders", command=edit_colliders)
        self.palettemenu.add_separator()
        self.palettemenu.add_command(label="Manage Palette Groups", command=edit_groups)
        self.palettemenu.add_separator()
        self.palettemenu.add_command(label="Check ID List", command=check_config)
        self.menubar.add_cascade(label="Palette", menu=self.palettemenu)
        # Help menubar
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        # Finish menubar setup
        master.config(menu=self.menubar)
        

        # Function shortcut keys
        def ctrl_s(event):
            save_file()

        def ctrl_o(event):
            open_file()

        def ctrl_n(event):
            new()

        def ctrl_e(event):
            export_file()

        def ctrl_i(event):
            import_image()

        def mode_cursor(event):
            cursor_mode.set(0)

        def mode_pan(event):
            cursor_mode.set(1)

        def mode_ground(event):
            view_mode.set(0)

        def mode_decoration(event):
            view_mode.set(1)

        def mode_loading_zones(event):
            view_mode.set(2)

        def mode_lightmap(event):
            view_mode.set(3)
        
        master.bind('<Control-s>', ctrl_s)
        master.bind('<Control-o>', ctrl_o)
        master.bind('<Control-n>', ctrl_n)
        master.bind('<Control-e>', ctrl_e)
        master.bind('<Control-i>', ctrl_i)
        master.bind("<Key-1>", mode_cursor)
        master.bind("<Key-2>", mode_pan)
        master.bind("<Key-3>", mode_ground)
        master.bind("<Key-4>", mode_decoration)
        master.bind("<Key-5>", mode_loading_zones)
        master.bind("<Key-6>", mode_lightmap)
        check_config()
        
        
print("Todo:")
print("-Do help menu")
print("-Add more controls for easier use")
print("\t*Add/Delete row/column at some position button")
print("\t*Shift field button")
print("\t*Control-z feature?")
print("\nPlanned:")
print("-Sprite layer (npcs, enemies, interactables, etc.)")

root = Tk()

app = App(root)

root.mainloop()
try:
    root.destroy()
except TclError:
    pass
