from flask import request, jsonify
from . import books_bp
from ...models import Book
from ...extensions import db
from sqlalchemy import select

@books_bp.route('/popular', methods=['GET'])
def get_popular_books():
    books = db.session.execute(select(Book)).scalars().all()
    books_sorted = sorted(books, key=lambda b: len(b.loans), reverse=True)
    limit = request.args.get('limit', default=10, type=int)
    return jsonify([{'id': b.id, 'title': b.title, 'loan_count': len(b.loans)} for b in books_sorted[:limit]])

@books_bp.route('/search', methods=['GET'])
def search_books():
    term = request.args.get('q', '')
    query = select(Book).where(Book.title.ilike(f'%{term}%'))
    books = db.session.execute(query).scalars().all()
    return jsonify([{'id': b.id, 'title': b.title} for b in books])

@books_bp.route('/', methods=['GET'])
def get_books():
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    offset = (page - 1) * page_size
    query = select(Book).offset(offset).limit(page_size)
    books = db.session.execute(query).scalars().all()
    return jsonify([{'id': b.id, 'title': b.title} for b in books])
