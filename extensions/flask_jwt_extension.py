from flask_jwt_extended import JWTManager, jwt_required

from config import Config

jwt = JWTManager()


def jwt_required_class(cls):
    methods = cls.__dict__.copy()

    if not Config.FLASK_DEBUG:
        for name, method in methods.items():
            if callable(method) and not name.startswith("__"):
                setattr(cls, name, jwt_required()(method))

    return cls
