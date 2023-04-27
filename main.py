from flask import Flask

from extensions import db, api, ma
from extensions.flask_restx_extension import favoriteNS, profileNS, reservationNS, restaurantNS, tableNS
from form.restaurant import RestaurantListResource, RestaurantResource
from form.user import UserResource, UserResourceList, userNS
from form.card import CardResource, CardResourceList, cardNS
from form.favorite import FavoriteResource, FavoriteResourceList
from form.profile import ProfileResource, ProfileResourceList
from form.tables import TableResource, TableResourceList
from form.reservation import ReservationResource, ReservationListResource


def register_resourse(api):
    #  User
    userNS.add_resource(UserResourceList, '')
    userNS.add_resource(UserResource, '/<int:id>')
    api.add_namespace(userNS, path='/user')

    # Card
    cardNS.add_resource(CardResourceList, '')
    cardNS.add_resource(CardResource, '/<int:id>')
    api.add_namespace(cardNS, path='/card')

    # Profile
    profileNS.add_resource(ProfileResourceList, '')
    profileNS.add_resource(ProfileResource, '/<int:id>')
    api.add_namespace(profileNS, path='/profile')

    # Reservation
    reservationNS.add_resource(ReservationListResource, '')
    reservationNS.add_resource(ReservationResource, '/<int:id>')
    api.add_namespace(reservationNS, path='/reservation')

    # Restaurant
    restaurantNS.add_resource(RestaurantListResource, '')
    restaurantNS.add_resource(RestaurantResource, '/<int:id>')
    api.add_namespace(restaurantNS, path='/restaurant')

    # Favorite
    favoriteNS.add_resource(FavoriteResourceList, '')
    favoriteNS.add_resource(FavoriteResource, '/<int:id>')
    api.add_namespace(favoriteNS, path='/favorite')

    # Tables
    tableNS.add_resource(TableResourceList, '')
    tableNS.add_resource(TableResource, '/<int:id>')
    api.add_namespace(tableNS, path='/table')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['JSON_AS_ASCII'] = False
    app.config['ERROR_INCLUDE_MESSAGE'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4863826M@localhost/mystolik'
    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    register_resourse(api)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
