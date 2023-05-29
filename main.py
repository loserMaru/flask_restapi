from flask import Flask

from extensions import db, api, ma, uploadNS, jwt, loginNS
from extensions import favoriteNS, profileNS, reservationNS, restaurantNS, tableNS, cardNS, userNS
from extensions.flask_restx_extension import authNS, authWebNS
# from extensions.flask_uploads_extension import UPLOAD_FOLDER
from form import CardResource, CardResourceList
from form import FavoriteResource, FavoriteResourceList
from form import ProfileResource, ProfileResourceList
from form import ReservationResource, ReservationListResource
from form import RestaurantListResource, RestaurantResource
from form import TableResource, TableResourceList
from form import UserResource, UserResourceList
from form.auth import AuthResource
from form.authweb import WebAuthResource, ReservationStatusOne, ReservationStatusZero
from form.uploads import UploadImage
from form.user import UserEmailResource


def register_resource(api):
    # Auth
    authNS.add_resource(AuthResource, '')
    api.add_namespace(authNS, path='/auth')

    # Web Auth
    authWebNS.add_resource(WebAuthResource, '/auth')
    authWebNS.add_resource(ReservationStatusOne, '/one')
    authWebNS.add_resource(ReservationStatusZero, '/zero')
    api.add_namespace(authWebNS, path='/web')

    # Login
    # loginNS.add_resource(Login, '')
    # api.add_namespace(loginNS, path='/login')

    #  User
    userNS.add_resource(UserResourceList, '')
    userNS.add_resource(UserResource, '/<int:id>')
    userNS.add_resource(UserEmailResource, '/<string:email>')
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
    # DB_USERNAME = 'loserMaru'
    # DB_PASSWORD = '4863826M'
    # DB_HOST = 'loserMaru.mysql.pythonanywhere-services.com'
    # DB_NAME = 'loserMaru$mytable'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:4863826M@localhost/mystolik'

    # JWT Token
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

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
