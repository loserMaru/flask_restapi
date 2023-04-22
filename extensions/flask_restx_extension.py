from flask_restx import Api

api = Api(default='Мой столик', default_label='All operations')
userNS = api.namespace('Users', description='Users operations')
cardNS = api.namespace('Card', description='Card operations')
profileNS = api.namespace('Profile', description='Profile operations')
restaurantNS = api.namespace('Restaurant', description='Restaurant operations')
reservationNS = api.namespace('Reservation', description='Reservation operations')
favoriteNS = api.namespace('Favorite', description='Favorite operations')
tableNS = api.namespace('Tables', description='Tables operations')
