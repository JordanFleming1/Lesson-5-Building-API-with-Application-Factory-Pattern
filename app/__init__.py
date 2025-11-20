from flask import Flask
from app.extensions import db, ma
from app.config import DevelopmentConfig
from app.blueprints import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    ma.init_app(app)
    register_blueprints(app)
    return app