import sqlite3
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

p1 = hashlib.sha256("shores".encode()).hexdigest()
p2 = hashlib.sha256("captian".encode()).hexdigest()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cursor.executemany("""
INSERT INTO users (username, password, role)
VALUES (?, ?, ?)
""", [("pirate", p1, "admin"), ("sailor", p2, "basic")])

conn.commit()


cursor.execute("SELECT * FROM users")

rows = cursor.fetchall()
print(rows)

cursor.execute("""
CREATE TABLE IF NOT EXISTS ships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ship TEXT NOT NULL,
    gold INTEGER NOT NULL,
    owner TEXT NOT NULL
                                    
               
)
""")

cursor.executemany("""
INSERT INTO ships (ship, gold, owner)
VALUES (?, ?, ?)                 
""", [("seaship", 10000, "pirate"), ("seabrig", 1000, "sailor")])

conn.commit()

cursor.execute("SELECT * FROM ships")

rows = cursor.fetchall()
print(rows)
conn.close()


print("Table created")