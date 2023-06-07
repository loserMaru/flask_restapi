from datetime import timedelta

from flask import Flask
from flask_cors import CORS

from extensions import db, api, ma, uploadNS, jwt, loginNS, ratingNS
from extensions import favoriteNS, profileNS, reservationNS, restaurantNS, tableNS, cardNS, userNS, authNS, authWebNS
from extensions import categoryNS
from form import CardResource, CardResourceList, CategoryResourceList, CategoryResource, RatingResourceList, \
    RatingResource, TokenRefresh
from form import FavoriteResource, FavoriteResourceList
from form import ProfileResource, ProfileResourceList, UploadProfilePic
from form import ReservationResource, ReservationListResource
from form import RestaurantListResource, RestaurantResource
from form import TableResource, TableResourceList
from form import UserResource, UserResourceList, UserEmailResource
from form import AuthResource
from form import WebAuthResource, ReservationStatusOne, ReservationStatusZero
from form import UploadImage
from form.rating import AverageRatingResource


def register_resource(api):
    # Refresh Token
    authNS.add_resource(TokenRefresh, '/refresh')

    # Auth
    authNS.add_resource(AuthResource, '')
    api.add_namespace(authNS, path='/auth')

    # Web Auth
    authWebNS.add_resource(WebAuthResource, '/auth')
    authWebNS.add_resource(ReservationStatusOne, '/one')
    authWebNS.add_resource(ReservationStatusZero, '/zero')
    api.add_namespace(authWebNS, path='/web')

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
    profileNS.add_resource(UploadProfilePic, '/upload/<int:id>')
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

    # Categories
    categoryNS.add_resource(CategoryResourceList, '')
    categoryNS.add_resource(CategoryResource, '/<int:id>')
    api.add_namespace(categoryNS, path='/category')

    # Ratings
    ratingNS.add_resource(RatingResourceList, '')
    ratingNS.add_resource(RatingResource, '/<int:id>')
    ratingNS.add_resource(AverageRatingResource, '/average/<int:restaurant_id>')
    api.add_namespace(ratingNS, path='/rating')


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
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Время истечения access token
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # Время истечения refresh token

    # Inits
    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app, origins='*')
    register_resource(api)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
