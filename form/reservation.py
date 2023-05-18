from datetime import datetime
from sqlalchemy.exc import IntegrityError

from flask import request, jsonify
from flask_restx import Resource, fields

from extensions import api, db
from extensions.flask_restx_extension import reservationNS
from models import Reservation
from schemas import ReservationSchema

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)

reservation_model = reservationNS.model('Reservation', {
    'id': fields.Integer(readonly=True),
    'day': fields.Date(required=True),
    'time': fields.String(description='Time in HH:MM format',
                          pattern='^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$',
                          required=True),
    'number': fields.String(required=True),
    'name': fields.String(required=True),
    'user_id': fields.Integer(required=True),
    'restaurant_id': fields.Integer(required=True),
})


# Определение ресурса списка всех Reservation
class ReservationListResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Бронь не найдена'})
    @reservationNS.marshal_list_with(reservation_model)
    def get(self):
        reservations = Reservation.query.all()
        return reservations, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, объект создан',
        400: 'Неверные данные'})
    @reservationNS.expect(reservation_model, validate=True)
    def post(self):
        data = request.json
        errors = reservation_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        reservation = Reservation(
            day=datetime.strptime(data['day'], '%Y-%m-%d').date(),
            time=data['time'],
            number=data['number'],
            name=data['name'],
            user_id=data.get('user_id'),
            restaurant_id=data.get('restaurant_id')
        )
        try:
            db.session.add(reservation)
            db.session.commit()
            return reservation_schema.dump(reservation), 201
        except IntegrityError as e:
            db.session.rollback()
            return {'message': 'Ошибка сохранения в базу данных. Неверные внешние ключи'}, 400


# Определение ресурса для одного Reservation
class ReservationResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Бронь не найдена'})
    @reservationNS.marshal_with(reservation_model)
    def get(self, id):
        reservation = Reservation.query.filter_by(id=id).first()
        if not reservation:
            reservationNS.abort(404, 'Бронь не найдена')
        return reservation, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        400: 'Неверные данные',
        404: 'Бронь не найдена'
    })
    @reservationNS.expect(reservation_model, validate=True)
    def put(self, id):
        reservation = Reservation.query.filter_by(id=id).first()
        if not reservation:
            reservationNS.abort(404, 'Бронь не найдена')
        data = request.json
        errors = reservation_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        try:
            for field, value in data.items():
                setattr(reservation, field, value)
            db.session.commit()
            return reservation_schema.dump(reservation), 200
        except IntegrityError as e:
            db.session.rollback()
            return {'message': 'Ошибка сохранения в базу данных. Неверные внешние ключи'}, 400

    @api.doc(responses={
        200: 'Успешный DELETE-запрос',
        404: 'Бронь не найдена'})
    def delete(self, id):
        reservation = Reservation.query.filter_by(id=id).first()
        if not reservation:
            reservationNS.abort(404, 'Бронь не найдена')
        db.session.delete(reservation)
        db.session.commit()
        return {'msg': 'Бронь удалена успешно'}, 200
