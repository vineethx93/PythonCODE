import sqlite3
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

    def __init__(self, name, price):
        self.name = name
        self.price = price

    # for every model class its good to have a jsonifying method to
    # return the model as a json representation
    def get_json(self):
        return {'name': self.name, 'price': self.price}

    # this should be a class method as it return an object of type ItemModel
    # and not a dictionary
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
            item = cls(name=row[0], price=row[1])
            # same as above
            # item = cls(row[0], row[1])
        return item

    def insert_item(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = 'INSERT INTO ITEMS(NAME, PRICE) VALUES(?, ?)'
        cursor.execute(insert_query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update_item(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        update_query = 'UPDATE ITEMS SET PRICE=? WHERE NAME=?'
        cursor.execute(update_query, (self.price, self.name))
        connection.commit()
        connection.close()
