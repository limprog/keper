import tkinter as tk
import os


root = tk.Tk()


class Marcer:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, height=1080, width=1920)
        img = tk.PhotoImage(file='Screenshoot/data/1')
        self.lab = tk.Label(master, width=20,bg='black', fg='white')
        self.but1 = tk.Button(master,text="0 - плохо", width=10)
        self.but2 = tk.Button(master,text="1 - норм", width=10)
        self.but3 = tk.Button(master,text='2 - хорошо', width=10)
        self.lab.pack()
        self.canvas.create_image(0, 0, anchor='nw',image=img)
        self.but1.pack()
        self.but2.pack()
        self.but3.pack()
Marcer(root)
root.mainloop()