import tkinter as tk

from tkinter import messagebox
from tkinter import colorchooser

import functions as functions
from cube import Cube


class UserActionFrame(tk.Frame):
    top_level = None
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)

        self.screen_width = self.winfo_screenwidth()
        self.screen_heigt = self.winfo_screenheight()

        self.height_main_frame = (self.screen_heigt//2)+200

        self.master_frame = tk.Frame(self.master, width=200, height=self.height_main_frame)
        self.master_frame.pack(side=tk.RIGHT)

        self.info_app_frame = tk.Frame(self.master_frame, width=200, height=self.height_main_frame//2-200)
        self.info_app_frame.pack(side=tk.TOP)

        self.info_app_nb_cubes = tk.Label(self.info_app_frame, text="Il y a actuellement: 0 cubes")
        self.info_app_nb_cubes.pack()

        self.info_cube_frame = tk.Frame(self.master_frame, width=200, height=self.height_main_frame//2+200)
        self.info_cube_frame.pack(fill=tk.Y)

        self.id_cube_label = tk.Label(self.info_cube_frame)
        self.update_cube_btn = tk.Button(self.info_cube_frame)

        self.info_canv = tk.Canvas(self.info_cube_frame, width=200, height=250)
        self.info_canv.pack()

        self.color1 = 'GRAY55'
        self.color2 = 'GRAY80'
        self.color3 = 'GRAY22'

    def display_info_app(self, new_info):
        self.info_app_nb_cubes['text'] = "Il y a actuellement {} cubes".format(new_info)

    def find_cube_with_id(self, canv, cube_id):
        item_cube = canv.find_withtag(cube_id)
        dict_cube = {}
        for i in range(len(item_cube)):
            color = canv.itemcget(item_cube[i], "fill")
            tags = canv.itemcget(item_cube[i], 'tags').split(" ")
            canv.itemconfig(item_cube[i], outline="red")

            dict_cube[item_cube[i]] = [color, tags[4], tags[5]]
        return dict_cube

    def display_info(self, tags_item, canvas):
        try:
            cube = [s for s in tags_item if "cpt_" in s]
            print(cube)
        except IndexError:
            print("Erreur {UserActionFrame/display_info}: no such id")

        dico_cube = self.find_cube_with_id(canvas, cube[0])

        self.id_cube_label['text'] = "Id du cube: {}".format(cube[0][4:])
        self.id_cube_label.pack()

        self.info_canv.delete("all")

        i = 0
        j = 0
        list_pos = ['first', 'second', 'third']
        for key, value in dico_cube.items():
            self.info_canv.create_text(100, 20+i, text="Couleur de la face {}".format(value[1]))
            self.info_canv.create_rectangle(100, 30+i, 120, 50+i, fill=value[0], tags=("color", value[0], list_pos[j]))
            j += 1
            i += 50

        self.update_cube_btn['text'] = "Modifier le cube"
        self.update_cube_btn['command'] = lambda cube=dico_cube: self.update_cube(cube)

        self.update_cube_btn.pack()


    def update_cube(self, dict_cube):
        UserActionFrame.top_level = tk.Toplevel(self.master, width=300, height=400)
        UserActionFrame.top_level.geometry("300x300+{}+250".format(self.screen_width//3))
        UserActionFrame.top_level.title("Modification d'un cube")
        UserActionFrame.top_level.grab_set()

    def create_cube(self, event, **kwargs):
        x = float(kwargs['x'])
        y = float(kwargs['y'])
        canvas = kwargs['canvas']
        container = kwargs['container']
        dict_case_grid = kwargs['dict_case']
        instant = kwargs['instant']

        id_case_closest = canvas.find_closest(x, y)
        tags = canvas.gettags(id_case_closest)

        bary_x_closest = int(tags[2])
        bary_y_closest = int(tags[3])
        try:
            face = tags[4]
        except IndexError:
            pass

        try:
            if face == "haut":
                if str(bary_y_closest)[-1] == '3' or str(bary_y_closest)[-1] == '8':
                    bary_y_closest -= 25

            elif face == "droite":
                bary_x_closest += 25
                bary_y_closest += 13

            elif face == "gauche":
                bary_x_closest -= 25
                bary_y_closest += 13

            else:
                bary_y_closest -= 25
            if instant:
                self.create_instant_cube(
                    [
                        50,
                        [self.color1, self.color2, self.color3],
                        [bary_x_closest, bary_y_closest],
                        canvas,
                        container,
                        dict_case_grid,
                        id_case_closest[0],
                    ]
                )
            else:
                self.custom_cube(
                    [bary_x_closest, bary_y_closest],
                    canvas,
                    container,
                    dict_case_grid,
                    id_case_closest[0],
                )

        except UnboundLocalError:
            pass

    def custom_cube(self, coords, canv, container, dict_case, id_case):
        UserActionFrame.top_level = tk.Toplevel(self.master, width=300, height=400)
        UserActionFrame.top_level.geometry("300x300+{}+250".format(self.screen_width//3))
        UserActionFrame.top_level.title("Ajout d'un cube")
        UserActionFrame.top_level.grab_set()
        frame = tk.Frame(UserActionFrame.top_level, width=300, height=150)
        frame.pack()
        canvas = tk.Canvas(UserActionFrame.top_level, width=300, height=200)
        canvas.pack()
        button_frame = tk.Frame(UserActionFrame.top_level, width=300, height=50)
        button_frame.pack()

        size = tk.IntVar()
        tk.Label(frame, text="Taille du cube: ").pack()

        entry_size = tk.Entry(frame, textvariable=size)
        entry_size.pack()

        canvas.create_text(150, 20, text="Couleur de la face gauche")
        color_left = canvas.create_rectangle(140, 30, 160, 50, fill=self.color1, tags=("color", "first", self.color1))

        canvas.create_text(150, 70, text="Couleur de la face du dessus")
        color_top = canvas.create_rectangle(140, 80, 160, 100, fill=self.color2, tags=("color", "second", self.color2))

        canvas.create_text(150, 120, text="Couleur de la face droite")
        color_right = canvas.create_rectangle(140, 130, 160, 150, fill=self.color3, tags=("color", "third", self.color3))

        canvas.tag_bind("color", '<Button-1>', lambda event, canvas=canvas:
            self.choose_color(event, canvas)
        )

        create_button = tk.Button(button_frame, text="Créer le boutton",
            command=lambda: self.create(
                size=entry_size,
                colors=[color_left, color_top, color_right],
                coords=coords,
                main_canvas=canv,
                top_canvas=canvas,
                container=container,
                dict_case=dict_case,
                id_case=id_case,
            ),
        )
        create_button.pack()


    def choose_color(self, event, canvas):
        id_item = canvas.find_withtag('current')
        tags = canvas.gettags(id_item)

        color = colorchooser.askcolor(title="Choisir une couleur")
        if id_item[0] == 2:
            pos = "first"
        elif id_item[0] == 4:
            pos = "second"
        elif id_item[0] == 6:
            pos = "third"

        canvas.itemconfig(id_item, fill=color[1])
        canvas.itemconfig(id_item, tags=('color', pos, color[1]))

    def create(self, event=None, **kwargs):
        try:
            size = int(kwargs['size'].get())
        except AttributeError:
            pass
        colors = kwargs['colors']
        coords = kwargs['coords']
        main_canvas = kwargs['main_canvas']
        top_canvas = kwargs['top_canvas']
        container = kwargs['container']
        dict_case_grid = kwargs['dict_case']
        id_case = kwargs['id_case']

        list_color = []
        for i in range(len(colors)):
            list_color.append(top_canvas.itemcget(colors[i], "tags").split(" ")[2])

        cube = Cube(coords, size, list_color, main_canvas)
        id_item = main_canvas.find_withtag('current')

        container.set_liste_cube(cube)
        self.display_info_app(len(container.get_liste_cube()))


        try:
            dict_case_grid[id_case][1] = 1
        except KeyError:
            # Ce produit lorsqu'on empile des cubes.
            pass

        UserActionFrame.top_level.destroy()

    def create_instant_cube(self, list_param):
        size = list_param[0]
        colors = list_param[1]
        coords = list_param[2]
        main_canvas = list_param[3]
        container = list_param[4]
        dict_case_grid = list_param[5]
        id_case = list_param[6]

        cube = Cube(coords, size, colors, main_canvas)
        id_item = main_canvas.find_withtag('current')

        try:
            dict_case_grid[id_case][1] = 1
        except KeyError:
            # Ce produit lorsqu'on empile des cubes.
            pass

        container.set_liste_cube(cube)
        self.display_info_app(len(container.get_liste_cube()))
