from .extensions import ma
from .models import Member
from marshmallow import ValidationError

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
