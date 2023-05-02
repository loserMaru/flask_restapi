from marshmallow import Schema, fields


class RestaurantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    picture = fields.Str()
    hidden = fields.Bool(required=True)
