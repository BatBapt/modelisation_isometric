import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import askquestion
import sys

from user_action import UserAction
from grid import Grid
from container import Container


class CanvasApp(tk.Canvas):
    """
    This is the canvas application class
    In the MVC pattern, this is the View
    """
    def __init__(self, cubes_size, grid_size, master):
        try:
            assert isinstance(cubes_size, int), 'Erreur Création Grille: la taille des cubes doit être un entier'
            assert isinstance(grid_size, int), 'Erreur Création Grille: la taille de la grille doit être un entier'
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self.cubes_size = cubes_size
        self.grid_size = grid_size
        self.master = master
        tk.Canvas.__init__(self, self.master)

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_heigt = self.master.winfo_screenheight()

        self.canvas = tk.Canvas(self.master, width=self.screen_width // 2 + 450, height=self.screen_heigt // 2 + 400)
        self.canvas.pack(side=tk.LEFT)

        self.grid = Grid(self.screen_width // 2 + 300, self.screen_heigt // 2 + 900, self.cubes_size, self.grid_size,
                         self.canvas)
        self.draw_support()

        self.container = Container(self.grid, self.canvas)
        self.__list_cube = self.container.liste_cube
        self.__dict_case = self.container.list_poly_to_dict_case()

        self.user_action = UserAction(self.master)

        self.canvas.bind('<Button-3>', self.popup)
        self.canvas.bind('<Button-1>', self.click_on_cube)
        self.canvas.bind_all('<Control-z>', self.delete_last)
        self.canvas.bind_all('<Control-s>', self.save)
        self.canvas.bind_all('<Control-d>', self.delete)
        self.canvas.bind_all('<F1>', self.user_action.call_help)
        self.canvas.bind_all('<F2>', self.user_action.about)

        self.has_been_saved = False

    @property
    def list_cube(self):
        return self.__list_cube

    @list_cube.setter
    def list_cube(self, new_list):
        try:
            assert isinstance(new_list, list), 'Erreur: le paramètre doit être une liste'
        except AssertionError as e:
            print(e)
            sys.exit(-1)

    @property
    def dict_case(self):
        return self.__dict_case

    def delete_last(self, event):
        """
        This function allows the user to press Ctrl+Z to delete the last cube created
        :param event: Ctrl + Z
        :return:
        """
        if len(self.__list_cube) > 0:
            cube = self.__list_cube.pop()
            self.canvas.delete(cube[0])
            self.canvas.delete(cube[1])
            self.canvas.delete(cube[2])
            self.user_action.display_info_app(len(self.__list_cube))

    def popup(self, event):
        """
        This function create the pop up menu when the user right click on the screen
        :param event: Button 1
        :return:
        """
        global popup_menu

        popup_menu = tk.Menu(self.master, tearoff=0)
        # Function used to create a custom cube
        popup_menu.add_command(label="Créer cube personnalisé ici",
                               command=lambda canv=self.canvas, contain=self.container, case_dict=self.__dict_case, grid=self.grid:
                               self.user_action.preprocess_creation(
                                   event,
                                   x=event.x,
                                   y=event.y,
                                   canvas=canv,
                                   container=contain,
                                   dict_case=case_dict,
                                   grid=grid,
                                   instant=False
                               ),
                               )

        # Function used_to create a cube with his default info
        popup_menu.add_command(label="Créer instantanément un cube ici",
                               command=lambda canv=self.canvas, contain=self.container, case_dict=self.__dict_case, grid=self.grid:
                               self.user_action.preprocess_creation(
                                   event,
                                   x=event.x,
                                   y=event.y,
                                   canvas=canv,
                                   container=contain,
                                   dict_case=case_dict,
                                   grid=grid,
                                   instant=True
                               ),
                               )

        # Function used to created a columns of cube
        popup_menu.add_command(label="Créer colonne ici",
                               command=lambda canv=self.canvas, contain=self.container, case_dict=self.__dict_case, grid=self.grid:
                               self.user_action.preprocess_creation(
                                   event,
                                   x=event.x,
                                   y=event.y,
                                   canvas=canv,
                                   container=contain,
                                   dict_case=case_dict,
                                   grid=grid,
                                   instant=False,
                                   kind="columns",
                               ))
        popup_menu.add_command(label="Créer ligne ici",
                               command=lambda canv=self.canvas, contain=self.container, case_dict=self.__dict_case, grid=self.grid:
                               self.user_action.preprocess_creation(
                                   event,
                                   x=event.x,
                                   y=event.y,
                                   canvas=canv,
                                   container=contain,
                                   dict_case=case_dict,
                                   grid=grid,
                                   instant=False,
                                   kind="lines",
                               ))
        popup_menu.add_separator()
        popup_menu.add_command(label="Detruire cube",
                                command=lambda canv=self.canvas, contain=self.container, cube_list=self.__list_cube:
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

    def save(self, event=None):
        """
        This function is the pre-process to save the canvas as SVG file
        :param event: Binding Ctrl + S
        :return:
        """
        file = asksaveasfile(mode="w", defaultextension=".svg")
        try:
            file_name = file.name
        except AttributeError as e:
            print("{}: Pas de nom de fichier.".format(e))

        save_dict = {}
        liste_color = []
        for cube in self.__list_cube:
            tags = self.canvas.gettags(cube[1])
            coords = tags[7]
            barys = [tags[2], tags[3]]
            if int(tags[6]) > 0:
                barys[1] = int(barys[1]) + int(tags[6]) * self.cubes_size
            for faces in cube:
                tags = self.canvas.gettags(faces)
                color = tags[8]
                liste_color.append(color)

            save_dict[coords] = [barys, tags[6], liste_color]  # We stock all the informations we need

        self.has_been_saved = True
        self.user_action.save_final(file_name, save_dict, self.cubes_size, self.grid_size)

    def destroy_popup(self, event):
        """
        This function dismiss the right click (Button 3) popup by clicking on the left click (Button 1)
        :param event: Button 1
        :return:
        """
        popup_menu.unpost()
        self.canvas.bind('<Button-1>', self.click_on_cube)

    def delete(self, event=None):
        """
        Delte all cubes in the Grid
        """
        answer = askquestion("Attention", "Êtes vous sûr de supprimer tout les cubes de la grille?")
        if answer == "yes":
            self.__list_cube = []
            self.canvas.delete("cube")

    def draw_support(self, event=None):
        """
        Draw the entire grid
        """
        self.grid.draw_grid()

    def click_on_cube(self, event):
        """
        By clicking on a cube, display all the information about it
        If the clicked widget is not a cube, hide all informations
        """
        for cube in self.__list_cube:
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
