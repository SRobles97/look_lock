from io import BytesIO

import face_recognition
import requests
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, FailedLoginAttempt

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/sign-up', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    username = data['username']
    password = generate_password_hash(data['password'])
    image_url = data['image_url']

    # Verificar si el email ya está en uso
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'El correo ya está en uso'}), 400

    # Verificar si el nombre de usuario ya está en uso
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'El nombre de usuario ya está en uso'}), 400

    # Crear un nuevo usuario
    new_user = User(
        email=email,
        username=username,
        password_hash=password,
        image_url=image_url
    )

    # Agregar el usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201


@auth_blueprint.route('/sign-in', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)  # Inicia sesión con Flask-Login
        access_token = create_access_token(identity=username)  # Crea el token JWT
        return jsonify({'message': 'Inicio de sesión exitoso', 'access_token': access_token}), 200

    return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401


@auth_blueprint.route('/sign-in/face', methods=['POST'])
def login_with_image():
    image_url = request.json.get('image_url')

    if not image_url:
        return jsonify({'message': 'No se ha enviado ninguna imagen'}), 400

    response = requests.get(image_url)
    sent_image = face_recognition.load_image_file(BytesIO(response.content))

    face_found = False

    for user in User.query.all():
        user_image_url = user.image_url
        response = requests.get(user_image_url)
        user_image = face_recognition.load_image_file(BytesIO(response.content))

        try:
            sent_encoding = face_recognition.face_encodings(sent_image)[0]
            user_encoding = face_recognition.face_encodings(user_image)[0]
            results = face_recognition.compare_faces([user_encoding], sent_encoding)
            if results[0]:
                face_found = True
                access_token = create_access_token(identity=user.id)
                return jsonify({'message': 'Inicio de sesión exitoso', 'access_token': access_token}), 200
        except IndexError:
            continue

    if not face_found:
        # Crear un registro de intento fallido
        failed_attempt = FailedLoginAttempt(attempted_url=image_url)
        db.session.add(failed_attempt)
        db.session.commit()
        return jsonify({'message': 'Reconocimiento facial no coincidente'}), 401
