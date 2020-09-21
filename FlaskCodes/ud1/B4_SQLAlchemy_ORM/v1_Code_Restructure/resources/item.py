import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.item_model import ItemModel


class Item(Resource):

    # adding class variable parser to use with any methods
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be blank')

    # adding @jwt_required() decorator to enforce the Token validation for below /item/<string:item_name>/ GET method
    @jwt_required
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)  # self.find_by_name(name) will also work here
        except:
            return {'message': 'db search failed'}, 500
        if item:
            # rather than returning the object itself we should return a dictionary
            # this can be done by calling the get_json() method inside the item model to create a dictionary.
            return item.get_json(), 200
        return {'message': 'item not found!'}, 404

    @fresh_jwt_required
    def post(self, name):
        # item trying to add is already present in the items list
        if ItemModel.find_by_name(name):
            return {'message': "item '{0}' already exists".format(name)}, 400

        # access class variable by ClassName.variable_name
        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'])
        try:
            item.insert_item()
        except:
            return {'message': 'insertion to db failed'}, 500
        # if error then execution will stop at return statement of except block
        # if no error then return the item and success code
        return item.get_json(), 201

    @fresh_jwt_required
    def delete(self, name):
        if not ItemModel.find_by_name(name):
            return {'message': 'item with name {0} NOT FOUND!'.format(name)}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        delete_query = 'DELETE FROM ITEMS WHERE NAME=?'
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()
        return {'message': "Item: '{0}' deleted".format(name)}, 200

    @fresh_jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        new_item = ItemModel(name, data['price'])

        # check whether item exists
        try:
            existing_item = ItemModel.find_by_name(name)
        except:
            return {'message': 'db search failed'}, 500

        # if item exists then update it
        if existing_item:
            try:
                existing_item.price = data['price']
                existing_item.update_item()
            except:
                return {'message': 'item update failed'}, 500
            return {"message": "Item '{0}' updated successfully".format(name)}, 200

        # if item is not existing then create a new item
        try:
            new_item.insert_item()
        except:
            return {'message': 'item insertion failed'}, 500
        return {'message': "new item '{0}' created".format(name)}, 201


class Items(Resource):
    @jwt_required
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_query = 'SELECT NAME FROM ITEMS'
        result = cursor.execute(select_query)
        rows = result.fetchall()
        item_names = list()
        if rows:
            for row in rows:
                item_names.append(row[0])
        return {'items': item_names}, 200
