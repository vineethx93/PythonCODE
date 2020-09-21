import sqlite3
from db import db


# To use a model class with SQLAlchemy ORM it should extend db.Model
# This will tell the SQLAlchemy that UserModel is a thing that we are going to save/retrieve using database
# This will create a mapping between the database and this class/obj
class UserModel(db.Model):

    # tell the table and column details that need to use for UserModel class
    # IMP: column names that are being used as table columns should match the properties in the __init__
    # but there is no need that all the properties of the class should be used as a column
    # table name for UserModel
    __tablename__ = 'users'
    # Columns used/associated for UserModel
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))  # its good to limit the size
    password = db.Column(db.String(80))  # its good to limit the size

    def __init__(self, _id, username, password):
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

