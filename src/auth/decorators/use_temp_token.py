from functools import wraps
from firebase_admin import auth
from flask_restful import request

def use_temp_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        _ = function(*args, **kwargs)
        temp_token = request.headers.get('_temptoken')
        if temp_token is None or temp_token == "":
            return {
                "message": "No token provided",
                "field": "token"
            }, 403
    return wrapper