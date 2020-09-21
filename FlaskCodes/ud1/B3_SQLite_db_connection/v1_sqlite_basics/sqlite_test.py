import sqlite3

connection = sqlite3.connect('data.db')
# our db will be a single file

cursor = connection.cursor()
# cursor is responsible for executing the queries and storing the results

create_table = 'CREATE TABLE USERS(id int, username string, password string)'

cursor.execute(create_table)
print('USERS table created')

# inserting single user
user = (1, 'vineeth', 'asdf')
insert_query = 'INSERT INTO USERS VALUES(?, ?, ?)'
cursor.execute(insert_query, user)
connection.commit()
print('user inserted to USERS table')

# inserting multiple users
users = [
    (2, 'bob', 'abc'),
    (3, 'alice', 'def')
]
cursor.executemany(insert_query, users)
connection.commit()
print('multiple users inserted to USERS table')

select_query = 'SELECT * FROM USERS'
result = cursor.execute(select_query)
for row in result:
    print(row)

connection.close()
