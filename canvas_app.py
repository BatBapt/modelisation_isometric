import tkinter as tk
from math import sqrt

import functions as functions

from user_action_frame import UserActionFrame
from grid import Grid
from cube import Cube


class CanvasApp(tk.Canvas):

    def __init__(self, master):
        self.master = master
        tk.Canvas.__init__(self, self.master)

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_heigt = self.master.winfo_screenheight()

        self.canvas = tk.Canvas(self.master, width=self.screen_width//2+200, height=self.screen_heigt//2 + 200)
        self.canvas.pack(side=tk.LEFT)

        self.grid = Grid(self.screen_width // 2, self.screen_heigt//2 + 200, 50, self.canvas)
        self.draw_support()
        self.list_cube = self.grid.list_cube

        self.user_action = UserActionFrame(self.master)

        self.canvas.bind('<Button-3>', self.popup)
        self.canvas.bind('<Button-1>', self.click_on_cube)
        self.canvas.bind_all('<Control-z>', self.delete_last)

    def delete_last(self, event):
        if len(self.list_cube) > 0:
            cube = self.list_cube.pop()
            self.canvas.delete(cube[0])
            self.canvas.delete(cube[1])
            self.canvas.delete(cube[2])

    def popup(self, event):
        global popup_menu
        popup_menu = tk.Menu(self.master, tearoff=0)
        popup_menu.add_command(label="Créer cube ici",
            command=lambda canv=self.canvas, cube=self.list_cube: self.user_action.create_cube(
                event,
                x=event.x,
                y=event.y,
                canvas=canv,
                cubes=cube),
        )
        popup_menu.add_separator()
        popup_menu.add_command(label="Detruire block",
            command=lambda: self.destroy_cube(
            event,
            )
        )
        try:
            popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            popup_menu.grab_release()

        self.canvas.bind('<Button-1>', self.destroy_popup)

    def destroy_popup(self, event):
        popup_menu.unpost()
        self.canvas.bind('<Button-1>', self.click_on_cube)

    def destroy_cube(self, event):
        id_case_closest = self.canvas.find_closest(event.x, event.y)

        for i in range(len(self.list_cube)):
            try:
                if id_case_closest[0] in self.list_cube[i]:
                    cube = self.list_cube.pop(i)
                    self.canvas.delete(cube[0])
                    self.canvas.delete(cube[1])
                    self.canvas.delete(cube[2])
            except IndexError:
                pass

    def delete(self):
        self.list_cube = []
        self.canvas.delete("cube")

    def draw_house(self):
        # colonne arrière
        functions.draw_cube_col([580, 235], 4, 50, self.canvas)

        # ligne arrière haute droite
        functions.draw_cube_row([630, 110], 2, 50, "right", self.canvas)
        # ligne arrière basse droite
        functions.draw_cube_row([630, 260], 2, 50, "right", self.canvas)
        # colonne arrière droite
        functions.draw_cube_col([730, 310], 4, 50, self.canvas)

        # ligne arrière basse gauche
        functions.draw_cube_row([530, 260], 2, 50, "left", self.canvas)
        # colonne avant gauche
        functions.draw_cube_col([430, 310], 3, 50, self.canvas)
        # ligne arrière haute gauche
        functions.draw_cube_row([530, 110], 3, 50, 'left', self.canvas)

        # ligne avant haute droite
        functions.draw_cube_row([680, 185], 2, 50, "left", self.canvas)
        # ligne avant basse droite
        functions.draw_cube_row([680, 335], 2, 50, "left", self.canvas)

        # ligne avant haute gauche
        functions.draw_cube_row([480, 185], 2, 50, "right", self.canvas)
        # ligne avant basse gauche
        functions.draw_cube_row([480, 335], 2, 50, "right", self.canvas)

        # colonne avant
        functions.draw_cube_col([580, 385], 4, 50, self.canvas)

    def draw_support(self):
        self.grid.draw_grid()

    def click_on_cube(self, event):
        try:
            id_item = self.canvas.find_withtag("current")
            tags = self.canvas.gettags(id_item)
            if tags[0] == "cube":
                self.user_action.display_info(tags, self.canvas)
        except IndexError:
            pass
