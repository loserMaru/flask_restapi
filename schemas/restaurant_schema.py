from marshmallow import Schema, fields


class RestaurantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    picture = fields.Str()
    price = fields.Float(required=True)
    star = fields.Float(required=True)
    tableCount = fields.Int(required=True)
    cat_id = fields.Int(required=True)
