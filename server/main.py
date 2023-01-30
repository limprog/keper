'''
Этот фаил для того что-бы бот мог работать
'''

from flask import Flask, render_template, session, request,  redirect, url_for, flash
import sqlite3
import os


def get_db_connection():
    conn = sqlite3.connect(os.path.join('database/database.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def get_test():
    data = request
    print(data)
    return ("ok")


@app.route('/recieve_screenshot', methods=['POST'])
def recieve_screenshot():
    data = request
    print(data)
    return ('', 204)

