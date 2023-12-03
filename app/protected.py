from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flask_login import login_required

from app import db
from app.models import User, FailedLoginAttempt
from datetime import datetime

protected_blueprint = Blueprint('protected_blueprint', __name__)


@protected_blueprint.route('/attempts/all', methods=['GET'])
@jwt_required()
@login_required
def get_all_attempts():
    attempts = FailedLoginAttempt.query.all()
    return jsonify([attempt.to_dict() for attempt in attempts]), 200


@protected_blueprint.route('/attempts/<attempt_id>', methods=['GET'])
@jwt_required()
@login_required
def get_attempt_by_id(attempt_id):
    attempt = FailedLoginAttempt.query.get(attempt_id)
    return jsonify(attempt.to_dict()), 200


@protected_blueprint.route('/attempts/date/<date>', methods=['GET'])
@jwt_required()
@login_required
def get_attempts_by_date(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Formato de fecha inválido. Formato correcto: AAAA-MM-DD'}), 400

    attempts = FailedLoginAttempt.query.filter(
        db.func.date(FailedLoginAttempt.timestamp) == date_obj.date()
    ).all()

    return jsonify([attempt.to_dict() for attempt in attempts]), 200


@protected_blueprint.route('/attempts/date/<date>/from/<start_time>/to/<end_time>', methods=['GET'])
@jwt_required()
@login_required
def get_attempts_by_time_range(date, start_time, end_time):
    try:
        # Convierte fecha y horas de string a objetos datetime
        start_datetime = datetime.strptime(f"{date} {start_time}", '%Y-%m-%d %H-%M')
        end_datetime = datetime.strptime(f"{date} {end_time}", '%Y-%m-%d %H-%M')
    except ValueError:
        return jsonify({'message': 'Formato de fecha y hora inválido. Formato correcto: AAAA-MM-DD HH-MM'}), 400

    # Asegúrate de que el rango de tiempo es válido
    if end_datetime <= start_datetime:
        return jsonify({'message': 'La hora de finalización debe ser posterior a la hora de inicio.'}), 400

    # Filtra los intentos fallidos dentro del rango de tiempo dado
    attempts = FailedLoginAttempt.query.filter(
        db.func.date(FailedLoginAttempt.timestamp) == start_datetime.date(),
        FailedLoginAttempt.timestamp >= start_datetime,
        FailedLoginAttempt.timestamp <= end_datetime
    ).all()

    attempts_dict = [attempt.to_dict() for attempt in attempts]
    return jsonify(attempts_dict), 200


@protected_blueprint.route('/users/all', methods=['GET'])
@jwt_required()
@login_required
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@protected_blueprint.route('/users/<user_id>', methods=['GET'])
@jwt_required()
@login_required
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return jsonify(user.to_dict()), 200
