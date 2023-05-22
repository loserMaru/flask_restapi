import sqlalchemy
from flask import request
from flask_restx import fields, Resource

from extensions import api, db
from extensions.flask_restx_extension import restaurantNS
from models import Restaurant, Favorite, Reservation
from schemas import RestaurantSchema

restaurant_model = restaurantNS.model('Restaurant', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'address': fields.String(required=True),
    'picture': fields.String(),
    'price': fields.Float(required=True),
    'hidden': fields.Boolean(required=True, default=False)
})

restaurant_schema = RestaurantSchema()


class RestaurantListResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @restaurantNS.marshal_list_with(restaurant_model)
    def get(self):
        restaurants = Restaurant.query.all()
        return restaurants, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресторана',
        400: 'Некорректный запрос'
    })
    @restaurantNS.expect(restaurant_model)
    def post(self):
        restaurant = Restaurant(**restaurantNS.payload)
        db.session.add(restaurant)
        db.session.commit()
        return restaurant.to_dict(), 201


class RestaurantResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресторан не найден'
    })
    @restaurantNS.marshal_with(restaurant_model)
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            restaurantNS.abort(404, 'Ресторан не найден')
        return restaurant, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресторан не найден'
    })
    @restaurantNS.expect(restaurant_model)
    def put(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            restaurantNS.abort(404, 'Ресторан не найден')
        data = restaurant_schema.load(request.get_json())
        restaurant.name = data['name']
        restaurant.address = data['address']
        restaurant.picture = data['picture']
        restaurant.price = data['price']
        restaurant.hidden = data['hidden']
        db.session.commit()
        return restaurant_schema.dump(restaurant), 200

    @api.doc(responses={
        200: 'Успешный DELETE-запрос, ресторан удален',
        400: 'Некорректный запрос',
        404: 'Ресторан не найден'
    })
    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            restaurantNS.abort(404, 'Ресторан не найден')
        favorites = Favorite.query.filter_by(restaurant_id=restaurant.id).all()
        for favorite in favorites:
            db.session.delete(favorite)
        reservations = Reservation.query.filter_by(restaurant_id=restaurant.id).all()
        for reservation in reservations:
            db.session.delete(reservation)
        try:
            db.session.delete(restaurant)
            db.session.commit()
            return {'msg': 'Ресторан удален успешно'}, 200
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка.'}, 400
