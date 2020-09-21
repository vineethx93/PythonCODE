from db import db


# To use a model class with SQLAlchemy ORM it should extend db.Model
# This will tell the SQLAlchemy that ItemModel is a thing that we are going to save/retrieve using database
# This will create a mapping between the database and this class/obj
class ItemModel(db.Model):

    # tell the table and column details that need to use for ItemModel class
    # IMP: column names should match the variables in the __init__
    # but there is no need that all the properties of the class should be used as a column
    # table name for ItemModel
    __tablename__ = 'items'
    # columns associated with ItemModel
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))  # precision is the no. of digits after the decimal point
    # this is to create link between the Items and Stores.
    # In Items store_id is a Foreign key and in Stores it is a primary key
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # so the store which matches the store_id will be available as a propery of item.
    # same as using JOIN in SQL (on items.store_id = stores.id)
    # one or more items will be related to a 'store'
    # it will be a single store value corresponding to that particular item
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # for every model class its good to have a jsonifying method to
    # return the model as a json representation
    def get_json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    # this should be a class method as it return an object of type ItemModel
    # and not a dictionary
    @classmethod
    def find_by_name(cls, name):
        # sql alchemy finds the row in the db and automaticaly convert that now into a python
        # object of class ItemModel.
        # ItemModel.query is a query builder -> we can build queries using this builder.
        # below statement will create a query same as
        # select * from items where name = name.

        # item = ItemModel.query.filter_by(name=name).first()
        item = cls.query.filter_by(name=name).first()  # same as above

        # LIMIT 1 -> ItemModel.query.filter_by(name=name).first()
        # to filter by multiple things (WHERE col1 = a AND col2 = b AND col3 = c) we can give
        # multiple filter_by one after the another -> ItemModel.query.filter_by(id=id).filter_by(name=name)
        return item

    def upsert_item(self):
        db.session.add(self)
        db.session.commit()

        # db.session will contain a collection of all the objects that we are going to write to database.
        # we can add multiple objects to the session and write once but here only one obj.

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
