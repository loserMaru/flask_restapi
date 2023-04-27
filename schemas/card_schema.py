from marshmallow import Schema, fields

class CardSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    number = fields.Integer(required=True)
    expiration_date = fields.String(required=True)
