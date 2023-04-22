from flask_restx import fields, Resource

from extensions import api, db
from extensions.flask_restx_extension import reservationNS
from models.models import Reservation

reservation_model = reservationNS.model('Reservation', {
    'id': fields.Integer(readonly=True),
    'day': fields.DateTime,
    'time': fields.String,
    'number': fields.String,
    'name': fields.String,
    'user_id': fields.Integer,
})


# Определение ресурса списка всех Reservation
class ReservationListResource(Resource):
    @reservationNS.marshal_list_with(reservation_model)
    def get(self):
        reservations = Reservation.query.all()
        return reservations

    @reservationNS.expect(reservation_model)
    def post(self):
        reservation = Reservation(**reservationNS.payload)
        db.session.add(reservation)
        db.session.commit()
        return {'result': 'success'}


# Определение ресурса для одного Reservation
class ReservationResource(Resource):
    @reservationNS.marshal_with(reservation_model)
    def get(self, reservation_id):
        reservation = Reservation.query.filter_by(id=reservation_id).first()
        if not reservation:
            reservationNS.abort(404, 'Reservation not found')
        return reservation

    @reservationNS.expect(reservation_model)
    def put(self, reservation_id):
        reservation = Reservation.query.filter_by(id=reservation_id).first()
        if not reservation:
            reservationNS.abort(404, 'Reservation not found')
        reservation.day = reservationNS.payload['day']
        reservation.time = reservationNS.payload['time']
        reservation.number = reservationNS.payload['number']
        reservation.name = reservationNS.payload['name']
        reservation.user_id = reservationNS.payload['user_id']
        db.session.commit()
        return {'result': 'success'}

    def delete(self, reservation_id):
        reservation = Reservation.query.filter_by(id=reservation_id).first()
        if not reservation:
            reservationNS.abort(404, 'Reservation not found')
        db.session.delete(reservation)
        db.session.commit()
        return {'result': 'success'}
