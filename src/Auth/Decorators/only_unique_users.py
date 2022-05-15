from functools import wraps
from firebase_admin import auth
from flask_restful import request

def only_unique_users(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        _ = function(*args, **kwargs)
        try:
            email = request.get_json()['email']
            auth.get_user_by_email(email)
        except auth.UserNotFoundError:
            pass
        else:
            return {
                "message": "User already exists",
                "field": "email"
            }, 403
        return _
    return wrapper