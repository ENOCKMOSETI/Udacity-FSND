import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "bookshelf"
database_uri = os.environ.get('DB_URI')
database_path = "postgresql://{}/{}".format(
    database_uri, database_name
)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Book

"""


class Book(db.Model):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    rating = Column(Integer)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "rating": self.rating,
        }

    def format_all(raw):
        books = []
        for book in raw:
            books.append({
                "id": book[0],
                "title": book[1],
                "author": book[2],
                "rating": book[3],
            })
        return books