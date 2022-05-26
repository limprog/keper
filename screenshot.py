import pyautogui
from datetime import datetime
import time
from datetime import date
import os


class Screenshoot():
    def __init__(self):
        today = str(date.today())
        os.makedirs("Screenshoot", exist_ok=True)
        os.makedirs(os.path.join('Screenshoot', today), exist_ok=True)

    def screen(self):
        today = str(date.today())
        now = datetime.now()
        now_time = now.strftime("%H_%M_%S")
        os.makedirs("Screenshoot", exist_ok=True)
        os.makedirs(os.path.join('Screenshoot', today), exist_ok=True)
        screen = pyautogui.screenshot(os.path.join('Screenshoot', today, f'{now_time}.png'))
        print(screen)
        # pyautogui.screenshot(f'{datetime.datetime.now()}.png')

