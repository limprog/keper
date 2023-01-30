import sqlite3
import os

df = sqlite3.connect(os.path.join("database.db"))
data = df.cursor()
data.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   fname TEXT,
   sname TEXT,
   cod TEXT, 
   email TEXT,
   tgid TETX);
""")
data.execute("""CREATE TABLE IF NOT EXISTS class(
   classid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   name TEXT,
   cod TEXT,
   grop TEXT,
   email TEXT,
   chairmanid INTEGER);
""")

df.commit()
data = df.cursor()
data.execute("""CREATE TABLE IF NOT EXISTS users_class(
    id INTEGER  PRIMARY KEY,
    userid INTEGER,
    classid INTEGER,
    FOREIGN KEY (userid) REFERENCES users(userid),
    FOREIGN KEY (classid) REFERENCES class(classid));
""")

data.execute("SELECT * FROM users;")
print(data.fetchall(), 'users')
data.execute("SELECT * FROM class")
print(data.fetchall(), 'class')

print(os.path.join('database.py'))
df.commit()
df.close()

