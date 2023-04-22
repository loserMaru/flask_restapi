from flask import Flask

from extensions import db, api
from extensions.flask_restx_extension import favoriteNS, profileNS, reservationNS, restaurantNS, tableNS
from form.restaurant import RestaurantListResource, RestaurantResource
from form.user import UserResource, UserResourceList, userNS
from form.card import CardResource, CardResourceList, cardNS
from form.favorite import FavoriteResource, FavoriteResourceList
from form.profile import ProfileResource, ProfileResourceList
from form.tables import TableResource, TableResourceList


def register_resourse(api):
    #  User
    userNS.add_resource(UserResourceList, '/user')
    userNS.add_resource(UserResource, '/user/<int:id>')
    api.add_namespace(userNS)

    # Card
    cardNS.add_resource(CardResourceList, '/card')
    cardNS.add_resource(CardResource, '/card/<int:id>')
    api.add_namespace(cardNS)

    # Profile
    profileNS.add_resource(ProfileResourceList, '/profile')
    profileNS.add_resource(ProfileResource, '/profile/<int:id>')
    api.add_namespace(profileNS)

    # Reservation
    reservationNS.add_resource(ProfileResourceList, '/reservation')
    reservationNS.add_resource(ProfileResource, '/reservation/<int:id>')
    api.add_namespace(reservationNS)

    # Restaurant
    restaurantNS.add_resource(RestaurantListResource, '/restaurant')
    restaurantNS.add_resource(RestaurantResource, '/restaurant/<int:id>')

    # Favorite
    favoriteNS.add_resource(FavoriteResourceList, '/favorite')
    favoriteNS.add_resource(FavoriteResource, '/favorite/<int:id>')
    api.add_namespace(favoriteNS)

    # Tables
    tableNS.add_resource(TableResourceList, '/table')
    tableNS.add_resource(TableResource, '/table/<int:id>')
    api.add_namespace(tableNS)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['JSON_AS_ASCII'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4863826M@localhost/mystolik'
    db.init_app(app)
    api.init_app(app)
    register_resourse(api)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
