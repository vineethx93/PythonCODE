import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister
from resources.auth import Login
from resources.item import Item, Items
from resources.store import Store, StoreList


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

# tell the sqlalchemy where to find the database
# data.db should be in the same folder/package as app.py
# THIS WILL ALSO CREATE A data.db AT RUNTIME IF NOT ALREADY EXISTNG
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# can use url for other database systems here to connect to them instead

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ynhckrushmwuqx:85fb755d7a11b694606c7370c07efe00baaf9a3860aee4bbf59b4e52503cc010@ec2-54-75-229-28.eu-west-1.compute.amazonaws.com:5432/d9eonfs8s8hoi6'
# OR
# since the heroku will the url as an os environment variable when we add the addon of postgres
# we can simple use the environment variable as follows
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# if we want to run in local then give the sqlite also
# here the get method fails and return the default sqlite conn. string
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

# this will turnoff the flask-sqlalchemy modification tracker
# But NOT the sqlalchemy(main library) builtin modification tracker(which is better)
# modification tracking is the tracking of modifications to an object (but changes not being saved to the database)
# modification tracking will track any modifications to the sqlalchemy session
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
jwt = JWTManager(app)

# this will call the user.py->UserRegister class
api.add_resource(UserRegister, '/register')
# this will do the user login
api.add_resource(Login, '/login')
api.add_resource(Item, '/item/<string:name>/')
api.add_resource(Items, '/items/')
api.add_resource(Store, '/store/<string:name>/')
api.add_resource(StoreList, '/stores/')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
