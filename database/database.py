import sqlite3
import os

df = sqlite3.connect(os.path.join("database.db"))
data = df.cursor()
data.execute("""CREATE TABLE IF NOT EXISTS occupation(
   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   name TEXT,
   city TEXT);
""")

data.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   nickname TEXT,
   name TEXT,
   position TEXT, 
   timetable TEXT,
   occupation_id INTEGER NOT NULL,
   tgid TETX,
   FOREIGN KEY (occupation_id) REFERENCES occupation(id));
""")


df.commit()
data = df.cursor()
data.execute("""CREATE TABLE IF NOT EXISTS room(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    number INTEGER,
    occupation_id INTEGER,
    FOREIGN KEY (occupation_id) REFERENCES occupation(id));
""")


data.execute("""CREATE TABLE IF NOT EXISTS computer(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    room_number INTEGER,
    room_occupation_id INTEGER,
    FOREIGN KEY (room_number) REFERENCES room(number),
    FOREIGN KEY (room_occupation_id) REFERENCES room(occupation_id));
""")
data.execute("SELECT * FROM users;")
print(data.fetchall(), 'users')
data.execute("SELECT * FROM occupation;")
print(data.fetchall(), 'occupation')
data.execute("SELECT * FROM room;")
print(data.fetchall(), 'room')
data.execute("SELECT * FROM computer;")
print(data.fetchall(), 'computer')
print(os.path.join('database.py'))
df.commit()
df.close()

