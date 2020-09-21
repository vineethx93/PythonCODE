import sqlite3


class ItemModel:
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
