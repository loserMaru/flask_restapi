from flask_restx import Api

# Namespaces
api = Api(title='Мой Столик', version='1.0',
          authorizations={
              'jwt': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization',
                  'description': 'JWT authorization, e.g. "Bearer {token}"'
              }
          })

loginNS = api.namespace('Login', description='Login operations', path='/login')
authNS = api.namespace('Auth', description='Authorization', path='/auth')
authWebNS = api.namespace('Web', description='Web auth', path='/web')
userNS = api.namespace('Users', description='Users operations', path='/user')
cardNS = api.namespace('Card', description='Card operations', path='/card')
profileNS = api.namespace('Profile', description='Profile operations', path='/profile')
restaurantNS = api.namespace('Restaurant', description='Restaurant operations', path='/restaurant')
reservationNS = api.namespace('Reservation', description='Reservation operations', path='/reservation')
favoriteNS = api.namespace('Favorite', description='Favorite operations', path='/favorite')
tableNS = api.namespace('Tables', description='Tables operations', path='/table')
uploadNS = api.namespace('Uploads', description='Uploads operations', path='/upload')
