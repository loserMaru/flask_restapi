from marshmallow import Schema, fields

from models import Tables


class TableSchema(Schema):
    id = fields.Int(dump_only=True)
    number = fields.Str(required=True)
    seat = fields.Str()
    restaurant_id = fields.Int(required=True)

    class Meta:
        model = Tables
