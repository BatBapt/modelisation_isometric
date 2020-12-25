"""
self.new_frame = tk.Frame(self.master_frame, width=200, height=self.master_frame.winfo_height()//3+200, bg="red")
self.new_frame.pack(side=tk.TOP)

self.create_cube_btn = tk.Button(self.new_frame, text="Créer nouveau cube", width=40, command=self.new_cube)
self.create_cube_btn.pack(side=tk.TOP, pady=(25, 0))

self.create_col_btn = tk.Button(self.new_frame, text="Crée colonne de cube", width=40, command=self.new_col)
self.create_col_btn.pack(side=tk.TOP, pady=(25, 0))

self.update_frame = tk.Frame(self.master_frame, width=200, height=400, bg="blue")
self.update_frame.pack(side=tk.BOTTOM)

self.coord_1 = tk.DoubleVar()
self.coord_2 = tk.DoubleVar()
self.taille = tk.DoubleVar(value=50)

self.top_lvl = None

self.coord_x_lab = None
self.coord_y_lab = None
self.size_lab = None
self.entry_x = None
self.entry_y = None
self.entry_size = None

self.default_taille = 50

def new_cube(self):
    self.top_lvl = tk.Toplevel()
    self.top_lvl.grab_set()
    self.top_lvl.geometry("600x400+{}+{}".format(self.screen_width//3, self.screen_heigt//3))

    main_frame = tk.Frame(self.top_lvl, width=300, height=400)
    main_frame.pack(side=tk.TOP)

    preview_canv = tk.Canvas(main_frame, width=300, height=200)
    preview_canv.pack(side=tk.TOP)

    preview_canv.create_text(150, 10, text="Apercu du cube")
    functions.draw_cube([150, 75], self.default_taille, preview_canv)

    info_frame = tk.Frame(main_frame, width=300, heigh=200)
    info_frame.pack(side=tk.TOP)

    self.coord_x_lab = tk.Label(info_frame, text="Coordonnées X")
    self.coord_x_lab.pack()

    self.entry_x = tk.Entry(info_frame, textvariable=self.coord_1)
    self.entry_x.pack()

    self.coord_y_lab = tk.Label(info_frame, text="Coordonnées Y")
    self.coord_y_lab.pack()
    self.entry_y = tk.Entry(info_frame, textvariable=self.coord_2)
    self.entry_y.pack()

    self.size_lab = tk.Label(info_frame, text="Taille du cube")
    self.size_lab.pack()
    self.entry_size = tk.Entry(info_frame, textvariable=self.taille)
    self.entry_size.pack()

    self.validate_btn = tk.Button(info_frame, text="Créer ce cube",
        command=lambda: self.validate_cube(
            x=self.entry_x,
            y=self.entry_y,
            s=self.entry_size),
    )
    self.validate_btn.pack()

def validate_cube(self, event=None, **kwargs):
    is_ok = False
    try:
        x_coords = float(kwargs['x'].get())
        y_coords = float(kwargs['y'].get())

        is_ok = True
    except ValueError:
        messagebox.showerror('Erreur', 'Des nombres sont demandés')

    if is_ok:
        size = kwargs['s'].get()
        if len(size) == 0:
            size = 50
        else:
            size = float(size)

        functions.draw_cube([x_coords, y_coords], size, self.master.canvas.canvas)

        self.entry_x.delete(0, 'end')
        self.entry_y.delete(0, 'end')
        self.top_lvl.destroy()

def new_col(self):
    self.top_lvl = tk.Toplevel()
    self.top_lvl.grab_set()
    self.top_lvl.geometry("600x500+{}+{}".format(self.screen_width//3, self.screen_heigt//3))

    main_frame = tk.Frame(self.top_lvl, width=300, height=500)
    main_frame.pack(side=tk.TOP)

    preview_canv = tk.Canvas(main_frame, width=300, height=300)
    preview_canv.pack(side=tk.TOP)

    preview_canv.create_text(150, 10, text="Apercu du cube")
    functions.draw_cube([150, 200], self.default_taille, preview_canv)
    functions.draw_cube([150, 150], self.default_taille, preview_canv)


    info_frame = tk.Frame(main_frame, width=300, heigh=200)
    info_frame.pack(side=tk.TOP)

    self.coord_x_lab = tk.Label(info_frame, text="Coordonnées X")
    self.coord_x_lab.pack()

    self.entry_x = tk.Entry(info_frame, textvariable=self.coord_1)
    self.entry_x.pack()

    self.coord_y_lab = tk.Label(info_frame, text="Coordonnées Y")
    self.coord_y_lab.pack()
    self.entry_y = tk.Entry(info_frame, textvariable=self.coord_2)
    self.entry_y.pack()

    self.size_lab = tk.Label(info_frame, text="Taille du cube")
    self.size_lab.pack()
    self.entry_size = tk.Entry(info_frame, textvariable=self.taille)
    self.entry_size.pack()

    number = tk.IntVar
    number_lab = tk.Label(info_frame, text="Nombre de cube")
    number_lab.pack()
    entry_number = tk.Entry(info_frame, textvariable=number)
    entry_number.pack()

    self.validate_btn = tk.Button(info_frame, text="Créer ce cube",
        command=lambda: self.validate_col(
            x=self.entry_x,
            y=self.entry_y,
            s=self.entry_size,
            n=entry_number),
    )
    self.validate_btn.pack()

def validate_col(self, event=None, **kwargs):
    is_ok = False
    try:
        x_coords = float(kwargs['x'].get())
        y_coords = float(kwargs['y'].get())
        number = int(kwargs['n'].get())

        is_ok = True

    except ValueError:
        messagebox.showerror('Erreur', 'Des nombres sont demandés')

    if is_ok:
        size = kwargs['s'].get()
        if len(size) == 0:
            size = 50
        else:
            size = float(size)

        functions.draw_cube_col([x_coords, y_coords], number, size, self.master.canvas.canvas)

        self.entry_x.delete(0, 'end')
        self.entry_y.delete(0, 'end')
        self.top_lvl.destroy()


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
"""
