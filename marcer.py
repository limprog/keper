import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import os


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.a = 0
        # создаем рабочую область
        self.frame = tk.Frame(self.root)
        self.frame.grid()
        self.image = Image.open(r"./Screenshoot/data/HI.png")
        width, height = self.image.size
        new_width = 1000  # ширина
        new_height = int(new_width * height / width)
        self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

        # вставляем кнопку
        self.but = tk.Button(self.frame, text="сменить", width=50, command=self.my_event_handler)
        self.but.grid(row=2, column=1)
        self.lab = tk.Label(self.frame, width=50, bg='black', fg='white', text='привет')
        self.lab.grid(row=1, column=1)
        self.but1 = tk.Button(self.frame, text="0 - плохо", width=50, command=self.bad_z)
        self.but2 = tk.Button(self.frame, text="1 - норм", width=50, command=self.normal_z)
        self.but3 = tk.Button(self.frame, text='2 - хорошо', width=50, command=self.good_z)
        self.but4 = tk.Button(self.frame, text='сохранить', width=50, command=self.sev )
        self.but1.grid(row=3, column=1)
        self.but2.grid(row=4, column=1)
        self.but3.grid(row=5, column=1)
        self.but4.grid(row=6, column=1)
        e = {"files":['HI.png'], "bad": [0], "normal":[0],"good":[0]}
        self.data = pd.DataFrame(e)
        # Добавим изображение
        self.canvas = tk.Canvas(self.root, height=1080, width=1920)
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(row=1, column=1)
        self.root.mainloop()
        self.f = ""



    def my_event_handler(self):
        fils = os.listdir('./Screenshoot/data')
        self.f = '{0}.png'.format(self.a + 1)
        self.image = Image.open(f"./Screenshoot/data/{self.f}")
        self.a += 1
        width, height = self.image.size
        new_width = 1000  # ширина
        new_height = int(new_width * height / width)
        self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.lab['text'] = self.f
        self.photo = ImageTk.PhotoImage(self.image)
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(row=2, column=1)

    def bad_z(self):
        print(self.f)
        dataf = pd.DataFrame({"files":[self.f], "bad": [1], "normal":[0],"good":[0]})
        # dataf = pd.Series([self.f, 1, 0,0])
        self.data = pd.concat([self.data, dataf], axis=0)
        print(self.data.head())
    def normal_z(self):
        dataf = pd.DataFrame({"files":[self.f], "bad": [0], "normal":[1],"good":[0]})
        # dataf = pd.Series([self.f, 1, 0,0])
        self.data = pd.concat([self.data, dataf], axis=0)
        print(self.data.head())
    def good_z(self):
        dataf = pd.DataFrame({"files":[self.f], "bad": [0], "normal":[0],"good":[1]})
        # dataf = pd.Series([self.f, 1, 0,0])
        self.data = pd.concat([self.data, dataf], axis=0)
        print(self.data.head())

    def sev(self):
        self.data.to_csv("data")



app = App()