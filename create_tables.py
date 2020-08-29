import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(query)

# query = 'INSERT INTO users VALUES (?,?,?)'
query = 'SELECT * FROM users'
# cursor.execute(query,(None,'qqqq','1111'))
result = cursor.execute(query)
print(result.fetchone())

connection.commit()

query = 'CREATE TABLE IF NOT EXISTS items (name text, price real)'
cursor.execute(query)
connection.commit()

connection.close()