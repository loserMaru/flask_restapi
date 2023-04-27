from marshmallow import Schema, fields


class FavoriteSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    restaurant_id = fields.Integer(required=True)

    class Meta:
        fields = ('id', 'user_id', 'restaurant_id')
