from functools import wraps
from flask_jwt_extended import current_user, jwt_required

def role_required(role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            # Auth logic
            # case, member and user is seperate role
            # print(f"DEBUG: Current User: {current_user.role}")
            # if current_user and current_user.role == role:

            #     return func(*args, **kwargs)
            # else:
            #     return {'message' : 'unauthorized'}, 403


            # case 2, member has more power than user
            
            # role yang member, di abisa akses semua
            if current_user.role == 'member':
                return func(*args, **kwargs)
                
            # role yang akses user, kalo require user, dia lolos
            elif role == 'user' and current_user.role == 'user':
                return func(*args, **kwargs)
            
            # role yang di akses, require admin, dia gagal
            else:
                return {'message' : 'unauthorized'}, 403

        return wrapper
    return decorator