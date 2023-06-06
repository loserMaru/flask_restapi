import sqlalchemy
from flask import request
from flask_restx import fields, Resource

from extensions import api, db, jwt_required_class
from extensions.flask_restx_extension import restaurantNS, categoryNS
from models import Restaurant, Favorite, Reservation, Category
from schemas import RestaurantSchema

category_model = categoryNS.model('Category', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True)
})

restaurant_model = restaurantNS.model('Restaurant', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'picture': fields.String(),
    'price': fields.Float(required=True),
    'star': fields.Float(required=True),
    'tableCount': fields.Integer(required=True),
    'category_id': fields.Nested(category_model)
})

restaurant_schema = RestaurantSchema()


@jwt_required_class
class RestaurantListResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @restaurantNS.marshal_list_with(restaurant_model)
    @restaurantNS.doc(security='jwt')
    def get(self):
        restaurants = Restaurant.query.all()
        return restaurants, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресторана',
        400: 'Некорректный запрос'
    })
    @restaurantNS.expect(restaurant_model)
    @restaurantNS.doc(security='jwt')
    def post(self):
        restaurant_data = restaurantNS.payload

        category_data = restaurant_data.pop('category_id', None)
        if category_data:
            category = Category.query.filter_by(name=category_data['name']).first()
            if category is None:
                category = Category(name=category_data['name'])
                db.session.add(category)
                db.session.commit()
            restaurant_data['category_id'] = category.id

        restaurant = Restaurant(**restaurant_data)
        db.session.add(restaurant)
        db.session.commit()

        return restaurant.to_dict(), 201


@jwt_required_class
class RestaurantResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресторан не найден'
    })
    @restaurantNS.marshal_with(restaurant_model)
    @restaurantNS.doc(security='jwt')
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
    @restaurantNS.doc(security='jwt')
    def put(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            restaurantNS.abort(404, 'Ресторан не найден')
        data = restaurant_schema.load(request.get_json())
        restaurant.name = data['name']
        restaurant.address = data['description']
        restaurant.picture = data['picture']
        restaurant.price = data['price']
        restaurant.star = data['star']
        restaurant.tableCount = data['tableCount']
        restaurant.cat_id = data['cat_id']
        db.session.commit()
        return restaurant_schema.dump(restaurant), 200

    @api.doc(responses={
        200: 'Успешный DELETE-запрос, ресторан удален',
        400: 'Некорректный запрос',
        404: 'Ресторан не найден'
    })
    @restaurantNS.doc(security='jwt')
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
