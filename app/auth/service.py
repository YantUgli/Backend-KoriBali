from app.extensions import db
from app.user.models import User
from flask_jwt_extended import create_access_token


def register_service(data):

    username = data.get('username')
    email =  data.get('email')
    password = data.get('password')
    number_phone = data.get('number_phone')

    if not email:
        return {
            'message' : 'email is required'
        }
    
    if not number_phone:
        return {
            'message' : 'number phone is required'
        }

    existing_user = User.query.filter(
        (User.email==email) | (User.number_phone == number_phone)
        ).first()

    # print(existing_user)

    if existing_user:
        return {
            'message': 'Email or Number Phone already registered'
        }, 400
    
    user = User(
        username = username,
        email = email,
        number_phone = number_phone
    )

    user.set_password(password)
    # print(user)
    db.session.add(user)
    db.session.commit()

    # After Register langsung login
    access_token = create_access_token(identity=str(user.id))

    return {
        'message' : 'User created',
        # 'access_token' : access_token
    }, 201



def login_service(data):
    print(data)
    email = data.get('email')
    password = data.get('password')

    # print(password)
    user = User.query.filter_by(email=email).first()
    # print('ini user', user)
    
    if not user or not user.check_password(password):
        return {
            'message' : 'Invalid Credential'
        }, 401
    
    access_token = create_access_token(identity=str(user.id))

    return {
        'access_token': access_token
    }, 200
