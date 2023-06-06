from extensions import ratingNS, api, db, jwt_required_class
from models.models import Rating, User, Restaurant
from schemas import RatingSchema
from flask_restx import fields, Resource

rating_schema = RatingSchema()

rating_model = ratingNS.model('Rating', {
    'id': fields.Integer(readonly=True, description='Rating ID'),
    'rating': fields.Float(required=True, description='Rating value'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'restaurant_id': fields.Integer(required=True, description='Restaurant ID')
})


@jwt_required_class
class RatingResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @ratingNS.marshal_list_with(rating_model)
    @ratingNS.doc(security='jwt')
    def get(self):
        ratings = Rating.query.all()
        return ratings, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @ratingNS.expect(rating_model)
    @ratingNS.marshal_with(rating_model, code=201)
    @ratingNS.doc(security='jwt')
    def post(self):
        """Create a new rating"""
        data = api.payload
        user_id = data['user_id']
        restaurant_id = data['restaurant_id']
        rating_value = data['rating']

        # Check if the user and restaurant exist
        user = User.query.get(user_id)
        restaurant = Restaurant.query.get(restaurant_id)
        if not user or not restaurant:
            api.abort(404, 'User or restaurant not found')

        # Check if the rating already exists for the user and restaurant
        existing_rating = Rating.query.filter_by(user_id=user_id, restaurant_id=restaurant_id).first()
        if existing_rating:
            existing_rating.rating = rating_value
            db.session.commit()
            return existing_rating, 200

        rating = Rating(user_id=user_id, restaurant_id=restaurant_id, rating=rating_value)
        db.session.add(rating)
        db.session.commit()
        return rating, 201


@jwt_required_class
class RatingResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @ratingNS.doc(security='jwt')
    @ratingNS.marshal_with(rating_model)
    def get(self, id):
        rating = Rating.query.filter_by(id=id).first()
        if not rating:
            api.abort(404, 'rating not found')
        return rating, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @ratingNS.doc(security='jwt')
    @ratingNS.expect(rating_model)
    def put(self, id):
        rating = Rating.query.filter_by(id=id).first()
        if not rating:
            api.abort(404, 'Rating not found')
        for key, value in ratingNS.payload.items():
            setattr(rating, key, value)
        db.session.commit()
        return rating_schema.dump(rating), 200

    @api.doc(responses={
        204: 'Успешный DELETE-запрос, ресурс удален',
        404: 'Ресурс не найден'
    })
    @ratingNS.doc(security='jwt')
    def delete(self, id):
        """Delete a rating by ID"""
        rating = Rating.query.get(id)
        if not rating:
            api.abort(404, 'Rating not found')

        db.session.delete(rating)
        db.session.commit()
        return {'result': 'success'}, 204


@jwt_required_class
class AverageRatingResource(Resource):
    @ratingNS.doc(params={'restaurant_id': 'Restaurant ID'})
    @ratingNS.doc(security='jwt')
    def get(self, restaurant_id):
        """Get the average rating for a restaurant by ID"""
        average_rating = db.session.query(db.func.avg(Rating.rating)).filter_by(restaurant_id=restaurant_id).scalar()
        if average_rating is None:
            api.abort(404, 'Restaurant not found')

        return {'average_rating': average_rating}
