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

        self.color1 = '#8c8c8c'
        self.color2 = '#cccccc'
        self.color3 = '#383838'

    def draw_cube_in_svg(self, point, dim):
        point = [int(point[0]), int(point[1])]
        A = [point[0], point[1]]
        B = [A[0], A[1] + dim]
        C = [B[0] + dim, B[1] - (dim // 2)]
        D = [A[0] + dim, A[1] - (dim // 2)]
        E = [A[0], A[1] - dim]
        F = [A[0] - dim, A[1] - (dim // 2)]
        G = [B[0] - dim, B[1] - (dim // 2)]

        return [[F, A, B, G], [A, D, E, F], [A, B, C, D]]

    def python_to_svg(self, points, color, file):
        i = 0
        for faces in points:
            for coords in faces:
                string = '\t<polygon points="{},{} {},{}, {},{} {},{}" fill="{}"/>'.format(
                    coords[0][0]-300,
                    coords[0][1],
                    coords[1][0]-300,
                    coords[1][1],
                    coords[2][0]-300,
                    coords[2][1],
                    coords[3][0]-300,
                    coords[3][1],
                    color[i],
                )
                file.write(string + "\n")
                i += 1
            file.write("\n")

    def save_final(self, cubes_dict, cube_size, grid_dim):
        with open("tmp.svg", "w") as svg:
            svg.write('<svg xmlns="http://www.w3.org/2000/svg" height="800" width="800">\n')
            face_list = []
            for k,v in cubes_dict.items():
                coords = k.split("_")[1]
                number_of_cubes = int(v[1]) + 1
                if number_of_cubes > 1:
                    k = 0
                    for j in range(number_of_cubes):
                        cube = draw_cube_in_svg([int(v[0][0]), int(v[0][1])-k], 50)
                        k += 50
                        face_list.append(cube)
                else:
                    cube = self.draw_cube_in_svg(v[0], 50)
                    face_list.append(cube)

            list_color = []
            for j in range(len(v[2])):
                list_color.append(v[2][j])

            self.python_to_svg(face_list, list_color, svg)
            svg.write("</svg>")


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
        UserAction.top_level.transient(self.master)
        UserAction.top_level.grab_set()

    def destroy_cube(self, event, **kwargs):
        """
        This function destroy the cube the user clicked on
        """
        canvas = kwargs['canvas']
        container = kwargs['container']
        list_cube = kwargs['list_cube']

        id_case_closest = canvas.find_closest(event.x, event.y)

        for i in range(len(list_cube)):
            try:
                if id_case_closest[0] in list_cube[i]:
                    cube = list_cube.pop(i)
                    canvas.delete(cube[0])
                    canvas.delete(cube[1])
                    canvas.delete(cube[2])
                    self.display_info_app(len(list_cube))
            except IndexError:
                pass

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
        grid = kwargs['grid']
        # If True, the instant param is used to create a cube by default
        # Else, it will create a custom cube
        instant = kwargs['instant']

        try:
            # If the kind key is present, we have to call another function to draw columns or lines
            kind = kwargs['kind']
        except KeyError:
            kind = ""

        dim = dict_case_grid['coords_0:0'][1]  # We are sure that key 'coords_0:0' exist

        # This is a 'homemade' method to place a cube in function of his size
        adjust_dim = int((dim / 2) // 2)
        if str(adjust_dim)[-1] != '0':
            adjust_dim += 1


        # We find the closest id widget on the canvas. This could be a cube or a case of the grid
        id_case_closest = canvas.find_closest(x, y)
        tags = canvas.gettags(id_case_closest)

        id_case = tags[1]
        if tags[0] == "cube":
            height_minus_hauteur = int(tags[3]) + int(tags[6]) * dim + dim
            res = grid.look_in((str(tags[2]), str(height_minus_hauteur)))
            id_case = res[1]

        # We store the barycenter of the cube/case closest to x, y
        bary_x_closest = int(tags[2])
        bary_y_closest = int(tags[3])


        try:
            face = tags[4]
        except IndexError:
            face = "grid"

        try:

            # This switch if will determine where the user clicked

            if face == "haut":
                bary_y_closest -= dim // 2

            elif face == "droite":
                bary_x_closest += dim // 2
                bary_y_closest += adjust_dim

            elif face == "gauche":
                bary_x_closest -= dim // 2
                bary_y_closest += adjust_dim

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
                        id_case,
                    ]
                )
            else:
                self.custom_cube(
                    [bary_x_closest, bary_y_closest],
                    canvas,
                    container,
                    dict_case_grid,
                    id_case,
                )
        else:
            self.create_figure(
                [bary_x_closest, bary_y_closest],
                canvas,
                container,
                dict_case_grid,
                id_case,
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
        dict_box_grid = kwargs['dict_case']
        id_case = kwargs['id_case']

        # We store the color for the cube
        list_color = []
        for i in range(len(colors)):
            list_color.append(top_canvas.itemcget(colors[i], "tags").split(" ")[2])

        hauteur = dict_box_grid[id_case][0]

        cube = Cube(coords, size, list_color, hauteur, main_canvas)

        dict_box_grid[id_case][0] += 1

        # We update the container list_cube in adding the previous created cube
        container.liste_cube = cube

        # We update the update the information of the app
        self.display_info_app(len(container.liste_cube))

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

        hauteur = dict_box_grid[id_case][0]

        cube = Cube(coords, size, colors, hauteur, id_case, main_canvas)

        dict_box_grid[id_case][0] += 1

        # We update the container list_cube in adding the previous created cube
        container.liste_cube = cube

        # We update the update the information of the app
        self.display_info_app(len(container.liste_cube))

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

        self.display_info_app(len(container.liste_cube))

        try:
            # We update the dictionnary of the grid.
            # Now, the container knows that this box have at least 1 cube
            dict_case_grid[id_case][1] = 1
        except KeyError:
            # Ce produit lorsqu'on empile des cubes.
            pass

        UserAction.top_level.destroy()
