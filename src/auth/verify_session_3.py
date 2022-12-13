import json
import os
import jwt

from src.auth.auth_instance import AuthInstance
from src.auth.encryption.encrypt import Encrypto
from time import time
from lang.translate import Translate

# from src.Auth.Decorators.use_temp_token import use_temp_token


class VerifyAccountSession3(AuthInstance):
    schema = {
        'code': 'String'
    }
    
    def __init__(self):
        self.json_data = self.get_req_body
        self.lang = self.get_lang_from_previous_session
        self.translate = Translate(self.lang)
    
    def post(self):        

        # validate req body
        valid_req_body = self.validate_req_body(self.schema, self.json_data)

        if not valid_req_body:
            return self.get_invalid_schema_request_message()

        # code provided by user
        input_code = self.json_data["code"]

        # get .env variables
        jwt_key = os.environ.get("SMS_JWT_KEY")
        code_encryption_key = os.environ.get("SMS_CODE_ENCRYPTION_KEY")

        # get token from header
        temp_token = self.get_temp_token

        # check temptoken
        temptoken_persists = self.check_temptoken()
        if not temptoken_persists:
            return self.get_no_temp_token_header_exception


        try:
            decoded_token = jwt.decode(temp_token, jwt_key, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            return {
                "message": self.translate.t("invalid_token"),
                "field": "token"
            }, 403
        except jwt.exceptions.ExpiredSignatureError:
            return {
                "message": self.translate.t("token_expired"),
                "field": "token"
            }, 403
        except Exception:
            return {"message": self.translate.t("token_decoding_failed")}, 500
        else:
            encrypto = Encrypto()
            try:
                real_code = encrypto.decrypt(decoded_token['code'], code_encryption_key)
                if str(real_code) != str(input_code):
                    return {
                        "message": self.translate.t("invalid_code")
                    }, 400
            except Exception:
                return {"message": self.translate.t("internal_server_error")}, 500

        return {
            "message": self.translate.t("success_the_provider_has_been_verified"),
            "token": jwt.encode(
                {
                    "payload": {
                        **decoded_token['payload'],
                        "verified": True
                    },
                    "exp": time() + 3600,
                },
                jwt_key,
                algorithm='HS256'
            )
        }, 200
