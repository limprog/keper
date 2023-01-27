import pyautogui
from processing import *
from datetime import datetime
import os
import socket
import time
def server(now, pcname):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
    client.connect(('localhost', 4344))  # 127.0.0.1
    client.send("1".encode())
    time.sleep(1)
    file = open(os.path.join('../Screenshoot/data/HI.png'), 'rb')
    image_data = file.read(2048)

    while image_data:
        client.send(image_data)
        image_data = file.read(2048)

    file.close()
    client.close()
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