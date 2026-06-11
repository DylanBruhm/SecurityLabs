import sqlite3
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

p1 = hashlib.sha256("shores".encode()).hexdigest()
p2 = hashlib.sha256("captian".encode()).hexdigest()
p3 = hashlib.sha256("gold".encode()).hexdigest()
p4 = hashlib.sha256("ship".encode()).hexdigest()
p5 = hashlib.sha256("treasue".encode()).hexdigest()
p6 = hashlib.sha256("deck".encode()).hexdigest()

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
""", [("pirate", p1, "admin"), ("sailor", p2, "basic"), ("davyjones", p3, "basic"), ("blackbeard", p4, "basic"), ("jack", p5, "basic"), ("crew", p6, "basic")])

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
""", [("seaship", 10000, "pirate"), ("seabrig", 1000, "sailor"), ("blackpearl", 1000, "davyjones"), ("flyingdutchman", 1000, "blackbeard"), ("oceantrader", 1000, "jack"), ("ironkraken", 1000, "crew")])

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    receiver TEXT NOT NULL,
    subject TEXT,
    body TEXT NOT NULL,
    sent_at NOT NULL                    
)
""")

cursor.execute("""
INSERT INTO messages (sender, receiver, subject, body, sent_at)
VALUES (?, ?, ?, ?, ?)
""", ("Admin", "pirate", "gold", "we gunna be rich dont tell the others", "2026-06-02 22:00"))

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT , 
    severity TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,        
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL       
)

""")

cursor.execute("""
INSERT INTO alerts (severity, title, description, status)
VALUES (?, ?, ?, ?)
""", ("high", "Brute", "multiple login atempts", "open"))

cursor.execute("SELECT * FROM ships")

rows = cursor.fetchall()
print(rows)
conn.close()


print("Table created")