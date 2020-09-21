from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import safe_str_cmp
from user import User, UserRegister, Login
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


api.add_resource(Item, '/item/<string:name>/')
api.add_resource(Items, '/items/')
api.add_resource(Login, '/login')

# this will call the user.py->UserRegister class
# dont forget to import the class
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(debug=False)
