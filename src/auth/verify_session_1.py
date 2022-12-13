import os
import jwt
from email_validator import validate_email, EmailNotValidError
from time import time
from firebase_admin import auth
from src.auth.auth_instance import AuthInstance
from src.constant.constants_vars import user_types, user_types_generic
from src.auth.users.user import User
from src.constant.constants_vars import DEFAULT_LANGUAGE
from lang.translate import Translate


class VerifyAccountSession1(AuthInstance):
    schema = {
        'lang': 'String',
        'verifyExistingAccount': False,
        'firstName': 'String',
        'lastName': 'String',
        'email': 'String'
    }
    
    def __init__(self):
        self.json_data = self.get_req_body
        self.lang = self.json_data.get('lang', DEFAULT_LANGUAGE)
        self.translate = Translate(self.lang)

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
        # validate req body
        valid_req_body = self.validate_req_body(self.schema, self.json_data)

        if not valid_req_body:
            return self.get_invalid_schema_request_message()
        
        verify_existing_account = self.json_data.get('verifyExistingAccount', False)
        is_user_unique = self.is_user_unique_by_email(email=self.json_data['email'])

        if verify_existing_account is True:
            # validate is the account is existing
            if is_user_unique:
                return {
                    "message": self.translate.t('account_does_not_exist'),
                    "field": "email"
                }, 403
            # validate if the account is indeed not verified
            is_user_valid = User.validate(self.json_data.get('email'))
            if is_user_valid:
                return {
                    "message": f"{self.translate.t('account_already_verified')} (204)",
                    "field": "email"
                }, 403
            if not is_user_valid:
                user_uid = auth.get_user_by_email(self.json_data.get('email')).uid
        elif verify_existing_account is False:
            if not is_user_unique:
                return {
                    "message": self.translate.t("account_already_exists"),
                    "field": "email"
                }, 403

        # first session
        raw_session_credentials = {
            "lang": self.json_data['lang'],
            "verify_existing_account": self.json_data['verifyExistingAccount'],
            "firstName": self.json_data['firstName'],
            "lastName": self.json_data['lastName'],
            "email": self.json_data['email']
        }

        email_valid, exception = self.check_email(
            email=raw_session_credentials["email"]
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
        
        session1_credentials = {
            **raw_session_credentials
        }
        
        try:
            if user_uid is not None:
                session1_credentials['verify_account_uid'] = user_uid
        except Exception as e:
            print(e)
        
        encoded_success, encoded_credentials, exception = self.encode_credentials_in_session(
            credentials=session1_credentials,
            expiration=3600
        )

        if not encoded_success:
            return {
               "message": self.translate.t('internal_server_error'),
               "field": None
            }, 500

        return {
            "token": encoded_credentials,
            "message": self.translate.t('success_please_bring_this_token_with_you')
        }, 200
