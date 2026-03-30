from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.middleware.role_checker import role_required
import os 

from app.extensions import db
from app.user.models import User, Profile, EmployeeDetail
from app.user.service import (
    get_user_profile_service, 
    update_user_profile_service,
    get_all_users_service,
    create_user_service,
    update_user_service,
    delete_user_service
    )



user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    
    user_id = get_jwt_identity()

    result, status = get_user_profile_service(user_id)

    return jsonify(result), status



@user_blueprint.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    # data = request.json
    data = request.form.to_dict()
    image = request.files.get('profile_image')

    # print(data, image)
    
    result, status = update_user_profile_service(user_id, data, image )

    return jsonify(result), status



@user_blueprint.route('', methods=['GET'])
# @jwt_required()
# @role_required('user')
def get_users():

    result = get_all_users_service()

    return jsonify(result)


# CREATE USER
@user_blueprint.route('', methods=['POST'])
@role_required('member')
def create_user():

    data = request.json

    result, status = create_user_service(data)

    return jsonify(result), status


@user_blueprint.route('/<int:user_id>', methods=['PUT'])
@role_required('member')
def update_user(user_id):
    
    data = request.json

    result, status = update_user_service(user_id, data)

    return jsonify(result), status


@user_blueprint.route('/<int:user_id>' , methods=['DELETE'])
@role_required('member')
def delete_user(user_id):
    
    result, status = delete_user_service(user_id)

    return jsonify(result), status


@user_blueprint.route('/image', methods = ['POST'])
def upload_file():

    file = request.files.get('photo')

    if not file:
        return jsonify({
            'message' : 'no file uploaded'
        }), 400
    
    upload_folder = current_app.config['UPLOAD_FOLDER']

    filepath = os.path.join(upload_folder, file.filename)

    file.save(filepath)

    return jsonify({
        'message' : 'upload success',
        'path' : filepath
    })