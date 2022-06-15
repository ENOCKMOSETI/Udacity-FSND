import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.

def paginate_books (request, books):
    page = request.args.get('page', 1, type=int)
    start = (page -1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    books = [book.format() for book in books]
    books_on_page = books[start:end]

    return books_on_page

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization,true"
        response.headers["Access-Control-Allow-Methods"] = "GET,PATCH,POST,DELETE,OPTIONS"
        return response

    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
    @app.route('/books', methods=['GET'])
    def get_books():
        books = Book.query.order_by(Book.id).all()
        books_on_page = paginate_books(request, books)
        if len(books_on_page) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'books': books_on_page,
            'total_books': len(books_on_page)
        })
        # page = request.args.get('page', 1, type=int)
        # start = (page - 1) * BOOKS_PER_SHELF
        # end = start + BOOKS_PER_SHELF
        # try:
        #     books = Book.query.all()
        #     formatted_books = [book.format() for book in books]
        # except:
        #     print(sys.exc_info())
        #     abort(404)
        # return jsonify({
        #     'success': True,
        #     'books': formatted_books[start:end],
        #     'total_books': len(formatted_books)
        # })
    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):
        body = request.get_json()

        try:

            book = Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                abort(404)

            if 'rating' in body:
                book.rating = int(body['rating'])
            
            book.update()

            return jsonify({
                "success": True, 
                "book": book.format()
            })

        except:
            print(sys.exc_info())
            abort(422)
    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)
            book.delete()
            books = Book.query.order_by(Book.id).all()
            books_on_page = paginate_books(request, books)
            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': books_on_page,
                'total_books': len(books_on_page)
            })
        except:
            print(sys.exc_info())
            abort(404)
        # book = Book.query.filter(book_id == Book.id).one_or_none()
        # book.delete()
        # page = request.args.get('page', 1, type=int)
        # start = (page - 1) * BOOKS_PER_SHELF
        # end = start + BOOKS_PER_SHELF
        # try:
        #     books = Book.query.all()
        #     formatted_books = [book.format() for book in books]
        # except:
        #     print(sys.exc_info())
        # return jsonify({
        #     'success': True,
        #     'books': formatted_books[start:end],
        #     'total_books': len(formatted_books)
        # })
    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.

    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to add a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.
    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()
        book = Book(
            title = body['title'],
            author = body['author'],
            rating = body['rating']
        )
        try:
            book.insert()
            books = Book.query.order_by(Book.id).all()
            books_on_page = paginate_books(request, books)
            return ({
                'success': True,
                'created': book.format()
            })
        except:
            abort(422)

    #search for book by title
    @app.route('/books/search', methods=['POST'])
    def search_book_by_title():
        body = request.get_json()
        search = body['search']
        try:
            books = Book.query.filter(Book.title.ilike('%' + search + '%')).with_entities(Book.id.label('id'), Book.title.label('title'), Book.author.label('author'), Book.rating.label('rating')).all()
            return ({
                'success': True,
                'totalBooks': len(books),
                'books': Book.format_all(books),
                'page': request.args.get('page')
            })
        except:
            print(sys.exc_info())
            abort(404)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': '400',
            'message': 'could not process bad request'
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': '404',
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': '405',
            'message': 'method not allowed'
        })

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': '422',
            'message': 'resource unprocessable'
        }), 422

    return app