from flask import Flask
from app.extensions import db, ma, cache, limiter
from app.config import DevelopmentConfig
from app.blueprints import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    # Optional: Set a global default rate limit
    app.config['RATELIMIT_DEFAULT'] = '100 per hour'
    register_blueprints(app)
    return app