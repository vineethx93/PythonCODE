import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# use "INTEGER PRIMARY KEY" to create auto incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS USERS(ID INTEGER PRIMARY KEY, USERNAME STRING, PASSWORD STRING)"
cursor.execute(create_table)
connection.commit()
connection.close()
print('USERS table created')
