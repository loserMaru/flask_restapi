from flask_restx import fields, Resource
from sqlalchemy.exc import IntegrityError
from flask import request

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
    def post(self):
        data = request.json
        favorite = Favorite(user_id=data.get('user_id'),
                            restaurant_id=data.get('restaurant_id'))
        print(favorite.to_dict())
        try:
            db.session.add(favorite)
            db.session.commit()
            return favorite_schema.dump(favorite), 201
        except IntegrityError as e:
            db.session.rollback()
            return {'message': 'Ошибка сохранения в базу данных. Неверные внешние ключи'}, 400


class FavoriteResource(Resource):
    @api.doc(responses={
        200: 'Успешный GET-запрос',
        404: 'Ресурс не найден'
    })
    @favoriteNS.marshal_with(favorite_model)
    def get(self, id):
        favorite = Favorite.query.get(id)
        if not favorite:
            favoriteNS.abort(404, 'Избранное не найдено')
        return favorite, 200

    @api.doc(responses={
        200: 'Успешный PUT-запрос',
        404: 'Ресурс не найден'
    })
    @favoriteNS.expect(favorite_model)
    def put(self, id):
        favorite = Favorite.query.filter_by(id=id).first()
        if not favorite:
            favoriteNS.abort(404, 'Избранное не найдено')
        favorite.user_id = favoriteNS.payload['user_id']
        favorite.restaurant_id = favoriteNS.payload['restaurant_id']
        try:
            db.session.commit()
            return favorite_schema.dump(favorite), 200
        except IntegrityError as e:
            db.session.rollback()
            return {'message': 'Ошибка сохранения в базу данных. Неверные внешние ключи'}, 400

    @api.doc(responses={
        200: 'Успешный DELETE-запрос, ресурс удален',
        404: 'Ресурс не найден'
    })
    def delete(self, id):
        favorite = Favorite.query.filter_by(id=id).first()
        if not favorite:
            favoriteNS.abort(404, 'Избранное не найдено')
        db.session.delete(favorite)
        db.session.commit()
        return {'msg': 'Удален из избранного'}, 200
