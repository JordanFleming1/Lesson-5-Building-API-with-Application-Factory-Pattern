from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from jose import jwt

SECRET_KEY = 'your-secret-key'  # Change this to a secure value

db = SQLAlchemy()
ma = Marshmallow()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
limiter = Limiter(key_func=get_remote_address)

def encode_auth_token(user_id):
    return jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')

def decode_auth_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except Exception:
        return None