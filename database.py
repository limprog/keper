import sqlite3
import os


os.makedirs("databas", exist_ok=True)
df = sqlite3.connect(r'databas/keperdata.db')
data = df.cursor()
data.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   fname TEXT,
   sname TEXT,
   cod TEXT.
   gender TEXT,
   age INT);
""")
data.execute("""CREATE TABLE IF NOT EXISTS class(
   classid INT PRIMARY KEY,
   name TEXT,
   grop TEXT,
   chairmanid INT,
   FOREIGN KEY (chairmanid) REFERENCES chairman(chairman));
""")
df.commit()
data = df.cursor()
data.execute("""CREATE TABLE IF NOT EXISTS users_class(
    id INT  PRIMARY KEY,
    userid INT,
    classid INT,
    FOREIGN KEY (userid) REFERENCES users(userid),
    FOREIGN KEY (classid) REFERENCES class(classid));
""")
data.execute("""CREATE TABLE IF NOT EXISTS chairman(
    chairmanid INT PRIMARY KEY,
    userid INT,
    classid INT,
    FOREIGN KEY (userid) REFERENCES users(userid),
    FOREIGN KEY (classid) REFERENCES class(classid));
""")
df.commit()

