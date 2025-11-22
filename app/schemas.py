from .extensions import ma
from .models import Member, Mechanic, ServiceTicket
from marshmallow import ValidationError, fields

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Mechanic schema for mechanics blueprint
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

# ServiceTicket schema for service_tickets blueprint
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

# CustomerSchema for authentication (alias for MemberSchema)
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

# LoginSchema: only email and password
class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

login_schema = LoginSchema()
