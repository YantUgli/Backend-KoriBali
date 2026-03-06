from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extention import db
from app.models import User, Profile, EmployeeDetail


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
    
    profile_data= {
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
    }

    if user.role == 'member':
        profile_data['employee_detail'] = {
            'division' : user.employee_details.division if user.employee_details else None,
            'joined_date' : user.employee_details.joined_date if user.employee_details else None,
            'employee_id' : user.employee_details.employee_id if user.employee_details else None
        }
    
    return jsonify(profile_data) 


@user_blueprint.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    data = request.json
    print('ini data',data)
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message' : 'user not found'}), 404

    full_name = data.get('full_name')
    address = data.get('address')
    path_image_profile = data.get('path_image_profile')

    if not full_name:
        return jsonify({'message' : 'full name is required'})

    if not address:
        return jsonify({'message' : 'address is required'})


    profile = Profile.query.filter_by(user_id=user_id).first()


    if not profile:
        profile = Profile(user_id=user_id)
        db.session.add(profile)


    if path_image_profile:
        profile.path_image_profile = path_image_profile

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.number_phone = data.get('number_phone', user.number_phone)

    profile.full_name = full_name
    profile.address = address

    if user.role == 'member':
        employee_detail = EmployeeDetail.query.filter_by(user_id=user_id).first()

        if not employee_detail:
            employee_detail = EmployeeDetail(user_id=user_id)
            db.session.add(employee_detail)

        employee_detail.division = data.get('division', employee_detail.division)
        employee_detail.employee_id = data.get('employee_id', employee_detail.employee_id)
        employee_detail.joined_date = data.get('joined_date', employee_detail.joined_date)
    
    db.session.commit()

    return jsonify({'message' : 'Profile updated'})