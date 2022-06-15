# API Reference

## Introduction

    This is the documentation for a bookshelf api

## Getting Started

    - Base URL: App runs locally at http://127.0.0.1:5000 which is set as a proxy in the frontend configuration
    - Authentication: This version does not require authentication or API keys

## Errors

    Errors are returned as json objects in the following format:
    {
        'success': False,
        'error': 404,
        'message': 'not found'
    }
    - Response codes: 400, 404, 422
    - Messages: 'success', 'bad request', 'method not allowed', 'unprocessable'
    - Error types: 'not found'
## Endpoints

# GET /books
    Returns an object with a success value, list of book objects sorted by id and total number of books on page
    Results are paginated in groups of 8. Include a page number as a request argument.
    Returns the first page if no argument is passed

    Sample: curl http://127.0.0.1:5000/books
    `
        "books": [
            {
            "author": "Stephen King", 
            "id": 1, 
            "rating": 5, 
            "title": "The Outsider: A Novel"
            }, 
            {
            "author": "Lisa Halliday", 
            "id": 2, 
            "rating": 4, 
            "title": "Asymmetry: A Novel"
            }, 
            {
            "author": "Kristin Hannah", 
            "id": 3, 
            "rating": 5, 
            "title": "The Great Alone"
            }, 
            {
            "author": "Tara Westover", 
            "id": 4, 
            "rating": 5, 
            "title": "Educated: A Memoir"
            }, 
            {
            "author": "Leila Slimani", 
            "id": 6, 
            "rating": 5, 
            "title": "Lullaby"
            }, 
            {
            "author": "Amitava Kumar", 
            "id": 7, 
            "rating": 5, 
            "title": "Immigrant, Montana"
            }, 
            {
            "author": "Tayari Jones", 
            "id": 10, 
            "rating": 1, 
            "title": "An American Marriage"
            }, 
            {
            "author": "Jordan B. Peterson", 
            "id": 11, 
            "rating": 5, 
            "title": "12 Rules for Life: An Antidote to Chaos"
            }
        ], 
        "success": true, 
        "total_books": 8

    `
# DELETE /books/{book_id}
    Removes a book object with specified id and returns an object with a success value, the id of the deleted book, list of remaining book objects sorted by id and total number of books on page
    Requires a valid book id else just returns a 404 for resource not found

    Sample: curl -X DELETE http://127.0.0.1:5000/1
    `
        "books": [
        {
        "author": "Lisa Halliday", 
        "id": 2, 
        "rating": 4, 
        "title": "Asymmetry: A Novel"
        }, 
        {
        "author": "Kristin Hannah", 
        "id": 3, 
        "rating": 5, 
        "title": "The Great Alone"
        }, 
        {
        "author": "Tara Westover", 
        "id": 4, 
        "rating": 5, 
        "title": "Educated: A Memoir"
        }, 
        {
        "author": "Leila Slimani", 
        "id": 6, 
        "rating": 5, 
        "title": "Lullaby"
        }, 
        {
        "author": "Amitava Kumar", 
        "id": 7, 
        "rating": 5, 
        "title": "Immigrant, Montana"
        }, 
        {
        "author": "Tayari Jones", 
        "id": 10, 
        "rating": 1, 
        "title": "An American Marriage"
        }, 
        {
        "author": "Jordan B. Peterson", 
        "id": 11, 
        "rating": 5, 
        "title": "12 Rules for Life: An Antidote to Chaos"
        }, 
        {
        "author": "Kiese Laymon", 
        "id": 12, 
        "rating": 2, 
        "title": "Heavy: An American Memoir"
        }
    ], 
    "deleted": 1, 
    "success": true, 
    "total_books": 8
    ` 
    curl -X DELETE http://127.0.0.1:5000/1
    `
        {
            "error": "404", 
            "message": "resource not found", 
            "success": false
        }
    `
# PATCH http://127.0.0.1/books/{book_id}
    updates the rating of a book object returning a success value and the updated book object

    Sample: curl http://127.0.0.1:5000/books/2 -X PATCH -H "Content-Type: application/json" -d '{"rating":"2"}'
    `
        "book": {
            "author": "Lisa Halliday", 
            "id": 2, 
            "rating": 2,
            "title": "Asymmetry: A Novel"
        }, 
        "success": true

    `
# POST http://127.0.0.1/books
    adds a book object to the list of book objects returning a sucess value and the created book object

    Sample: curl http://127.0.0.1:5000/books -X POST -H "Content-Type: application/json" -d '{"title": "Google It", "author": "Newton Lee", "rating": '3'}'
    `
        "created": {
            "author": "Newton Lee", 
            "id": 41, 
            "rating": 3, 
            "title": "Google It"
        }, 
        "success": true

    `

# POST http://127.0.0.1/books/{search}
    returns a success value and a list of book object with a title that includes the search term

    Sample: curl http://127.0.0.1:5000/books/search -X POST -H "Content-Type: application/json" -d '{"search": "Google"}'
    `
        "books": [
            {
            "author": "Patrice-Anne Rutledge", 
            "id": 39, 
            "rating": 4, 
            "title": "My Google Apps"
            }, 
            {
            "author": "Newton Lee", 
            "id": 40, 
            "rating": 3, 
            "title": "Google It"
            }, 
            {
            "author": "Newton Lee", 
            "id": 41, 
            "rating": 3, 
            "title": "Google It"
            }
        ], 
        "page": null, 
        "success": true, 
        "totalBooks": 3
    `
