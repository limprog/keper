import pyautogui
from processing import *
import os
from constants import *
from datetime import datetime
from datetime import date


class Screenshoot():
    def __init__(self, der):
        os.makedirs("Screenshoot", exist_ok=True)
        os.makedirs(os.path.join('Screenshoot', der), exist_ok=True)

    def screen(self,der):
        os.makedirs("Screenshoot", exist_ok=True)
        os.makedirs(os.path.join('Screenshoot', der), exist_ok=True)
        now = datetime.now()
        now_time = now.strftime("%H_%M_%S")
        screen = pyautogui.screenshot(os.path.join('Screenshoot', der, f'{now_time}.png'))
        resize(image=screen)