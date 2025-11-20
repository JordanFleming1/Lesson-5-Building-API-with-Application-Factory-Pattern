from flask import request, jsonify
from . import loans_bp
from ...models import Loan
from ...extensions import db
from sqlalchemy import select

@loans_bp.route('/', methods=['GET'])
def get_loans():
    query = select(Loan)
    loans = db.session.execute(query).scalars().all()
    # You can add a schema for serialization if needed
    return jsonify([loan.id for loan in loans])
