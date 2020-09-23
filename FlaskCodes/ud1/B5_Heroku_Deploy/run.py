from app import app
from db import db


db.init_app(app)


# this will execute the below function before the first request hits the application
@app.before_first_request
def create_tables():
    db.create_all()
    # this will create the tables(as configured in the models)
    # in the db URI - app.config['SQLALCHEMY_DATABASE_URI'] - IF NOT already existing
