from marshmallow import Schema, fields


class CardSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    cardNumber = fields.Integer(required=True)
