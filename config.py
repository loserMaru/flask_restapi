import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

    # JWT Token
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_HEADER_NAME = os.getenv('JWT_HEADER_NAME')
    JWT_TOKEN_LOCATION = 'headers'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Время истечения access token
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Время истечения refresh token
    FLASK_DEBUG = int(os.environ['FLASK_DEBUG'])
