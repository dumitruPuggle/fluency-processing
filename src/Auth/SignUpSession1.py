import os
from flask_restful import Resource, request
import jwt
from email_validator import validate_email, EmailNotValidError

class SignUpSession1(Resource):
    def post(self):
        # get JSON body content from request
        json_data = request.get_json()
        
        # first session
        session1_credentials = {
            "firstName": json_data['firstName'],
            "lastName": json_data['lastName'],
            "email": json_data['email']
        }

        try:
            # Validate.
            validate_email(session1_credentials["email"])
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            return {
                "error": str(e),
                "field": "email"
            }, 403

        key = os.environ.get("JWT_SECRETS")
        encoded_credentials = jwt.encode({ **session1_credentials }, key, algorithm="HS256")
        return {
            "token": encoded_credentials,
            "message": "Please bring this token with you to the next session. Don't share it with anyone."
        }