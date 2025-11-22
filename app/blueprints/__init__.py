from .members import members_bp
from .books import books_bp
from .loans import loans_bp
from .mechanics import mechanics_bp
from .service_tickets import service_tickets_bp
from .user import user_bp
from .customer import customer_bp
from .inventory import inventory_bp

def register_blueprints(app):
    app.register_blueprint(members_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(loans_bp)
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(inventory_bp)
