from flask_restx import fields, Resource

from extensions import api, db
from extensions.flask_restx_extension import favoriteNS
from models import Favorite
from schemas import FavoriteSchema

favorite_schema = FavoriteSchema()

favorite_model = favoriteNS.model('Favorite', {
    'id': fields.Integer(readonly=True),
    'user_id': fields.Integer,
    'restaurant_id': fields.Integer,
})


class FavoriteResourceList(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        400: 'Некорректный запрос'
    })
    @favoriteNS.marshal_list_with(favorite_model)
    def get(self):
        favorites = Favorite.query.all()
        return favorites, 200

    @api.doc(responses={
        201: 'Успешный POST-запрос, создание нового ресурса',
        400: 'Некорректный запрос'
    })
    @favoriteNS.expect(favorite_model)
    @favoriteNS.marshal_with(favorite_model, code=201)
    def post(self):
        favorite = Favorite(user_id=favoriteNS.payload.get('user_id'),
                            restaurant_id=favoriteNS.payload.get('restaurant_id'))
        db.session.add(favorite)
        db.session.commit()
        return favorite.to_dict(), 201


class FavoriteResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @favoriteNS.marshal_with(favorite_model)
    def get(self, id):
        favorite = Favorite.query.get(id)
        if not favorite:
            favoriteNS.abort(404, 'Favorite not found')
        return favorite, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @favoriteNS.expect(favorite_model)
    def put(self, id):
        favorite = Favorite.query.filter_by(id=id).first()
        if not favorite:
            favoriteNS.abort(404, 'Favorite not found')
        favorite.user_id = favoriteNS.payload['user_id']
        favorite.restaurant_id = favoriteNS.payload['restaurant_id']
        db.session.commit()
        return favorite_schema.dump(favorite), 200

    @api.doc(responses={
        204: 'Успешный DELETE-запрос, ресурс удален',
        404: 'Ресурс не найден'
    })
    def delete(self, id):
        favorite = Favorite.query.filter_by(id=id).first()
        if not favorite:
            favoriteNS.abort(404, 'Favorite not found')
        db.session.delete(favorite)
        db.session.commit()
        return {'result': 'success'}, 204
