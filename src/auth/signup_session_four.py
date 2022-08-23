import os
from flask_restful import Resource, request
import jwt
from password_validator import PasswordValidator
from src.auth.creator import Creator

# from src.auth.decorators.use_temp_token import use_temp_token


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

        # insert creator into firestore
        creator = Creator(
            firstName=payload['firstName'], 
            lastName=payload['lastName'], 
            email=payload['email'], 
            phoneNumber=payload['phoneNumber']
        )

        creator.create_user(password)
        creator.insert_user_firestore()

        # create a new token
        new_token = creator.create_token()

        return {"message": "User has been successfully created", "token": new_token}, 200
