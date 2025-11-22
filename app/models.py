from .extensions import db
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from datetime import date, datetime

class Base(DeclarativeBase):
    pass

# Simple junction table for many-to-many (no extra fields)
loan_book = db.Table(
    'loan_book',
    db.Column('loan_id', db.Integer, db.ForeignKey('loans.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
)

mechanic_service_ticket = db.Table(
    'mechanic_service_ticket',
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)

# Inventory <-> ServiceTicket many-to-many
inventory_service_ticket = db.Table(
    'inventory_service_ticket',
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
)

class MechanicServiceTicket(db.Model):
    __tablename__ = "mechanic_service_ticket_model"
    id = db.Column(db.Integer, primary_key=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey("mechanics.id"), nullable=False)
    service_ticket_id = db.Column(db.Integer, db.ForeignKey("service_tickets.id"), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    mechanic = db.relationship("Mechanic", back_populates="mechanic_tickets")
    service_ticket = db.relationship("ServiceTicket", back_populates="mechanic_tickets")

class Mechanic(db.Model):
    __tablename__ = "mechanics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(150), unique=True, nullable=False)
    salary = db.Column(db.Float(), nullable=False)
    # Simple many-to-many
    service_tickets = db.relationship(
        'ServiceTicket',
        secondary=mechanic_service_ticket,
        back_populates='mechanics'
    )
    # Complex many-to-many
    mechanic_tickets = db.relationship("MechanicServiceTicket", back_populates="mechanic")

class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"
    id = db.Column(db.Integer, primary_key=True)
    VIN = db.Column(db.Float(), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    service_date = db.Column(db.Date)
    customer_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    # Simple many-to-many
    mechanics = db.relationship(
        'Mechanic',
        secondary=mechanic_service_ticket,
        back_populates='service_tickets'
    )
    # Complex many-to-many
    mechanic_tickets = db.relationship("MechanicServiceTicket", back_populates="service_ticket")
    inventory_items = db.relationship(
        'Inventory',
        secondary=inventory_service_ticket,
        back_populates='service_tickets'
    )

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    service_tickets = db.relationship(
        'ServiceTicket',
        secondary=inventory_service_ticket,
        back_populates='inventory_items'
    )

# Member, Loan, Book models
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

# User model for authentication/authorization (for user blueprint)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
