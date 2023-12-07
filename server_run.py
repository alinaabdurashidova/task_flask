from flask import Flask, jsonify, request
from main import *

app = Flask(__name__)

@app.route('/get_all_books/', methods=['GET'])
def get_all_books_route():
    try:
        books = get_all_books()
        return jsonify({'books': books})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/create_book/', methods=['POST'])
def create_book_route():
    try:
        new_book_data = request.get_json()
        new_book = create_book(new_book_data)
        return jsonify({'message': 'Book created successfully', 'book': new_book})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/update_book/<int:book_id>/', methods=['PUT'])
def update_book_route(book_id):
    try:
        updated_data = request.get_json()
        updated_book = update_book(book_id, updated_data)
        if updated_book:
            return jsonify({'message': 'Book updated successfully', 'book': updated_book})
        else:
            return jsonify({'error': 'Book not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/delete_book/<int:book_id>/', methods=['DELETE'])
def delete_book_route(book_id):
    try:
        delete_result = delete_book_by_id(book_id)
        if delete_result:
            return jsonify({'message': 'Book deleted successfully'})
        else:
            return jsonify({'error': 'Book not found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.run(host='localhost', port=8000) 