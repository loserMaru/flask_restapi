from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token
from flask_restx import Resource, reqparse, fields

from extensions import loginNS
from models import User

login_model = loginNS.model('Login', {
    'email': fields.String(required=True, default='string@gmail.com'),
    'password': fields.String(required=True)
})


@loginNS.route('/', methods=['POST'])
class Login(Resource):
    @loginNS.doc(security='jwt')
    @loginNS.expect(login_model)
    def post(self):
        # Получаем данные из запроса
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        # Получаем данные пользователя из базы данных
        user = User.query.filter_by(email=args['email']).first()

        # Проверяем пароль
        if user and check_password_hash(user.password, args['password']):
            # Генерируем JWT токен
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid email or password'}, 401
