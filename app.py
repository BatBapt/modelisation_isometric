import tkinter as tk

from canvas_app import CanvasApp


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.screen_width = self.winfo_screenwidth()
        self.screen_heigt = self.winfo_screenheight()

        self.geometry("{}x{}+300+100".format(self.screen_width//2+400, self.screen_heigt//2+300))

        menu_frame = tk.Frame(self.master, width=self.screen_width//2+200, height=25)
        menu_frame.pack(side=tk.TOP, anchor=tk.NW)

        self.file = tk.Menubutton(menu_frame, text="Fichier", width=20, borderwidth=2)
        self.file.pack(side=tk.LEFT, fill=tk.X)

        self.obj = tk.Menubutton(menu_frame, text="Objet", width=20, borderwidth=2)
        self.obj.pack(side=tk.LEFT, fill=tk.X)

        self.file_menu = tk.Menu(self.file, tearoff=0)
        self.obj_menu = tk.Menu(self.obj, tearoff=0)

        self.canvas = CanvasApp(self)

        self.menu_widget()


    def menu_widget(self):
        self.file_menu.add_command(label="Ouvrir")
        self.file_menu.add_command(label="Enregistrer")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.destroy)

        self.file.configure(menu=self.file_menu)

        self.obj_menu.add_command(label="Maison", command=self.canvas.draw_house)

        self.obj_menu.add_separator()
        self.obj_menu.add_command(label="Grille", command=self.canvas.draw_support)
        self.obj_menu.add_command(label="Effacer", command=self.canvas.delete)

        self.obj.configure(menu=self.obj_menu)




if __name__ == "__main__":
    app = App()
    app.mainloop()
    exit(0)
