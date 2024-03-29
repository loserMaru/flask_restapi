from sqlalchemy import func
from sqlalchemy.orm import backref

from extensions.database_extension import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=True)

    # Добавляем отношение к ресторану, если это необходимо
    restaurant = db.relationship('Restaurant', backref='moderators', foreign_keys=[restaurant_id])

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'restaurant_id': self.restaurant_id
        }


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True)
    cardNumber = db.Column(db.String(45), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='cards')

    def to_dict(self):
        return {
            'id': self.id,
            'cardNumber': self.cardNumber,
            'user_id': self.user_id
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    user = db.relationship('User', backref=backref('favorites', cascade='all, delete'))
    restaurant = db.relationship('Restaurant', backref=backref('favorites', cascade='all, delete'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id
        }


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255))
    phone = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='profiles')

    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'picture': self.picture,
            'phone': self.phone,
            'user_id': self.user_id
        }


class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    number = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    status = db.Column(db.String(45), nullable=False)
    picture = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    user = db.relationship('User', backref=backref('reservations', cascade='all, delete'))
    restaurant = db.relationship('Restaurant', backref=backref('reservations', cascade='all, delete'))

    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day,
            "time": self.time.strftime("%H:%M:%S"),
            'number': self.number,
            'name': self.name,
            'price': self.price,
            'status': self.status,
            'picture': self.picture,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id
        }


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255))
    price = db.Column(db.Float(), nullable=False)
    star = db.Column(db.Float(), nullable=False)
    tableCount = db.Column(db.Integer(), nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', backref='restaurants')

    def calculate_average_rating(self):
        average_rating = db.session.query(func.avg(Rating.rating)).filter_by(restaurant_id=self.id).scalar()
        return average_rating if average_rating is not None else 0.0

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture': self.picture,
            'price': self.price,
            'star': self.star,
            'tableCount': self.tableCount,
            'category_id': self.category_id,
        }


class Tables(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255), nullable=False)
    seat = db.Column(db.String(45))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    restaurant = db.relationship('Restaurant', foreign_keys=[restaurant_id])

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'seat': self.seat,
            'restaurant_id': self.restaurant_id
        }


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    picture = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'picture': self.picture
        }


class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    user = db.relationship('User', backref='ratings')
    restaurant = db.relationship('Restaurant', backref='ratings')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id,
            'rating': self.rating
        }
