
from werkzeug.security import safe_str_cmp
from user import User


# checks in incoming username and pwd from /auth and if they are valid then return user to JWT
def authenticate(username, password):
    print('in auth')
    user = User.find_by_username(username)
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
    return User.find_by_id(userid)
