from marshmallow import Schema, fields


class RatingSchema(Schema):
    id = fields.Integer(dump_only=True)
    rating = fields.Float(required=True)
    user_id = fields.Integer(required=True)
    restaurant_id = fields.Integer(required=True)
