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
            item.upsert_item()
        except:
            return {'message': 'insertion to db failed'}, 500
        # if error then execution will stop at return statement of except block
        # if no error then return the item and success code
        return item.get_json(), 201

    @fresh_jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
            return {'message': "Item: '{0}' deleted".format(name)}, 200
        return {'message': 'item with name {0} NOT FOUND!'.format(name)}, 404

    @fresh_jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        # check whether item already exists
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'db search failed'}, 500

        # if item exists then update it and write it to database,
        # else create a new item and write it to database
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'])

        # write the changes to database
        try:
            item.upsert_item()
        except:
            return {'message': 'database write failed'}, 500
        return {"message": 'db write success'}, 200


class Items(Resource):
    @jwt_required
    def get(self):
        items = ItemModel.query.all()
        item_names = [item.name for item in items]

        # if returning all items (not item names only) then use the .get_json() to send a proper dictionary
        # ret_items = [item.get_json() for item in items]

        # will be an empty list if there are no items
        return {'items': item_names}, 200
