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
        item = Item.find_by_name(name)  # self.find_by_name(name) will also work here
        if item:
            return {'item': item}, 200
        return {'message': 'item not found!'}, 404

    @classmethod
    def find_by_name(cls, name):
        item = None
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM ITEMS WHERE NAME=?'

        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()  # always close the connection before return statement

        if row:
            item = {'name': row[0], 'price': row[1]}
            return item
        return item

    @jwt_required
    def post(self, name):
        # item trying to add is already present in the items list
        if Item.find_by_name(name):
            return {'message': "item '{0}' already exists".format(name)}, 400

        # access class variable by ClassName.variable_name
        request_data = Item.parser.parse_args()
        item = {'name': name, 'price': request_data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = 'INSERT INTO ITEMS(NAME, PRICE) VALUES(?, ?)'
        cursor.execute(insert_query, (item['name'], item['price']))
        connection.commit()
        connection.close()

        return item, 201

    @jwt_required
    def delete(self, name):
        if not Item.find_by_name(name):
            return {'message': 'item with name {0} NOT FOUND!'.format(name)}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        delete_query = 'DELETE FROM ITEMS WHERE NAME=?'
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()
        return {'message': "Item: '{0}' deleted".format(name)}, 200


    @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if item:
            update_query = 'UPDATE ITEMS SET PRICE=? WHERE NAME=?'
            cursor.execute(update_query, (data['price'], name))
            connection.commit()
            connection.close()
            return {"message": "Item '{0}' updated successfully".format(name)}, 200
        insert_query = 'INSERT INTO ITEMS(NAME, PRICE) VALUES(?, ?)'
        cursor.execute(insert_query, (name, data['price']))
        connection.commit()
        connection.close()
        return {"message": "New item '{0}' created".format(name)}, 201


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
