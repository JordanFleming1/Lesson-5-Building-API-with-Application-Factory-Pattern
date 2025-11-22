from flask import request, jsonify
from app.blueprints.customer import customer_bp
from app.models import Member, Loan
from app.extensions import db
from app.schemas import login_schema, CustomerSchema
from utils.util import encode_token, token_required
from sqlalchemy import select

@customer_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    email = data['email']
    password = data['password']
    query = select(Member).where(Member.email == email)
    customer = db.session.execute(query).scalar_one_or_none()
    if customer and customer.password == password:
        token = encode_token(customer.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid email or password'}), 401

@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
def my_tickets(customer_id):
    query = select(Loan).where(Loan.member_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    # You can serialize tickets with a schema if needed
    return jsonify({'tickets': [ticket.id for ticket in tickets]})

@customer_bp.route('/', methods=['GET'])
def get_customers():
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    offset = (page - 1) * page_size
    query = select(Member).offset(offset).limit(page_size)
    customers = db.session.execute(query).scalars().all()
    schema = CustomerSchema(many=True)
    return jsonify(schema.dump(customers))
