from flask_restx import fields, Resource

from extensions import api, db
from extensions.flask_restx_extension import cardNS
from models.models import Card

card_model = cardNS.model('Card', {
    'id': fields.Integer(readonly=True),
    'cardNumber': fields.String,
    'user_id': fields.Integer,
})


class CardResourceList(Resource):
    @cardNS.marshal_list_with(card_model)
    def get(self):
        cards = Card.query.all()
        return cards

    @cardNS.expect(card_model)
    def post(self):
        card = Card(**cardNS.payload)
        db.session.add(card)
        db.session.commit()
        return {'result': 'success'}


class CardResource(Resource):
    @cardNS.marshal_with(card_model)
    def get(self, card_id):
        card = Card.query.filter_by(id=card_id).first()
        if not card:
            cardNS.abort(404, 'Card not found')
        return card

    @cardNS.expect(card_model)
    def put(self, card_id):
        card = Card.query.filter_by(id=card_id).first()
        for key, value in cardNS.payload.items():
            setattr(card, key, value)
        db.session.commit()
        return {'result': 'success'}

    def delete(self, card_id):
        card = Card.query.filter_by(id=card_id).first()
        if not card:
            cardNS.abort(404, 'User not found')
        db.session.delete(card)
        db.session.commit()
        return {'result': 'success'}
