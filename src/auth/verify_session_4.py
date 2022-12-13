import os
from flask_restful import Resource, request
import jwt
from password_validator import PasswordValidator
from src.auth.users.user import User
from src.auth.auth_instance import AuthInstance
from src.constant.constants_vars import user_types_generic, PHONE_PROVIDER
from firebase_admin import _auth_utils
from lang.translate import Translate


class VerifyAccountSession4(AuthInstance):
    schema = {
        'password': "String"
    }
    
    def __init__(self):        
        self.json_data = self.get_req_body
        self.lang = self.get_lang_from_previous_session
        self.translate = Translate(self.lang)
    
    def post(self):
        # get JSON body content from request
        json_data = self.get_req_body
        

        # get .env variables
        jwt_key = os.environ.get("SMS_JWT_KEY")

        # validate req body
        valid_req_body = self.validate_req_body(self.schema, json_data)

        if not valid_req_body:
            return self.get_invalid_schema_request_message()

        password = json_data['password']

        try:
            payload = jwt.decode(self.get_temp_token, jwt_key, algorithms=['HS256'])['payload']
        except jwt.exceptions.InvalidSignatureError:
            return {
                "message": self.translate.t('invalid_token'),
                "field": "token"
            }, 403
        except jwt.exceptions.ExpiredSignatureError:
            return {
                "message": self.translate.t('token_expired'),
                "field": "token"
            }, 403
        except Exception:
            return {"message": self.translate.t('internal_server_error')}, 500


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
                "message": self.translate.t('passwordIsNotValid'),
                "field": "password"
            }, 400

        # create user
        INFLUENCER = user_types_generic[3]
        AGENCY = user_types_generic[2]
        ENTREPRENEUR = user_types_generic[1]
        MARKETER = user_types_generic[0]
        try:
            auth_instance = User(
                provider_type=payload.get('provider'), 
                verified=payload.get('verified'), 
                firstName=payload.get('firstName'), 
                lastName=payload.get('lastName'), 
                email=payload.get('email'), 
                phone_number=payload.get('phoneNumber', None)
            )
        except Exception as e:
            print(e)
            return {
                "message": self.translate.t('internal_server_error'),
                "field": "request"
            }, 400
        else:
            if payload.get('verify_existing_account', False) is False:
                try:
                    auth_instance.create_user(password)
                except _auth_utils.EmailAlreadyExistsError:
                    return {
                        "message": self.translate.t('this_user_has_been_already_created'),
                        "field": "request"
                    }, 400
                except Exception as e:
                    print(e)
                    return {
                        "message": self.translate.t('internal_server_error'),
                        "field": "request"
                    }, 400
            elif payload.get('verify_existing_account', False) is True:
                try:
                    auth_instance.update_user(
                        uid=payload.get('verify_account_uid'), 
                        password=password
                    )
                except _auth_utils.EmailAlreadyExistsError:
                    return {
                        "message": self.translate.t('this_user_has_been_already_created'),
                        "field": "request"
                    }, 400
                except Exception as e:
                    print(e)
                    return {
                        "message": self.translate.t('internal_server_error'),
                        "field": "request"
                    }, 400
                    
            return {"message": self.translate.t('success_user_has_been_created_sign_in_with_sdk')}, 200
