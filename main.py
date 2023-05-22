from flask import Flask

from extensions import db, api, ma, uploadNS, jwt
from extensions import favoriteNS, profileNS, reservationNS, restaurantNS, tableNS, cardNS, userNS
# from extensions.flask_uploads_extension import UPLOAD_FOLDER
from form import CardResource, CardResourceList
from form import FavoriteResource, FavoriteResourceList
from form import ProfileResource, ProfileResourceList
from form import ReservationResource, ReservationListResource
from form import RestaurantListResource, RestaurantResource
from form import TableResource, TableResourceList
from form import UserResource, UserResourceList
from form.auth import UserLogin
from form.uploads import UploadImage


def register_resource(api):
    #  User
    userNS.add_resource(UserResourceList, '')
    userNS.add_resource(UserResource, '/<int:id>')
    userNS.add_resource(UserLogin, '/login')
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

    # Uploads
    uploadNS.add_resource(UploadImage, '')
    api.add_namespace(uploadNS, path='/upload')


def create_app():
    # App configs
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['JSON_AS_ASCII'] = False
    app.config['ERROR_INCLUDE_MESSAGE'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # Upload files
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4863826M@localhost/mystolik'

    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    # Inits
    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    register_resource(api)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
