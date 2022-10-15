import os
import jwt
from email_validator import validate_email, EmailNotValidError
from time import time
from firebase_admin import auth
from src.auth.auth_instance import AuthInstance


class SignUpSession1(AuthInstance):
    schema = {
        'firstName': "String",
        'lastName': "String",
        'email': "String"
    }

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

    def is_user_unique_by_email(self, email: str):
        try:
            email = email
            auth.get_user_by_email(email)
        except auth.UserNotFoundError:
            return True
        else:
            return False

    def post(self):
        # get JSON body content from request
        json_data = self.get_req_body

        # validate req body
        valid_req_body = self.validate_req_body(self.schema, json_data)

        if not valid_req_body:
            return self.get_invalid_schema_request_message()

        is_user_unique = self.is_user_unique_by_email(email=json_data['email'])

        if not is_user_unique:
            return {
                "message": "User already exists",
                "field": "email"
            }, 403

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

        # Hint: The mechanism of authentication is quite simple
        # instead of storing this state progress on server,
        # we just return a jwt token with all user's data.

        # The process below appends the user credentials to a jwt token:

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
