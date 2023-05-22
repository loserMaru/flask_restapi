from extensions import jwt


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return {'message': 'Не авторизован'}, 401


@jwt.expired_token_loader
def expired_token_callback(callback):
    return {'message': 'Токен истек'}, 401
