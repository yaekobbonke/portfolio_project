from flask import Flask, jsonify, request, Blueprint, render_template, url_for
from .models import Book
import requests
import asyncio
import httpx
import json
from . import redis_client

library_bp = Blueprint('library', __name__)


@library_bp.route('/add_to_db', methods=['POST', 'GET'])
def add_to_db():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']

        books = Book.query.all()
        if books:
            return jsonify([book.json() for book in books])
        else:
            new_books = Book(
                title=title,
                author=author,
                description=description)
            db.session.add(new_books)
            db.session.commit()
            return redirect(url_for('library.home'))
    else:
        return render_template('library_data.html')


@library_bp.route('/library/books/<isbn>', methods=['GET'])
async def get_book(isbn):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://openlibrary.org/isbn/{isbn}.json')

        if response.status_code == 200:
            book_data = response.json()
            book_title = book_data['title']
            book_author = book_data['authors'][0]['name']

            book = {
                'title': book_title,
                'author': book_author
            }

            return render_template('book.html', book=book)
        else:
            return jsonify({'error': 'Book not found'}), 404


@library_bp.route('/library', methods=['GET'])
def library():
    library_data = get_library_data_from_cache()
    if not library_data:
        library_data = fetch_library_data_from_database()
        cache_library_data(library_data)
    return render_template('library.html', library_data=library_data)


def get_library_data_from_cache():
    library_data = redis_client.get('library_data')

    if library_data:
        return json.loads(library_data.decode('utf-8'))
    else:
        return None


def cache_library_data(library_data):
    redis_client.set('library_data', json.dumps(library_data))


def fetch_library_data_from_database():
    books = Book.query.all()
    library_data = [{'title': book.title, 'author': book.author}
                    for book in books]
    return library_data
