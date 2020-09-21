from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import safe_str_cmp
from user import User, UserRegister
from item import Item, Items

# following modules are created to use with this module
# 1. user.py

app = Flask(__name__)

# inorder to encrypt and decrypt this secret key is required
# move this key from here to a proper location in production
app.config['JWT_SECRET_KEY'] = 'vineeth'

# if this is not set then proper errors wont be propagated back to api caller
# not required if debug=True
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
jwt = JWTManager(app)


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
                # username or user.id anything can be used here as identity
                # access_token = create_access_token(identity=username)
                access_token = create_access_token(identity=user.id)
                return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials!'}, 401


api.add_resource(Item, '/item/<string:name>/')
api.add_resource(Items, '/items/')
api.add_resource(Login, '/login')

# this will call the user.py->UserRegister class
# dont forget to import the class
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(debug=True)
