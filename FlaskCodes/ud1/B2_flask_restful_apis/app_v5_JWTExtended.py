from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from security import authenticate, identity
from werkzeug.security import safe_str_cmp
from user import User

# following modules are created to use with this module
# 1. user.py

# IMP: TRY PASSWORD HASHING INSTEAD
# https://geekflare.com/securing-flask-api-with-jwt/

app = Flask(__name__)
# inorder to encrypt and decrypt this secret key is required
# move this key from here to a proper location in production
app.config['JWT_SECRET_KEY'] = 'vineeth'
api = Api(app)
jwt = JWTManager(app)


items = []


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    users = [
        User(1, 'bob', 'asdf')  # creating an object of User class from user.py module for EACH USER
    ]
    username_mapping = {u.username: u for u in users}
    userid_mapping = {u.id: u for u in users}

    def post(self):
        request_data = Login.parser.parse_args()
        username = request_data.get('username')
        password = request_data.get('password')
        if username in Login.username_mapping.keys():
            user = Login.username_mapping.get(username)
            if safe_str_cmp(password, user.password):
                # username or user.id anything can be used here as identity
                access_token = create_access_token(identity=username)
                return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials!'}, 401


class Item(Resource):

    # adding class variable parser to use with any methods
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be blank')

    # adding @jwt_required() decorator to enforce the Token validation for below /item/<string:item_name>/ GET method
    @jwt_required
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # item trying to add is already present in the items list
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "item '{0}' already exists".format(name)}, 400

        # access class variable by ClassName.variable_name
        request_data = Item.parser.parse_args()

        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        for item in items:
            if item['name'] == name:
                items.remove(item)
                return {'message': '{0} removed from items'.format(name)}, 200
        return {'message': 'item with name {0} NOT FOUND!'.format(name)}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        for item in items:
            if item['name'] == name:
                item['price'] = data['price']
                return {'message': 'Item Updated'}, 200
        items.append({'name': name, 'price': data['price']})
        return {'message': 'New Item Created'}, 201


class Items(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>/')
api.add_resource(Items, '/items/')
api.add_resource(Login, '/login')


if __name__ == '__main__':
    app.run(debug=True)
