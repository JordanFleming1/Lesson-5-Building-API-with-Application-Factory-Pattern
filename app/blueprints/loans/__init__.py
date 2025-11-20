from flask import Blueprint

loans_bp = Blueprint('loans', __name__, url_prefix='/loans')

from . import routes
