from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister
from resources.auth import Login
from resources.item import Item, Items

# following modules are created to use with this module
# 1. user.py

app = Flask(__name__)

# inorder to encrypt and decrypt this secret key is required
# move this key from here to a proper location in production
app.config['JWT_SECRET_KEY'] = 'vineeth'

# can set the access token expiry time using below technique also
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=1800)
# can do lot more like this check:
# https://flask-jwt-extended.readthedocs.io/en/stable/options/

# if this is not set then proper errors wont be propagated back to api caller
# not required if debug=True
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
jwt = JWTManager(app)


api.add_resource(Item, '/item/<string:name>/')
api.add_resource(Items, '/items/')
# this will call the user.py->UserRegister class
# dont forget to import the class
api.add_resource(UserRegister, '/register')
# this will do the user login
api.add_resource(Login, '/login')


if __name__ == '__main__':
    app.run(debug=True)
