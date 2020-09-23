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

        user = UserModel(data['username'], data['password'])
        # here it wont update coz in the above return we are handling situation where user already exists
        # so here it will create new user only
        user.upsert()

        return {'message': 'user created successfully'}, 201


