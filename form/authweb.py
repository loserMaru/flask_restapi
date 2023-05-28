from datetime import datetime, timedelta

from flask_restx import fields, Resource
from flask import request

from extensions import loginNS, jwt
from extensions.flask_restx_extension import authWebNS, api, reservationNS
from form.reservation import reservation_model
from form.validations import is_valid_email, password_is_valid, verify_password
from models import User, Reservation

login_model = loginNS.model('Login', {
    'email': fields.String(required=True, default='string@gmail.com'),
    'password': fields.String(required=True)
})

JWT_SECRET_KEY = 'super-secret-key'


class WebAuthResource(Resource):
    @authWebNS.expect(login_model)
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not is_valid_email(email):
            authWebNS.abort(400, 'Некорректный email')
        if not password_is_valid(password):
            authWebNS.abort(400, 'Некорректный пароль')

        user = User.query.filter_by(email=email).first()
        if not user:
            authWebNS.abort(401, 'Неправильный email или пароль')

        if not verify_password(password, user.password):
            authWebNS.abort(401, 'Неправильный email или пароль')

        if user.role != 'restaurant':
            authWebNS.abort(401, 'Неподходящая роль')

        return {'message': 'Успешный вход'}, 200

    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Бронь не найдена'})
    @reservationNS.marshal_list_with(reservation_model)
    def get(self):
        reservations = Reservation.query.filter_by(status=0).all()
        return [{"id": r.id, "name": r.name} for r in reservations], 200


class ReservationStatusOne(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Бронь не найдена'})
    @reservationNS.marshal_list_with(reservation_model)
    def get(self):
        reservations = Reservation.query.filter_by(status=1).all()
        return [{"id": r.id, "name": r.name} for r in reservations], 200
