from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extention import db
from app.models.user import User


auth_blueprint = Blueprint('auth', __name__)

# Register
@auth_blueprint.route('/register', methods=['POST'])
def register():

    data = request.get_json()
    # print(data)

    username = data.get('username')
    email =  data.get('email')
    password = data.get('password')
    number_phone = data.get('number_phone')

    if not email:
        return jsonify({
            'message' : 'email is required'
        })
    
    if not number_phone:
        return jsonify({
            'message' : 'number phone is required'
        })

    existing_user = User.query.filter(
        (User.email==email) | (User.number_phone == number_phone)
        ).first()

    # print(existing_user)

    if existing_user:
        return jsonify({
            'message': 'Email or Number Phone already registered'
        }), 400
    
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


    return jsonify({
        'message' : 'User created',
        # 'access_token' : access_token
    }), 201

# Login
@auth_blueprint.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    print(data)
    email = data.get('email')
    password = data.get('password')

    # print(password)
    user = User.query.filter_by(email=email).first()
    # print('ini user', user)
    
    if not user or not user.check_password(password):
        return jsonify({
            'message' : 'Invalid Credential'
        }), 401
    
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'access_token': access_token
    }) 

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