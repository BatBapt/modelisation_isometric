import tkinter as tk


class MenuApp(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)

        self.screen_width = self.winfo_screenwidth()
        self.screen_heigt = self.winfo_screenheight()

        menu_frame = tk.Frame(self.master, width=self.screen_width, height=25)
        menu_frame.pack(side=tk.TOP, anchor=tk.NW)

        self.menu = tk.Menubutton(menu_frame, text="Fichier", width=20, borderwidth=2)
        self.menu.pack(side=tk.LEFT, fill=tk.X)

        self.file_menu = tk.Menu(self.menu, tearoff=0)

        self.menu_widget()

    def menu_widget(self):
        self.file_menu.add_command(label="Ouvrir")
        self.file_menu.add_command(label="Enregistrer")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.master.destroy)

        self.menu.configure(menu=self.file_menu)




if __name__ == "__main__":
    root = tk.Tk()
    app = Menu(root)
    app.mainloop()
