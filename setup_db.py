import sqlite3
import hashlib

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
p1 = hashlib.sha256("shores".encode()).hexdigest()
p2 = hashlib.sha256("captian".encode()).hexdigest()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.executemany("""
INSERT INTO users (username, password)
VALUES (?, ?)
""", [("pirate", p1), ("sailor", p2)])

conn.commit()


cursor.execute("SELECT * FROM users")

rows = cursor.fetchall()
print(rows)

conn.close()


print("Table created")