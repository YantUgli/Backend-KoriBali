from cerberus import Validator



create_article_schema = {
    'title' : {
        'type' : 'string',
        'required' : True,
        'empty' : False,
        'maxlength' : 255
    },
    'description' : {
        'type' : 'string',
        'required' : True
    }
}

update_article_schema = {
    'title' : {
        'type' : 'string',
        'required' : True,
        'emtpy' : False,
        'maxlength' : 255
    },
    'description' : {
        'type' : 'string',
        'required' : False
    }
}


def validate(schema, data):
    v = Validator(schema)

    if not v.validate(data):
        return False, v.errors

    return True, None