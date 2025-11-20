from flask import request, jsonify
from . import books_bp
from ...models import Book
from ...extensions import db
from sqlalchemy import select

@books_bp.route('/', methods=['GET'])
def get_books():
    query = select(Book)
    books = db.session.execute(query).scalars().all()
    # You can add a schema for serialization if needed
    return jsonify([book.title for book in books])
