from flask_restx import fields, Resource

from extensions import api, db
from extensions.flask_restx_extension import restaurantNS
from models.models import Restaurant

restaurant_model = restaurantNS.model('Restaurant', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'address': fields.String(required=True),
    'picture': fields.String(),
    'hidden': fields.Boolean(required=True),
    'user_id': fields.Integer(required=True),
    'restaurantcol': fields.String(),
})


class RestaurantListResource(Resource):
    @restaurantNS.marshal_list_with(restaurant_model)
    def get(self):
        restaurants = Restaurant.query.all()
        return restaurants

    @restaurantNS.expect(restaurant_model)
    def post(self):
        restaurant = Restaurant(**restaurantNS.payload)
        db.session.add(restaurant)
        db.session.commit()
        return {'result': 'success'}


class RestaurantResource(Resource):
    @restaurantNS.marshal_with(restaurant_model)
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            restaurantNS.abort(404, 'Restaurant not found')
        return restaurant

    @restaurantNS.expect(restaurant_model)
    def put(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            restaurantNS.abort(404, 'Restaurant not found')
        for key, value in restaurantNS.payload.items():
            setattr(restaurant, key, value)
        db.session.commit()
        return {'result': 'success'}

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            restaurantNS.abort(404, 'Restaurant not found')
        db.session.delete(restaurant)
        db.session.commit()
        return {'result': 'success'}
