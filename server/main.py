'''
Этот фаил для того что-бы бот мог работать
'''

from flask import Flask, render_template, session, request,  redirect, url_for, flash
import sqlite3
import os
from PIL import Image
from telegbot.main import *
import asyncio
import torch
import torchvision
import torchvision.transforms as transforms
from mmcls.apis import inference_model, init_model, show_result_pyplot


def get_db_connection():
    conn = sqlite3.connect(os.path.join('../database/database.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


loop = asyncio.get_event_loop()
app = Flask(__name__)


@app.route('/test', methods=['POST'])
def get_test():
    data = request
    print(data)
    return ("ok")


@app.route('/scr', methods=['POST'])
def recieve_screenshot():
    print(request.files, request.form)
    data = request.form
    file = request.files['image']
    img = Image.open(file.stream)
    img.save(f'{data["id"]}_{data["time"]}.png')
    file = f'{data["id"]}_{data["time"]}.png'
    loop.run_until_complete(scrin(file, tgid=90808437, id=data['id']))
    return ('', 204)

@app.route('/reg', methods=['POST'])
def reg():
    data = request.form
    print(data)
    conn, cur = get_db_connection()
    conn.execute('INSERT INTO users(name, nickname, position, timetable, tgid, cod) VALUES (?, ?, ?, ?, ?, ?)',
                 (data['name'], data['nickname'], data["position"], data['timetable'], data['tgid'], data["cod"],))
    conn.commit()
    conn.close()
    return ('', 204)




if __name__ == '__main__':
    app.run(debug=False)
