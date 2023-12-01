from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_login import login_required

test_blueprint = Blueprint('test_blueprint', __name__)


@test_blueprint.route('/ruta-test', methods=['GET'])
@jwt_required()
@login_required
def test():
    return 'Esta es una ruta de prueba', 200
