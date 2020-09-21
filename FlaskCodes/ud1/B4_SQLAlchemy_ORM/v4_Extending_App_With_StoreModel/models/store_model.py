from db import db


# To use a model class with SQLAlchemy ORM it should extend db.Model
# This will tell the SQLAlchemy that StoreModel is a thing that we are going to save/retrieve using database
# This will create a mapping between the database and this class/obj
class StoreModel(db.Model):

    # tell the table and column details that need to use for StoreModel class
    # IMP: column names should match the variables in the __init__
    # but there is no need that all the properties of the class should be used as a column
    # table name for StoreModel
    __tablename__ = 'stores'
    # columns associated with StoreModel
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # creates a relationship b/w stores and their items(linked by store.id)
    # when SQLAlchemy sees below statement it will go to ItemModel and search for the
    # relationship condition ie.. store_id = db.Column(db.Integer, db.ForeignKey('stores.id')).
    # This will be a list of 'items' that are related to this instance of 'store' model.
    # This will be a many-to-one relationship ie.. many items related to a store by store.id
    #items = db.relationship('ItemModel')  #--------IMP
    # one issue with this is whenever we create a StoreModel/store in db then
    # SQLAlchemy will go to the entire 'items' table and try to establish a relationship
    # for each of the item with the current store (based on store_id/store.id)
    # this is a very expensive operation if the number of items are very large
    # to solve this below statement can be used
    #items = db.relationship('ItemModel', lazy='dynamic') #------IMP
    # but for now lets go with the former(seems less complex to me)
    items = db.relationship('ItemModel')

    def __init__(self, name):
        self.name = name

    # for every model class its good to have a jsonifying method to
    # return the model as a json representation
    def get_json(self):
        # below will work if "lazy='dynamic'" is not given in the relationship above
        #return {'name': self.name, 'items': [item.get_json() for item in self.items]}  #-----IMP
        # but if it is specified "lazy='dynamic'" then "self.items" wont be a list of items
        # but will be a query builder that has the ability to look into the 'items' table
        # (since they are not linked yet).. so use .all() on it
        #return {'name': self.name, 'items': [item.get_json() for item in self.items.all()]}  #-----IMP
        # so everytime we call json it will lookup the items table this will be also might be slower
        # so we can choose any of the approaches..
        # either link all the items to to store when a store/item is created() - No "lazy='dynamic'"
        # or look up them when we call the get_json() "lazy='dynamic'"
        # should choose the right based on the situation
        # so the trade-off is between speed of creation and speed of retrieval using get_json()
        # but for now lets go with former(less complex to me)
        return {'name': self.name, 'items': [item.get_json() for item in self.items]}

    # this should be a class method as it return an object of type StoreModel
    # and not a dictionary
    @classmethod
    def find_by_name(cls, name):
        # sql alchemy finds the row in the db and automaticaly convert that now into a python
        # object of class StoreModel.
        # StoreModel.query is a query builder -> we can build queries using this builder.
        # below statement will create a query same as
        # select * from items where name = name.

        # item = StoreModel.query.filter_by(name=name).first()
        item = cls.query.filter_by(name=name).first()  # same as above

        # LIMIT 1 -> StoreModel.query.filter_by(name=name).first()
        # to filter by multiple things (WHERE col1 = a AND col2 = b AND col3 = c) we can give
        # multiple filter_by one after the another -> StoreModel.query.filter_by(id=id).filter_by(name=name)
        return item

    def upsert(self):
        db.session.add(self)
        db.session.commit()

        # db.session will contain a collection of all the objects that we are going to write to database.
        # we can add multiple objects to the session and write once but here only one obj.

    def delete(self):
        db.session.delete(self)
        db.session.commit()
