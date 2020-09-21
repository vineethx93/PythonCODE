import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# use "INTEGER PRIMARY KEY" to create auto incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS USERS(ID INTEGER PRIMARY KEY, USERNAME STRING, PASSWORD STRING)"
cursor.execute(create_table)
connection.commit()


# use "INTEGER PRIMARY KEY" to create auto incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS ITEMS(NAME STRING, PRICE DOUBLE)"
cursor.execute(create_table)
connection.commit()

insert_query = 'INSERT INTO ITEMS(NAME, PRICE) VALUES(?, ?)'
cursor.execute(insert_query, ('test_item', 9.99))
connection.commit()

connection.close()
print('USERS table created')
print('ITEMS table created')
