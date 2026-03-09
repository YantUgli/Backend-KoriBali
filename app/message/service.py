from app.extensions import db
from app.models.message import Message

from cerberus import Validator

def get_all_messages_service():
    
    messages = Message.query.all()

    output = []

    for m in messages:
        data = m.to_dict()
        output.append(data)

    return output


def create_message_service(data):
    name = data.get('name')
    email = data.get('email')
    number_phone = data.get('number_phone')
    message = data.get('message')

    request_body= Message(
        name = name,
        email = email,
        number_phone = number_phone,
        message = message
    )

    print(data)
    try:
        db.session.add(request_body)
        db.session.commit()
        return {
            'message' : 'create message successfully',
            "data" : request_body.to_dict()
        }, 201
                
    except Exception as e:
        db.session.rollback()
        return {
            'message' : 'terjadi kesalahan saat menyimpan data',
            'error' : str(e)
        }, 400