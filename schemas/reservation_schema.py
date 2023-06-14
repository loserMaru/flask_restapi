from marshmallow import Schema, fields, validate, EXCLUDE


class ReservationSchema(Schema):
    id = fields.Integer(dump_only=True)
    day = fields.Date(required=True)
    time = fields.String(required=True)
    number = fields.String(required=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    status = fields.Boolean()
    picture = fields.String(required=True)
    user_id = fields.Integer()
    restaurant_id = fields.Integer()

    class Meta:
        fields = ('id', 'day', 'time', 'number', 'name', 'status', 'picture', 'user_id', 'restaurant_id')
        load_instance = True
        unknown = EXCLUDE

    def load_instance(self, data, partial=None, **kwargs):
        if partial and self.only:
            # Не допустить использование `only` с `partial=True`
            raise ValueError("Cannot use 'only' with 'partial=True'")
        return super().load_instance(data, partial=partial, **kwargs)
