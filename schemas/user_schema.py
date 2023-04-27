from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    email = fields.Email(error_messages={'invalid': 'Некорректный email адрес'}, required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True)
