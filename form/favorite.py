from flask_restx import fields, Resource

from extensions import api, db
from extensions.flask_restx_extension import favoriteNS
from models.models import Favorite

favorite_model = favoriteNS.model('Favorite', {
    'id': fields.Integer(readonly=True),
    'user_id': fields.Integer,
    'restaurant_id': fields.Integer,
})


class FavoriteResourceList(Resource):
    @favoriteNS.marshal_list_with(favorite_model)
    def get(self):
        favorites = Favorite.query.all()
        return favorites

    @favoriteNS.expect(favorite_model)
    def post(self):
        favorite = Favorite(**favoriteNS.payload)
        db.session.add(favorite)
        db.session.commit()
        return {'result': 'success'}


class FavoriteResource(Resource):
    @favoriteNS.marshal_with(favorite_model)
    def get(self, favorite_id):
        favorite = Favorite.query.filter_by(id=favorite_id).first()
        if not favorite:
            favoriteNS.abort(404, 'Favorite not found')
        return favorite

    @favoriteNS.expect(favorite_model)
    def put(self, favorite_id):
        favorite = Favorite.query.filter_by(id=favorite_id).first()
        for key, value in favoriteNS.payload.items():
            setattr(favorite, key, value)
        db.session.commit()
        return {'result': 'success'}

    def delete(self, favorite_id):
        favorite = Favorite.query.filter_by(id=favorite_id).first()
        if not favorite:
            favoriteNS.abort(404, 'Favorite not found')
        db.session.delete(favorite)
        db.session.commit()
        return {'result': 'success'}
