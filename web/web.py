from flask import Flask, render_template, session, request,  redirect, url_for, flash
import datetime
import sqlite3
import os


fnamea =0
def get_db_connection():
    conn = sqlite3.connect(os.path.join('database/database.db'))
    conn.row_factory = sqlite3.Row
    return conn
def reg_write():
    pass

# Устоновка значений
app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.permanent_session_lifetime = datetime.timedelta(days=365*2)



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
            cur = conn.cursor()
            conn.execute('INSERT INTO users (fname, sname, cod, email) VALUES (?, ?, ?, ?)',
                         (fname, sname, cod, email,))
            conn.commit()
            conn.execute("SELECT * FROM users;")
            cur.execute("SELECT * FROM users where email = (?)", (email,))
            row = cur.fetchone()
            userid = row['userid']
            conn.close()
            session['fname'] = fname
            session['userid'] = userid
            session['classname'] =[]
            test = 1


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
            print(cod)
            rcod = row['cod']
            fname = row['fname']
            userid = row['userid']
            session['classname'] = []
            if cod == rcod:
                authenticity = 1
                session['fname'] = fname
                session['userid'] = userid
                print(session.get('fname'))
            else:
                test = 1
                authenticity = 0
                print(authenticity)
    return render_template('auth.html', authenticity=authenticity, test=test)


@app.route('/head',   methods=('GET', 'POST'))
def head():
    classes = session.get('classname')
    return render_template('head.html', fname=session.get('fname'), classes=classes)

@app.route('/exit',  methods=('GET', 'POST'))
def exit():
    session.pop('fname', None)
    session.pop('userid', None)
    session.pop('classname', None)
    session.pop('class', None)
    session.pop("classid", None)
    print(session)
    return render_template('exit.html')

@app.route('/class/reg', methods=('GET', 'POST'))
def class_reg():
    test = 0
    if request.method == 'POST':
        name = str(request.form['name'])
        cod = str(request.form['cod'])
        email = str(request.form['email'])
        grop = str(request.form['grop'])
        if not name or not cod or not email or not grop:
            test = 1
        else:
            userid = int(session.get('userid'))
            print(int(userid))
            conn = get_db_connection()
            conn.execute('INSERT INTO class(name, cod,grop, email, chairmanid) VALUES (?, ?, ?, ?, ?)',
                         (name, grop, cod, email, userid ,))
            conn.commit()
            cur = conn.cursor()
            cur.execute("SELECT * FROM class;")
            row = cur.fetchone()
            session['classname'].append(row['name'])
            conn.close()
    return render_template("class_reg.html")


@app.route('/class/auth',  methods=('GET', 'POST'))
def class_auth():
    classname = str(request.form['classname'])
    cod = str(request.form['cod'])
    if not classname or not cod:
        test = 1
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM class where name = (?)", (classname,))
        row = cur.fetchone()
        rcod = row['cod']
        if rcod == cod:
            session['classname'].append(classname)
    return render_template('class_auth.html')




if __name__ == '__main__':
    app.run(debug=False)