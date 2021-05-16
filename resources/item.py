import sqlite3
from flask_restful import Resource, reqparse  # reqparse to be used to retrieve only important part of the request
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be blank!')

    @jwt_required()  # ensure JWT is received before we can make this call
    def get(self, name):  # name of the item
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400 # bad request

        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'])
        try:
            item.insert()
        except:
            return {'message': 'An error occurred inserting an item.'}, 500 #internal server error
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item = {'item': name}
            connection = sqlite3.connect('flask_training.db')
            cursor = connection.cursor()
            query = "delete from items where name = ?"
            cursor.execute(query, (item['item'],))

            connection.commit()
            connection.close()
            return {'message': 'Item deleted'}
        else:
            return {'message': 'Item not found'}, 404

    def put(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, request_data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occurred inserting an item.'}, 500  # internal server error
        else:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occurred updating an item.'}, 500  # internal server error
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('flask_training.db')
        cursor = connection.cursor()

        query = "select * from items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'item': row[0], 'price': row[1]})
        connection.close()
        return {'items': items}


