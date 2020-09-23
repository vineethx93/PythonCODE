from flask_restful import Resource
from models.store_model import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.get_json(), 200
        return {'message': 'store not found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "store with name '{0}' already exists".format(name)}, 400

        store = StoreModel(name)
        try:
            StoreModel.upsert(store)
        except:
            return {'message': 'internal server error'}, 500
        return {"message": "store with name '{0}' created successfully".format(name)}, 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
            return {'message': 'store deleted successfully'}, 200
        return {'message': 'store not found'}, 404

class StoreList(Resource):
    def get(self):
        stores = StoreModel.query.all()
        store_names = [store.name for store in stores]
        return {'stores': store_names}, 200
