import pyautogui
from processing import *
import os
from constants import *


class Screenshoot():
    def __init__(self):
        os.makedirs("Screenshoot", exist_ok=True)
        os.makedirs(os.path.join('Screenshoot', today), exist_ok=True)

    def screen(self):
        os.makedirs("Screenshoot", exist_ok=True)
        os.makedirs(os.path.join('Screenshoot', today), exist_ok=True)
        screen = pyautogui.screenshot(os.path.join('Screenshoot', today, f'{now_time}.png'))
        resize(image=screen)