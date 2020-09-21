import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import safe_str_cmp
from models.user_model import UserModel


class UserRegister(Resource):
    # create a parser
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='cannot be blank')
    parser.add_argument('password', type=str, required=True, help='cannot be blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
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


