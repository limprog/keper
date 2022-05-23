import pyautogui
import datetime
import time
from datetime import date
import os


class Screenshoot():
    def __init__(self):
        today = str(date.today())
        now = datetime.datetime.now()
        now1 = now.hour
        now2 = now.minute
        now3 = now.second
        os.makedirs("Screenshoot", exist_ok=True)
        os.makedirs(os.path.join('Screenshoot', today), exist_ok=True)
        pyautogui.screenshot(os.path.join('Screenshoot', today, f'{now1, now2,now3}.png'))
        # pyautogui.screenshot(f'{datetime.datetime.now()}.png')

