from datetime import timedelta
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)
from werkzeug.security import safe_str_cmp
from user import User


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        request_data = Login.parser.parse_args()
        username = request_data.get('username')
        password = request_data.get('password')
        user = User.find_by_username(username)
        if user:
            if safe_str_cmp(password, user.password):
                # create expiration time for access and refresh tokens
                access_token_expiry_time = timedelta(minutes=15)
                refresh_token_expiry_time = timedelta(hours=1)

                # username or user.id anything can be used here as identity
                # eg. access_token = create_access_token(identity=User.id)
                access_token = create_access_token(identity=username, fresh=True, expires_delta=access_token_expiry_time)
                # similary create a refresh token
                refresh_token = create_refresh_token(identity=username, expires_delta=refresh_token_expiry_time)
                return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        return {'message': 'Invalid credentials!'}, 401

    @jwt_refresh_token_required
    def get(self):
        access_token_expiry_time = timedelta(minutes=15)
        current_user = get_jwt_identity()
        # setting fresh=False since we donot verify uname/pwd credentials here
        # can limit the access of non-fresh access tokens by @fresh_jwt_required
        access_token = create_access_token(identity=current_user, fresh=False, expires_delta=access_token_expiry_time)
        return {'access token': access_token}
