from flask import Blueprint, jsonify

public_blueprint = Blueprint('public_blueprint', __name__)


@public_blueprint.route('/check-connection', methods=['GET'])
def check_connection():
    return jsonify({'message': 'Conexión exitosa'}), 200
