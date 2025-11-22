from flask import request, jsonify
from . import members_bp
from ...models import Member
from ...schemas import member_schema, members_schema
from ...extensions import db, cache
from sqlalchemy import select
from marshmallow import ValidationError
from functools import wraps
from app.extensions import cache, decode_auth_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        user_id = decode_auth_token(token)
        if not user_id:
            return jsonify({'error': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

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
@cache.cached(timeout=60)
@token_required
def get_members():
    limit = request.args.get('limit', default=10, type=int)
    query = select(Member).limit(limit)
    members = db.session.execute(query).scalars().all()
    return members_schema.jsonify(members)
