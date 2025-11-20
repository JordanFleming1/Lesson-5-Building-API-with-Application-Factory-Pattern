from .extensions import db
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from datetime import date

class Base(DeclarativeBase):
    pass



loan_book = db.Table('loan_book',
    db.Column('loan_id', db.Integer, db.ForeignKey('loans.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
)

class Member(db.Model):
    __tablename__ = 'members'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    DOB: Mapped[date]
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    loans: Mapped[list['Loan']] = relationship('Loan', back_populates='member')

class Loan(db.Model):
    __tablename__ = 'loans'
    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[date] = mapped_column(db.Date)
    member_id: Mapped[int] = mapped_column(db.ForeignKey('members.id'))
    member: Mapped['Member'] = relationship('Member', back_populates='loans')
    books: Mapped[list['Book']] = relationship('Book', secondary=loan_book, back_populates='loans')

class Book(db.Model):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(db.String(255), nullable=False)
    genre: Mapped[str] = mapped_column(db.String(255), nullable=False)
    desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    loans: Mapped[list['Loan']] = relationship('Loan', secondary=loan_book, back_populates='books')
    member_id: Mapped[int] = mapped_column(db.ForeignKey('members.id'))
