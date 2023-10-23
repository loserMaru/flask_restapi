import sqlalchemy
from flask import request
from flask_restx import fields, Resource

from extensions import api, db, jwt_required_class
from extensions.flask_restx_extension import restaurantNS, categoryNS
from models import Restaurant, Favorite, Reservation, Category
from schemas import RestaurantSchema

restaurant_model = restaurantNS.model('Restaurant', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'picture': fields.String(),
    'price': fields.Float(required=True),
    'star': fields.Float(required=True),
    'tableCount': fields.Integer(required=True),
    'category_id': fields.Integer(required=True)
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
        """Get a list of restaurants"""
        restaurants = Restaurant.query.all()
        return restaurants, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресторана',
        400: 'Некорректный запрос'
    })
    @restaurantNS.expect(restaurant_model)
    @restaurantNS.doc(security='jwt')
    def post(self):
        """Create new restaurant"""
        restaurant_data = restaurantNS.payload

        # Проверка, что category_id существует в базе данных
        category_id = restaurant_data.get('category_id')
        category = Category.query.get(category_id)
        if category is None:
            restaurantNS.abort(400, 'Недопустимый category_id. Категория не существует.')

        # Если category_id существует, создаем новый ресторан
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
        """Get restaurant by ID"""
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
        """Edit restaurant by ID"""
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            restaurantNS.abort(404, 'Ресторан не найден')

        data = restaurant_schema.load(request.get_json())

        # Проверка, что category_id существует в базе данных
        category_id = data['category_id']
        category = Category.query.get(category_id)
        if category is None:
            restaurantNS.abort(400, 'Недопустимый category_id. Категория не существует.')

        # Если category_id существует, обновляем остальные поля
        restaurant.name = data['name']
        restaurant.address = data['description']
        restaurant.picture = data['picture']
        restaurant.price = data['price']
        restaurant.star = data['star']
        restaurant.tableCount = data['tableCount']
        restaurant.category_id = category_id  # Устанавливаем category_id после проверки
        db.session.commit()

        return restaurant_schema.dump(restaurant), 200

    @api.doc(responses={
        200: 'Успешный DELETE-запрос, категория удалена',
        400: 'Некорректный запрос',
        404: 'Ресторан не найден'
    })
    @restaurantNS.doc(security='jwt')
    def delete(self, id):
        """Delete restaurant by ID"""
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            restaurantNS.abort(404, 'Ресторан не найден')
        try:
            db.session.delete(restaurant)
            db.session.commit()
            return {'msg': 'Ресторан удален успешно'}, 200
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return {'msg': 'Ошибка.'}, 400
