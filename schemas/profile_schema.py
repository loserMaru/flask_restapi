from marshmallow import Schema, fields


class ProfileSchema(Schema):
    id = fields.Integer(dump_only=True)
    nickname = fields.String(required=True)
    picture = fields.String()
    phone = fields.String(required=True)
    user_id = fields.Integer(required=True)

    class Meta:
        fields = ('id', 'nickname', 'picture', 'phone', 'user_id')
