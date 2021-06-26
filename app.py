import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from blacklist import BLACKLIST

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] #blacklist is enabled for both access and refresh token
app.secret_key = 'jose' #or app.config['JWT_SECRET_KEY']
api = Api(app)

jwt = JWTManager(app)  # not creating /auth endpoint


@jwt.additional_claims_loader
def add_claims_to_jwt(identity): #identity is user.id as defined in login resource
    if identity == 1: # first user created is an admin, but instead of hard-coding you can look up in DB
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return {'description': 'The token has expired', 'error': 'token_expired'}, 401


@jwt.invalid_token_loader
def invalid_token_callback():
    return {'description': 'Signature verification failed', 'error': 'token_invalid'}, 401


@jwt.unauthorized_loader
def unauthorized_token_callback():
    return {'description': 'Request does not contain an access token', 'error': 'authorization_required'}, 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return {'description': 'The token is not fresh', 'error': 'fresh_token_required'}, 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_headers, jwt_payload):
    return {'description': 'Token has been revoked', 'error': 'token_revoked'}, 401


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')


#this code here for testing on local only
@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)