from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

def get_db_connection():
    conn = sqlite3.connect(r'databas/database.db')
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
        fname = request.form['fname']
        if not fname:
            flash("чего-го не хватает")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (fname) VALUES (?)',
                         (fname))
            conn.commit()
            conn.execute("SELECT * FROM users;")
            conn.fetchall()
            conn.close()
            return redirect(url_for('index'))

    return render_template('reg.html'),


if __name__ == '__main__':
    app.run()