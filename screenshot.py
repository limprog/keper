import pyautogui
from processing import *
import os
from constants import *


class Screenshoot():
    def __init__(self, der):
        os.makedirs("Screenshoot", exist_ok=True)
        os.makedirs(os.path.join('Screenshoot', der), exist_ok=True)

    def screen(self,der):
        os.makedirs("Screenshoot", exist_ok=True)
        os.makedirs(os.path.join('Screenshoot', der), exist_ok=True)
        screen = pyautogui.screenshot(os.path.join('Screenshoot', der, f'{now_time}.png'))
        resize(image=screen)