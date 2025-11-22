import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../utils')))
from util import encode_token, token_required

from flask import request, jsonify
from app.blueprints.user import user_bp
from app.models import User
from app.extensions import db
#from .schemas import user_schema, users_schema  # Uncomment if you have user schemas
from sqlalchemy import select

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = request.json
        email = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify({'message': 'Invalid payload, expecting email and password'}), 400
    query = select(User).where(User.email == email)
    user = db.session.execute(query).scalar_one_or_none()
    if user and user.password == password:
        auth_token = encode_token(user.id)
        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': "Invalid email or password"}), 401

@user_bp.route('/', methods=['DELETE'])
@token_required
def delete_user(user_id):
    query = select(User).where(User.id == user_id)
    user = db.session.execute(query).scalars().first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"successfully deleted user {user_id}"}), 200
