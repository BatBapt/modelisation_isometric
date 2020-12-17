import tkinter as tk

from tkinter import messagebox
from tkinter import colorchooser

import functions as functions
from cube import Cube


class UserActionFrame(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)

        self.screen_width = self.winfo_screenwidth()
        self.screen_heigt = self.winfo_screenheight()

        self.height_main_frame = (self.screen_heigt//2)+200

        self.master_frame = tk.Frame(self.master, width=200, height=self.height_main_frame, bg="red")
        self.master_frame.pack(side=tk.RIGHT)

        self.info_frame = tk.Frame(self.master_frame, width=200, height=self.height_main_frame, bg="green")
        self.info_frame.pack(side=tk.TOP)

        self.info_label = tk.Label(self.info_frame)

        self.color1 = 'GRAY55'
        self.color2 = 'GRAY80'
        self.color3 = 'GRAY22'

    def find_cube_with_id(self, canv, cube_id):
        item_cube = canv.find_withtag(cube_id)

        for i in range(len(item_cube)):
            print(canv.itemcget(item_cube[i], "fill"))

    def display_info(self, tags_item, canvas):
        try:
            cube = [s for s in tags_item if "cpt_" in s]
        except IndexError:
            print("Erreur {UserActionFrame/display_info}")

        self.find_cube_with_id(canvas, cube[0])

        self.info_label['text'] = "Id du cube: {}".format(cube[0][4:])
        self.info_label.pack()

    def create_cube(self, event, **kwargs):
        x = float(kwargs['x'])
        y = float(kwargs['y'])
        canvas = kwargs['canvas']
        cubes = kwargs['cubes']

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

            self.custom_cube([bary_x_closest, bary_y_closest], canvas, cubes)
        except UnboundLocalError:
            pass

    def custom_cube(self, coords, canv, liste_cube):
        self.top_level = tk.Toplevel(self.master, width=300, height=400)
        frame = tk.Frame(self.top_level, width=300, height=150)
        frame.pack()
        canvas = tk.Canvas(self.top_level, width=300, height=200)
        canvas.pack()
        button_frame = tk.Frame(self.top_level, width=300, height=50)
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
                cubes=liste_cube
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
        size = int(kwargs['size'].get())
        colors = kwargs['colors']
        coords = kwargs['coords']
        main_canvas = kwargs['main_canvas']
        top_canvas = kwargs['top_canvas']
        cubes = kwargs['cubes']

        list_color = []
        for i in range(len(colors)):
            list_color.append(top_canvas.itemcget(colors[i], "tags").split(" ")[2])

        cube = Cube(coords, size, list_color, main_canvas)
        id_item = main_canvas.find_withtag('current')

        cubes.append(cube.get_cubes())

        self.top_level.destroy()
