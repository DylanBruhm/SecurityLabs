import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
INSERT INTO users (username, password)
VALUES (?, ?)
""", ("pirate", "shores"))

conn.commit()


cursor.execute("SELECT * FROM users")

rows = cursor.fetchall()
print(rows)

conn.close()


print("Table created")