import sqlite3
from flask_restful import Resource, reqparse
from masha_sandbox.flask_training.models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank!')
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank!')

    def post(self):
        request_data = self.parser.parse_args()
        if UserModel.find_by_username(request_data['username']):
            return {"message": "A user with this username already exists"}

        connection = sqlite3.connect('flask_training.db')
        cursor = connection.cursor()

        query = "insert into users values (NULL, ?, ?)"

        cursor.execute(query, (request_data['username'], request_data['password']))

        connection.commit()
        connection.close()

        return {"message": "User is created successfully!"}, 201




