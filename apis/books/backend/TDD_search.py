import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book

class BookSearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'bookshelf_test'
        self.database_uri = os.environ.get('DB_URI')
        self.database_path = 'postgresql://{}/{}'.format(self.database_uri, self.database_name)
        setup_db(self.app, self.database_path)

        # bind app to current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
        
    def tearDown(self) -> None:
        return super().tearDown()

# @TODO write tests for when searching a book, one each for success and error
    def test_search_book_by_title(self):
        res = self.client().post('/books/search', json={'search': 'novel'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalBooks'], 2)
        self.assertTrue(data['books'])

if __name__ == '__main__':
    unittest.main()