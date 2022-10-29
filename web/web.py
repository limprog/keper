from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
import os


def get_db_connection():
    conn = sqlite3.connect(os.path.join('database/database.db'))
    conn.row_factory = sqlite3.Row
    return conn
def reg_write():
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reg',  methods=('GET', 'POST'))
def reg():
    test = 0
    if request.method == 'POST':
        fname = str(request.form['fname'])
        sname = str(request.form['sname'])
        cod = str(request.form['cod'])
        email = str(request.form['email'])

        if not fname or not sname or not cod or not email:
            test = 1
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (fname, sname, cod, email) VALUES (?, ?, ?, ?)',
                         (fname, sname, cod, email,))
            conn.commit()
            conn.execute("SELECT * FROM users;")
            conn.close()

    return render_template('reg.html', test=test)

@app.route('/auth',  methods=('GET', 'POST'))
def auth():
    test = 0
    authenticity = 2
    if request.method == 'POST':
        email = str(request.form['emaila'])
        cod = str(request.form['cod'])
        if not email or not cod:
            test = 1
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users where email = (?)",(email,))
            row = cur.fetchone()
            print(row['cod'])
            rcod = row['cod']
            if cod == rcod:
                authenticity = 1
    return render_template('auth.html', authenticity=authenticity)
if __name__ == '__main__':
    app.run()