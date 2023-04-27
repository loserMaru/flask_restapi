from flask_restx import fields, Resource

from extensions import api, db
from extensions.flask_restx_extension import cardNS
from models.models import Card
from schemas import CardSchema

card_model = cardNS.model('Card', {
    'id': fields.Integer(readonly=True),
    'cardNumber': fields.String,
    'user_id': fields.Integer,
})

card_schema = CardSchema()

class CardResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @cardNS.marshal_list_with(card_model)
    def get(self):
        cards = Card.query.all()
        return cards

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @cardNS.expect(card_model)
    @cardNS.marshal_with(card_model, code=201)
    def post(self):
        card = Card(**cardNS.payload)
        db.session.add(card)
        db.session.commit()
        return card.to_dict(), 201


class CardResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @cardNS.marshal_with(card_model)
    def get(self, id):
        card = Card.query.filter_by(id=id).first()
        if not card:
            cardNS.abort(404, 'Card not found')
        return card, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @cardNS.expect(card_model)
    def put(self, id):
        card = Card.query.filter_by(id=id).first()
        if not card:
            cardNS.abort(404, 'Card not found')
        for key, value in cardNS.payload.items():
            setattr(card, key, value)
        db.session.commit()
        return card_schema.dump(card), 200

    @api.doc(responses={
        204: 'Успешный DELETE-запрос, ресурс удален',
        404: 'Ресурс не найден'
    })
    def delete(self, id):
        card = Card.query.filter_by(id=id).first()
        if not card:
            cardNS.abort(404, 'Card not found')
        db.session.delete(card)
        db.session.commit()
        return {'result': 'success'}, 204
