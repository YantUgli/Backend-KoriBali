from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extention import db
from app.models import User, Profile


user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            'message' : 'Profile not found'
        }),404
    
    return jsonify({
        'id' : user.id,
        'username' : user.username,
        'email' : user.email,
        'number_phone' : user.number_phone,
        'role' : user.role,
        'profile' : {
            'full_name' : user.profiles.full_name if user.profiles else None,
            'address' : user.profiles.address if user.profiles else None,
            'path_image_profile' : user.profiles.path_image_profile if user.profiles else None
        }
    }) 


@user_blueprint.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    data = request.json

    full_name = data.get('full_name')
    address = data.get('address')
    path_image_profile = data.get('path_image_profile')

    if not full_name:
        return jsonify({'message' : 'nama lengkap is required'})

    if not address:
        return jsonify({'message' : 'address is required'})


    profile = Profile.query.filter_by(user_id=user_id).first()


    if not profile:
        profile = Profile(user_id=user_id)
        db.session.add(profile)


    if path_image_profile:
        profile.path_image_profile = path_image_profile

    profile.full_name = full_name
    profile.address = address
    
    db.session.commit()

    return jsonify({'message' : 'Profile updated'})