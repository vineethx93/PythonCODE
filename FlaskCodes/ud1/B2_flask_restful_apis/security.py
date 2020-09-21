
from werkzeug.security import safe_str_cmp
from user import User

# IMP: TRY PASSWORD HASHING INSTEAD
# https://geekflare.com/securing-flask-api-with-jwt/

# an in-memory table of registered users
# should use db for real applications
users = [
   User(1, 'bob', 'asdf')  # creating an object of User class from user.py module for EACH USER
]

# a username mapping table(in-memory, should use db)
# using set comprehension.. produces a dictionary similar to below
username_mapping = {u.username: u for u in users}
# username_mapping = {'bob': {
#     'id': 1,
#     'username': 'bob',
#     'password': 'asdf'
# }}

# a userid mapping table(in-memory, should use db)
userid_mapping = {u.id: u for u in users}
# using set comprehension.. produces a dictionary similar to below
# userid_mapping = {1: {
#     'id': 1,
#     'username': 'bob',
#     'password': 'asdf'
# }}


# checks in incoming username and pwd from /auth and if they are valid then return user to JWT
def authenticate(username, password):
    print('in auth')
    user = username_mapping.get(username, None)
    # if user is not None and also if password match then return the user
    # this is a safer version of string comparison instead of "user.password == password"
    if user and safe_str_cmp(user.password, password):
        print('if user and str_comp satisfied')
        return user


# payload is the content of the JWT token
# if the Token is valid then return the user
def identity(payload):
    print('in identity')
    # extract the userid from the paylod
    userid = payload['identity']
    print('userid:', userid)
    return userid_mapping.get(userid, None)
