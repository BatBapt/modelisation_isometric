#!/usr/bin/env python3

import tkinter as tk

from canvas_app import CanvasApp


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

        menu_frame = tk.Frame(self.master, width=self.screen_width//2+200, height=25)
        menu_frame.pack(side=tk.TOP, anchor=tk.NW)

        self.file = tk.Menubutton(menu_frame, text="Fichier", width=20, borderwidth=2)
        self.file.pack(side=tk.LEFT, fill=tk.X)

        self.obj = tk.Menubutton(menu_frame, text="Objet", width=20, borderwidth=2)
        self.obj.pack(side=tk.LEFT, fill=tk.X)

        self.file_menu = tk.Menu(self.file, tearoff=0)
        self.obj_menu = tk.Menu(self.obj, tearoff=0)

        self.start()

    def start(self):
        App.start_top_level = tk.Toplevel(self)
        App.start_top_level.transient(self)
        App.start_top_level.geometry("300x100+{}+250".format(self.screen_width // 3))
        App.start_top_level.title("Démarrage de l'application")
        App.start_top_level.grab_set()
        # self.wait_window(top_level)

        frame = tk.Frame(App.start_top_level, width=200, height=200)
        frame.pack()

        cube_size = tk.IntVar()
        tk.Label(frame, text="Choisissez une taille par défaut des cubes: ").pack()

        entry_cube_size = tk.Entry(frame, textvariable=cube_size)
        entry_cube_size.pack()

        validate_button = tk.Button(frame, text="Valider",
                                    command=lambda: self.validate(
                                    entry=entry_cube_size
                                    ))

        validate_button.pack()

    def validate(self, **kwargs):
        size = kwargs['entry'].get()
        try:
            size = int(size)
        except ValueError as e:
            print(e)

        print(type(size), size)
        if size > 0:
            App.start_top_level.destroy()

            self.canvas = CanvasApp(size, self)

    def menu_widget(self):
        """
        This function will create the menu
        :return:
        """
        self.file_menu.add_command(label="Ouvrir")
        self.file_menu.add_command(label="Enregistrer")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.destroy)

        self.file.configure(menu=self.file_menu)

        #self.obj_menu.add_command(label="Maison", command=self.canvas.draw_house)

        self.obj_menu.add_separator()
        self.obj_menu.add_command(label="Grille", command=self.canvas.draw_support)
        self.obj_menu.add_command(label="Effacer", command=self.canvas.delete)

        self.obj.configure(menu=self.obj_menu)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    exit(0)
