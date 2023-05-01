from extensions.database_extension import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role
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
    user = db.relationship('User', backref='favorites')
    restaurant = db.relationship('Restaurant', backref='favorites')

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    user = db.relationship('User', backref='reservations')
    restaurant = db.relationship('Restaurant', backref='reservations')

    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day,
            'time': self.time,
            'number': self.number,
            'name': self.name,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id
        }


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255))
    hidden = db.Column(db.Boolean, nullable=False)
    restaurantcol = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'picture': self.picture,
            'hidden': self.hidden,
            'restaurantcol': self.restaurantcol
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
