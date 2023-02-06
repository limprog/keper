import pyautogui
from processing import *
from datetime import datetime
import os
import socket
import time
import requests
import base64
import uuid
import  io
import pyautogui as pyautogui
from requests_toolbelt import MultipartEncoder
from date import *
from apscheduler.schedulers.blocking import BlockingScheduler
from txt_reader import *
tgid, timetabel, id, date_of_week, time1 = read()


sched = BlockingScheduler()
url = "http://127.0.0.1:5000"


class Screenshoot():
    def __init__(self, der=today):
        os.makedirs("data", exist_ok=True)
        os.makedirs(os.path.join('data', der), exist_ok=True)

    def screen(self,der=today):
        os.makedirs("data", exist_ok=True)
        os.makedirs(os.path.join('data', der), exist_ok=True)
        now = datetime.now()
        now_time = now.strftime("%H_%M_%S")
        screen = pyautogui.screenshot(os.path.join('data', der, f'{now_time}.png'))
        print(screen)
        resize(image=screen)
        departure(now_time, screen, der)


def departure(time, img, der):
    mem_file = io.BytesIO()
    img.save(mem_file, "PNG")
    mem_file.seek(0)
    files = {
        'image': (
            'img.png',
            mem_file,
            'image/png'
        )
    }
    data = {
        'id': '1',
        "time":time,
        "der":der,
    }
    r = requests.post(
        url+"/scr",
        data=data,
        files=files
    )


scrin = Screenshoot()


@sched.scheduled_job('cron', day_of_week=date_of_week, hour=time1[0:1], minute=time1[3:4], second='*/3')
def main():
    while True:
        print('gg')
        scrin.screen(today)
        time.sleep(random.randint(1, 2))
if __name__ == '__main__':
    main()