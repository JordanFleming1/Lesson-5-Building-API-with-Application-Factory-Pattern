import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps

SECRET_KEY = 'your-secret-key'  # Use a secure, environment-based value in production
ALGORITHM = 'HS256'

# Expires in 1 hour by default
def encode_token(user_id, expires_in=3600):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['user_id']
    except Exception:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        user_id = decode_token(token)
        if not user_id:
            return jsonify({'error': 'Token is invalid!'}), 401
        return f(user_id, *args, **kwargs)
    return decorated
