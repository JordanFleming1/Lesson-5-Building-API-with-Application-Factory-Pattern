from flask import request, jsonify
from . import loans_bp
from ...models import Loan, Book, Member
from ...extensions import db
from sqlalchemy import select

@loans_bp.route('/', methods=['GET'])
def get_loans():
    query = select(Loan)
    loans = db.session.execute(query).scalars().all()
    return jsonify([loan.id for loan in loans])

@loans_bp.route('/<int:loan_id>/books', methods=['GET'])
def get_books_for_loan(loan_id):
    loan = db.session.get(Loan, loan_id)
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404
    return jsonify({'books': [book.id for book in loan.books]})

@loans_bp.route('/<int:loan_id>/add-book/<int:book_id>', methods=['PUT'])
def add_book_to_loan(loan_id, book_id):
    loan = db.session.get(Loan, loan_id)
    book = db.session.get(Book, book_id)
    if not loan or not book:
        return jsonify({'error': 'Loan or Book not found'}), 404
    if book not in loan.books:
        loan.books.append(book)
        db.session.commit()
    return jsonify({'message': 'Book added to loan', 'books': [b.id for b in loan.books]})

@loans_bp.route('/<int:loan_id>/remove-book/<int:book_id>', methods=['PUT'])
def remove_book_from_loan(loan_id, book_id):
    loan = db.session.get(Loan, loan_id)
    book = db.session.get(Book, book_id)
    if not loan or not book:
        return jsonify({'error': 'Loan or Book not found'}), 404
    if book in loan.books:
        loan.books.remove(book)
        db.session.commit()
    return jsonify({'message': 'Book removed from loan', 'books': [b.id for b in loan.books]})

@loans_bp.route('/book/<int:book_id>/loans', methods=['GET'])
def get_loans_for_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({'loans': [loan.id for loan in book.loans]})

@loans_bp.route('/member/<int:member_id>/loans', methods=['GET'])
def get_loans_for_member(member_id):
    member = db.session.get(Member, member_id)
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    return jsonify({'loans': [loan.id for loan in member.loans]})
