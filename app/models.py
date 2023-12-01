from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Asigna un nombre a la tabla

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    image_url = db.Column(db.String(256))

    def __repr__(self):
        return f'<User {self.username}>'
