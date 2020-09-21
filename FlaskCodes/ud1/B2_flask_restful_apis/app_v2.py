from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        # can replace the for loop and conditional check by any of the below two lines

        # use a filter function(lambda function here) and the list of items to find the match >>
        # converting filter iterator obj into a list and accessing first item of it
        # while using this be careful to check the length of the list first before accessing the first element
        # as list donot have a safe .get() with default value
        # item = list(filter(lambda x: x['name'] == name, items))[0]

        # use a filter function(lambda function here) and the list of items to find the match >>
        # calling next() one time on the filter iterator obj to get the first element >>
        # if no element found then None is returned
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
        # "if item" wont be satisfied if the item is None,0,0.00 etc..(a False value)

    def post(self, name):
        # item trying to add is already present in the items list
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "item '{0}' already exists".format(name)}, 400

        # else if item is not in the list then try to insert the item
        request_data = request.get_json()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201


class Items(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>/')
api.add_resource(Items, '/items/')


if __name__ == '__main__':
    app.run(debug=True)
