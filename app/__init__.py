from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.public import public_blueprint
    from app.auth import auth_blueprint
    from app.protected import protected_blueprint
    app.register_blueprint(public_blueprint, url_prefix='/public')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(protected_blueprint, url_prefix='/protected')

    return app
