from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db
from app.user.models import User
from cerberus import Validator
from app.auth.validation import user_register_schema
from app.auth.service import (
    register_service,
    login_service
)


auth_blueprint = Blueprint('auth', __name__)

# Register
@auth_blueprint.route('/register', methods=['POST'])
def register():

    data = request.get_json()
    # print(data)

    valid = Validator(user_register_schema)

    if not valid.validate(data):
        return {'error' : valid.errors}, 409

    result, status = register_service(data)

    return jsonify(result), status


# Login
@auth_blueprint.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    result, status = login_service(data)

    return jsonify(result), status
    
# Protected Route
@auth_blueprint.route('/me', methods=['GET'])
@jwt_required()
def me():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify({
        'id' : user.id,
        'username' : user.username,
        'email' : user.email
    })

@auth_blueprint.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    current_user_id = get_jwt_identity()
    return({
        'status' : 'valid',
        'user_id' : current_user_id
    }), 200 