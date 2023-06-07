from flask_restx import fields, Resource

from extensions import api, db, jwt_required_class
from extensions.flask_restx_extension import cardNS
from form.validations import contains_only_digits
from models.models import Card
from schemas import CardSchema

card_model = cardNS.model('Card', {
    'id': fields.Integer(readonly=True),
    'cardNumber': fields.String(required=True),
    'user_id': fields.Integer(required=True),
})

card_schema = CardSchema()


@jwt_required_class
class CardResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @cardNS.doc(security='jwt')
    @cardNS.marshal_list_with(card_model)
    def get(self):
        """Get card list"""
        cards = Card.query.all()
        return cards

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @cardNS.expect(card_model)
    @cardNS.doc(security='jwt')
    @cardNS.marshal_with(card_model, code=201)
    def post(self):
        """Add new card"""
        card = Card(**cardNS.payload)
        card_number = cardNS.payload.get('cardNumber')
        if not contains_only_digits(card_number):
            api.abort(400, 'Карта должна содержать только цифры')
        user_id = cardNS.payload.get('user_id')
        if user_id == 0:
            cardNS.abort(400, 'Карта должна кому-то принадлежать(user_id = 0)')
        db.session.add(card)
        db.session.commit()
        return card.to_dict(), 201


@jwt_required_class
class CardResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @cardNS.doc(security='jwt')
    @cardNS.marshal_with(card_model)
    def get(self, id):
        """Get card with id"""
        card = Card.query.filter_by(id=id).first()
        if not card:
            cardNS.abort(404, 'Карта не найдена')
        return card, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @cardNS.doc(security='jwt')
    @cardNS.expect(card_model)
    def put(self, id):
        """Edit an existing card"""
        card = Card.query.filter_by(id=id).first()
        if not card:
            cardNS.abort(404, 'Карта не найдена')
        for key, value in cardNS.payload.items():
            setattr(card, key, value)
        db.session.commit()
        return card_schema.dump(card), 200

    @api.doc(responses={
        200: 'Успешный DELETE-запрос, ресурс удален',
        404: 'Ресурс не найден'
    })
    @cardNS.doc(security='jwt')
    def delete(self, id):
        """Delete existing card"""
        card = Card.query.filter_by(id=id).first()
        if not card:
            cardNS.abort(404, 'Карта не найдена')
        db.session.delete(card)
        db.session.commit()
        return {'msg': 'Успешный DELETE-запрос, ресурс удален'}, 200
