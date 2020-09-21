import sqlite3


class UserModel:
    # _id is used here since "id: is a keyword.. better to keep _id rather than any other name
    def __init__(self, _id, username, password):
        # DONOT change this "id" in "self.id" to any other name [JWT thing]
        self.id = _id
        self.username = username
        self.password = password

    # not mandatory to define as classmethod
    # if defining as classmethod use cls instead of self and cls for accessing
    # else use self and ClassName for accessing
    @classmethod
    def find_by_username(cls, username):  # cls instead of self since its a classmethod
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM USERS WHERE USERNAME=?'
        result = cursor.execute(query, (username,))  # a tuple containing single item is used
        row = result.fetchone()
        if row:
            # user = User(row[0], row[1], row[2])
            # user = cls(row[0], row[1], row[2])  # cls instead of 'User' coz classmethod # same as above
            # user = User(*row)  # same as above
            user = cls(*row)  # same as above
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):  # cls instead of self since its a classmethod
        user = ''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM USERS WHERE ID=?'
        result = cursor.execute(query, (_id,))  # a tuple containing single item is used
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])  # cls instead of 'User' coz classmethod
            user = cls(*row)  # same as above
        else:
            user = None

        connection.close()
        return user

