import tkinter as tk
from math import sqrt
import sys

from user_action import UserAction
from grid import Grid
from cube import Cube
from container import Container


class CanvasApp(tk.Canvas):
    """
    This is the canvas application class
    In the MVC pattern, this is the View
    """
    def __init__(self, cubes_size, master):
        try:
            assert isinstance(cubes_size, int), 'Erreur Création Grille: la taille des cubes doit être un entier'
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self.cubes_size = cubes_size
        self.master = master
        tk.Canvas.__init__(self, self.master)

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_heigt = self.master.winfo_screenheight()

        self.canvas = tk.Canvas(self.master, width=self.screen_width // 2 + 450, height=self.screen_heigt // 2 + 400)
        self.canvas.pack(side=tk.LEFT)

        self.grid = Grid(self.screen_width // 2 + 300, self.screen_heigt // 2 + 900, self.cubes_size, self.canvas)
        self.draw_support()

        self.container = Container(self.grid, self.canvas)
        self.list_cube = self.container.liste_cube
        self.dict_case = self.container.list_poly_to_dict_case()

        self.user_action = UserAction(self.master)

        self.canvas.bind('<Button-3>', self.popup)
        self.canvas.bind('<Button-1>', self.click_on_cube)
        self.canvas.bind_all('<Control-z>', self.delete_last)

    def delete_last(self, event):
        """
        This function allows the user to press Ctrl+Z to delete the last cube created
        :param event: Ctrl + Z
        :return:
        """
        if len(self.list_cube) > 0:
            cube = self.list_cube.pop()
            self.canvas.delete(cube[0])
            self.canvas.delete(cube[1])
            self.canvas.delete(cube[2])
            self.user_action.display_info_app(len(self.list_cube))

    def popup(self, event):
        """
        This function create the pop up menu when the user right click on the screen
        :param event: Button 1
        :return:
        """
        global popup_menu

        popup_menu = tk.Menu(self.master, tearoff=0)
        # Function used to create a custom cube
        popup_menu.add_command(label="Créer custom cube ici",
                               command=lambda canv=self.canvas, contain=self.container, case_dict=self.dict_case:
                               self.user_action.preprocess_creation(
                                   event,
                                   x=event.x,
                                   y=event.y,
                                   canvas=canv,
                                   container=contain,
                                   dict_case=case_dict,
                                   instant=False
                               ),
                               )

        # Function used_to create a cube with his default info
        popup_menu.add_command(label="Créer cube ici",
                               command=lambda canv=self.canvas, contain=self.container, case_dict=self.dict_case:
                               self.user_action.preprocess_creation(
                                   event,
                                   x=event.x,
                                   y=event.y,
                                   canvas=canv,
                                   container=contain,
                                   dict_case=case_dict,
                                   instant=True
                               ),
                               )

        # Function used to created a columns of cube
        popup_menu.add_command(label="Créer colonne ici",
                               command=lambda canv=self.canvas, contain=self.container, case_dict=self.dict_case:
                               self.user_action.preprocess_creation(
                                   event,
                                   x=event.x,
                                   y=event.y,
                                   canvas=canv,
                                   container=contain,
                                   dict_case=case_dict,
                                   instant=False,
                                   kind="columns",
                               ))
        popup_menu.add_command(label="Créer ligne ici",
                               command=lambda canv=self.canvas, contain=self.container, case_dict=self.dict_case:
                               self.user_action.preprocess_creation(
                                   event,
                                   x=event.x,
                                   y=event.y,
                                   canvas=canv,
                                   container=contain,
                                   dict_case=case_dict,
                                   instant=False,
                                   kind="lines",
                               ))
        popup_menu.add_separator()
        popup_menu.add_command(label="Detruire cube",
                                command=lambda canv=self.canvas, contain=self.container, cube_list=self.list_cube:
                                 self.user_action.destroy_cube(
                                    event,
                                    canvas=canv,
                                    container=contain,
                                    list_cube=cube_list
                                ))

        try:
            popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            popup_menu.grab_release()

        self.canvas.bind('<Button-1>', self.destroy_popup)

    def destroy_popup(self, event):
        """
        This function dismiss the right click (Button 3) popup by clicking on the left click (Button 1)
        :param event: Button 1
        :return:
        """
        popup_menu.unpost()
        self.canvas.bind('<Button-1>', self.click_on_cube)

    def delete(self):
        """
        Delte all cubes in the Grid
        """
        self.list_cube = []
        self.canvas.delete("cube")

    def draw_support(self):
        """
        Draw the entire grid
        """
        self.grid.draw_grid()

    def click_on_cube(self, event):
        """
        By clicking on a cube, display all the information about it
        If the clicked widget is not a cube, hide all informations
        """
        for cube in self.list_cube:
            for i in range(len(cube)):
                self.canvas.itemconfig(cube[i], outline="black")
        try:
            id_item = self.canvas.find_withtag("current")
            tags = self.canvas.gettags(id_item)
            if tags[0] == "cube":
                self.user_action.display_info(tags, self.canvas)
            else:
                self.user_action.clean_info()
        except IndexError:
            pass
