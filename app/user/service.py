from datetime import datetime
from app.extensions import db
from app.models import User, Profile, EmployeeDetail

def get_user_profile_service(user_id):

    user = User.query.get(user_id)

    if not user:
        return{
            'message' : 'Profile not found'
        }, 404
    
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
        detail = user.employee_details
        profile_data['employee_detail'] = {
            'division' : detail.division if user.employee_details else None,
            'joined_date' : detail.joined_date.isoformat() if user.employee_details else None,
            'employee_id' : detail.employee_id if user.employee_details else None
        }
    
    return profile_data, 200



def update_user_profile_service(user_id, data): 

    user = User.query.get(user_id)

    if not user:
        return {'message' : 'user not found'}, 404
    
    full_name = data.get('full_name')
    address = data.get('address')
    path_image_profile = data.get('path_image_profile')

    if not full_name:
        return {'message' : 'full name is required'}, 400

    if not address:
        return {'message' : 'address is required'}, 400


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
        joined_date = data.get('joined_date', employee_detail.joined_date)

        if joined_date:
            try:
                # Mengubah "2024-05-20T10:30:00" menjadi objek date
                # .fromisoformat menangani format T dengan sangat baik
                dt_obj = datetime.fromisoformat(joined_date)
                employee_detail.joined_date = dt_obj.date()
            except ValueError:
                return {'message': 'Format tanggal harus YYYY-MM-DDTHH:MM:SS'}, 400
    
    db.session.commit()

    return {'message' : 'Profile updated'}, 200


def get_all_users_service():
    
    users = User.query.all()

    output = []

    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'profile' : {
            'full_name' : user.profiles.full_name if user.profiles else None,
            'address' : user.profiles.address if user.profiles else None,
            'path_image_profile' : user.profiles.path_image_profile if user.profiles else None
        },
            
            'employee_detail': {
                'division': user.employee_details.division if user.employee_details else None,
                'employee_id': user.employee_details.employee_id if user.employee_details else None
            } if user.role == 'member' else None
        }
        output.append(user_data)

    return output


def create_user_service(data): 
    username = data.get('username')
    email = data.get('email')
    number_phone = data.get('number_phone')
    password = data.get('password')

    request_body = User(
        username = username,
        email =email,
        number_phone = number_phone,
    )

    try:
        request_body.set_password(password)
        db.session.add(request_body)
        db.session.commit()
        return{
            'message' : 'user create successfully',
            'data' : {
                'id' : request_body.id,
                'username' : request_body.username,
                'email' : request_body.email
            }            
        }, 201

    except Exception as e:
        db.session.rollback
        return{
            'message' : 'terjadi kesalahan saat menyimpan data user',
            'error' : str(e)
        }, 400



def update_user_service(user_id, data):
    
    user = User.query.get(user_id)

    if not user:
        return {
            'message' : 'User not found'
        }, 404
    
    full_name = data.get('full_name')
    address = data.get('address')
    path_image_profile = data.get('path_image_profile')

    # KONDISI KALAU FULL NAME DAN ADDRESS REQUIRED
    # if not full_name:
    #     return {'message' : 'full name is required'}, 400

    # if not address:
    #     return {'message' : 'address is required'}, 400


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
        joined_date = data.get('joined_date')

        if joined_date:
            try:
                
                dt_obj = datetime.fromisoformat(joined_date)
                employee_detail.joined_date = dt_obj.date()
            except ValueError:
                return {'message': 'Format tanggal harus YYYY-MM-DDTHH:MM:SS'}, 400
    
    db.session.commit()

    return {'message' : 'Profile updated'}, 200



def delete_user_service(user_id):
    user = User.query.get(user_id)

    try:
        db.session.delete(user)
        db.session.commit()

        return{
            'message' : 'data user berhasil di hapus'
        }, 200
    except Exception as e:
        db.session.rollback()
        return {
            'message' : 'terjadi kesalahan saat delete user',
            'error' : str(e)
        }, 400
