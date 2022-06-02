import os
from flask_restful import Resource, request
import jwt
from firebase_admin import auth
from password_validator import PasswordValidator

from src.Auth.Decorators.use_temp_token import use_temp_token


class SignUpSession4(Resource):
    # @use_temp_token
    def post(self):
        # get JSON body content from request
        json_data = request.get_json()

        password = json_data['password']

        # get .env variables
        jwt_key = os.environ.get("SMS_JWT_KEY")

        # get token from header
        temp_token = request.headers.get('_temptoken')

        try:
            payload = jwt.decode(temp_token, jwt_key, algorithms=['HS256'])['payload']
        except jwt.exceptions.InvalidSignatureError:
            return {
                "message": "Invalid token",
                "field": "token"
            }, 403
        except jwt.exceptions.ExpiredSignatureError:
            return {
                "message": "Token expired",
                "field": "token"
            }, 403
        except Exception:
            return {"message": "Internal server error"}, 500


        # validate the password
        schema = PasswordValidator()

        schema\
            .min(8)\
            .max(100)\
            .has().uppercase()\
            .has().lowercase()\
            .has().digits()\
            .has().no().spaces()\

        isNotValid = schema.validate(password) is False
        if isNotValid:
            return {
                "message": "Password is not valid",
                "field": "password"
            }, 400

        # create user
        auth.create_user(
            email=payload['email'],
            email_verified=False,
            phone_number=payload['phoneNumber'],
            password=password,
            photo_url="https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?crop=entropy&cs=tinysrgb&fm=jpg&ixlib=rb-1.2.1&q=80&raw_url=true&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dmlld3xlbnwwfHwwfHw%3D&w=1000",
            display_name=payload['firstName'] + " " + payload['lastName'],
            disabled=False)


        return {"message": "User has been successfully created"}, 200
