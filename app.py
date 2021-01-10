#!/usr/bin/env python3

import tkinter as tk

from canvas_app import CanvasApp
from user_action import UserAction


class App(tk.Tk):
    """
    This is the main file. This file will call all other file
    """
    start_top_level = None

    def __init__(self):
        tk.Tk.__init__(self)

        self.screen_width = self.winfo_screenwidth()
        self.screen_heigt = self.winfo_screenheight()

        self.geometry("{}x{}".format(self.screen_width, self.screen_heigt))

        self.canvas = None
        self.user_action = None

        menu_frame = tk.Frame(self.master, width=self.screen_width // 2 + 100, height=25)
        menu_frame.pack(side=tk.TOP, anchor=tk.NW)

        self.file = tk.Menubutton(menu_frame, text="Fichier", width=20, borderwidth=2)
        self.file.pack(side=tk.LEFT, fill=tk.X)

        self.obj = tk.Menubutton(menu_frame, text="Action", width=20, borderwidth=2)
        self.obj.pack(side=tk.LEFT, fill=tk.X)

        self.help = tk.Menubutton(menu_frame, text="Aide", width=20, borderwidth=2)
        self.help.pack(side=tk.LEFT, fill=tk.X)

        self.file_menu = tk.Menu(self.file, tearoff=0)
        self.obj_menu = tk.Menu(self.obj, tearoff=0)
        self.help_menu = tk.Menu(self.help, tearoff=0)
        self.start()

    def start(self):
        App.start_top_level = tk.Toplevel(self)
        App.start_top_level.transient(self)
        App.start_top_level.geometry("350x150+{}+350".format(self.screen_width // 3 + 100))
        App.start_top_level.title("Démarrage de l'application")
        App.start_top_level.grab_set()
        # self.wait_window(top_level)

        frame = tk.Frame(App.start_top_level, width=200, height=200)
        frame.pack()

        cube_size = tk.IntVar()
        tk.Label(frame, text="Choisissez une taille par défaut des cubes: ").pack()

        entry_cube_size = tk.Entry(frame, textvariable=cube_size)
        entry_cube_size.pack()

        grid_size = tk.IntVar()
        tk.Label(frame, text="Choisissez le nombre de case de la grille (NxN): ").pack()

        entry_grid_size = tk.Entry(frame, textvariable=grid_size)
        entry_grid_size.pack()

        validate_button = tk.Button(frame, text="Valider",
                                    command=lambda: self.validate(
                                        entry_one=entry_cube_size,
                                        entry_two=entry_grid_size,
                                    ), width=20, borderwidth=2)

        validate_button.pack()

        quit_button = tk.Button(frame, text="Quitter", command=self.destroy, width=10, borderwidth=2)
        quit_button.pack()

    def validate(self, **kwargs):
        default_cube_size = kwargs['entry_one'].get()
        grid_size = kwargs['entry_two'].get()
        try:
            default_cube_size = int(default_cube_size)
            grid_size = int(grid_size)
        except ValueError as e:
            print(e)

        if default_cube_size > 0 and grid_size > 0:
            App.start_top_level.destroy()

            self.canvas = CanvasApp(default_cube_size, grid_size, self)
            self.user_action = UserAction(self.canvas)

            self.menu_widget()

    def menu_widget(self):
        """
        This function will create the menu
        :return:
        """
        self.file_menu.add_command(label="Nouveau (Ctrl + N")
        self.file_menu.add_command(label="Ouvrir (Ctrl + O)")
        self.file_menu.add_command(label="Enregistrer (Ctrl + S)", command=self.canvas.save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter (Ctrl + Q)", command=self.destroy)

        self.file.configure(menu=self.file_menu)

        self.obj_menu.add_command(label="Effacer (Ctrl + D)", command=self.canvas.delete)

        self.obj.configure(menu=self.obj_menu)

        self.help_menu.add_command(label="Aide (F1)", command=self.user_action.call_help)
        self.help_menu.add_command(label="A propos (F2)", command=self.user_action.about)

        self.help.configure(menu=self.help_menu)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    exit(0)
