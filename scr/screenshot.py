import pyautogui
from processing import *
from datetime import datetime
import os
import socket
import time
import requests
test_url = "http://httpbin.org/post"

class Screenshoot():
    def __init__(self, der):
        os.makedirs("data", exist_ok=True)
        os.makedirs(os.path.join('data', der), exist_ok=True)

    def screen(self,der):
        os.makedirs("data", exist_ok=True)
        os.makedirs(os.path.join('data', der), exist_ok=True)
        now = datetime.now()
        now_time = now.strftime("%H_%M_%S")
        screen = pyautogui.screenshot(os.path.join('data', der, f'{now_time}.png'))
        resize(image=screen)