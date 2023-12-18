from datetime import datetime

from flask import request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource, fields
from sqlalchemy.exc import IntegrityError

from extensions import api, db, jwt_required_class
from extensions.flask_restx_extension import reservationNS
from models import Reservation, User
from schemas import ReservationSchema

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)
#  pattern='^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$',                         for time in model

reservation_model = reservationNS.model('Reservation', {
    'id': fields.Integer(readonly=True),
    'day': fields.Date(required=True),
    'time': fields.String(description='Time in HH:MM format', default='23:05', required=True),
    'number': fields.String(required=True),
    'name': fields.String(required=True),
    'price': fields.Float(required=True),
    'status': fields.String(default='waiting', required=True),
    'picture': fields.String(required=True),
    'user_id': fields.Integer(required=True),
    'restaurant_id': fields.Integer(required=True),
})


@jwt_required_class
class ReservationListResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Бронь не найдена'})
    @reservationNS.doc(security='jwt')
    @reservationNS.marshal_list_with(reservation_model)
    def get(self):
        """Get a list of reservations"""
        current_user = get_jwt_identity()
        user_id = current_user.get('id')
        role = current_user.get('role')
        restaurant_id = current_user.get('restaurant_id')

        if role == 'moderator' and restaurant_id:
            # Если пользователь - модератор, и у него есть ресторан_id,
            # получаем только бронирования, относящиеся к его ресторану
            reservations = Reservation.query.filter_by(restaurant_id=restaurant_id).all()
        else:
            # Если не модератор или у модератора нет ресторана, получаем все бронирования
            reservations = Reservation.query.filter_by(user_id=user_id).all()

        # Преобразование объектов в словари и возврат списка бронирований
        reservations_data = [reservation.to_dict() for reservation in reservations]
        return reservations_data, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, объект создан',
        400: 'Неверные данные'})
    @reservationNS.doc(security='jwt')
    @reservationNS.expect(reservation_model)
    def post(self):
        """Create new reservation"""
        data = request.json
        errors = reservation_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        reservation = Reservation(
            day=datetime.strptime(data['day'], '%Y-%m-%d').date(),
            time=data['time'],
            number=data['number'],
            name=data['name'],
            price=data['price'],
            status=data.get('status'),
            picture=data['picture'],
            user_id=data['user_id'],
            restaurant_id=data.get('restaurant_id')
        )
        try:
            db.session.add(reservation)
            db.session.commit()
            return reservation_schema.dump(reservation), 201
        except IntegrityError as e:
            db.session.rollback()
            return {'message': 'Ошибка сохранения в базу данных. Неверные внешние ключи'}, 400


@jwt_required_class
class ReservationResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Бронь не найдена'})
    @reservationNS.doc(security='jwt')
    @reservationNS.marshal_with(reservation_model)
    def get(self, id):
        """Get reservation with id"""
        reservation = Reservation.query.filter_by(id=id).first()
        if not reservation:
            reservationNS.abort(404, 'Бронь не найдена')
        return reservation, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        400: 'Неверные данные',
        404: 'Бронь не найдена'
    })
    @reservationNS.doc(security='jwt')
    @reservationNS.expect(reservation_model, validate=True)
    def put(self, id):
        """Edit existing reservation"""
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
    @reservationNS.doc(security='jwt')
    def delete(self, id):
        """Delete existing reservation"""
        reservation = Reservation.query.filter_by(id=id).first()
        if not reservation:
            reservationNS.abort(404, 'Бронь не найдена')
        db.session.delete(reservation)
        db.session.commit()
        return {'msg': 'Бронь удалена успешно'}, 200
