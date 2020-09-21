from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'test_store',
        'items': [
            {
                'item': 'test_item',
                'price': 15.99
            }
        ]
    }
]

# POST /store data:{name:}
@app.route('/store/', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {'name': request_data['name'],
                 'items': []
                 }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Store Not Found'})

# GET /store
@app.route('/store/', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'item': request_data['item'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Store Not Found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['GET'])
def get_item(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'Store Not Found'})


# another way
# app.add_url_rule('/store/', get_stores)

if __name__ == '__main__':
    app.run(debug=False)