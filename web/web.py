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
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reg',  methods=('GET', 'POST'))
def reg():
    if request.method == 'POST':
        #flash("ij")

        fname = str(request.form['fname'])
        sname = str(request.form['sname'])
        cod = str(request.form['cod'])
        email = str(request.form['email'])

        if not fname or not sname or not cod or not email:
            flash("ddddddddddd")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (fname, sname, cod, email) VALUES (?, ?, ?, ?)',
                         (fname, sname, cod, email,))
            conn.commit()
            conn.execute("SELECT * FROM users;")
            conn.close()

    return render_template('reg.html')

@app.route('/auth',  methods=('GET', 'POST'))
def auth():
    if request.method == 'POST':
        email = str(request.form['emaila'])
        cod = str(request.form['cod'])
        if not email or not cod:
            pass
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users where email = (?)",(email,))
            row = cur.fetchone()
            rcod = row['cod']
            if cod == rcod:
                pass
    return render_template('auth.html')
if __name__ == '__main__':
    app.run()