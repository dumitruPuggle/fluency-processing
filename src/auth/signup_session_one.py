import os
from flask_restful import Resource, request
import jwt
from email_validator import validate_email, EmailNotValidError
from time import time
from src.auth.decorators.only_unique_users import only_unique_users


class SignUpSession1(Resource):

    def check_email(self, email: str):
        try:
            validate_email(email)
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            return False, str(e)
        else:
            return True, None

    def encode_credentials_in_session(self, credentials: dict, expiration: int):
        key = os.environ.get("JWT_SECRET_KEY")
        data = {
            "payload": credentials,
            "exp": time() + expiration
        }
        try:
            encoded = jwt.encode(data, key, algorithm="HS256")
        except Exception as e:
            return False, None, e
        else:
            return True, encoded, None

    @only_unique_users
    def post(self):
        # get JSON body content from request
        json_data = request.get_json()

        # first session
        session1_credentials = {
            "firstName": json_data['firstName'],
            "lastName": json_data['lastName'],
            "email": json_data['email']
        }

        email_valid, exception = self.check_email(
            email=session1_credentials["email"]
        )

        if not email_valid:
            return {
                "message": exception,
                "field": "email"
            }, 403

        encoded_success, encoded_credentials, exception = self.encode_credentials_in_session(
            credentials=session1_credentials,
            expiration=3600
        )

        if not encoded_success:
            return {
                "message": "Internal server error",
                "field": None
            }, 500

        return {
            "token": encoded_credentials,
            "message": "Please bring this token with you to the next session. Don't share it with anyone."
        }, 200
