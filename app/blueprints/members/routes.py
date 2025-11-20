from flask import request, jsonify
from . import members_bp
from ...models import Member
from ...schemas import member_schema, members_schema
from ...extensions import db
from sqlalchemy import select
from marshmallow import ValidationError

@members_bp.route('/', methods=['POST'])
def create_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    query = select(Member).where(Member.email == member_data['email'])
    existing_member = db.session.execute(query).scalars().all()
    if existing_member:
        return jsonify({'error': 'Email already associated with an account.'}), 400
    new_member = Member(**member_data)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member), 201

@members_bp.route('/', methods=['GET'])
def get_members():
    query = select(Member)
    members = db.session.execute(query).scalars().all()
    return members_schema.jsonify(members)
