import tkinter as tk

from tkinter import messagebox
from tkinter import colorchooser

from cube import Cube
from cube_factory import CubeFactory


class UserAction(tk.Frame):
    """
    This is the User Action Frame
    In the MVC pattern, this is the Controller
    """
    top_level = None

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)

        self.screen_width = self.winfo_screenwidth()
        self.screen_heigt = self.winfo_screenheight()

        self.height_main_frame = self.screen_heigt // 2

        self.master_frame = tk.Frame(self.master, width=400, height=self.height_main_frame)
        self.master_frame.pack(side=tk.RIGHT)

        self.info_app_frame = tk.Frame(self.master_frame, width=400, height=self.height_main_frame // 2 - 200)
        self.info_app_frame.pack(side=tk.TOP)

        self.info_app_nb_cubes = tk.Label(self.info_app_frame, text="Il y a actuellement: 0 cubes")
        self.info_app_nb_cubes.pack()

        self.info_cube_frame = tk.Frame(self.master_frame, width=300, height=self.height_main_frame // 2 + 200)
        self.info_cube_frame.pack(fill=tk.Y)

        self.id_cube_label = tk.Label(self.info_cube_frame)
        self.update_cube_btn = tk.Button(self.info_cube_frame)

        self.info_canv = tk.Canvas(self.info_cube_frame, width=250, height=250)
        self.info_canv.pack()

        self.color1 = 'GRAY55'
        self.color2 = 'GRAY80'
        self.color3 = 'GRAY22'

    def display_info_app(self, new_info):
        """
        Display all info on the app like:
        - Number of cube
        - Actual dimension
        :param new_info: all the info we need
        :return:
        """
        self.info_app_nb_cubes['text'] = "Il y a actuellement {} cubes".format(new_info)

    def find_cube_with_id(self, canv, cube_id):
        """
        This function create a dictionnary that contain information about a cube
        :param canv: the canvas (in canvas_app)
        :param cube_id: id of the cube
        :return: the dictionnary
        """
        item_cube = canv.find_withtag(cube_id)
        dict_cube = {}

        for i in range(len(item_cube)):
            color = canv.itemcget(item_cube[i], "fill")
            tags = canv.itemcget(item_cube[i], 'tags').split(" ")
            canv.itemconfig(item_cube[i], outline="red")
            dict_cube[item_cube[i]] = [color, tags[4], tags[5]]
        return dict_cube

    def display_info(self, tags_item, canvas):
        """
        Display all the cube about a clicked cube
        :param tags_item: all the tag of the cube
        :param canvas: the canvas (in canvas_app)
        :return:
        """
        cube = []
        try:
            # Look for the id of the cube
            cube = [s for s in tags_item if "cpt_" in s]
        except IndexError:
            # This error will not be raised because we are sure that the 'cpt_' pattern is in the tags_item
            print("ERROR: {UserAction/display_info}: no such id")

        dico_cube = self.find_cube_with_id(canvas, cube[0])

        self.id_cube_label['text'] = "Id du cube: {}".format(cube[0][4:])
        self.id_cube_label.pack()

        # We delete the canvas to refresh the informations
        self.info_canv.delete("all")

        i = 0
        j = 0
        list_pos = ['first', 'second', 'third']
        # Creation of 3 little square to display the color of the faces
        for key, value in dico_cube.items():
            self.info_canv.create_text(100, 20 + i, text="Couleur de la face {}".format(value[1]))
            self.info_canv.create_rectangle(100, 30 + i, 120, 50 + i, fill=value[0],
                                            tags=("color", value[0], list_pos[j]))
            j += 1
            i += 50

        self.update_cube_btn['text'] = "Modifier le cube"
        self.update_cube_btn['command'] = lambda cube=dico_cube: self.update_cube(cube)

        self.update_cube_btn.pack()

    def clean_info(self):
        self.info_canv.delete("all")
        self.update_cube_btn.pack_forget()
        self.id_cube_label.pack_forget()

    def update_cube(self, dict_cube):
        """
        Function to update a cube: change his color, his dimensions
        :param dict_cube:
        :return:
        """
        UserAction.top_level = tk.Toplevel(self.master, width=300, height=400)
        UserAction.top_level.geometry("300x300+{}+250".format(self.screen_width // 3))
        UserAction.top_level.title("Modification d'un cube")
        UserAction.top_level.grab_set()

    def preprocess_creation(self, event=None, **kwargs):
        """
        This function will start the process to create a cube
        """

        # First we store every informations with the **kwargs arguments
        x = float(kwargs['x'])
        y = float(kwargs['y'])
        canvas = kwargs['canvas']
        container = kwargs['container']
        dict_case_grid = kwargs['dict_case']
        # If True, the instant param is used to create a cube by default
        # Else, it will create a custom cube
        instant = kwargs['instant']

        try:
            # If the kind key is present, we have to call another function to draw columns or lines
            kind = kwargs['kind']
        except KeyError:
            kind = ""

        # We find the closest id widget on the canvas. This could be a cube or a case of the grid
        id_case_closest = canvas.find_closest(x, y)
        tags = canvas.gettags(id_case_closest)

        # We store the barycenter of the cube/case closest to x, y
        bary_x_closest = int(tags[2])
        bary_y_closest = int(tags[3])

        try:
            face = tags[4]
        except IndexError:
            face = "grid"

        dim = dict_case_grid[1][2]  # We are sure that key 1 exist

        try:
            # This switch if will determine where the user clicked
            if face == "haut":
                bary_y_closest -= dim // 2

            elif face == "droite":
                bary_x_closest += dim // 2
                bary_y_closest += 13

            elif face == "gauche":
                bary_x_closest -= dim // 2
                bary_y_closest += 13

            else:
                bary_y_closest -= dim // 2

        except UnboundLocalError:
            pass

        if kind == "":
            if instant:
                self.create_instant_cube(
                    [
                        dim,
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
        else:
            self.create_figure(
                [bary_x_closest, bary_y_closest],
                canvas,
                container,
                dict_case_grid,
                id_case_closest[0],
                kind,
            )

    def custom_cube(self, coords, canv, container, dict_case, id_case):
        """
        This is the second part of the cube's creation process
        :param coords: The coords we need to place the cube
        :param canv: The canvas
        :param container: The container
        :param dict_case: The dictionnary of all case
        :param id_case: The id of the case
        :return:
        """
        UserAction.top_level = tk.Toplevel(self.master, width=300, height=400)
        UserAction.top_level.geometry("300x300+{}+250".format(self.screen_width // 3))
        UserAction.top_level.title("Ajout d'un cube")
        UserAction.top_level.grab_set()

        frame = tk.Frame(UserAction.top_level, width=300, height=150)
        frame.pack()
        color_canvas = tk.Canvas(UserAction.top_level, width=300, height=200)
        color_canvas.pack()
        button_frame = tk.Frame(UserAction.top_level, width=300, height=50)
        button_frame.pack()

        size = tk.IntVar()
        tk.Label(frame, text="Taille du cube: ").pack()

        entry_size = tk.Entry(frame, textvariable=size)
        entry_size.pack()

        # Creation of 3 little square to pick a color
        color_canvas.create_text(150, 20, text="Couleur de la face gauche")
        color_left = color_canvas.create_rectangle(140, 30, 160, 50, fill=self.color1,
                                                   tags=("color", "first", self.color1))

        color_canvas.create_text(150, 70, text="Couleur de la face du dessus")
        color_top = color_canvas.create_rectangle(140, 80, 160, 100, fill=self.color2,
                                                  tags=("color", "second", self.color2))

        color_canvas.create_text(150, 120, text="Couleur de la face droite")
        color_right = color_canvas.create_rectangle(140, 130, 160, 150, fill=self.color3,
                                                    tags=("color", "third", self.color3))

        color_canvas.tag_bind("color", '<Button-1>', lambda event, canvas=color_canvas:
        self.choose_color(event, canvas))

        create_button = tk.Button(button_frame, text="Créer le cube",
                                  command=lambda: self.create(
                                      size=entry_size,
                                      colors=[color_left, color_top, color_right],
                                      coords=coords,
                                      main_canvas=canv,
                                      top_canvas=color_canvas,
                                      container=container,
                                      dict_case=dict_case,
                                      id_case=id_case,
                                  ),
                                  )
        create_button.pack()

    def choose_color(self, event, canvas):
        """
        This the function used to change the color of a face
        :param event: The user click on the Button-1
        :param canvas: The canvas of the top level window
        :return: Update the square on the top level
        """
        id_item = canvas.find_withtag('current')

        pos = ""
        color = colorchooser.askcolor(title="Choisir une couleur")
        # Switch with the clicked cube pos
        if id_item[0] == 2:
            pos = "first"
        elif id_item[0] == 4:
            pos = "second"
        elif id_item[0] == 6:
            pos = "third"

        canvas.itemconfig(id_item, fill=color[1])
        canvas.itemconfig(id_item, tags=('color', pos, color[1]))

    def create(self, **kwargs):
        """
        This is the last part of the custom cube creation
        :param kwargs: The dictionnary of the custom cube: size, coords, color, canvas....
        :return: Create the cube
        """
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

        # We store the color for the cube
        list_color = []
        for i in range(len(colors)):
            list_color.append(top_canvas.itemcget(colors[i], "tags").split(" ")[2])

        cube = Cube(coords, size, list_color, main_canvas)

        # We update the container list_cube in adding the previous created cube
        container.set_liste_cube(cube)

        # We update the update the information of the app
        self.display_info_app(len(container.get_liste_cube()))

        try:
            # We update the dictionnary of the grid.
            # Now, the container knows that this box have at least 1 cube
            dict_case_grid[id_case][1] = 1
        except KeyError:
            # Ce produit lorsqu'on empile des cubes.
            pass

        UserAction.top_level.destroy()

    def create_instant_cube(self, list_param):
        """
        This is the last functions to create a default cube
        :param list_param: all the informations for the cube. Instead pass them one by one, a list is better
        :return:
        """
        size = list_param[0]
        colors = list_param[1]
        coords = list_param[2]
        main_canvas = list_param[3]
        container = list_param[4]
        dict_box_grid = list_param[5]
        id_case = list_param[6]

        cube = Cube(coords, size, colors, main_canvas)

        try:
            # We update the dictionnary of the grid.
            # Now, the container knows that this box have at least 1 cube
            dict_box_grid[id_case][1] = 1
        except KeyError:
            # This error occurs when we stack cubes, but I don't know why so don't remove it
            pass

        # We update the container list_cube in adding the previous created cube
        container.set_liste_cube(cube)

        # We update the update the information of the app
        self.display_info_app(len(container.get_liste_cube()))

    def create_figure(self, coords, canv, container, dict_case, id_case, kind):
        """
        Second part for the creation of special figure: columns or line
        :param coords: the start coords
        :param canv: the main canvas
        :param container: the container of cube
        :param dict_case: the dictionnary of all box of the grid
        :param id_case: the id of the case whe clicked on
        :param kind: columns or lines
        :return:
        """
        UserAction.top_level = tk.Toplevel(self.master, width=300, height=400)
        UserAction.top_level.geometry("300x400+{}+250".format(self.screen_width // 3))
        UserAction.top_level.title("Ajout d'une figure spéciale")
        UserAction.top_level.grab_set()

        frame = tk.Frame(UserAction.top_level, width=300, height=150)
        frame.pack()
        color_canvas = tk.Canvas(UserAction.top_level, width=300, height=200)
        color_canvas.pack()
        button_frame = tk.Frame(UserAction.top_level, width=300, height=50)
        button_frame.pack()

        size = tk.IntVar()
        number_of_cube = tk.IntVar()

        tk.Label(frame, text="Taille des cube: ").pack()
        entry_size = tk.Entry(frame, textvariable=size)
        entry_size.pack()

        tk.Label(frame, text="Nombre de cubes: ").pack()
        entry_number = tk.Entry(frame, textvariable=number_of_cube)
        entry_number.pack()

        var_dir = ""

        # If it's a line, we ask another option: the direction of the line. Right or Left
        # We ask the user with a Radio Button checkbox
        if kind == "lines":
            tk.Label(frame, text="Direction des cubes: ").pack()
            var_dir = tk.StringVar()
            var_dir.set(0)
            radio_1 = tk.Radiobutton(frame, variable=var_dir, text='Gauche', value='left')
            radio_1.pack(side="left", expand=1)
            radio_2 = tk.Radiobutton(frame, variable=var_dir, text='Droite', value='right')
            radio_2.pack(side='left', expand=1)

        # Creation of 3 little square to pick a color
        color_canvas.create_text(150, 20, text="Couleur des faces gauche")
        color_left = color_canvas.create_rectangle(140, 30, 160, 50, fill=self.color1,
                                                   tags=("color", "first", self.color1))

        color_canvas.create_text(150, 70, text="Couleur des faces du dessus")
        color_top = color_canvas.create_rectangle(140, 80, 160, 100, fill=self.color2,
                                                  tags=("color", "second", self.color2))

        color_canvas.create_text(150, 120, text="Couleur des faces droite")
        color_right = color_canvas.create_rectangle(140, 130, 160, 150, fill=self.color3,
                                                    tags=("color", "third", self.color3))

        color_canvas.tag_bind("color", '<Button-1>', lambda event, canvas=color_canvas:
        self.choose_color(event, canvas))

        create_col_btn = tk.Button(button_frame,
                                   text="Créer la figure",
                                   command=lambda: self.create_figure_final(
                                       size=entry_size,
                                       number=entry_number,
                                       colors=[color_left, color_top, color_right],
                                       coords=coords,
                                       main_canvas=canv,
                                       top_canvas=color_canvas,
                                       container=container,
                                       dict_case=dict_case,
                                       id_case=id_case,
                                       kind=kind,
                                       direction=var_dir,
                                   ),
                                   )
        create_col_btn.pack()

    def create_figure_final(self, **kwargs):
        """
        Last part of the creation for figure
        :param kwargs: arguments passed by the callback of the button
        :return:
        """
        try:
            size = int(kwargs['size'].get())
            number = int(kwargs['number'].get())
        except AttributeError:
            pass

        colors = kwargs['colors']
        coords = kwargs['coords']
        main_canvas = kwargs['main_canvas']
        top_canvas = kwargs['top_canvas']
        container = kwargs['container']
        dict_case_grid = kwargs['dict_case']
        id_case = kwargs['id_case']
        kind = kwargs['kind']

        try:
            # We test if the direction key exist. If Yes, it's a line. Else it's a column
            direction = kwargs['direction'].get()
        except AttributeError:
            pass

        list_color = []
        for i in range(len(colors)):
            list_color.append(top_canvas.itemcget(colors[i], "tags").split(" ")[2])

        cube_factory = CubeFactory(coords, size, list_color, main_canvas, container, number)

        if kind == "columns":
            cube_factory.factory_col()

        elif kind == "lines":
            cube_factory.factory_lines(direction)

        self.display_info_app(len(container.get_liste_cube()))

        try:
            # We update the dictionnary of the grid.
            # Now, the container knows that this box have at least 1 cube
            dict_case_grid[id_case][1] = 1
        except KeyError:
            # Ce produit lorsqu'on empile des cubes.
            pass

        UserAction.top_level.destroy()
