from flask import Blueprint, jsonify

from app import db
from app.models import User, FailedLoginAttempt
from datetime import datetime

machine_blueprint = Blueprint('machine_blueprint', __name__)


def tomar_foto():
    pass


@machine_blueprint.route('/take-photo', methods=['GET'])
def take_photo_endpoint():
    take_photo()
    return "Foto tomada", 200
