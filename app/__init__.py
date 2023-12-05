from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

from app.mqtt_client import configure_mqtt
from config import Config
from app.machine import initialize_photo_process
import threading

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    configure_mqtt(app)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    from app.models import User

    # Inicializa el proceso de captura de fotos
    photo_process = threading.Thread(target=initialize_photo_process, daemon=True)
    photo_process.start()

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
