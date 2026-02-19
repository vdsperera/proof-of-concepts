import sqlite3

connection = sqlite3.connect('rawsql.db')
curser = connection.cursor()

curser.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
curser.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
connection.commit()

curser.execute("SELECT * FROM users")
rows = curser.fetchall()
print(rows)

connection.close()