import os
from flask_restful import Resource, request
import jwt
from src.auth.encryption.encrypt import Encrypto
from time import time

# from src.Auth.Decorators.use_temp_token import use_temp_token


class SignUpSession3(Resource):
    # @use_temp_token
    def post(self):
        # get JSON body content from request
        json_data = request.get_json()

        # code provided by user
        input_code = json_data["code"]

        # get .env variables
        jwt_key = os.environ.get("SMS_JWT_KEY")
        code_encryption_key = os.environ.get("SMS_CODE_ENCRYPTION_KEY")

        # get token from header
        temp_token = request.headers.get('_temptoken')

        if temp_token == None or len(temp_token) == 0:
            return {"message": "No token provided", "field": "token"}, 403

        try:
            decoded_token = jwt.decode(temp_token, jwt_key, algorithms=['HS256'])
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
            return {"message": "Token decoding failed, please enter an valid token"}, 500
        else:
            encrypto = Encrypto()
            try:
                real_code = encrypto.decrypt(decoded_token['code'], code_encryption_key)
                if real_code != input_code:
                    return {
                        "message": "Invalid code"
                    }, 400
            except Exception:
                return {"message": "Internal server error"}, 500

        return {
            "message": "Success. Your account was verified.",
            "token": jwt.encode(
                {
                    "payload": decoded_token['payload'],
                    "exp": time() + 3600,
                    "verified": True
                },
                jwt_key,
                algorithm='HS256'
            )
        }, 200
