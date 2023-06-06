from flask_jwt_extended import JWTManager, jwt_required

jwt = JWTManager()


def jwt_required_class(cls):
    methods = cls.__dict__.copy()

    for name, method in methods.items():
        if callable(method) and not name.startswith("__"):
            setattr(cls, name, jwt_required()(method))

    return cls
