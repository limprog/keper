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
from reader import *
from writer import *


model = torch.load(os.path.join('../net/best_scr_v3_shufflenet_v2.pth'), map_location={'cuda:0': 'cpu'})


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
    os.makedirs('img', exist_ok=True)
    img = Image.open(file.stream)
    img.save(f'img/{data["id"]}_{data["time"]}.png')
    file = f'{data["id"]}_{data["time"]}.png'
    result = inference_model(model, os.path.join("../server/img", file))
    writer(data['id'], result)
    loop.run_until_complete(scrin(file, tgid=data['tgid'], id=data['id'],result=result))

    return ('', 204)

@app.route('/reg', methods=['POST'])
def reg():
    data = request.form
    print(data)
    conn, cur = get_db_connection()
    cur.execute('INSERT INTO users(name, nickname, position, timetable, tgid, cod) VALUES (?, ?, ?, ?, ?, ?)',
                 (data['name'], data['nickname'], data["position"], data['timetable'], data['tgid'], data["cod"],))
    id = cur.lastrowid
    print(id)
    conn.commit()
    conn.close()
    return ("ggtgyfku", 204)


@app.route('/auth', methods=['POST'])
def auth():
    data = request.form
    print(data)
    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM users where nickname  = ?", (data['nickname'],))
    row = cur.fetchall()
    print(row)
    if row == []:
        return ("", 418)
    if row[0][1] == data['nickname']:
        return ({"name":row[0][2], "id":row[0][0]}, 201)
    else:
        return ('', 401)


@app.route("/del",  methods=['POST'])
def delite():
    data = request.form
    print(data)
    conn, cur = get_db_connection()
    conn.execute("""DELETE from  users where nickname = ?""", (data['nickname'], ))
    conn.commit()
    conn.close()
    return ("", 201)


@app.route("/chan/name", methods=['POST'])
def chan_name():
    data = request.form
    print(data['newname'])
    conn, cur = get_db_connection()
    cur.execute("""Update users set name = ? where nickname = ?""", (data['newname'], data['nickname'], ))
    conn.commit()
    conn.close()
    return ("", 201)


@app.route("/chan/nickname",  methods=['POST'])
def chan_nick():
    data = request.form
    print(data['newnickname'])
    conn, cur = get_db_connection()
    cur.execute("""Update users set nickname = ? where nickname = ?""", (data['newnickname'], data['nickname'],))
    conn.commit()
    conn.close()
    return ("", 201)


@app.route("/chan/cod",  methods=['POST'])
def chan_cod():
    data = request.form
    print(data['newcod'])
    conn, cur = get_db_connection()
    cur.execute("""Update users set cod = ? where nickname = ?""", (data['newcod'], data['nickname'],))
    conn.commit()
    conn.close()
    return ("", 201)


@app.route("/chan/time",  methods=['POST'])
def chan_time():
    data = request.form
    print(data['newtime'])
    conn, cur = get_db_connection()
    cur.execute("""Update users set timetable = ? where nickname = ?""", (data['newtime'], data['nickname'],))
    conn.commit()
    conn.close()
    return ("", 201)


@app.route("/room/reg",methods=['POST'])
def room_reg():
    data = request.form
    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM users where nickname  = ?", (data['nickname'],))
    row = cur.fetchall()
    us_id = row[0][0]
    cur.execute("SELECT * FROM occupation where name  = ?", (data['op_name'],))
    row = cur.fetchall()
    op_id = row[0][0]
    conn.execute('INSERT INTO room(number, occupation_id, user_id) VALUES (?, ?, ?)',
                 (data['name'], op_id,us_id, ))
    conn.commit()
    conn.close()
    return ('', 201)


@app.route('/op/reg',methods=['POST'])
def op_reg():
    data = request.form
    conn, cur = get_db_connection()
    conn.execute('INSERT INTO occupation(name, city, cod) VALUES (?, ?, ?)',
                (data['op_name'], data['op_city'], data['op_cod'],))
    conn.commit()
    conn.close()
    return ('', 201)


@app.route('/op/auth', methods=['POST'])
def op_auth():
    data = request.form
    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM occupation where name  = ?", (data['op_name'],))
    row = cur.fetchall()
    if row[0][-1] == data['op_cod']:
        return ('',201)
    else:
        return ('',418)
    conn.commit()
    conn.close()
    return ('', 204)


@app.route('/comp/reg', methods=['POST'])
def comp_reg():
    data = request.form
    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM users where nickname  = ?", (data['nickname'],))
    row = cur.fetchall()
    us_id = row[0][0]
    timetabel = row[0][4]
    tgid = row[0][6]
    cur.execute("SELECT * FROM occupation where name  = ?", (data['op'],))
    row = cur.fetchall()
    op_id = row[0][0]
    cur.execute('INSERT INTO computer(room_number, room_occupation_id, user_id) VALUES (?, ?, ?)',
                 (data['socet'], op_id, us_id,))
    id = cur.lastrowid
    print(row)
    conn.commit()
    conn.close()
    ans = {'id': id, 'timetabel':timetabel, 'tgid':tgid}
    return (ans, 201)


@app.route('/stat/today', methods=['POST'])
def stat_today():
    data = request.form
    today = str(date.today())
    loogs = os.listdir(f"loogs/{today}")
    for i in loogs:
        loog = i.split(".")[0::2]
        print(loog[0])
        print(data['stat_id'])
        if loog[0] == data['stat_id']:
            score = read(data['stat_id'], today)
            s =[]
            s.append(score)
            return (s, 202)

        else:
            return ("",404)

    return ("",201)


@app.route('/stat/class', methods=['POST'])
def stat_class():
    data = request.form()
    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM users where nickname  = ?", (data['nickname'],))
    row = cur.fetchall()
    us_id = row[0][0]
    cur.execute("SELECT * FROM computer where room_number, user_id  = ?", (data["room_nb"], us_id))
    row = cur.fetchall()
    #today = str(date.today())
    today = "2023-02-09"
    id = []
    scores = {}
    for i in row:
        id.append(i[0])
    for j in id:
        score = read_class(j, today)
        scores[j] = score
    print(scores)



if __name__ == '__main__':
    app.run(debug=True)
