import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

class Item(Resource):

    # adding class variable parser to use with any methods
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be blank')

    # adding @jwt_required() decorator to enforce the Token validation for below /item/<string:item_name>/ GET method
    @jwt_required
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM ITEMS WHERE NAME=?'

        result = cursor.execute(query, (name,))
        row = result.fetchone()

        # always close the connection before return statement
        connection.close()

        if row:
            item = {'name': row[0], 'price': row[1]}
            return {'item': item}, 200
        return {'message': 'item not found!'}, 404

    @jwt_required
    def post(self, name):
        # item trying to add is already present in the items list
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "item '{0}' already exists".format(name)}, 400

        # access class variable by ClassName.variable_name
        request_data = Item.parser.parse_args()

        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    @jwt_required
    def delete(self, name):
        for item in items:
            if item['name'] == name:
                items.remove(item)
                return {'message': '{0} removed from items'.format(name)}, 200
        return {'message': 'item with name {0} NOT FOUND!'.format(name)}, 404

    @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        for item in items:
            if item['name'] == name:
                item['price'] = data['price']
                return {'message': 'Item Updated'}, 200
        items.append({'name': name, 'price': data['price']})
        return {'message': 'New Item Created'}, 201


class Items(Resource):
    @jwt_required
    def get(self):
        return {'items': items}
