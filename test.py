import tkinter as tk

def popup(event):
    global popup_menu
    popup_menu = tk.Menu(root)
    popup_menu.add_command(label="Test", command=test)
    try:
        popup_menu.tk_popup(event.x_root, event.y_root, 0)
    finally:
        popup_menu.grab_release()

def test():
    print("Salut")


def test2(event):
    print("Hey")
    popup_menu.destroy()
    # tk.Wm.wm_deiconify(popup_menu)
    # tk.Wm.wm_withdraw(popup_menu)


root = tk.Tk()

canv = tk.Canvas(root, width=200, height=200)
canv.pack()

canv.bind('<Button-3>', popup)
canv.bind('<Button-1>', test2)

root.mainloop()
