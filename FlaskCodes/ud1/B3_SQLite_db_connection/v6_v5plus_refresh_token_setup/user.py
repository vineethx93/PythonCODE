import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import safe_str_cmp


class User:
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


class UserRegister(Resource):
    # create a parser
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='cannot be blank')
    parser.add_argument('password', type=str, required=True, help='cannot be blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        user = User.find_by_username(data['username'])
        if user:
            return {'message': 'username already exists. please try another..'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # id is passed as NULL coz its auto incrementing field
        query = "INSERT INTO USERS VALUES(NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {'message': 'user created successfully'}, 201


