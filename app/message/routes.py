from flask import Blueprint, request, jsonify
# from flask_jwt_extended import get_jwt_identity

from app.models.message import Message
from app.extensions import db

from cerberus import Validator
from app.message.validation import message_create_schema
from app.middleware.role_checker import role_required

from app.message.service import (
    get_all_messages_service,
    create_message_service
)

message_blueprint = Blueprint('message', __name__)

@message_blueprint.route('', methods=['GET'])
@role_required('member')
def get_messages():
    
    result = get_all_messages_service()
    return result


@message_blueprint.route('', methods=['POST'])
def create_message():

    data = request.json

    

    valid = Validator(message_create_schema)

    if not valid.validate(data):
        return {'error' : valid.errors}, 409
    
    result, status = create_message_service(data)

    return jsonify(result), status


    

