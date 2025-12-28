import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM expenses").fetchall()

for row in rows:
    print(row)

conn.close()
