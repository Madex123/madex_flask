from flask import Flask
from flask_restful import Api  # reqparse to be used to retrieve only important part of the request
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList

from security.security import authenticate, identity

# jsonify is not required as flask_restful already does it for us
# to run the debugger export FLASK_ENV=development


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)  # to add resources to the app, as API works with the resources

jwt = JWT(app, authenticate, identity)  #JWT implements a new endpoint called /auth, it returns a JWT token

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items/')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)


