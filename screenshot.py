import pyautogui
import datetime

class Screenshoot():
    def __init__(self):
        pyautogui.screenshot(f'{datetime.datetime.now()}.png')