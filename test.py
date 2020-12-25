import tkinter as tk


def cR():
    if w.find_withtag('one'):
            w.tag_remove("")
    else:
        w.create_line(10, 40, 60, 40, fill='yellow', tags='one')


def delete(tag):
    w.delete(w.find_withtag(tag))


root = tk.Tk()
w = tk.Canvas(root, width=200, height=100)
w.pack()
w.create_line(10, 40, 60, 40, fill='red', tags='one')
b = tk.Button(root, text="red", command=cR)
b.pack()
root.mainloop()

