import os
from flask_restful import Resource, request
import jwt
from src.Auth.PasswordService import PasswordService, PasswordTooShortException, PasswordContainsBannedWordException, PasswordDoesNotContainNumberException, PasswordDoesNotContainUpperCaseException, PasswordDoesNotContainLowerCaseException


class SignUpSession4(Resource):
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
        try:
            banned_words = [payload['email'], payload['firstName'], payload['lastName']]
            PasswordService(password, banned_words).validate()
        except PasswordTooShortException:
            return {
                "message": "Password too short",
                "field": "password"
            }, 400

        except PasswordContainsBannedWordException:
            return {
                "message": "Password contains banned word",
                "field": "password"
            }, 400
        
        except PasswordDoesNotContainNumberException:
            return {
                "message": "Password must contain at least one number",
                "field": "password"
            }, 400

        except PasswordDoesNotContainUpperCaseException:
            return {
                "message": "Password must contain at least one uppercase letter",
                "field": "password"
            }, 400

        # TODO create the user.
        
        
        return {"message": "User has been successfully created"}, 200
