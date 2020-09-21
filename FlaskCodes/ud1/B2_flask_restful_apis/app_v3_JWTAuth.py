from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# following modules are created to use with this module
# 1. security.py
# 2. user.py

# JWT -> Json Web Token
# 1.User send a UNAME + PWD to Server
# 2.Server send back a JWT
# 3.User can now send JWT with any request to the server to show that he is previously authenticated
# ie.. (they are logged in now)
# IMP: TRY PASSWORD HASHING INSTEAD
# https://geekflare.com/securing-flask-api-with-jwt/

app = Flask(__name__)
# inorder to encrypt and decrypt this secret key is required
# move this key from here to a proper location in production
app.secret_key = 'vineeth'
api = Api(app)

# JWT creates an endpoint '/auth' and from the client side they have to call this endpoint
# with username and pwd to obtain Token
# After the Token should be included in the Authorization header of the request for a successful API call
jwt = JWT(app, authenticate, identity)


items = []


class Item(Resource):
    # adding @jwt_required() decorator to enforce the Token validation for below /item/<string:item_name>/ GET method
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # item trying to add is already present in the items list
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "item '{0}' already exists".format(name)}, 400

        # else if item is not in the list then try to insert the item
        request_data = request.get_json()
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
        # data = request.get_json()
        # instead of blindly getting the json data(as above)
        # below method makes sure that the required fields are present in the json payload
        # if not present it will reject the request with 400 bad request error
        # also it will not consider the unregistered arguments
        # so parser.parse_args() will contain only the args added using add_argument()
        # if we try to access an unregistered argument like data['colour'] then we will get a KeyError
        # even if it is sent in the json payload
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help='This field cannot be blank')
        data = parser.parse_args()

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


if __name__ == '__main__':
    app.run(debug=True)
