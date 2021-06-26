import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt

from blacklist import BLACKLIST

_parser = reqparse.RequestParser()
_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )
_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be blank.")


class UserRegister(Resource):

    def post(self):
        data = _parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.delete_from_db()


class UserLogin(Resource):

    @classmethod
    def post(cls):
        #this is what security/authenticate function used to do
        #get data from parser
        data = _parser.parse_args()
        #find user in the db
        user = UserModel.find_by_username(data['username'])
        #check password
        if user and safe_str_cmp(user.password, data['password']):
            # create access token - this is what security/identity function used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(user.id)
            # return them
            return {'access_token': access_token,
                    'refresh_token': refresh_token}, 200

        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self): #blacklist the current access token
        jti = get_jwt()['jti']  # jti is the unique ID for JWT
        BLACKLIST.add(jti)
        return {'message': 'bye bye'}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt()
        new_token = create_access_token(current_user, fresh=False)
        return {'access_token': new_token}, 200








