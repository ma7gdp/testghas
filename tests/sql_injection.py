import sqlite3

user_id = input("Enter user id: ")
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE users (id TEXT, name TEXT)")
cur.execute("INSERT INTO users VALUES ('1', 'Alice')")
cur.execute("SELECT name FROM users WHERE id = %s" % user_id)
print(cur.fetchall())
