from datetime import datetime

from flask import request, jsonify
from flask_restx import Resource, fields, ValidationError

from extensions import api, db
from extensions.flask_restx_extension import reservationNS
from models import Reservation
from schemas import ReservationSchema

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)

reservation_model = reservationNS.model('Reservation', {
    'id': fields.Integer(readonly=True),
    'day': fields.Date(required=True),
    'time': fields.String(description='Time in HH:MM format', pattern='^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'),
    'number': fields.String(required=True),
    'name': fields.String(required=True),
    'user_id': fields.Integer,
    'restaurant_id': fields.Integer,
})


# Определение ресурса списка всех Reservation
class ReservationListResource(Resource):
    @api.doc(responses={200: 'Success', 404: 'Reservation not found'})
    @reservationNS.marshal_list_with(reservation_model)
    def get(self):
        reservations = Reservation.query.all()
        return reservations, 200

    @api.doc(responses={201: 'Created', 400: 'Invalid data'})
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
        db.session.add(reservation)
        db.session.commit()
        return reservation_schema.dump(reservation), 201


# Определение ресурса для одного Reservation
class ReservationResource(Resource):
    @api.doc(responses={200: 'Success', 404: 'Reservation not found'})
    @reservationNS.marshal_with(reservation_model)
    def get(self, id):
        reservation = Reservation.query.filter_by(id=id).first()
        if not reservation:
            reservationNS.abort(404, 'Reservation not found')
        return reservation, 200

    @api.doc(responses={200: 'Success', 400: 'Invalid data', 404: 'Reservation not found'})
    @reservationNS.expect(reservation_model)
    def put(self, id):
        reservation = Reservation.query.filter_by(id=id).first()
        if not reservation:
            reservationNS.abort(404, 'Reservation not found')

        try:
            reservation_data = reservation_schema.load(request.json, partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400

        for field, value in reservation_data.items():
            setattr(reservation, field, value)

        db.session.commit()
        return reservation_schema.dump(reservation), 200

    @api.doc(responses={200: 'Success', 404: 'Reservation not found'})
    def delete(self, id):
        reservation = Reservation.query.filter_by(id=id).first()
        if not reservation:
            reservationNS.abort(404, 'Reservation not found')
        db.session.delete(reservation)
        db.session.commit()
        return {'result': 'success'}, 200
