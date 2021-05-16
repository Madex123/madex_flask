from werkzeug.security import safe_str_cmp
from models.user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):  # safe string compare with all unicode, ASCII
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)